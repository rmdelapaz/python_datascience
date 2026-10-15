"""check_environment.py: is this computer ready for Python Data Science?

Run it from a terminal with the course environment active:

    python check_environment.py

It checks four things and tells you exactly what to fix:
  1. Python is 3.12 or newer
  2. a virtual environment is active
  3. every course package imports (and prints its version)
  4. the Pinecrest course data can be found and has every file

The last line is either "READY for Python Data Science" or "NOT READY" with a numbered fix list.
This file is a tool, not an exercise: there is nothing to edit.
"""
import importlib
import os
import pathlib
import platform
import sys

# (name you import, name on the pip line, where it is first needed, must it be there today?)
PACKAGES = [
    ("numpy", "numpy", "Module 1", True),
    ("pandas", "pandas", "Module 2", True),
    ("pyarrow", "pyarrow", "Module 2", True),
    ("matplotlib", "matplotlib", "Module 3", True),
    ("seaborn", "seaborn", "Module 7", True),
    ("scipy", "scipy", "Module 4", True),
    ("statsmodels", "statsmodels", "Module 4", True),
    ("jupyterlab", "jupyterlab", "notebooks in JupyterLab", False),
    ("openpyxl", "openpyxl", "Lesson 2.2", True),
    ("sqlalchemy", "SQLAlchemy", "Module 5", True),
    ("pymongo", "pymongo", "Lesson 5.5", True),
    ("mongomock", "mongomock", "Lesson 5.5", True),
    ("requests", "requests", "Module 6", True),
    ("bs4", "beautifulsoup4", "Lesson 6.2", True),
    ("lxml", "lxml", "Lesson 6.2", True),
    ("selenium", "selenium", "Lesson 6.3", True),
    ("plotly", "plotly", "Lesson 7.2", True),
    ("kaleido", "kaleido", "static Plotly images in Lesson 7.2", False),
    ("bokeh", "bokeh", "Lesson 7.3", True),
    ("streamlit", "streamlit", "Lesson 7.4", True),
]

DATA_FILES = [
    "orders.csv", "customers.csv", "products.csv", "order_items.csv", "orders_messy.csv",
    "daily_sales.csv", "store_weather.csv", "survey.csv", "ab_test.csv",
    "web_sessions.json", "pinecrest.db", "sales_2025.xlsx",
]

fixes = []      # things that must be fixed before Session 2
notes = []      # things that can wait


def line(mark, label, detail=""):
    print(f"  {'[' + mark + ']':<7}{label:<22} {detail}")


def find_data():
    """The folder that holds orders.csv: PINECREST_DATA, or a data/ folder here or in any folder above."""
    env = os.environ.get("PINECREST_DATA", "").strip()
    if env:
        return pathlib.Path(env).expanduser()
    starts = [pathlib.Path.cwd(), pathlib.Path(__file__).resolve().parent]
    for start in starts:
        for folder in [start, *start.parents]:
            if (folder / "data" / "orders.csv").is_file():
                return folder / "data"
    return None


print("Python Data Science: environment check")
print("=" * 60)

# 1. Python version
print("1. Python")
version = sys.version.split()[0]
if sys.version_info >= (3, 12):
    line("ok", "Python " + version, platform.system() + " " + platform.machine())
else:
    line("FIX", "Python " + version, "the course needs 3.12 or newer")
    fixes.append("Install Python 3.12 or newer from python.org, then rebuild the environment "
                 "(delete .venv, create it again, install from requirements.txt).")
print("       running from:", sys.executable)

# 2. Virtual environment
print("2. Virtual environment")
in_venv = sys.prefix != sys.base_prefix or bool(os.environ.get("CONDA_PREFIX"))
if in_venv:
    line("ok", "environment active", pathlib.Path(sys.prefix).name)
else:
    line("FIX", "no environment active", "this is the computer-wide Python")
    fixes.append("Activate the course environment in THIS terminal, then run the check again:\n"
                 "       Windows PowerShell:  .venv\\Scripts\\Activate.ps1\n"
                 "       macOS / Linux:       source .venv/bin/activate")

# 3. Packages
print("3. Course packages")
missing = []
for module, pip_name, first_used, core in PACKAGES:
    try:
        mod = importlib.import_module(module)
    except Exception as err:            # ImportError, or a broken install raising something else
        if core:
            line("FIX", pip_name, f"not importable ({type(err).__name__}); first needed in {first_used}")
            missing.append(pip_name)
        else:
            line("note", pip_name, f"not installed; needed for {first_used}")
            notes.append(f"{pip_name} is missing. It is needed for {first_used}; "
                         "python -m pip install -r requirements.txt installs it.")
        continue
    line("ok", pip_name, getattr(mod, "__version__", "installed"))
if missing:
    fixes.append("Install the missing packages with the environment active:\n"
                 "       python -m pip install -r requirements.txt\n"
                 "     (missing: " + ", ".join(missing) + ")")

# 4. Course data
print("4. Course data")
data = find_data()
if data is None or not (data / "orders.csv").is_file():
    line("FIX", "data folder", "not found")
    fixes.append("Unzip the course data so that a data folder sits in your project folder:\n"
                 "       python -m zipfile -e pinecrest-data.zip .\n"
                 "     then run this check from the project folder (the one that contains data/).")
else:
    line("ok", "data folder", str(data))
    absent = [name for name in DATA_FILES if not (data / name).is_file()]
    if absent:
        line("FIX", "files missing", ", ".join(absent))
        fixes.append("Unzip pinecrest-data.zip again: these files are missing from the data folder: "
                     + ", ".join(absent))
    else:
        line("ok", f"{len(DATA_FILES)} data files", "all present")
        with open(data / "orders.csv", encoding="utf-8") as f:
            rows = sum(1 for _ in f) - 1
        if rows == 20302:
            line("ok", "orders.csv", f"{rows:,} orders")
        else:
            line("FIX", "orders.csv", f"{rows:,} rows, expected 20,302")
            fixes.append("orders.csv does not have 20,302 rows. Download pinecrest-data.zip again and unzip it.")

print("=" * 60)
for text in notes:
    print("Note:", text)
if fixes:
    print("NOT READY. Fix before Session 2:")
    for number, text in enumerate(fixes, start=1):
        print(f"  {number}. {text}")
    print("Then run this check again. Stuck? Show this output to your instructor.")
else:
    print("READY for Python Data Science")
