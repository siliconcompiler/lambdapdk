#!/usr/bin/env python3

###############################################################################
# Script for auto-generating lambda views using Yosys
###############################################################################

import os
import lambdalib
import multiprocessing

from siliconcompiler.targets import (
    skywater130_demo,
    asap7_demo,
    freepdk45_demo,
    gf180_demo
)

if __name__ == "__main__":
    pdk_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    libs = {
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

    procs = []
    for pdk, info in libs.items():
        target = info["target"]

        for lib in info['libs']:
            p = multiprocessing.Process(target=lambdalib.generate,
                                        args=(target.__name__,
                                              lib,
                                              f"{pdk_root}/lambdapdk/{pdk}/libs/{lib}/lambda"))
            procs.append(p)
            p.start()
    for proc in procs:
        proc.join()

    srams = {
        "asap7": {
            "name": "fakeram7",
            "implementations": ["la_spram"]
        },
        "freepdk45": {
            "name": "fakeram45",
            "implementations": ["la_spram"]
        },
        "sky130": {
            "name": "sky130sram",
            "implementations": ["la_spram"]
        },
        "gf180": {
            "name": "gf180mcu_fd_ip_sram",
            "implementations": ["la_spram"]
        },
    }

    for pdk, info in srams.items():
        lib = info['name']
        lambdalib.copy(f"{pdk_root}/lambdapdk/{pdk}/libs/{lib}/lambda",
                       la_lib='ramlib',
                       exclude=info['implementations'])

    iolib = {
        "sky130": {
            "name": "sky130io",
            "implementations": ["la_iobidir",
                                "la_iocorner",
                                "la_iocut",
                                "la_iopoc",
                                "la_iovdd",
                                "la_iovddio",
                                "la_iovss",
                                "la_iovssio"]
        },
        "gf180": {
            "name": "gf180mcu_fd_io",
            "implementations": ["la_ioanalog",
                                "la_iobidir",
                                "la_iocorner",
                                "la_iocut",
                                "la_iopoc",
                                "la_iovdd",
                                "la_iovddio",
                                "la_iovss",
                                "la_iovssio"]
        },
    }

    for pdk, info in iolib.items():
        lib = info['name']
        lambdalib.copy(f"{pdk_root}/lambdapdk/{pdk}/libs/{lib}/lambda",
                       la_lib='iolib',
                       exclude=info['implementations'])
