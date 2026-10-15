# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import OFFLINE, fixtures

# %% [markdown]
# # Lab 6.1-B · Ask the API: which category costs the most? (STARTER)
# Question: among Tents, Snow and Camp Kitchen, which category has the highest median
# list price, and how many products does each have? What does the API say when you ask
# for a category or a product that does not exist?
#
# Practices: query parameters as a dictionary, r.url, r.json(), JSON to DataFrame,
# an empty result versus an error, and reading an error message from a JSON body.
#
# Two modes, one function (api_get):
#   online  : the practice API on your own computer. Start it first, in a second terminal:
#                 python data/mock_api.py
#   offline : LABS_OFFLINE=1 -> saved responses in labs/module-16/_fixtures/, no network.
#
# Expected when you finish: the URL requests built for "Camp Kitchen" (look at the space),
# a 75-row DataFrame, a three-row summary sorted by median price, the status and total for
# a category that does not exist, the API's own message for a product that does not exist,
# and a one-sentence answer.

# %% Setup (done for you)
import json
import os
import re

import pandas as pd
import requests

API = os.environ.get("PINECREST_API", "http://127.0.0.1:8000")
HEADERS = {"User-Agent": "pinecrest-course-bot/1.0 (learning project; contact: you@example.com)"}


def api_get(path, params=None):
    """GET one API address and return the Response (no status check here)."""
    if OFFLINE:
        return saved_response(path, params)
    return requests.get(API + path, params=params, headers=HEADERS, timeout=10)


def saved_response(path, params):
    """Rebuild a real requests.Response from the saved body, status and headers."""
    key = path + ("_" + "_".join(f"{k}-{v}" for k, v in sorted(params.items())) if params else "")
    name = "api_" + re.sub(r"[^A-Za-z0-9.-]+", "_", key).strip("_") + ".json"
    folder = fixtures(__file__)
    meta = json.loads((folder / (name + ".meta.json")).read_text(encoding="utf-8"))
    resp = requests.Response()
    resp.status_code, resp.reason = meta["status"], meta["reason"]
    resp.url = requests.Request("GET", API + path, params=params).prepare().url
    resp.headers.update(meta["headers"])
    resp._content = (folder / name).read_bytes()
    resp.encoding = requests.utils.get_encoding_from_headers(resp.headers)
    return resp


print("mode:", "offline (saved responses in _fixtures/)" if OFFLINE else f"online ({API})")

# %% Step 1: one category, and the URL that requests built
# TODO 1a: pass the query parameters as a dictionary: category "Camp Kitchen", per_page 100.
r = api_get("/products", params=None)
r.raise_for_status()
print("1. URL:", r.url)
print("   Content-Type:", r.headers["Content-Type"])
# TODO 1b: parse the body with r.json() instead of the empty dictionary below.
data = {}
print("   keys:", list(data))
if "total" in data:
    print("   total:", data["total"], "| items on this page:", len(data["items"]), "| next:", data["next"])

# %% Step 2: three categories into one DataFrame
frames = []
for category in ["Tents", "Snow", "Camp Kitchen"]:
    # TODO 2a: r = api_get("/products", params={...})   (this category, per_page 100)
    # TODO 2b: r.raise_for_status()
    # TODO 2c: frames.append(pd.DataFrame(r.json()["items"]))
    pass
products = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=["category", "price"])
print("2. products:", products.shape)

# TODO 2d: group `products` by category and aggregate price: products="count",
#          median_price="median", max_price="max"; sort by median_price, largest first.
summary = pd.DataFrame(columns=["products", "median_price", "max_price"])
print(summary.to_string() if len(summary) else "   TODO 2 not done yet: the summary is empty.")

# %% Step 3: an empty result is not an error
r = api_get("/products", params={"category": "Skis", "per_page": 100})
# TODO 3: print the status code, the "total" and the number of items. Predict them first.
print("3. category Skis: status", None, "| total", None, "| items", None)

# %% Step 4: a real error explains itself in the body
r = api_get("/products/TNT-9999")
print("4. product TNT-9999: status", r.status_code, "| ok:", r.ok)
# TODO 4: call r.raise_for_status() inside try / except requests.exceptions.HTTPError as err,
#         and in the except branch print err.response.json()["error"]["message"].
print("   TODO 4 not done yet: the error has not been handled.")

# %% Step 5: the answer
if len(summary):
    top = summary.index[0]
    print(f"5. Highest median price: {top} (${summary.loc[top, 'median_price']:.2f} "
          f"across {summary.loc[top, 'products']} products).")
else:
    print("5. No answer yet: finish TODO 2.")
