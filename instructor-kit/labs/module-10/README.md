# Session 10 labs: Saving Figures; Center and Spread

Lessons 3.4 (Saving Figures) and 4.1 (Descriptive Statistics I: Center and Spread).
Four guided labs and two "find the bug" handouts. Every lab is new practice on the lesson's
skills with a different question from the lesson's project and exercises.

Hand out the `*_starter.py` and `debug_*.py` files. Keep the `*_solution.py` files for yourself
until the lab is over.

| Lab | Practices | Minutes | Expected output (solution) |
|-----|-----------|---------|----------------------------|
| `l3_4-saving-figures/pixel_budget_*.py` | `fig.savefig`, pixels = inches x dpi, same pixels from two sheet sizes, PDF and SVG, closing figures | 12 | email image `(700, 350)`; both newsletter images `(1400, 700)`; `5 files`; `open figures: 0` |
| `l3_4-saving-figures/category_price_pack_*.py` | a `PRESETS` table, `new_figure()` and `save_chart()`, a create-draw-save-close loop, `PdfPages`, a manifest that verifies the files | 15 (finish at home) | 7 files: three web PNGs at 960 x 480, three slide PNGs at 1920 x 1080, `price_ranges.pdf` with 3 pages; `open figures: 0` |
| `l3_4-saving-figures/debug_blank_slide.py` | finding three silent export mistakes: `plt.savefig()` on the wrong figure, `bbox_inches="tight"` changing the size, a huge sheet making tiny text | 5 to 8 (stretch) | as shipped: `saved size: 660 x 500`, `slide is blank: True`, `open figures: 2`. Fixed: `1920 x 1080: True`, `blank: False`, `open figures: 0` |
| `l4_1-center-and-spread/orders_per_buyer_*.py` | mean, median, mode; the mean of a boolean is a proportion; which center multiplies back to a total | 12 | 3,942 buyers; mean 5.15, median 4.0, mode 1; 65.1% of buyers below the mean; mean x buyers = 20302, median x buyers = 15768 |
| `l4_1-center-and-spread/visitor_spread_*.py` | variance by hand, `ddof=0` and `ddof=1`, range, SD and IQR by group, a robustness stress test | 15 (finish at home) | five-day variance 510.96 (divide by n) and 638.7 (n - 1); smallest SD Asheville 89.5, largest Boise 161.8; a bad row moves Bend's SD from 109.1 to 302.8 and leaves the IQR at 131.25 |
| `l4_1-center-and-spread/debug_average_of_averages.py` | finding three quiet summary mistakes: averaging averages, `np.mean` on missing values, two `ddof` defaults | 5 to 8 (stretch) | as shipped: `$ 190.56` (the true mean is 194.60), `$ nan` (the true mean is 7435.04), and SDs of 37.13 and 40.1 for the same seven days |

## How to run

From any folder, with the course environment active:

```bash
python labs/module-10/l3_4-saving-figures/pixel_budget_starter.py
python labs/module-10/l4_1-center-and-spread/orders_per_buyer_starter.py
```

or open a file in VS Code and run it cell by cell (the `# %%` lines are cell markers).

- The chart labs save into an `output/` folder next to the lab file (`OUTPUT` from `labs_paths`).
  They never call `plt.show()`: open the saved files to look at them, which is the habit the
  lesson teaches.
- Every starter runs as shipped and prints what is still to do. A `TODO` is finished when the
  printed result matches the "Expected" lines at the top of the file.
- File sizes in kilobytes can differ a little between computers (fonts). Pixel sizes do not.

## Check all of them

```bash
python3 labs/check_labs.py module-10
```

Eight lines should say `PASS` (four starters, four solutions). The two `debug_*.py` handouts are
broken on purpose and are not run by the checker; both still run to the end without an error.

## Timing in the session

| Clock | Lab |
|-------|-----|
| 0:45 to 1:05 | `pixel_budget` (everyone), then `category_price_pack` TODO 1 and 2 (the rest at home) |
| 2:10 to 2:35 | `orders_per_buyer` (everyone), then `visitor_spread` Steps 1 to 3 (Steps 4 and 5 at home) |

Early finishers take the matching `debug_*.py` handout.
