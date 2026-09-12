#!/usr/bin/env python3
"""Diff a lambdapdk dataroot between its pinned revision and a candidate one.

Downloads both upstream archives, then reports three things:

  BROKEN   paths lambdapdk references that no longer exist in the new tree
           (with a basename-matched suggestion where one exists)
  REMOVED  files that disappeared upstream but that lambdapdk never referenced
  ADDED    files that are new upstream -- the candidates for new enablement

Usage:
    tree_diff.py <pdk> --new-rev <rev> [--dataroot <name>] [--added-filter EXT,EXT]

Example:
    tree_diff.py ihp130 --new-rev 5e6d592e4002946a4616f798c357f0f3c06cf3b6
"""

import argparse
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import zipfile
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import _bootstrap  # noqa: F401  - must precede lambdapdk
import lambdapdk


# Extensions worth surfacing in the ADDED report by default. Upstream PDKs carry
# a lot of documentation and scratch content that is never wired into a flow.
INTERESTING = {
    ".lef", ".lib", ".gds", ".gds2", ".cdl", ".sp", ".spice", ".v", ".vhd",
    ".lyt", ".lyp", ".map", ".layermap", ".drc", ".lvs", ".lydrc", ".rules",
    ".tlef", ".tf", ".itf", ".nxtgrd", ".captable", ".json", ".tcl", ".pm3",
    ".db", ".cir", ".mod", ".l", ".scs",
}


def cache_dir() -> Path:
    base = os.environ.get("LAMBDAPDK_REVCACHE")
    if base:
        path = Path(base)
    else:
        path = Path(tempfile.gettempdir()) / "lambdapdk-revdiff"
    path.mkdir(parents=True, exist_ok=True)
    return path


def fetch(url: str, dest: Path) -> bool:
    """Download and extract an archive into dest. Returns False if it 404s."""
    if dest.exists() and any(dest.iterdir()):
        return True

    dest.mkdir(parents=True, exist_ok=True)
    suffix = ".zip" if url.endswith(".zip") else ".tar"
    archive = dest.with_suffix(suffix)

    proc = subprocess.run(["curl", "-fsSL", "-o", str(archive), url],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        shutil.rmtree(dest, ignore_errors=True)
        print(f"  ! download failed: {url}", file=sys.stderr)
        return False

    try:
        if suffix == ".zip":
            with zipfile.ZipFile(archive) as zf:
                zf.extractall(dest)
        else:
            with tarfile.open(archive) as tf:
                tf.extractall(dest, filter="data")
    finally:
        archive.unlink(missing_ok=True)

    # GitHub archives wrap everything in a single <repo>-<rev> directory; the
    # paths lambdapdk stores are relative to inside that wrapper.
    entries = list(dest.iterdir())
    if len(entries) == 1 and entries[0].is_dir():
        inner = entries[0]
        for item in inner.iterdir():
            shutil.move(str(item), str(dest / item.name))
        inner.rmdir()

    return True


def list_files(root: Path) -> Set[str]:
    out = set()
    for path in root.rglob("*"):
        if path.is_file():
            out.add(str(path.relative_to(root)))
    return out


def collect(pdk_name: str) -> Tuple[Dict[str, Tuple[str, Optional[str]]], Dict[str, Set[str]]]:
    """Return remote dataroots and, per dataroot, the paths lambdapdk references."""
    prefix = f"lambdapdk.{pdk_name}"
    roots: Dict[str, Tuple[str, Optional[str]]] = {}
    refs: Dict[str, Set[str]] = defaultdict(set)

    for obj in (*lambdapdk.get_pdks(), *lambdapdk.get_libs()):
        if not type(obj).__module__.startswith(prefix):
            continue

        for name in obj.getkeys("dataroot"):
            path = obj.get("dataroot", name, "path")
            if str(path).startswith("http") and name != "lambdapdk":
                roots[name] = (path, obj.get("dataroot", name, "tag"))

        for key in obj.allkeys():
            if key[0] != "fileset":
                continue
            param = obj.get(*key, field=None)
            if "file" not in str(param.get(field="type")):
                continue
            values = obj.get(*key)
            if not values:
                continue
            if not isinstance(values, list):
                values = [values]
            datarootv = param.get(field="dataroot") or []
            if not isinstance(datarootv, list):
                datarootv = [datarootv]
            for idx, value in enumerate(values):
                dr = datarootv[idx] if idx < len(datarootv) else None
                if dr and dr != "lambdapdk":
                    refs[dr].add(str(value))

    return roots, refs


def suggest(missing: str, new_files: Set[str]) -> Optional[str]:
    """Best-effort replacement for a path that moved or was renamed."""
    base = os.path.basename(missing)
    exact = [f for f in new_files if os.path.basename(f) == base]
    if len(exact) == 1:
        return exact[0]
    if exact:
        return f"{len(exact)} candidates: " + ", ".join(sorted(exact)[:3])

    stem, ext = os.path.splitext(base)

    # Same directory and stem, different extension -- catches the common
    # sg13g2_io/spice/sg13g2_io.spi -> sg13g2_io/spice/sg13g2_io.spice rename.
    directory = os.path.dirname(missing)
    restem = [f for f in new_files
              if os.path.splitext(os.path.basename(f))[0] == stem
              and os.path.dirname(f) == directory]
    if not restem:
        restem = [f for f in new_files if os.path.splitext(os.path.basename(f))[0] == stem]
    if restem:
        return "renamed extension? " + ", ".join(sorted(restem)[:3])

    # Same extension somewhere else, similar stem -- catches corner renames like
    # sg13g2_stdcell_typ_1p20V_25C.lib -> sg13g2_stdcell_typ_1p20V_25C_ccs.lib
    near = [f for f in new_files
            if f.endswith(ext) and (stem in os.path.basename(f)
                                    or os.path.basename(f).split("_")[0] == stem.split("_")[0])]
    if near:
        return f"{len(near)} near matches: " + ", ".join(sorted(near)[:3])
    return None


def summarize_added(added: Set[str], exts: Optional[Set[str]], limit: int) -> None:
    """Group new files by directory so a large upstream diff stays readable."""
    if exts is None:
        filtered = set(added)
    else:
        filtered = {f for f in added if Path(f).suffix.lower() in exts}
    if not filtered:
        print("    (no new files with flow-relevant extensions)")
        return

    by_dir: Dict[str, List[str]] = defaultdict(list)
    for f in sorted(filtered):
        by_dir[os.path.dirname(f)].append(os.path.basename(f))

    for directory in sorted(by_dir):
        names = by_dir[directory]
        shown = names[:limit]
        more = f"  (+{len(names) - limit} more)" if len(names) > limit else ""
        print(f"    {directory or '.'}/")
        for name in shown:
            print(f"      {name}")
        if more:
            print(f"     {more.strip()}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pdk", help="PDK package name, e.g. ihp130")
    parser.add_argument("--new-rev", required=True, help="candidate upstream revision")
    parser.add_argument("--dataroot", help="limit to one dataroot name")
    parser.add_argument("--added-filter",
                        help="comma separated extensions to show under ADDED "
                             "(default: flow-relevant set, 'all' for everything)")
    parser.add_argument("--limit", type=int, default=12,
                        help="max files listed per directory under ADDED")
    args = parser.parse_args()

    if args.added_filter == "all":
        exts = None  # no filtering
    elif args.added_filter:
        exts = {e if e.startswith(".") else f".{e}" for e in args.added_filter.split(",")}
    else:
        exts = INTERESTING

    roots, refs = collect(args.pdk)
    if not roots:
        print(f"{args.pdk}: no remote dataroot to diff")
        return 0

    cache = cache_dir()
    rc = 0

    for name, (url, old_rev) in sorted(roots.items()):
        if args.dataroot and name != args.dataroot:
            continue
        if not old_rev:
            print(f"=== {name}: no pinned tag, skipping ===")
            continue

        new_url = url.replace(old_rev, args.new_rev)
        if new_url == url:
            # URL embeds the rev only via the tag field (lambdapdk-style refs/tags/ suffix)
            new_url = url + args.new_rev

        print(f"\n=== dataroot {name}: {old_rev} -> {args.new_rev} ===")

        old_dir = cache / f"{name}-{old_rev}"
        new_dir = cache / f"{name}-{args.new_rev}"

        if not fetch(url, old_dir):
            print("  ! could not fetch the currently pinned archive")
            rc = 1
            continue
        if not fetch(new_url, new_dir):
            print(f"  ! could not fetch {new_url}")
            print("  release assets are often renamed between tags -- check the asset list "
                  "with rev_candidates.py and update the URL by hand")
            rc = 1
            continue

        old_files = list_files(old_dir)
        new_files = list_files(new_dir)
        referenced = refs.get(name, set())

        broken = sorted(p for p in referenced if p not in new_files)
        if broken:
            rc = 1
            print(f"  BROKEN ({len(broken)}) -- referenced by lambdapdk, gone in {args.new_rev}:")
            for path in broken:
                hint = suggest(path, new_files)
                print(f"    {path}")
                if hint:
                    print(f"      -> {hint}")
        else:
            print(f"  BROKEN: none ({len(referenced)} referenced paths all still present)")

        removed = sorted((old_files - new_files) - referenced)
        print(f"\n  REMOVED ({len(removed)}) -- gone upstream, not referenced here")
        for path in removed[:20]:
            print(f"    {path}")
        if len(removed) > 20:
            print(f"    (+{len(removed) - 20} more)")

        added = new_files - old_files
        print(f"\n  ADDED ({len(added)}) -- new upstream:")
        summarize_added(added, exts, args.limit)

    print(f"\nExtracted trees kept under {cache}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
