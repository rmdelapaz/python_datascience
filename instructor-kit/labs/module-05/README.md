# Session 5 labs · Cleaning and Grouping

Lessons 2.3 (Cleaning Data) and 2.4 (GroupBy Operations). These labs are new practice on the
lessons' skills with the Pinecrest data; they are not the lesson projects (The Cleaning Pipeline
and The Store Scorecard), which learners start in class and finish at home.

Starters (`*_starter.py`) are the handouts: each runs as shipped, lists its numbered TODOs and says
what to expect. Solutions (`*_solution.py`) are the instructor's reference and print the answers.

| Lab | Practices | Minutes | Expected output (solution) |
|-----|-----------|--------:|----------------------------|
| `l2_3-cleaning-data/register_log_*.py` | the whole cleaning routine on an unfamiliar file: audit, headers, a TOTAL row, duplicates, text variants, `$1,234.56` text, a lost decimal point found with evidence, three date formats, honest blanks, assertions, a scorecard | 25 | 35 rows become 31; `pending` and one `n/a` stay blank; lost decimal on 2025-05-17 repaired; `cells compared: 217 \| still blank: 2 \| wrong: 0`; stretch: the pending day recovered from the TOTAL row (3,668.50), then 1 blank |
| `l2_3-cleaning-data/total_row_check_*.py` | a control total: the lesson's repairs on `orders_messy.csv` applied one at a time while tracking the sum of `Order Total` | 20 | careless sum 4,126,451.89 (+4.45%); duplicates -42,630.16; negatives +6,654.16; 8 lost decimals -147,396.15; remaining gap 7,621.71 = the 40 blank totals, to the cent |
| `l2_4-groupby-operations/store_days_*.py` | named aggregation, `size` vs `count`, two keys + `unstack`, a computed year key, `transform`, the average-of-averages trap on `daily_sales.csv` | 20 | conversion 23.5% to 23.7% in every store; promo-day lift 1.88 to 1.98; growth Flagstaff +19.7%, Boise +9.3%, Bend +3.8%, Asheville -5.0%; 63 standout days (61.9% promo days) |
| `l2_4-groupby-operations/basket_sizes_*.py` | choosing the key (per order, per SKU), `agg` / `transform` / `filter`, the transform-then-mask twin on `order_items.csv` | 20 | 20,302 baskets, mean 2.24 lines; top SKU by units and revenue ACC-1015, but the next two differ; 5,890 single-line orders; 1,106 lines in 175 orders with six or more lines, by both methods |
| `l2_4-groupby-operations/debug_groupby.py` | "find the bug": five broken summaries of `orders.csv` (two crash, three are quiet) | 10 | after the fixes: five store means, five store names, card 12392, `20302 of 20302`, 194.6. Broken on purpose, so the checker does not run it |

`l2_3-cleaning-data/asheville_may_log.csv` is the data file for the `register_log` lab: the 31 days of
May 2025 for the Asheville store from `daily_sales.csv`, rewritten as a hand-typed log with planted
damage (untidy headers, 3 duplicate rows, a TOTAL row, five spellings of the store, seven spellings of
yes/no, currency text, one `pending`, one `n/a`, one revenue figure 100 times too large, three date
formats). `daily_sales.csv` is its answer key. It is read-only: every fix is a line of code.

## In the room

Session 5 gives Lesson 2.3 a 25-minute guided lab (`register_log`) and Lesson 2.4 a 20-minute one
(`store_days`). `total_row_check`, `basket_sizes` and `debug_groupby.py` are for fast finishers and
for homework.

## Running

```bash
python labs/module-05/l2_3-cleaning-data/register_log_starter.py     # from the kit folder, or from any folder
python3 labs/check_labs.py module-05                                  # 8 passed, 0 failed
```

The files open as notebook cells in VS Code and Jupyter (`# %%` markers). They read the course data
through `from labs_paths import DATA` and write nothing. Nothing here needs the internet or a server.
