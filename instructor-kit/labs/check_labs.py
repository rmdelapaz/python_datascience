#!/usr/bin/env python3
"""Run every lab program in the kit and report PASS/FAIL.

For each labs/module-NN/ folder (NN = 01 ... 21, one folder per session) this runs

  * every  *_starter.py   (must run cleanly as handed out, TODOs and all),
  * every  *_solution.py  (must run cleanly and print its answers),
  * every  test_*.py      with pytest (a test_*_starter.py only has to be collected, because
                          its tests may be TODO stubs that fail until the learner writes code),

each one in a fresh temporary COPY of its session folder, started from the lab's own lesson
folder inside that copy (so `../_fixtures/` still resolves and nothing a lab writes can touch
the kit), with this environment:

    LABS_OFFLINE=1               network labs read labs/module-NN/_fixtures/, nothing opens a browser
    PINECREST_DATA=<course>/data the real course data (read-only by agreement: never write into it)
    MPLBACKEND=Agg               Matplotlib draws to memory, no windows
    PYTHONPATH=<kit>/labs        so `from labs_paths import DATA` works inside the copy
    PYTHONDONTWRITEBYTECODE=1    no __pycache__ folders
    TMPDIR=<the temp copy>/tmp   scratch files die with the copy
    PINECREST_API_KEY, PINECREST_USER, PINECREST_PASSWORD
                                 the public demo values from lesson 6.4, unless already set

A file FAILS if it exits non-zero, prints a Traceback on stderr, or runs past the timeout
(default 120 s each). Starter and solution files must come in pairs. Files named debug_*.py
(deliberately broken handouts) and anything under _fixtures/ are ignored.

After the runs the checker compares a listing of the checked session folders, labs/ itself and
the data folder with the listing it took before: any new, changed or missing file is a failure
(a lab wrote outside its temp copy).

Python used for the labs: --python, else $LABS_PYTHON, else ~/.cache/ds-course-venv/bin/python
when it exists, else the interpreter running this script.

Usage (from anywhere):
    python3 labs/check_labs.py                 # all sessions
    python3 labs/check_labs.py module-07       # one session (also: 07 or 7; several allowed)
    python3 labs/check_labs.py module-07 -v    # also show each program's output tail
    python3 labs/check_labs.py --timeout 300 module-17
    python3 labs/check_labs.py --strict        # all sessions; a session with no labs is a failure
Exit code: 0 when everything passed, 1 otherwise.
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

LABS = Path(__file__).resolve().parent
KIT = LABS.parent
COURSE = KIT.parent
DEFAULT_PYTHON = Path.home() / ".cache" / "ds-course-venv" / "bin" / "python"
DEFAULT_TIMEOUT = 120
IGNORE_DIRS = {"_fixtures", "__pycache__", "output", ".pytest_cache", ".ipynb_checkpoints"}
TRACEBACK = "Traceback (most recent call last)"
# The mock API's public teaching values (lesson 6.4), so labs that call require_env() run in the checker.
DEMO_ENV = {"PINECREST_API_KEY": "pinecrest-demo-key", "PINECREST_USER": "analyst", "PINECREST_PASSWORD": "trailmix"}


def pick_python(arg: str | None) -> str:
    for cand, label in ((arg, "--python"), (os.environ.get("LABS_PYTHON"), "LABS_PYTHON")):
        if cand:
            p = Path(cand).expanduser()
            if not p.exists() and not shutil.which(cand):
                raise SystemExit(f"{label}={cand!r} does not exist")
            return str(p) if p.exists() else cand
    if DEFAULT_PYTHON.exists():
        return str(DEFAULT_PYTHON)
    return sys.executable


def find_data() -> Path | None:
    env = os.environ.get("PINECREST_DATA")
    for cand in ([Path(env).expanduser()] if env else []) + [COURSE / "data", KIT / "data"]:
        if (cand / "orders.csv").is_file():
            return cand.resolve()
    return None


def module_dir(spec: str) -> Path:
    m = re.fullmatch(r"(?:module-)?(\d{1,2})/?", spec.strip())
    if not m:
        raise SystemExit(f"Not a session: {spec!r} (use module-07, 07 or 7)")
    d = LABS / f"module-{int(m.group(1)):02d}"
    if not d.is_dir():
        raise SystemExit(f"No such folder: {d}")
    return d


def lab_files(mod: Path) -> list[Path]:
    """Starters, solutions and pytest files of one session, in a stable order."""
    out = []
    for py in sorted(mod.rglob("*.py")):
        rel = py.relative_to(mod)
        if IGNORE_DIRS & set(rel.parts[:-1]) or py.name.startswith("debug_"):
            continue
        if py.name.startswith("test_") or py.stem.endswith(("_starter", "_solution")):
            out.append(py)
    return out


def unpaired(files: list[Path]) -> list[tuple[Path, str]]:
    have = {f for f in files if not f.name.startswith("test_")}
    bad = []
    for f in sorted(have):
        for a, b in (("_starter", "_solution"), ("_solution", "_starter")):
            if f.stem.endswith(a):
                twin = f.with_name(f.stem[: -len(a)] + b + ".py")
                if twin not in have:
                    bad.append((f, twin.name))
    return bad


def snapshot(roots: list[Path]) -> dict[str, tuple[int, int]]:
    snap = {}
    for root in roots:
        if root.is_file():
            st = root.stat()
            snap[str(root)] = (st.st_size, st.st_mtime_ns)
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            for name in dirnames + filenames:
                p = Path(dirpath) / name
                try:
                    st = p.lstat()
                except OSError:
                    continue
                snap[str(p)] = (-1, 0) if p.is_dir() else (st.st_size, st.st_mtime_ns)
    return snap


def run_one(py: Path, mod: Path, python: str, timeout: int, data: Path | None) -> tuple[bool, str]:
    with tempfile.TemporaryDirectory(prefix="check-labs-") as tmp:
        tmp = Path(tmp)
        work_mod = tmp / mod.name
        shutil.copytree(mod, work_mod, ignore=shutil.ignore_patterns(
            "__pycache__", "output", ".pytest_cache", ".ipynb_checkpoints"))
        cwd = work_mod / py.relative_to(mod).parent
        (tmp / "tmp").mkdir()
        env = {**os.environ,
               "LABS_OFFLINE": "1", "MPLBACKEND": "Agg", "PYTHONDONTWRITEBYTECODE": "1",
               "PYTHONIOENCODING": "utf-8", "PYTHONUNBUFFERED": "1",
               "TMPDIR": str(tmp / "tmp"), "TEMP": str(tmp / "tmp"), "TMP": str(tmp / "tmp"),
               "BROWSER": "echo",   # a stray webbrowser.open() prints a URL instead of opening a window
               "PYTHONPATH": os.pathsep.join(filter(None, [str(LABS), os.environ.get("PYTHONPATH", "")]))}
        for k, v in DEMO_ENV.items():
            env.setdefault(k, v)
        if data:
            env["PINECREST_DATA"] = str(data)
        if py.name.startswith("test_"):
            cmd = [python, "-m", "pytest", "-q", "-p", "no:cacheprovider"]
            if py.stem.endswith("_starter"):
                cmd.append("--collect-only")
            cmd.append(py.name)
        else:
            cmd = [python, py.name]
        posix = os.name == "posix"
        proc = subprocess.Popen(cmd, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                start_new_session=posix)
        timed_out = False
        try:
            out, err = proc.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            _kill(proc, posix)
            out, err = proc.communicate()
        finally:
            _kill(proc, posix)     # also reaps helpers a lab left running (servers, browsers)
        out = out.decode("utf-8", "replace").strip()
        err = err.decode("utf-8", "replace").strip()
        both = (out + ("\n--- stderr ---\n" + err if err else "")).strip()
        if timed_out:
            return False, f"timeout after {timeout}s (waiting for input, a server, a browser, or looping?)\n" + both[-800:]
        if proc.returncode != 0:
            return False, f"exit code {proc.returncode}\n" + both[-1500:]
        if TRACEBACK in err:
            return False, "Traceback on stderr (exit code 0)\n" + err[-1500:]
        return True, both[-400:]


def _kill(proc: subprocess.Popen, posix: bool) -> None:
    try:
        if posix:
            os.killpg(proc.pid, signal.SIGKILL)
        elif proc.poll() is None:
            proc.kill()
    except (ProcessLookupError, PermissionError, OSError):
        pass


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Run every lab starter, solution and test file; report PASS/FAIL.",
                                 epilog="See the top of this file or labs/README.md for the rules.")
    ap.add_argument("modules", nargs="*", help="module-07, 07 or 7 (default: all sessions)")
    ap.add_argument("--module", action="append", default=[], help="same as a positional session (repeatable)")
    ap.add_argument("--python", help="interpreter that runs the labs (default: $LABS_PYTHON, the course venv, or this one)")
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help=f"seconds per file (default {DEFAULT_TIMEOUT})")
    ap.add_argument("--strict", action="store_true", help="a session folder with no lab files is a failure even when running all")
    ap.add_argument("-v", "--verbose", action="store_true", help="show the tail of every program's output")
    a = ap.parse_args(argv)

    wanted = a.modules + a.module
    explicit = bool(wanted)
    mods = [module_dir(s) for s in wanted] if explicit else sorted(LABS.glob("module-[0-9][0-9]"))
    python = pick_python(a.python)
    data = find_data()
    print(f"python: {python}")
    print(f"data:   {data if data else 'NOT FOUND (labs that read DATA will fail; set PINECREST_DATA)'}")
    print(f"timeout {a.timeout}s per file · LABS_OFFLINE=1 · MPLBACKEND=Agg\n")

    watch = mods + [p for p in LABS.iterdir() if p.is_file()] + [LABS / "__pycache__"] + ([data] if data else [])
    before = snapshot([w for w in watch if w.exists()])

    ok = bad = 0
    empty = []
    for mod in mods:
        files = lab_files(mod)
        if not files:
            empty.append(mod.name)
            if explicit or a.strict:
                print(f"FAIL  {mod.name}/  no *_starter.py / *_solution.py / test_*.py files found")
                bad += 1
            continue
        for f, twin in unpaired(files):
            print(f"FAIL  {f.relative_to(LABS)}  has no partner {twin} (starters and solutions come in pairs; "
                  "name a handout that is neither debug_*.py)")
            bad += 1
        for py in files:
            passed, out = run_one(py, mod, python, a.timeout, data)
            print(f"{'PASS' if passed else 'FAIL'}  {py.relative_to(LABS)}")
            if not passed or a.verbose:
                print("      " + out.replace("\n", "\n      "))
            ok += passed
            bad += not passed

    after = snapshot([w for w in watch if w.exists()])
    changes = ([f"new      {p}" for p in sorted(set(after) - set(before))]
               + [f"missing  {p}" for p in sorted(set(before) - set(after))]
               + [f"changed  {p}" for p in sorted(set(before) & set(after)) if before[p] != after[p]])
    if changes:
        print("\nFAIL  files in the kit or the data folder changed while the labs ran. A lab wrote outside its "
              "temp copy (write to OUTPUT from labs_paths, never into DATA), or someone edited these files meanwhile:")
        for c in changes[:40]:
            print("      " + c)
        bad += 1

    if empty and not (explicit or a.strict):
        print(f"\nNo labs yet in {len(empty)} session folder(s): {', '.join(empty)}")
    print(f"\n{ok} passed, {bad} failed")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
