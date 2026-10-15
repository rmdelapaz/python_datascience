# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 3.2-B · Two measures, honestly (STARTER)
# A manager wants "Asheville's visitors and the number of rainy days on one chart".
# Question: does a rainier month mean fewer visitors? And how do you show that without misleading anyone?
#
# Expected when you finish (three PNG files in output/):
#   - one figure with two twin-axis charts of the SAME data that seem to tell different stories
#   - stacked panels that share the x axis (the honest version)
#   - a temperature chart with Fahrenheit on the left and Celsius on the right (the honest use of a second axis)
#   - one printed number that answers the question directly

# %% Load and merge (done for you): Asheville, one row per month
import matplotlib.pyplot as plt
import pandas as pd

daily = pd.read_csv(DATA / "daily_sales.csv", parse_dates=["date"])
weather = pd.read_csv(DATA / "store_weather.csv", parse_dates=["date"])
ash = daily[daily["store"] == "Asheville"].merge(
    weather[weather["city"] == "Asheville"], on="date", how="left", validate="one_to_one")
ash["rainy"] = ash["precip_in"] >= 0.10
ash["month"] = ash["date"].dt.to_period("M").dt.to_timestamp()
am = ash.groupby("month").agg(visitors=("visitors", "mean"), rainy_days=("rainy", "sum"), high_f=("high_f", "mean"))
print(am.shape, "| rainy days per month from", am["rainy_days"].min(), "to", am["rainy_days"].max())

# %% Step 1: the twin axis, twice
# TODO 1: fig, axs = plt.subplots(1, 2, figsize=(10, 3.6), layout="constrained")
#         In each panel: visitors as a line on ax; right = ax.twinx(); rainy_days on `right` (dashed).
#         Left panel: right.set_ylim(0, 20). Right panel: right.set_ylim(0, 60). Save "twin_two_stories.png".
#         Looking only at the pictures, what would a reader conclude from each?

# %% Step 2: stacked panels instead
# TODO 2: fig, (top, bottom) = plt.subplots(2, 1, figsize=(9, 5), sharex=True, layout="constrained")
#         visitors on top, rainy_days as bars on the bottom, a y label on each. Save "stacked.png".

# %% Step 3: compute the relationship
# TODO 3: print am["rainy_days"].corr(am["visitors"]) rounded to 2,
#         and the mean daily visitors on rainy and on dry DAYS (group `ash` by "rainy").

# %% Step 4: one quantity, two units
# TODO 4: plot am["high_f"]; celsius = ax.secondary_yaxis("right", functions=(f_to_c, c_to_f)).
#         Write the two small conversion functions first. Save "temperature_two_units.png".
print("Expected at the end: three PNG files and one honest sentence.")
