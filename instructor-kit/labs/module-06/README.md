# Session 6 labs · Merging and Reshaping

Lessons 2.5 (Merging and Joining) and 2.6 (Pivot Tables and Reshaping). These labs are new practice
on the lessons' skills with the Pinecrest data; they are not the lesson projects (Revenue by Category
and The Seasonality Report), which learners start in class and finish at home.

Starters (`*_starter.py`) are the handouts: each runs as shipped, lists its numbered TODOs and says
what to expect. Solutions (`*_solution.py`) are the instructor's reference and print the answers.

| Lab | Practices | Minutes | Expected output (solution) |
|-----|-----------|--------:|----------------------------|
| `l2_5-merging-joining/customer_profiles_*.py` | aggregate first, then merge; `how="left"`, `validate="one_to_one"`, `indicator=True`; an honest `fillna(0)`; an outer-join audit | 25 | `4850 -> 4850` (3,792 both, 1,058 left_only); top spender Rosa Blackwood $8,305.39; 37.5% of Basic accounts never ordered; 150 ids / 739 orders / $154,273.80 with no account |
| `l2_5-merging-joining/orders_weather_*.py` | a two-column key with different names (`left_on` / `right_on`), choosing the left table so zero-order days survive | 20 | `2924 -> 2924` (336 store-days with no order); rainy days: Asheville -12.0%, Bend -15.3%, Boise -29.9%, Flagstaff -16.3%; 2.55 orders per store-day vs 2.88 if empty days drop out |
| `l2_5-merging-joining/debug_merges.py` | "find the bug": five broken merges (three crash, two are quiet) | 10 | after the fixes: 45490, 2903, 45490, 3950701.45, 194.6. Broken on purpose, so the checker does not run it |
| `l2_6-pivot-tables/payment_returns_*.py` | `pivot_table` with `fill_value` / `margins`, a rate as a boolean mean, counts behind cells, `crosstab` `normalize` both ways, a total that hides a difference | 15 | corner 20,302; return rates card 5.7%, digital wallet 6.4%, gift card 5.2%, cash 3.0%; gift cards in Bend 1.0% of 102 orders; online about 7% for every method, stores 2.1% to 3.7% |
| `l2_6-pivot-tables/survey_by_age_*.py` | `melt`, `pivot_table` for means and counts, `idxmin(axis=1)`, `stack` back to tidy, a CSV in `OUTPUT` | 15 | 9,000 tidy rows; lowest item is price for every age group except 65+ (website 3.04); 18-24 price 2.80; saved file `(30, 3)` |
| `l2_6-pivot-tables/weather_grid_*.py` | `pivot` when there is one row per cell, `idxmax(axis=1)`, `pivot_table` on month numbers, the alphabetical-month trap and `reindex`, `melt` back | 15 | wide `(731, 4)` with no gaps; warmest city Asheville 338 days, Boise 227, Flagstaff 106, Bend 60; Boise July high 92.0, January 29.7; melt back to 2,924 rows |

## In the room

Session 6 gives each lesson a 25-minute guided lab: `customer_profiles` for 2.5, `payment_returns`
then `survey_by_age` for 2.6. `orders_weather`, `weather_grid` and `debug_merges.py` are for fast
finishers and for homework.

## Running

```bash
python labs/module-06/l2_5-merging-joining/customer_profiles_starter.py   # from the kit folder, or from any folder
python3 labs/check_labs.py module-06                                     # 10 passed, 0 failed
```

The files open as notebook cells in VS Code and Jupyter (`# %%` markers). They read the course data
through `from labs_paths import DATA` and write only to `OUTPUT` (`survey_by_age` saves one CSV there).
Nothing here needs the internet or a server.
