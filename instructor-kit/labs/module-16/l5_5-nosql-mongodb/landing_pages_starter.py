# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 5.5-B · Landing pages and what is in the carts (STARTER)
# Question 1: which landing page (the FIRST page of a session) starts the most visits,
#             and which one leads to an order most often?
# Question 2: which five products are put into carts most often, by units?
#
# Practices: the aggregation pipeline ($addFields, $group, $match after $group, $sort,
# $unwind, $limit) and flattening with pd.json_normalize(record_path=...).
#
# Expected when you finish: a table of six landing pages with sessions, orders and
# order_pct; a table of five SKUs with units and carts; and a pandas check that agrees
# with the pipeline about the top SKU.

# %% Load the sessions into a collection (done for you)
import json

import mongomock
import pandas as pd

with open(DATA / "web_sessions.json", encoding="utf-8") as f:
    sessions = json.load(f)["sessions"]

coll = mongomock.MongoClient()["pinecrest"]["sessions"]
coll.insert_many(sessions)
print("sessions in the collection:", coll.count_documents({}))


def run(pipeline):
    """Run a pipeline and return its documents as a DataFrame."""
    return pd.DataFrame(list(coll.aggregate(pipeline)))


# %% Step 1: one output document per landing page
# The first stage is written for you: it adds a field `landing` to every session.
# {"$arrayElemAt": ["$pages.path", 0]} is "element 0 of the list of page paths".
pipeline_1 = [
    {"$addFields": {"landing": {"$arrayElemAt": ["$pages.path", 0]}}},
    # TODO 1a: {"$group": ...} with _id "$landing", sessions = {"$sum": 1} and
    #          orders = {"$sum": {"$cond": ["$converted", 1, 0]}}
    # TODO 1b: {"$match": ...} keeping groups with at least 80 sessions (this is HAVING)
    # TODO 1c: {"$sort": ...} by sessions, largest first
]
landing = run(pipeline_1)
if "sessions" in landing.columns:
    landing = landing.rename(columns={"_id": "landing"})[["landing", "sessions", "orders"]]
    # TODO 1d: add the column order_pct = 100 * orders / sessions, rounded to 1 decimal (in pandas)
    print("1. landing pages with at least 80 sessions:")
    print(landing.to_string(index=False))
else:
    print("1. TODO 1a-1c not done yet: the pipeline still returns", len(landing), "raw session documents.")

# %% Step 2: the five products with the most units in carts
pipeline_2 = [
    # TODO 2a: {"$unwind": "$cart.items"}   -> one document per cart line
    # TODO 2b: {"$group": ...} with _id "$cart.items.sku", units = sum of "$cart.items.qty",
    #          carts = {"$sum": 1}
    # TODO 2c: {"$sort": {"units": -1, "_id": 1}}  then  {"$limit": 5}
]
if pipeline_2:
    top = run(pipeline_2).rename(columns={"_id": "sku"})[["sku", "units", "carts"]]
    print("2. top five SKUs by units in carts:")
    print(top.to_string(index=False))
else:
    print("2. TODO 2a-2c not done yet: pipeline_2 is empty.")

# %% Step 3: check the pipeline a second way, in pandas
docs = list(coll.find({"cart.items.0": {"$exists": True}},
                      {"_id": 0, "session_id": 1, "cart.items": 1}))
# TODO 3: items = pd.json_normalize(docs, record_path=["cart", "items"], meta=["session_id"])
#         then group by sku, sum qty, and compare the top SKU with Step 2.
items = None
if items is None:
    print("3. TODO 3 not done yet:", len(docs), "sessions with a cart are waiting to be flattened.")
else:
    print("3. one row per cart line:", items.shape, list(items.columns))
