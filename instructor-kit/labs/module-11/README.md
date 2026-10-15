# Session 11 labs: Shape, Outliers and Distributions

Lessons 4.2 (Descriptive Statistics II: Shape, Position and Outliers) and 4.3 (Probability
Distributions). Four guided labs and two "find the bug" handouts. Every lab is new practice on
the lesson's skills with a different question from the lesson's project and exercises.

Hand out the `*_starter.py` and `debug_*.py` files. Keep the `*_solution.py` files for yourself
until the lab is over.

| Lab | Practices | Minutes | Expected output (solution) |
|-----|-----------|---------|----------------------------|
| `l4_2-shape-position-outliers/catalog_weights_*.py` | `.skew()`, a log transform, `.quantile([...])`, a share from a boolean, IQR fences against z-scores, investigating flags before removing anything, a grouped summary with n | 12 | 228 of 242 products have a weight; skew 3.46 (0.18 after a log); IQR fences -0.872 to 1.908 kg flag 26 products, `abs(z) > 3` flags 4 (a cooler and three 6-person tents); median 0.35 kg; nothing removed |
| `l4_2-shape-position-outliers/price_satisfaction_*.py` | ordinal data: counts and percents, median, top-two and bottom-two shares by group with named aggregation, who skipped the question, a stacked bar saved to `OUTPUT` | 15 (finish at home) | ages 18-24: n 186, 19.4% satisfied and 38.2% dissatisfied, against 44% and 15% for the other 1,567; every group skipped at about 2 to 3%; `price_satisfaction_by_age.png` is 990 x 440 pixels |
| `l4_2-shape-position-outliers/debug_summary_report.py` | finding four quiet reporting mistakes | 5 to 8 (stretch) | as shipped: "90% of orders are below $ 13.5" (the right figure is 405.395), a box plot whose median is `nan`, a mean order id, and group means with no n |
| `l4_3-probability-distributions/conversion_model_*.py` | freezing `stats.norm`, checking the 68-95-99.7 rule against data, `cdf`, `sf`, `ppf`, `rvs` with one seeded generator | 13 | conversion mean 0.2354, SD 0.0271, skew 0.05; within 1, 2, 3 SD: data 69.4%, 95.6%, 99.5%; P(below 20%) model 0.096, data 0.090; 5th percentile model 0.1908, data 0.1920; 34 simulated days below 20% in a year (the model expects 34.9) |
| `l4_3-probability-distributions/lines_per_order_ci_*.py` | sample mean, standard error two ways, a 95% t interval, SD against SE, checking coverage by simulation, how the width shrinks with n | 15 (finish at home) | true mean 2.241 lines; the sample of 150 gives 2.093, SE 0.0821, 95% CI 1.931 to 2.256; 95.2% of 5,000 intervals contain the true mean; median width 0.358 at n = 150 and 0.179 at n = 600 |
| `l4_3-probability-distributions/debug_delivery_model.py` | finding four quiet modeling mistakes: variance passed as `scale`, `uniform(loc, scale)` read as (low, high), `sf` off by one, a generator re-created in a loop | 5 to 8 (stretch) | as shipped: 0.257 (the data says 0.019), 0.6 with a range of 10 to 30, 0.024 (the right figure is 0.072), and one distinct simulated count |

## How to run

From any folder, with the course environment active:

```bash
python labs/module-11/l4_2-shape-position-outliers/catalog_weights_starter.py
python labs/module-11/l4_3-probability-distributions/conversion_model_starter.py
```

or open a file in VS Code and run it cell by cell (the `# %%` lines are cell markers).

- `price_satisfaction` saves its chart into an `output/` folder next to the lab file (`OUTPUT` from
  `labs_paths`). It never calls `plt.show()`: open the saved file to look at it.
- The two 4.3 labs use a seeded random generator, created once at the top. Run the file from top to
  bottom and you get exactly the numbers above. Run a cell twice in a notebook and the later random
  results change a little; the conclusions do not.
- Every starter runs as shipped and prints what is still to do.

## Check all of them

```bash
python3 labs/check_labs.py module-11
```

Eight lines should say `PASS` (four starters, four solutions). The two `debug_*.py` handouts are
wrong on purpose and are not run by the checker; both still run to the end without an error.

## Timing in the session

| Clock | Lab |
|-------|-----|
| 0:45 to 1:05 | `catalog_weights` (everyone), then `price_satisfaction` TODO 1 to 3 (the rest at home) |
| 2:10 to 2:35 | `conversion_model` (everyone), then `lines_per_order_ci` Steps 1 to 4 (Steps 5 and 6 at home) |

Early finishers take the matching `debug_*.py` handout.
