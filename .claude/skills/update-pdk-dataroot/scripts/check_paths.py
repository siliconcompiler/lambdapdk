#!/usr/bin/env python3
"""Run check_filepaths() for one PDK and every library in its package.

tests/test_paths.py parametrizes over every PDK and library at once and gives
the cases opaque ids (pdk0, lib17, ...), so there is no way to ask pytest for
just the one being updated. This does that, and names what is missing.

Usage:
    check_paths.py <pdk>        # e.g. ihp130
    check_paths.py --all
"""

import argparse
import sys
from typing import List

import _bootstrap  # noqa: F401  - must precede lambdapdk
import lambdapdk


def objects_for(pdk_name: str) -> List[object]:
    prefix = f"lambdapdk.{pdk_name}"
    objs = [o for o in (*lambdapdk.get_pdks(), *lambdapdk.get_libs())
            if type(o).__module__.startswith(prefix)]
    return sorted(objs, key=lambda o: (type(o).__module__, o.name))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pdk", nargs="?", help="PDK package name, e.g. ihp130")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    if not args.pdk and not args.all:
        parser.error("give a PDK name or --all")

    if args.all:
        names = sorted({type(p).__module__.split(".")[1] for p in lambdapdk.get_pdks()})
    else:
        names = [args.pdk]

    failures = 0
    total = 0
    for name in names:
        objs = objects_for(name)
        if not objs:
            print(f"{name}: no PDK or library found in lambdapdk.{name}")
            return 1
        print(f"=== {name}: {len(objs)} objects ===")
        for obj in objs:
            total += 1
            # check_filepaths() logs each missing file itself
            if not obj.check_filepaths():
                failures += 1
                print(f"  FAIL {type(obj).__name__} ({obj.name})")

    print(f"\n{total - failures}/{total} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
