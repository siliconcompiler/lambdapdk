import argparse
import math

import os.path

from pathlib import Path

from typing import Dict, Tuple

from lambdalib import LambalibTechLibrary
from lambdapdk import LambdaLibrary, _LambdaPath
from lambdalib.ramlib import Spram, RAMTechLib
from lambdapdk.freepdk45 import FreePDK45PDK
from lambdapdk.utils import format_verilog


class _FakeRAM45Library(LambdaLibrary, RAMTechLib):
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

    def __ram_props(self) -> Tuple[int, int]:
        """Returns the RAM properties (width, depth) based on the configuration."""
        size = self.name.split('_')[-1]
        width = int(size.split('x')[1])
        depth = int(size.split('x')[0])
        return width, depth

    def get_ram_width(self) -> int:
        """Returns the width of the RAM cell.

        Returns:
            int: The width of the RAM cell.
        """
        width, _ = self.__ram_props()
        return width

    def get_ram_depth(self) -> int:
        """Returns the depth of the RAM cell.

        Returns:
            int: The depth of the RAM cell.
        """
        _, depth = self.__ram_props()
        return int(math.log2(depth))

    def get_ram_ports(self) -> Dict[str, str]:
        """Returns the port mapping for the RAM cell.

        Returns:
            Dict[str, str]: A dictionary mapping port names to their expressions.
        """
        return {
            "clk": "clk",
            "addr_in": "mem_addr",
            "ce_in": "ce_in",
            "rd_out": "mem_dout",
            "we_in": "we_in",
            "w_mask_in": "mem_wmask",
            "wd_in": "mem_din"
        }

    def get_ram_libcell(self) -> str:
        """Returns the name of the RAM library cell.

        Returns:
            str: The name of the RAM library cell.
        """
        return self.name


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

    spram = Spram()
    files.append(os.path.join(os.path.dirname(__file__), "fakeram45", "lambda", f"{spram.name}.v"))
    spram.write_lambdalib(
        files[-1],
        FakeRAM45Lambdalib_SinglePort().techlibs)

    for f in files:
        format_verilog(f, args.verible_bin)
