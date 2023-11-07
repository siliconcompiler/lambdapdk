#!/usr/bin/env python3

###############################################################################
# Script for auto-generating lambda views using Yosys
###############################################################################

import glob
import os
import shutil
import siliconcompiler

from siliconcompiler.targets import (
    skywater130_demo,
    asap7_demo,
    freepdk45_demo
)

if __name__ == "__main__":
    root = os.path.join(os.path.dirname(__file__), '..')
    # Get List of stdlib cells in lambdalib
    cells_dir = os.path.join(root, 'submodules/lambdalib/stdlib/rtl')
    cells = glob.glob(f'{cells_dir}/la_*.v')

    exclude = ['la_decap',
               'la_keeper',
               'la_footer',
               'la_header',
               'la_antenna']

    # TODO: make script less janky
    pdks = {
        "sky130": {
            "target": skywater130_demo,
            "libs": [
                "sky130hd"
            ]
        },
        "freepdk45": {
            "target": freepdk45_demo,
            "libs": [
                "nangate45"
            ]
        },
        "asap7": {
            "target": asap7_demo,
            "libs": [
                "asap7sc7p5t_rvt",
                "asap7sc7p5t_lvt",
                "asap7sc7p5t_slvt"
            ]
        },
    }

    for pdk, info in pdks.items():
        target = info["target"]

        for lib in info['libs']:
            lambda_dir = f"{root}/lambdapdk/{pdk}/libs/{lib}/lambda"
            shutil.rmtree(lambda_dir, ignore_errors=True)
            os.makedirs(lambda_dir, exist_ok=True)

            for verilog in cells:
                cell_name, _ = os.path.splitext(os.path.basename(verilog))

                if cell_name in exclude:
                    continue

                jobname = f"{target.__name__}-{lib}"

                chip = siliconcompiler.Chip(cell_name)
                chip.input(verilog)
                chip.load_target(target)
                chip.set('asic', 'logiclib', lib)
                chip.set('option', 'to', 'syn')
                chip.set('option', 'quiet', True)
                chip.set('option', 'resume', True)
                chip.set('option', 'jobname', jobname)

                chip.add('option', 'ydir', cells_dir)
                chip.run()

                shutil.copy(chip.find_result("vg", step="syn", index=0),
                            lambda_dir)
