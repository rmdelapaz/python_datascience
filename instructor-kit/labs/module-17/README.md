# Session 17 labs · Scraping Static and Dynamic Pages

Lessons **6.2 Parsing HTML with Beautiful Soup** and **6.3 Dynamic Pages with Selenium**. Four
labs, each a `*_starter.py` (the handout) and a `*_solution.py` (the instructor's reference),
with `# %%` cell markers so they open as notebook cells in VS Code and Jupyter.

| Lab | Practices | Minutes | Expected output (solution) |
|-----|-----------|---------|----------------------------|
| `l6_2-beautifulsoup/sleeping_bag_shortlist_*.py` | `select` / `select_one`, one card → one dictionary, `.get()` for optional attributes, narrowing before visiting detail pages, the specs table, cleaning text | 25 (in the room) | 24 cards on the Sleeping page (claims 24); 12 sleeping bags, 6 at $260 or less and available; lightest SLP-1002 (0.81 kg, $132.95); SLP-1019 has no weight listed |
| `l6_2-beautifulsoup/price_list_tables_*.py` | `pd.read_html` on bytes, choosing a table by `attrs`, cleaning `$` text, crosstab, cross-checking a table against cards | 20 (finish-if-fast, or homework) | 2 tables; list prices total 29,475.90; Packs has the most out of stock (3); 8 unrated products; Boise open longest (11 hours); Accessories: 32 rows = 32 cards |
| `l6_3-selenium/budget_search_*.py` | what `requests` sees on a dynamic page, a search as a URL (`urlencode`), headless Chrome, an explicit wait, `page_source` → Beautiful Soup, `quit()` in `finally`, the data file behind the page | 25 (in the room) | the rendered page shows 60 rows but says "73 products found"; products.json has 73 products at $50 or less and available; the 13 not shown are all Accessories |
| `l6_3-selenium/page_triage_*.py` | static or dynamic? raw HTML vs rendered counts, using a form (`Select`, submit, two waits), the verdict table | 20 (finish-if-fast, or homework) | Climbing category 24 / 24 (static); Deals 0 / 8 and Search 0 / 24 (dynamic: request the data file first); the form search and the category page give the same 24 SKUs |

Every starter runs without error as shipped and prints what is still to do.

## How to run

From the `instructor-kit/` folder: `python labs/module-17/l6_2-beautifulsoup/sleeping_bag_shortlist_starter.py`.

The labs work in three ways:

1. **Online (default):** requests go to `https://rays-python-datascience.netlify.app/practice/shop/`,
   one second apart (the shop's crawl delay).
2. **The offline copy of the shop:** unzip `data/pinecrest-practice-site.zip` in your project folder
   (`python -m zipfile -e data/pinecrest-practice-site.zip .`), run `python -m http.server 8001`
   there, and set `PINECREST_BASE_URL=http://127.0.0.1:8001/practice/shop/` (or edit the `BASE_URL`
   line). Selenium loads local pages the same way.
3. **No network and no browser:** `LABS_OFFLINE=1` (PowerShell: `$env:LABS_OFFLINE = "1"`). The labs
   read the saved pages in `_fixtures/`; the Selenium labs then start no browser and say so
   (`[offline] no browser started; reading the saved finished page ...`).

**Selenium labs need Google Chrome.** Selenium 4 downloads a matching driver by itself the first time
(internet needed once). If Chrome cannot start (not installed, driver download blocked), the lab prints
`[no browser] Chrome could not be started (...)` and continues with the saved finished page, so the
rest of the lab still works. To use a Chrome or Chromium program in an unusual place, set
`PINECREST_CHROME` to its path. The browser is always closed in a `finally` block.

## `_fixtures/`

`shop_*` files are real responses (body + `.meta.json` with status and headers) fetched from a local
copy of the practice shop that sends the course host's headers. `rendered_*.html` files are
`driver.page_source` saved from real headless-Chrome runs after the page's JavaScript had finished:
the budget search (`max_price=50&in_stock=1`), the Climbing search done through the form, the deals
page after its first batch, and the Climbing category page.

Labs write their CSV files to `OUTPUT` (`output/` next to the lab; a temporary folder offline).

## Check

```bash
python3 labs/check_labs.py module-17        # expect: 8 passed, 0 failed
```
