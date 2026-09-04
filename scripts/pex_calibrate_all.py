#!/usr/bin/env python3

###############################################################################
# Sweep the OpenROAD PEX calibration over every lambdapdk PDK variant.
#
# One "variant" is one (PDK, stackup, standard cell library) combination, since
# that triple is what the calibration measures:
#
#   * the initial per-layer R/C model ('bench' phase) comes from the PDK's tech
#     LEF and its OpenRCX deck -- so it varies with the PDK and its stackup;
#   * the correction factors ('full' phase) come from routing a survey of real
#     designs -- so they also vary with the standard cell library used.
#
# Variants where the two differ independently (asap7 vt flavors, sky130 hd/hdll,
# ihp130 1p2/1p5, gt2n width/vt) are therefore each run on their own; GF180
# ships stackup and cell height as separate PDK objects, so its 22 variants come
# straight from lambdapdk.get_pdks().
#
# The sweep is long and tools crash, so every variant runs in its own
# subprocess with its own log, build directory and output directory. A variant
# that fails, crashes or times out is recorded as such and the sweep continues;
# nothing is ever silently missing from the summary. Re-running resumes: only
# variants without a recorded success for this phase are run again.
#
# Output under --outdir:
#
#   results.json          machine-readable status of every variant
#   summary.txt           the end-of-run table, including every failure
#   all_rclayer.csv       every variant's per-layer R/C model, one table
#   all_rccorr.csv        every variant's correction factors, one table
#   <variant>/            that variant's CSVs, setup lines and result.json
#   logs/<variant>.log    everything the variant's run printed
#   build/<variant>/      its SiliconCompiler build directory
#
# Statuses: ok / cached (success), skipped (nothing to calibrate: the PDK ships
# no OpenRCX deck, or has no standard cell library), and failed / crashed /
# timeout / aborted, all of which are failures and set a non-zero exit code.
#
# Requires a SiliconCompiler carrying the PEX calibration utility
# (siliconcompiler.tools.openroad.utils.pex_calibrate) and an OpenROAD new
# enough for it (>=26Q3-23). Run --check first to confirm the setup resolves
# before committing to a long sweep. See patch_pex_tech_requirement() for the
# one SiliconCompiler bug this works around (sky130 and ihp130 cannot start the
# bench without it).
#
# Examples:
#   # what would run, and the PEX deck state of each variant
#   ./scripts/pex_calibrate_all.py --list
#
#   # validate every variant's setup end to end without running a tool
#   ./scripts/pex_calibrate_all.py --check
#
#   # phase 1 only (cheap, no routing): per-layer R/C from the decks
#   ./scripts/pex_calibrate_all.py --phase bench -j 4
#
#   # full correlation, 4 variants at a time, 6h cap per variant, saving disk.
#   # Re-run the same command afterwards to retry whatever did not succeed.
#   ./scripts/pex_calibrate_all.py --phase full -j 4 --timeout 21600 --clean-build
#
#   # just one PDK family, forcing a recompute
#   ./scripts/pex_calibrate_all.py --pdk sky130 --rerun
###############################################################################

import argparse
import contextlib
import csv
import functools
import json
import os
import shutil
import signal
import subprocess
import sys
import threading
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# Calibrate the checkout this script ships with, not whatever lambdapdk happens
# to be installed in the environment: the wheel carries no PDK data (it fetches
# a released tarball into ~/.sc instead), so importing the installed copy would
# silently calibrate the last release rather than the working tree.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import lambdapdk  # noqa: E402

from siliconcompiler import ASIC  # noqa: E402
from siliconcompiler.flows import asicflow, synflow  # noqa: E402

from lambdapdk.asap7.libs.asap7sc7p5t import ASAP7SC7p5RVT, ASAP7SC7p5LVT, \
    ASAP7SC7p5SLVT  # noqa: E402
from lambdapdk.asap7.libs.fakeio7 import FakeIO7Lambdalib_IO  # noqa: E402
from lambdapdk.asap7.libs.fakeram7 import FakeRAM7Lambdalib_SinglePort, \
    FakeRAM7Lambdalib_SinglePortRegfile  # noqa: E402
from lambdapdk.freepdk45.libs.nangate45 import Nangate45  # noqa: E402
from lambdapdk.freepdk45.libs.fakeram45 import FakeRAM45Lambdalib_SinglePort, \
    FakeRAM45Lambdalib_SinglePortRegfile  # noqa: E402
from lambdapdk.gf180.libs import gf180io, gf180mcu  # noqa: E402
from lambdapdk.gf180.libs.gf180sram import GF180Lambdalib_SinglePort, \
    GF180Lambdalib_SinglePortRegfile  # noqa: E402
from lambdapdk.gt2n.libs import stdcells as gt2n_stdcells  # noqa: E402
from lambdapdk.ihp130.libs.sg13g2_stdcell import IHP130StdCell_1p2, \
    IHP130StdCell_1p5  # noqa: E402
from lambdapdk.ihp130.libs.sg13g2_io import IHP130LambdaLib_IO_1p2, \
    IHP130LambdaLib_IO_1p5  # noqa: E402
from lambdapdk.ihp130.libs.sg13g2_sram import IHP130Lambdalib_SinglePort, \
    IHP130Lambdalib_SinglePortRegfile  # noqa: E402
from lambdapdk.sky130.libs.sky130sc import Sky130_SCHDLibrary, \
    Sky130_SCHDLLLibrary  # noqa: E402
from lambdapdk.sky130.libs.sky130io import Sky130LambdaLib_IO  # noqa: E402
from lambdapdk.sky130.libs.sky130sram import Sky130Lambdalib_SinglePort, \
    Sky130Lambdalib_SinglePortRegfile  # noqa: E402

try:
    from siliconcompiler.tools.openroad.utils import pex_calibrate  # noqa: E402
except ImportError as exc:  # pragma: no cover - environment guard
    sys.exit(
        f"error: this SiliconCompiler has no PEX calibration utility ({exc}).\n"
        "       Install/point at an SC that provides "
        "siliconcompiler.tools.openroad.utils.pex_calibrate.")


SCRIPT = Path(__file__).resolve()

# Statuses a variant can end in. 'ok' and 'cached' are successes; 'skipped' is a
# variant that cannot be calibrated at all (no deck, no cell library) and is not
# counted as a failure; the rest are failures.
OK_STATUSES = ("ok", "cached")
SKIP_STATUSES = ("skipped",)


##############################################################################
# Variant definition
##############################################################################
class Variant:
    """One (PDK, stackup, libtype) combination to calibrate.

    ``factory`` builds the pex_calibrate target callable; it is None for a
    variant that cannot be calibrated (see ``skip``).
    """

    def __init__(self, name, pdk, stackup, libtype, corners, factory, skip=None):
        self.name = name
        self.pdk = pdk
        self.stackup = stackup
        self.libtype = libtype
        self.corners = tuple(corners)
        self.factory = factory
        self.skip = skip

    def target(self, builddir=None):
        """The pex_calibrate target callable, optionally pinned to a build dir."""
        if self.factory is None:
            raise RuntimeError(f"{self.name} cannot be calibrated: {self.skip}")
        return self.factory(builddir)


def _finish(project, builddir):
    """Apply the settings every variant shares, last so nothing overrides them."""
    project.set_asic_delaymodel("nldm")
    if builddir:
        # Per-variant build directory: pex_calibrate names its job after the PDK,
        # so two libtypes of the same PDK (asap7 rvt/lvt, sky130 hd/hdll, ...)
        # would otherwise share -- and, run concurrently, corrupt -- one job.
        project.option.set_builddir(str(builddir))


##############################################################################
# Target builders, one per PDK family
#
# Each mirrors the family's shipped demo target (same flows, corners, voltages
# and constraints) with the standard cell library swapped for the variant's, so
# the sweep measures the variant rather than the demo's fixed pairing. The
# survey routes with the variant's library alone -- the other vt/height flavors
# are deliberately not added as alternates, so each row of the sweep is
# attributable to one library.
##############################################################################
def _freepdk45_target(builddir):
    def target(project):
        project.set_mainlib(Nangate45())
        project.set_flow(asicflow.ASICFlow())
        project.add_dep(synflow.SynthesisFlow())
        project.set_pdk("freepdk45")

        scenario = project.constraint.timing.make_scenario("typical")
        scenario.add_libcorner(["typical", "generic"])
        scenario.set_pexcorner("typical")
        scenario.add_check(["setup", "hold", "power"])

        project.constraint.area.set_density(40)
        project.constraint.area.set_coremargin(1)

        FakeRAM45Lambdalib_SinglePort.alias(project)
        FakeRAM45Lambdalib_SinglePortRegfile.alias(project)
        _finish(project, builddir)
    return target


def _asap7_target(lib_cls):
    def factory(builddir):
        def target(project):
            project.set_mainlib(lib_cls())
            project.set_flow(asicflow.ASICFlow())
            project.add_dep(synflow.SynthesisFlow())
            project.set_pdk("asap7")

            for name, libcorner, check in (("slow", "slow", "setup"),
                                           ("typical", "typical", "power"),
                                           ("fast", "fast", "hold")):
                scenario = project.constraint.timing.make_scenario(name)
                scenario.add_libcorner([libcorner, "generic"])
                scenario.set_pexcorner("typical")
                scenario.add_check(check)

            project.constraint.area.set_density(40)
            project.constraint.area.set_coremargin(1)

            FakeRAM7Lambdalib_SinglePort.alias(project)
            FakeRAM7Lambdalib_SinglePortRegfile.alias(project)
            FakeIO7Lambdalib_IO.alias(project)
            _finish(project, builddir)
        return target
    return factory


def _sky130_target(lib_cls):
    def factory(builddir):
        def target(project):
            project.set_mainlib(lib_cls())
            project.set_flow(asicflow.ASICFlow())
            project.add_dep(synflow.SynthesisFlow())
            project.set_pdk("skywater130")

            # Unlike skywater130_demo, which points every scenario at the
            # 'typical' deck, each scenario here uses the deck matching its
            # process corner. The survey only derives a correction factor for
            # the pexcorners a scenario names, so this is what gets all three
            # sky130 decks calibrated in one pass.
            for name, libcorner, pexcorner, check in (
                    ("slow", "slow", "maximum", "setup"),
                    ("typical", "typical", "typical", "power"),
                    ("fast", "fast", "minimum", "hold")):
                scenario = project.constraint.timing.make_scenario(name)
                scenario.add_libcorner([libcorner, "generic"])
                scenario.set_pexcorner(pexcorner)
                scenario.add_check(check)

            project.constraint.area.set_density(40)
            project.constraint.area.set_coremargin(1)

            Sky130Lambdalib_SinglePort.alias(project)
            Sky130Lambdalib_SinglePortRegfile.alias(project)
            Sky130LambdaLib_IO.alias(project)
            _finish(project, builddir)
        return target
    return factory


def _ihp130_target(lib_cls, io_cls):
    def factory(builddir):
        def target(project):
            project.set_mainlib(lib_cls())
            project.set_flow(asicflow.ASICFlow())
            project.add_dep(synflow.SynthesisFlow())
            project.set_pdk("ihp130")

            for name, check in (("slow", "setup"), ("typical", "power"), ("fast", "hold")):
                scenario = project.constraint.timing.make_scenario(name)
                scenario.add_libcorner(name)
                scenario.set_pexcorner("typical")
                scenario.add_check(check)

            project.constraint.area.set_density(40)
            project.constraint.area.set_coremargin(4.8)

            IHP130Lambdalib_SinglePort.alias(project)
            IHP130Lambdalib_SinglePortRegfile.alias(project)
            io_cls.alias(project)
            _finish(project, builddir)
        return target
    return factory


def _gt2n_target(lib_cls):
    def factory(builddir):
        def target(project):
            project.set_mainlib(lib_cls())
            project.set_flow(asicflow.ASICFlow())
            project.add_dep(synflow.SynthesisFlow())
            project.set_pdk("gt2n")

            scenario = project.constraint.timing.make_scenario("typical")
            scenario.add_libcorner("typical")
            scenario.set_pexcorner("typical")
            scenario.add_check(["setup", "hold", "power"])

            project.constraint.area.set_density(40)
            project.constraint.area.set_coremargin(1.0)
            _finish(project, builddir)
        return target
    return factory


def _gf180_target(pdk_cls, stackup, libtype):
    def factory(builddir):
        def target(project):
            stdcell = _gf180_stdcell_cls(stackup, libtype)()

            project.set_pdk(pdk_cls())
            project.add_asiclib(stdcell)
            project.set_mainlib(stdcell)
            project.set_flow(asicflow.ASICFlow())
            project.add_dep(synflow.SynthesisFlow())

            for name, libcorner, pexcorner, check, voltage in (
                    ("slow", "slow", "wst", "setup", 4.5),
                    ("typical", "typical", "typ", "power", 5.0),
                    ("fast", "fast", "bst", "hold", 5.5)):
                scenario = project.constraint.timing.make_scenario(name)
                scenario.add_libcorner(libcorner)
                scenario.set_pexcorner(pexcorner)
                scenario.add_check(check)
                scenario.set_pin_voltage("VDD", voltage)

            project.constraint.area.set_density(40)
            project.constraint.area.set_coremargin(1)

            GF180Lambdalib_SinglePort.alias(project)
            GF180Lambdalib_SinglePortRegfile.alias(project)
            io_cls = _gf180_io_cls(stackup)
            if io_cls is not None:
                io_cls.alias(project)

            # Register the decks on the PDK object the project resolved, not on
            # the instance handed to set_pdk: the standard cell library declares
            # its own compatible PDK instances, so the object the flow reads back
            # is not necessarily the one constructed above.
            register_gf180_decks(project.get_library(str(project.get("asic", "pdk"))), stackup)
            _finish(project, builddir)
        return target
    return factory


##############################################################################
# GF180 OpenRCX deck selection
#
# lambdapdk ships GF180 as 22 PDK objects (11 stackups x 7t/9t), but only the
# six stackups with an OPTB deck are wired up: gf180/__init__.py builds the deck
# name with a hardcoded '_sp_smim_OPTB_' and bails out early for any stackup
# missing from its _PEX table. The other five stackups do ship decks -- as OPTA
# -- so every variant can be correlated once the right option is selected.
##############################################################################
GF180_CORNERS = ("bst", "typ", "wst")

# Prefer OPTB (the thicker MIM option), which is what gf180/__init__.py already
# uses where it exists, so the six already-wired stackups reproduce their
# current decks rather than silently switching to OPTA.
GF180_DECK_OPTIONS = ("B", "A")

GF180_DECK_SUBPATH = Path("lambdapdk", "gf180", "base", "pex", "openroad")


def _gf180_metal_layers(stackup):
    """Routing layer count, e.g. 5 for '5LM_1TM_9K'."""
    return int(stackup[0])


def _gf180_stdcell_cls(stackup, libtype):
    """The standard cell library paired with this stackup and cell height.

    The 30K options carry their own library. They share the cells with the
    thinner options of the same layer count, but not the power grid: their top
    metal has a 2.2um minimum width, which the shared 1.6um stripe violates.
    """
    name = f"GF180_MCU_{libtype.upper()}_{_gf180_metal_layers(stackup)}LM"
    if stackup.endswith("_30K"):
        name += "_30K"
    return getattr(gf180mcu, f"{name}Library")


def _gf180_io_cls(stackup):
    """The matching IO lambdalib, or None (there is no 6LM IO library)."""
    return getattr(gf180io, f"GF180Lambdalib_IO_{_gf180_metal_layers(stackup)}LM", None)


@functools.lru_cache(maxsize=None)
def gf180_deck_dir():
    """On-disk directory holding the GF180 OpenRCX decks.

    Taken from a deck lambdapdk already registers rather than from the package
    layout: the 'lambdapdk' dataroot resolves either to this checkout or to a
    tarball unpacked under ~/.sc, and the injected decks have to come from the
    same place as the ones the PDK ships or the two would disagree.
    """
    from lambdapdk.gf180 import GF180_5LM_1TM_9K_9t
    pdk = GF180_5LM_1TM_9K_9t()
    for corner in sorted(registered_corners(pdk)):
        for path in deck_files(pdk, corner):
            return Path(path).parent
    return Path(lambdapdk.__file__).parent / "gf180" / "base" / "pex" / "openroad"


def gf180_deck_base(stackup, option):
    """Deck basename for a stackup, mirroring gf180/__init__.py's construction."""
    return f'gf180mcu_1p{stackup.replace("L", "").lower()}_sp_smim_OPT{option}'


def gf180_deck_option(stackup):
    """Return the deck option shipping a complete corner set, or None."""
    for option in GF180_DECK_OPTIONS:
        if all((gf180_deck_dir() / f"{gf180_deck_base(stackup, option)}_{corner}.rules").is_file()
               for corner in GF180_CORNERS):
            return option
    return None


def register_gf180_decks(pdk, stackup):
    """Register any missing OpenRCX decks on ``pdk``.

    Returns the deck option used, or None when the PDK already carried a
    complete set (the six stackups gf180/__init__.py wires up itself).
    """
    missing = [corner for corner in GF180_CORNERS if corner not in registered_corners(pdk)]
    if not missing:
        return None

    option = gf180_deck_option(stackup)
    if option is None:
        raise RuntimeError(
            f"no complete OpenRCX deck set found for stackup '{stackup}' in "
            f"{gf180_deck_dir()}; looked for {gf180_deck_base(stackup, 'B')}_<corner>.rules "
            "and the OPTA equivalent")

    with pdk.active_dataroot("lambdapdk"):
        for corner in missing:
            deck = f"{gf180_deck_base(stackup, option)}_{corner}.rules"
            with pdk.active_fileset(f"openroad.pex.{corner}"):
                pdk.add_file(GF180_DECK_SUBPATH / deck, filetype="openrcx")
                pdk.add_pexmodelfileset("openroad", corner)
    return option


##############################################################################
# Variant enumeration
##############################################################################
def _gf180_variants():
    variants = []
    for pdk in lambdapdk.get_pdks():
        if not pdk.name.startswith("GF180_"):
            continue
        # Names are built as GF180_<stackup>_<libtype>, e.g. GF180_5LM_1TM_9K_9t.
        stackup, libtype = pdk.name[len("GF180_"):].rsplit("_", 1)
        variants.append(Variant(
            name=pdk.name, pdk=pdk.name, stackup=stackup, libtype=libtype,
            corners=GF180_CORNERS,
            factory=_gf180_target(type(pdk), stackup, libtype)))
    return sorted(variants, key=lambda v: v.name)


def _interposer_variants():
    variants = []
    for pdk in lambdapdk.get_pdks():
        if not pdk.name.startswith("interposer_"):
            continue
        variants.append(Variant(
            name=pdk.name, pdk=pdk.name, stackup=str(pdk.get("pdk", "stackup")),
            libtype="-", corners=(), factory=None,
            skip="interposer PDK: no standard cell library and no OpenRCX deck"))
    return sorted(variants, key=lambda v: v.name)


def all_variants():
    """Every variant of every lambdapdk PDK, sorted by name."""
    variants = [
        Variant("freepdk45", "freepdk45", "10M", "nangate45", ("typical",),
                _freepdk45_target),
    ]

    for libtype, lib_cls in (("rvt", ASAP7SC7p5RVT),
                             ("lvt", ASAP7SC7p5LVT),
                             ("slvt", ASAP7SC7p5SLVT)):
        variants.append(Variant(f"asap7.{libtype}", "asap7", "10M", f"asap7sc7p5t_{libtype}",
                                ("typical",), _asap7_target(lib_cls)))

    for libtype, lib_cls in (("hd", Sky130_SCHDLibrary), ("hdll", Sky130_SCHDLLLibrary)):
        variants.append(Variant(f"skywater130.{libtype}", "skywater130", "5M1LI",
                                f"sky130{libtype}", ("minimum", "typical", "maximum"),
                                _sky130_target(lib_cls)))

    for libtype, lib_cls, io_cls in (("1p2", IHP130StdCell_1p2, IHP130LambdaLib_IO_1p2),
                                     ("1p5", IHP130StdCell_1p5, IHP130LambdaLib_IO_1p5)):
        variants.append(Variant(f"ihp130.{libtype}", "ihp130", "5M2TL",
                                f"sg13g2_stdcell_{libtype}", ("typical",),
                                _ihp130_target(lib_cls, io_cls)))

    for width in ("13", "31"):
        for vt in ("hvt", "svt", "lvt", "ulvt", "elvt"):
            lib_cls = getattr(gt2n_stdcells, f"GT2N6TW{width}{vt.upper()}")
            variants.append(Variant(f"gt2n.w{width}_{vt}", "gt2n", "13M",
                                    f"gt2n_stdcells_w{width}_{vt}", ("typical",),
                                    _gt2n_target(lib_cls)))

    variants.extend(_gf180_variants())
    variants.extend(_interposer_variants())
    return variants


def select_variants(variants, pdks=None, stackups=None, libtypes=None, names=None):
    """Filter the variant list by the CLI selectors (case-insensitive substrings)."""
    def matches(value, patterns):
        return any(pattern.lower() in str(value).lower() for pattern in patterns)

    if names:
        variants = [v for v in variants if v.name in names]
    if pdks:
        variants = [v for v in variants if matches(v.pdk, pdks)]
    if stackups:
        variants = [v for v in variants if matches(v.stackup, stackups)]
    if libtypes:
        variants = [v for v in variants if matches(v.libtype, libtypes)]
    return variants


##############################################################################
# Preflight: does this variant have everything it needs?
##############################################################################
def registered_corners(pdk):
    """Pexcorners the PDK has registered an OpenRCX deck fileset for."""
    if not pdk.valid("pdk", "pexmodelfileset", "openroad"):
        return set()
    return set(pdk.getkeys("pdk", "pexmodelfileset", "openroad"))


def deck_files(pdk, corner):
    files = []
    for fileset in pdk.get("pdk", "pexmodelfileset", "openroad", corner):
        files.extend(pdk.get_file(fileset=fileset, filetype="openrcx"))
    return files


def preflight(variant, log_path=None):
    """Build the variant's target and check it can actually be calibrated.

    An exception's traceback is appended to ``log_path`` when one is given.

    Returns ``(status, message)`` where status is:

        * ``"ok"``    -- ready to run;
        * ``"skip"``  -- nothing to calibrate here and never will be (the PDK
          ships no OpenRCX deck, or has no standard cell library at all);
        * ``"error"`` -- the setup is broken and should be fixed.

    Exercises the whole setup path -- library pairing, scenarios, deck
    injection, PDK name resolution, deck files on disk -- without launching a
    tool, so a broken variant is caught in seconds instead of after an hour of
    routing.
    """
    if variant.factory is None:
        return "skip", variant.skip

    try:
        target = variant.target()
        project = ASIC(pex_calibrate._bench_design())
        project.add_fileset("rtl")
        target(project)
        pdk_name = str(project.get("asic", "pdk"))
        if not pdk_name:
            return "error", "target selects no PDK ([asic,pdk] is unset)"
        pdk = project.get_library(pdk_name)

        corners = sorted(corner for corner in registered_corners(pdk)
                         if deck_files(pdk, corner))
        if not corners:
            return "skip", "PDK ships no OpenRCX deck (pdk 'pexmodelfileset' / 'openrcx')"

        missing = [f for corner in corners for f in deck_files(pdk, corner)
                   if not Path(f).is_file()]
        if missing:
            return "error", f"deck file(s) not on disk: {', '.join(missing)}"

        # Every pexcorner a timing scenario names must have a deck: the calibrate
        # task refuses to run rather than silently omit a corner.
        wanted = set()
        for scenario in project.getkeys("constraint", "timing", "scenario"):
            pexcorner = project.get("constraint", "timing", "scenario", scenario, "pexcorner")
            if pexcorner:
                wanted.add(str(pexcorner))
        uncovered = sorted(wanted - set(corners))
        if uncovered:
            return "error", f"timing scenario pexcorner(s) with no deck: {', '.join(uncovered)}"

        return "ok", f"{len(corners)} deck corner(s): {', '.join(corners)}"
    except Exception as exc:
        # The summary only carries the one-line message, which is not always
        # enough to tell a broken PDK setup from a transient (a concurrent
        # dataroot fetch losing a race, say), so keep the traceback next to the
        # variant's other output rather than dropping it on the floor.
        if log_path:
            log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(log_path, "a") as fid:
                fid.write(f"preflight failed for {variant.name}:\n")
                fid.write(traceback.format_exc())
        return "error", f"{type(exc).__name__}: {exc}"


def describe(variant, result=None):
    """A one-line plan for a variant, optionally annotated with its preflight."""
    line = f"{variant.name:26} {variant.pdk:24} {variant.stackup:16} {variant.libtype:22}"
    if result is None:
        return line.rstrip()
    return f"{line} {result[0].upper():5} {result[1]}"


##############################################################################
# Worker: calibrate one variant (runs in its own process)
##############################################################################
def patch_pex_tech_requirement():
    """Stop the PEX bench tasks demanding a LEF from every APR tech fileset.

    ``siliconcompiler.tools.openroad.pex.PEXBaseTask.setup`` marks
    ``[fileset,<fs>,file,lef]`` required for every fileset in the PDK's
    ``aprtechfileset``, without the ``has_file()`` guard the APR tasks
    (``_apr.py``) and the metal fill task use. A PDK that registers a non-LEF
    fileset there -- sky130 and ihp130 both register their metal fill JSON as an
    OpenROAD APR tech fileset -- then fails the bench flow before it starts with
    'Cannot resolve required keypath [library,...,fileset,openroad.fill,file,lef]'.

    Drop the requirement for filesets that ship no LEF, and only for these tasks:
    the tech LEF fileset still carries one, so it stays required. Once
    SiliconCompiler adds the guard upstream this becomes a no-op (the bad key is
    never requested), so it is safe to leave applied.
    """
    from siliconcompiler.tools.openroad.pex import PEXBaseTask

    original = PEXBaseTask.add_required_key

    def add_required_key(self, *keypath, **kwargs):
        if (len(keypath) >= 5 and keypath[1] == "fileset" and keypath[-2:] == ("file", "lef")
                and hasattr(keypath[0], "has_file")
                and not keypath[0].has_file(fileset=keypath[2], filetype="lef")):
            return
        return original(self, *keypath, **kwargs)

    PEXBaseTask.add_required_key = add_required_key


def via_note(variant):
    """Warn when a variant's setup lines will carry no via resistance.

    The bench characterizes routing layers only -- vias are never produced by
    the correlation and survive only as PDK-preserved entries. A variant that
    starts with no rclayer at all therefore emits no via lines, and pasting its
    output as-is leaves the variant with no via resistance model.
    """
    try:
        project = ASIC(pex_calibrate._bench_design())
        project.add_fileset("rtl")
        variant.target()(project)
        pdk = project.get_library(str(project.get("asic", "pdk")))
        if pdk.get("tool", "openroad", "rclayer"):
            return None
    except Exception:
        return None
    return (f"# NOTE: {variant.name} had no rclayer entries before this run, so the lines\n"
            f"#       below contain NO via resistance. Carry the PDK's via resistance over by\n"
            f"#       hand, or the variant ships without a via model.\n")


def run_variant(variant, vardir, builddir, phase, rerun, score):
    """Calibrate one variant into ``vardir``. Raises on failure."""
    vardir.mkdir(parents=True, exist_ok=True)
    target = variant.target(builddir)

    if phase == "bench":
        pdk_name = pex_calibrate.derive_pdk_name(target)
        rclayer_path = vardir / f"{pdk_name}.rclayer.csv"
        if rclayer_path.is_file() and not rerun:
            model = pex_calibrate.read_rclayer_csv(rclayer_path)
        else:
            model = pex_calibrate.run_bench(target)
            pex_calibrate.write_rclayer_csv(rclayer_path, model)
        setup = pex_calibrate.format_rclayer_lines(model)
    else:
        model, factors = pex_calibrate.calibrate(
            target, outdir=str(vardir), rerun=rerun, score=score)
        setup = (pex_calibrate.format_rclayer_lines(model, factors) + "\n\n" +
                 pex_calibrate.format_rccorr_lines(factors))

    # The paste-able setup lines are rendered here rather than taken from what
    # calibrate() prints: SiliconCompiler logs the whole flow to stdout too, so
    # capturing stdout would bury the lines. The log keeps the flow output; this
    # file holds nothing but the lines meant for the PDK setup.
    setup_path = vardir / f"{variant.name}.setup.txt"
    note = via_note(variant)
    setup_path.write_text((note or "") + setup + "\n")
    return setup_path


def worker_main(args):
    """--worker entry point: calibrate exactly one variant, report via JSON."""
    matches = [v for v in all_variants() if v.name == args.worker]
    if not matches:
        print(f"error: unknown variant '{args.worker}'", file=sys.stderr)
        return 2
    variant = matches[0]

    if not args.no_patch:
        patch_pex_tech_requirement()

    outdir = Path(args.outdir).resolve()
    vardir = outdir / variant.name
    builddir = Path(args.builddir).resolve() / variant.name if args.builddir else None
    vardir.mkdir(parents=True, exist_ok=True)
    result_path = vardir / "result.json"

    started = time.time()
    result = {"variant": variant.name, "pdk": variant.pdk, "stackup": variant.stackup,
              "libtype": variant.libtype, "phase": args.phase, "score": args.score}
    try:
        setup_path = run_variant(variant, vardir, builddir, args.phase, args.rerun, args.score)
        result.update(status="ok", setup=str(setup_path), error=None)
        rc = 0
    except Exception as exc:
        traceback.print_exc(file=sys.stderr)
        result.update(status="failed", setup=None, error=f"{type(exc).__name__}: {exc}")
        rc = 1
    result["seconds"] = round(time.time() - started, 1)
    result_path.write_text(json.dumps(result, indent=2) + "\n")
    return rc


##############################################################################
# Driver: run every variant in its own subprocess
##############################################################################
_children = set()
_children_lock = threading.Lock()
_aborting = threading.Event()


def _spawn(cmd, log_path, timeout):
    """Run ``cmd`` with its output teed to ``log_path``. Returns (rc, timed_out)."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "w") as log:
        log.write(f"$ {' '.join(cmd)}\n\n")
        log.flush()
        # start_new_session so a timeout can take down the whole tool process
        # tree (OpenROAD/yosys children), not just the python wrapper.
        proc = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT,
                                start_new_session=True)
        with _children_lock:
            _children.add(proc)
        try:
            try:
                proc.wait(timeout=timeout or None)
                return proc.returncode, False
            except subprocess.TimeoutExpired:
                _kill(proc)
                log.write(f"\n\n*** killed after {timeout}s timeout ***\n")
                return proc.wait(), True
        finally:
            with _children_lock:
                _children.discard(proc)


def _kill(proc):
    """Terminate a child's whole process group, escalating to SIGKILL."""
    for sig in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(os.getpgid(proc.pid), sig)
        except (ProcessLookupError, PermissionError):
            return
        try:
            proc.wait(timeout=10)
            return
        except subprocess.TimeoutExpired:
            continue


def _kill_all():
    with _children_lock:
        children = list(_children)
    for proc in children:
        _kill(proc)


def _install_interrupt_handler():
    """Make Ctrl-C take the tools down with it.

    Without this the running variants keep going: the thread pool's shutdown
    waits for its workers, and each worker is blocked in proc.wait(). Killing
    the children from the handler unblocks them, and the variants that never
    started see the abort flag and record themselves as aborted.
    """
    def handler(signum, frame):
        if not _aborting.is_set():
            _aborting.set()
            print("\ninterrupted: killing running variants...", file=sys.stderr)
            _kill_all()
        raise KeyboardInterrupt

    signal.signal(signal.SIGINT, handler)


def load_result(vardir):
    """Read a variant's recorded result, or None."""
    path = vardir / "result.json"
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return None


def run_one(variant, args, outdir, builddir, index, total, preflights):
    """Run (or skip/resume) one variant and return its result dict."""
    vardir = outdir / variant.name
    log_path = outdir / "logs" / f"{variant.name}.log"
    base = {"variant": variant.name, "pdk": variant.pdk, "stackup": variant.stackup,
            "libtype": variant.libtype, "phase": args.phase, "log": str(log_path),
            "seconds": 0.0, "setup": None}

    if variant.factory is None:
        return {**base, "status": "skipped", "error": variant.skip, "log": None}

    # Resume: a recorded success is reused only when it answers this run's
    # question. A 'bench' result is not a 'full' one, and an unscored result is
    # not a scored one, so neither counts as done here.
    previous = load_result(vardir)
    if (previous and previous.get("status") == "ok"
            and previous.get("phase") == args.phase
            and (previous.get("score") or not args.score)
            and not args.rerun and not args.force):
        return {**base, **previous, "status": "cached", "log": str(log_path)}

    if not args.no_preflight:
        status, message = preflights[variant.name]
        if status != "ok":
            # A structural skip (no deck) is expected and not a failure; a broken
            # setup is reported as a failure so it cannot hide in the summary.
            # A failure keeps its log: preflight left the traceback there.
            return {**base, "status": "skipped" if status == "skip" else "failed",
                    "error": message, "log": None if status == "skip" else str(log_path)}

    if _aborting.is_set():
        return {**base, "status": "aborted", "error": "sweep aborted before this variant ran"}

    cmd = [sys.executable, str(SCRIPT), "--worker", variant.name,
           "--outdir", str(outdir), "--phase", args.phase]
    if builddir:
        cmd += ["--builddir", str(builddir)]
    if args.rerun:
        cmd.append("--rerun")
    if args.score:
        cmd.append("--score")
    if args.no_patch:
        cmd.append("--no-patch")

    # Drop any earlier verdict first: if this run's worker dies before it can
    # record one, a stale result.json would be read back as this run's outcome.
    (vardir / "result.json").unlink(missing_ok=True)

    print(f"[{index}/{total}] {variant.name}: running ({args.phase})", flush=True)
    started = time.time()
    rc, timed_out = _spawn(cmd, log_path, args.timeout)
    elapsed = round(time.time() - started, 1)

    # The worker records its own outcome; fall back to the exit code when it
    # died before it could (crash, OOM kill, timeout).
    result = load_result(vardir) if not timed_out else None
    if result and result.get("status") in ("ok", "failed"):
        result = {**base, **result, "log": str(log_path), "seconds": elapsed}
    elif timed_out:
        result = {**base, "status": "timeout", "seconds": elapsed,
                  "error": f"exceeded the {args.timeout}s per-variant timeout"}
    elif _aborting.is_set():
        result = {**base, "status": "aborted", "seconds": elapsed,
                  "error": "interrupted"}
    else:
        result = {**base, "status": "crashed", "seconds": elapsed,
                  "error": f"worker exited {rc} without recording a result "
                           f"(see {log_path})"}

    if not load_result(vardir):
        # The worker died before recording anything (timeout, crash, OOM kill).
        # Write the driver's verdict in its place so the variant directory always
        # explains itself: otherwise the only record of the failure is the
        # sweep-wide results.json, and it is gone the moment that is rewritten.
        vardir.mkdir(parents=True, exist_ok=True)
        (vardir / "result.json").write_text(json.dumps(result, indent=2) + "\n")

    status = result["status"]
    detail = "" if status == "ok" else f": {result.get('error')}"
    print(f"[{index}/{total}] {variant.name}: {status.upper()} in {elapsed}s{detail}", flush=True)

    if args.clean_build and status == "ok" and builddir:
        shutil.rmtree(builddir / variant.name, ignore_errors=True)
    return result


##############################################################################
# Reporting
##############################################################################
def load_previous_results(outdir):
    """Read the results.json a previous run of this outdir left, keyed by variant.

    A run over a subset of the variants (retrying the failures, say) must not
    make the sweep-wide files forget everything else in the directory, so its
    output is merged onto whatever is already recorded.
    """
    path = outdir / "results.json"
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text())
    except (OSError, ValueError):
        return {}
    return {result["variant"]: result
            for result in payload.get("results", []) if result.get("variant")}


def write_results(outdir, results, args, previous):
    """Write results.json. Called after every variant so a crash keeps the data."""
    merged = {**previous, **results}
    payload = {
        "phase": args.phase,
        "score": args.score,
        "outdir": str(outdir),
        "results": [merged[name] for name in sorted(merged)],
    }
    tmp = outdir / "results.json.tmp"
    tmp.write_text(json.dumps(payload, indent=2) + "\n")
    tmp.replace(outdir / "results.json")


def collect_csvs(outdir, results):
    """Merge the per-variant CSVs into two sweep-wide tables.

    Each row is prefixed with the variant it came from, so the whole sweep can
    be loaded as one table instead of 40 files. Every variant directory in
    ``outdir`` is collected, not just the ones this run touched -- the CSVs on
    disk are the record, and a partial re-run must not shrink these tables.
    """
    merged = {}
    for kind, columns in (
            ("rclayer", ["pexcorner", "layertype", "layer", "res_ohm_per_um",
                         "cap_F_per_um", "source"]),
            ("rccorr", ["pexcorner", "layer", "cap_factor", "res_factor", "nseg"])):
        rows = []
        for vardir in sorted(p for p in outdir.iterdir() if p.is_dir() and p.name != "logs"):
            name = vardir.name
            meta = results.get(name, {})
            for path in sorted(vardir.glob(f"*.{kind}.csv")):
                with open(path, newline="") as fid:
                    for row in csv.DictReader(fid):
                        rows.append({"variant": name,
                                     "pdk": meta.get("pdk", ""),
                                     "stackup": meta.get("stackup", ""),
                                     "libtype": meta.get("libtype", ""),
                                     **{col: row.get(col, "") for col in columns}})
        if not rows:
            continue
        path = outdir / f"all_{kind}.csv"
        with open(path, "w", newline="") as fid:
            writer = csv.DictWriter(
                fid, fieldnames=["variant", "pdk", "stackup", "libtype"] + columns)
            writer.writeheader()
            writer.writerows(rows)
        merged[kind] = (path, len(rows))
    return merged


def summarize(outdir, results, variants, elapsed, merged, previous):
    """Render the end-of-sweep summary; returns the text (also written to disk).

    Covers everything recorded in ``outdir``, not only this run: a re-run of a
    few variants should still leave a summary that describes the whole sweep.
    Rows this run did not touch are marked, so the two are never confused.
    """
    order = [v.name for v in variants]
    carried = [name for name in sorted({**previous, **results}) if name not in order]
    all_results = {**previous, **results}

    lines = []
    lines.append(f"{'variant':26} {'status':9} {'time':>9}  detail")
    lines.append("-" * 110)
    for name in order + carried:
        result = all_results.get(name)
        if not result:
            continue
        detail = result.get("error") or result.get("setup") or ""
        mark = " (earlier run)" if name in carried else ""
        lines.append(f"{name:26} {result['status']:9} {result['seconds']:>8.1f}s  {detail}{mark}")

    counts = {}
    for result in all_results.values():
        counts[result["status"]] = counts.get(result["status"], 0) + 1
    failures = [name for name in order + carried
                if all_results.get(name, {}).get("status") not in OK_STATUSES + SKIP_STATUSES]
    results = all_results

    lines.append("")
    lines.append("counts: " + ", ".join(f"{status}={count}"
                                        for status, count in sorted(counts.items())))
    lines.append(f"wall time: {elapsed / 60:.1f} min")
    for kind, (path, nrows) in sorted(merged.items()):
        lines.append(f"collected: {path} ({nrows} rows)")
    lines.append(f"results:   {outdir / 'results.json'}")
    if failures:
        lines.append("")
        lines.append(f"FAILED ({len(failures)}):")
        for name in failures:
            result = results[name]
            lines.append(f"  {name:26} {result['status']:9} {result.get('error')}")
            if result.get("log"):
                lines.append(f"  {'':26} log: {result['log']}")
    text = "\n".join(lines)
    (outdir / "summary.txt").write_text(text + "\n")
    return text


##############################################################################
# CLI
##############################################################################
def main():
    parser = argparse.ArgumentParser(
        description="Run the OpenROAD PEX calibration across every lambdapdk PDK, stackup "
                    "and standard cell library, collecting the results and recording every "
                    "failure.",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "-o", "--outdir", default="pex_sweep", metavar="DIR",
        help="output directory for the per-variant data, logs and summary (default: ./pex_sweep)")
    parser.add_argument(
        "-b", "--builddir", default=None, metavar="DIR",
        help="SiliconCompiler build directory root; each variant gets a subdirectory "
             "(default: <outdir>/build)")
    parser.add_argument(
        "--phase", choices=("bench", "full"), default="full",
        help="'bench' derives the per-layer R/C from the decks only (cheap, no routing); "
             "'full' also runs the design survey to derive correction factors (default: full)")
    parser.add_argument(
        "-j", "--jobs", type=int, default=1, metavar="N",
        help="number of variants to calibrate concurrently (default: 1). Each variant already "
             "runs multi-threaded tools, so keep N well below the core count")
    parser.add_argument(
        "--timeout", type=int, default=0, metavar="SECONDS",
        help="kill a variant (and its tool processes) after this long; 0 disables (default: 0)")
    parser.add_argument(
        "--pdk", action="append", metavar="NAME",
        help="restrict to PDKs whose name contains NAME, e.g. gf180; repeatable")
    parser.add_argument(
        "--stackup", action="append", metavar="STACKUP",
        help="restrict to stackups containing STACKUP, e.g. 3LM; repeatable")
    parser.add_argument(
        "--libtype", action="append", metavar="LIBTYPE",
        help="restrict to standard cell libraries containing LIBTYPE, e.g. 9t; repeatable")
    parser.add_argument(
        "--variant", action="append", metavar="NAME",
        help="restrict to an exact variant name (see --list); repeatable")
    parser.add_argument(
        "--rerun", action="store_true",
        help="recompute a variant even when its CSVs already exist")
    parser.add_argument(
        "--force", action="store_true",
        help="re-run variants already recorded as ok, but reuse their CSVs (unlike --rerun)")
    parser.add_argument(
        "--score", action="store_true",
        help="also re-route the survey to report the estimate error before/after (much slower)")
    parser.add_argument(
        "--clean-build", action="store_true",
        help="delete a variant's build directory after it succeeds (saves a lot of disk)")
    parser.add_argument(
        "--no-preflight", action="store_true",
        help="do not check a variant's setup before running it")
    parser.add_argument(
        "--no-patch", action="store_true",
        help="do not apply the PEX-bench APR tech fileset workaround "
             "(see patch_pex_tech_requirement); sky130 and ihp130 then fail to start")
    parser.add_argument(
        "--list", action="store_true",
        help="print the variants that would run, with their PEX deck state, and exit")
    parser.add_argument(
        "--check", action="store_true",
        help="preflight every variant (no tool is run) and exit")
    parser.add_argument(
        "--worker", metavar="VARIANT", help=argparse.SUPPRESS)
    args = parser.parse_args()

    variants = select_variants(all_variants(), pdks=args.pdk, stackups=args.stackup,
                               libtypes=args.libtype, names=args.variant)
    if not variants:
        parser.error("no variants selected")

    if args.worker:
        return worker_main(args)

    if args.list or args.check:
        statuses = {}
        for variant in variants:
            if args.check:
                statuses[variant.name] = preflight(variant)
            print(describe(variant, statuses.get(variant.name)), flush=True)
        if not args.check:
            print(f"\n{len(variants)} variant(s) selected")
            return 0

        ready = [name for name, (status, _) in statuses.items() if status == "ok"]
        broken = [(name, message) for name, (status, message) in statuses.items()
                  if status == "error"]
        print(f"\n{len(ready)}/{len(variants)} variant(s) ready, "
              f"{len(variants) - len(ready) - len(broken)} nothing to calibrate, "
              f"{len(broken)} broken")
        for name, message in broken:
            print(f"  BROKEN {name}: {message}")
        return 1 if broken else 0

    outdir = Path(args.outdir).resolve()
    builddir = Path(args.builddir).resolve() if args.builddir else outdir / "build"
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "logs").mkdir(exist_ok=True)

    # Anything an earlier run of this directory recorded, so a run over a subset
    # of the variants adds to the sweep instead of replacing it.
    previous = load_previous_results(outdir)

    print(f"phase:    {args.phase}{' (+score)' if args.score else ''}")
    print(f"variants: {len(variants)}  jobs: {args.jobs}  "
          f"timeout: {args.timeout or 'none'}")
    print(f"outdir:   {outdir}")
    print(f"builddir: {builddir}\n")

    _install_interrupt_handler()

    started = time.time()

    # Preflight every variant here, serially, before any worker starts. Besides
    # catching broken setups in seconds, this resolves every remote dataroot
    # once: SiliconCompiler mis-handles several processes fetching the same
    # uncached dataroot at the same time (it fails with "Source URI ... is not
    # supported"), which silently costs a variant or two on a cold ~/.sc.
    preflights = {}
    if not args.no_preflight:
        print(f"preflighting {len(variants)} variant(s) (also warms the dataroot cache)...",
              flush=True)
        for variant in variants:
            preflights[variant.name] = preflight(
                variant, log_path=outdir / "logs" / f"{variant.name}.log")
        broken = sum(1 for status, _ in preflights.values() if status == "error")
        ready = sum(1 for status, _ in preflights.values() if status == "ok")
        print(f"  {ready} ready, {len(variants) - ready - broken} nothing to calibrate, "
              f"{broken} broken\n", flush=True)

    results = {}
    results_lock = threading.Lock()

    def work(item):
        index, variant = item
        try:
            result = run_one(variant, args, outdir, builddir, index, len(variants), preflights)
        except Exception as exc:  # a driver-side bug must not lose the sweep
            traceback.print_exc()
            result = {"variant": variant.name, "pdk": variant.pdk, "stackup": variant.stackup,
                      "libtype": variant.libtype, "phase": args.phase, "seconds": 0.0,
                      "status": "crashed", "log": None, "setup": None,
                      "error": f"driver error: {type(exc).__name__}: {exc}"}
        with results_lock:
            results[variant.name] = result
            write_results(outdir, results, args, previous)
        return result

    items = list(enumerate(variants, start=1))
    try:
        if args.jobs > 1:
            with ThreadPoolExecutor(max_workers=args.jobs) as pool:
                list(pool.map(work, items))
        else:
            for item in items:
                work(item)
    except KeyboardInterrupt:
        # The SIGINT handler has already flagged the abort and killed the
        # children; this only stops the sweep and falls through to the summary,
        # which still names every variant that did not finish.
        _aborting.set()

    with results_lock:
        for variant in variants:
            results.setdefault(variant.name, {
                "variant": variant.name, "pdk": variant.pdk, "stackup": variant.stackup,
                "libtype": variant.libtype, "phase": args.phase, "seconds": 0.0,
                "status": "aborted", "log": None, "setup": None,
                "error": "never ran (sweep interrupted)"})
        write_results(outdir, results, args, previous)
        merged = collect_csvs(outdir, {**previous, **results})
        print("\n" + summarize(outdir, results, variants, time.time() - started,
                               merged, previous))

    failures = [r for r in results.values()
                if r["status"] not in OK_STATUSES + SKIP_STATUSES]
    return 1 if failures else 0


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        sys.exit(main())
    _kill_all()
    sys.exit(130)
