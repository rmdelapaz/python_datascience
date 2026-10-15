# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 7.4-B · A shortlist that remembers (SOLUTION)
# A customer is choosing a tent. The app lets staff add products to a shortlist and shows the total.
# The list must survive reruns, so it lives in st.session_state and is changed in callbacks.
#
#   streamlit run gear_shortlist_solution.py      opens the app
#   python gear_shortlist_solution.py             checks it with AppTest
#
# Practices: the rerun model, an ordinary variable that forgets, session state that remembers,
# callbacks with on_click, and predicting what a test will print before running it.

import pandas as pd
import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx

if get_script_run_ctx(suppress_warning=True) is None:     # plain `python file.py`: silence Streamlit's bare-mode notes
    import logging
    for name in ("streamlit.runtime.caching.cache_data_api", "streamlit.runtime.scriptrunner_utils.script_run_context"):
        logging.getLogger(name).setLevel(logging.ERROR)


@st.cache_data
def load_tents(path):
    products = pd.read_csv(path)
    tents = products[products["category"] == "Tents"].sort_values("name")
    return tents[["name", "price"]].reset_index(drop=True)


def add_to_shortlist():
    choice = st.session_state["choice"]               # the selectbox's current value, read by its key
    if choice not in st.session_state["shortlist"]:
        st.session_state["shortlist"].append(choice)


def clear_shortlist():
    st.session_state["shortlist"] = []


def main():
    tents = load_tents(str(DATA / "products.csv"))
    if "shortlist" not in st.session_state:           # runs once per browser tab
        st.session_state["shortlist"] = []

    st.title("Tent shortlist")
    st.selectbox("Tent", tents["name"], key="choice")
    left, right = st.columns(2)
    left.button("Add to shortlist", on_click=add_to_shortlist)
    right.button("Clear", on_click=clear_shortlist)

    reruns_plain = 0                                  # an ordinary variable: starts over on every rerun
    reruns_plain += 1

    chosen = tents[tents["name"].isin(st.session_state["shortlist"])]
    k1, k2, k3 = st.columns(3)
    k1.metric("On the shortlist", len(chosen))
    k2.metric("Total price", f"${chosen['price'].sum():,.2f}")
    k3.metric("Ordinary counter", reruns_plain)
    st.dataframe(chosen, hide_index=True)


def self_check():
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file(__file__, default_timeout=30).run()
    assert not at.exception, at.exception
    names = list(at.selectbox[0].options)
    print(len(names), "tents | first two:", names[:2])

    def report(label):
        print(f"{label:<22}", [m.value for m in at.metric])

    report("start")
    at.button[0].click().run()                        # add the first tent
    report("add first tent")
    at.button[0].click().run()                        # the same tent again: no duplicate
    report("add it again")
    at.selectbox[0].select(names[1]).run()            # choosing is a rerun too
    report("choose second tent")
    at.button[0].click().run()
    report("add second tent")
    at.button[1].click().run()                        # clear
    report("clear")
    assert not at.exception


# %% Run as an app, or check without a browser (done for you; do not change)
if get_script_run_ctx(suppress_warning=True) is not None:
    main()                                   # started by `streamlit run` (or by AppTest below)
elif __name__ == "__main__":
    self_check()                             # started by `python <this file>`: no server, no browser
