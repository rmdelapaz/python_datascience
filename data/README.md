# Pinecrest Outfitters course data

Pinecrest Outfitters is a **fictional** outdoor-gear retailer with an online shop and four stores
(Boise, Bend, Flagstaff, Asheville). These files are the shared dataset for the
[Python Data Science](https://rays-python-datascience.netlify.app/) course. Every person, product,
email address, phone number and figure is invented.

**License:** Fictional data written for this course. © 2026 Ray de la Paz.

## Using it

Unzip `pinecrest-data.zip` next to your notebooks so you have a `data/` folder, then load files with a
relative path:

```python
import pandas as pd
orders = pd.read_csv("data/orders.csv", parse_dates=["order_date"])
```

Rebuild everything (seeded, so you get the same files): `python data/make_data.py`.
CSV, JSON, XLSX and ZIP output is byte-identical from run to run. `pinecrest.db` is byte-identical with
the same SQLite library version (SQLite writes its version number into the file header); its contents
are identical everywhere. `make_data.py` needs numpy and pandas, plus openpyxl for the workbook.

Period covered: 2024-01-01 to 2025-12-31 unless noted.

## Files at a glance

| File | Rows | One row is |
|---|---:|---|
| `products.csv` | 242 | a product in the current catalog |
| `customers.csv` | 4,850 | a customer account |
| `orders.csv` | 20,302 | an order (all online orders, plus in-store orders by signed-in account holders) |
| `order_items.csv` | 45,490 | one product line on an order |
| `orders_messy.csv` | 20,515 | the same orders, damaged on purpose (see below) |
| `daily_sales.csv` | 2,903 | one store on one day (point-of-sale totals) |
| `store_weather.csv` | 2,924 | one store city on one day |
| `survey.csv` | 1,800 | one customer survey response (October to mid-November 2025) |
| `ab_test.csv` | 28,000 | one visitor in the checkout-page experiment (2025-09-08 to 2025-10-05) |
| `web_sessions.json` | 2,400 sessions | nested website sessions for November 2025 |
| `pinecrest.db` | 6 tables | SQLite: products, customers, orders, order_items, employees (55), inventory (1,210) |
| `sales_2025.xlsx` | 2 sheets | "Monthly Sales" (12 months, title rows above the header) and "Targets" (16 rows) |
| `mock_api.py` | | local practice API over products and orders (`python data/mock_api.py`) |
| `make_data.py` | | the generator |

## Schemas

Missing values are empty cells. Dates are `YYYY-MM-DD` text.

### products.csv
| Column | Type | Notes |
|---|---|---|
| `sku` | text | key, like `TNT-1001`; the prefix is the category (TNT, SLP, PCK, FTW, APL, CLM, KIT, SNW, ACC) |
| `name` | text | brand + model + product type, unique |
| `category` | text | Tents, Sleeping, Packs, Footwear, Apparel, Climbing, Camp Kitchen, Snow, Accessories |
| `product_type` | text | for example `2-Person Tent` |
| `brand` | text | 8 invented brands |
| `price` | float | current list price in USD |
| `cost` | float | what Pinecrest pays |
| `weight_kg` | float | 14 missing |
| `color` | text | |
| `rating` | float | 2.8 to 5.0, 1 decimal; 8 missing (products with no reviews yet) |
| `review_count` | int | 0 for those 8 |
| `stock_status` | text | `in_stock` (198), `low_stock` (29), `out_of_stock` (15) |
| `launch_date` | date | 8 products launched 2025-12-20 or later and have never sold |

### customers.csv
| Column | Type | Notes |
|---|---|---|
| `customer_id` | int | key, 10001 to 15000 (150 ids are absent: closed accounts) |
| `first_name`, `last_name` | text | names repeat, as in life |
| `email` | text | unique, all `@example.com` |
| `phone` | text | `(208) 555-01xx` style; 280 missing |
| `city`, `state` | text | 14 states; most customers live near a store |
| `signup_date` | date | 2019-01-01 to 2025-12-15 |
| `birth_year` | int | 442 missing, so pandas reads the column as float |
| `acquisition_channel` | text | organic, paid_search, social, referral, in_store |
| `loyalty_tier` | text | Basic, Silver (completed spend of $600 or more), Gold ($1,500 or more) |
| `marketing_opt_in` | bool | `True` / `False` |

### orders.csv
| Column | Type | Notes |
|---|---|---|
| `order_id` | int | key, 100001 to 120302, in date order |
| `customer_id` | int | 739 orders belong to the 150 closed accounts that are not in `customers.csv` |
| `order_date` | date | |
| `channel` | text | `online` (12,854) or `store` (7,448) |
| `store` | text | Boise, Bend, Flagstaff, Asheville, or `Online` |
| `status` | text | completed, returned, cancelled |
| `payment_method` | text | card, digital_wallet, cash (stores only), gift_card |
| `promo_code` | text | WELCOME10, GEARUP5, TRAIL15, SUMMIT20; empty for 18,154 orders |
| `discount_pct` | int | 0, 5, 10, 15 or 20, set by the promo code |
| `shipping_cost` | float | 0.00, 6.95 or 14.95 (online only) |
| `order_total` | float | `round(items_subtotal * (1 - discount_pct / 100), 2) + shipping_cost` |

### order_items.csv
| Column | Type | Notes |
|---|---|---|
| `order_item_id` | int | key |
| `order_id` | int | every value exists in `orders.csv` |
| `sku` | text | 609 rows use 6 discontinued SKUs that are not in `products.csv` |
| `quantity` | int | 1 to 6, except 12 bulk lines of 25 to 39 |
| `unit_price` | float | price charged at the time; list prices rose on 2025-03-01 for about 60% of products |

### daily_sales.csv
All in-store sales from the registers, including walk-in customers who never appear in `orders.csv`.
| Column | Type | Notes |
|---|---|---|
| `date` | date | |
| `store` | text | Boise, Bend, Flagstaff, Asheville |
| `visitors` | int | door counter |
| `transactions` | int | |
| `units` | int | |
| `revenue` | float | 6 missing |
| `staff_on_duty` | int | scheduled in advance |
| `promo_day` | int | 1 during the six sale weekends |

Gaps (21 store-days have no row): every store closed on 2024-11-28, 2024-12-25, 2025-11-27 and 2025-12-25;
Bend's export failed 2024-08-12 to 2024-08-14; Flagstaff's on 2025-01-21 and 2025-01-22.

### store_weather.csv
`date`, `city` (same four names as `store`), `high_f` (int), `low_f` (int), `precip_in` (float, inches).
Complete: 731 days for each city. Values are made up.

### survey.csv
| Column | Type | Notes |
|---|---|---|
| `response_id` | int | key |
| `customer_id` | int | exists in `customers.csv` |
| `survey_date` | date | 2025-10-01 to 2025-11-15 |
| `age_group` | text | 18-24, 25-34, 35-44, 45-54, 55-64, 65+ |
| `store` | text | where the customer shops most: a store name or `Online` |
| `sat_overall`, `sat_selection`, `sat_price`, `sat_staff`, `sat_website` | int 1 to 5 | Likert items (1 = very dissatisfied, 5 = very satisfied); each has missing answers |
| `recommend` | int 0 to 10 | "How likely are you to recommend us?" |
| `comment` | text | free text; empty for a little over half |

Missing answers are not all random: most online shoppers skipped `sat_staff`, and many store shoppers
skipped `sat_website`.

### ab_test.csv
| Column | Type | Notes |
|---|---|---|
| `visitor_id` | text | unique |
| `date` | date | 28 days |
| `variant` | text | `control` (old checkout page) or `treatment` (new one) |
| `device` | text | mobile, desktop, tablet |
| `returning` | bool | visited before |
| `converted` | int | 1 if the visitor completed an order |
| `order_value` | float | present only when `converted` is 1 |

### web_sessions.json
```
{"site": ..., "period": {"start", "end"}, "note": ...,
 "sessions": [
   {"session_id": "S00001",
    "customer_id": 12345 or null,
    "started_at": "2025-11-01T08:02:15",
    "device": {"type", "os", "browser"},
    "utm": {"source", "medium", "campaign"},   # key absent for direct visits; "campaign" sometimes absent
    "pages": [{"path", "seconds", "at"}, ...],
    "cart": {"items": [{"sku", "qty", "unit_price"}, ...], "value": 0.0},
    "converted": true or false,
    "order_id": 119876 or null}                 # matches orders.csv when converted
 ]}
```

Honest notes about this file:

- `utm.source` values are invented labels: `search`, `newsletter`, `trailgram` (a made-up social app) and
  `partner_blog`.
- `cart.value` is the sum of `qty * unit_price` over the cart items in that session. It is **not** tied to
  the `order_total` of the linked order: the cart was generated separately, so the two numbers do not match.
- Every session that reaches `/checkout` converts (230 of 230). Real funnels lose people at checkout; this
  file does not model that step.
- The `device.os` and `device.browser` values (iOS, Android, Windows, macOS, Linux, iPadOS; Safari, Chrome,
  Edge, Firefox) are ordinary technology names used as labels. Nothing here describes real usage.

### pinecrest.db
`products`, `customers`, `orders`, `order_items` hold the same rows as the CSV files (dates as text,
booleans as 0/1). Two more tables:

- `employees`: `employee_id`, `first_name`, `last_name`, `title`, `department`, `location`
  (HQ, Warehouse or a store), `manager_id` (NULL for the CEO; six levels deep), `hire_date`, `salary`, `email`.
- `inventory`: `sku`, `location` (four stores and `Warehouse`), `quantity`, `reorder_point`, `last_counted`.
  Primary key (`sku`, `location`).

There are no indexes beyond the primary keys. That is deliberate: the query-optimization lesson adds them.

### sales_2025.xlsx
- **Monthly Sales**: a title in A1, a note in A2, a blank row, then the header on row 4:
  `Month, Boise, Bend, Flagstaff, Asheville, Online` and 12 rows. Read it with `skiprows=3`.
- **Targets**: `store`, `quarter` (Q1 to Q4), `target_revenue`. 16 rows, tidy.

## Deliberate flaws in orders_messy.csv

20,515 rows: the 20,302 real orders, 212 duplicates and 1 total row. Counts are exact.

| # | Flaw | Rows |
|---|---|---:|
| 1 | Header names: `Order ID`, ` Customer ID` (leading space), `Order Date`, `Channel`, `Store`, `Status`, `Payment Method`, `Promo Code`, `Discount %`, `Shipping Cost`, `Order Total ` (trailing space) | all |
| 2 | Exact duplicate rows, each placed within 40 rows after its original | 212 |
| 3 | A final `TOTAL` row with the sum of all order totals (it turns `Order ID` and `Discount %` into text/float columns) | 1 |
| 4 | `Order Date` written as `MM/DD/YYYY` | 1,827 |
| 5 | `Order Date` written like `March 5, 2024` | 812 |
| 6 | `Order Date` empty | 25 |
| 7 | `Order Date` impossible (`2024-02-30`, `2025-02-29`, `2024-13-01`, `2025-04-31`, `2024-06-31`, `2025-00-15`) | 6 |
| 8 | `Store` in the wrong case or with a leading/trailing space (`boise`, `BEND`, ` Flagstaff`, `Online `) | 1,218 |
| 9 | `Store` misspelled: `Bosie`, `Flagstaf`, `Ashville`, `Bend OR` | 160 |
| 10 | `Store` says `Web` or `website` instead of `Online` | 602 |
| 11 | `Status` variants: `Completed`, `COMPLETED`, `complete`, `completed `, `Returned`, `RETURNED`, `returned `, `refunded`, `Cancelled`, `CANCELLED`, `canceled`, `cancelled ` | 2,030 |
| 12 | ` Customer ID` empty (60), `N/A` (40) or `unknown` (25) | 125 |
| 13 | `Order Total ` written as currency text like `$1,249.00` | 1,421 |
| 14 | `Order Total ` empty | 40 |
| 15 | `Order Total ` negative (on returned orders) | 15 |
| 16 | `Order Total ` 100 times too large (a lost decimal point) | 8 |
| 17 | `Shipping Cost` says `free` or `FREE` instead of 0.00 | 1,994 |
| 18 | `Shipping Cost` empty | 30 |
| 19 | `Payment Method` empty | 406 |
| 20 | `Payment Method` written `Card`, `CARD` or `credit card` | 971 |
| 21 | `Promo Code` in lowercase (`trail15`) | 322 |
| 22 | `Promo Code` placeholder `none` or `-` where there was no code | 544 |

A row can carry more than one flaw. The duplicates were copied after the other flaws were applied, so
they are exact copies. `orders.csv` is the answer key.

## Things worth knowing before you analyze

- `orders.csv` is not all of Pinecrest's sales. Store revenue in `daily_sales.csv` includes walk-in
  customers; only account holders' store purchases become rows in `orders.csv`.
- Recomputing `order_total` from `order_items.csv` matches to within one cent (80 discounted orders
  differ by exactly $0.01 because of floating-point rounding).
- Twelve online orders are bulk purchases by outfitters (one line of 25 to 39 units, totals from
  about $2,260 to $4,893). They are real orders, not errors.
