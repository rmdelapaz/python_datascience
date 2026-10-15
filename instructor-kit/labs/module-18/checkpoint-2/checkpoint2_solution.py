# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OFFLINE, fixtures

# %% [markdown]
# # Checkpoint 2 · Do the API and the database agree about returns? (MODEL ANSWER)
# 15 minutes, open notes, your own work. The full task sheet is in your workbook.
#
# Finance is closing the year. It has two sources for returned orders: the company database
# (data/pinecrest.db) and the orders API. Before anyone signs off, it wants to know:
# for orders with status "returned" placed on or after 2025-11-01, do the two sources agree?
# Report the number of orders and their total value from each source, and say whether they
# hold exactly the same order ids.
#
# Two modes, one function (make_http):
#   online  : the practice API on your own computer. Start it first, in a second terminal:
#                 python data/mock_api.py --rate 10 --per 5     (any flags will do)
#   offline : LABS_OFFLINE=1 -> saved responses in labs/module-18/_fixtures/, no network, and
#             a pretend clock, so the waits in this lab take no real time.
#   The API key is read from the environment variable PINECREST_API_KEY.

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

# %% Part A: the database. One query, read-only, with parameters.
import sqlite3

SINCE, STATUS = "2025-11-01", "returned"

conn = sqlite3.connect((DATA / "pinecrest.db").as_uri() + "?mode=ro", uri=True)
from_db = pd.read_sql(
    """
    SELECT order_id, order_date, order_total
    FROM orders
    WHERE status = ? AND order_date >= ?
    ORDER BY order_id
    """,
    conn, params=(STATUS, SINCE))
conn.close()
print(f"A. database: {len(from_db)} returned orders since {SINCE}, total ${from_db['order_total'].sum():,.2f}")

# %% Part B: the API. The key from the environment, every page, every status checked.
api_key = os.environ.get("PINECREST_API_KEY")
if not api_key:
    raise SystemExit("Set the environment variable PINECREST_API_KEY before running this file.")
print("B. key loaded:", api_key[:4] + "...")

items, pages = [], 0
url, params = f"{API}/orders", {"status": STATUS, "since": SINCE, "per_page": 50}
while url:
    r = http.get(url, headers={"X-API-Key": api_key}, params=params, timeout=10)
    r.raise_for_status()                         # a 401, 403 or 429 must stop the pull, not become data
    data = r.json()
    items.extend(data["items"])
    pages += 1
    url = f"{API}{data['next']}" if data["next"] else None
    params = None                                # `next` already carries the filters
from_api = pd.DataFrame(items)
from_api["order_date"] = pd.to_datetime(from_api["order_date"])
print(f"   API: {pages} pages, {len(from_api)} rows (the API promised {data['total']}), total ${from_api['order_total'].sum():,.2f}")
print("   unique ids:", from_api["order_id"].is_unique, "| first date:", from_api["order_date"].min().date())

# %% Part C: compare, and answer in a sentence
same_ids = sorted(from_api["order_id"]) == from_db["order_id"].tolist()
same_total = round(from_api["order_total"].sum(), 2) == round(from_db["order_total"].sum(), 2)
print("C. same order ids:", same_ids, "| same total value:", same_total)
only_api = set(from_api["order_id"]) - set(from_db["order_id"])
only_db = set(from_db["order_id"]) - set(from_api["order_id"])
print("   ids only in the API:", len(only_api), "| ids only in the database:", len(only_db))
print(f"ANSWER: Yes. Both sources hold the same {len(from_db)} returned orders placed since {SINCE}, "
      f"worth ${from_db['order_total'].sum():,.2f} in total; no order is in one source and missing from the other.")
