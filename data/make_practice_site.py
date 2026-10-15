"""Build the practice catalog in practice/shop/ from data/products.csv.

    python data/make_practice_site.py            # writes ../practice/ next to data/
    python data/make_practice_site.py --out DIR  # writes DIR/shop/ and DIR/robots.txt

It also writes data/pinecrest-practice-site.zip (next to this script, or --zip PATH): the same
practice/ folder for learners who want to work offline. Unzip it in the project folder, run
`python -m http.server 8001` there, and use http://127.0.0.1:8001/practice/shop/ as the base URL.
The zip has fixed timestamps, so it is byte-identical from run to run.

Standard library only, no randomness: the same products.csv always gives the same pages.
The site is a scraping target for the web lessons. Everything on it is fictional.
(c) 2026 Ray de la Paz.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import math
import shutil
import zipfile
from pathlib import Path

PER_PAGE = 20
BANNER = "Practice site for the Python Data Science course — fictional products"
STOCK_LABEL = {"in_stock": "In stock", "low_stock": "Low stock", "out_of_stock": "Out of stock"}
STORES = [("Boise", "ID", "9 am to 8 pm", "(208) 555-0142"), ("Bend", "OR", "9 am to 7 pm", "(541) 555-0118"),
          ("Flagstaff", "AZ", "10 am to 7 pm", "(928) 555-0167"), ("Asheville", "NC", "10 am to 8 pm", "(828) 555-0193")]
BLURB = {
    "Tents": "Pitches fast, sheds wind and rain, and packs down small for the trail.",
    "Sleeping": "Built for warm, quiet nights after long days outside.",
    "Packs": "Carries the load comfortably, with pockets where you reach for them.",
    "Footwear": "Grippy, supportive and ready for rocky, rooty miles.",
    "Apparel": "Layers that breathe on the climb and hold warmth at the top.",
    "Climbing": "Dependable hardware and soft goods for the gym and the crag.",
    "Camp Kitchen": "Simple, sturdy gear for good meals far from a kitchen.",
    "Snow": "Made for cold mornings, deep snow and short winter days.",
    "Accessories": "The small things that make a trip safer and easier.",
}

ROBOTS = """# Practice rules for the Python Data Science course (fictional shop).
# A real robots.txt lives at the root of a site; this one is a teaching copy
# that the lessons read with urllib.robotparser.
User-agent: *
Disallow: /practice/shop/staff/
Crawl-delay: 1

User-agent: BadBot
Disallow: /
"""

CSS = """/* Practice shop for the Python Data Science course. Fictional products. */
:root { --ink: #1f2937; --muted: #5b6472; --line: #d9dee7; --green: #1f6f4a; --bg: #f6f7f4; --card: #fff; }
* { box-sizing: border-box; }
body { margin: 0; font-family: system-ui, -apple-system, 'Segoe UI', Arial, sans-serif; color: var(--ink); background: var(--bg); line-height: 1.5; }
.practice-banner { background: #3b2f63; color: #fff; text-align: center; padding: 0.45rem 1rem; font-size: 0.9rem; margin: 0; }
.site-header { background: var(--green); color: #fff; padding: 0.8rem 1rem; }
.site-header .inner, main, .site-footer .inner { max-width: 1040px; margin: 0 auto; }
.site-header a { color: #fff; }
.logo { font-size: 1.3rem; font-weight: 700; text-decoration: none; }
.site-nav { display: flex; flex-wrap: wrap; gap: 0.3rem 1rem; margin-top: 0.3rem; font-size: 0.95rem; }
main { padding: 1rem; }
h1 { font-size: 1.6rem; margin: 0.4rem 0 0.8rem; }
a { color: #14532d; }
.breadcrumbs ol { list-style: none; display: flex; flex-wrap: wrap; gap: 0.3rem; padding: 0; margin: 0 0 0.6rem; font-size: 0.9rem; }
.breadcrumbs li + li::before { content: "›"; margin-right: 0.3rem; color: var(--muted); }
.product-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 0.9rem; padding: 0; margin: 1rem 0; list-style: none; }
.product-card { background: var(--card); border: 1px solid var(--line); border-radius: 8px; padding: 0.8rem; }
.product-card h2 { font-size: 1rem; margin: 0 0 0.3rem; }
.product-card p { margin: 0.15rem 0; }
.product-category, .review-count, .result-count, .sku { color: var(--muted); font-size: 0.9rem; }
.price { font-weight: 700; font-size: 1.1rem; }
.price .was { font-weight: 400; color: var(--muted); margin-right: 0.4rem; }
.stock.in-stock { color: #166534; } .stock.low-stock { color: #92400e; } .stock.out-of-stock { color: #991b1b; }
.pagination { display: flex; justify-content: space-between; align-items: center; gap: 0.5rem; margin: 1.2rem 0; flex-wrap: wrap; }
.pagination a, .pagination span { padding: 0.4rem 0.8rem; border: 1px solid var(--line); border-radius: 6px; background: var(--card); text-decoration: none; }
.pagination .disabled { color: #9aa3af; }
.pagination .current { border: 0; background: none; color: var(--muted); }
.table-scroll { overflow-x: auto; background: var(--card); border: 1px solid var(--line); border-radius: 8px; }
table { border-collapse: collapse; width: 100%; font-size: 0.93rem; }
th, td { text-align: left; padding: 0.4rem 0.7rem; border-bottom: 1px solid var(--line); }
caption { text-align: left; font-weight: 700; padding: 0.6rem 0.7rem; }
.specs { max-width: 480px; }
.specs th { width: 40%; color: var(--muted); font-weight: 600; }
form.filters { display: flex; flex-wrap: wrap; gap: 0.7rem; align-items: end; background: var(--card); border: 1px solid var(--line); border-radius: 8px; padding: 0.8rem; }
form.filters label { display: flex; flex-direction: column; font-size: 0.85rem; color: var(--muted); gap: 0.2rem; }
form.filters label.inline { flex-direction: row; align-items: center; }
input, select, button { font: inherit; padding: 0.4rem 0.6rem; border: 1px solid #aab2bf; border-radius: 6px; background: #fff; color: var(--ink); }
button { background: var(--green); color: #fff; border-color: var(--green); cursor: pointer; }
.notice { background: #fff8e1; border: 1px solid #e6cf7a; border-radius: 8px; padding: 0.7rem 0.9rem; }
.site-footer { border-top: 1px solid var(--line); margin-top: 2rem; padding: 1rem; color: var(--muted); font-size: 0.9rem; }
"""

JS = """/* Practice shop: fills the deals page and the search page from JSON. Fictional products. */
(function () {
    'use strict';
    function money(n) { return '$' + Number(n).toFixed(2); }
    function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }

    /* deals.html: the list arrives 1.5 s after the page loads, the way many real pages work */
    var dealList = document.getElementById('deal-list');
    if (dealList) {
        var shown = 0, deals = [];
        var status = document.getElementById('deal-status');
        var more = document.getElementById('load-more');
        function addBatch() {
            deals.slice(shown, shown + 8).forEach(function (d) {
                var li = el('li', 'product-card deal');
                li.setAttribute('data-sku', d.sku);
                var h = el('h2', 'product-name'); var a = el('a', null, d.name); a.href = 'products/' + d.sku + '.html'; h.appendChild(a);
                var p = el('p', 'price');
                var was = el('s', 'was', money(d.price)); var now = el('span', 'deal-price', money(d.deal_price));
                p.appendChild(was); p.appendChild(now);
                li.appendChild(h); li.appendChild(el('p', 'product-category', d.category)); li.appendChild(p);
                li.appendChild(el('p', 'discount', 'Save ' + d.discount_pct + '%'));
                dealList.appendChild(li);
            });
            shown = Math.min(shown + 8, deals.length);
            status.textContent = 'Showing ' + shown + ' of ' + deals.length + ' deals';
            if (shown >= deals.length) { more.hidden = true; }
        }
        window.setTimeout(function () {
            fetch('deals.json').then(function (r) { return r.json(); }).then(function (data) {
                deals = data.deals;
                document.getElementById('loading').remove();
                more.hidden = false;
                addBatch();
                dealList.setAttribute('data-loaded', 'true');
            }).catch(function () { status.textContent = 'Could not load deals. Open this page through a web server, not as a file.'; });
        }, 1500);
        more.addEventListener('click', function () { more.disabled = true; window.setTimeout(function () { addBatch(); more.disabled = false; }, 700); });
    }

    /* search.html: the form submits with GET; results are filtered in the browser from products.json */
    var results = document.getElementById('search-results');
    if (results) {
        var params = new URLSearchParams(window.location.search);
        var form = document.getElementById('search-form');
        ['q', 'category', 'max_price'].forEach(function (name) { if (params.get(name)) form.elements[name].value = params.get(name); });
        form.elements['in_stock'].checked = params.get('in_stock') === '1';
        fetch('products.json').then(function (r) { return r.json(); }).then(function (data) {
            var q = (params.get('q') || '').toLowerCase(), cat = params.get('category') || '', max = parseFloat(params.get('max_price'));
            var hits = data.products.filter(function (p) {
                return (!q || p.name.toLowerCase().indexOf(q) !== -1) && (!cat || p.category === cat) &&
                       (isNaN(max) || p.price <= max) && (params.get('in_stock') !== '1' || p.stock_status !== 'out_of_stock');
            });
            document.getElementById('search-count').textContent = hits.length + ' product' + (hits.length === 1 ? '' : 's') + ' found';
            hits.slice(0, 60).forEach(function (p) {
                var li = el('li', 'product-card'); li.setAttribute('data-sku', p.sku);
                var h = el('h2', 'product-name'); var a = el('a', null, p.name); a.href = 'products/' + p.sku + '.html'; h.appendChild(a);
                li.appendChild(h); li.appendChild(el('p', 'product-category', p.category)); li.appendChild(el('p', 'price', money(p.price)));
                results.appendChild(li);
            });
            results.setAttribute('data-loaded', 'true');
        }).catch(function () { document.getElementById('search-count').textContent = 'Could not load products.json.'; });
    }
})();
"""


def e(text) -> str:
    return html.escape(str(text), quote=True)


def slug(text: str) -> str:
    return text.lower().replace(" ", "-")


def money(value: float) -> str:
    return f"${value:,.2f}"


def page(title: str, body: str, depth: int = 0, script: bool = False) -> str:
    up = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="noindex">
    <title>{e(title)} | Pinecrest Outfitters (practice site)</title>
    <link rel="stylesheet" href="{up}shop.css">
    <link rel="icon" type="image/png" href="{up}../../favicon.png">
</head>
<body>
    <p class="practice-banner">{BANNER}</p>
    <header class="site-header">
        <div class="inner">
            <a class="logo" href="{up}index.html">Pinecrest Outfitters</a>
            <nav class="site-nav" aria-label="Shop">
                <a href="{up}index.html">All products</a>
                <a href="{up}price-list.html">Price list</a>
                <a href="{up}deals.html">Deals</a>
                <a href="{up}search.html">Search</a>
            </nav>
        </div>
    </header>
    <main>
{body}
    </main>
    <footer class="site-footer">
        <div class="inner">
            <p>{BANNER}. Pinecrest Outfitters is not a real company. Scraping rules: <a href="{up}../robots.txt">robots.txt</a>. &copy; 2026 Ray de la Paz.</p>
        </div>
    </footer>{f'''
    <script src="{up}shop.js"></script>''' if script else ''}
</body>
</html>
"""


def card(p: dict, prefix: str = "") -> str:
    if p["rating"] is None:
        rating = '<p class="rating no-rating">No reviews yet</p>'
    else:
        n = p["review_count"]
        rating = (f'<p class="rating" data-rating="{p["rating"]:.1f}">★ {p["rating"]:.1f} '
                  f'<span class="review-count">({n} review{"" if n == 1 else "s"})</span></p>')
    stock = p["stock_status"]
    return f"""            <li class="product-card" data-sku="{e(p['sku'])}">
                <h2 class="product-name"><a href="{prefix}products/{e(p['sku'])}.html">{e(p['name'])}</a></h2>
                <p class="product-category">{e(p['category'])}</p>
                <p class="price" data-price="{p['price']:.2f}">{money(p['price'])}</p>
                {rating}
                <p class="stock {stock.replace('_', '-')}">{STOCK_LABEL[stock]}</p>
            </li>"""


def load_products(path: Path) -> list[dict]:
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            r["price"] = float(r["price"])
            r["rating"] = float(r["rating"]) if r["rating"] else None
            r["review_count"] = int(r["review_count"])
            r["weight_kg"] = float(r["weight_kg"]) if r["weight_kg"] else None
            rows.append(r)
    return rows


def build(products_csv: Path, out: Path) -> dict:
    products = load_products(products_csv)
    shop = out / "shop"
    if shop.exists():
        shutil.rmtree(shop)
    (shop / "products").mkdir(parents=True)
    (shop / "staff").mkdir()
    (out / "robots.txt").write_text(ROBOTS, encoding="utf-8")
    (shop / "robots.txt").write_text(ROBOTS, encoding="utf-8")
    (shop / "shop.css").write_text(CSS, encoding="utf-8")
    (shop / "shop.js").write_text(JS, encoding="utf-8")
    categories = sorted({p["category"] for p in products})

    # --- paginated catalog --------------------------------------------------
    n_pages = math.ceil(len(products) / PER_PAGE)
    name = lambda k: "index.html" if k == 1 else f"page-{k}.html"
    for k in range(1, n_pages + 1):
        chunk = products[(k - 1) * PER_PAGE: k * PER_PAGE]
        first, last = (k - 1) * PER_PAGE + 1, (k - 1) * PER_PAGE + len(chunk)
        prev = f'<a class="prev" rel="prev" href="{name(k - 1)}">← Previous</a>' if k > 1 else '<span class="prev disabled">← Previous</span>'
        nxt = f'<a class="next" rel="next" href="{name(k + 1)}">Next →</a>' if k < n_pages else '<span class="next disabled">Next →</span>'
        cats = " · ".join(f'<a href="category-{slug(c)}.html">{e(c)}</a>' for c in categories)
        body = f"""        <h1>All products</h1>
        <p class="category-links">Categories: {cats}</p>
        <p class="result-count">Showing {first}–{last} of {len(products)} products</p>
        <ul class="product-grid">
{chr(10).join(card(p) for p in chunk)}
        </ul>
        <nav class="pagination" aria-label="Pages">
            {prev}
            <span class="current">Page <span class="page-number">{k}</span> of <span class="page-total">{n_pages}</span></span>
            {nxt}
        </nav>"""
        (shop / name(k)).write_text(page(f"All products, page {k}", body), encoding="utf-8")

    # --- category pages -----------------------------------------------------
    for c in categories:
        chunk = [p for p in products if p["category"] == c]
        body = f"""        <nav class="breadcrumbs" aria-label="Breadcrumb"><ol><li><a href="index.html">Shop</a></li><li aria-current="page">{e(c)}</li></ol></nav>
        <h1>{e(c)}</h1>
        <p class="result-count">{len(chunk)} products</p>
        <ul class="product-grid">
{chr(10).join(card(p) for p in chunk)}
        </ul>"""
        (shop / f"category-{slug(c)}.html").write_text(page(c, body), encoding="utf-8")

    # --- product detail pages -----------------------------------------------
    for p in products:
        weight = f"{p['weight_kg']:.2f} kg" if p["weight_kg"] is not None else "Not listed"
        rating = (f'<p class="rating" data-rating="{p["rating"]:.1f}">★ <span class="rating-value">{p["rating"]:.1f}</span> out of 5 '
                  f'<span class="review-count">({p["review_count"]} reviews)</span></p>' if p["rating"] is not None
                  else '<p class="rating no-rating">No reviews yet</p>')
        stock = p["stock_status"]
        ld = {"@context": "https://schema.org", "@type": "Product", "sku": p["sku"], "name": p["name"], "category": p["category"],
              "brand": {"@type": "Brand", "name": p["brand"]},
              "offers": {"@type": "Offer", "price": f"{p['price']:.2f}", "priceCurrency": "USD",
                         "availability": "https://schema.org/" + {"in_stock": "InStock", "low_stock": "LimitedAvailability", "out_of_stock": "OutOfStock"}[stock]}}
        if p["rating"] is not None:
            ld["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": p["rating"], "reviewCount": p["review_count"]}
        body = f"""        <nav class="breadcrumbs" aria-label="Breadcrumb"><ol><li><a href="../index.html">Shop</a></li><li><a href="../category-{slug(p['category'])}.html">{e(p['category'])}</a></li><li aria-current="page">{e(p['name'])}</li></ol></nav>
        <article class="product" data-sku="{e(p['sku'])}">
            <h1 class="product-title">{e(p['name'])}</h1>
            <p class="sku">SKU: <span class="sku-value">{e(p['sku'])}</span></p>
            <p class="price" data-price="{p['price']:.2f}">{money(p['price'])}</p>
            <p class="category">Category: <a href="../category-{slug(p['category'])}.html">{e(p['category'])}</a></p>
            {rating}
            <p class="stock {stock.replace('_', '-')}">{STOCK_LABEL[stock]}</p>
            <p class="description">{e(p['brand'])} {e(p['product_type'].lower())} in {e(p['color'].lower())}. {BLURB[p['category']]}</p>
            <table class="specs">
                <caption>Specifications</caption>
                <tbody>
                    <tr><th scope="row">Brand</th><td>{e(p['brand'])}</td></tr>
                    <tr><th scope="row">Type</th><td>{e(p['product_type'])}</td></tr>
                    <tr><th scope="row">Weight</th><td>{weight}</td></tr>
                    <tr><th scope="row">Color</th><td>{e(p['color'])}</td></tr>
                    <tr><th scope="row">Launched</th><td>{e(p['launch_date'])}</td></tr>
                    <tr><th scope="row">Warranty</th><td>{'Lifetime' if p['brand'] == 'Pinecrest' else '2 years'}</td></tr>
                </tbody>
            </table>
        </article>
        <script type="application/ld+json">{json.dumps(ld)}</script>"""
        (shop / "products" / f"{p['sku']}.html").write_text(page(p["name"], body, depth=1), encoding="utf-8")

    # --- price list: two HTML tables for pandas.read_html --------------------
    rows = "\n".join(
        f"                    <tr><td>{e(p['sku'])}</td><td>{e(p['name'])}</td><td>{e(p['category'])}</td><td>{money(p['price'])}</td>"
        f"<td>{'' if p['rating'] is None else format(p['rating'], '.1f')}</td><td>{STOCK_LABEL[p['stock_status']]}</td></tr>" for p in products)
    stores = "\n".join(f"                    <tr><td>{c}</td><td>{s}</td><td>{h}</td><td>{ph}</td></tr>" for c, s, h, ph in STORES)
    body = f"""        <h1>Price list</h1>
        <p>Every product in one table, then our store hours.</p>
        <div class="table-scroll">
            <table id="price-list">
                <caption>Product price list</caption>
                <thead><tr><th>SKU</th><th>Product</th><th>Category</th><th>Price</th><th>Rating</th><th>Availability</th></tr></thead>
                <tbody>
{rows}
                </tbody>
            </table>
        </div>
        <h2>Stores</h2>
        <div class="table-scroll">
            <table id="store-hours">
                <caption>Store hours</caption>
                <thead><tr><th>City</th><th>State</th><th>Open daily</th><th>Phone</th></tr></thead>
                <tbody>
{stores}
                </tbody>
            </table>
        </div>"""
    (shop / "price-list.html").write_text(page("Price list", body), encoding="utf-8")

    # --- deals: filled in by JavaScript after a delay ------------------------
    rated = sorted((p for p in products if p["rating"] is not None and p["stock_status"] != "out_of_stock"),
                   key=lambda p: (-p["review_count"], p["sku"]))[:24]
    deals = []
    for i, p in enumerate(rated):
        pct = (15, 20, 25, 30)[i % 4]
        deals.append({"sku": p["sku"], "name": p["name"], "category": p["category"], "price": p["price"],
                      "discount_pct": pct, "deal_price": round(p["price"] * (1 - pct / 100), 2)})
    (shop / "deals.json").write_text(json.dumps({"note": BANNER, "deals": deals}, indent=1) + "\n", encoding="utf-8")
    body = """        <h1>Deals of the week</h1>
        <p class="notice">This list is added by JavaScript about 1.5 seconds after the page loads, and "Load more" adds 8 more each time.
        A plain HTTP request sees only the "Loading" message. The data comes from <a href="deals.json">deals.json</a>.</p>
        <p id="loading">Loading deals…</p>
        <p id="deal-status" class="result-count" aria-live="polite"></p>
        <ul id="deal-list" class="product-grid"></ul>
        <button type="button" id="load-more" hidden>Load more</button>
        <noscript><p>This page needs JavaScript.</p></noscript>"""
    (shop / "deals.html").write_text(page("Deals", body, script=True), encoding="utf-8")

    # --- search form ----------------------------------------------------------
    public = [{k: p[k] for k in ("sku", "name", "category", "product_type", "brand", "price", "rating", "review_count", "stock_status")}
              for p in products]
    (shop / "products.json").write_text(json.dumps({"note": BANNER, "count": len(public), "products": public}, indent=1) + "\n", encoding="utf-8")
    options = "".join(f'<option value="{e(c)}">{e(c)}</option>' for c in categories)
    body = f"""        <h1>Search</h1>
        <form id="search-form" class="filters" action="search.html" method="get">
            <label>Name contains <input type="search" name="q" placeholder="tent"></label>
            <label>Category <select name="category"><option value="">Any</option>{options}</select></label>
            <label>Max price <input type="number" name="max_price" min="0" step="1" placeholder="200"></label>
            <label class="inline"><input type="checkbox" name="in_stock" value="1"> Hide out of stock</label>
            <button type="submit">Search</button>
        </form>
        <p id="search-count" class="result-count" aria-live="polite">Loading…</p>
        <ul id="search-results" class="product-grid"></ul>
        <p class="notice">The form sends a GET request (look at the address bar after you search). The results are filtered in the browser
        from <a href="products.json">products.json</a>, so the first 60 matches appear only after JavaScript runs.</p>"""
    (shop / "search.html").write_text(page("Search", body, script=True), encoding="utf-8")

    # --- a page robots.txt disallows -----------------------------------------
    body = """        <h1>Staff area</h1>
        <p class="notice">robots.txt disallows <code>/practice/shop/staff/</code>. A polite scraper checks the rules first and never requests this page.</p>"""
    (shop / "staff" / "index.html").write_text(page("Staff area", body, depth=1), encoding="utf-8")

    return {"products": len(products), "catalog_pages": n_pages, "categories": len(categories), "deals": len(deals),
            "files": sum(1 for _ in shop.rglob("*") if _.is_file()) + 1}


FIXED_ZIP_TIME = (2026, 1, 1, 0, 0, 0)


def write_zip(practice: Path, zip_path: Path) -> int:
    """Pack the practice folder as practice/... with sorted names and fixed timestamps (byte-identical reruns)."""
    files = sorted((f for f in practice.rglob("*") if f.is_file()), key=lambda f: f.relative_to(practice).as_posix())
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in files:
            zi = zipfile.ZipInfo("practice/" + f.relative_to(practice).as_posix(), FIXED_ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, f.read_bytes())
    return len(files)


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description="Build the practice shop from products.csv.")
    ap.add_argument("--products", type=Path, default=here / "products.csv")
    ap.add_argument("--out", type=Path, default=here.parent / "practice", help="folder that will contain shop/ and robots.txt")
    ap.add_argument("--zip", type=Path, default=here / "pinecrest-practice-site.zip",
                    help="where to write the offline copy of the practice folder")
    args = ap.parse_args()
    print(build(args.products, args.out))
    n = write_zip(args.out, args.zip)
    print(f"{args.zip.name}: {n} files, {args.zip.stat().st_size / 1e6:.2f} MB")
