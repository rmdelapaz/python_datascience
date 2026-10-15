# Session 15 labs · SQL Windows and Query Speed (Lessons 5.3 + 5.4)

New practice against `pinecrest.db`. The window-function labs ask questions the lesson does not
(pay within each location, the order on which customers reach Silver, online orders week by week);
the optimization labs tune queries the lesson does not (a customer lookup screen, an N+1 loop).

**The shipped database is never written to.** The 5.3 labs open it read-only. The 5.4 labs create
indexes, so they copy it to `OUTPUT` first and open the copy with `cached_statements=0` (so that a
plan asked for again after `DROP INDEX` is planned afresh, as Lesson 5.4 explains). **Timings are
printed with "your numbers will differ" and never checked**: only plans and answers are.

| Lab | Practices | Where | Minutes | Expected output (solution) |
|-----|-----------|-------|---------|----------------------------|
| `l5_3-sql-window-functions/staff_rankings_*.py` | `AVG`/`SUM ... OVER (PARTITION BY)`, `RANK` against `DENSE_RANK`, top N per group, pandas check | room | 12 | Boise average 43,950; a tie at 39,000 (RANK 5, 5, 7 against DENSE_RANK 5, 5, 6); 12 rows of top two earners at 6 locations; pandas agrees |
| `l5_3-sql-window-functions/silver_milestone_*.py` | `ROW_NUMBER` with a tiebreaker, running `SUM` with an explicit `ROWS` frame, a named `WINDOW`, first row meeting a condition, `LAG` + `julianday` | room | 18 | 2,028 customers reach $600 (equal to Silver + Gold in `customers`), on order 3.5 on average (1 to 9); gap before order 2 is 118.2 days, before the 6th or later 57.2 |
| `l5_3-sql-window-functions/weekly_trend_*.py` | `LAG`, two frames (to `CURRENT ROW`, to `1 PRECEDING`), partial frames against pandas `min_periods`, `NTILE` | home | 20 | 51 weeks; spikes above 25% in weeks 20, 34, 47 (the three sale weekends); differences against pandas 0; quartiles of 13, 13, 13, 12 weeks |
| `l5_4-query-optimization/customer_lookup_plans_*.py` | `EXPLAIN QUERY PLAN`, a composite index, the leftmost-prefix rule, removing a sort with a third column, `DROP INDEX` and re-planning | room | 15 | all SCAN before; `SEARCH ... (state=? AND city=?)` after; city-only still a SCAN (of the index); the sort step disappears with (state, city, signup_date); SCAN again after the drop; 488 customers in Boise, ID |
| `l5_4-query-optimization/n_plus_one_*.py` | the N+1 loop against one `IN (...) GROUP BY` query, an index on a foreign key, proving answers unchanged | room (start) / home | 20 | SCAN, then `SEARCH ... USING INDEX idx_orders_customer_id`; "same answers: True" three times; 300 Gold customers with 3 to 31 completed orders |

Hand out the `*_starter.py` files only. Starters run as shipped and say which TODOs are open.

Run one (from the kit folder, or from any folder):

    python labs/module-15/l5_3-sql-window-functions/staff_rankings_starter.py

Check all: `python3 labs/check_labs.py module-15` (expect `10 passed, 0 failed`).

Helpers and files these labs create: `show()` (5.3 labs), `plan()` and `timed()` (copied from
Lesson 5.4), `best_ms()` (n_plus_one); query strings `TOP2_SQL`, `RUNNING`, `MILESTONE`, `WEEKLY`;
working copies `pinecrest_plans.db` and `pinecrest_nplus1.db` in `OUTPUT` (an `output/` folder next
to the lab, or a temporary folder when `LABS_OFFLINE=1`). Delete the `output/` folders when done.
