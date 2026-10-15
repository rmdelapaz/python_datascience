# Session 19 labs: Seaborn and Plotly

Lessons 7.1 (Statistical Graphics with Seaborn) and 7.2 (Interactive Charts with Plotly).
Four labs, each a `_starter.py` (the handout) and a `_solution.py` (the instructor's reference).
They are new practice on the lesson skills: different questions from the lesson projects and exercises,
same Pinecrest data.

| Lab | Practices | Minutes | Expected output (solution) |
|-----|-----------|---------|----------------------------|
| `l7_1-seaborn/tier_order_sizes_*.py` | a merge check, `ecdfplot` with `hue` and `log_scale`, `pointplot` with `errorbar=("ci", 95)` and `seed`, two axes-level charts in one figure, finishing with Matplotlib | 25 (in class) | 18,762 completed orders, 18,079 matched, 683 dropped; median order total Basic 110.66 / Silver 146.98 / Gold 162.28; orders per customer 2.05 / 5.12 / 10.81; Gold vs Basic x1.47 and x5.26; `tier_orders.png` |
| `l7_1-seaborn/website_by_age_*.py` | `order=`, `errorbar=("ci", 95)` against `"sd"`, a hand check of the bars, figure-level `catplot` with `col=`, a missing-data caveat | 20 (class or home) | 65+ mean 3.04 vs 3.68 for everyone else (gap 0.64); `FacetGrid`, axes shape `(1, 2)`; no website rating from 3% of online and 46% of store shoppers; two PNG files |
| `l7_2-plotly/product_map_*.py` | one Plotly Express scatter, `hover_name` / `hover_data` formats, layout and axis finishing, an annotation, `write_html`, checking what is inside the file | 25 (in class) | `Figure with 9 traces of type scatter`; Spearman −0.01; lowest rated: Juniper Vane Trailhead Down Jacket ($372.95, 2.8, 4 reviews); `product_map.html` about 31 KB; name in file True, cost in file False |
| `l7_2-plotly/promo_share_trend_*.py` | aggregate before plotting, `custom_data` and `hovertemplate`, `hovermode="x unified"`, `add_vrect`, range slider, `write_html`, guarded `write_image` | 20 (class or home) | weekly table `(210, 4)`; 6 sale weekends shaded; code used on 51.0% of orders on sale-weekend days vs 8.0% otherwise; `promo_share.html` about 19 KB |

## How to run

From the kit folder, or from anywhere:

```bash
python labs/module-19/l7_1-seaborn/tier_order_sizes_starter.py
```

or open a file in VS Code or JupyterLab and run it cell by cell (`# %%` markers).
Every starter runs as shipped and ends with a line that says which TODOs are still open.

## Where the charts go

Everything is written to `OUTPUT`: an `output/` folder next to the lab file (a temporary folder
when `LABS_OFFLINE=1`). Seaborn labs save PNG files. Plotly labs write HTML files and **never call
`fig.show()`**: open `output/product_map.html` from your file manager. In a room with no internet,
write the HTML with `include_plotlyjs=True` instead of `"cdn"` so the file works offline.

## Static images are optional

`promo_share_trend_solution.py` also exports a PNG with `fig.write_image`, but only when it can
find Chrome (the environment variable `BROWSER_PATH`, or a Chrome on the PATH). Otherwise it prints
`static image skipped: ...` and carries on. To enable it, run `plotly_get_chrome` once, or set
`BROWSER_PATH` to a Chrome binary.

## Check

```bash
python3 labs/check_labs.py module-19      # 8 passed, 0 failed
```
