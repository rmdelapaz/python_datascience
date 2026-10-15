# Session 2 labs: Vectorized Operations and Broadcasting

Lessons **1.2 Vectorized Operations** and **1.3 Broadcasting**. Every lab asks a new question of
`daily_sales.csv` with the lesson's skills; none repeats a lesson project or exercise.

Hand out the four `*_starter.py` files and the two `debug_*.py` handouts. Keep every
`*_solution.py` for yourself until after the lab.

## What is here

| File | Practices | In class | Expected output (solution) |
|------|-----------|---------:|----------------------------|
| `l1_2-vectorized-operations/staffing_load_starter.py` / `_solution.py` | Array-with-array arithmetic, a mask (count and fraction), `&` and `\|`, `np.select`, `np.unique`, `argmax` with parallel arrays | 13 min | Visitors per staff member: mean 55.3, min 28.2, max 116.5; 814 stretched store-days (28.0%); stretched and sale day 26; stretched or sale day 884; quiet 361, steady 1,728, stretched 814; most stretched 2025-02-26 at Bend (233 visitors, 2 staff) |
| `l1_2-vectorized-operations/eight_weeks_axis_starter.py` / `_solution.py` | `sum` with `axis=0` and `axis=1`, predicting result shapes, `argmax` along each axis, `argsort`, positions used on parallel arrays | 10 min (pairs) | Total 13,255; per store `[2935. 3312. 4347. 2661.]`; busiest days 2024-02-24, 2024-02-24, 2024-01-13, 2024-01-27; three busiest days 2024-02-24 (392), 2024-01-13 (374), 2024-01-20 (360); days won: Asheville 1, Bend 8, Boise 45, Flagstaff 2 |
| `l1_2-vectorized-operations/debug_masks.py` | Four mask bugs: `and`, missing parentheses, `nan` in neither group, a "copy" that is a second name (deliberately broken) | fast finishers | Fixed: 15, 15, 6, and 101 capped values with `revenue` untouched (largest real revenue 27677.1) |
| `l1_3-broadcasting/fair_visitors_starter.py` / `_solution.py` | A table and a row, a table and a column, `keepdims=True`, reading the broadcast error from the right, `argmax(axis=0)` | 13 min | Store averages `[281.4 323.4 440.9 281.6]`; busiest day 2.51, 2.45, 2.30, 2.40 times normal, all on 2024-05-25; average share `[0.213 0.244 0.332 0.211]`; Boise's share from 0.243 (2024-02-10) to 0.406 (2024-04-20) |
| `l1_3-broadcasting/target_grid_starter.py` / `_solution.py` | `np.broadcast_shapes`, `np.newaxis`, a column meeting a row (a grid), a mask on a grid, the accidental grid and `ravel()` | 10 min (pairs) | A `(4, 3)` table of targets (Boise 10449, 10651, 11159); 5 of 12 above $7,500, per store `[0 1 3 1]`; wrong shape `(4, 4)` with average size 1753.02; fixed: four errors, average size 209.9 |
| `l1_3-broadcasting/debug_shapes.py` | Three shape bugs: a flat array where a column was needed, a 7 by 7 grid of "gaps", the square-table trap (deliberately broken) | fast finishers | Fixed: seven zeros; 7 gaps, largest 6131.55; four zeros |

A starter runs without an error exactly as handed out and prints its `TODO` reminders. "Done"
for each lab is the output in the last column. Both 1.3 starters leave blanks in the comments
for a shape prediction: learners fill those in before running the line.

## How to run

With the course environment active, from any folder:

```bash
python labs/module-02/l1_2-vectorized-operations/staffing_load_starter.py
python labs/module-02/l1_3-broadcasting/fair_visitors_starter.py
```

Or open a file in VS Code or JupyterLab and run it cell by cell (`# %%` marks the cells).
The labs find the data through `labs_paths.py` (see `labs/README.md`).

Check everything in this session at once (8 files):

```bash
python3 labs/check_labs.py module-02
```

## Timing in Session 2

| Clock | Lab |
|-------|-----|
| 0:50 | `staffing_load_starter.py` (13 min + 2 min debrief), then `eight_weeks_axis_starter.py` in pairs (10 min); fast finishers take `debug_masks.py` |
| 2:10 | `fair_visitors_starter.py` (13 min + 2 min debrief), then `target_grid_starter.py` in pairs (10 min); fast finishers take `debug_shapes.py` |

Each lab repeats the `load(col, dtype=float)` helper from Lesson 1.2, reading
`DATA / "daily_sales.csv"`. No lab writes any file.
