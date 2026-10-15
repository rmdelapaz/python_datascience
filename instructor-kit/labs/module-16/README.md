# Session 16 labs · Documents and HTTP

Lessons **5.5 NoSQL with MongoDB** and **6.1 HTTP with Requests**. Four labs, each a
`*_starter.py` (the handout) and a `*_solution.py` (the instructor's reference). The files use
`# %%` cell markers, so they open as notebook cells in VS Code and Jupyter, and they also run
as plain scripts.

| Lab | Practices | Minutes | Expected output (solution) |
|-----|-----------|---------|----------------------------|
| `l5_5-nosql-mongodb/sale_page_audit_*.py` | query dictionaries, dot notation, `$gte`, `$elemMatch`, `$exists`, projection + sort + limit | 25 (in the room) | 290 sessions saw /sale; 37 ordered; loose 218 vs strict 81; 92 with no `utm`; order rate 12.8% vs 9.6% overall |
| `l5_5-nosql-mongodb/landing_pages_*.py` | pipelines: `$addFields`, `$group`, `$match` after a group, `$unwind`, `$sort`, `$limit`; `pd.json_normalize(record_path=...)` | 20 (finish-if-fast, or homework) | six landing pages (`/` has 1,301 sessions, 9.6%); top SKU SNW-1016 with 16 units; 734 cart lines, 1,106 units, 543 carts |
| `l6_1-http-requests/category_check_*.py` | `robots.txt` in code, User-Agent, timeout, status codes, `raise_for_status()`, bytes vs text, encoding | 25 (in the room) | Footwear 28 products (25 rated), Snow 22 (22 rated), Skis is a 404 and gets no count; stars vanish under cp1252 |
| `l6_1-http-requests/api_price_check_*.py` | `params=`, `r.url`, `r.json()`, JSON to DataFrame, empty result vs error, JSON error bodies | 20 (finish-if-fast, or homework) | median price Tents $298.45, Snow $78.45, Camp Kitchen $39.95; `Skis` is 200 with total 0; `TNT-9999` is 404 |

Every starter runs without error as shipped: it prints `None` or a "TODO not done yet" line
where your code goes, and its header says what to expect when you finish.

## How to run

From the `instructor-kit/` folder (any folder works):

```bash
python labs/module-16/l5_5-nosql-mongodb/sale_page_audit_starter.py
python labs/module-16/l6_1-http-requests/category_check_starter.py
```

**MongoDB labs** need no server: they use `mongomock`, which imitates MongoDB inside Python
and was installed with the course environment in Lesson 0.1. They read `web_sessions.json`
from the course `data/` folder.

**HTTP labs** work in three ways. Pick one:

1. **Online (default).** `category_check` sends its requests to the practice shop at
   `https://rays-python-datascience.netlify.app/practice/shop/`, one second apart.
   `api_price_check` talks to the practice API on your own computer; start it first in a
   second terminal with `python data/mock_api.py` (no flags needed).
2. **The offline copy of the shop.** Unzip `data/pinecrest-practice-site.zip` in your project
   folder (`python -m zipfile -e data/pinecrest-practice-site.zip .`), run
   `python -m http.server 8001` there, and either change the `BASE_URL` line in the lab to
   `"http://127.0.0.1:8001/practice/shop/"` or set the environment variable
   `PINECREST_BASE_URL` to that address. (`PINECREST_API` does the same for the API address.)
3. **No network at all.** Set `LABS_OFFLINE=1`. The labs then rebuild real `requests.Response`
   objects from the saved pages and JSON in `_fixtures/` and touch nothing.
   macOS / Linux: `LABS_OFFLINE=1 python category_check_starter.py`.
   PowerShell: `$env:LABS_OFFLINE = "1"; python category_check_starter.py`.

The numbers are the same in all three. On the offline copy two printed details differ: the
`type` column reads `text/html` (Python's small server sends no charset) and the 404 page is
335 bytes instead of 2,514.

## `_fixtures/`

Saved responses for offline runs: each body (`shop_category-snow.html`,
`api_products_category-Tents_per_page-100.json`, ...) with a small `.meta.json` next to it that
holds the status code and the headers. They were made by really fetching the pages from a local
copy of the practice shop (served with the course host's headers) and from `data/mock_api.py`.

## Check

```bash
python3 labs/check_labs.py module-16        # expect: 8 passed, 0 failed
```
