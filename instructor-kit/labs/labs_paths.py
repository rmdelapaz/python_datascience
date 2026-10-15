"""labs_paths: where the course data lives and where a lab may write files.

Every lab starts with the same bootstrap (see labs/README.md), which puts this folder on
sys.path, then:

    from labs_paths import DATA                 # pathlib.Path to the folder holding orders.csv
    from labs_paths import DATA, OUTPUT, OFFLINE

    orders = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
    fig.savefig(OUTPUT / "monthly_revenue.png")

DATA      The course data folder. Found, in this order:
            1. the environment variable PINECREST_DATA, if it is set;
            2. a `data/orders.csv` in the lab's own folder or any folder above it
               (also tried: the current folder and this file's folder, and the folders above them);
            3. otherwise a FileNotFoundError that says what to do.
OUTPUT    A folder the lab may write to. Normally `output/` next to the lab file (created the
          first time it is used). When LABS_OFFLINE=1 it is a temporary folder that is deleted
          when the program ends, so the lab checker never leaves files behind.
OFFLINE   True when the environment variable LABS_OFFLINE is 1 (also true/yes/on). Network labs
          then read saved pages from the session's `_fixtures/` folder instead of the internet,
          and no lab may open a browser window.
fixtures(start=None)
          The nearest `_fixtures/` folder at or above `start` (a file or folder; default: the lab
          file). Call it as fixtures(__file__) from a pytest file.

DATA and OUTPUT are worked out on first use, so `from labs_paths import OFFLINE` alone never
needs the data folder and never creates a folder.
"""
from __future__ import annotations

import atexit
import os
import shutil
import sys
import tempfile
from pathlib import Path

__all__ = ["DATA", "OUTPUT", "OFFLINE", "fixtures"]

LABS_DIR = Path(__file__).resolve().parent
MARKER = Path("data") / "orders.csv"

OFFLINE = os.environ.get("LABS_OFFLINE", "").strip().lower() in ("1", "true", "yes", "on")

_cache: dict[str, Path] = {}


def _lab_dir() -> Path:
    """Folder of the program being run (the lab file); the current folder in a notebook or under pytest."""
    main = sys.modules.get("__main__")
    f = getattr(main, "__file__", None)
    if f and Path(f).suffix == ".py" and Path(f).name not in ("__main__.py",):
        p = Path(f).resolve().parent
        # `python -m pytest` and friends: __main__ is a tool inside site-packages, not a lab
        if "site-packages" not in p.parts and "dist-packages" not in p.parts:
            return p
    return Path.cwd().resolve()


def _walk_up(start: Path):
    start = start.resolve()
    yield start
    yield from start.parents


def _find_data() -> Path:
    env = os.environ.get("PINECREST_DATA", "").strip()
    if env:
        p = Path(env).expanduser().resolve()
        if (p / "orders.csv").is_file():
            return p
        raise FileNotFoundError(
            f"\n\nPINECREST_DATA is set to {env!r}, but there is no orders.csv in that folder.\n"
            "Point it at the folder that holds orders.csv, products.csv and pinecrest.db,\n"
            "or remove the variable so the labs can look for a data/ folder themselves.\n")
    tried = []
    for start in (_lab_dir(), Path.cwd(), LABS_DIR):
        for folder in _walk_up(start):
            if folder in tried:
                continue
            tried.append(folder)
            if (folder / MARKER).is_file():
                return (folder / "data").resolve()
    raise FileNotFoundError(
        "\n\nThe Pinecrest course data was not found.\n"
        "Fix it in one of two ways:\n"
        f"  1. Unzip pinecrest-data.zip next to the labs folder, so that this file exists:\n"
        f"       {LABS_DIR.parent / MARKER}\n"
        "  2. Or set the environment variable PINECREST_DATA to the folder that holds orders.csv:\n"
        "       macOS / Linux:  export PINECREST_DATA=/path/to/data\n"
        "       PowerShell:     $env:PINECREST_DATA = \"C:\\path\\to\\data\"\n"
        f"Looked for data/orders.csv in {_lab_dir()} and every folder above it.\n")


def _make_output() -> Path:
    if OFFLINE:
        p = Path(tempfile.mkdtemp(prefix="pinecrest-labs-"))
        atexit.register(shutil.rmtree, p, ignore_errors=True)
        return p
    p = _lab_dir() / "output"
    p.mkdir(exist_ok=True)
    return p


def fixtures(start: str | os.PathLike | None = None) -> Path:
    """Nearest `_fixtures/` folder at or above `start` (default: the lab file's folder)."""
    base = Path(start).resolve() if start else _lab_dir()
    if base.is_file():
        base = base.parent
    for folder in _walk_up(base):
        if (folder / "_fixtures").is_dir():
            return folder / "_fixtures"
    raise FileNotFoundError(
        f"\n\nNo _fixtures folder was found at or above {base}.\n"
        "Offline labs keep their saved pages in labs/module-NN/_fixtures/.\n")


def __getattr__(name: str):
    # DATA and OUTPUT are computed on first use (PEP 562), then remembered.
    if name == "DATA":
        if "DATA" not in _cache:
            _cache["DATA"] = _find_data()
        return _cache["DATA"]
    if name == "OUTPUT":
        if "OUTPUT" not in _cache:
            _cache["OUTPUT"] = _make_output()
        return _cache["OUTPUT"]
    raise AttributeError(f"module 'labs_paths' has no attribute {name!r}")


if __name__ == "__main__":
    print("labs folder :", LABS_DIR)
    print("OFFLINE     :", OFFLINE)
    try:
        print("DATA        :", __getattr__("DATA"))
    except FileNotFoundError as e:
        print("DATA        : NOT FOUND", e)
        sys.exit(1)
