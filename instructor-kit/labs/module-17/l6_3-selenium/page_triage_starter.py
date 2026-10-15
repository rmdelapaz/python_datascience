# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import OFFLINE, OUTPUT, fixtures

# %% [markdown]
# # Lab 6.3-B · Static or dynamic? Triage three pages (STARTER)
# Question: before anyone writes a scraper for the Climbing category page, the Deals page
# and the Search page, decide for each one: is the data in the HTML that requests receives,
# or does JavaScript add it afterward? And if it is added afterward, where does it come from?
#
# You will count the same items twice, once in the raw HTML and once in the page a browser
# finished, and let the two numbers give the verdict.
#
# Practices: telling a static page from a dynamic one, find the data file a page loads,
# headless Chrome with explicit waits, choosing from a menu and submitting a form (two
# waits after a submit), page_source into Beautiful Soup, and quitting the browser in finally.
#
# Three modes, one function (rendered):
#   online, Chrome works : a headless browser opens each page at BASE_URL and runs your steps.
#   online, no browser   : a clear message, then the saved copy of the finished page is used.
#   offline              : LABS_OFFLINE=1 -> no browser and no network. The saved copies of the
#                          finished pages in labs/module-17/_fixtures/ are parsed instead.
#                          (The browser TODOs, 2 and 3, are then not exercised: do them with
#                          a partner whose Chrome works, or read them in the solution.)
#
# Expected when you finish: raw counts 24, 0, 0; counts after JavaScript 24, 8, 24; the two
# data files named in shop.js; a three-row triage table with a verdict for each page; the
# Climbing category page and the Climbing search holding the same 24 SKUs; and one line
# comparing the 8 deals on the finished page with the 24 in deals.json.

# %% Setup (done for you)
import json
import os
import re
import time
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

pd.set_option("display.width", 150)
pd.set_option("display.max_columns", 20)

# The practice shop. Teaching from the unzipped copy? Use "http://127.0.0.1:8001/practice/shop/".
BASE_URL = os.environ.get("PINECREST_BASE_URL", "https://rays-python-datascience.netlify.app/practice/shop/")
USER_AGENT = "pinecrest-course-bot/1.0 (learning project; contact: you@example.com)"
HEADERS = {"User-Agent": USER_AGENT}
DELAY = 1                                           # the Crawl-delay in the shop's robots.txt


def get(path):
    """GET one file of the practice shop with requests and return the Response."""
    url = urljoin(BASE_URL, path)
    if OFFLINE:
        return saved_response("shop_" + path.replace("../", "").replace("/", "_"), url)
    resp = requests.get(url, headers=HEADERS, timeout=10)
    time.sleep(DELAY)
    return resp


def saved_response(name, url):
    """Rebuild a real requests.Response from a saved body and its saved status and headers."""
    folder = fixtures(__file__)
    meta = json.loads((folder / (name + ".meta.json")).read_text(encoding="utf-8"))
    resp = requests.Response()
    resp.status_code, resp.reason, resp.url = meta["status"], meta["reason"], url
    resp.headers.update(meta["headers"])
    resp._content = (folder / name).read_bytes()
    resp.encoding = requests.utils.get_encoding_from_headers(resp.headers)
    return resp


def make_driver():
    """Start headless Chrome with this course's settings. Whoever calls this must quit it."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1000,800")
    options.add_argument(f"--user-agent={USER_AGENT}")
    chrome = os.environ.get("PINECREST_CHROME")     # optional: the path of a Chrome or Chromium program
    if chrome:
        options.binary_location = os.path.expanduser(chrome)
        options.add_argument("--no-sandbox")
    return webdriver.Chrome(options=options)


def rendered(name, url, steps):
    """Return the HTML of a page AFTER its JavaScript has run.

    steps(driver, wait) is your browser work (waits, clicks). The browser is always quit.
    With LABS_OFFLINE=1, or when no browser can start, the saved copy of the finished page
    (_fixtures/rendered_<name>.html) is returned instead, and a line says so.
    """
    saved = fixtures(__file__) / f"rendered_{name}.html"
    if OFFLINE:
        print(f"   [offline] no browser started; reading the saved finished page {saved.name}")
        return saved.read_text(encoding="utf-8")
    try:
        driver = make_driver()
    except Exception as err:                        # no Chrome, or the driver download was blocked
        print(f"   [no browser] Chrome could not be started ({type(err).__name__}).")
        print(f"   Reading the saved finished page {saved.name} instead. See the README for what to do.")
        return saved.read_text(encoding="utf-8")
    try:
        driver.get(url)
        steps(driver, WebDriverWait(driver, 10))
        return driver.page_source
    except WebDriverException as err:               # a wait that timed out, a locator that found nothing
        first_line = (err.msg or "").splitlines()[0] if err.msg else ""
        print(f"   [browser step failed] {type(err).__name__}: {first_line}")
        print(f"   Reading the saved finished page {saved.name} instead.")
        return saved.read_text(encoding="utf-8")
    finally:
        driver.quit()


print("mode:", "offline (saved pages in _fixtures/, no browser)" if OFFLINE else f"online ({BASE_URL})")

# %% Step 1: count the items in the HTML that requests receives
PAGES = {                       # page -> (file, CSS selector of one item)
    "Climbing category": ("category-climbing.html", "li.product-card"),
    # TODO 1: fill in the selector of ONE item on each of these two pages (inspect them in
    #         your browser): a deal is an li with class "deal" inside the element with id
    #         "deal-list"; a search result is an li inside the element with id "search-results".
    "Deals": ("deals.html", "li.todo-1"),
    "Search": ("search.html", "li.todo-1"),
}

raw_soups, raw_counts = {}, {}
for page, (path, selector) in PAGES.items():
    resp = get(path)
    resp.raise_for_status()
    raw_soups[page] = BeautifulSoup(resp.content, "html.parser")
    raw_counts[page] = len(raw_soups[page].select(selector))
    print(f"1. raw HTML of {page:<18} status {resp.status_code} | items: {raw_counts[page]}")

# %% Step 2: the same three pages after a browser has run their JavaScript
RESULTS_READY = EC.presence_of_element_located((By.CSS_SELECTOR, '#search-results[data-loaded="true"]'))


def no_steps(driver, wait):
    """A static page needs nothing: get() already has everything."""


def deals_steps(driver, wait):
    # TODO 2: wait (no sleep) until the first deal is present, with a message for the day it
    #         never comes:
    #         wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#deal-list li.deal")),
    #                    message="the first deals did not appear")
    pass


def search_steps(driver, wait):
    """Use the form the way a person would: choose Climbing from the menu and submit."""
    wait.until(RESULTS_READY, message="the search page never finished loading")
    # TODO 3: choose "Climbing" from the menu named "category", click the submit button, then
    #         wait TWICE: first for the address to change, then for the new page's results.
    #         Select(driver.find_element(By.NAME, "category")).select_by_visible_text("Climbing")
    #         driver.find_element(By.CSS_SELECTOR, "#search-form button[type='submit']").click()
    #         wait.until(EC.url_contains("category=Climbing"), message="the address did not change after submitting")
    #         wait.until(RESULTS_READY, message="the new page's results never finished loading")


STEPS = {"Climbing category": ("category-climbing", no_steps),
         "Deals": ("deals", deals_steps),
         "Search": ("search_climbing", search_steps)}

done_soups, done_counts = {}, {}
for page, (path, selector) in PAGES.items():
    name, steps = STEPS[page]
    print(f"2. rendering {page}:")
    done_soups[page] = BeautifulSoup(rendered(name, urljoin(BASE_URL, path), steps), "html.parser")
    done_counts[page] = len(done_soups[page].select(selector))
    print(f"   items after JavaScript: {done_counts[page]}")
print("   deals status line:", repr(done_soups["Deals"].select_one("#deal-status").get_text()),
      "| search count line:", repr(done_soups["Search"].select_one("#search-count").get_text()))
print("   (Until TODO 1 is done the Deals and Search counts are 0 in both columns.)")

# %% Step 3: for the dynamic pages, where does the data come from?
script = get("shop.js")
script.raise_for_status()
data_files = re.findall(r"fetch\('(.+?)'\)", script.text)
print("3. files the pages' script fetches:", data_files)

# %% Step 4: the verdict
def verdict(raw, done):
    # TODO 4: return one of three texts.
    #   the same number both times, and more than 0 -> "static: requests + Beautiful Soup"
    #   0 in the raw HTML, more than 0 afterward     -> "dynamic: request the data file first"
    #   anything else                                 -> "look again"
    return "TODO 4"


triage = pd.DataFrame({"in_raw_html": raw_counts, "after_javascript": done_counts})
triage["verdict"] = [verdict(r, d) for r, d in zip(triage["in_raw_html"], triage["after_javascript"])]
print("4. triage:")
print(triage.to_string())

# %% Step 5: do the static route and the browser route agree?
static_skus = {card["data-sku"] for card in raw_soups["Climbing category"].select("li.product-card")}
search_skus = {li["data-sku"] for li in done_soups["Search"].select(PAGES["Search"][1])}
print("5. Climbing: category page", len(static_skus), "SKUs | search through the form", len(search_skus),
      "SKUs | same set:", static_skus == search_skus)

# %% Step 6: a finished page is not always the whole data either
resp = get("deals.json")
resp.raise_for_status()
all_deals = len(resp.json()["deals"])
print(f"6. Deals: {done_counts['Deals']} on the finished page | {all_deals} in deals.json")
print("   In one sentence: for which of the three pages would you start a browser at all, and why?")
triage.to_csv(OUTPUT / "page_triage.csv")
print("   saved page_triage.csv in the output folder:", len(pd.read_csv(OUTPUT / "page_triage.csv")), "rows")
