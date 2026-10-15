# Labs

All hands-on lab programs for **Python Data Science**, grouped by session (one folder per
3-hour session; `module-07` = Session 7). Each session folder has its own `README.md` with the
exact files, what each lab practices, how long it takes and what "done" looks like. This file
is the map and the rules.

```
labs/
├─ labs_paths.py    finds the course data (DATA), a safe place to write (OUTPUT), and the OFFLINE switch
├─ check_labs.py    runs every starter, solution and test file and reports PASS/FAIL
├─ module-01/       Session 1 · lessons 0.1 + 1.1
│   ├─ README.md
│   ├─ l0_1-orientation/        (Session 1 only: environment check, diagnostic)
│   ├─ l1_1-<slug>/             one folder per lesson: l<module>_<lesson>-<slug>
│   │   ├─ <name>_starter.py    the handout
│   │   ├─ <name>_solution.py   the instructor's reference
│   │   └─ debug_<name>.py      (optional) a deliberately broken "find the bug" handout
│   └─ _fixtures/               (optional) saved web pages / JSON for offline runs
├─ module-02/ ... module-21/
```

## The data

Labs read the same Pinecrest Outfitters files the lessons use (`orders.csv`, `pinecrest.db`, ...).
They never contain a path to the data. They ask `labs_paths` for it:

```python
from labs_paths import DATA
orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
```

`DATA` is found in this order:

1. the environment variable **`PINECREST_DATA`**, if it is set (the folder that holds `orders.csv`);
2. a **`data/orders.csv`** in the lab's own folder or any folder above it. Inside the course
   repository that is the course's `data/` folder. If you received the kit on its own, unzip
   `pinecrest-data.zip` next to the `labs/` folder so that `instructor-kit/data/orders.csv` exists;
3. otherwise the lab stops with a message that says exactly those two fixes.

**Labs only read from `DATA`.** Anything a lab writes (charts, CSV exports, HTML charts, a
working copy of `pinecrest.db` before adding an index or a table) goes to `OUTPUT`:

```python
from labs_paths import DATA, OUTPUT
fig.savefig(OUTPUT / "monthly_revenue.png")          # ./output/ next to the lab file
```

`OUTPUT` is an `output/` folder next to the lab file, created the first time a lab uses it
(it is git-ignored). When `LABS_OFFLINE=1` it is a temporary folder that disappears when the
program ends.

## The bootstrap: the first lines of every lab

Every `*_starter.py`, `*_solution.py` and `debug_*.py` begins with exactly these lines
(change only the names imported on the last one):

```python
# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA
```

The middle line walks up from the lab file until it reaches the folder that holds
`labs_paths.py` (this `labs/` folder) and puts it on Python's import path. That is why a lab
runs the same way from its own folder, from `labs/`, from the kit root or from anywhere else,
and as cells in VS Code (`# %%`). In a plain Jupyter notebook there is no `__file__`, so the
walk starts at the notebook's working folder instead; keep the notebook somewhere under `labs/`.
The last line may import any of `DATA`, `OUTPUT`, `OFFLINE`, `fixtures`.

A pytest file (`test_*.py`) uses the same lines. To import the lab it tests, it adds its own
folder too: `sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))`.

## Naming rules

| File | Meaning | Run by the checker |
|------|---------|--------------------|
| `<name>_starter.py` | The handout. **Runs without error exactly as shipped**: numbered `# TODO` comments, placeholder values, and a printed line that says what is expected once the TODOs are done. | yes |
| `<name>_solution.py` | The reference. Complete; prints its answers. Do not hand out before the lab. | yes |
| `test_<name>.py` | pytest file. Must pass. A `test_<name>_starter.py` only has to be collected (its tests may be TODO stubs). | yes (pytest) |
| `debug_<name>.py` | A deliberately broken or crashing "find the bug" handout. | **no** |
| `_fixtures/...` | Saved responses for offline runs. Not programs. | **no** |
| anything else (`check_environment.py`, helper modules, `README.md`, data a lab ships) | Support files. | no |

- Starters and solutions come in **pairs** with the same `<name>`; a starter without a solution
  (or the reverse) fails the check. A handout that is neither a starter nor a solution must not
  end in `_starter.py` / `_solution.py`.
- Lesson folders are `l<module>_<lesson>-<slug>`: `l2_7-time-series`, `l6_4-api-authentication`.
- Use `# %%` cell markers so a lab opens as notebook cells in VS Code and Jupyter.
- Labs take no keyboard input (`input()` gets an empty stdin in the checker) and seed any randomness.

## Offline rule and `_fixtures/`

The checker sets **`LABS_OFFLINE=1`**. `labs_paths.OFFLINE` is then `True`, and a lab must:

- **not touch the network.** Read the saved response from the session's `_fixtures/` folder
  instead (`labs/module-NN/_fixtures/`: HTML pages, JSON). `fixtures(__file__)` returns that
  folder: `page = (fixtures(__file__) / "catalog-page-1.html").read_text(encoding="utf-8")`.
  The same lab must also work online (against `BASE_URL` or the mock API) when the variable is
  not set. Put the choice in one small function so the rest of the lab does not care.
- **not open a browser or a window.** No `fig.show()`, `show()`, `plt.show()` that blocks or
  `webbrowser.open()` when `OFFLINE` is true; write the HTML or PNG to `OUTPUT` instead.
  Selenium labs check for a browser first and fall back to a fixture with a clear message.
- **not start a server it does not stop.** (The checker kills leftovers, but a learner's
  terminal will not.)

Teaching in a room with no internet: `LABS_OFFLINE=1 python <lab>.py`
(PowerShell: `$env:LABS_OFFLINE = "1"; python <lab>.py`).

Reference example of the pattern: `~/projects/_kit_tools/python_ds/sample_session/labs/module-07/l2_8-window-functions/offline_fixture_demo_solution.py`.

## Checking the labs

From the `instructor-kit/` folder (any folder works):

```bash
python3 labs/check_labs.py                 # all sessions
python3 labs/check_labs.py module-07       # one session (also 07 or 7; several allowed)
python3 labs/check_labs.py module-07 -v    # also show the tail of each program's output
python3 labs/check_labs.py --timeout 300 module-17     # allow slower labs (default 120 s per file)
python3 labs/check_labs.py --python /path/to/python    # choose the interpreter that runs the labs
python3 labs/check_labs.py --strict        # all sessions; a session with no labs counts as a failure
```

What it does for every `*_starter.py`, `*_solution.py` and `test_*.py`:

- copies the whole session folder to a temporary folder and runs the file from its own lesson
  folder inside that copy, so nothing a lab writes can land in the kit;
- sets `LABS_OFFLINE=1`, `PINECREST_DATA=<course>/data`, `MPLBACKEND=Agg`,
  `PYTHONPATH=<kit>/labs`, `PYTHONDONTWRITEBYTECODE=1`, a private `TMPDIR`, and the mock API's
  public demo values `PINECREST_API_KEY`, `PINECREST_USER`, `PINECREST_PASSWORD` (lesson 6.4)
  unless they are already set;
- fails the file if it exits non-zero, prints a `Traceback` on stderr, or runs past the timeout;
- prints one `PASS` / `FAIL` line per file, then `N passed, M failed`; the exit code is 0 only
  when nothing failed. Asking for one session that has no lab files is a failure.

After the runs it compares a listing of the checked session folders, `labs/` and the data
folder with the listing it took before. A new, changed or missing file is a failure: some lab
wrote outside its temporary copy (usually into `DATA`).

**Which Python runs the labs:** `--python`, else the environment variable `LABS_PYTHON`, else
`~/.cache/ds-course-venv/bin/python` when it exists (the author's course environment), else the
interpreter you started the checker with. On your own machine, activate the course virtual
environment from the setup guide and run `python labs/check_labs.py`.

**How the documents refer to labs:** the facilitator guide, workbook and answer key use paths
like `labs/module-07/l2_7-time-series/`, relative to the `instructor-kit/` folder (where the
combined books live). Keep the whole `instructor-kit/` folder together so those pointers hold.
