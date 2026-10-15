# Session 3 labs: Randomness and Linear Algebra

Lessons **1.4 Random Number Generation** and **1.5 Linear Algebra Essentials**. Every lab asks a
new question of the course data with the lesson's skills; none repeats a lesson project or exercise.

Hand out the four `*_starter.py` files and the two `debug_*.py` handouts. Keep every
`*_solution.py` for yourself until after the lab.

## What is here

| File | Practices | In class | Expected output (solution) |
|------|-----------|---------:|----------------------------|
| `l1_4-random-generation/mystery_shopper_starter.py` / `_solution.py` | A seeded generator, `choice` with `replace=False`, sampling row positions and using them on parallel arrays, reproducing a result, `permutation` for a 70/30 split | 12 min | Seed 7: pilot stores Boise and Flagstaff; 12 Flagstaff dates in 2025 (2025-01-02 to 2025-11-26), 2 on a weekend; same schedule from the same seed: True; groups of 2,032 and 871 with mean visitors 356.8 and 353.8 |
| `l1_4-random-generation/returns_desk_starter.py` / `_solution.py` | Monte Carlo (model, repeat, count) with `rng.poisson`, a chance as the mean of a mask, checking a model against real data | 13 min (pairs) | Seed 14: 1.564 returns per day; 4 or more returns: simulated 7.4%, real 7.3%; none: simulated 21.1%, real 20.7%; then 40 or more orders: simulated 1.7%, real 7.3% (the model fails: variance 64.35 against a mean of 27.77) |
| `l1_4-random-generation/debug_random.py` | A five-faced die, `shuffle` assigned to a name, a generator re-created in a loop, probabilities that do not add up to 1 (deliberately broken) | fast finishers | Fixed: rolls 1 to 6; a shuffled deck; 3 different weeks; three different store names |
| `l1_5-linear-algebra/payroll_receipt_starter.py` / `_solution.py` | A dot product as a weighted average, matrix @ vector, matrix @ matrix, `*` with `axis=0` against `@`, `.T`, `np.linalg.solve` with a check | 12 min | Ratings 4.138 plain, 4.146 weighted; payroll per day `[3172. 2816. 2820. 2996. 4036. 5276. 4396.]`; week totals 25,512 and 27,252; per store `[5880. 5984. 8832. 4816.]`; hourly rates `[22. 19. 17.]` |
| `l1_5-linear-algebra/basket_model_starter.py` / `_solution.py` | `np.column_stack` with a column of ones, `np.linalg.lstsq`, RMSE and R squared, a second route to a slope, adding a column, predictions with one `@` | 12 min (pairs) | Flagstaff, 724 days: `revenue = 117.23 + 87.10 * transactions`, RMSE $631.35, R squared 0.945; direct basket value 88.77; sale-day coefficient -172.09 with RMSE $630.73 (the column does not earn its place); forecasts $5,341.19, $8,842.11, $13,046.16 |
| `l1_5-linear-algebra/debug_linalg.py` | `*` for `@`, a product that needs `.T`, one `nan` that ruins a fit, a missing column of ones (deliberately broken) | fast finishers | Fixed: `[756.35 348.95 356.3 ]`; `[1461.6  1242.41]`; slope 21.39; about -238.85 and 21.39 |

A starter runs without an error exactly as handed out and prints its `TODO` reminders. "Done"
for each lab is the output in the last column. Random labs use fixed seeds: a learner who makes
the draws in the order the starter gives gets exactly the solution's numbers.

## How to run

With the course environment active, from any folder:

```bash
python labs/module-03/l1_4-random-generation/mystery_shopper_starter.py
python labs/module-03/l1_5-linear-algebra/payroll_receipt_starter.py
```

Or open a file in VS Code or JupyterLab and run it cell by cell (`# %%` marks the cells). In a
notebook, rerunning a cell that draws from the generator changes the numbers: run from the top.
The labs find the data through `labs_paths.py` (see `labs/README.md`).

Check everything in this session at once (8 files):

```bash
python3 labs/check_labs.py module-03
```

## Timing in Session 3

| Clock | Lab |
|-------|-----|
| 0:45 | `mystery_shopper_starter.py` (12 min), then `returns_desk_starter.py` in pairs (13 min including the debrief); fast finishers take `debug_random.py` |
| 2:10 | `payroll_receipt_starter.py` (12 min), then `basket_model_starter.py` in pairs (12 min + debrief); fast finishers take `debug_linalg.py` |

Data used: `daily_sales.csv` (all four labs' NumPy columns), `orders.csv` (order dates and
statuses, `returns_desk`), `products.csv` (ratings and review counts, `payroll_receipt`).
No lab writes any file.
