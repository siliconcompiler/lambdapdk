import os
import shutil
import subprocess
import sys

import pytest

from lambdapdk.asap7 import ASAP7PDK
from lambdapdk.asap7.libs.asap7sc7p5t import (
    ASAP7SC7p5RVT,
    ASAP7SC7p5LVT,
    ASAP7SC7p5SLVT,
)


# Cells verified to compare clean against the shipped CDL. Chosen to span the
# interesting cases rather than for coverage volume: the full library sweep sits
# at 192/209 and is documented next to the deck.
STDCELLS = [
    # (library class, cell) -- smallest useful case upwards
    (ASAP7SC7p5RVT, "INVx1_ASAP7_75t_R"),
    (ASAP7SC7p5RVT, "NAND2x1_ASAP7_75t_R"),
    # NAND2xp67 is the cell that exposed the LIG/LISD short, where merging the
    # two local-interconnect layers extracted A and Y as a single net. It is the
    # regression guard for the subtlest bug in the deck -- keep it.
    (ASAP7SC7p5RVT, "NAND2xp67_ASAP7_75t_R"),
    (ASAP7SC7p5RVT, "A2O1A1Ixp33_ASAP7_75t_R"),
    (ASAP7SC7p5RVT, "DFFHQNx1_ASAP7_75t_R"),
    (ASAP7SC7p5RVT, "SDFHx1_ASAP7_75t_R"),
    (ASAP7SC7p5RVT, "ICGx1_ASAP7_75t_R"),
    # Edge cases: a tap cell and a decap have few or no devices.
    (ASAP7SC7p5RVT, "TAPCELL_ASAP7_75t_R"),
    (ASAP7SC7p5RVT, "DECAPx1_ASAP7_75t_R"),
    # Threshold-flavor splits: LVT is marked by 98/0, SLVT by 97/0.
    (ASAP7SC7p5LVT, "INVx1_ASAP7_75t_L"),
    (ASAP7SC7p5LVT, "NAND2x1_ASAP7_75t_L"),
    (ASAP7SC7p5SLVT, "INVx1_ASAP7_75t_SL"),
    (ASAP7SC7p5SLVT, "NAND2x1_ASAP7_75t_SL"),
]

# Representative folded cell. The ASAP7 CDL models this as two w=162.00n
# devices, but a 7.5-track row cannot fit 6 fins so the layout folds each into
# two 3-fin fingers with separate intermediate diffusion nodes. Tracked as an
# xfail so the limitation stays visible in test output.
FOLDED_CELL = (ASAP7SC7p5RVT, "AOI21x1_ASAP7_75t_R")

DATADIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "asap7_lvs")

needs_klayout = pytest.mark.skipif(
    shutil.which("klayout") is None,
    reason="klayout binary not installed; the LVS DSL needs it (the pip "
           "klayout package provides only the Python API)")


@pytest.fixture
def asap7():
    return ASAP7PDK()


@pytest.fixture
def deck(asap7):
    '''Resolves the LVS deck through the schema, not by hardcoded path.'''

    runsets = asap7.get("pdk", "lvs", "runsetfileset", "klayout", "lvs")
    assert runsets, "no klayout lvs runset registered for asap7"

    files = []
    for fileset in runsets:
        files.extend(asap7.get_file(fileset, "lvs"))
    assert len(files) == 1, f"expected exactly one lvs deck, got {files}"
    return files[0]


def extract_subckt(cdl, cell, dest):
    '''Writes the single .SUBCKT definition for `cell` out of `cdl`.'''

    lines = []
    capture = False
    with open(cdl) as fobj:
        for line in fobj:
            if line.startswith(".SUBCKT ") and line.split()[1] == cell:
                capture = True
            if capture:
                lines.append(line)
                if line.strip() == ".ENDS":
                    break

    assert lines, f"{cell} not found in {cdl}"
    with open(dest, "w") as fobj:
        fobj.writelines(lines)
    return dest


def run_lvs(deck, layout, topcell, schematic, tmp_path):
    '''Runs the deck and returns the CompletedProcess.'''

    return subprocess.run(
        ["klayout", "-b", "-r", deck,
         "-rd", f"input={os.path.abspath(layout)}",
         "-rd", f"topcell={topcell}",
         "-rd", f"schematic={os.path.abspath(schematic)}",
         "-rd", f"target_netlist={tmp_path / f'{topcell}.cir'}",
         "-rd", f"report={tmp_path / f'{topcell}.lvsdb'}",
         "-rd", "threads=2"],
        capture_output=True, text=True)


def compare_stdcell(deck, libcls, cell, tmp_path):
    '''Extracts `cell` from its library GDS and compares it to the shipped CDL.'''

    lib = libcls()
    gds = lib.get_file("models.physical", "gds")
    cdl = lib.get_file("models.lvs", "cdl")
    assert len(gds) == 1 and len(cdl) == 1, f"unexpected filesets for {lib.name}"

    schematic = extract_subckt(cdl[0], cell, tmp_path / f"{cell}.cdl")
    return run_lvs(deck, gds[0], cell, schematic, tmp_path)


#
# Registration -- runs everywhere, no tools required.
#

def test_lvs_runset_registered(asap7):
    assert asap7.get("pdk", "lvs", "runsetfileset", "klayout", "lvs") == ["klayout.lvs"]


def test_lvs_deck_resolves(deck):
    assert os.path.isfile(deck)
    assert deck.endswith(os.path.join("setup", "klayout", "lvs", "asap7.lvs"))


def test_lvs_deck_documents_its_parameters(deck):
    '''The -rd contract is the deck header, since there is no lvs_params key.'''

    with open(deck) as fobj:
        header = fobj.read()

    for param in ("input", "schematic", "topcell", "report",
                  "target_netlist", "threads"):
        assert f"#  {param}" in header, f"{param} not documented in deck header"


def test_article_files_present():
    for name in ("generate.py", "sramvt_inv.gds", "sramvt_inv.cdl"):
        assert os.path.isfile(os.path.join(DATADIR, name))


#
# Real LVS -- requires the klayout binary, skipped otherwise.
#

@needs_klayout
@pytest.mark.parametrize("libcls,cell", STDCELLS, ids=[c for _, c in STDCELLS])
def test_lvs_stdcell(deck, libcls, cell, tmp_path):
    proc = compare_stdcell(deck, libcls, cell, tmp_path)

    assert "LVS_RESULT: MATCH" in proc.stdout, \
        f"{cell} did not compare clean:\n{proc.stdout}\n{proc.stderr}"
    assert proc.returncode == 0, f"{cell} exited {proc.returncode}"


@needs_klayout
def test_lvs_sramvt_article(deck, tmp_path):
    '''The only coverage of the SRAMVT (110/0) device flavor.'''

    proc = run_lvs(deck,
                   os.path.join(DATADIR, "sramvt_inv.gds"),
                   "sramvt_inv",
                   os.path.join(DATADIR, "sramvt_inv.cdl"),
                   tmp_path)

    assert "LVS_RESULT: MATCH" in proc.stdout, \
        f"sram-vt article did not compare clean:\n{proc.stdout}\n{proc.stderr}"
    assert proc.returncode == 0

    netlist = (tmp_path / "sramvt_inv.cir").read_text()
    assert "nmos_sram" in netlist
    assert "pmos_sram" in netlist


@needs_klayout
def test_lvs_reports_mismatch_as_failure(deck, tmp_path):
    '''A mismatch must exit non-zero, so a harness need not parse the lvsdb.'''

    lib = ASAP7SC7p5RVT()
    gds = lib.get_file("models.physical", "gds")[0]

    # Same cell name and pins as the real inverter, but the pmos is missing.
    # Keeping the name is what lets the compare actually run: a name mismatch
    # aborts earlier with "can't find a schematic counterpart".
    schematic = tmp_path / "wrong.cdl"
    schematic.write_text(
        ".SUBCKT INVx1_ASAP7_75t_R A VDD VSS Y\n"
        "MM0 Y A VSS VSS nmos_rvt w=81.0n l=20n nfin=3\n"
        ".ENDS\n")

    proc = run_lvs(deck, gds, "INVx1_ASAP7_75t_R", schematic, tmp_path)

    assert "LVS_RESULT: MISMATCH" in proc.stdout, \
        f"expected a mismatch:\n{proc.stdout}\n{proc.stderr}"
    assert proc.returncode != 0


@needs_klayout
@pytest.mark.xfail(reason="folded multi-finger device: the CDL models one "
                          "w=162.00n device where the layout draws two 3-fin "
                          "fingers with separate intermediate nodes",
                   strict=True)
def test_lvs_folded_cell(deck, tmp_path):
    libcls, cell = FOLDED_CELL
    proc = compare_stdcell(deck, libcls, cell, tmp_path)
    assert "LVS_RESULT: MATCH" in proc.stdout


#
# Test article reproducibility -- needs only the klayout Python module.
#

def test_sramvt_article_is_reproducible():
    pytest.importorskip("klayout.db",
                        reason="klayout python module needed to rebuild the article")

    # sys.executable, not "python3": the generator needs the klayout module from
    # the environment running the tests, which need not be the one on PATH.
    proc = subprocess.run(
        [sys.executable, os.path.join(DATADIR, "generate.py"), "--check"],
        capture_output=True, text=True)

    assert proc.returncode == 0, \
        f"committed sramvt_inv.gds has drifted from generate.py:\n{proc.stderr}"
