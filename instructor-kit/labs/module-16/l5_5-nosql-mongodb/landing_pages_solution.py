# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 5.5-B · Landing pages and what is in the carts (SOLUTION)
# Question 1: which landing page (the FIRST page of a session) starts the most visits,
#             and which one leads to an order most often?
# Question 2: which five products are put into carts most often, by units?
#
# Practices: the aggregation pipeline ($addFields, $group, $match after $group, $sort,
# $unwind, $limit) and flattening with pd.json_normalize(record_path=...).

# %% Load the sessions into a collection (done for you)
import json

import mongomock
import pandas as pd

with open(DATA / "web_sessions.json", encoding="utf-8") as f:
    sessions = json.load(f)["sessions"]

coll = mongomock.MongoClient()["pinecrest"]["sessions"]
coll.insert_many(sessions)
print("sessions in the collection:", coll.count_documents({}))

# %% Step 1: one output document per landing page
# {"$arrayElemAt": ["$pages.path", 0]} is "element 0 of the list of page paths".
landing = pd.DataFrame(list(coll.aggregate([
    {"$addFields": {"landing": {"$arrayElemAt": ["$pages.path", 0]}}},
    {"$group": {"_id": "$landing",
                "sessions": {"$sum": 1},
                "orders": {"$sum": {"$cond": ["$converted", 1, 0]}}}},
    {"$match": {"sessions": {"$gte": 80}}},           # after $group this is HAVING
    {"$sort": {"sessions": -1}},
]))).rename(columns={"_id": "landing"})[["landing", "sessions", "orders"]]

# finish the percentage in pandas (mongomock has no $round)
landing["order_pct"] = (100 * landing["orders"] / landing["sessions"]).round(1)
print("1. landing pages with at least 80 sessions:")
print(landing.to_string(index=False))
best = landing.sort_values("order_pct", ascending=False).iloc[0]
print(f"   most visits start at {landing.iloc[0]['landing']!r}; "
      f"highest order rate: {best['landing']!r} ({best['order_pct']}%, {best['orders']} orders)")
print("   Small groups: 8 orders out of 80 sessions is not a firm 10.0%. Report the counts too.")

# %% Step 2: the five products with the most units in carts
top = pd.DataFrame(list(coll.aggregate([
    {"$unwind": "$cart.items"},                        # one document per cart line
    {"$group": {"_id": "$cart.items.sku",
                "units": {"$sum": "$cart.items.qty"},
                "carts": {"$sum": 1}}},
    {"$sort": {"units": -1, "_id": 1}},
    {"$limit": 5},
]))).rename(columns={"_id": "sku"})[["sku", "units", "carts"]]
print("2. top five SKUs by units in carts:")
print(top.to_string(index=False))

# %% Step 3: check the pipeline a second way, in pandas
docs = list(coll.find({"cart.items.0": {"$exists": True}},
                      {"_id": 0, "session_id": 1, "cart.items": 1}))
items = pd.json_normalize(docs, record_path=["cart", "items"], meta=["session_id"])
print("3. one row per cart line:", items.shape, list(items.columns))
check = items.groupby("sku")["qty"].sum().sort_values(ascending=False)
print("   pandas says the top SKU is", check.index[0], "with", int(check.iloc[0]), "units")
print("   total units in all carts:", int(items["qty"].sum()),
      "| lines:", len(items), "| sessions with a cart:", items["session_id"].nunique())
