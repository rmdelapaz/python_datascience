# Session 7 labs: Time Series and Windows

Four labs for lessons 2.7 (Time Series) and 2.8 (Window Functions). Each one asks a question the lesson did not ask, on the same Pinecrest data. The first lab of each lesson is the guided lab done in the room; the second is for early finishers and homework. No lab writes a file or draws a chart.

| Lab | Files | Practices | Time |
|-----|-------|-----------|------|
| Lab 2.7-A · An honest weekly calendar | `l2_7-time-series/units_calendar_*.py` | the order of operations on a new column (units) and a new bucket (weeks). units has no blank values, so after zeroing the four closed days the only unknowns are the five failed-export days (Bend 3, Flagstaff 2). | 25 minutes, in class |
| Lab 2.7-B · Is the online return rate getting worse? | `l2_7-time-series/returns_trend_*.py` | resample(..., on=) on a table whose dates are a column; the mean of a True/False column as a rate; diff(12) for year over year in percentage points; and reading a noisy series without inventing a story. | 20 minutes, early finishers or homework |
| Lab 2.8-A · Foot traffic: when did Flagstaff pass Bend? | `l2_8-window-functions/foot_traffic_*.py` | rolling().mean() and its NaN edge, min_periods, comparing two smoothed series, cummax() for records, and rolling().sum() with idxmax() for a best stretch. Everything is on the wide calendar, so no grouping is needed. | 25 minutes, in class |
| Lab 2.8-B · The online shop: milestones, ranks and a fair baseline | `l2_8-window-functions/online_milestones_*.py` | a running total that restarts per group, ranking within groups, cummax(), and the leakage idea from the project on a new series. | 20 minutes, early finishers or homework |

## How to run

From any folder (the labs find the course data through `labs_paths.py`, one level above this folder):

```bash
python labs/module-07/l2_7-time-series/units_calendar_starter.py
python3 labs/check_labs.py module-07        # runs every starter and solution: all PASS
```

Each file has `# %%` cell markers, so it also opens as notebook cells in VS Code and Jupyter. Every starter runs
without error as shipped and prints which TODOs are still open. Hand out the `*_starter.py` files only; the
`*_solution.py` files are the instructor's reference.

## Lab 2.7-A · An honest weekly calendar

**Question.** Bend's manager wants unit sales by week with no misleading weeks. Which weekly totals are built from fewer than 7 days, what was the best complete week, and which week-over-week changes should not be reported?

**Done looks like:** a list of four closed dates; missing days of 4, 7, 4, 6 and then 0, 3, 0, 2; two incomplete weeks; a best complete week ending on a Sunday in late summer 2025; four changes, two of them caused by the gap.

Expected output of `l2_7-time-series/units_calendar_solution.py`:

```text
rows: 727 | index type: DatetimeIndex
days in the calendar: 731
closed on: ['2024-11-28', '2024-12-25', '2025-11-27', '2025-12-25']
missing days per store after asfreq:
store
Asheville    4
Bend         7
Boise        4
Flagstaff    6
still unknown after zeroing the closed days:
store
Asheville    0
Bend         3
Boise        0
Flagstaff    2
Bend weeks built from fewer than 7 days:
              sum  count
date                    
2024-08-18  831.0      4
2026-01-04  373.0      3
best complete week: ends 2025-08-31 (Sunday), 1767 units
week-over-week change in units, August 2024:
date
2024-08-04    -96.0
2024-08-11     80.0
2024-08-18   -542.0
2024-08-25    443.0
Freq: W-SUN
The -542 and the +443 are the gap, not the customers: the week ending 2024-08-18 has only 4 days.
```

## Lab 2.7-B · Is the online return rate getting worse?

**Question.** The support team says returns feel worse this year. Compute the share of online orders returned by month, quarter and year, compare each month with the same month a year earlier, and write one honest sentence.

**Done looks like:** 24 monthly rates between about 5.7% and 9.1%, 8 quarterly rates, 2 yearly rates, 12 year-over-year changes, and a sentence that says whether there is a trend.

Expected output of `l2_7-time-series/returns_trend_solution.py`:

```text
online orders: 12854 | returned: 890
            rate_pct  sum  count
order_date                      
2024-01-31      5.87   24    409
2024-02-29      7.07   28    396
2024-03-31      7.19   33    459
2024-04-30      5.92   27    456
2024-05-31      9.06   50    552
2024-06-30      8.71   42    482
2024-07-31      5.76   28    486
2024-08-31      7.38   40    542
2024-09-30      6.21   29    467
2024-10-31      7.25   35    483
2024-11-30      8.12   41    505
2024-12-31      6.47   46    711
2025-01-31      7.61   36    473
2025-02-28      7.11   33    464
2025-03-31      5.74   31    540
2025-04-30      8.76   46    525
2025-05-31      6.26   38    607
2025-06-30      6.05   36    595
2025-07-31      6.28   37    589
2025-08-31      5.87   37    630
2025-09-30      6.34   35    552
2025-10-31      8.10   46    568
2025-11-30      6.90   41    594
2025-12-31      6.63   51    769
highest: 2024-05 at 9.06% (50 of 552 orders)
lowest:  2025-03 at 5.74% (31 of 540 orders)
by quarter (%):
order_date
2024-03-31    6.72
2024-06-30    7.99
2024-09-30    6.49
2024-12-31    7.18
2025-03-31    6.77
2025-06-30    6.95
2025-09-30    6.15
2025-12-31    7.15
Freq: QE-DEC
by year (%):
order_date
2024-12-31    7.11
2025-12-31    6.76
Freq: YE-DEC
2025 minus the same month of 2024, in percentage points:
order_date
2025-01-31    1.74
2025-02-28    0.04
2025-03-31   -1.45
2025-04-30    2.84
2025-05-31   -2.80
2025-06-30   -2.66
2025-07-31    0.52
2025-08-31   -1.51
2025-09-30    0.13
2025-10-31    0.85
2025-11-30   -1.22
2025-12-31    0.16
Freq: ME
months of 2025 with a higher rate than a year earlier: 7 of 12
Conclusion: no trend. Monthly rates bounce between about 5.7% and 9.1% because each month has only
24 to 51 returns. 2025 was worse in 7 months and better in 5, and the yearly rate went DOWN slightly,
from 7.11% to 6.76%. 'Returns feel worse' is not supported by the data.
```

## Lab 2.8-A · Foot traffic: when did Flagstaff pass Bend?

**Question.** Daily visitor counts zigzag with the week. Smooth them, then find when Flagstaff's foot traffic passed Bend's, how many visitor records Flagstaff set, and each store's busiest 7 consecutive days.

**Done looks like:** six `NaN` then two numbers; a 4-by-4 table of 28-day averages; three lines about the crossover; a count of record days with the last three; four lines naming each store's busiest 7 days.

Expected output of `l2_8-window-functions/foot_traffic_solution.py`:

```text
(731, 4) | unknown store-days: 5
Boise, 7-day average, first 8 days:
date
2024-01-01      NaN
2024-01-02      NaN
2024-01-03      NaN
2024-01-04      NaN
2024-01-05      NaN
2024-01-06      NaN
2024-01-07    380.4
2024-01-08    366.3
Freq: D
28-day average visitors:
store       Asheville   Bend  Boise  Flagstaff
date                                          
2024-06-30      319.0  388.0  530.0      350.0
2024-12-31      304.0  358.0  523.0      367.0
2025-06-30      300.0  384.0  577.0      412.0
2025-12-31      292.0  367.0  575.0      420.0
Flagstaff first ahead of Bend on: 2024-12-25
days with Flagstaff ahead: 324
Bend last ahead on: 2025-06-03 | Flagstaff ahead for good since: 2025-06-04
Flagstaff record days: 18
date
2024-08-31    762.0
2025-05-24    816.0
2025-08-30    853.0
Asheville  2024-05-24 to 2024-05-30  2,809 visitors
Bend       2025-08-29 to 2025-09-04  3,431 visitors
Boise      2025-08-27 to 2025-09-02  4,812 visitors
Flagstaff  2025-12-15 to 2025-12-21  3,492 visitors
```

## Lab 2.8-B · The online shop: milestones, ranks and a fair baseline

**Question.** When did completed online revenue pass $1,000,000 in each year, where does each month rank within its year, how often did the shop set a new best day, and how unusual was the best day when judged only by what was known that morning?

**Done looks like:** two million-dollar dates about two months apart in the calendar; a 24-row table with December ranked 1 in both years; a count of record days; and two ratios for the best day, the honest one clearly larger.

Expected output of `l2_8-window-functions/online_milestones_solution.py`:

```text
days: 731 | days with no revenue: 0 | total: 2357984.45
2024: passed $1,000,000 on 2024-12-11 | full year 1,077,800.75
2025: passed $1,000,000 on 2025-10-16 | full year 1,280,183.70
             revenue  rank_in_year
order_date                        
2024-01      73567.0            11
2024-02      70712.0            12
2024-03      80882.0            10
2024-04      86564.0             8
2024-05      99581.0             2
2024-06      97009.0             3
2024-07      90041.0             6
2024-08      92585.0             4
2024-09      90564.0             5
2024-10      82443.0             9
2024-11      88500.0             7
2024-12     125352.0             1
2025-01      86269.0            11
2025-02      86043.0            12
2025-03      96183.0             9
2025-04      92205.0            10
2025-05     114708.0             5
2025-06     127372.0             2
2025-07     116606.0             4
2025-08     125729.0             3
2025-09     101342.0             7
2025-10     105098.0             6
2025-11      98475.0             8
2025-12     130155.0             1
record days: 13
order_date
2025-05-26    8115.83
2025-06-11    8925.85
2025-06-24    8960.15
2025-06-24 (Tuesday): revenue 8,960.15
  mean of the 4 Tuesdays BEFORE it: 4,066.72 -> 2.20 times normal
  without shift(1):                 5,583.56 -> 1.60 times 'normal' (the day is in its own baseline)
days at least 2 times their baseline: honest 25 | leaky 2
```
