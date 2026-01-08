import argparse

import os.path

from pathlib import Path

from lambdalib import LambalibTechLibrary
from lambdapdk import LambdaLibrary, _LambdaPath
from lambdalib.ramlib import Spram
from lambdapdk.freepdk45 import FreePDK45PDK
from lambdapdk.utils import format_verilog


class _FakeRAM45Library(LambdaLibrary):
    def __init__(self, config):
        super().__init__()
        self.set_name(f"fakeram45_{config}")

        self.add_asic_pdk(FreePDK45PDK())

        path_base = Path("lambdapdk", "freepdk45", "libs", "fakeram45")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("models.physical"):
                self.add_file(path_base / "lef" / f"{self.name}.lef")
                self.add_asic_aprfileset()

                with self.active_fileset("models.timing.nldm"):
                    self.add_file(path_base / "nldm" / f"{self.name}.lib")
                    self.add_asic_libcornerfileset("generic", "nldm")

            with self.active_fileset("openroad.powergrid"):
                self.add_file(path_base / "apr" / "openroad" / "pdngen.tcl")
                self.add_openroad_powergridfileset()
            with self.active_fileset("openroad.globalconnect"):
                self.add_file(path_base / "apr" / "openroad" / "global_connect.tcl")
                self.add_openroad_globalconnectfileset()

            self.add_klayout_allowmissingcell(self.name)


class FakeRAM45_64x32(_FakeRAM45Library):
    def __init__(self):
        super().__init__("64x32")


class FakeRAM45_128x32(_FakeRAM45Library):
    def __init__(self):
        super().__init__("128x32")


class FakeRAM45_256x32(_FakeRAM45Library):
    def __init__(self):
        super().__init__("256x32")


class FakeRAM45_256x64(_FakeRAM45Library):
    def __init__(self):
        super().__init__("256x64")


class FakeRAM45_512x32(_FakeRAM45Library):
    def __init__(self):
        super().__init__("512x32")


class FakeRAM45_512x64(_FakeRAM45Library):
    def __init__(self):
        super().__init__("512x64")


class FakeRAM45Lambdalib_SinglePort(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_spram", [
            FakeRAM45_64x32,
            FakeRAM45_128x32,
            FakeRAM45_256x32,
            FakeRAM45_256x64,
            FakeRAM45_512x32,
            FakeRAM45_512x64])
        self.set_name("fakeram45_la_spram")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "freepdk45", "libs", "fakeram45")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_spram.v")
                self.add_depfileset(Spram(), "rtl.impl")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--verible_bin',
                        metavar='<verible>',
                        required=True,
                        help='path to verible-verilog-format')
    args = parser.parse_args()

    files = []

    freepdk45_spram_port_map = [
        ("clk", "clk"),
        ("addr_in", "mem_addr"),
        ("ce_in", "ce_in"),
        ("rd_out", "mem_dout"),
        ("we_in", "we_in"),
        ("w_mask_in", "mem_wmask"),
        ("wd_in", "mem_din")
    ]

    spram = Spram()
    files.append(os.path.join(os.path.dirname(__file__), "fakeram45", "lambda", f"{spram.name}.v"))
    spram.write_lambdalib(
        files[-1],
        {
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
    })

    for f in files:
        format_verilog(f, args.verible_bin)
