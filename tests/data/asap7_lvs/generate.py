#!/usr/bin/env python3
# Copyright 2026 ZeroASIC Corp
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
'''
Generates the SRAM-VT test article for the ASAP7 KLayout LVS runset.

The three shipped ASAP7 standard cell libraries only instantiate the rvt, lvt
and slvt device flavors, so nothing in the repository exercises the SRAMVT
(110/0) branch of the LVS deck. This builds a minimal inverter drawn on that
marker, paired with the reference netlist in sramvt_inv.cdl.

Usage:
    python3 generate.py            # (re)write sramvt_inv.gds
    python3 generate.py --check    # verify the committed GDS is reproducible

Runs against either the klayout Python module (``pip install klayout``) or the
standalone binary. ``klayout -b`` does not forward argv, so under the binary the
options are passed as globals instead:

    klayout -b -r generate.py
    klayout -b -r generate.py -rd check=1
'''

import argparse
import os
import sys

try:
    import klayout.db as db
except ImportError:  # running under `klayout -b -r`
    import pya as db

# ASAP7 draws at 4x scale; 0.25nm database units undo it, so coordinates below
# are real micrometers. This matches base/setup/klayout/asap7.lyt.
DBU = 0.00025

CELL = "sramvt_inv"

# GDS layers, from the ASAP7 DRM Table 2.1.1 and base/setup/klayout/asap7.lyp.
WELL = (1, 0)
WELL_PIN = (1, 251)
PSUB_PIN = (3, 251)
GATE = (7, 0)
GCUT = (10, 0)
ACTIVE = (11, 0)
NSELECT = (12, 0)
PSELECT = (13, 0)
LIG = (16, 0)
LISD = (17, 0)
V0 = (18, 0)
M1 = (19, 0)
M1_PIN = (19, 251)
SDT = (88, 0)
SRAMVT = (110, 0)
BOUNDARY = (100, 0)

CELL_W = 0.162
CELL_H = 0.270


def build():
    '''Builds the article layout and returns the klayout Layout object.'''

    layout = db.Layout()
    layout.dbu = DBU
    top = layout.create_cell(CELL)

    def layer(spec):
        return layout.layer(*spec)

    def box(spec, x1, y1, x2, y2):
        top.shapes(layer(spec)).insert(db.DBox(x1, y1, x2, y2))

    def text(spec, string, x, y):
        top.shapes(layer(spec)).insert(db.DText(string, x, y))

    box(BOUNDARY, 0, 0, CELL_W, CELL_H)

    # Wells and implants: nmos in the lower half, pmos in the upper half.
    box(WELL, 0, 0.135, CELL_W, CELL_H)
    box(NSELECT, 0, 0, CELL_W, 0.135)
    box(PSELECT, 0, 0.135, CELL_W, CELL_H)

    # The whole cell is SRAM-Vt, which is what this article exists to exercise.
    box(SRAMVT, 0, 0, CELL_W, CELL_H)

    # Two 3-fin active islands (81nm tall => w=81.0n in the reference netlist).
    box(ACTIVE, 0.046, 0.027, 0.116, 0.108)
    box(ACTIVE, 0.046, 0.162, 0.116, 0.243)

    # One 20nm gate line crossing both islands (=> l=20n), with GCUT severing
    # the ends so the gate does not short to the power rails.
    box(GATE, 0.071, -0.005, 0.091, 0.2755)
    box(GCUT, 0, -0.022, CELL_W, 0.022)
    box(GCUT, 0, 0.248, CELL_W, 0.292)

    # Source/drain trench, then the local interconnect over it. The source
    # shapes deliberately reach the rails so the sources tie to VSS and VDD.
    for y1, y2 in ((0.027, 0.108), (0.162, 0.243)):
        box(SDT, 0.042, y1, 0.066, y2)
        box(SDT, 0.096, y1, 0.120, y2)
    box(LISD, 0.042, 0.000, 0.066, 0.108)
    box(LISD, 0.096, 0.027, 0.120, 0.108)
    box(LISD, 0.042, 0.162, 0.066, 0.270)
    box(LISD, 0.096, 0.162, 0.120, 0.243)

    # Local interconnect: power rails plus the gate contact.
    box(LIG, 0, -0.008, CELL_W, 0.008)
    box(LIG, 0, 0.262, CELL_W, 0.278)
    box(LIG, 0.054, 0.124, 0.093, 0.146)

    for x, y in ((0.045, -0.009), (0.099, 0.027), (0.055, 0.126),
                 (0.099, 0.225), (0.045, 0.261), (0.099, 0.261)):
        box(V0, x, y, x + 0.018, y + 0.018)

    # M1: VSS rail, A pin, Y pin, VDD rail.
    box(M1, 0, -0.009, CELL_W, 0.009)
    box(M1, 0.018, 0.027, 0.078, 0.243)
    box(M1, 0.094, 0.027, 0.144, 0.243)
    box(M1, 0, 0.261, CELL_W, 0.279)

    # Port names live on the M1 pin layer as text; 19/2 is unused in ASAP7.
    text(M1_PIN, "VSS", 0.029, 0.000)
    text(M1_PIN, "VDD", 0.036, 0.267)
    text(M1_PIN, "A", 0.047, 0.136)
    text(M1_PIN, "Y", 0.135, 0.114)

    # Well and substrate tap substitutes, tied by name (see base/README.md).
    text(WELL_PIN, "VDD", 0.154, 0.187)
    text(PSUB_PIN, "VSS", 0.206, 0.080)

    return layout


def parse_options():
    '''
    Resolves options from argv, or from -rd globals when run by `klayout -b`.

    `klayout -b -r script.py` does not forward argv, so the binary path reads
    `check` and `output` out of the interpreter globals instead.
    '''

    injected = globals()
    if "check" in injected or "output" in injected:
        return argparse.Namespace(check=bool(injected.get("check")),
                                  output=injected.get("output"))

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true",
                        help="verify the committed GDS matches this generator")
    parser.add_argument("-o", "--output",
                        help="output path (default: sramvt_inv.gds beside this script)")
    # Under `klayout -b` argv holds klayout's own options, so ignore extras.
    known, _ = parser.parse_known_args()
    return known


def main():
    args = parse_options()

    default = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{CELL}.gds")
    layout = build()

    if not args.check:
        out = args.output or default
        layout.write(out)
        print(f"wrote {out}")
        return 0

    committed = args.output or default
    if not os.path.isfile(committed):
        print(f"ERROR: {committed} does not exist", file=sys.stderr)
        return 1

    if not layouts_equivalent(layout, committed):
        print(f"ERROR: {committed} does not match this generator; "
              f"re-run without --check to regenerate", file=sys.stderr)
        return 1

    print(f"{committed} matches this generator")
    return 0


def layouts_equivalent(layout, path):
    '''
    Compares a generated layout against one on disk, geometrically.

    Compares per-layer shapes rather than bytes, so that GDS timestamps and
    writer-version differences do not cause spurious failures.
    '''

    other = db.Layout()
    other.read(path)

    # GDS stores the database unit as a float, so it does not round-trip
    # exactly: 0.00025 comes back as 0.00025000000000000006.
    if abs(layout.dbu - other.dbu) > 1e-15:
        return False

    cell = layout.cell(CELL)
    other_cell = other.cell(CELL)
    if cell is None or other_cell is None:
        return False

    def inventory(ly, cl):
        found = {}
        for index in ly.layer_indexes():
            info = ly.get_info(index)
            key = (info.layer, info.datatype)
            region = db.Region()
            texts = []
            for shape in cl.each_shape(index):
                if shape.is_text():
                    texts.append((shape.text.string,
                                  shape.text.x, shape.text.y))
                else:
                    region.insert(shape.polygon)
            region.merge()
            if not region.is_empty() or texts:
                found[key] = (region, sorted(texts))
        return found

    mine = inventory(layout, cell)
    theirs = inventory(other, other_cell)

    if set(mine) != set(theirs):
        return False

    for key, (region, texts) in mine.items():
        other_region, other_texts = theirs[key]
        if texts != other_texts:
            return False
        if not (region ^ other_region).is_empty():
            return False

    return True


if __name__ == "__main__":
    sys.exit(main())
