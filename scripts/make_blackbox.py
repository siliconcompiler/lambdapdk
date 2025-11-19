#!/usr/bin/env python3

import sc_leflib
import argparse
import os


def get_cells(path):
    lef = sc_leflib.parse(path)

    cells = {}
    for cell, info in lef['macros'].items():
        cells[cell] = {}
        multipins = {}
        multipins_dir = {}
        for pin, pin_info in info.get('pins', {}).items():
            if "[" in pin:
                direction = pin_info.get("direction", "inout").lower()
                pin = pin[:pin.find("[")]
                if pin not in multipins:
                    multipins[pin] = 0
                multipins[pin] += 1
                multipins_dir[pin] = direction
                continue

            direction = pin_info.get("direction", "inout").lower()
            cells[cell][pin] = direction

        for pin, width in multipins.items():
            cells[cell][f"[{width-1}:0] {pin}"] = multipins_dir[pin]

    return cells


def write_blackbox(lef_file, filename):
    with open(filename, 'w') as f:
        f.write(f"// Source {os.path.relpath(lef_file, os.getcwd())}\n")

        for cell, pins in get_cells(lef_file).items():
            f.write("\n(* blackbox *)\n")
            f.write(f"module {cell} (\n")
            first_pin = True
            for pin, direction in pins.items():
                if not first_pin:
                    f.write(",\n")
                f.write(f"    {direction} {pin}")
                first_pin = False
            f.write("\n);\n")
            f.write("endmodule\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Create blackbox verilog model file from lef file')
    parser.add_argument('--lef', required=True, help='Liberty file', metavar='<file>')
    parser.add_argument('--output', required=True, help='Output file', metavar='<file>')

    args = parser.parse_args()

    write_blackbox(args.lef, args.output)
