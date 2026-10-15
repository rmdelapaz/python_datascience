# Session 9 labs: Composing and Customizing Figures

Four labs for lessons 3.2 (Subplots and Composition) and 3.3 (Customizing Plots). Each asks a question the lesson did not ask, on the same Pinecrest data. The first lab of each lesson is the guided lab done in the room; the second is for early finishers and homework. Every lab saves its charts as PNG files to an `output/` folder next to the lab file and never calls `plt.show()`.

| Lab | Files | Practices | Time |
|-----|-------|-----------|------|
| Lab 3.2-A · Foot traffic on one page | `l3_2-subplots-composition/traffic_panels_*.py` | a grid and its array, zip(axs.flat, ...), separate against shared scales, suptitle and supylabel, a panel-drawing function for small multiples, and subplot_mosaic with named panels. | 25 minutes, in class |
| Lab 3.2-B · Two measures, honestly | `l3_2-subplots-composition/honest_axes_*.py` | twinx() and why it misleads, stacked panels with sharex=True, computing the relationship instead of drawing two lines, and secondary_yaxis with a pair of conversion functions. | 20 minutes, early finishers or homework |
| Lab 3.3-A · From first draft to finished chart | `l3_3-customizing-plots/finish_chart_*.py` | checking a finding with numbers, a headline with a subtitle, FuncFormatter, set_xticks with labels, gray plus one, direct labels, an annotation with an arrow, and clean-up, all as small functions that take an ax. | 25 minutes, in class |
| Lab 3.3-B · Give color a job | `l3_3-customizing-plots/color_jobs_*.py` | choosing a palette type from the data (sequential against diverging), ax.imshow with aspect="auto", a colorbar as the legend of a colormap, tick labels for a grid, and centering a diverging map. | 20 minutes, early finishers or homework |

## How to run

From any folder (the labs find the course data through `labs_paths.py`, one level above this folder):

```bash
python labs/module-09/l3_2-subplots-composition/traffic_panels_starter.py
python3 labs/check_labs.py module-09        # runs every starter and solution: all PASS
```

Each file has `# %%` cell markers, so it also opens as notebook cells in VS Code and Jupyter. Every starter runs
without error as shipped and prints which TODOs are still open. Hand out the `*_starter.py` files only; the
`*_solution.py` files are the instructor's reference.

## Lab 3.2-A · Foot traffic on one page

**Question.** Which store's foot traffic is growing, and how big is each store's traffic next to the others? Build the same grid twice (own scales, then shared), then small multiples with gray context, then a one-store summary with a named layout.

**Done looks like:** four PNG files in `output/`; four different y ranges, then `True`; four lines in every small-multiples panel; the panel names `['trend', 'week', 'spread']`.

Expected output of `l3_2-subplots-composition/traffic_panels_solution.py`:

```text
monthly mean visitors: (24, 4) ['Asheville', 'Bend', 'Boise', 'Flagstaff']
change in mean daily visitors, 2025 vs 2024 (%): {'Asheville': -7.5, 'Bend': 2.5, 'Boise': 9.2, 'Flagstaff': 21.0}
Step 1 y ranges: [(203, 341), (238, 418), (303, 629), (191, 446)]
Step 2 same y range in every panel: True
Step 3 lines per panel: [4, 4, 4, 4]
Flagstaff rows: 725
Step 4 panels: ['trend', 'week', 'spread'] | busiest weekday: Sat 482 | quietest: 252
saved: ['flagstaff_summary.png', 'grid_own_scales.png', 'grid_shared.png', 'small_multiples.png']
```

## Lab 3.2-B · Two measures, honestly

**Question.** A manager wants Asheville's visitors and the number of rainy days on one chart. Make the twin-axis version tell two different stories, then show the data honestly, compute the relationship directly, and finish with the one honest use of a second axis.

**Done looks like:** three PNG files; a correlation near 0.3; a clear per-day difference; a temperature chart with two agreeing scales.

Expected output of `l3_2-subplots-composition/honest_axes_solution.py`:

```text
(24, 3) | rainy days per month from 3 to 13
Step 1: same data, two right-axis ranges; figure has 4 Axes
Step 3: monthly correlation of rainy days and visitors: 0.28
        mean visitors on dry days: 286.8 | on rainy days: 236.4 (-17.6%)
Step 4: warmest month 2025-08, 86.6 °F = 30.3 °C
saved: ['stacked.png', 'temperature_two_units.png', 'twin_two_stories.png']
```

## Lab 3.3-A · From first draft to finished chart

**Question.** The online team will show one chart at the year-end meeting: completed online revenue by month, 2024 against 2025. Check the story with numbers, then edit the first draft until a stranger gets the point in five seconds.

**Done looks like:** `draft.png` and `finished.png`; 12 of 12 months; y labels like `$20K`; month names on the x axis; only the left and bottom spines; no legend.

Expected output of `l3_3-customizing-plots/finish_chart_solution.py`:

```text
year      2024     2025
month                  
1      73567.0  86269.0
2      70712.0  86043.0
3      80882.0  96183.0
months in which 2025 beat 2024: 12 of 12
largest gap: Aug, $33,144 | smallest gap: Dec, $4,803
full year: $1,077,801 -> $1,280,184 (18.8%)
y tick labels: ['$0K', '$20K', '$40K', '$60K']
x tick labels: ['Jan', 'Feb', 'Mar', 'Apr'] ...
visible spines: ['left', 'bottom']
legend: None
saved: ['draft.png', 'finished.png']
```

## Lab 3.3-B · Give color a job

**Question.** Two store-by-month tables need two different kinds of color: mean visitors (low to high: sequential) and revenue change against 2024 (above or below zero: diverging, centered). Draw both as heatmaps and check what the colors claim.

**Done looks like:** two PNG files; the change map's color limits symmetric around zero; shrinking months per store printed.

Expected output of `l3_3-customizing-plots/color_jobs_solution.py`:

```text
visitors table: (4, 12) | change table: (4, 12)
Step 1: lowest cell 214, highest cell 588
Step 2: changes from -12.6% to 29.0%; color limits -29.0 to 29.0
Step 3: months that shrank against 2024: {'Asheville': 9, 'Bend': 5, 'Boise': 0, 'Flagstaff': 0}
saved: ['heat_change.png', 'heat_visitors.png']
```
