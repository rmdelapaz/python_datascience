# Python Data Science: Instructor Kit ("Course-in-a-Box")

A ready-to-teach package that lets another instructor deliver the course
**Python Data Science** without building it from scratch. The live course site
(<https://rays-python-datascience.netlify.app/>) is the learner's textbook: 41 lessons, each with
real output under every code block, a guided project, exercises, a quiz and a journal prompt. This
kit is everything the instructor needs around it. The course follows **Introduction to Programming
with Python** and **Intermediate Python** (both at <https://rays-home.netlify.app/>).

**Format:** 21 sessions × 3 hours (63 class hours), two lessons per session (Session 21, the
capstone, has one). Run it weekly (21 weeks), twice a week (about 11 weeks), or as intensive days
(two sessions a day). In the file layout a session is called a "module": `source/module-07/` is
Session 7. In prose, "Module 2" always means a course module (pandas).

Learners start each lesson project in the room and finish it at home, so "leave with" below means
"have started in class and finish before the next session".

| Session | Lessons | Learners leave with |
|---------|---------|---------------------|
| S1 · Toolkit and First Arrays | 0.1–1.1 (+ welcome, environment check, 6-item diagnostic) | A working `.venv` with the course data (`check_environment.py` says READY); `first_look.py`, a sales summary and chart of 20,302 orders; a list-versus-array benchmark report |
| S2 · Vectorized Operations and Broadcasting | 1.2–1.3 | A loop-free store scorecard (conversion, basket, sale-weekend lift); a weekday index that removes store size |
| S3 · Randomness and Linear Algebra | 1.4–1.5 | A seeded simulation of 10,000 possible months of Boise revenue, checked against the real months; a least-squares revenue model for Asheville |
| S4 · DataFrames and Loading Data | 2.1–2.2 | A catalog health check of 242 products; a typed Parquet snapshot of seven tables loaded from CSV, Excel and JSON |
| S5 · Cleaning and Grouping | 2.3–2.4 | A rerunnable `clean_orders()` pipeline for the 20,515-row messy export, scored against the answer key; a store scorecard and customer summary |
| S6 · Merging and Reshaping | 2.5–2.6 | A revenue-by-category report from three merged tables with every unmatched row accounted for; a tidy category-by-month seasonality report |
| S7 · Time Series and Windows | 2.7–2.8 | A store trend report on a clean daily calendar (the 21 missing store-days decided); a leak-free sale-day detector |
| S8 · Features and First Charts | 2.9–3.1 | A leak-free customer feature table (`customer_features.csv`); a four-chart answer to "does rain keep shoppers away?" |
| S9 · Composing and Customizing Figures | 3.2–3.3 | A nine-panel seasonality figure; a presentation-ready footwear returns chart. |
| S10 · Saving Figures; Center and Spread | 3.4–4.1 | A chart pack saved for web and print plus a one-function save preset; a "typical order" memo |
| S11 · Shape, Outliers and Distributions | 4.2–4.3 | A store profile sheet with flagged days investigated; a checked Poisson returns forecast |
| S12 · Correlation and Hypothesis Tests | 4.4–4.5 | A like-with-like "rain check" correlation analysis; a tested, caveated answer on rain and traffic. |
| S13 · A/B Testing and the EDA Workflow | 4.6–4.7 + **Checkpoint 1** (30 min) | A decision memo for the checkout experiment; a returns EDA ending in a findings note; a scored checkpoint |
| S14 · SQL from Python: Queries and Joins | 5.1–5.2 | A parameterized store-scorecard function that reads from and writes back to SQLite; a four-table returns investigation |
| S15 · SQL Windows and Query Speed | 5.3–5.4 | A monthly store performance table built with window functions; a before-and-after index tuning report. |
| S16 · Documents and HTTP | 5.5–6.1 | A web funnel report from nested sessions in MongoDB (mongomock); a polite snapshot tool that checks robots.txt and logs every request |
| S17 · Scraping Static and Dynamic Pages | 6.2–6.3 | A category price report scraped from the practice shop; a Selenium deals collector checked against the page's own data. |
| S18 · APIs: Keys, Tokens and Polite Clients | 6.4–6.5 + **Checkpoint 2** (15 min) | A December returns brief from the protected API with keys kept out of code; a resumable, rate-limited order pull. |
| S19 · Seaborn and Plotly | 7.1–7.2 | A four-panel store performance brief (PNG); `sales_explorer.html`, a one-file interactive report |
| S20 · Bokeh and Streamlit | 7.3–7.4 + capstone kickoff | `store_explorer.html` with linked charts; `dashboard.py`, a Streamlit dashboard; a chosen capstone question and a one-paragraph plan |
| S21 · Capstone Studio and Showcase | 8.1 | The Pinecrest Report in progress: a notebook that reruns, one or two figures, a one-page report; a showcase talk. Submit within a week |

**Why this shape (and the timing trade-off):** the lessons were written and timed honestly for a
solo learner at 75 to 110 minutes each (the capstone at 420), so two of them come to 155 to 210
solo minutes against about 150 room minutes once the warm-up, break and wrap-up are out. They do
not fit whole, and the kit does not pretend they do. The room protects what is hardest alone: the
**mental model**, a **live-coding demo** learners type along with, the **guided lab** (new practice
on the same data, not the lesson's project), and **starting** each lesson project together. Home
gets the rest: finishing the two projects, the lesson's own exercises, quiz and journal, about two
to three hours between sessions (Session 13 is closer to three and a half). Every facilitator guide
says, for its session, what is done in the room, what goes home, what to protect and what to cut
first if you run long.

Every session runs 0:00 to 3:00: warm-up (five retrieval questions, homework check, 10 min;
Session 1 opens with a 30-minute welcome, environment check and diagnostic instead), Lesson A
(frame, demo, guided lab, project start), a 10-minute break, Lesson B, and a 10-minute wrap-up
(exit ticket, homework, the next session's bring list).

### Primary documents: the combined books (start here)

| File | Audience | Contents |
|------|----------|----------|
| `participant-workbook.{html,pdf}` | Learner | The complete workbook: all 21 sessions as chapters. At v1.0 the PDF is 337 pages. |
| `facilitator-guide.{html,pdf}` | Instructor | The complete teaching manual: all 21 sessions. At v1.0 the PDF is 520 pages. |
| `answer-key.{html,pdf}` | Instructor | Every self-check answered with reasons, lab solution notes, the lesson pages' quiz answers, warm-up and exit-ticket answers (confidential). At v1.0 the PDF is 358 pages. |

**Self-check items:** 12 per session, 21 × 12 = **252**, every one answered in the answer key with
why each wrong option is wrong. The workbook quiz, the answer key and the guide's compact answers
were generated from one item list per session and are checked to match word for word.

The editable per-session docs live in `source/module-NN/`. **If you edit a session's doc, run
`python3 build-combined.py` to regenerate the three books, then re-render their PDFs.**

### Kit-wide documents

| File | Audience | Purpose |
|------|----------|---------|
| `setup-guide.html` | Learner | Before-you-begin sheet: an "am I ready?" list of Intro and Intermediate skills; Python 3.12+, a `.venv`, `python -m pip install -r requirements.txt`, JupyterLab or VS Code, both data zips, Chrome; Windows/macOS/Linux commands; common install problems; and `check_environment.py`. Send it a week before Session 1 with `labs/module-01/l0_1-orientation/check_environment.py` attached |
| `final-assessment.html` | Instructor | The capstone (The Pinecrest Report, lesson 8.1): the four questions, the rubric and the instructor answer notes for each question (confidential) |
| `sell-sheet.html` | Prospective instructors | Marketing one-pager: what's inside, who it's for, the dataset and practice site, license tiers |
| `README.md` · `LICENSE.md` | — | This overview and the tiered license template |

Slide decks: one per session in `slides/` (`module-NN-<slug>.html`). At v1.0 the 21 decks hold 708 slides.
Labs: 90 starter/solution pairs across `labs/module-01/` … `labs/module-21/`.

The 21-session **syllabus** lives in the course root, one level up, so it stays public:
`syllabus.html` (screen, light/dark), `syllabus-print.html` (print-first), and
`Python-Data-Science-Syllabus-21-sessions.pdf`. They are generated (see "Editing and building").

**Still to do:** the `LICENSE.md` is a plain-language **template**; have it reviewed by a
lawyer before commercial distribution. Pricing in the sell sheet and the license is a suggested
anchor (the bracketed prices are placeholders set at point of sale).

---

## Folder layout

```
instructor-kit/
├─ participant-workbook.{html,pdf}   ← canonical hand-out books (all 21 sessions)
├─ facilitator-guide.{html,pdf}
├─ answer-key.{html,pdf}
├─ setup-guide / final-assessment / sell-sheet  (.html + .pdf)
├─ slides/            one self-contained deck per session: module-NN-<slug>.html (NN = 01 … 21)
├─ labs/              labs_paths.py, check_labs.py, README.md, and module-01/ … module-21/:
│                     per lesson a folder lM_N-<slug>/ with *_starter.py + *_solution.py pairs,
│                     debug_*.py "find the bug" handouts, and _fixtures/ for offline runs
├─ source/            module-01/ … module-21/ editable per-session docs (build the books)
├─ kit.css            shared print-first stylesheet
├─ build-combined.py  regenerate the 3 books from source/
└─ README.md · LICENSE.md
```

Every document is print-ready (a **Print / Save as PDF** button and a tuned print layout,
US Letter). Slide decks are single files and need no server (arrow keys / space to advance).

The whole `instructor-kit/` folder is kept **off the live site**: the course root's
`_redirects` returns 404 for `/instructor-kit/*`. It lives in the repository only.

### How to teach from it
1. Send learners the **setup guide** and `check_environment.py` a week before Session 1; ask each
   learner to reply with its last line (`READY for Python Data Science`).
2. Before each session, read that session's **facilitator guide**: "Before the session" (files,
   servers to start, known environment traps), the 0:00–3:00 agenda, each lesson's live-demo script
   (the exact code to type, all of it run), the three mistakes to expect, and "If you run long".
3. Present from the session's deck in **`slides/`**; live-code in JupyterLab or VS Code.
4. Hand out the `labs/` folder **without the `*_solution.py` files**. Learners keep it inside their
   `pinecrest-analysis` folder next to `data/`, so every lab finds the data by itself
   (`labs_paths.py`; or set `PINECREST_DATA`).
5. Learners work in the **participant workbook** and keep a **learning journal**.
6. Check self-checks, warm-ups and exit tickets with the **answer key**; score the checkpoints and
   the capstone with their rubrics.

## The data and the practice site

Everything runs on **Pinecrest Outfitters**, a fictional outdoor-gear retailer (an online shop and
four stores: Boise, Bend, Flagstaff, Asheville), 2024–2025. Every person, product and figure is
invented, so learners can dig into "customer records" with no privacy concerns.

- `data/pinecrest-data.zip` (on the course site): `orders.csv` (20,302), `order_items.csv`,
  `customers.csv`, `products.csv`, `orders_messy.csv` (the same orders with 22 documented flaws, plus
  212 duplicates and a total row), `daily_sales.csv`, `store_weather.csv`, `survey.csv`,
  `ab_test.csv`, `web_sessions.json`, `pinecrest.db` (SQLite, six tables, no indexes on purpose),
  `sales_2025.xlsx`, the generator `make_data.py` (seeded: it rebuilds identical files) and
  `mock_api.py`. `data/README.md` documents every file and column, the planted flaws and the
  honest caveats.
- **The practice shop** (`practice/shop/` on the course site) is a small static store to scrape in
  Sessions 16 and 17, with a `robots.txt`, paginated categories, product pages and a Deals page that
  only JavaScript fills.
- **The practice API**, `python data/mock_api.py`, runs on each learner's laptop at
  `http://127.0.0.1:8000` over products and orders. Flags: `--token-ttl 5` (lesson 6.4: tokens
  expire in 5 seconds), `--rate 10 --per 5` (lesson 6.5: rate limit), `--port`, `--quiet`. The demo
  credentials are environment variables, never typed into code: `PINECREST_API_KEY`,
  `PINECREST_USER`, `PINECREST_PASSWORD` (values in lesson 6.4 and the Session 18 guide).

## Teaching offline

The venue's internet is only needed by learners who have not installed yet (installation is
homework before Session 1). For the web sessions:

- **Practice shop without the internet:** learners unzip `data/pinecrest-practice-site.zip` in their
  project folder (`python -m zipfile -e pinecrest-practice-site.zip .`), run
  `python -m http.server 8001` there, and set `BASE_URL = "http://127.0.0.1:8001/practice/shop/"`.
  The lesson code works unchanged; a few printed headers differ (lesson 6.1 explains which).
- **The practice API** is local by design.
- **Selenium (Session 17)** needs Chrome installed; Selenium Manager downloads the driver once while
  online, so check every machine in Session 16. Plotly image export (Session 19) uses Chrome too
  (`plotly_get_chrome` if Kaleido cannot find it).
- **Labs:** with `LABS_OFFLINE=1` set, every web and API lab reads saved responses from
  `labs/module-NN/_fixtures/` instead of the network, Selenium labs fall back to a fixture with a
  clear message, and Plotly/Bokeh labs write files instead of opening a browser
  (`LABS_OFFLINE=1 python <lab>.py`; PowerShell: `$env:LABS_OFFLINE = "1"; python <lab>.py`).
  Without the variable the same solutions run online against `BASE_URL` and the mock API.

## Checkpoints and the capstone

- **Checkpoint 1 (Session 13, 30 minutes):** an individual, open-notebook analysis task on Modules 1
  to 4; task sheet in the workbook, five-row rubric and model answer in the answer key.
- **Checkpoint 2 (Session 18, 15 minutes):** a short data-access task on Modules 5 and 6
  (`labs/module-18/checkpoint-2/`).
- **Capstone, The Pinecrest Report (lesson 8.1):** in the **Session 20** wrap-up each learner chooses
  one of four questions (Asheville's decline; acquisition channel and spend; whether WELCOME10 brings
  customers back; the March 2025 price increase) and leaves with a one-paragraph plan. **Session 21**
  is a studio with milestone check-ins and a coaching guide per question (what a good analysis finds,
  the traps, what an honest null result looks like), then a showcase (lightning talks or a gallery
  walk). Learners submit a notebook that reruns from top to bottom, one or two figures and a
  one-page `report.md` within a week. `final-assessment.html` holds the rubric and the instructor
  answer notes.

## Requirements
- **Python 3.12 or newer** on Windows, macOS or Linux, with a virtual environment, and the course
  `requirements.txt` (NumPy 2.5, pandas 3.0, Matplotlib 3.11, seaborn 0.13, SciPy 1.18,
  statsmodels 0.15, JupyterLab 4.6, SQLAlchemy 2.1, PyMongo 4.18 + mongomock, Requests 2.34,
  Beautiful Soup 4.15, Selenium 4.51, Plotly 7.1 + Kaleido, Bokeh 3.10, Streamlit 1.65).
- **JupyterLab or VS Code**, and **Google Chrome**.
- About 2 GB of disk. No paid tools, accounts or real API keys.

## Editing and building

```bash
cd instructor-kit
python3 build-combined.py                 # regenerate the 3 books from source/ (skips missing sessions)
python3 labs/check_labs.py                # run every starter, solution and test offline (LABS_OFFLINE=1)
python3 labs/check_labs.py module-07      # one session
```

The author's tools in `~/projects/_kit_tools/python_ds/` (not shipped with a licensed kit):

```bash
python3 check_kit_ds.py --all             # per-session consistency: one sheet/foot, agenda sums to 180,
                                          # quiz identical across workbook/key/guide, lab paths exist,
                                          # decks fit 1280x720, nothing wider than 390 px
python3 gen_syllabus_ds.py                # rebuild ../syllabus.html + ../syllabus-print.html; reads each
                                          # session's agenda from source/module-NN/facilitator-guide.html
python3 render_pdfs_ds.py Python-Data-Science-Syllabus-21-sessions.pdf
                                          # render every kit PDF + the syllabus PDF, print page counts,
                                          # and phone-check every page at 390 px
python3 verify_all.py                     # the course itself: page checks + every lesson's code run and
                                          # compared with its printed output (web lessons on local servers)
```

Or open any document and use **Print / Save as PDF** (Letter, 0.5 in margins, background
graphics on).

---

## License

See `LICENSE.md`. Short version: licensed to a **single instructor or organization** to
teach the course; **not** for resale; the facilitator guide, answer key and final assessment are
**not** for learner distribution. The Pinecrest dataset and the practice shop are part of the
licensed materials. Tiers (Solo / Organization / White-label, plus an optional updates add-on) are
set at point of sale.

© 2026 Ray de la Paz. Python Data Science. All rights reserved.
