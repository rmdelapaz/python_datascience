# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 7.4-B · A shortlist that remembers (STARTER)
# A customer is choosing a tent. The app lets staff add products to a shortlist and shows the total.
# As shipped, the shortlist is an ordinary variable, so it forgets everything on every rerun.
# Your job: move it into st.session_state and change it in callbacks.
#
#   streamlit run gear_shortlist_starter.py       opens the app (click Add twice and watch the count)
#   python gear_shortlist_starter.py              checks it with AppTest
#
# Expected when you finish: after "add first tent" the first metric says 1; after "add second tent" it
# says 2 and the total is the sum of the two prices; after "clear" it says 0. The third metric,
# "Ordinary counter", says 1 on every line. Before you fix anything: predict what the check prints now.

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
    # TODO 2: read the chosen tent from st.session_state["choice"] and append it to
    #         st.session_state["shortlist"] if it is not already there.
    pass


def clear_shortlist():
    # TODO 3: set st.session_state["shortlist"] to an empty list.
    pass


def main():
    tents = load_tents(str(DATA / "products.csv"))
    # TODO 1: if "shortlist" is not in st.session_state yet, create it as an empty list.

    st.title("Tent shortlist")
    choice = st.selectbox("Tent", tents["name"], key="choice")
    left, right = st.columns(2)

    shortlist = []                                    # an ordinary variable: starts over on every rerun
    if left.button("Add to shortlist"):               # TODO 4: replace the if-block with on_click=add_to_shortlist
        shortlist.append(choice)
    right.button("Clear")                             # TODO 4: on_click=clear_shortlist

    reruns_plain = 0                                  # leave this one as it is: it shows what "forgets" means
    reruns_plain += 1

    chosen = tents[tents["name"].isin(shortlist)]     # TODO 5: use st.session_state["shortlist"] here
    k1, k2, k3 = st.columns(3)
    k1.metric("On the shortlist", len(chosen))
    k2.metric("Total price", f"${chosen['price'].sum():,.2f}")
    k3.metric("Ordinary counter", reruns_plain)
    st.dataframe(chosen, hide_index=True)


def self_check():
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file(__file__, default_timeout=30).run()
    names = list(at.selectbox[0].options)
    print(len(names), "tents | first two:", names[:2], "| errors:", len(at.exception))

    def report(label):
        print(f"{label:<22}", [m.value for m in at.metric])

    report("start")
    at.button[0].click().run()
    report("add first tent")
    at.selectbox[0].select(names[1]).run()
    report("choose second tent")
    at.button[0].click().run()
    report("add second tent")
    at.button[1].click().run()
    report("clear")
    print("When TODO 1-5 are done, the first numbers read 0, 1, 1, 2, 0.")


# %% Run as an app, or check without a browser (done for you; do not change)
if get_script_run_ctx(suppress_warning=True) is not None:
    main()                                   # started by `streamlit run` (or by AppTest below)
elif __name__ == "__main__":
    self_check()                             # started by `python <this file>`: no server, no browser
