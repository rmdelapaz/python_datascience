# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import OUTPUT, OFFLINE, fixtures

# %% [markdown]
# # Lab 6.5-B · Retry what is temporary, cache what you have (SOLUTION)
# Question: the pricing team wants the median list price of three categories (Climbing,
# Packs, Sleeping), and you will ask for them six times while you work. How many requests
# does that really need? On the way: an endpoint that fails twice before it answers, and a
# product that is not there at all.
#
# Practices: exponential backoff with a cap and jitter, a retry function that obeys
# Retry-After and knows what NOT to retry, urllib3's Retry policy, and a disk cache that
# checks before it writes.
#
# Two modes, one function (make_http):
#   online  : the practice API on your own computer. Start it first, in a second terminal:
#                 python data/mock_api.py --rate 10 --per 5
#   offline : LABS_OFFLINE=1 -> saved responses in labs/module-18/_fixtures/, no network, and
#             a pretend clock, so the waits in this lab take no real time.
#   (The default limit works too.) Every request in this lab passes through a Throttle:
#   pacing is plan A, the retries are plan B.

# %% Setup (done for you): one Session for every request, and a clock
import json
import math
import os
import re
import time
from urllib.parse import parse_qsl, urlsplit

import pandas as pd
import requests

API = os.environ.get("PINECREST_API", "http://127.0.0.1:8000")
USER_AGENT = "pinecrest-course-bot/1.0 (learning project; contact: you@example.com)"


class SavedApi(requests.adapters.BaseAdapter):
    """OFFLINE stand-in for the practice API. You do not need to read this to do the lab.

    It answers from _fixtures/ (responses saved from the real practice API) and applies the
    server's own rules for keys, tokens and the rate limit on a pretend clock, so nothing
    touches the network and nobody really waits."""

    def __init__(self, root):
        super().__init__()
        self.folder, self.root = fixtures(__file__), root
        self.t, self.window, self.tokens, self.flaky = 0.0, (0.0, 0), {}, 0
        limit, per = re.findall(r"[\d.]+", json.loads(self.load(root)[1])["rate_limit"])[:2]
        self.limit, self.per = int(limit), float(per)

    def monotonic(self):                      # the pretend clock: clock.monotonic(), clock.sleep()
        return self.t

    def sleep(self, seconds):
        self.t += max(0.0, seconds)

    def load(self, name):
        body = self.folder / (name + ".json")
        if not body.is_file():
            raise requests.exceptions.ConnectionError(f"offline: no saved response named {body.name} in _fixtures/")
        meta = json.loads((self.folder / (body.name + ".meta.json")).read_text(encoding="utf-8"))
        return meta, body.read_bytes()

    def send(self, request, **kwargs):
        parts, sent, extra = urlsplit(request.url), request.headers, {}
        path = parts.path.rstrip("/") or "/"
        query = "".join(f" {k}-{v}" for k, v in sorted(parse_qsl(parts.query)))
        name = re.sub(r"[^A-Za-z0-9.-]+", "_", path + query).strip("_")
        if path in ("/", "/health"):          # these two are not rate limited
            name = self.root if path == "/" else "health"
        else:
            start, count = self.window if self.t - self.window[0] < self.per else (self.t, 0)
            self.window = (start, count + 1)
            left = math.ceil(self.per - (self.t - start))
            extra = {"X-RateLimit-Limit": str(self.limit), "X-RateLimit-Reset": str(left),
                     "X-RateLimit-Remaining": str(max(0, self.limit - count - 1))}
            if count + 1 > self.limit:
                name, extra["Retry-After"] = "rate_limited", str(max(1, left))
            elif path == "/orders" and sent.get("X-API-Key") != os.environ.get("PINECREST_API_KEY", "?"):
                name = "orders_bad_key" if sent.get("X-API-Key") else "orders_no_key"
            elif path == "/login":
                good = {"username": os.environ.get("PINECREST_USER"), "password": os.environ.get("PINECREST_PASSWORD")}
                try:
                    name = "login" if json.loads(request.body or b"{}") == good else "login_bad_password"
                except ValueError:
                    name = "login_not_json"
            elif path == "/me":
                auth = sent.get("Authorization", "")
                token = auth[7:] if auth.startswith("Bearer ") else None
                if token is None:
                    name = "me_no_token"
                elif token not in self.tokens:
                    name = "me_bad_token"
                elif self.t >= self.tokens[token]:
                    name = "me_expired"
            elif path == "/flaky":
                self.flaky += 1
                name = "flaky_ok" if self.flaky % 3 == 0 else "flaky_503"
        meta, content = self.load(name)
        resp = requests.Response()
        resp.status_code, resp.reason, resp.url, resp.request = meta["status"], meta["reason"], request.url, request
        resp.headers.update({**meta["headers"], **extra})
        resp._content = content
        resp.encoding = requests.utils.get_encoding_from_headers(resp.headers)
        if name == "login":
            self.tokens[resp.json()["access_token"]] = self.t + resp.json()["expires_in"]
        return resp

    def close(self):
        pass


def make_http(root="root_rate-10_per-5"):
    """The ONE place that decides where requests go. Returns (session, clock)."""
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    if not OFFLINE:
        return session, time                  # the real practice API and the real clock
    saved = SavedApi(root)
    session.mount("http://", saved)
    session.mount("https://", saved)
    return session, saved                     # saved responses and a pretend clock


http, clock = make_http()
print("mode:", "offline (saved responses in _fixtures/; waits run on a pretend clock, so they take no real time)"
      if OFFLINE else f"online ({API})")


def require_env(name):
    """Read a required setting from the environment, or stop with a clear message."""
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Set the environment variable {name} before running this code.")
    return value


class ApiError(Exception):
    """An error response from the API, with its status, code and message (Lesson 6.4)."""

    def __init__(self, status, code, message):
        super().__init__(f"{status} {code}: {message}")
        self.status, self.code, self.message = status, code, message


def check(resp):
    """Return the response if it succeeded. Otherwise raise ApiError."""
    if resp.ok:
        return resp
    try:
        error = resp.json()["error"]
        code, message = error["code"], error["message"]
    except (requests.exceptions.JSONDecodeError, KeyError, TypeError):
        code, message = "http_error", resp.reason
    raise ApiError(resp.status_code, code, message)


rate_text = http.get(f"{API}/", timeout=10).json()["rate_limit"]       # "/" is not rate limited
LIMIT, PER = int(re.findall(r"[\d.]+", rate_text)[0]), float(re.findall(r"[\d.]+", rate_text)[1])
print("this server allows:", rate_text)
if LIMIT > 10:
    print("  NOTE: this lab is written for a tight limit. Stop the API (Ctrl+C) and start it with:")
    print("        python data/mock_api.py --rate 10 --per 5")


def fresh_window():
    """Wait out the current rate-limit window, so that a step starts from zero."""
    clock.sleep(PER)


class Throttle:
    """Keep calls at least `interval` seconds apart (Lesson 6.5, with `clock` in place of `time`)."""

    def __init__(self, interval):
        self.interval = interval
        self.last = None

    def wait(self):
        if self.last is not None:
            remaining = self.interval - (clock.monotonic() - self.last)
            if remaining > 0:
                clock.sleep(remaining)
        self.last = clock.monotonic()


throttle = Throttle(PER / LIMIT * 1.1)


def paced_get(url, **kwargs):
    """http.get at a polite pace, with a timeout."""
    kwargs.setdefault("timeout", 10)
    throttle.wait()
    return http.get(url, **kwargs)


# Put /flaky at the start of its fail, fail, succeed cycle, whatever ran before this lab.
for _ in range(3):
    if paced_get(f"{API}/flaky").ok:
        break

# %% Step 1: a backoff schedule with a ceiling, then with jitter
import hashlib
import random
import shutil

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def backoff_delay(attempt, base=0.25, cap=3.0):
    """Seconds to wait after failed attempt number `attempt` (counting from 0)."""
    return min(cap, base * 2 ** attempt)


print("1. schedule:   ", [backoff_delay(n) for n in range(6)])
rng = random.Random(7)                           # seeded only so that every screen shows the same numbers
print("   with jitter:", [round(rng.uniform(0, backoff_delay(n)), 2) for n in range(6)])

# %% Step 2: meet the flaky endpoint (three plain requests)
seen = [paced_get(f"{API}/flaky") for _ in range(3)]
print("2. /flaky:", [r.status_code for r in seen], "| Retry-After on the first:", seen[0].headers.get("Retry-After"))

# %% Step 3: one function that decides whether a retry can help
RETRY_STATUSES = {429, 500, 502, 503, 504}


def get_with_backoff(url, max_tries=5, **kwargs):
    """GET with retries. Returns (response, tries used). Raises RuntimeError when the tries run out."""
    for attempt in range(max_tries):
        resp = paced_get(url, **kwargs)
        if resp.status_code not in RETRY_STATUSES:
            return resp, attempt + 1             # success, or an error a retry cannot fix
        if attempt == max_tries - 1:
            break
        asked = resp.headers.get("Retry-After")
        delay = float(asked) if asked else random.uniform(0, backoff_delay(attempt))
        clock.sleep(delay)                       # the server's instruction beats our own guess
    raise RuntimeError(f"gave up after {max_tries} tries (last status: {resp.status_code})")


resp, tries = get_with_backoff(f"{API}/flaky")
print("3. /flaky:", resp.status_code, resp.json(), "| tries:", tries)
resp, tries = get_with_backoff(f"{API}/products/SNW-1007")
print("   /products/SNW-1007:", resp.status_code, resp.json()["error"]["code"], "| tries:", tries)
try:
    get_with_backoff(f"{API}/flaky", max_tries=2)
except RuntimeError as err:
    print("   with max_tries=2:", err)
paced_get(f"{API}/flaky")                        # the third request of that cycle, so the next step starts clean

# %% Step 4: the same policy from urllib3. Ask it what it would do.
policy = Retry(total=4, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504],
               allowed_methods=["GET", "HEAD"], respect_retry_after_header=True)
print("4. would the policy retry?")
for method, status in [("GET", 503), ("GET", 429), ("GET", 404), ("GET", 401), ("POST", 503)]:
    print(f"   {method:<4} {status}: {policy.is_retry(method, status)}")
if OFFLINE:
    print("   offline: a mounted Retry policy needs the real practice API, so this step is skipped.")
    print("   Online it prints: 200 after retrying [503, 503]")
elif policy is not None:
    with requests.Session() as retrying:
        retrying.mount("http://", HTTPAdapter(max_retries=policy))
        retrying.headers["User-Agent"] = USER_AGENT
        throttle.wait()
        resp = retrying.get(f"{API}/flaky", timeout=10)
        print("  ", resp.status_code, "after retrying", [a.status for a in resp.raw.retries.history])

# %% Step 5: a cache that checks before it writes
CACHE_DIR = OUTPUT / "cache"
shutil.rmtree(CACHE_DIR, ignore_errors=True)     # start cold, so that every run of this lab prints the same


def cache_path(url, params=None):
    key = url + "?" + json.dumps(params or {}, sort_keys=True)
    return CACHE_DIR / (hashlib.sha256(key.encode("utf-8")).hexdigest()[:16] + ".json")


def cached_get_json(url, params=None):
    """Return (data, source). Reads the cache when it can; asks the network when it must."""
    path = cache_path(url, params)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8")), "cache"
    resp = check(paced_get(url, params=params))  # check FIRST: an error is never saved
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(resp.text, encoding="utf-8")
    return resp.json(), "network"


asked = ["Climbing", "Packs", "Sleeping", "Packs", "Climbing", "Packs"]
sources, frames = [], {}
for category in asked:
    data, source = cached_get_json(f"{API}/products", {"category": category, "per_page": 100})
    sources.append(source)
    frames[category] = pd.DataFrame(data["items"])
print("5. asked", len(asked), "times:", sources)
print(f"   {sources.count('network')} requests sent, {sources.count('cache')} answers from the cache,",
      len(list(CACHE_DIR.glob("*.json"))), "files in the cache")
try:
    cached_get_json(f"{API}/products/SNW-1007")
except ApiError as err:
    print("   a 404 is raised, not saved:", err.status, err.code, "| files in the cache:", len(list(CACHE_DIR.glob("*.json"))))

# %% Step 6: the answer
prices = pd.concat(frames.values(), ignore_index=True)
summary = (prices.groupby("category")["price"].agg(products="count", median_price="median")
           .sort_values("median_price", ascending=False))
print("6. median list price:")
print(summary.to_string())
print("   Six questions, three requests. Run the lab again without the rmtree line and it needs none.")
