# Session 12 labs: Correlation and Hypothesis Tests

Lessons 4.4 (Correlation Analysis) and 4.5 (Hypothesis Testing). Four guided labs and two
"find the bug" handouts. Every lab is new practice on the lesson's skills with a different
question from the lesson's project and exercises. The 4.4 labs contain no hypothesis tests and
no p-values, as in the lesson: tests start in 4.5.

Hand out the `*_starter.py` and `debug_*.py` files. Keep the `*_solution.py` files for yourself
until the lab is over.

| Lab | Practices | Minutes | Expected output (solution) |
|-----|-----------|---------|----------------------------|
| `l4_4-correlation-analysis/reviews_and_sales_*.py` | scatter plots first, Pearson and Spearman, a Spearman matrix and an annotated heatmap saved to `OUTPUT`, a partial correlation, reverse causation | 12 | 234 products; reviews and units sold: Pearson 0.456, Spearman 0.442; rating: 0.095 and 0.012; price: -0.319 and -0.600; reviews and units controlling for price 0.424 |
| `l4_4-correlation-analysis/staffing_rule_*.py` | `stats.linregress`, slope and intercept in units, r squared, the typical miss, one line per group, the reversed regression, what a slope does not say | 15 (finish at home) | 1.59 staff per 100 visitors, intercept 0.84, r 0.925, r squared 0.856; 7.2 staff predicted for 400 visitors, give or take 0.95; store slopes 1.55 to 1.63; the reversed slope is 53.9 visitors per staff member, not 63.0 |
| `l4_4-correlation-analysis/debug_correlation_claims.py` | four wrong readings of r: a NumPy `nan`, r read as a slope, r read as a percentage, r = 0 read as "unrelated" | 5 to 8 (stretch) | as shipped: `nan`, "94 cents", "90%", and 0.0 for a perfect curve |
| `l4_5-hypothesis-testing/returned_order_size_*.py` | hypotheses written first, Welch t-test with its CI, Cohen's d, a permutation test, challenging a result with a confounder, a full report | 15 | returned 1,143 orders (mean 218.72), completed 18,762 (193.17); difference 25.54, 95% CI 15.29 to 35.79, p = 1.1e-06, d = 0.14; permutation p 0.0002; online only 23.85 (CI 12.29 to 35.42), d = 0.12 |
| `l4_5-hypothesis-testing/footwear_returns_*.py` | `pd.crosstab`, rates and their ratio, `chi2_contingency` with expected counts, Cramér's V, a non-significant result worded honestly, Holm correction | 15 (finish at home) | online: 14.4% against 4.8% (3.0 times), chi-square 313.8, p = 3.3e-70, smallest expected count 197.6, V = 0.157; store: 3.8% against 3.3%, p = 0.43 |
| `l4_5-hypothesis-testing/debug_test_report.py` | five wrong conclusions: `nan` from a missing value, p read as the probability of the null, "not significant" read as "the same", significant read as big, a one-sided test chosen after looking | 5 to 8 (stretch) | as shipped: `nan`, "3% chance", "equally likely", "big problem", p = 0.015 one-sided |

## How to run

From any folder, with the course environment active:

```bash
python labs/module-12/l4_4-correlation-analysis/reviews_and_sales_starter.py
python labs/module-12/l4_5-hypothesis-testing/returned_order_size_starter.py
```

or open a file in VS Code and run it cell by cell (the `# %%` lines are cell markers).

- `reviews_and_sales` saves two charts into an `output/` folder next to the lab file (`OUTPUT`).
  It never calls `plt.show()`: open the saved files.
- `footwear_returns` uses `statsmodels` (for `multipletests`); it is in the course environment.
- The permutation test in `returned_order_size` takes a few seconds.

## Check all of them

```bash
python3 labs/check_labs.py module-12
```

Eight lines should say `PASS` (four starters, four solutions). The two `debug_*.py` handouts are
wrong on purpose and are not run by the checker; both still run to the end without an error.

## Timing in the session

| Clock | Lab |
|-------|-----|
| 0:45 to 1:05 | `reviews_and_sales` (everyone), then `staffing_rule` Steps 1 and 2 (the rest at home) |
| 2:10 to 2:35 | `returned_order_size` (everyone), then `footwear_returns` Step 1 (Steps 2 to 4 at home) |

Early finishers take the matching `debug_*.py` handout.
