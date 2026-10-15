# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import OFFLINE, fixtures

# %% [markdown]
# # Lab 6.4-B · The life of a token (SOLUTION)
# Question: what does the API answer at each moment in a bearer token's life (fresh,
# malformed, expired, renewed), and which of those answers is worth a second try?
#
# Practices: POST with a JSON body, the Authorization: Bearer header, reading error codes
# with ApiError, token expiry, and "renew and retry ONCE".
#
# Two modes, one function (make_http):
#   online  : the practice API on your own computer. Start it first, in a second terminal:
#                 python data/mock_api.py --token-ttl 5
#   offline : LABS_OFFLINE=1 -> saved responses in labs/module-18/_fixtures/, no network, and
#             a pretend clock, so the waits in this lab take no real time.
#   --token-ttl 5 makes tokens last five seconds, so you can watch one expire.
#   The user name and password are read from PINECREST_USER and PINECREST_PASSWORD.

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
                    del self.tokens[token]        # like the real API: reported once, then forgotten
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

# %% Step 1: log in once (POST, JSON body) and print only a hint of the token
USERNAME = require_env("PINECREST_USER")
PASSWORD = require_env("PINECREST_PASSWORD")
journal = []                                     # (request, status, code) for every step


def login():
    """POST /login. Returns (token, lifetime in seconds)."""
    body = check(http.post(f"{API}/login", json={"username": USERNAME, "password": PASSWORD}, timeout=10)).json()
    return body["access_token"], body["expires_in"]


token, lifetime = login()
logins = 1
journal.append(("log in", 200, "ok"))
print(f"1. Bearer token {token[:6]}... valid for {lifetime} seconds (your token will differ)")


# %% Step 2: use the token
def get_me(token):
    """GET /me with a bearer token. Returns the parsed JSON, or raises ApiError."""
    return check(http.get(f"{API}/me", headers={"Authorization": f"Bearer {token}"}, timeout=10)).json()


me = get_me(token)
journal.append(("fresh token", 200, "ok"))
print("2. answered for:", me["name"], "|", me["role"])

# %% Step 3: three requests that must fail. Predict each status and code first.
mistakes = [
    ("token without the word Bearer", "GET", "/me", {"headers": {"Authorization": token}}),
    ("a token nobody issued", "GET", "/me", {"headers": {"Authorization": "Bearer made-up-token"}}),
    ("wrong password", "POST", "/login", {"json": {"username": USERNAME, "password": "marshmallow"}}),
]
for label, method, path, extra in mistakes:
    try:
        check(http.request(method, f"{API}{path}", timeout=10, **extra))
        print(f"3. {label}: accepted, and it should not have been")
    except ApiError as err:
        journal.append((label, err.status, err.code))
        print(f"3. {label}: {err.status} {err.code}")

# %% Step 4: wait until the token has expired, then use it again
if lifetime <= 10:
    print(f"4. waiting {lifetime + 1} seconds for the token to expire ...")
    clock.sleep(lifetime + 1)
else:
    print(f"4. tokens last {lifetime} s on this server. To watch one expire, restart the API with --token-ttl 5.")
# (The server forgets an expired token the first time it reports it: a second request with the
# same token gets invalid_token. So the next request, in Step 5, is the one that finds out.)


# %% Step 5: renew and retry ONCE
def me_with_renewal():
    """GET /me. If the token has expired, log in again and repeat the request one time."""
    global token, logins
    try:
        return get_me(token)
    except ApiError as err:
        if err.code != "token_expired":
            raise                                # anything else is not ours to fix: let it surface
        journal.append(("the same token, later", err.status, err.code))
        print("   the same token, later:", err.status, err.code)
    token, _ = login()
    logins += 1
    return get_me(token)                         # a second failure raises: no loop


me = me_with_renewal()
journal.append(("renewed token", 200, "ok"))
print("5. answered for:", me["username"], "| logins so far:", logins)

# %% Step 6: the journal, and the next move for each answer
MOVES = {"ok": "use the data", "missing_token": "stop: fix the header", "invalid_token": "stop: this token was never issued",
         "invalid_credentials": "stop: fix the password, never loop", "token_expired": "log in again, retry ONCE"}
table = pd.DataFrame(journal, columns=["request", "status", "code"])
table["next move"] = table["code"].map(MOVES).fillna("TODO")
print("6. the journal:")
print(table.to_string(index=False))
print("   Only token_expired earns a second try, and exactly one.")
