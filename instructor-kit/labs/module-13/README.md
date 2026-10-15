# Session 13 labs · A/B Testing and the EDA Workflow (Lessons 4.6 + 4.7, Checkpoint 1)

New practice on the two lessons' skills, using the course data. Every lab asks a question the
lesson pages do not answer. Starters run as shipped and say which TODOs are still open;
solutions print the reference answers quoted below. All labs read from `DATA` and write
nothing, except the checkpoint model answer, which saves one figure to `OUTPUT`.

| Lab | Practices | Where | Minutes | Expected output (solution) |
|-----|-----------|-------|---------|----------------------------|
| `l4_6-ab-testing/novelty_check_*.py` | `compare_rates` on slices, intervals instead of p-values, testing the difference between two lifts | room | 20 | weekly lifts +1.05, +0.76, +0.80, +2.08 points (only week 4 has p < 0.05); halves +0.91 and +1.43; difference +0.52 points, p = 0.46: no novelty effect |
| `l4_6-ab-testing/followup_test_plan_*.py` | `proportion_effectsize`, `NormalIndPower().solve_power` and `.power`, visitors into days | fast finishers / home | 20 | mobile baseline 6.8%, 552 visitors a day; 16,376 / 7,458 / 3,432 per arm for 7.6% / 8.0% / 8.6%; 28 days gives 81% power for 8.0%; the raw-difference mistake gives 109,012 |
| `l4_6-ab-testing/aa_test_*.py` | a seeded NumPy simulation, false-alarm rate | stretch | 15 | 4.9% of 2,000 A/A splits have p < 0.05; 0.8% below 0.01; smallest p 0.0021 |
| `l4_7-eda-workflow/shipping_rules_*.py` | EDA steps 3 to 7 on one column: quality, one variable, a derived column, two variables, a written note | room | 20 | stores never pay; online 71.4% / 21.4% / 7.2% at 0.00 / 6.95 / 14.95; goods of 75.00 or more ship free, under 75.00 pay 6.95, no exceptions; 14.95 on about 7% of orders at every size |
| `l4_7-eda-workflow/order_size_scan_*.py` | a segment scan with Holm, then a competing explanation | home (room if time) | 25 | 22 tests, 4 below 0.05 before correction, 1 after (June: median 169.40 against 154.95); 17.7% of June orders contain a tent against 10.4%; within tent / non-tent orders p = 0.60 / 0.14 |
| `l4_7-eda-workflow/customer_overview_*.py` | `overview()`, "missing for whom?", a merge with `validate` and `indicator` | stretch | 20 | phone 5.8% and birth_year 9.1% missing, no pattern by channel or tier (p 0.43 to 0.85); 739 orders from 150 customer ids have no customer row |
| `checkpoint-1/checkpoint1_starter.py` | Checkpoint 1 scaffold: the question, the load line, six empty headings | room, 2:15 | 30 | prints the unfilled plan and note |
| `checkpoint-1/checkpoint1_solution.py` | Checkpoint 1 model answer (instructor only) | n/a | n/a | December 44.95 against 41.65 per unit: +3.31 (+7.9%), 95% CI 2.97 to 3.65, Cohen's d 1.33; all four stores; against March to October +3.84 (+9.3%) |

Hand out the `*_starter.py` files only. `checkpoint1_solution.py` is the model answer for the
checkpoint: keep it back until every group has sat the checkpoint.

Run one (from the kit folder, or from any folder):

    python labs/module-13/l4_6-ab-testing/novelty_check_starter.py

Each file is split into `# %%` cells, so it also opens as a notebook in VS Code or Jupyter.

Check all: `python3 labs/check_labs.py module-13` (expect `14 passed, 0 failed`).

Helper functions these labs define (copied from the lessons, so learners can keep them):
`compare_rates(df)` and `describe(label, r)` (Lesson 4.6), `p_two_prop(c1, n1, c2, n2)` (Lesson 4.6),
`overview(df)` (Lesson 4.7), `cohens_d(x, y)` (Lesson 4.5, in the checkpoint model answer).
