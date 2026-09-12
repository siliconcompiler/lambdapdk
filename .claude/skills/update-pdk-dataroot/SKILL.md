---
name: update-pdk-dataroot
description: Update a lambdapdk PDK or library that pulls its collateral from an upstream dataroot (gt2n, ihp130, icsprout55) to a newer upstream revision, then verify it locally and against the scgallery design matrix. Use when asked to bump, update, or refresh a PDK's pinned rev, check whether a PDK is behind upstream, or find new upstream collateral worth enabling.
---

# Updating a dataroot-backed PDK

PDKs like `gt2n`, `ihp130` and `icsprout55` do not vendor their collateral. They pin an
upstream revision and let SiliconCompiler fetch it:

```python
pdk_rev = 'd490cfb2e3258f71f362167e74e1fcfc55381ab4'

class _IHP130Path(_LambdaPath):
    def __init__(self):
        super().__init__()
        self.set_dataroot("ihp130",
                          f"https://github.com/IHP-GmbH/IHP-Open-PDK/archive/{pdk_rev}.tar.gz",
                          pdk_rev)
```

Updating one is not just editing that string. Upstream moves files, renames corners and
adds collateral, and every path in `lambdapdk/<pdk>/` and `lambdapdk/<pdk>/libs/` is a
path into *their* tree. Work through the phases below in order.

Run every script with a Python that has SiliconCompiler installed. The scripts put the
repository root on `sys.path` themselves, so the working directory does not matter.

```bash
PY=python3    # or whichever venv has siliconcompiler, e.g. .venv/bin/python
S=.claude/skills/update-pdk-dataroot/scripts
```

Check the environment first — `$PY -c "import siliconcompiler, lambdapdk"` must succeed,
and `import lambdapdk` must land on this working tree, not site-packages.

## Phase 1 — pick the revision

```bash
$PY $S/rev_candidates.py <pdk>      # or --all to survey every PDK
```

This prints each dataroot the PDK and its libraries declare, the currently pinned rev,
and upstream's default-branch HEAD, latest release and recent tags.

Choose by what the PDK already does: **if it pins a tag or release, take the newest
tag/release; otherwise take the default-branch HEAD sha.** Do not convert a sha-pinned
PDK to tags or vice versa as a side effect of an update.

Report the candidate and what it replaces before editing anything. If upstream has not
moved, say so and stop.

## Phase 2 — diff the trees

```bash
$PY $S/tree_diff.py <pdk> --new-rev <rev>
```

This downloads both revisions and reports three things:

- **BROKEN** — paths lambdapdk references that are gone in the new tree, each with a
  suggested replacement where one is findable. Every one of these must be resolved.
- **REMOVED** — files that vanished upstream that we never referenced. Usually noise,
  but scan for decks and models that we *should* have been using.
- **ADDED** — new upstream files, grouped by directory and filtered to flow-relevant
  extensions. This is where new enablement comes from. Use `--added-filter all` to see
  everything, `--limit N` to widen each directory listing.

Read `reference.md` next to this file: it maps every PDK and library setter to the
upstream collateral that feeds it, and lists what specific kinds of new files usually
mean (a new corner, a new macro, a new DRC deck, a dual-port SRAM, a changed tech LEF).

## Phase 3 — apply the update

Edit `lambdapdk/<pdk>/__init__.py` and the files under `lambdapdk/<pdk>/libs/`.

**Apply directly:**

- The `pdk_rev` bump itself.
- `package.set_version(pdk_rev)` — but only where the PDK already ties the two together
  (ihp130, icsprout55). GT2N deliberately versions its package `"v0"` independently.
- Every BROKEN path, repointed at its new location.
- New collateral that slots into a pattern already present in the file — for example
  another timing corner beside corners that are already registered, when the new one
  follows the same naming and belongs to a library that already exists.

**Stop and ask before doing:** anything structural. A new library class, a new SRAM or
IO macro, a new DRC or LVS deck, a new stackup variant, a new lambdalib mapping, or
dropping a lambdapdk-owned file because upstream now ships its own. Present what you
found and what you would add, and let the user decide.

If the user says yes to adding a library, macro or stackup variant, that is the
`add-pdk-or-library` skill's job — switch to it rather than improvising the class
layout, registration and demo target here.

Watch for changes that reach beyond this repository:

- New or renamed library classes must be added to `get_pdks()` / `get_libs()` in
  `lambdapdk/__init__.py`, or nothing tests them.
- SiliconCompiler's `siliconcompiler/targets/<pdk>_demo.py` imports library classes by
  name. A rename or addition needs a matching change there, and CI in this repo will
  not catch it. Flag it explicitly.
- A changed technology LEF invalidates the PEX numbers. `add_openroad_rclayer` and
  `add_openroad_rccorrection` values come from `scripts/pex_calibrate_all.py`; say so
  rather than hand-adjusting them.
- `README.md` carries a "Supported PDKs" table and a per-PDK inventory section.

## Phase 4 — verify locally

Run all four. Paths and lint are the CI gate; the build is what catches a changed tech
LEF, a renamed site or a broken Liberty, which path checks cannot see. Phase 5 then
checks the update against real designs.

```bash
# 1. every file the PDK and its libraries reference actually resolves
$PY $S/check_paths.py <pdk>

# 2. the full suite, as CI runs it
$PY -m pytest tests/

# 3. lint
$PY -m flake8 --statistics .
tclfmt --check . && tclint .          # only if TCL changed

# 4. a real design through the flow
$PY $S/smoke_build.py <pdk>           # --keep to retain the build directory
```

`check_paths.py` exists because `tests/test_paths.py` parametrizes over every PDK at
once with opaque ids (`pdk0`, `lib17`), so pytest cannot be pointed at just one PDK. It
names the exact keypath and path of anything missing.

### Reading a smoke build result

`smoke_build.py` refuses to run if the `lambdapdk` dataroot resolves to a published
GitHub release instead of the working tree — in that state SiliconCompiler would test
the last release and silently ignore local edits. The scripts' bootstrap normally
prevents this; if the guard still fires, `pip install -e .` in the environment.

Exit codes distinguish the outcomes:

| Code | Meaning |
|---|---|
| 0 | the design built — the update is good |
| 1 | a node failed for a reason that is not obviously environmental: treat as a real regression and read the node log |
| 3 | every failed node failed on a broken tool install (a snap-packaged klayout dies on a glibc symbol error in `write.gds`), so the PDK collateral itself loaded and routed |

Exit 3 is reported as INCOMPLETE, not PASSED. It is only claimed when *every* failed
node has an environmental cause; one unexplained failure downgrades the whole run to
exit 1. Say which of the three you got rather than reporting a bare pass or fail.

## Phase 5 — gallery regression run

Phase 4 proves one small design builds. It does not prove the update leaves real designs
where they were. scgallery runs a matrix of ~25 designs per target and fails a job when a
design breaks or misses its rules, so a pair that was green on `main` and is red on your
branch is a regression this update caused.

Push the update branch first — scgallery checks out `siliconcompiler/lambdapdk` at the
ref you name, so **the branch must exist on the canonical repo; a fork or a local branch
will not resolve.**

Dispatching runs CI on a shared repository and can occupy ~150 runners. **Ask the user
before dispatching**, and say which `run` scope you intend:

```bash
gh workflow run "Run Gallery Designs" -R siliconcompiler/scgallery \
    -f lambdapdk-ref=<your-branch> \
    -f run=default              # default | all | tiny
```

| `run` | Matrix |
|---|---|
| `tiny` | heartbeat only — a fast confidence check, not a regression run |
| `default` | the committed matrix, ~141 design jobs across all targets |
| `all` | the full generated matrix |

Other inputs: `sc-ref` pins a SiliconCompiler branch — use it when the update also needs
a change to `siliconcompiler/targets/<pdk>_demo.py`, since otherwise the gallery runs
your PDK against a target that has not been updated. `concurrency` (default 50) and
`timeout` (default 120 min) rarely need changing.

The dispatch has no per-PDK filter, so a single-PDK update still runs every target. To
exercise only the PDK you touched, run the gallery locally instead — it needs the full
tool stack, but it is the whole matrix for one target:

```bash
sc-gallery -target ihp130_sg13g2_stdcell     # gt2n_6t_w31, icsprout55_ics55, ...
```

Then compare against a baseline rather than reading job results by hand:

```bash
$PY $S/gallery_compare.py --list                          # find run ids
$PY $S/gallery_compare.py --run <id> --baseline latest-success
```

It maps each `Run design (design, target, …)` job to a (design, target) pair and splits
the difference into REGRESSED, already-failing, fixed, and matrix-only changes. It exits
1 if anything regressed.

Two things to be honest about when reading it:

- `latest-success` is a guess — the newest successful run older than yours. Confirm it
  actually ran against unmodified lambdapdk before calling a clean result clean.
- Designs already failing on the baseline are listed separately and are **not** yours.
  Do not report them as caused by the update, and do not quietly count them as passes.

The gallery is the slowest check and needs a pushed branch, so it is the last phase, not
a gate on the earlier ones. If the user declines the run, say the update is unverified
against the gallery rather than implying full verification.

## Reporting

Close with: the rev moved from and to, the broken paths fixed, what was enabled, what
was found but left for the user to decide, anything needing a matching SiliconCompiler
change, and the result of each verification step — the four local ones and the gallery
run. State plainly if a step failed, was skipped, or was declined.
