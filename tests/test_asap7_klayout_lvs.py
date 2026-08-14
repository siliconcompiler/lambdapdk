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


def run_lvs(deck, layout, topcell, schematic, tmp_path, *extra):
    '''Runs the deck and returns the CompletedProcess.

    `extra` is appended verbatim, for additional '-rd name=value' pairs.
    '''

    return subprocess.run(
        ["klayout", "-b", "-r", deck,
         "-rd", f"input={os.path.abspath(layout)}",
         "-rd", f"topcell={topcell}",
         "-rd", f"schematic={os.path.abspath(schematic)}",
         "-rd", f"target_netlist={tmp_path / f'{topcell}.cir'}",
         "-rd", f"report={tmp_path / f'{topcell}.lvsdb'}",
         "-rd", "threads=2",
         *extra],
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
# Hierarchical test article. Built at test time from the shipped library GDS so
# that no library geometry is duplicated into the repository.
#

ROW_TOPCELL = "lvs_row"

# ASAP7 7.5-track geometry, in the library's 0.25nm database units: the power
# rails are the only M1 boxes drawn from x=0, and they are what fixes the cell
# pitch, so the row is built by abutting instances on that width.
RAIL_TOP = 1080
PIN_PAD = 20


def build_row(libcls, cell, count, tmp_path, route=False, miswire=False):
    '''Builds a row of `count` abutted `cell` instances plus its CDL.

    With route=False every signal pin of every instance is brought out as a
    top-level pin named "<pin><instance>"; the compare then checks the pin
    identification and the rail abutment. With route=True the instances are
    chained Y -> A, which additionally checks a real M1 route; it therefore only
    applies to a cell with exactly the pins A, Y, VDD and VSS.

    miswire=True writes a CDL that ties every instance input to the row input
    instead of to the route, i.e. a netlist the layout does not implement.

    Returns (gds, cdl, topcell).
    '''

    db = pytest.importorskip("klayout.db",
                             reason="klayout python module needed to build the row article")

    lib = libcls()
    layout = db.Layout()
    layout.read(lib.get_file("models.physical", "gds")[0])
    src = layout.cell(cell)
    assert src, f"{cell} not in the library GDS"

    m1 = layout.layer(19, 0)
    m1_lbl = layout.layer(19, 251)

    pitch = max([shape.box.right for shape in src.shapes(m1).each()
                 if shape.is_box() and shape.box.left == 0] or [0])
    assert pitch > 0, f"no power rail found on 19/0 in {cell}"

    pins = {shape.text.string: (shape.text.trans.disp.x, shape.text.trans.disp.y)
            for shape in src.shapes(m1_lbl).each() if shape.is_text()}
    signals = {name: xy for name, xy in pins.items() if name not in ("VDD", "VSS")}
    assert signals, f"no signal pin labels on 19/251 in {cell}"
    if route:
        assert set(signals) == {"A", "Y"}, \
            f"route=True needs a single-input cell, {cell} has {sorted(signals)}"

    top = layout.create_cell(ROW_TOPCELL)

    def add_pin(name, x, y):
        top.shapes(m1).insert(db.Box(x - PIN_PAD, y - PIN_PAD, x + PIN_PAD, y + PIN_PAD))
        top.shapes(m1_lbl).insert(db.Text(name, db.Trans(db.Vector(x, y))))

    for inst in range(count):
        offset = inst * pitch
        top.insert(db.CellInstArray(src.cell_index(), db.Trans(db.Vector(offset, 0))))

        if not route:
            for name, (x, y) in signals.items():
                add_pin(f"{name}{inst}", x + offset, y)
            continue

        ax, ay = signals["A"]
        yx, yy = signals["Y"]
        if inst == 0:
            add_pin("A", ax, ay)
        else:
            # M1 jumper from the previous instance's Y to this instance's A. Drawn
            # in the load pin's row band, which is where both pin shapes are.
            top.shapes(m1).insert(db.Box(yx + offset - pitch, ay - PIN_PAD,
                                         ax + offset, ay + PIN_PAD))
        if inst == count - 1:
            add_pin("Y", yx + offset, yy)

    # The rails run the length of the row; label either end of one of them.
    add_pin("VDD", PIN_PAD, RAIL_TOP)
    add_pin("VSS", PIN_PAD, 0)

    gds = tmp_path / f"{ROW_TOPCELL}.gds"
    layout.write(str(gds))

    cdl = tmp_path / f"{ROW_TOPCELL}.cdl"
    cell_cdl = extract_subckt(lib.get_file("models.lvs", "cdl")[0], cell,
                              tmp_path / f"{cell}.cdl")
    with open(cell_cdl) as fobj:
        body = fobj.readlines()
    order = body[0].split()[2:]

    if route:
        ports = ["A", "VDD", "VSS", "Y"]
        nets = [{"A": "A" if inst == 0 else f"net{inst}",
                 "Y": "Y" if inst == count - 1 else f"net{inst + 1}"}
                for inst in range(count)]
        if miswire:
            for net in nets:
                net["A"] = "A"
    else:
        ports = [f"{name}{inst}" for inst in range(count) for name in signals] + \
                ["VDD", "VSS"]
        nets = [{name: f"{name}{inst}" for name in signals} for inst in range(count)]

    with open(cdl, "w") as fobj:
        fobj.writelines(body)
        fobj.write(f".SUBCKT {ROW_TOPCELL} {' '.join(ports)}\n")
        for inst in range(count):
            conn = [pin if pin in ("VDD", "VSS") else nets[inst][pin] for pin in order]
            fobj.write(f"XI{inst} {' '.join(conn)} {cell}\n")
        fobj.write(".ENDS\n")

    return gds, cdl, ROW_TOPCELL


#
# Pin geometry above M1. A standard cell carries its pin labels on M1 only, so
# nothing in the library exercises the rest of the label stack; a hardened block
# in an abutting design does the opposite, putting every port on the upper
# metals. This article is that shape, in miniature.
#

# Bottom-up from the M1 pin shape to the M4 pad, alternating metal and via.
UPPER_PIN_STACK = [(19, 0), (21, 0), (20, 0), (25, 0), (30, 0), (35, 0), (40, 0)]
UPPER_PIN_LABEL = (40, 251)


def build_upper_metal_row(libcls, cell, tmp_path, swap_inputs=False):
    '''Builds two abutted `cell` instances whose signal ports are M4 pins.

    Each instance's A and Y are carried from the cell's own M1 pin shape up a via
    stack to an M4 pad, and the port name is a text object on 40/251 -- nothing
    on M1 names them. The rails stay labelled on M1, as they are in a real block.

    swap_inputs=True writes a CDL that exchanges the two inputs, i.e. a netlist
    the layout does not implement. The two are distinguishable only if the pins
    carry names: the instances are identical, so with the port names stripped the
    swapped netlist is isomorphic to the correct one and KLayout -- which matches
    unnamed pins permissively -- reports a false clean.

    Returns (gds, cdl, topcell).
    '''

    db = pytest.importorskip("klayout.db",
                             reason="klayout python module needed to build the row article")

    lib = libcls()
    layout = db.Layout()
    layout.read(lib.get_file("models.physical", "gds")[0])
    src = layout.cell(cell)
    assert src, f"{cell} not in the library GDS"

    m1 = layout.layer(19, 0)
    m1_lbl = layout.layer(19, 251)
    stack = [layout.layer(*spec) for spec in UPPER_PIN_STACK]
    top_lbl = layout.layer(*UPPER_PIN_LABEL)

    pitch = max([shape.box.right for shape in src.shapes(m1).each()
                 if shape.is_box() and shape.box.left == 0] or [0])
    assert pitch > 0, f"no power rail found on 19/0 in {cell}"

    pins = {shape.text.string: (shape.text.trans.disp.x, shape.text.trans.disp.y)
            for shape in src.shapes(m1_lbl).each() if shape.is_text()}
    assert set(pins) >= {"A", "Y"}, f"{cell} has no A/Y pins: {sorted(pins)}"

    top = layout.create_cell(ROW_TOPCELL)

    for inst in range(2):
        offset = inst * pitch
        top.insert(db.CellInstArray(src.cell_index(), db.Trans(db.Vector(offset, 0))))

        for name in ("A", "Y"):
            x, y = pins[name]
            x += offset
            # One box per layer at the same spot. LVS is connectivity, not DRC,
            # so full overlap is all the stack needs to be a conductor.
            box = db.Box(x - PIN_PAD, y - PIN_PAD, x + PIN_PAD, y + PIN_PAD)
            for layer in stack:
                top.shapes(layer).insert(box)
            top.shapes(top_lbl).insert(db.Text(f"{name}{inst}",
                                               db.Trans(db.Vector(x, y))))

    # The rails are labelled on M1, the way a block's power pins really are.
    for name, y in (("VDD", RAIL_TOP), ("VSS", 0)):
        top.shapes(m1).insert(db.Box(0, y - PIN_PAD, 2 * PIN_PAD, y + PIN_PAD))
        top.shapes(m1_lbl).insert(db.Text(name, db.Trans(db.Vector(PIN_PAD, y))))

    gds = tmp_path / f"{ROW_TOPCELL}_m4.gds"
    layout.write(str(gds))

    cell_cdl = extract_subckt(lib.get_file("models.lvs", "cdl")[0], cell,
                              tmp_path / f"{cell}.cdl")
    with open(cell_cdl) as fobj:
        body = fobj.readlines()
    order = body[0].split()[2:]

    inputs = ["A1", "A0"] if swap_inputs else ["A0", "A1"]
    nets = [{"A": inputs[inst], "Y": f"Y{inst}"} for inst in range(2)]

    cdl = tmp_path / f"{ROW_TOPCELL}_m4.cdl"
    with open(cdl, "w") as fobj:
        fobj.writelines(body)
        fobj.write(f".SUBCKT {ROW_TOPCELL} A0 Y0 A1 Y1 VDD VSS\n")
        for inst in range(2):
            conn = [pin if pin in ("VDD", "VSS") else nets[inst][pin] for pin in order]
            fobj.write(f"XI{inst} {' '.join(conn)} {cell}\n")
        fobj.write(".ENDS\n")

    return gds, cdl, ROW_TOPCELL


#
# Registration -- runs everywhere, no tools required.
#

def test_lvs_runset_registered(asap7):
    assert asap7.get("pdk", "lvs", "runsetfileset", "klayout", "lvs") == ["klayout.lvs"]


def test_lvs_blackbox_runset_registered(asap7):
    '''Both deck names are the same deck, differing only in their parameters.'''

    assert asap7.get("pdk", "lvs", "runsetfileset", "klayout", "lvs_blackbox") == \
        ["klayout.lvs"]


def test_lvs_params_registered(asap7):
    '''The -rd contract published as metadata for a flow to consume.'''

    params = asap7.get("tool", "klayout", "lvs_params")

    for deck in ("lvs", "lvs_blackbox"):
        for param in ("input=<input>", "topcell=<topcell>", "schematic=<schematic>",
                      "target_netlist=<target_netlist>", "report=<report>",
                      "threads=<threads>", "run_mode=deep"):
            assert (deck, param) in params, f"{deck} is missing {param}"

    assert ("lvs_blackbox", "blackbox=*_ASAP7_75t_*") in params

    # The default deck must not black-box anything, or a plain run would silently
    # stop checking cell internals.
    assert not [param for deck, param in params
                if deck == "lvs" and param.startswith("blackbox=")]


def test_lvs_deck_resolves(deck):
    assert os.path.isfile(deck)
    assert deck.endswith(os.path.join("setup", "klayout", "lvs", "asap7.lvs"))


def test_lvs_deck_documents_its_parameters(deck):
    '''The -rd contract is the deck header, since there is no lvs_params key.'''

    with open(deck) as fobj:
        header = fobj.read()

    for param in ("input", "schematic", "topcell", "report",
                  "target_netlist", "threads", "run_mode", "blackbox"):
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


#
# Hierarchy. A standard cell as the top cell is the easy case: the well and the
# rail are both labelled inside the cell. One level up they are not, which is
# what the well global in the deck's connectivity section is there for.
#

BLACKBOX_ALL_STDCELLS = "-rd", "blackbox=*_ASAP7_75t_*"


@needs_klayout
def test_lvs_hierarchical_row(deck, tmp_path):
    '''Two routed instances one level down. Regression guard for the well tie.

    Without connect_global(nwell, "VDD") this fails during extraction with
    "[must-connect] ... Must-connect nets VDD ... are not connected", because
    above the standard cell the well net carries no label to tie it by.
    '''

    gds, cdl, topcell = build_row(ASAP7SC7p5RVT, "INVx1_ASAP7_75t_R", 2, tmp_path,
                                  route=True)
    proc = run_lvs(deck, gds, topcell, cdl, tmp_path)

    assert "must-connect" not in proc.stderr, \
        f"hierarchical extraction failed:\n{proc.stderr}"
    assert "LVS_RESULT: MATCH" in proc.stdout, \
        f"routed row did not compare clean:\n{proc.stdout}\n{proc.stderr}"
    assert proc.returncode == 0


@needs_klayout
def test_lvs_hierarchical_row_detects_miswire(deck, tmp_path):
    '''The same layout against a netlist it does not implement.'''

    gds, _, topcell = build_row(ASAP7SC7p5RVT, "INVx1_ASAP7_75t_R", 2, tmp_path,
                                route=True)
    _, cdl, _ = build_row(ASAP7SC7p5RVT, "INVx1_ASAP7_75t_R", 2, tmp_path,
                          route=True, miswire=True)
    proc = run_lvs(deck, gds, topcell, cdl, tmp_path)

    assert "LVS_RESULT: MISMATCH" in proc.stdout, \
        f"expected a mismatch:\n{proc.stdout}\n{proc.stderr}"
    assert proc.returncode != 0


#
# Pin labels above M1. The deck connects every <metal>/251 label layer, not just
# M1's, because a block's ports are wherever its pin geometry lands.
#

@needs_klayout
def test_lvs_reads_pin_labels_above_m1(deck, tmp_path):
    '''Ports on M4 must reach the netlist by name.

    With only connect(m1, m1_lbl) in the deck these four pins are nameless: the
    extracted netlist keeps the two M1-labelled rails and nothing else, so a
    block whose ports are all above M1 loses its pins outright.
    '''

    gds, cdl, topcell = build_upper_metal_row(ASAP7SC7p5RVT, "INVx1_ASAP7_75t_R",
                                              tmp_path)
    proc = run_lvs(deck, gds, topcell, cdl, tmp_path)

    assert "LVS_RESULT: MATCH" in proc.stdout, \
        f"M4-pinned row did not compare clean:\n{proc.stdout}\n{proc.stderr}"
    assert proc.returncode == 0

    # The decisive assertion, read off the layout side of the LVS database: the
    # four M4 port names, which exist nowhere but 40/251. The extracted SPICE is
    # no good for this -- KLayout's writer numbers pins rather than naming them,
    # in that netlist even the M1-labelled rails come out as "5" and "6".
    db = pytest.importorskip("klayout.db")
    lvsdb = db.LayoutVsSchematic()
    lvsdb.read(str(tmp_path / f"{topcell}.lvsdb"))
    circuit = lvsdb.netlist().circuit_by_name(topcell)
    assert circuit, f"no {topcell} circuit in the extracted netlist"

    pins = {pin.name() for pin in circuit.each_pin()}
    assert pins == {"A0", "Y0", "A1", "Y1", "VDD", "VSS"}, \
        f"expected the M4 pin names on the layout side, got {sorted(pins)}"


@needs_klayout
def test_lvs_upper_metal_pins_are_matched_by_name(deck, tmp_path):
    '''The soundness half: unnamed pins match permissively.

    The layout is the same two inverters either way; only the port names tell the
    correct netlist from the one with its inputs exchanged. A deck that does not
    read 40/251 leaves those pins unnamed, and KLayout treats unnamed pins as
    equivalent -- so it reports this swapped netlist as a match.
    '''

    gds, _, topcell = build_upper_metal_row(ASAP7SC7p5RVT, "INVx1_ASAP7_75t_R",
                                            tmp_path)
    _, cdl, _ = build_upper_metal_row(ASAP7SC7p5RVT, "INVx1_ASAP7_75t_R",
                                      tmp_path, swap_inputs=True)
    proc = run_lvs(deck, gds, topcell, cdl, tmp_path)

    assert "LVS_RESULT: MISMATCH" in proc.stdout, \
        f"swapped M4 ports must not match:\n{proc.stdout}\n{proc.stderr}"
    assert proc.returncode != 0


#
# Black-boxing.
#

@needs_klayout
def test_lvs_folded_cell_in_hierarchy(deck, tmp_path):
    '''The case for the blackbox parameter, measured.

    AOI21x1 is one of the 17 cells whose CDL is not structurally isomorphic to
    its layout, so a hierarchical compare fails on the cell even though the row
    is wired correctly. Black-boxing reduces it to its pins and the row compares.
    '''

    gds, cdl, topcell = build_row(ASAP7SC7p5RVT, FOLDED_CELL[1], 2, tmp_path)

    plain = run_lvs(deck, gds, topcell, cdl, tmp_path)
    assert "LVS_RESULT: MISMATCH" in plain.stdout, \
        f"expected the folded cell to sink the compare:\n{plain.stdout}\n{plain.stderr}"

    boxed = run_lvs(deck, gds, topcell, cdl, tmp_path, *BLACKBOX_ALL_STDCELLS)
    assert "LVS_RESULT: MATCH" in boxed.stdout, \
        f"black-boxed row did not compare clean:\n{boxed.stdout}\n{boxed.stderr}"
    assert boxed.returncode == 0

    # A black-boxed result is a weaker claim, so the log has to say so.
    assert "LVS_BLACKBOX: *_ASAP7_75t_*" in boxed.stdout
    assert "LVS_BLACKBOX_NOTE:" in boxed.stdout

    netlist = (tmp_path / f"{topcell}.cir").read_text()
    assert FOLDED_CELL[1] in netlist, "the black-boxed cell should still be instantiated"
    assert "nmos_rvt" not in netlist, "black-boxed cells should contribute no devices"


@needs_klayout
def test_lvs_blackboxed_still_detects_miswire(deck, tmp_path):
    '''Black-boxing must not weaken the check it is there to make.'''

    gds, _, topcell = build_row(ASAP7SC7p5RVT, "INVx1_ASAP7_75t_R", 2, tmp_path,
                                route=True)
    _, cdl, _ = build_row(ASAP7SC7p5RVT, "INVx1_ASAP7_75t_R", 2, tmp_path,
                          route=True, miswire=True)
    proc = run_lvs(deck, gds, topcell, cdl, tmp_path, *BLACKBOX_ALL_STDCELLS)

    assert "LVS_RESULT: MISMATCH" in proc.stdout, \
        f"a miswired route must still be caught:\n{proc.stdout}\n{proc.stderr}"
    assert proc.returncode != 0


@needs_klayout
def test_lvs_blackbox_rejects_top_cell_glob(deck, tmp_path):
    '''Blanking the top cell would compare nothing and pass. It must be refused.'''

    gds, cdl, topcell = build_row(ASAP7SC7p5RVT, "INVx1_ASAP7_75t_R", 2, tmp_path,
                                  route=True)
    proc = run_lvs(deck, gds, topcell, cdl, tmp_path, "-rd", f"blackbox={topcell[:3]}*")

    assert proc.returncode != 0
    assert "matches the top cell" in proc.stderr, proc.stderr
    assert "LVS_RESULT" not in proc.stdout, "the compare must not have run"


@needs_klayout
def test_lvs_run_mode_rejects_unknown(deck, tmp_path):
    proc = run_lvs(deck,
                   os.path.join(DATADIR, "sramvt_inv.gds"), "sramvt_inv",
                   os.path.join(DATADIR, "sramvt_inv.cdl"), tmp_path,
                   "-rd", "run_mode=bogus")

    assert proc.returncode != 0
    assert "unknown run_mode 'bogus'" in proc.stderr, proc.stderr


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
