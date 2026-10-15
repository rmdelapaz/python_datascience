# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import OFFLINE, fixtures

# %% [markdown]
# # Lab 6.5-A · Thirteen requests, ten allowed (SOLUTION)
# Question: the merchandising team wants a stock check: for each of the nine categories, how
# many products are out of stock or running low? And four SKUs that customers asked about:
# are they in stock? That is thirteen requests to a server that allows ten every five seconds.
# Send them three ways and compare: all at once, with plan B (obey Retry-After), with plan A
# (a steady pace).
#
# Practices: the X-RateLimit headers, a polite interval, 429 and Retry-After with a default
# and a bound, a Throttle, and telling a refusal you should retry (429) from an answer you
# should not (404).
#
# Two modes, one function (make_http):
#   online  : the practice API on your own computer. Start it first, in a second terminal:
#                 python data/mock_api.py --rate 10 --per 5
#   offline : LABS_OFFLINE=1 -> saved responses in labs/module-18/_fixtures/, no network, and
#             a pretend clock, so the waits in this lab take no real time.
#   Online this lab really waits: allow about half a minute.

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

# %% The job: thirteen requests (done for you)
CATEGORIES = ["Tents", "Sleeping", "Packs", "Footwear", "Apparel", "Climbing", "Camp Kitchen", "Snow", "Accessories"]
SKUS = ["SNW-1007", "TNT-1020", "PCK-1015", "KIT-1027"]
JOBS = ([("/products", {"category": c, "per_page": 100}) for c in CATEGORIES]
        + [(f"/products/{sku}", None) for sku in SKUS])

# %% Step 1: read the allowance, and choose a pace
fresh_window()
r = http.get(f"{API}/products", params={"per_page": 1}, timeout=10)
print("1.", r.status_code, {k: v for k, v in r.headers.items() if k.startswith("X-RateLimit")})
interval = PER / LIMIT * 1.1                     # the allowance, plus a 10% margin
print(f"   a polite pace: one request every {interval:.2f} s, so {len(JOBS)} requests take about {(len(JOBS) - 1) * interval:.0f} s")

# %% Step 2: all at once (the wrong way, on purpose)
fresh_window()
burst = [http.get(f"{API}{path}", params=params, timeout=10) for path, params in JOBS]
statuses = [r.status_code for r in burst]
print("2. burst: ", statuses)
last = burst[-1]
wait = float(last.headers.get("Retry-After", 1))  # a default: not every 429 carries the header
print(f"   answered {len(JOBS) - statuses.count(429)} of {len(JOBS)}, refused {statuses.count(429)} | Retry-After: {wait:.0f} s")
print("   the server said:", last.json()["error"]["message"])


# %% Step 3: plan B, obey the 429
def get_polite(url, max_tries=4, **kwargs):
    """GET; on 429 wait as long as Retry-After asks, then try again. Returns (response, waits)."""
    kwargs.setdefault("timeout", 10)
    for attempt in range(1, max_tries + 1):
        resp = http.get(url, **kwargs)
        if resp.status_code != 429 or attempt == max_tries:
            return resp, attempt - 1
        clock.sleep(float(resp.headers.get("Retry-After", 1)))


fresh_window()
started = clock.monotonic()
polite = [get_polite(f"{API}{path}", params=params) for path, params in JOBS]
statuses = [r.status_code for r, waits in polite]
print("3. plan B:", statuses)
print(f"   refused in the end: {statuses.count(429)} | waits: {sum(waits for r, waits in polite)} | took about {clock.monotonic() - started:.0f} s")

# %% Step 4: plan A, a steady pace
fresh_window()
throttle = Throttle(interval)
started = clock.monotonic()
paced = []
for path, params in JOBS:
    throttle.wait()
    paced.append(http.get(f"{API}{path}", params=params, timeout=10))
statuses = [r.status_code for r in paced]
print("4. plan A:", statuses)
print(f"   refused: {statuses.count(429)} | took about {clock.monotonic() - started:.0f} s")

# %% Step 5: the stock check itself, from the responses of step 4
rows = []
for (path, params), r in zip(JOBS[:len(CATEGORIES)], paced):
    if r.ok:
        items = pd.DataFrame(r.json()["items"])
        rows.append({"category": params["category"], "products": len(items),
                     "out_of_stock": int((items["stock_status"] == "out_of_stock").sum()),
                     "low_stock": int((items["stock_status"] == "low_stock").sum())})
print(f"5. {len(rows)} of {len(CATEGORIES)} categories answered")
if rows:
    stock = pd.DataFrame(rows).sort_values(["out_of_stock", "low_stock"], ascending=False)
    print(stock.to_string(index=False))
for sku, r in zip(SKUS, paced[len(CATEGORIES):]):
    answer = r.json()
    print(f"   {sku}: {r.status_code}", answer.get("stock_status") or answer["error"]["message"])
print("   The two 404s were each asked once in steps 3 and 4: a product that does not exist")
print("   will not exist in five seconds either. Only the 429 earned a second try.")
