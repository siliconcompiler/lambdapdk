"""Drop the pin-level ``max_transition`` from the sky130 SRAM liberty.

``sky130_sram_2kbyte_1rw1r_32x512_8_TT_1p8V_25C.lib`` puts
``max_transition : 0.04;`` on the ``addr0``, ``wmask0`` and ``addr1`` buses.
0.04ns is the top of the characterised slew axis
(``index_1("0.00125, 0.005, 0.04")``), not a design rule, and no sky130hd cell
can drive it -- the best achievable is 0.062ns -- so the resizer fails with
RSZ-0090 on any design that instantiates this macro.  Removing the three lines
lets the library's own ``default_max_transition : 0.5`` apply to those buses as
it does to every other pin.

The macro this one replaced carried no pin-level ``max_transition`` at all.

This is the only delta between the vendored liberty and the upstream one -- the
LEF and Verilog are byte-identical -- so it is the one file ``sky130sram``
cannot take by reference.  Not yet reported upstream; see
``lambdapdk/sky130/PATCHES.md``.

Run from the repository root::

    python3 scripts/patch_sky130sram_maxtran.py \\
        --input $PDK/sky130A/libs.ref/sky130_sram_macros/lib/<name>.lib \\
        --output lambdapdk/sky130/libs/sky130sram/<macro>/nldm/<name>.lib

With no arguments it rewrites the vendored liberty in place, which is a no-op on
an already-patched file.
"""

import argparse
import re
import sys

from pathlib import Path

MACRO = "sky130_sram_2kbyte_1rw1r_32x512_8"
CORNER = "TT_1p8V_25C"

DEFAULT = Path("lambdapdk", "sky130", "libs", "sky130sram", MACRO, "nldm",
               f"{MACRO}_{CORNER}.lib")

#: The buses upstream puts the offending attribute on. Named rather than matched
#: blindly so that the attribute appearing somewhere new is a failure to look at
#: rather than a line silently dropped.
BUSES = ("addr0", "wmask0", "addr1")

#: What is removed, as it appears in the file.
PATTERN = re.compile(r"^[ \t]*max_transition[ \t]*:[ \t]*0\.04;[ \t]*\n", re.M)


def patch(text):
    """Returns the liberty with the pin-level max_transition lines removed.

    Raises:
        RuntimeError: If the number of matches is not the number of buses the
            attribute is known to sit on, since that means upstream moved it and
            the removal is no longer the understood change.
    """
    found = len(PATTERN.findall(text))
    if found == 0:
        return text, 0
    if found != len(BUSES):
        raise RuntimeError(
            f"expected {len(BUSES)} 'max_transition : 0.04;' lines "
            f"({', '.join(BUSES)}), found {found} -- upstream changed, re-check "
            "before patching")
    return PATTERN.sub("", text), found


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", type=Path, default=DEFAULT,
                        help="liberty to read (default: the vendored copy)")
    parser.add_argument("--output", type=Path, default=None,
                        help="where to write it (default: over --input)")
    args = parser.parse_args()

    output = args.output or args.input
    text = args.input.read_text()

    patched, removed = patch(text)
    if removed == 0:
        print(f"{args.input}: no pin-level max_transition, nothing to do")
        if output != args.input:
            output.write_text(patched)
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(patched)
    print(f"removed {removed} max_transition lines -> {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
