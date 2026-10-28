"""Declare the bond pad landing area of the sky130 IO cells as pin geometry.

The vendor LEF for the sky130 IO pads only declares a shrunken piece of the
bond pad plate as the supply/signal pin and leaves the rest of it inside OBS.
The GDS disagrees: every pad carries a 65.4um x 75.4um plate on met4/met5
labelled ``<PIN>_PAD``, which is exactly the footprint of
``sky130_ef_io__bare_pad``.  A bond pad placed on the plate therefore always
lands on what the abstract calls an obstruction, which any short check reads
as the supply net shorting to the pad instance.

This rewrites the LEF so the plate is what the layout says it is: pin geometry
of the pad it belongs to, removed from OBS.  The plate bounding box is used
rather than the chamfered outline in the GDS, matching how ``bare_pad`` itself
abstracts the same area.

The defect is in the upstream artifact, not in lambdapdk's copy of it: at
open_pdks ``1689ac3`` exactly one of the 39 macros in ``sky130_ef_io.lef`` --
``sky130_ef_io__bare_pad`` -- declares the plate as pin geometry.  So this runs
against an upstream-sourced tree and the patched LEF is vendored, the one
file ``sky130io`` cannot take by reference.  Not yet reported upstream; see
``lambdapdk/sky130/PATCHES.md``.

Run from the repository root; KLayout supplies the GDS reader and the polygon
booleans::

    klayout -b -r scripts/patch_sky130io_bondpads.py

By default it reads and rewrites the vendored LEF in place, taking the GDS from
the same directory.  To re-derive it from an unpacked upstream dataroot,
point it at one -- ``lef`` is read and ``out`` is written, so the vendored file
is only touched by ``out``::

    klayout -b -r scripts/patch_sky130io_bondpads.py \\
        -rd lef=$PDK/sky130A/libs.ref/sky130_fd_io/lef/sky130_ef_io.lef \\
        -rd gds_dir=$PDK/sky130A/libs.ref/sky130_fd_io/gds \\
        -rd out=lambdapdk/sky130/libs/sky130io/lef/sky130_ef_io.lef
"""

import re

import pya


IO_DIR = "lambdapdk/sky130/libs/sky130io"

# ``-rd name=value`` on the KLayout command line defines these as globals, so a
# plain lookup is what tells an override from the default.
LEF = globals().get("lef", f"{IO_DIR}/lef/sky130_ef_io.lef")
OUT = globals().get("out", LEF)
GDS_DIR = globals().get("gds_dir", f"{IO_DIR}/gds")
GDS = [f"{GDS_DIR}/sky130_fd_io.gds", f"{GDS_DIR}/sky130_ef_io.gds"]

# The bond plate is this size on every pad, which is what tells it apart from
# the supply rails that also show up as large met5 shapes.
PLATE_SIZE = (65.400, 75.400)
PLATE_TOLERANCE = 0.001

MET4 = (71, 20)
MET5 = (72, 20)

# Layers the plate's label may sit on, searched together.  open_pdks wrote the
# name to both met5.pin and met5.label up to the 2023 vintage this library was
# first vendored from; at 1689ac3 only met5.label carries it, so keying on
# met5.pin alone finds nothing on a current artifact.
MET5_LABELS = ((72, 16), (72, 5))

# Macros that only exist in the LEF take their plate from the macro they wrap,
# shifted by the offset between the two PAD pins.
DERIVED = {"sky130_ef_io__gpiov2_pad_wrapped": ("sky130_ef_io__gpiov2_pad", "PAD")}

# The bond pad itself is the plate, so it has nothing to reattribute.
SKIP = {"sky130_ef_io__bare_pad"}


def macro_pins(macro):
    """Returns the set of pin names a macro body declares."""
    return set(re.findall(r"^  PIN (\S+)$", macro, re.M))


def find_plates(layout, macros):
    """Returns {macro: (pin, plate)} for every macro carrying a bond plate."""
    dbu = layout.dbu
    met5 = layout.layer(*MET5)
    label_layers = [layout.layer(*spec) for spec in MET5_LABELS]

    plates = {}
    for name in sorted(set(macros) - SKIP):
        cell = layout.cell(name)
        if cell is None:
            continue
        pins = macro_pins(macros[name])
        region = pya.Region(cell.begin_shapes_rec(met5))
        region.merge()
        for polygon in region.each():
            box = polygon.bbox().to_dtype(dbu)
            if abs(box.width() - PLATE_SIZE[0]) > PLATE_TOLERANCE:
                continue
            if abs(box.height() - PLATE_SIZE[1]) > PLATE_TOLERANCE:
                continue

            pin = plate_pin(cell, label_layers, box, dbu, pins)
            if pin is None:
                raise RuntimeError(f"{cell.name}: bond plate {box} carries no label "
                                   "naming a pin of the macro")
            if cell.name in plates:
                raise RuntimeError(f"{cell.name}: more than one bond plate")
            plates[cell.name] = (pin, box)

    return plates


def plate_pin(cell, layers, box, dbu, pins):
    """Returns the pin the plate belongs to, from the label sitting inside it.

    Every layer in ``layers`` is searched and the names pooled, since which of
    them carries the label depends on the artifact's vintage -- see
    :data:`MET5_LABELS`.  Pooling them can turn up more than one name, so a
    label counts only if it resolves to a pin the macro actually declares:

    * verbatim, which is how a current artifact names it -- ``vccd_hvc_pad``
      declares both ``VCCD_PAD`` and ``VCCD``, and the plate belongs to the
      former;
    * with the ``_PAD`` suffix removed, which is how the 2023 vintage named it,
      where the same macro declared only ``VCCD``.

    Anything resolving to no pin is a marker that happens to sit on the plate
    (``P_PAD``, on the supply pads) and is ignored.  Returns None unless exactly
    one label survives, so an ambiguous plate stops the run rather than
    guessing.
    """
    candidates = set()
    for layer in layers:
        shapes = cell.begin_shapes_rec(layer)
        while not shapes.at_end():
            shape = shapes.shape()
            if shape.is_text():
                text = shape.text.transformed(shapes.trans())
                if box.contains(pya.DPoint(text.x * dbu, text.y * dbu)):
                    candidates.add(shape.text.string)
            shapes.next()

    resolved = set()
    for name in candidates:
        if name in pins:
            resolved.add(name)
        elif name.endswith("_PAD") and name[: -len("_PAD")] in pins:
            resolved.add(name[: -len("_PAD")])

    return resolved.pop() if len(resolved) == 1 else None


def pin_rect(macro, pin, layer):
    """Returns the first rect of ``pin`` on ``layer``, used to align a wrapper."""
    body = re.search(rf"^  PIN {re.escape(pin)}$(.*?)^  END {re.escape(pin)}$",
                     macro, re.S | re.M)
    current = None
    for line in body.group(1).splitlines():
        line = line.strip()
        if line.startswith("LAYER"):
            current = line.split()[1].rstrip(";").strip()
        elif line.startswith("RECT") and current == layer:
            x0, y0, x1, y1 = (float(v) for v in line.replace(";", "").split()[1:5])
            return pya.DBox(x0, y0, x1, y1)
    return None


def add_plate_ports(macro, pin, plate):
    """Adds the plate to ``pin`` as met4 and met5 geometry."""
    rect = f"RECT {plate.left:.3f} {plate.bottom:.3f} {plate.right:.3f} {plate.top:.3f} ;"
    if rect in macro:
        return macro, False

    ports = "".join(
        f"    PORT\n      LAYER {layer} ;\n        {rect}\n    END\n"
        for layer in ("met4", "met5")
    )
    end = f"  END {pin}\n"
    head, sep, tail = macro.rpartition(end)
    if not sep:
        raise RuntimeError(f"pin {pin} has no END")
    return head + ports + sep + tail, True


def rect_minus(rect, cut):
    """Returns ``rect`` with ``cut`` taken out of it, as up to four rects."""
    x0, y0, x1, y1 = rect
    cx0, cy0, cx1, cy1 = cut
    if cx1 <= x0 or cx0 >= x1 or cy1 <= y0 or cy0 >= y1:
        return [rect]

    pieces = []
    if y0 < cy0:
        pieces.append((x0, y0, x1, min(y1, cy0)))
    if y1 > cy1:
        pieces.append((x0, max(y0, cy1), x1, y1))

    my0, my1 = max(y0, cy0), min(y1, cy1)
    if my0 < my1:
        if x0 < cx0:
            pieces.append((x0, my0, min(x1, cx0), my1))
        if x1 > cx1:
            pieces.append((max(x0, cx1), my0, x1, my1))

    return pieces


def subtract_from_obs(macro, plate):
    """Removes the plate from the met4 and met5 obstructions.

    Each rect is cut on its own so that the obstructions that do not meet the
    plate stay exactly as the vendor wrote them.
    """
    obs = re.search(r"^  OBS$(.*?)^  END$", macro, re.S | re.M)
    if obs is None:
        raise RuntimeError("macro has no OBS")

    cut = tuple(int(round(v * 1000))
                for v in (plate.left, plate.bottom, plate.right, plate.top))

    out = []
    layer = None
    for line in obs.group(1).split("\n"):
        stripped = line.strip()
        if stripped.startswith("LAYER"):
            layer = stripped.split()[1].rstrip(";").strip()
        elif stripped.startswith("RECT") and layer in ("met4", "met5"):
            rect = tuple(int(round(float(v) * 1000))
                         for v in stripped.replace(";", "").split()[1:5])
            pieces = rect_minus(rect, cut)
            if pieces != [rect]:
                out.extend(f"        RECT {x0 / 1000:.3f} {y0 / 1000:.3f} "
                           f"{x1 / 1000:.3f} {y1 / 1000:.3f} ;"
                           for x0, y0, x1, y1 in pieces)
                continue
        out.append(line)

    return macro[: obs.start(1)] + "\n".join(out) + macro[obs.end(1):]


def main():
    layout = pya.Layout()
    for gds in GDS:
        layout.read(gds)

    lef = open(LEF).read()
    macros = dict(re.findall(r"^MACRO (\S+)$(.*?)^END \1$", lef, re.S | re.M))

    plates = find_plates(layout, macros)

    for wrapper, (wrapped, pin) in DERIVED.items():
        if wrapper not in macros or wrapped not in plates:
            continue
        here = pin_rect(macros[wrapper], pin, "met5")
        there = pin_rect(macros[wrapped], pin, "met5")
        shift = pya.DVector(here.left - there.left, here.bottom - there.bottom)
        plates[wrapper] = (plates[wrapped][0], plates[wrapped][1].moved(shift))

    patched = 0
    for name, (pin, plate) in sorted(plates.items()):
        if name not in macros:
            continue
        macro, changed = add_plate_ports(macros[name], pin, plate)
        if not changed:
            print(f"{name}: already patched")
            continue
        macro = subtract_from_obs(macro, plate)
        lef = lef.replace(macros[name], macro, 1)
        macros[name] = macro
        patched += 1
        print(f"{name}: plate {plate} -> pin {pin}")

    open(OUT, "w").write(lef)
    print(f"patched {patched} macros -> {OUT}")


main()
