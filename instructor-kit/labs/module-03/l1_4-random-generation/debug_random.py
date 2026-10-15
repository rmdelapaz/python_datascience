# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Handout 1.4 · Four random bugs (find the bug)
# Wrong random output looks exactly as random as right output, so each block prints a CHECK.
# Blocks 1 to 3 run without an error and are wrong. Block 4 stops with an error.
#
# Correct answers:
#     Block 1: smallest roll 1, largest roll 6
#     Block 2: the deck prints as ten shuffled numbers, not None
#     Block 3: 3 different weeks (the three lines are not identical)
#     Block 4: three different store names

# %%
import numpy as np

# %% Block 1: a six-sided die
rng = np.random.default_rng(1)
rolls = rng.integers(1, 6, size=10_000)
print("Block 1: smallest roll", rolls.min(), "largest roll", rolls.max())

# %% Block 2: shuffle a deck of ten cards
deck = np.arange(10)
deck = rng.shuffle(deck)
print("Block 2:", deck)

# %% Block 3: simulate three different weeks of visitor counts
weeks = []
for week in range(3):
    week_rng = np.random.default_rng(42)
    weeks.append(week_rng.integers(200, 500, size=7))
    print("        ", weeks[-1])
print("Block 3:", len({tuple(w) for w in weeks}), "different weeks")

# %% Block 4: pick three DIFFERENT stores, where Boise is twice as likely as each of the others
names = np.array(["Asheville", "Bend", "Boise", "Flagstaff"])
picked = rng.choice(names, size=3, replace=False, p=[0.2, 0.2, 0.4, 0.1])
print("Block 4:", picked)
