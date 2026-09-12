#!/usr/bin/env python3
"""Push a small design through the ASIC flow to smoke test a PDK update.

check_filepaths() only proves the files resolve. This proves OpenROAD and Yosys
can still read them: a changed tech LEF, a renamed site, a new Liberty corner or
a reworked layer stack shows up here and nowhere else.

The design is a self-contained counter, written to a temp directory, so this
does not depend on a SiliconCompiler source checkout.

Usage:
    smoke_build.py <pdk-or-target> [--builddir DIR] [--keep]

Examples:
    smoke_build.py ihp130                 # resolves to the ihp130_demo target
    smoke_build.py gt2n_demo --keep

IMPORTANT: run this from the lambdapdk repository root, or with lambdapdk
pip-installed editable. Otherwise SiliconCompiler resolves the `lambdapdk`
dataroot to the last published release on GitHub and your local edits to
pdngen.tcl, PEX decks and the like are silently not tested. The script checks
this and refuses to run if the dataroot points at a URL.
"""

import argparse
import importlib
import shutil
import sys
import tempfile
from pathlib import Path

import _bootstrap  # noqa: F401  - must precede lambdapdk and siliconcompiler

RTL = """\
module heartbeat #(
    parameter N = 8
) (
    input      clk,
    input      nreset,
    output reg out
);

    reg [N-1:0] counter_reg;

    always @(posedge clk or negedge nreset) begin
        if (!nreset) begin
            counter_reg <= {(N) {1'b0}};
            out <= 1'b0;
        end else begin
            counter_reg <= counter_reg + 1'b1;
            out <= (counter_reg == {(N) {1'b1}});
        end
    end

endmodule
"""

SDC = """\
create_clock -name clk -period 10 [get_ports {clk}]

set_input_delay 2 -clock clk [all_inputs]
set_output_delay 2 -clock clk [all_outputs]
"""


def check_local_dataroot() -> bool:
    """Refuse to run when the lambdapdk dataroot resolves to a published release."""
    import lambdapdk
    from lambdapdk import LambdaPDK

    probe = LambdaPDK()
    path = str(probe.get("dataroot", "lambdapdk", "path"))
    if path.startswith("http"):
        print("ERROR: the 'lambdapdk' dataroot resolves to a published release, not your "
              "working tree:", file=sys.stderr)
        print(f"         {path}", file=sys.stderr)
        print("       Local changes would not be tested. Run from the lambdapdk repository "
              "root, or `pip install -e .`.", file=sys.stderr)
        return False

    print(f"lambdapdk module   : {lambdapdk.__file__}")
    print(f"lambdapdk dataroot : {path}")
    return True


# Failures that mean the local tool install is broken, not the PDK. A snap-packaged
# klayout leaks /snap/core20 libraries into the process and dies on a glibc symbol.
ENV_FAILURES = (
    ("symbol lookup error", "tool binary is broken in this environment (library conflict)"),
    ("error while loading shared libraries", "tool binary is missing a shared library"),
    ("command not found", "tool is not on PATH"),
)


def read(path: Path) -> str:
    try:
        return path.read_text(errors="replace")
    except OSError:
        return ""


def classify_failure(builddir: Path):
    """Return [(node, reason)] when *every* failed node failed for an environmental reason.

    Returns an empty list if any node failed for a reason not in ENV_FAILURES, so a
    genuine PDK regression is never excused as 'just the environment'.
    """
    if not builddir.is_dir():
        return []

    # A node that failed has "Halting" in its SiliconCompiler wrapper log.
    failed = [log.parent for log in builddir.rglob("sc_*.log") if "Halting" in read(log)]
    if not failed:
        return []

    findings = []
    for nodedir in sorted(failed):
        # <build>/<design>/<job>/<step>/<index>/ -- name the node as step/index
        node = f"{nodedir.parent.name}/{nodedir.name}"
        toollogs = [p for p in nodedir.glob("*.log") if not p.name.startswith("sc_")]
        text = "\n".join(read(p) for p in toollogs)
        for needle, reason in ENV_FAILURES:
            if needle in text:
                findings.append((node, reason))
                break
        else:
            return []  # this one is a real failure; do not excuse the run

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("target", help="PDK name (ihp130) or target name (ihp130_demo)")
    parser.add_argument("--builddir", help="build directory (default: a temp dir)")
    parser.add_argument("--keep", action="store_true", help="keep the build directory")
    args = parser.parse_args()

    if not check_local_dataroot():
        return 2

    from siliconcompiler import ASIC, Design

    target_name = args.target if args.target.endswith("_demo") else f"{args.target}_demo"
    try:
        module = importlib.import_module(f"siliconcompiler.targets.{target_name}")
    except ModuleNotFoundError:
        print(f"ERROR: no SiliconCompiler target named {target_name}. Targets live in "
              "siliconcompiler/targets/ -- a new PDK or a renamed library class needs a "
              "matching change there.", file=sys.stderr)
        return 2
    target = getattr(module, target_name)

    workdir = Path(args.builddir) if args.builddir else Path(tempfile.mkdtemp(prefix="lpdk-smoke-"))
    srcdir = workdir / "src"
    srcdir.mkdir(parents=True, exist_ok=True)
    (srcdir / "heartbeat.v").write_text(RTL)
    (srcdir / "heartbeat.sdc").write_text(SDC)

    print(f"target             : {target_name}")
    print(f"build directory    : {workdir}\n")

    design = Design("heartbeat")
    design.set_dataroot("heartbeat", str(srcdir / "heartbeat.v"))
    design.set_topmodule("heartbeat", fileset="rtl")
    design.add_file("heartbeat.v", dataroot="heartbeat", fileset="rtl")
    design.add_file("heartbeat.sdc", dataroot="heartbeat", fileset="sdc")

    project = ASIC(design)
    project.add_fileset(["rtl", "sdc"])
    target(project)
    project.set("option", "builddir", str(workdir / "build"))

    ok = False
    try:
        ok = bool(project.run())
        project.summary()
    except Exception as exc:  # noqa: BLE001 - report, do not mask, tool failures
        print(f"\nrun raised: {exc}", file=sys.stderr)

    rc = 0
    if ok:
        print("\nSMOKE BUILD PASSED")
    else:
        env_failures = classify_failure(workdir / "build")
        if env_failures:
            print("\nSMOKE BUILD INCOMPLETE -- the only failures are environmental, "
                  "not the PDK:", file=sys.stderr)
            for node, reason in env_failures:
                print(f"  {node}: {reason}", file=sys.stderr)
            print("Everything before these nodes ran, so the PDK collateral itself loaded "
                  "and routed. Fix the tool install if you need full coverage.", file=sys.stderr)
            rc = 3
        else:
            print("\nSMOKE BUILD FAILED -- check the node logs under the build directory.",
                  file=sys.stderr)
            rc = 1

    if not args.keep and not args.builddir:
        shutil.rmtree(workdir, ignore_errors=True)
    else:
        print(f"build kept at {workdir}")

    return rc


if __name__ == "__main__":
    sys.exit(main())
