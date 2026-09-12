#!/usr/bin/env python3
"""Report the upstream revisions a lambdapdk dataroot could be bumped to.

Reads the dataroot URLs a PDK (and its libraries) declare, works out which
GitHub repository each one points at, and asks that repository for its newest
release, newest tags and default-branch HEAD.

Usage:
    rev_candidates.py <pdk>            # e.g. ihp130, gt2n, icsprout55
    rev_candidates.py --all            # every PDK with a remote dataroot

Requires the `gh` CLI to be authenticated.
"""

import argparse
import json
import re
import subprocess
import sys
from typing import Dict, List, Optional, Tuple

import _bootstrap  # noqa: F401  - must precede lambdapdk
import lambdapdk


# https://github.com/<owner>/<repo>/archive/<...>  and  .../releases/download/<tag>/<asset>
_GITHUB_RE = re.compile(r"https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)/")


def gh_api(path: str, jq: Optional[str] = None) -> Optional[str]:
    """Run `gh api`, returning None when the endpoint 404s (e.g. no releases)."""
    cmd = ["gh", "api", path]
    if jq:
        cmd += ["--jq", jq]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def collect_dataroots(pdk_name: str) -> Dict[str, Tuple[str, Optional[str]]]:
    """Map dataroot name -> (url, pinned tag) for every remote dataroot of a PDK.

    Covers the PDK object and every library in the same package, since a PDK
    such as icsprout55 splits its collateral across several dataroots (the repo
    archive plus per-flavor release assets).
    """
    prefix = f"lambdapdk.{pdk_name}"
    roots = {}
    for obj in (*lambdapdk.get_pdks(), *lambdapdk.get_libs()):
        if not type(obj).__module__.startswith(prefix):
            continue
        for name in obj.getkeys("dataroot"):
            if name == "lambdapdk":
                # lambdapdk's own dataroot tracks this repo, not the upstream PDK
                continue
            path = obj.get("dataroot", name, "path")
            if not str(path).startswith("http"):
                continue
            roots[name] = (path, obj.get("dataroot", name, "tag"))
    return roots


def describe_repo(owner: str, repo: str) -> Dict[str, object]:
    """Latest release, recent tags and default-branch HEAD for one repository."""
    info: Dict[str, object] = {"repo": f"{owner}/{repo}"}

    default_branch = gh_api(f"repos/{owner}/{repo}", ".default_branch")
    info["default_branch"] = default_branch

    if default_branch:
        head = gh_api(f"repos/{owner}/{repo}/commits/{default_branch}",
                      '.sha + " " + .commit.committer.date')
        if head:
            sha, _, date = head.partition(" ")
            info["head_sha"] = sha
            info["head_date"] = date

    release = gh_api(f"repos/{owner}/{repo}/releases/latest",
                     '.tag_name + " " + .published_at')
    if release:
        tag, _, date = release.partition(" ")
        info["latest_release"] = tag
        info["latest_release_date"] = date
        assets = gh_api(f"repos/{owner}/{repo}/releases/latest", '[.assets[].name] | join(" ")')
        info["latest_release_assets"] = assets.split() if assets else []

    tags = gh_api(f"repos/{owner}/{repo}/tags", '[.[0:10][].name] | join(" ")')
    info["tags"] = tags.split() if tags else []

    return info


def report(pdk_name: str) -> int:
    roots = collect_dataroots(pdk_name)
    if not roots:
        print(f"{pdk_name}: no remote dataroot -- collateral is vendored in this repo")
        return 0

    print(f"=== {pdk_name} ===")
    seen: Dict[str, Dict[str, object]] = {}
    for name, (url, tag) in sorted(roots.items()):
        match = _GITHUB_RE.match(url)
        if not match:
            print(f"  {name}: non-GitHub dataroot, check by hand: {url}")
            continue
        owner, repo = match.group("owner"), match.group("repo")
        key = f"{owner}/{repo}"
        if key not in seen:
            seen[key] = describe_repo(owner, repo)
        is_asset = "/releases/download/" in url
        print(f"  dataroot {name}: pinned {tag}"
              f"{'  (release asset)' if is_asset else ''}")

    for key, info in seen.items():
        print(f"\n  upstream {key}")
        print(f"    default branch : {info.get('default_branch')}")
        print(f"    HEAD           : {info.get('head_sha')}  ({info.get('head_date')})")
        if info.get("latest_release"):
            print(f"    latest release : {info['latest_release']}  "
                  f"({info.get('latest_release_date')})")
            assets = info.get("latest_release_assets") or []
            if assets:
                print(f"    release assets : {' '.join(assets)}")
        else:
            print("    latest release : none published")
        if info.get("tags"):
            print(f"    recent tags    : {' '.join(info['tags'])}")

    print("\n  Rev policy: if this PDK already pins a tag, prefer the newest tag/release;")
    print("  otherwise take the default-branch HEAD sha. Confirm before editing.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pdk", nargs="?", help="PDK package name, e.g. ihp130")
    parser.add_argument("--all", action="store_true", help="report every PDK")
    parser.add_argument("--json", action="store_true", help="emit raw dataroot data as JSON")
    args = parser.parse_args()

    if not args.pdk and not args.all:
        parser.error("give a PDK name or --all")

    if args.all:
        names: List[str] = sorted({type(p).__module__.split(".")[1] for p in lambdapdk.get_pdks()})
    else:
        names = [args.pdk]

    if args.json:
        print(json.dumps({n: collect_dataroots(n) for n in names}, indent=2, default=str))
        return 0

    rc = 0
    for name in names:
        rc |= report(name)
    return rc


if __name__ == "__main__":
    sys.exit(main())
