# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

"""pytest file for Lab 7.4-A: the five-line safety net from the lesson, grown a little.

    python -m pytest labs/module-20/l7_4-streamlit/test_catalog_browser.py
"""
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from streamlit.testing.v1 import AppTest

APP = str(pathlib.Path(__file__).resolve().parent / "catalog_browser_solution.py")


def fresh():
    at = AppTest.from_file(APP, default_timeout=30).run()
    assert not at.exception
    return at


def test_opens_with_tents():
    at = fresh()
    assert at.title[0].value == "Pinecrest catalog browser"
    assert [m.label for m in at.metric] == ["Products", "Median price", "Mean rating"]
    assert at.metric[0].value == "24"


def test_empty_selection_shows_a_warning_not_an_error():
    at = fresh()
    at.sidebar.multiselect[0].set_value([]).run()
    assert not at.exception
    assert len(at.warning) == 1 and len(at.metric) == 0


def test_reset_restores_all_three_filters():
    at = fresh()
    at.sidebar.multiselect[0].set_value(["Snow"]).run()
    at.sidebar.slider[0].set_value((50, 200)).run()
    at.sidebar.toggle[0].set_value(True).run()
    at.sidebar.button[0].click().run()
    assert at.sidebar.multiselect[0].value == ["Tents"]
    assert at.sidebar.slider[0].value == (0, 620)
    assert at.sidebar.toggle[0].value is False
