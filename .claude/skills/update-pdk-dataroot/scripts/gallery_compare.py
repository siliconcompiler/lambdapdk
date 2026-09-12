#!/usr/bin/env python3
"""Diff two scgallery "Run Gallery Designs" runs to find regressions.

A gallery run fans out to one job per (design, target) pair. Comparing the
per-job conclusions of a run on your update branch against a baseline run tells
you exactly which pairs broke, rather than leaving you to read 150 job results.

Usage:
    gallery_compare.py --run <run-id> --baseline <run-id>
    gallery_compare.py --run <run-id> --baseline latest-success
    gallery_compare.py --list                       # recent runs, to pick ids

Exits 1 if any (design, target) pair regressed.

The baseline must be a run of the same workflow against unmodified lambdapdk.
`latest-success` picks the newest successful completed run older than --run,
which is usually right but is a guess -- confirm it is a main-ref run before
trusting a clean result.
"""

import argparse
import json
import re
import subprocess
import sys
from typing import Dict, Optional, Tuple

REPO = "siliconcompiler/scgallery"
WORKFLOW = "Run Gallery Designs"

# "designs / Run design (aes, ihp130_sg13g2_stdcell, false)"
JOB_RE = re.compile(r"Run design \((?P<design>[^,]+),\s*(?P<target>[^,)]+)")


def gh(*args: str) -> str:
    proc = subprocess.run(["gh", *args], capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stderr.strip(), file=sys.stderr)
        raise SystemExit(f"gh {' '.join(args)} failed")
    return proc.stdout


def list_runs(limit: int = 15):
    raw = gh("run", "list", "-R", REPO, "-w", WORKFLOW, "-L", str(limit),
             "--json", "databaseId,status,conclusion,createdAt,headBranch,url")
    return json.loads(raw)


def run_jobs(run_id: str) -> Dict[Tuple[str, str], str]:
    """Map (design, target) -> conclusion for one run's design jobs."""
    raw = gh("run", "view", str(run_id), "-R", REPO, "--json", "jobs")
    jobs = json.loads(raw).get("jobs", [])

    out: Dict[Tuple[str, str], str] = {}
    for job in jobs:
        match = JOB_RE.search(job.get("name", ""))
        if not match:
            continue  # setup/packaging jobs, not a design
        key = (match.group("design").strip(), match.group("target").strip())
        out[key] = job.get("conclusion") or job.get("status") or "unknown"
    return out


def resolve_baseline(run_id: str) -> Optional[str]:
    """Newest successful completed run older than run_id."""
    runs = list_runs(30)
    target = next((r for r in runs if str(r["databaseId"]) == str(run_id)), None)
    if not target:
        print(f"run {run_id} not in the {WORKFLOW} history", file=sys.stderr)
        return None

    for candidate in runs:
        if candidate["createdAt"] >= target["createdAt"]:
            continue
        if candidate["status"] == "completed" and candidate["conclusion"] == "success":
            return str(candidate["databaseId"])
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--run", help="run id for the update branch")
    parser.add_argument("--baseline", help="run id to compare against, or 'latest-success'")
    parser.add_argument("--list", action="store_true", help="list recent runs and exit")
    args = parser.parse_args()

    if args.list:
        for r in list_runs():
            state = r["conclusion"] or r["status"]
            print(f"{r['databaseId']}  {state:<10} {r['createdAt']}  {r['headBranch']}")
        return 0

    if not args.run or not args.baseline:
        parser.error("--run and --baseline are both required (or use --list)")

    baseline_id = args.baseline
    if baseline_id == "latest-success":
        baseline_id = resolve_baseline(args.run)
        if not baseline_id:
            print("could not find a baseline run; pass --baseline <run-id>", file=sys.stderr)
            return 2
        print(f"baseline resolved to run {baseline_id} "
              f"(confirm this ran against unmodified lambdapdk)\n")

    new = run_jobs(args.run)
    old = run_jobs(baseline_id)

    if not new:
        print(f"run {args.run} has no design jobs yet -- is it still running?", file=sys.stderr)
        return 2

    def ok(result: str) -> bool:
        return result == "success"

    regressed = sorted(k for k in new if k in old and ok(old[k]) and not ok(new[k]))
    fixed = sorted(k for k in new if k in old and not ok(old[k]) and ok(new[k]))
    still_failing = sorted(k for k in new if k in old and not ok(old[k]) and not ok(new[k]))
    added = sorted(set(new) - set(old))
    missing = sorted(set(old) - set(new))

    print(f"run {args.run}: {len(new)} design jobs")
    print(f"baseline {baseline_id}: {len(old)} design jobs\n")

    if regressed:
        print(f"REGRESSED ({len(regressed)}) -- passed on the baseline, failing now:")
        for design, target in regressed:
            print(f"  {design} / {target}   {old[(design, target)]} -> {new[(design, target)]}")
    else:
        print("REGRESSED (0)")

    if still_failing:
        print(f"\nalready failing on the baseline ({len(still_failing)}), not caused by this "
              f"update:")
        for design, target in still_failing:
            print(f"  {design} / {target}   {new[(design, target)]}")

    if fixed:
        print(f"\nfixed by this update ({len(fixed)}):")
        for design, target in fixed:
            print(f"  {design} / {target}")

    if added:
        print(f"\nonly in this run ({len(added)}):")
        for design, target in added:
            print(f"  {design} / {target}   {new[(design, target)]}")

    if missing:
        print(f"\nonly in the baseline ({len(missing)}) -- matrix changed or jobs were skipped:")
        for design, target in missing:
            print(f"  {design} / {target}   {old[(design, target)]}")

    return 1 if regressed else 0


if __name__ == "__main__":
    sys.exit(main())
