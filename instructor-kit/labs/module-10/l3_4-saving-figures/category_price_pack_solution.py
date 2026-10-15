# --- lab bootstrap: find labs_paths.py (the same three lines open every lab; see labs/README.md) ---
import pathlib, sys
sys.path[:0] = [str(p) for p in pathlib.Path(globals().get("__file__", "lab.py")).resolve().parents if (p / "labs_paths.py").is_file()]
from labs_paths import DATA, OUTPUT

# %% [markdown]
# # Lab 3.4-B · A price-range chart pack (SOLUTION)
# The buying team wants a picture of the list prices in three categories (Tents, Footwear,
# Apparel): a web image for the intranet, a slide image for Monday's meeting, and one PDF
# with all three to print. One table of presets, one save function, one loop, one manifest.

# %% Load the catalog
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

products = pd.read_csv(DATA / "products.csv")
CATEGORIES = ["Tents", "Footwear", "Apparel"]
print(products[products["category"].isin(CATEGORIES)].groupby("category")["price"].agg(["count", "median"]))

# %% Step 1: the presets and the two functions that read them
PRESETS = {
    "web":   {"figsize": (8, 4),     "dpi": 120, "extension": "png"},     # 960 x 480
    "slide": {"figsize": (9.6, 5.4), "dpi": 200, "extension": "png"},     # 1920 x 1080
    "print": {"figsize": (6.5, 3.5), "dpi": 300, "extension": "pdf"},
}


def new_figure(kind):
    """A figure sized for its destination, created BEFORE drawing."""
    return plt.subplots(figsize=PRESETS[kind]["figsize"], layout="constrained")


def save_chart(fig, name, kind, folder):
    """Save fig as folder/name_kind.ext with the preset's dpi and a white background. Returns the path."""
    preset = PRESETS[kind]
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{name}_{kind}.{preset['extension']}"
    fig.savefig(path, dpi=preset["dpi"], facecolor="white")
    return path


# %% Step 2: one drawing function, used for every category and every destination
def draw_prices(ax, category):
    prices = products.loc[products["category"] == category, "price"]
    ax.hist(prices, bins=12, color="#667eea", edgecolor="white")
    ax.axvline(prices.median(), color="#15803d", linewidth=2.5)
    ax.set_title(f"{category}: {len(prices)} products, median list price ${prices.median():,.2f}",
                 loc="left", fontweight="bold")
    ax.set_xlabel("List price ($)")
    ax.set_ylabel("Products")
    ax.spines[["top", "right"]].set_visible(False)


# %% Step 3: the loop. Create, draw, save, close
pack = OUTPUT / "price_pack"
saved = []
for category in CATEGORIES:
    for kind in ("web", "slide"):
        fig, ax = new_figure(kind)
        draw_prices(ax, category)
        saved.append(save_chart(fig, category.lower(), kind, pack))
        plt.close(fig)

# %% Step 4: one PDF, one page per category
combined = pack / "price_ranges.pdf"
with PdfPages(combined) as pdf:
    for category in CATEGORIES:
        page, ax = new_figure("print")
        draw_prices(ax, category)
        pdf.savefig(page)
        plt.close(page)
    pages = pdf.get_pagecount()
saved.append(combined)
print(combined.name, "has", pages, "pages")

# %% Step 5: the manifest. Do not trust, check
rows = []
for path in saved:
    size = ""
    if path.suffix == ".png":
        height, width = plt.imread(path).shape[:2]
        size = f"{width} x {height}"
    rows.append({"file": path.name, "pixels": size, "over_5_kb": path.stat().st_size > 5 * 1024})
manifest = pd.DataFrame(rows)
print(manifest.to_string(index=False))

web_ok = (manifest.loc[manifest["file"].str.endswith("_web.png"), "pixels"] == "960 x 480").all()
slide_ok = (manifest.loc[manifest["file"].str.endswith("_slide.png"), "pixels"] == "1920 x 1080").all()
print("files:", len(saved), "| web 960 x 480:", web_ok, "| slides 1920 x 1080:", slide_ok,
      "| open figures:", len(plt.get_fignums()))
