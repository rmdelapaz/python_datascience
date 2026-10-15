# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 7.4-A · A catalog browser for the shop floor (STARTER)
# Store staff ask: "what do we carry in this category, under this price, that is in stock?"
#
#   streamlit run catalog_browser_starter.py      opens the app in your browser (keep it open while you work)
#   python catalog_browser_starter.py             checks it with AppTest: no server, no browser
#
# Expected when you finish (from `python catalog_browser_starter.py`): the check prints
# "metrics: 3", "widgets in the sidebar: 4" and "empty selection handled: True", with no errors.

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
    # TODO 2: also reset "price" to (0, MAX_PRICE) and "in_stock" to False


def main():
    st.set_page_config(page_title="Pinecrest Catalog", layout="wide")
    products = load_products(str(DATA / "products.csv"))
    if "categories" not in st.session_state:          # first run of this session
        reset_filters()

    with st.sidebar:
        st.header("Filters")
        categories = st.multiselect("Categories", CATEGORIES, key="categories")
        # TODO 1: add, each with a key:
        #   low, high = st.slider("Price range ($)", 0, MAX_PRICE, step=10, key="price")
        #   in_stock  = st.toggle("In stock only", key="in_stock")
        #   st.button("Reset filters", on_click=reset_filters)
        low, high, in_stock = 0, MAX_PRICE, False

    st.title("Pinecrest catalog browser")
    view = products[products["category"].isin(categories) & products["price"].between(low, high)]
    # TODO 3: if in_stock is on, keep only rows whose stock_status is "in_stock".
    # TODO 4: if `view` is empty, show st.warning(...) and end this run with st.stop().
    st.caption(f"{len(view)} of {len(products)} products · priced {low} to {high} dollars · fictional course data")

    # TODO 5: three metrics side by side with st.columns(3): Products, Median price, Mean rating.

    table = view.sort_values("price")[["name", "category", "brand", "price", "rating", "stock_status"]]
    st.dataframe(table, hide_index=True, width="stretch")
    # TODO 6: st.download_button("Download these products as CSV", data=table.to_csv(index=False),
    #                            file_name="pinecrest_catalog.csv", mime="text/csv")


def self_check():
    """Runs the app in memory and reports how far you have got. It never fails on an unfinished TODO."""
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file(__file__, default_timeout=30).run()
    print("errors:", len(at.exception), "| title:", at.title[0].value if at.title else None)
    print("metrics:", len(at.metric), "(3 when TODO 5 is done)")
    widgets = len(at.sidebar.multiselect) + len(at.sidebar.slider) + len(at.sidebar.toggle) + len(at.sidebar.button)
    print("widgets in the sidebar:", widgets, "(4 when TODO 1 is done)")
    at.sidebar.multiselect[0].set_value([]).run()
    print("empty selection handled:", len(at.warning) == 1 and not at.exception, "(True when TODO 4 is done)")


# %% Run as an app, or check without a browser (done for you; do not change)
if get_script_run_ctx(suppress_warning=True) is not None:
    main()                                   # started by `streamlit run` (or by AppTest below)
elif __name__ == "__main__":
    self_check()                             # started by `python <this file>`: no server, no browser
