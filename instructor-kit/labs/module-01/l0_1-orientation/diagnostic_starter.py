# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Session 1 · Diagnostic: is your Python toolkit ready? (STARTER)
# Six small functions, one for each Intro / Intermediate Python skill this course leans on.
# Nothing here is graded. Each check prints PASS or "not yet", and the last line counts them.
#
# Expected when you finish: six PASS lines and "6 of 6 checks pass."
# As handed out, the starter prints six "not yet" lines and "0 of 6 checks pass."

# %% Skill 1: slicing a list
def weekend(days):
    """Return the last two items of the list `days` as a new list."""
    # TODO 1: replace the next line
    return None

# %% Skill 2: a copy is not the same list
def with_extra(items, extra):
    """Return a NEW list: everything in `items`, then `extra`. `items` itself must not change."""
    # TODO 2: replace the next line
    return None

# %% Skill 3: counting with a dictionary
def count_values(values):
    """Return a dict that maps each value to how many times it appears."""
    # TODO 3: replace the next line
    return None

# %% Skill 4: functions return, defaults, an empty-list guard
def average(numbers, digits=2):
    """Return the mean of `numbers` rounded to `digits` places; 0.0 for an empty list."""
    # TODO 4: replace the next line
    return None

# %% Skill 5: a list comprehension over dictionaries
def big_orders(orders, limit):
    """Return the order_id of every order whose total is at least `limit` (same order as given)."""
    # TODO 5: replace the next line
    return None

# %% Skill 6: reading a CSV file, text to numbers, skipping blanks
import csv


def column_total(path, column):
    """Add up one column of a CSV file. Cells are text: convert with float(), skip empty cells."""
    # TODO 6: replace the next line
    return None


# %% The checks (do not edit below this line)
def check(label, test):
    try:
        ok = bool(test())
    except Exception as err:
        ok = False
        label += f"  ({type(err).__name__}: {err})"
    print(("PASS     " if ok else "not yet  ") + label)
    return ok


def _copy_is_safe():
    stock = ["tent", "stove"]
    result = with_extra(stock, "lamp")
    return result == ["tent", "stove", "lamp"] and stock == ["tent", "stove"]


SAMPLE = [{"order_id": 100001, "total": 434.90}, {"order_id": 100002, "total": 278.90},
          {"order_id": 100003, "total": 75.90}]
results = [
    check("1 slicing          weekend()", lambda: weekend(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]) == ["Sat", "Sun"]),
    check("2 copies           with_extra()", _copy_is_safe),
    check("3 dictionaries     count_values()", lambda: count_values(["card", "cash", "card"]) == {"card": 2, "cash": 1}),
    check("4 functions        average()", lambda: average([1, 2, 2]) == 1.67 and average([]) == 0.0 and average([1, 2, 2], 1) == 1.7),
    check("5 comprehensions   big_orders()", lambda: big_orders(SAMPLE, 200) == [100001, 100002]),
    check("6 files            column_total()", lambda: round(column_total(DATA / "daily_sales.csv", "revenue") or 0, 2) == 21539319.88),
]
print(f"{sum(results)} of {len(results)} checks pass.")
if all(results):
    print("Your Python toolkit is ready. Two years of store revenue:", f"${column_total(DATA / 'daily_sales.csv', 'revenue'):,.2f}")
else:
    print("Each 'not yet' names a skill to review before Session 2 (the workbook lists where).")
