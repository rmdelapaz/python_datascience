# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 5.5-A · The sale page audit (STARTER)
# Question: the marketing team runs a /sale page. Who looks at it, do they stay,
# and do they buy more often than everyone else?
#
# Practices: query dictionaries, dot notation, operators, $elemMatch, $exists,
# projection + sort + limit. No server needed: mongomock runs inside Python.
#
# Expected when you finish: six numbered results. Line 1 says how many sessions saw /sale
# (a few hundred of the 2,400), line 3 shows two different counts for two similar-sounding
# questions, and line 6 compares the order rate of /sale visitors with all sessions.

# %% Load the sessions into a collection (done for you)
import json

import mongomock

with open(DATA / "web_sessions.json", encoding="utf-8") as f:
    sessions = json.load(f)["sessions"]

coll = mongomock.MongoClient()["pinecrest"]["sessions"]
coll.insert_many(sessions)
total = coll.count_documents({})
print("sessions in the collection:", total)

# Look at one document before you query: field names must be spelled exactly.
print("fields:", list(coll.find_one({}, {"_id": 0})))

# %% Step 1: who saw the sale page?
# "pages.path" means: the path of ANY page in the list.
# TODO 1: write the query dictionary for "some page has the path /sale".
saw_sale = None                     # {"pages.path": ...}
n_sale = coll.count_documents(saw_sale) if saw_sale else None
print("1. saw /sale:", n_sale)

# %% Step 2: add conditions (several pairs in one dictionary mean AND)
# TODO 2a: count the sessions that saw /sale AND converted.
#          Tip: {**saw_sale, "converted": True} copies saw_sale and adds a pair.
# TODO 2b: count the sessions that saw /sale, used a mobile device ("device.type")
#          AND have a cart value of 200 or more ("cart.value" with "$gte").
n_sale_orders = None
n_sale_mobile_big = None
print("2. saw /sale and ordered:", n_sale_orders)
print("   saw /sale, on mobile, cart of $200 or more:", n_sale_mobile_big)

# %% Step 3: a minute or more ON the sale page ($elemMatch) versus the loose version
# The loose query is written for you. It asks: "saw /sale, and SOME page took 60 s".
loose = {"pages.path": "/sale", "pages.seconds": {"$gte": 60}}
# TODO 3: write the strict query: one element of pages has BOTH path "/sale" and seconds >= 60.
strict = None                       # {"pages": {"$elemMatch": {...}}}
print("3. loose (any page took 60 s):", coll.count_documents(loose))
print("   strict (60 s on /sale itself):", coll.count_documents(strict) if strict else None)

# %% Step 4: missing is not null. How many /sale visitors arrived directly (no utm field)?
# TODO 4: use {"$exists": False} on the "utm" field, together with saw_sale.
n_direct = None
print("4. saw /sale with no utm field:", n_direct)

# %% Step 5: the three biggest carts among /sale visitors (projection, sort, limit)
# TODO 5: coll.find(saw_sale, projection).sort("cart.value", -1).limit(3)
#         The projection keeps session_id, device.type and cart.value, and drops _id.
print("5. three biggest carts:")
cursor = []
for doc in cursor:
    print("  ", doc)

# %% Step 6: the answer in one sentence
all_orders = coll.count_documents({"converted": True})
if n_sale and n_sale_orders is not None:
    print(f"6. order rate: {100 * n_sale_orders / n_sale:.1f}% of /sale visitors "
          f"vs {100 * all_orders / total:.1f}% of all sessions")
else:
    print("6. TODO 1 and 2a are not done yet, so there is no order rate to compare.")
