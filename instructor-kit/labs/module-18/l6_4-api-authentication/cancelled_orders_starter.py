# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OFFLINE, fixtures

# %% [markdown]
# # Lab 6.4-A · The cancellations report (STARTER)
# Question: how many orders were cancelled in the last quarter of 2025 (since 2025-10-01),
# what were they worth, and where were they placed? The orders endpoint is protected: it
# wants an API key in the X-API-Key header.
#
# Practices: a key read from the environment (and never printed whole), 401 versus 403,
# ApiError and check(), asking for the size of a job first, following `next` to the last
# page, and checking the pull against a source you trust.
#
# Two modes, one function (make_http):
#   online  : the practice API on your own computer. Start it first, in a second terminal:
#                 python data/mock_api.py --token-ttl 5
#   offline : LABS_OFFLINE=1 -> saved responses in labs/module-18/_fixtures/, no network, and
#             a pretend clock, so the waits in this lab take no real time.
#   The key is read from the environment variable PINECREST_API_KEY (see the workbook for
#   the command that sets it in your terminal). It is never typed into this file.
#
# Expected when you finish: a hint of the key (never the whole key), 401 and 403 with their
# codes, the size of the job (70 orders, 3 requests), a 70-row DataFrame that matches the
# promised total, a four-row table by store, the API's own message for a badly written
# date, and a check against orders.csv that says True twice.

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


def make_http(root="root"):
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

# %% Step 1: the key comes from the environment, and only a hint of it is printed
# TODO 1a: read the key with require_env("PINECREST_API_KEY") instead of the empty string.
API_KEY = ""
# TODO 1b: print a HINT of the key: its first four characters, "...", and its length.
print("1. key loaded:", "TODO 1b")
# TODO 1c: put the key in the dictionary below under the header name the API asks for.
#          (Run the lab as it is first: step 2 prints the name of the header.)
KEY = {}                                         # sent with a request as headers=KEY
FILTERS = {"status": "cancelled", "since": "2025-10-01"}

# %% Step 2: two knocks that must fail, and what each failure means
# Predict the status of each before you run this cell. It is complete: nothing to change.
for label, headers in [("no key", {}), ("a key with a typo", {"X-API-Key": API_KEY[:-1] + "x"})]:
    r = http.get(f"{API}/orders", headers=headers, params={"per_page": 1}, timeout=10)
    print(f"2. {label}: {r.status_code} {r.json().get('error', {}).get('code', 'ok')} | {r.json().get('error', {}).get('message', '')}")

# %% Step 3: ask how big the job is before pulling it
PER_PAGE = 25
total = None
try:
    probe = check(http.get(f"{API}/orders", headers=KEY, params={**FILTERS, "per_page": 1}, timeout=10)).json()
    # TODO 3: read the total from `probe`, then print how many requests the job needs at
    #         PER_PAGE orders per page.  Rounding up without a library:  -(-total // PER_PAGE)
    print("3. keys in the answer:", list(probe))
except ApiError as err:
    print("3. not yet:", err, "(finish TODO 1)")


# %% Step 4: follow `next` to the last page
def get_all(path, params):
    """Every item of a paginated endpoint, and the number of pages it took."""
    items, pages = [], 0
    url = f"{API}{path}"
    data = check(http.get(url, headers=KEY, params=params, timeout=10)).json()
    items.extend(data["items"])
    pages += 1
    # TODO 4: this reads ONE page. Turn it into a loop that keeps going while there is a
    #         `next` address:   url = f"{API}{data['next']}" if data["next"] else None
    #         and set params = None after the first request (`next` already carries the filters).
    return items, pages


try:
    items, pages = get_all("/orders", {**FILTERS, "per_page": PER_PAGE})
except ApiError as err:
    items, pages = [], 0
    print("4. not yet:", err, "(finish TODO 1)")
cancelled = pd.DataFrame(items, columns=None if items else ["order_id", "order_date", "channel", "store", "order_total"])
cancelled["order_date"] = pd.to_datetime(cancelled["order_date"])
print("4. pages read:", pages, "| shape:", cancelled.shape)
print("   matches the promised total:", len(cancelled) == total, "| unique ids:", cancelled["order_id"].is_unique)

# %% Step 5: answer the question
# TODO 5a: group `cancelled` by store: orders = count of order_id, value = sum of order_total;
#          sort by orders, largest first.
# TODO 5b: what percentage of the cancelled orders were placed online (channel == "online")?
print("5. cancelled orders by store: TODO 5")

# %% Step 6: a request the API refuses, in the API's own words
# TODO 6: send the same request as the probe, but with the date written "10/01/2025".
#         Wrap it in try / except ApiError as err, and print err.status, err.code and err.message.
print("6. TODO 6")

# %% Step 7 (done for you): check the pull against the source file
orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
recent = orders[orders["order_date"] >= FILTERS["since"]]
expected = recent[recent["status"] == "cancelled"]
print("7. orders.csv has", len(expected), "such orders | same ids:",
      cancelled["order_id"].tolist() == expected["order_id"].tolist(),
      "| same total:", round(cancelled["order_total"].sum(), 2) == round(expected["order_total"].sum(), 2))
print(f"   for comparison, online orders are {(recent['channel'] == 'online').mean() * 100:.1f}% of ALL orders since {FILTERS['since']}")
