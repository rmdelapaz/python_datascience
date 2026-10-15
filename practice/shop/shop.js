/* Practice shop: fills the deals page and the search page from JSON. Fictional products. */
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
