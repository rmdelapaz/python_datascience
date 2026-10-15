# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 7.4-A · A catalog browser for the shop floor (SOLUTION)
# Store staff ask: "what do we carry in this category, under this price, that is in stock?"
# An app answers the reader's own version of that question.
#
#   streamlit run catalog_browser_solution.py     opens the app in your browser
#   python catalog_browser_solution.py            checks it with AppTest: no server, no browser
#
# Practices: cached loading, sidebar widgets with keys, a reset callback, st.stop() for an
# empty result, metrics in columns, a table, a download button, and a test.

import pandas as pd
import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx

if get_script_run_ctx(suppress_warning=True) is None:     # plain `python file.py`: silence Streamlit's bare-mode notes
    import logging
    for name in ("streamlit.runtime.caching.cache_data_api", "streamlit.runtime.scriptrunner_utils.script_run_context"):
        logging.getLogger(name).setLevel(logging.ERROR)

CATEGORIES = ["Accessories", "Apparel", "Camp Kitchen", "Climbing", "Footwear", "Packs", "Sleeping", "Snow", "Tents"]
MAX_PRICE = 620


@st.cache_data
def load_products(path):
    """The only slow step, and it does not depend on any widget: cache it."""
    products = pd.read_csv(path)
    return products[["sku", "name", "category", "brand", "price", "rating", "review_count", "stock_status"]]


def reset_filters():
    st.session_state["categories"] = ["Tents"]
    st.session_state["price"] = (0, MAX_PRICE)
    st.session_state["in_stock"] = False


def main():
    st.set_page_config(page_title="Pinecrest Catalog", layout="wide")
    products = load_products(str(DATA / "products.csv"))
    if "categories" not in st.session_state:          # first run of this session
        reset_filters()

    with st.sidebar:
        st.header("Filters")
        categories = st.multiselect("Categories", CATEGORIES, key="categories")
        low, high = st.slider("Price range ($)", 0, MAX_PRICE, step=10, key="price")
        in_stock = st.toggle("In stock only", key="in_stock")
        st.button("Reset filters", on_click=reset_filters)

    st.title("Pinecrest catalog browser")
    view = products[products["category"].isin(categories) & products["price"].between(low, high)]
    if in_stock:
        view = view[view["stock_status"] == "in_stock"]
    if view.empty:
        st.warning("No products match these filters. Choose a category or widen the price range.")
        st.stop()
    st.caption(f"{len(view)} of {len(products)} products · priced {low} to {high} dollars · fictional course data")

    k1, k2, k3 = st.columns(3)
    k1.metric("Products", len(view))
    k2.metric("Median price", f"${view['price'].median():,.2f}")
    k3.metric("Mean rating", f"{view['rating'].mean():.2f}", help="Products with no reviews yet are left out")

    table = view.sort_values("price")[["name", "category", "brand", "price", "rating", "stock_status"]]
    st.dataframe(table, hide_index=True, width="stretch")
    st.download_button("Download these products as CSV", data=table.to_csv(index=False),
                       file_name="pinecrest_catalog.csv", mime="text/csv")


def self_check():
    """Drive the app the way a reader would, and print what it shows."""
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file(__file__, default_timeout=30).run()
    assert not at.exception, at.exception
    print("start      :", [(m.label, m.value) for m in at.metric])
    at.sidebar.multiselect[0].set_value(["Tents", "Sleeping"]).run()
    at.sidebar.slider[0].set_value((0, 100)).run()
    print("under $100 :", [(m.label, m.value) for m in at.metric], "|", at.caption[0].value)
    at.sidebar.toggle[0].set_value(True).run()
    print("in stock   :", at.metric[0].value, "products")
    at.sidebar.multiselect[0].set_value([]).run()
    print("no category:", at.warning[0].value, "| metrics shown:", len(at.metric), "| errors:", len(at.exception))
    at.sidebar.button[0].click().run()
    print("after reset:", at.sidebar.multiselect[0].value, at.sidebar.slider[0].value, at.sidebar.toggle[0].value,
          "|", at.metric[0].value, "products")
    assert not at.exception


# %% Run as an app, or check without a browser (done for you; do not change)
if get_script_run_ctx(suppress_warning=True) is not None:
    main()                                   # started by `streamlit run` (or by AppTest below)
elif __name__ == "__main__":
    self_check()                             # started by `python <this file>`: no server, no browser
