# Session 8 labs: Features and First Charts

Four labs for lessons 2.9 (Feature Engineering Basics) and 3.1 (Line, Scatter and Bar Charts). Each asks a question the lesson did not ask, on the same Pinecrest data. The first lab of each lesson is the guided lab done in the room; the second is for early finishers and homework. The two chart labs save PNG files to an `output/` folder next to the lab file and never call `plt.show()`.

| Lab | Files | Practices | Time |
|-----|-------|-----------|------|
| Lab 2.9-A · Which orders come back? | `l2_9-feature-engineering/order_features_*.py` | choosing a unit of analysis (an order), flags, a per-entity aggregate joined back with a left merge, qcut and cut, checking each feature against the target with rate and size, and an interaction feature. | 25 minutes, in class |
| Lab 2.9-B · How busy will the store be tomorrow? | `l2_9-feature-engineering/store_day_features_*.py` | a ratio within a group (transform), bins with open outer edges, a window feature built on the completed calendar (Lesson 2.7 meets 2.8), and a leak audit where the cutoff is a time of day. | 20 minutes, early finishers or homework |
| Lab 3.1-A · Four questions, four charts | `l3_1-line-scatter-bar/four_questions_*.py` | choosing the chart from the question; the five-line pattern four times; aggregating before a line and a bar and not before a scatter or a histogram; bar_label, alpha, axvline; saving with fig.savefig. | 25 minutes, in class |
| Lab 3.1-B · Chart repair | `l3_1-line-scatter-bar/chart_repair_*.py` | recognizing the three silent chart mistakes from the lesson on new data, and fixing the cause in pandas, not the symptom in Matplotlib. | 20 minutes, early finishers or homework |

## How to run

From any folder (the labs find the course data through `labs_paths.py`, one level above this folder):

```bash
python labs/module-08/l2_9-feature-engineering/order_features_starter.py
python3 labs/check_labs.py module-08        # runs every starter and solution: all PASS
```

Each file has `# %%` cell markers, so it also opens as notebook cells in VS Code and Jupyter. Every starter runs
without error as shipped and prints which TODOs are still open. Hand out the `*_starter.py` files only; the
`*_solution.py` files are the instructor's reference.

## Lab 2.9-A · Which orders come back?

**Question.** The returns desk asks which kinds of orders get returned. One row is an order. Build flags, per-order summaries from the order lines, and bins; check each against the return rate; then find the combination that stands out.

**Done looks like:** an overall return rate near 5.6%; six small tables; one combination of two features with a return rate about three times any other; a sentence about `status`.

Expected output of `l2_9-feature-engineering/order_features_solution.py`:

```text
orders: (20302, 11) | order lines: (45490, 5)
per_order rows: 20302
rows before and after the merge: 20302 20302 | orders with no lines: 0
missing after binning: 0 0
overall return rate: 0.0563
            mean   size
is_online              
False      0.034   7448
True       0.069  12854
             mean   size
used_promo              
False       0.057  18154
True        0.054   2148
             mean   size
is_weekend              
False       0.057  13690
True        0.054   6612
               mean   size
has_footwear              
False         0.042  15960
True          0.107   4342
             mean  size
value_band             
low         0.044  5091
mid         0.049  5062
high        0.068  5074
top         0.065  5075
             mean  size
lines_band             
1           0.043  5890
2           0.053  7244
3-4         0.069  6400
5+          0.074   768
                  mean   size
online_footwear              
False            0.042  17448
True             0.144   2854
                         mean   size
is_online has_footwear              
False     False         0.033   5960
          True          0.038   1488
True      False         0.048  10000
          True          0.144   2854
TODO 7: `status` IS the answer. returned is computed from it, so a table that keeps status as a feature
has the target written into it. Drop it (and anything else recorded after the order shipped).
```

## Lab 2.9-B · How busy will the store be tomorrow?

**Question.** One row is a store on a day, and the thing to predict is `visitors`. The cutoff rule here is "known the evening before". Build a ratio, date parts, temperature bands and a same-weekday-last-week feature, then audit every candidate column.

**Done looks like:** 2,903 rows throughout; four temperature bands with no missing values; relative traffic rising from cold to hot days; a count of rows where the two lag columns disagree; a verdict for seven columns.

Expected output of `l2_9-feature-engineering/store_day_features_solution.py`:

```text
rows before and after: 2903 2903
           visitors  rel_visitors
store                            
Asheville    274.90           1.0
Bend         334.87           1.0
Boise        485.17           1.0
Flagstaff    328.46           1.0
temp_band
cold     432
cool     932
warm    1012
hot      527
missing temp_band: 0
            mean  size
temp_band             
cold       0.824   432
cool       0.937   932
warm       1.054  1012
hot        1.153   527
        mean  size
rainy             
False  1.027  2514
True   0.823   389
            mean  size
promo_day             
0          0.976  2807
1          1.699    96
             mean  size
is_weekend             
False       0.858  2071
True        1.353   832
rows where 7 rows back is not 7 days back: 104
      date     store  visitors  lag7_rows  lag7_calendar
2024-11-29 Asheville       390      212.0          290.0
2024-11-30 Asheville       651      290.0          299.0
2024-12-01 Asheville       507      299.0          374.0
lag7_calendar  r =  0.86   feature: last week is in the past
staff_on_duty  r =  0.93   feature: the schedule is fixed in advance (but it encodes someone's forecast)
promo_day      r =  0.32   feature: the sale calendar is planned
high_f         r =  0.27   only as a FORECAST made the evening before, not the measured high
transactions   r =  0.96   LEAK: counted during the day being predicted
units          r =  0.96   LEAK: counted during the day being predicted
revenue        r =  0.94   LEAK: counted during the day being predicted
```

## Lab 3.1-A · Four questions, four charts

**Question.** Four questions about Pinecrest's customers and products. For each one, decide the chart type from the question before you read the TODO, draw it with a title and labeled axes, and save it.

**Done looks like:** four PNG files in `output/`; a line with 7 points; 5 horizontal bars with the longest on top; a scatter of the products that have a weight; a histogram with a dashed line at the median price.

Expected output of `l3_1-line-scatter-bar/four_questions_solution.py`:

```text
customers: (4850, 12) | products: (242, 13)
signup_date
2019    651
2020    665
2021    657
2022    614
2023    676
2024    838
2025    749
Q1 line: 1 line with 7 points; best year 2024 with 838
Q2 bars: 5 bars; top bar is organic with 1517
Q3 scatter: 228 dots, 14 products without a weight; correlation 0.69
Q4 histogram: 30 bins, each 20.28 dollars wide; median 82.95 | products above $300: 21
saved: ['q1_signups.png', 'q2_channels.png', 'q3_weight_price.png', 'q4_prices.png']
```

## Lab 3.1-B · Chart repair

**Question.** The starter runs with no error and draws three charts that are wrong. For each, read the printed clue, say what the chart is really showing, fix the cause and save the fixed chart.

**Done looks like:** 4 sorted bars showing totals; a line that breaks on January 21 and 22; a handful of date ticks.

Expected output of `l3_1-line-scatter-bar/chart_repair_solution.py`:

```text
Chart 1: was 1145 bars (largest single order per method: {'card': 3779.45, 'cash': 702.25, 'digital_wallet': 640.8, 'gift_card': 840.6} )
         now 4 bars: {'card': 132538.28, 'digital_wallet': 46513.22, 'gift_card': 16563.08, 'cash': 12888.0}
Chart 2: was 17 rows; now 19 days with 2 NaN on ['2025-01-21', '2025-01-22']
Chart 3: dtype is now datetime64[us] and the x axis has 9 ticks (it had 731)
saved: ['fixed_1_payment.png', 'fixed_2_visitors.png', 'fixed_3_temperature.png']
```
