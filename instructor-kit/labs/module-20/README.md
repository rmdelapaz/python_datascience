# Session 20 labs: Bokeh and Streamlit

Lessons 7.3 (Interactive Charts with Bokeh) and 7.4 (Dashboards with Streamlit).
Four labs, each a `_starter.py` (the handout) and a `_solution.py` (the instructor's reference), plus
one pytest file. They are new practice on the lesson skills: the lessons work on daily store sales;
these labs work on the product catalog.

| Lab | Practices | Minutes | Expected output (solution) |
|-----|-----------|---------|----------------------------|
| `l7_3-bokeh/margin_brush_*.py` | `ColumnDataSource`, column names as glyph arguments, a formatted `HoverTool`, selection tools, linked brushing through one shared source, `row`, `output_file` + `save` | 22 (in class) | source columns without `cost`; `renderers: 1 + 1 \| same source: True`; `margin_brush.html` about 29 KB; mean rating 4.17 (margin 50% or more, 67 products) vs 4.12 (167 products); Spearman +0.01 |
| `l7_3-bokeh/category_picker_*.py` | `CDSView` + `GroupFilter`, a `Select` with `CustomJS`, `Slider.js_link` to a `Span`, a `Div` rewritten by the callback, `mode="cdn"` against `mode="inline"` | 20 (class or home) | `view shows: category = Tents \| 24 products to start with`; cdn file about 21 KB, inline file about 1,750 KB; counts per category (Apparel 35 ... Packs 22) |
| `l7_4-streamlit/gear_shortlist_*.py` | the rerun model, a variable that forgets, `st.session_state`, callbacks with `on_click`, predicting a test's output | 10 (in class) | first metric 0, 1, 1, 1, 2, 0 across the check's steps; total $259.90 for two tents; the ordinary counter reads 1 on every line |
| `l7_4-streamlit/catalog_browser_*.py` | `@st.cache_data`, sidebar widgets with keys, a reset callback, `st.stop()` on an empty result, `st.columns` + `st.metric`, table, download | 12 in class, rest at home | start: 24 products, median $298.45, mean rating 4.25; Tents + Sleeping under $100: 12 (11 in stock); empty selection: warning, 0 metrics, 0 errors |
| `l7_4-streamlit/test_catalog_browser.py` | the lesson's "five-line safety net" as three pytest tests against the solution app | n/a | `3 passed` |

## How to run

Bokeh labs are ordinary scripts (or notebook cells: `# %%` markers):

```bash
python labs/module-20/l7_3-bokeh/margin_brush_starter.py
```

They write HTML files to `OUTPUT` (an `output/` folder next to the lab file) with `output_file` and
`save`, and **never call `show()`**: open `output/margin_brush.html` from your file manager. In a room
with no internet pass `mode="inline"` to `output_file` so the file works offline.

Streamlit labs are apps, and each one is also its own test. The same file runs two ways:

```bash
streamlit run labs/module-20/l7_4-streamlit/gear_shortlist_starter.py    # opens the app in a browser
python        labs/module-20/l7_4-streamlit/gear_shortlist_starter.py    # checks it with AppTest: no server, no browser
```

The last lines of each file choose: under `streamlit run` they call `main()`; under plain `python`
they call `self_check()`, which drives the app with `streamlit.testing.v1.AppTest` and prints what the
page shows. A starter's check never fails on an unfinished TODO: it reports how far you have got.
Stop a running app with Ctrl+C before starting the next one (or add `--server.port 8502`).

The pytest file:

```bash
python -m pytest labs/module-20/l7_4-streamlit/test_catalog_browser.py
```

## Check

```bash
python3 labs/check_labs.py module-20      # 9 passed, 0 failed
```

The checker runs every file with plain `python` (and pytest for the test file), so it starts no
Streamlit server and opens no browser.
