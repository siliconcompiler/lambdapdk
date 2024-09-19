#!/usr/bin/env python3

###############################################################################
# Script for auto-generating lambda views using Yosys
###############################################################################

import os
import lambdalib
import multiprocessing
import argparse
import subprocess
import glob
import re

from lambdalib.utils import write_la_spram

from siliconcompiler.targets import (
    skywater130_demo,
    asap7_demo,
    freepdk45_demo,
    gf180_demo,
    ihp130_demo
)

pdk_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

libs = {
    "sky130": {
        "target": skywater130_demo,
        "libs": [
            "sky130hd",
            "sky130hdll"
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
    "ihp130": {
        "target": ihp130_demo,
        "libs": [
            "sg13g2_stdcell"
        ]
    }
}


def __format_verilog(path, verible_bin):
    if os.path.isfile(path):
        paths = [os.path.abspath(path)]
    elif os.path.isdir(path):
        paths = glob.glob(os.path.join(path, '*.v'))
        paths.extend(glob.glob(os.path.join(path, '*.vh')))

    for f in paths:
        print(f"Formatting: {f}")
        with open(f) as fd:
            content = fd.read()
        with open(f, 'w') as fd:
            fd.write(re.sub(r"(\(\*\ssrc\s?=\s?\").*(\".*)", r"\1generated\2", content))
        subprocess.run([verible_bin, '--inplace', f])


def stdlib(verible_bin):
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

    for pdk, info in libs.items():
        for lib in info['libs']:
            __format_verilog(f"{pdk_root}/lambdapdk/{pdk}/libs/{lib}/lambda/stdlib", verible_bin)


def auxlib(verible_bin):
    always_copy = [
        'la_clkmux2',
        'la_clkmux4',
    ]
    generate_libs = {
        "sky130": {
            "sky130hd": {
                "implemented": [
                    'la_antenna',
                    'la_clkicgand',
                    'la_clkicgor',
                    'la_pwrbuf',
                    'la_tbuf',
                    'la_dsync',
                    'la_rsync',
                    'la_decap'
                ],
                "missing": [
                    'la_footer',
                    'la_header',
                    'la_ibuf',
                    'la_idiff',
                    'la_keeper',
                    'la_obuf',
                    'la_odiff'
                ]
            },
            "sky130hdll": {
                "implemented": [
                    'la_antenna',
                    'la_clkicgand',
                    'la_clkicgor',
                    'la_pwrbuf',
                    'la_tbuf',
                    'la_dsync',
                    'la_rsync',
                    'la_decap'
                ],
                "missing": [
                    'la_footer',
                    'la_header',
                    'la_ibuf',
                    'la_idiff',
                    'la_keeper',
                    'la_obuf',
                    'la_odiff'
                ]
            }
        },
        "gf180": {
            "gf180mcu_fd_sc_mcu7t5v0": {
                "implemented": [
                    'la_antenna',
                    'la_clkicgand',
                    'la_clkicgor',
                    'la_pwrbuf',
                    'la_tbuf',
                    'la_dsync',
                    'la_rsync'
                ],
                "missing": [
                    'la_decap',
                    'la_footer',
                    'la_header',
                    'la_ibuf',
                    'la_idiff',
                    'la_keeper',
                    'la_obuf',
                    'la_odiff'
                ]
            },
            "gf180mcu_fd_sc_mcu9t5v0": {
                "implemented": [
                    'la_antenna',
                    'la_clkicgand',
                    'la_clkicgor',
                    'la_pwrbuf',
                    'la_tbuf',
                    'la_dsync',
                    'la_rsync'
                ],
                "missing": [
                    'la_decap',
                    'la_footer',
                    'la_header',
                    'la_ibuf',
                    'la_idiff',
                    'la_keeper',
                    'la_obuf',
                    'la_odiff'
                ]
            }
        },
        "freepdk45": {
            "nangate45": {
                "implemented": [
                    'la_antenna',
                    'la_clkicgand',
                    'la_clkicgor',
                    'la_pwrbuf',
                    'la_tbuf',
                    'la_dsync',
                    'la_rsync'
                ],
                "missing": [
                    'la_decap',
                    'la_footer',
                    'la_header',
                    'la_ibuf',
                    'la_idiff',
                    'la_keeper',
                    'la_obuf',
                    'la_odiff'
                ]
            }
        },
        "asap7": {
            "asap7sc7p5t_rvt": {
                "implemented": [
                    'la_clkicgand',
                    'la_clkicgor',
                    'la_pwrbuf',
                    'la_dsync',
                    'la_rsync',
                    'la_decap'
                ],
                "missing": [
                    'la_antenna',
                    'la_footer',
                    'la_header',
                    'la_ibuf',
                    'la_idiff',
                    'la_keeper',
                    'la_obuf',
                    'la_odiff',
                    'la_tbuf'
                ]
            },
            "asap7sc7p5t_lvt": {
                "implemented": [
                    'la_clkicgand',
                    'la_clkicgor',
                    'la_pwrbuf',
                    'la_dsync',
                    'la_rsync',
                    'la_decap'
                ],
                "missing": [
                    'la_antenna',
                    'la_footer',
                    'la_header',
                    'la_ibuf',
                    'la_idiff',
                    'la_keeper',
                    'la_obuf',
                    'la_odiff',
                    'la_tbuf'
                ]
            },
            "asap7sc7p5t_slvt": {
                "implemented": [
                    'la_clkicgand',
                    'la_clkicgor',
                    'la_pwrbuf',
                    'la_dsync',
                    'la_rsync',
                    'la_decap'
                ],
                "missing": [
                    'la_antenna',
                    'la_footer',
                    'la_header',
                    'la_ibuf',
                    'la_idiff',
                    'la_keeper',
                    'la_obuf',
                    'la_odiff',
                    'la_tbuf'
                ]
            },
        },
        "ihp130": {
            "sg13g2_stdcell": {
                "implemented": [
                    'la_antenna',
                    'la_clkicgand',
                    'la_clkicgor',
                    'la_pwrbuf',
                    'la_tbuf',
                    'la_dsync',
                    'la_rsync'
                ],
                "missing": [
                    'la_decap',
                    'la_footer',
                    'la_header',
                    'la_ibuf',
                    'la_idiff',
                    'la_keeper',
                    'la_obuf',
                    'la_odiff'
                ]
            }
        },
    }

    procs = []
    for pdk, info in libs.items():
        for lib in info['libs']:
            exclude = []
            exclude.extend(generate_libs[pdk][lib]["implemented"])
            exclude.extend(generate_libs[pdk][lib]["missing"])

            p = multiprocessing.Process(
                target=lambdalib.copy,
                args=(f"{pdk_root}/lambdapdk/{pdk}/libs/{lib}/lambda/auxlib",),
                kwargs={
                    "la_lib": 'auxlib',
                    "exclude": exclude
                })
            procs.append(p)
            p.start()
    for proc in procs:
        proc.join()

    procs = []
    for pdk, info in libs.items():
        target = info["target"]

        for lib in info['libs']:
            exclude = [*always_copy]
            exclude.extend(generate_libs[pdk][lib]["implemented"])
            exclude.extend(generate_libs[pdk][lib]["missing"])

            p = multiprocessing.Process(
                target=lambdalib.generate,
                args=(target.__name__,
                      lib,
                      f"{pdk_root}/lambdapdk/{pdk}/libs/{lib}/lambda/auxlib"),
                kwargs={
                    "la_lib": 'auxlib',
                    "exclude": exclude
                })
            procs.append(p)
            p.start()
    for proc in procs:
        proc.join()

    for pdk, info in libs.items():
        for lib in info['libs']:
            __format_verilog(f"{pdk_root}/lambdapdk/{pdk}/libs/{lib}/lambda/auxlib", verible_bin)


def ramlib(verible_bin):
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

    ihp130_spram_port_map = [
        ("A_CLK", "clk"),
        ("A_MEN", "~ce_in"),
        ("A_WEN", "~we_in"),
        ("A_REN", "we_in"),
        ("A_ADDR", "mem_addr"),
        ("A_DIN", "mem_din"),
        ("A_DLY", "1'b1"),
        ("A_DOUT", "mem_dout"),
        ("A_BM", "mem_wmask"),
        ("A_BIST_CLK", "1'b0"),
        ("A_BIST_EN", "1'b0"),
        ("A_BIST_MEN", "1'b0"),
        ("A_BIST_WEN", "1'b0"),
        ("A_BIST_REN", "1'b0"),
        ("A_BIST_ADDR", "'b0"),
        ("A_BIST_DIN", "'b0"),
        ("A_BIST_BM", "'b0")
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
        "ihp130": {
            "name": "sg13g2_sram",
            "implementations": ["la_spram"],
            "la_spram": {
                "RM_IHPSG13_1P_1024x64_c2_bm_bist": {
                    "DW": 64, "AW": 10, "port_map": ihp130_spram_port_map
                },
                "RM_IHPSG13_1P_2048x64_c2_bm_bist": {
                    "DW": 64, "AW": 11, "port_map": ihp130_spram_port_map
                },
                "RM_IHPSG13_1P_256x48_c2_bm_bist": {
                    "DW": 48, "AW": 8, "port_map": ihp130_spram_port_map
                },
                "RM_IHPSG13_1P_256x64_c2_bm_bist": {
                    "DW": 64, "AW": 8, "port_map": ihp130_spram_port_map
                },
                "RM_IHPSG13_1P_512x64_c2_bm_bist": {
                    "DW": 64, "AW": 9, "port_map": ihp130_spram_port_map
                },
                "RM_IHPSG13_1P_64x64_c2_bm_bist": {
                    "DW": 64, "AW": 6, "port_map": ihp130_spram_port_map
                },
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

        __format_verilog(f"{pdk_root}/lambdapdk/{pdk}/libs/{lib}/lambda", verible_bin)


def iolib(verible_bin):
    iolib = {
        "sky130": {
            "name": "sky130io",
            "implementations": ["la_ioanalog",
                                "la_iobidir",
                                "la_ioclamp",
                                "la_iocorner",
                                "la_iocut",
                                "la_ioinput",
                                "la_iopoc",
                                "la_iorxdiff",
                                "la_iotxdiff",
                                "la_iovdd",
                                "la_iovdda",
                                "la_iovddio",
                                "la_iovss",
                                "la_iovssa",
                                "la_iovssio"]
        },
        "gf180": {
            "name": "gf180mcu_fd_io",
            "implementations": ["la_ioanalog",
                                "la_iobidir",
                                "la_iocorner",
                                "la_iocut",
                                "la_ioinput",
                                "la_iopoc",
                                "la_iorxdiff",
                                "la_iotxdiff",
                                "la_iovdd",
                                "la_iovdda",
                                "la_iovddio",
                                "la_iovss",
                                "la_iovssa",
                                "la_iovssio"]
        },
        "asap7": {
            "name": "fakeio7",
            "implementations": ["la_ioanalog",
                                "la_iobidir",
                                "la_ioclamp",
                                "la_ioinput",
                                "la_iocorner",
                                "la_iocut",
                                "la_iopoc",
                                "la_iovdd",
                                "la_iovss",
                                "la_iovddio",
                                "la_iovssio",
                                "la_iovdda",
                                "la_iovssa",
                                "la_iorxdiff",
                                "la_iotxdiff"]
        },
    }

    for pdk, info in iolib.items():
        lib = info['name']
        lambdalib.copy(f"{pdk_root}/lambdapdk/{pdk}/libs/{lib}/lambda",
                       la_lib='iolib',
                       exclude=info['implementations'])
        __format_verilog(f"{pdk_root}/lambdapdk/{pdk}/libs/{lib}/lambda", verible_bin)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--stdlib', action='store_true')
    parser.add_argument('--auxlib', action='store_true')
    parser.add_argument('--ramlib', action='store_true')
    parser.add_argument('--iolib', action='store_true')
    parser.add_argument('--verible_bin',
                        metavar='<verible>',
                        required=True,
                        help='path to verible-verilog-format')

    args = parser.parse_args()

    if args.stdlib:
        stdlib(args.verible_bin)

    if args.auxlib:
        auxlib(args.verible_bin)

    if args.ramlib:
        ramlib(args.verible_bin)

    if args.iolib:
        iolib(args.verible_bin)
