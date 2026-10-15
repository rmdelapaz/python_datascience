# Session 1 labs: Toolkit and First Arrays

Lessons **0.1 Your Data Science Toolkit** and **1.1 Arrays vs Lists**. Every lab is new practice on
the lesson's skills with the Pinecrest data; none of them repeats a lesson project or exercise.

Hand out the `*_starter.py` files, `check_environment.py` and the two `debug_*.py` handouts.
Keep every `*_solution.py` for yourself until after the lab.

## What is here

| File | Practices | In class | Expected output (solution) |
|------|-----------|---------:|----------------------------|
| `l0_1-orientation/check_environment.py` | A tool, not an exercise: Python 3.12+, an active environment, every course package, the data folder | 12 min (opening) | Last line `READY for Python Data Science`, or `NOT READY` with a numbered fix list |
| `l0_1-orientation/diagnostic_starter.py` / `_solution.py` | Six Intro and Intermediate Python skills: slicing, copies, dictionaries, functions, comprehensions, reading a CSV as text | homework (optional) | Six `PASS` lines, `6 of 6 checks pass.`, `Two years of store revenue: $21,539,319.88` |
| `l0_1-orientation/payment_methods_starter.py` / `_solution.py` | `read_csv`, `.shape`, picking a column, `value_counts()`, a True/False column and its mean, filtering rows | 15 min | `(20302, 11)`; card 12,392, digital_wallet 4,794, cash 1,614, gift_card 1,502; wallet share 23.6%; 1,502 gift-card orders averaging $193.22; cash is used only in stores |
| `l0_1-orientation/debug_traceback.py` | Reading a traceback from the bottom: three bugs fixed one at a time (deliberately broken) | fast finishers | Fixed: `Orders: 20302`, `Returned orders: 1143`, `Largest returned order: $1,168.75` |
| `l1_1-arrays-vs-lists/transactions_week_starter.py` / `_solution.py` | `genfromtxt`, `shape` / `dtype` / `ndim` / `size`, `np.isnan`, slicing, `reshape(7, 4)`, rows, columns and cells, `astype`, `nbytes` | 10 min | `(2903,)`, `float64`, 0 missing; Saturday `[93. 59. 151. 71.]`; Bend `[49. 42. 39. 46. 66. 59. 73.]`; busiest store-day 151; 224 bytes as `float64`, 56 as `int16` |
| `l1_1-arrays-vs-lists/what_if_copy_starter.py` / `_solution.py` | Views and copies, `np.shares_memory`, `.copy()`, a decimal stored in an integer array | 10 min (pairs) | Bend real total 868 (three times, unchanged); what-if total 938; `True` then `False` from `shares_memory`; 97.6 stored as 97 |
| `l1_1-arrays-vs-lists/debug_silent_traps.py` | Three bugs that raise no error: text in a numeric array, `int8` overflow, a view (deliberately wrong) | fast finishers | Fixed: average price 48.5, total stock 260, Monday is still 148 |

A starter runs without an error exactly as handed out: it prints its `TODO` reminders and whatever
is already done for the learner. "Done" for each lab is the output in the last column.

## How to run

With the course environment active, from any folder:

```bash
python labs/module-01/l0_1-orientation/check_environment.py
python labs/module-01/l0_1-orientation/payment_methods_starter.py
python labs/module-01/l1_1-arrays-vs-lists/transactions_week_starter.py
```

Or open a file in VS Code or JupyterLab: the `# %%` lines are notebook cells, so learners can run
one step at a time. The labs find the data through `labs_paths.py` (see `labs/README.md`): keep the
`labs/` folder inside the project folder, next to `data/`, or set `PINECREST_DATA`.
`check_environment.py` does not use `labs_paths.py`; run it from the project folder (the one that
contains `data/`), or copy it there.

Check everything in this session at once (8 files):

```bash
python3 labs/check_labs.py module-01
```

## Timing in Session 1

| Clock | Lab |
|-------|-----|
| 0:10 | `check_environment.py` on every machine (12 min, inside the 30-minute opening) |
| 1:00 | `payment_methods_starter.py` (15 min); fast finishers take `debug_traceback.py` |
| 2:15 | `transactions_week_starter.py` (10 min), then `what_if_copy_starter.py` in pairs (10 min); fast finishers take `debug_silent_traps.py` |

`diagnostic_starter.py` is optional homework for anyone who missed two or more of the six
diagnostic questions on the workbook's Start Here page.
