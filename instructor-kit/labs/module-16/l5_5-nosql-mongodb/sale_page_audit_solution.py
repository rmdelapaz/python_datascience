# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA

# %% [markdown]
# # Lab 5.5-A · The sale page audit (SOLUTION)
# Question: the marketing team runs a /sale page. Who looks at it, do they stay,
# and do they buy more often than everyone else?
#
# Practices: query dictionaries, dot notation, operators, $elemMatch, $exists,
# projection + sort + limit. No server needed: mongomock runs inside Python.

# %% Load the sessions into a collection (done for you)
import json

import mongomock

with open(DATA / "web_sessions.json", encoding="utf-8") as f:
    sessions = json.load(f)["sessions"]

coll = mongomock.MongoClient()["pinecrest"]["sessions"]
coll.insert_many(sessions)
total = coll.count_documents({})
print("sessions in the collection:", total)

# %% Step 1: who saw the sale page?
# "pages.path" means: the path of ANY page in the list.
saw_sale = {"pages.path": "/sale"}
n_sale = coll.count_documents(saw_sale)
print("1. saw /sale:", n_sale)

# %% Step 2: add conditions (several pairs in one dictionary mean AND)
n_sale_orders = coll.count_documents({**saw_sale, "converted": True})
n_sale_mobile_big = coll.count_documents({**saw_sale, "device.type": "mobile", "cart.value": {"$gte": 200}})
print("2. saw /sale and ordered:", n_sale_orders)
print("   saw /sale, on mobile, cart of $200 or more:", n_sale_mobile_big)

# %% Step 3: a minute or more ON the sale page ($elemMatch) versus the loose version
loose = {"pages.path": "/sale", "pages.seconds": {"$gte": 60}}
strict = {"pages": {"$elemMatch": {"path": "/sale", "seconds": {"$gte": 60}}}}
print("3. loose (any page took 60 s):", coll.count_documents(loose))
print("   strict (60 s on /sale itself):", coll.count_documents(strict))

# %% Step 4: missing is not null. How many /sale visitors arrived directly (no utm field)?
n_direct = coll.count_documents({**saw_sale, "utm": {"$exists": False}})
print("4. saw /sale with no utm field:", n_direct)

# %% Step 5: the three biggest carts among /sale visitors (projection, sort, limit)
cursor = (coll.find(saw_sale, {"_id": 0, "session_id": 1, "device.type": 1, "cart.value": 1})
          .sort("cart.value", -1)
          .limit(3))
print("5. three biggest carts:")
for doc in cursor:
    print("  ", doc)

# %% Step 6: the answer in one sentence
all_orders = coll.count_documents({"converted": True})
print(f"6. order rate: {100 * n_sale_orders / n_sale:.1f}% of /sale visitors "
      f"vs {100 * all_orders / total:.1f}% of all sessions")
print("   Careful: people who browse more pages are more likely to do both. This is a")
print("   difference between groups, not proof that the sale page causes orders.")
