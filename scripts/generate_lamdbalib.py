#!/usr/bin/env python3

###############################################################################
# Script for auto-generating lambda views using Yosys
###############################################################################

import os
import lambdalib
import multiprocessing

from lambdalib.utils import write_la_spram

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
            p = multiprocessing.Process(
                target=lambdalib.generate,
                args=(target.__name__,
                      lib,
                      f"{pdk_root}/lambdapdk/{pdk}/libs/{lib}/lambda/stdlib"))
            procs.append(p)
            p.start()
    for proc in procs:
        proc.join()

    procs = []
    for pdk, info in libs.items():
        target = info["target"]

        for lib in info['libs']:
            p = multiprocessing.Process(
                target=lambdalib.copy,
                args=(f"{pdk_root}/lambdapdk/{pdk}/libs/{lib}/lambda/auxlib",
                      'auxlib'))
            procs.append(p)
            p.start()
    for proc in procs:
        proc.join()

    asap7_spram_port_map = [
        ("clk", "clk"),
        ("addr_in", "mem_addr"),
        ("ce_in", "ce_in"),
        ("rd_out", "mem_dout"),
        ("we_in", "we_in"),
        ("w_mask_in", "mem_wmask"),
        ("wd_in", "mem_din")
    ]

    freepdk45_spram_port_map = [
        ("clk", "clk"),
        ("addr_in", "mem_addr"),
        ("ce_in", "ce_in"),
        ("rd_out", "mem_dout"),
        ("we_in", "we_in"),
        ("w_mask_in", "mem_wmask"),
        ("wd_in", "mem_din")
    ]

    gf180_spram_port_map = [
        ("CLK", "clk"),
        ("CEN", "~ce_in"),
        ("GWEN", "~we_in"),
        ("WEN", "~mem_wmask"),
        ("A", "mem_addr"),
        ("D", "mem_din"),
        ("Q", "mem_dout")
    ]

    sky130_spram_port_map = [
        ("clk0", "clk"),
        ("csb0", "ce_in && we_in"),
        ("web0", "ce_in && we_in"),
        ("wmask0", "{mem_wmask[24], mem_wmask[16], mem_wmask[8], mem_wmask[0]}"),
        ("addr0", "mem_addr"),
        ("din0", "mem_din"),
        ("dout0", ""),
        ("clk1", "clk"),
        ("csb1", "ce_in && ~we_in"),
        ("addr1", "mem_addr"),
        ("dout1", "mem_dout"),
    ]

    srams = {
        "asap7": {
            "name": "fakeram7",
            "implementations": ["la_spram"],
            "la_spram": {
                "fakeram7_512x32": {
                    "DW": 32, "AW": 9, "port_map": asap7_spram_port_map
                },
                "fakeram7_512x64": {
                    "DW": 64, "AW": 9, "port_map": asap7_spram_port_map
                },
                "fakeram7_256x64": {
                    "DW": 64, "AW": 8, "port_map": asap7_spram_port_map
                },
                "fakeram7_256x32": {
                    "DW": 32, "AW": 8, "port_map": asap7_spram_port_map
                },
                "fakeram7_128x32": {
                    "DW": 32, "AW": 7, "port_map": asap7_spram_port_map
                },
                "fakeram7_64x32": {
                    "DW": 32, "AW": 6, "port_map": asap7_spram_port_map
                }
            }
        },
        "freepdk45": {
            "name": "fakeram45",
            "implementations": ["la_spram"],
            "la_spram": {
                "fakeram45_512x32": {
                    "DW": 32, "AW": 9, "port_map": freepdk45_spram_port_map
                },
                "fakeram45_512x64": {
                    "DW": 64, "AW": 9, "port_map": freepdk45_spram_port_map
                },
                "fakeram45_256x64": {
                    "DW": 64, "AW": 8, "port_map": freepdk45_spram_port_map
                },
                "fakeram45_256x32": {
                    "DW": 32, "AW": 8, "port_map": freepdk45_spram_port_map
                },
                "fakeram45_128x32": {
                    "DW": 32, "AW": 7, "port_map": freepdk45_spram_port_map
                },
                "fakeram45_64x32": {
                    "DW": 32, "AW": 6, "port_map": freepdk45_spram_port_map
                }
            }
        },
        "gf180": {
            "name": "gf180mcu_fd_ip_sram",
            "implementations": ["la_spram"],
            "la_spram": {
                "gf180mcu_fd_ip_sram__sram512x8m8wm1": {
                    "DW": 8, "AW": 9, "port_map": gf180_spram_port_map
                },
                "gf180mcu_fd_ip_sram__sram256x8m8wm1": {
                    "DW": 8, "AW": 8, "port_map": gf180_spram_port_map
                },
                "gf180mcu_fd_ip_sram__sram128x8m8wm1": {
                    "DW": 8, "AW": 7, "port_map": gf180_spram_port_map
                },
                "gf180mcu_fd_ip_sram__sram64x8m8wm1": {
                    "DW": 8, "AW": 6, "port_map": gf180_spram_port_map
                }
            }
        },
        "sky130": {
            "name": "sky130sram",
            "implementations": ["la_spram"],
            "la_spram": {
                "sky130_sram_1rw1r_64x256_8": {
                    "DW": 64, "AW": 8, "port_map": sky130_spram_port_map
                }
            }
        },
    }

    for pdk, info in srams.items():
        lib = info['name']
        lambdalib.copy(f"{pdk_root}/lambdapdk/{pdk}/libs/{lib}/lambda",
                       la_lib='ramlib',
                       exclude=info['implementations'])
        for ram in info['implementations']:
            with open(f"{pdk_root}/lambdapdk/{pdk}/libs/{lib}/lambda/{ram}.v", "w") as f:
                write_la_spram(f, info[ram])

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
