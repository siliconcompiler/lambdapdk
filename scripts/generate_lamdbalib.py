#!/usr/bin/env python3

###############################################################################
# Script for auto-generating lambda views using Yosys
###############################################################################

import os
import lambdalib

from siliconcompiler.targets import (
    skywater130_demo,
    asap7_demo,
    freepdk45_demo,
    gf180_demo
)

if __name__ == "__main__":
    pdk_root = os.path.dirname(os.path.dirname(__file__))

    pdks = {
        "sky130": {
            "target": skywater130_demo,
            "libs": [
                "sky130hd"
            ]
        },
        "gf180": {
            "target": gf180_demo,
            "libs": [
                "gf180mcu_fd_sc_mcu7t5v0",
                "gf180mcu_fd_sc_mcu9t5v0"
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
            lambdalib.generate(target, lib, f"{pdk_root}/lambdapdk/{pdk}/libs/{lib}/lambda")
