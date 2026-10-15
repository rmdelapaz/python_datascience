# Session 4 labs · DataFrames and Loading Data

Lessons 2.1 (DataFrames and Series) and 2.2 (Loading Data). These labs are new practice on the
lessons' skills with the Pinecrest data; they are not the lesson projects (the Catalog Health Check
and the Pinecrest Snapshot), which learners start in class and finish at home.

Starters (`*_starter.py`) are the handouts: each runs as shipped, lists its numbered TODOs and says
what to expect. Solutions (`*_solution.py`) are the instructor's reference and print the answers.

| Lab | Practices | Minutes | Expected output (solution) |
|-----|-----------|--------:|----------------------------|
| `l2_1-dataframes-series/busiest_days_*.py` | the four-line greeting, `sort_values`, masks with `&` and `~`, `.idxmax()` + `.loc` on `daily_sales.csv` | 15 | five biggest store-days (all Boise sale weekends, top $27,677.10 on 2024-08-31); 101 store-days above $15,000 = 36 promo + 65 ordinary; quietest day Flagstaff 2024-01-29 ($2,093.79) |
| `l2_1-dataframes-series/recommend_groups_*.py` | a new column filled with `.loc[mask, col] = ...`, `value_counts`, mask means, a copy-on-write check on `survey.csv` | 15 | passive 637, promoter 556, detractor 553, no answer 54; score 0.2 for all shoppers, -14.7 for Asheville; 0 rows of `survey` changed |
| `l2_1-dataframes-series/debug_filters.py` | "find the bug": five broken filters on `products.csv` (three crash, two are silent) | 10 | after the fixes: 82.95, 14, 7, 8, 29. Broken on purpose, so the checker does not run it |
| `l2_2-loading-data/till_export_*.py` | `sep`, `skiprows`, `decimal`, `thousands`, `na_values`, `parse_dates` + `date_format`; proving a load against a clean file | 15 | 28 rows, `revenue` float64, 1 missing revenue (Bend, 2025-02-19), both totals 163,755.71, "totals match: True" |
| `l2_2-loading-data/product_pages_*.py` | `json.load`, `pd.json_normalize(record_path=, meta=)`, fixing dtypes, `.str` filters, Parquet and CSV round trip into `OUTPUT` | 15 | 9,348 page views, 2,793 product-page views; top SKU SNW-1016 (22 views); 46.2 s on product pages vs 48.1 s overall; Parquet equal to the original, CSV not |
| `l2_2-loading-data/targets_vs_actuals_*.py` | two Excel sheets with different options (`header=3`), a result table from a list of dicts, `to_excel(index=False)` | 15 | Flagstaff 106.4%, Bend 98.0%, Boise 97.1%, Asheville 90.9% of target; 1 store at or above target |

`l2_2-loading-data/till_export_week08.txt` is the data file for the `till_export` lab: one week of
`daily_sales.csv` (2025-02-17 to 2025-02-23) rewritten in an export dialect (semicolons, three note
lines, `3.536,91` amounts, `17.02.2025` dates, `n/a` for the one missing total).

## In the room

Session 4 gives each lesson a 25-minute guided lab: `busiest_days` then `recommend_groups` for 2.1,
`till_export` then `product_pages` for 2.2. `targets_vs_actuals` and `debug_filters.py` are for fast
finishers and for homework.

## Running

```bash
python labs/module-04/l2_1-dataframes-series/busiest_days_starter.py     # from the kit folder, or from any folder
python3 labs/check_labs.py module-04                                      # 10 passed, 0 failed
```

The files open as notebook cells in VS Code and Jupyter (`# %%` markers). They read the course data
through `from labs_paths import DATA` and write only to `OUTPUT` (an `output/` folder next to the lab).
Nothing here needs the internet or a server.
