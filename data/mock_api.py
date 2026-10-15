"""Pinecrest Outfitters mock API - a local practice API for the Python Data Science course.

Standard library only. It serves the course's fictional data so you can practice
pagination, API keys, bearer tokens and rate limits without touching a real service.

    python data/mock_api.py                 # http://127.0.0.1:8000
    python data/mock_api.py --port 8050     # another port
    python data/mock_api.py --rate 5 --per 10 --token-ttl 15   # stricter limits for experiments

Stop it with Ctrl+C.

Endpoints
    GET  /                      list of endpoints (no limit applied)
    GET  /health                {"status": "ok"} (no limit applied)
    GET  /products              ?page=1&per_page=20&category=Tents     public
    GET  /products/<sku>        one product                            public
    GET  /orders                ?page=&per_page=&status=&since=        needs header  X-API-Key: pinecrest-demo-key
    POST /login                 JSON {"username": "analyst", "password": "trailmix"} -> bearer token
    GET  /me                    needs header  Authorization: Bearer <token>
    GET  /slow                  ?seconds=2  answers late (practice timeouts)
    GET  /flaky                 fails with 503 twice, then succeeds (practice retries)

Every limited response carries X-RateLimit-Limit / -Remaining / -Reset. Going over the
limit returns 429 with a Retry-After header (seconds). Errors are always JSON:
    {"error": {"code": "not_found", "message": "..."}}

The demo key, user and password are public teaching values, not secrets.
Fictional data written for this course. (c) 2026 Ray de la Paz.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import secrets
import signal
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

API_KEY = "pinecrest-demo-key"
USERS = {"analyst": {"password": "trailmix", "role": "analyst", "name": "Demo Analyst"}}
MAX_PER_PAGE = 100
ENDPOINTS = {
    "GET /products": "public; ?page, ?per_page (max 100), ?category",
    "GET /products/<sku>": "public",
    "GET /orders": "X-API-Key header; ?page, ?per_page, ?status, ?since=YYYY-MM-DD",
    "POST /login": 'JSON body {"username", "password"}; returns a bearer token that expires',
    "GET /me": "Authorization: Bearer <token>",
    "GET /slow": "?seconds (max 10); answers late",
    "GET /flaky": "503 twice, then 200",
}


class ApiError(Exception):
    def __init__(self, status: int, code: str, message: str, headers: dict | None = None):
        super().__init__(message)
        self.status, self.code, self.message, self.headers = status, code, message, headers or {}


def _num(value: str):
    """CSV text -> int, float or None; anything else stays text."""
    if value == "":
        return None
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def load_csv(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return [{k: _num(v) for k, v in row.items()} for row in csv.DictReader(f)]


class State:
    """Everything the handlers share: the data, tokens and rate-limit counters."""

    def __init__(self, data_dir: Path, rate: int, per: float, token_ttl: float):
        self.products = load_csv(data_dir / "products.csv")
        self.by_sku = {p["sku"]: p for p in self.products}
        self.orders = load_csv(data_dir / "orders.csv")
        self.rate, self.per, self.token_ttl = rate, per, token_ttl
        self.tokens: dict[str, tuple[str, float]] = {}      # token -> (username, expires_at)
        self.windows: dict[str, tuple[float, int]] = {}     # client -> (window_start, count)
        self.flaky: dict[str, int] = {}
        self.lock = threading.Lock()

    def check_rate(self, client: str) -> dict:
        """Fixed window: `rate` requests per `per` seconds for each client. Raises 429 when over."""
        now = time.monotonic()
        with self.lock:
            start, count = self.windows.get(client, (now, 0))
            if now - start >= self.per:
                start, count = now, 0
            count += 1
            self.windows[client] = (start, count)
        reset = max(0.0, self.per - (now - start))
        headers = {"X-RateLimit-Limit": str(self.rate), "X-RateLimit-Remaining": str(max(0, self.rate - count)),
                   "X-RateLimit-Reset": str(math.ceil(reset))}
        if count > self.rate:
            wait = max(1, math.ceil(reset))
            raise ApiError(429, "rate_limited", f"Too many requests. Try again in {wait} second(s).",
                           {**headers, "Retry-After": str(wait)})
        return headers


class Handler(BaseHTTPRequestHandler):
    server_version = "PinecrestMockAPI/1.0"
    protocol_version = "HTTP/1.1"
    state: State          # set by make_server
    quiet = False

    # ---- plumbing ----------------------------------------------------------
    def log_message(self, fmt, *args):
        if not self.quiet:
            super().log_message(fmt, *args)

    def send_json(self, status: int, payload, headers: dict | None = None):
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def client_id(self) -> str:
        key = self.headers.get("X-API-Key")
        return f"key:{key}" if key else f"ip:{self.client_address[0]}"

    def int_param(self, query: dict, name: str, default: int, lo: int, hi: int) -> int:
        raw = query.get(name, [str(default)])[0]
        try:
            value = int(raw)
        except ValueError:
            raise ApiError(400, "bad_request", f"'{name}' must be a whole number, got {raw!r}.") from None
        if not lo <= value <= hi:
            raise ApiError(400, "bad_request", f"'{name}' must be between {lo} and {hi}, got {value}.")
        return value

    def paginate(self, rows: list, query: dict, path: str) -> dict:
        page = self.int_param(query, "page", 1, 1, 10**6)
        per_page = self.int_param(query, "per_page", 20, 1, MAX_PER_PAGE)
        total = len(rows)
        pages = max(1, math.ceil(total / per_page))
        extra = "".join(f"&{k}={v[0]}" for k, v in sorted(query.items()) if k not in ("page", "per_page"))
        nxt = f"{path}?page={page + 1}&per_page={per_page}{extra}" if page < pages else None
        return {"page": page, "per_page": per_page, "total": total, "total_pages": pages, "next": nxt,
                "items": rows[(page - 1) * per_page: page * per_page]}

    def require_bearer(self) -> tuple[str, float]:
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            raise ApiError(401, "missing_token", "Send the header 'Authorization: Bearer <token>'. Get a token from POST /login.",
                           {"WWW-Authenticate": "Bearer"})
        token = auth[len("Bearer "):].strip()
        entry = self.state.tokens.get(token)
        if entry is None:
            raise ApiError(401, "invalid_token", "That token is not recognized.", {"WWW-Authenticate": 'Bearer error="invalid_token"'})
        user, expires = entry
        left = expires - time.monotonic()
        if left <= 0:
            self.state.tokens.pop(token, None)
            raise ApiError(401, "token_expired", "The token has expired. Log in again with POST /login.",
                           {"WWW-Authenticate": 'Bearer error="invalid_token", error_description="expired"'})
        return user, left

    # ---- routes ------------------------------------------------------------
    def route(self, method: str) -> None:
        parts = urlsplit(self.path)
        path = parts.path.rstrip("/") or "/"
        query = parse_qs(parts.query)
        st = self.state
        if method == "POST":            # always read the body so the connection stays usable
            length = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(length) if length else b""
        if path == "/" and method == "GET":
            return self.send_json(200, {"name": "Pinecrest Outfitters mock API", "note": "Fictional data for the Python Data Science course.",
                                        "rate_limit": f"{st.rate} requests per {st.per:g} seconds per client",
                                        "endpoints": ENDPOINTS})
        if path == "/health" and method == "GET":
            return self.send_json(200, {"status": "ok"})
        limit_headers = st.check_rate(self.client_id())

        if path == "/login":
            if method != "POST":
                raise ApiError(405, "method_not_allowed", "Use POST for /login.", {"Allow": "POST"})
            try:
                body = json.loads(raw.decode("utf-8") or "null")
            except (ValueError, UnicodeDecodeError):
                raise ApiError(400, "bad_request", "The request body must be JSON.") from None
            if not isinstance(body, dict) or "username" not in body or "password" not in body:
                raise ApiError(400, "bad_request", 'Send JSON like {"username": "...", "password": "..."}.')
            user = USERS.get(str(body["username"]))
            if user is None or not secrets.compare_digest(str(body["password"]), user["password"]):
                raise ApiError(401, "invalid_credentials", "Wrong username or password.")
            token = secrets.token_urlsafe(24)
            with st.lock:
                st.tokens[token] = (str(body["username"]), time.monotonic() + st.token_ttl)
            return self.send_json(200, {"access_token": token, "token_type": "Bearer", "expires_in": int(st.token_ttl)}, limit_headers)
        if method != "GET":
            raise ApiError(405, "method_not_allowed", f"{method} is not supported on {path}.", {"Allow": "GET"})

        if path == "/products":
            rows = st.products
            if "category" in query:
                wanted = query["category"][0].lower()
                rows = [p for p in rows if str(p["category"]).lower() == wanted]
            return self.send_json(200, self.paginate(rows, query, "/products"), limit_headers)
        if path.startswith("/products/"):
            sku = path.split("/", 2)[2].upper()
            if sku not in st.by_sku:
                raise ApiError(404, "not_found", f"No product with SKU {sku!r}.")
            return self.send_json(200, st.by_sku[sku], limit_headers)
        if path == "/orders":
            key = self.headers.get("X-API-Key")
            if not key:
                raise ApiError(401, "missing_api_key", "Send your key in the X-API-Key header.")
            if not secrets.compare_digest(key, API_KEY):
                raise ApiError(403, "invalid_api_key", "That API key is not valid.")
            rows = st.orders
            if "status" in query:
                rows = [o for o in rows if o["status"] == query["status"][0]]
            if "since" in query:
                since = query["since"][0]
                try:
                    time.strptime(since, "%Y-%m-%d")
                except ValueError:
                    raise ApiError(400, "bad_request", f"'since' must look like 2025-01-31, got {since!r}.") from None
                rows = [o for o in rows if o["order_date"] >= since]
            return self.send_json(200, self.paginate(rows, query, "/orders"), limit_headers)
        if path == "/me":
            user, left = self.require_bearer()
            info = USERS[user]
            return self.send_json(200, {"username": user, "name": info["name"], "role": info["role"],
                                        "token_expires_in": round(left, 1)}, limit_headers)
        if path == "/slow":
            seconds = min(10.0, max(0.0, float(self.int_param(query, "seconds", 2, 0, 10))))
            time.sleep(seconds)
            return self.send_json(200, {"waited_seconds": seconds}, limit_headers)
        if path == "/flaky":
            with st.lock:
                n = st.flaky.get(self.client_id(), 0) + 1
                st.flaky[self.client_id()] = n
            if n % 3 != 0:
                raise ApiError(503, "service_unavailable", "Temporary failure. Try again shortly.", {**limit_headers, "Retry-After": "1"})
            return self.send_json(200, {"status": "ok", "attempts_needed": 3}, limit_headers)
        raise ApiError(404, "not_found", f"No endpoint at {path}. See GET / for the list.")

    def handle_method(self, method: str) -> None:
        try:
            self.route(method)
        except ApiError as e:
            self.send_json(e.status, {"error": {"code": e.code, "message": e.message}}, e.headers)
        except (BrokenPipeError, ConnectionResetError):
            pass
        except Exception as e:                                  # never leak a traceback as HTML
            self.send_json(500, {"error": {"code": "server_error", "message": f"{type(e).__name__}: {e}"}})

    def do_GET(self):
        self.handle_method("GET")

    def do_HEAD(self):
        self.handle_method("GET")

    def do_POST(self):
        self.handle_method("POST")

    def do_PUT(self):
        self.handle_method("PUT")

    def do_DELETE(self):
        self.handle_method("DELETE")


def make_server(port: int = 8000, host: str = "127.0.0.1", data_dir: Path | str | None = None, rate: int = 30,
                per: float = 10.0, token_ttl: float = 60.0, quiet: bool = False) -> ThreadingHTTPServer:
    """Build the server (not yet serving). Port 0 picks a free port: see server.server_address."""
    data_dir = Path(data_dir) if data_dir else Path(__file__).resolve().parent
    handler = type("PinecrestHandler", (Handler,), {"state": State(data_dir, rate, per, token_ttl), "quiet": quiet})
    server = ThreadingHTTPServer((host, port), handler)
    server.daemon_threads = True
    return server


def main() -> None:
    ap = argparse.ArgumentParser(description="Pinecrest Outfitters mock API (practice only, fictional data).")
    ap.add_argument("--port", type=int, default=8000, help="port to listen on (default 8000)")
    ap.add_argument("--host", default="127.0.0.1", help="address to bind (default 127.0.0.1: this computer only)")
    ap.add_argument("--data", type=Path, default=None, help="folder with products.csv and orders.csv (default: this script's folder)")
    ap.add_argument("--rate", type=int, default=30, help="requests allowed per window per client (default 30)")
    ap.add_argument("--per", type=float, default=10.0, help="window length in seconds (default 10)")
    ap.add_argument("--token-ttl", type=float, default=60.0, help="seconds before a bearer token expires (default 60)")
    ap.add_argument("--quiet", action="store_true", help="do not log each request")
    args = ap.parse_args()
    try:
        server = make_server(args.port, args.host, args.data, args.rate, args.per, args.token_ttl, args.quiet)
    except FileNotFoundError as e:
        raise SystemExit(f"Could not find the data files: {e}. Run this from the folder that contains data/.") from None
    except OSError as e:
        raise SystemExit(f"Could not start on port {args.port}: {e}. Try --port with another number.") from None

    def stop(signum, frame):            # SIGTERM (e.g. from a process manager) -> same clean exit as Ctrl+C
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, stop)
    host, port = server.server_address[:2]
    print(f"Pinecrest mock API on http://{host}:{port}  (limit: {args.rate} requests per {args.per:g} s; Ctrl+C to stop)", flush=True)
    try:
        server.serve_forever(poll_interval=0.2)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("Mock API stopped.", flush=True)


if __name__ == "__main__":
    main()
