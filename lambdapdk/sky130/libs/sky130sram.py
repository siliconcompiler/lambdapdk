import argparse
import math

import os.path

from pathlib import Path

from typing import Dict, Tuple

from lambdalib import LambalibTechLibrary
from lambdapdk import LambdaLibrary, _LambdaPath
from lambdalib.ramlib import Spram, RAMTechLib
from lambdapdk.sky130 import Sky130PDK
from lambdapdk.utils import format_verilog


class Sky130_SRAM_64x256(LambdaLibrary, RAMTechLib):
    def __init__(self):
        super().__init__()
        self.set_name('sky130_sram_1rw1r_64x256_8')

        self.add_asic_pdk(Sky130PDK())

        path_base = Path('lambdapdk', 'sky130', 'libs', "sky130sram")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("models.timing.nldm"):
                self.add_file(path_base / self.name / "nldm" / f"{self.name}_TT_1p8V_25C.lib")
                self.add_asic_libcornerfileset("generic", "nldm")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("models.physical"):
                self.add_file(path_base / self.name / "lef" / f"{self.name}.lef.gz")
                self.add_file(path_base / self.name / "gds" / f"{self.name}.gds")
                self.add_asic_aprfileset()

            with self.active_fileset("models.lvs"):
                self.add_file(path_base / self.name / "spice" / f"{self.name}.lvs.sp",
                              filetype="cdl")
                self.add_asic_aprfileset()

            with self.active_fileset("models.spice"):
                self.add_file(path_base / self.name / "spice" / f"{self.name}.sp")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("openroad.powergrid"):
                self.add_file(path_base / "apr" / "openroad" / "pdngen.tcl")
                self.add_openroad_powergridfileset()
            with self.active_fileset("openroad.globalconnect"):
                self.add_file(path_base / "apr" / "openroad" / "global_connect.tcl")
                self.add_openroad_globalconnectfileset()

    def __ram_props(self) -> Tuple[int, int]:
        """Returns the RAM properties (width, depth) based on the configuration."""
        size = self.name.split('_')[-2]
        depth = int(size.split('x')[1])
        width = int(size.split('x')[0])
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
            "clk0": "clk",
            "csb0": "ce_in && we_in",
            "web0": "ce_in && we_in",
            "wmask0": "{mem_wmask[24], mem_wmask[16], mem_wmask[8], mem_wmask[0]}",
            "addr0": "mem_addr",
            "din0": "mem_din",
            "dout0": "",
            "clk1": "clk",
            "csb1": "ce_in && ~we_in",
            "addr1": "mem_addr",
            "dout1": "mem_dout",
        }

    def get_ram_libcell(self) -> str:
        """Returns the name of the RAM library cell.

        Returns:
            str: The name of the RAM library cell.
        """
        return self.name


class Sky130Lambdalib_SinglePort(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_spram", [
            Sky130_SRAM_64x256])
        self.set_name("sky130_la_spram")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "sky130", "libs", "sky130sram")

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
    files.append(os.path.join(os.path.dirname(__file__), "sky130sram", "lambda", f"{spram.name}.v"))
    spram.write_lambdalib(
        files[-1],
        Sky130Lambdalib_SinglePort().techlibs)

    for f in files:
        format_verilog(f, args.verible_bin)
