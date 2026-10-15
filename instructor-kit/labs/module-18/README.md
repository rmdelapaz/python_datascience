# Session 18 labs · APIs: Keys, Tokens and Polite Clients

Lessons **6.4 API Authentication** and **6.5 Rate Limiting and Retries**, plus **Checkpoint 2**.
Four labs and the checkpoint, each a `*_starter.py` (the handout) and a `*_solution.py` (the
instructor's reference), with `# %%` cell markers.

| File | Practices | Minutes | Expected output (solution) |
|------|-----------|---------|----------------------------|
| `l6_4-api-authentication/cancelled_orders_*.py` | the key from the environment, 401 vs 403, `X-API-Key`, one small probe, following `next`, a 400 that explains itself, checking against `orders.csv` | 22 (in the room) | 70 cancelled orders since 2025-10-01, 3 pages of 25; 62 of them online (88.6%), $10,604.57 in all; the API and `orders.csv` agree |
| `l6_4-api-authentication/token_lifecycle_*.py` | POST `/login` with JSON, `Authorization: Bearer`, `missing_token` / `invalid_token` / `invalid_credentials` / `token_expired`, renew and retry ONCE | 20 (finish-if-fast, or homework) | a journal of seven requests; only `token_expired` earns a second try; 2 logins in all |
| `l6_5-rate-limiting/stock_check_*.py` | rate-limit headers, a burst that hits 429, `Retry-After`, plan B (wait as asked) vs plan A (a Throttle), not retrying 404s | 20 (in the room) | burst: 10 answered, 3 refused, Retry-After 5; plan B and plan A both 0 refused; Packs has the most out of stock (3) |
| `l6_5-rate-limiting/retry_and_cache_*.py` | backoff with jitter, `/flaky`, what not to retry, urllib3 `Retry` on a Session, a disk cache that never saves errors | 20 (finish-if-fast, or homework) | `/flaky` succeeds on try 3; 404 asked once; six questions, three requests |
| `checkpoint-2/checkpoint2_*.py` | Checkpoint 2 (15 minutes): one SQL query on `pinecrest.db` (read-only, parameters) and one authenticated, paginated API pull | 15 (in the room) | 118 returned orders since 2025-11-01 in both sources, $25,191.92, same ids |

## How to run

1. **Set the three environment variables** in the terminal you start Python, Jupyter or VS Code from
   (public demo values for the practice API; never put them in a file):

   ```bash
   # macOS / Linux
   export PINECREST_API_KEY="pinecrest-demo-key"
   export PINECREST_USER="analyst"
   export PINECREST_PASSWORD="trailmix"
   ```
   ```powershell
   # Windows PowerShell
   $env:PINECREST_API_KEY = "pinecrest-demo-key"
   $env:PINECREST_USER = "analyst"
   $env:PINECREST_PASSWORD = "trailmix"
   ```

2. **Start the practice API** in a second terminal, from the project folder, with the flags of the lesson:
   `python data/mock_api.py --token-ttl 5` for the 6.4 labs (tokens last 5 seconds), and
   `python data/mock_api.py --rate 10 --per 5` for the 6.5 labs (10 requests every 5 seconds).
   The checkpoint works with any flags. To use another address, set `PINECREST_API`.

3. **No network at all?** `LABS_OFFLINE=1` (PowerShell: `$env:LABS_OFFLINE = "1"`). The labs then
   replay real responses saved in `_fixtures/`, follow the same rate-limit and token rules, and run
   their waits on a pretend clock, so a lab that waits 5 seconds online finishes at once and says so.
   The lab checker sets the three variables to the demo values for you.

The practice shop is not used in Session 18.

## `_fixtures/`

Every file is a real response (body + `.meta.json` with status and headers) saved from
`data/mock_api.py`: product and order pages, the error bodies (`orders_no_key`, `orders_bad_key`,
`me_expired`, `rate_limited`, ...), and the `/flaky` answers. A small offline adapter in each lab picks
the right one for each request, so the starters and solutions run the same code in both modes.

Labs that save files (a cache, CSV exports) write to `OUTPUT`.

## Check

```bash
python3 labs/check_labs.py module-18        # expect: 10 passed, 0 failed
```
