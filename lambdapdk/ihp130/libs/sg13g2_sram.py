import argparse
import math

import os.path

from pathlib import Path

from typing import Dict, Tuple

from lambdalib import LambalibTechLibrary
from lambdapdk import LambdaLibrary, _LambdaPath
from lambdalib.ramlib import Spram, RAMTechLib
from lambdapdk.ihp130 import IHP130PDK, _IHP130Path
from lambdapdk.utils import format_verilog


class _IHP130SRAMLibrary(LambdaLibrary, _IHP130Path, RAMTechLib):
    def __init__(self, config):
        super().__init__()
        self.set_name(f'RM_IHPSG13_1P_{config}_c2_bm_bist')

        self.add_asic_pdk(IHP130PDK())

        path_base = Path("lambdapdk", "ihp130", "libs", "sg13g2_sram")

        with self.active_dataroot("ihp130"):
            with self.active_fileset("models.physical"):
                self.add_file(f"ihp-sg13g2/libs.ref/sg13g2_sram/lef/{self.name}.lef")
                self.add_file(f"ihp-sg13g2/libs.ref/sg13g2_sram/gds/{self.name}.gds")
                self.add_asic_aprfileset()

            with self.active_fileset("models.lvs"):
                self.add_file(f"ihp-sg13g2/libs.ref/sg13g2_sram/cdl/{self.name}.cdl")
                self.add_asic_aprfileset()

            for corner_name, filename in [
                    ('slow', f'{self.name}_slow_1p08V_125C.lib'),
                    ('typical', f'{self.name}_typ_1p20V_25C.lib'),
                    ('fast', f'{self.name}_fast_1p32V_m55C.lib')]:
                with self.active_fileset(f"models.timing.nldm.{corner_name}"):
                    self.add_file(f"ihp-sg13g2/libs.ref/sg13g2_sram/lib/{filename}")
                    self.add_asic_libcornerfileset(corner_name, "nldm")

            with self.active_fileset("rtl"):
                self.add_file(f"ihp-sg13g2/libs.ref/sg13g2_sram/verilog/{self.name}.v")
                self.add_file("ihp-sg13g2/libs.ref/sg13g2_sram/verilog/"
                              "RM_IHPSG13_1P_core_behavioral_bm_bist.v")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("openroad.powergrid"):
                self.add_file(path_base / "apr" / "openroad" / "pdngen.tcl")
                self.add_openroad_powergridfileset()
            with self.active_fileset("openroad.globalconnect"):
                self.add_file(path_base / "apr" / "openroad" / "global_connect.tcl")
                self.add_openroad_globalconnectfileset()

    def __ram_props(self) -> Tuple[int, int]:
        """Returns the RAM properties (width, depth) based on the configuration."""
        size = self.name.split('_')[3]
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
            "A_CLK": "clk",
            "A_MEN": "~ce_in",
            "A_WEN": "~we_in",
            "A_REN": "we_in",
            "A_ADDR": "mem_addr",
            "A_DIN": "mem_din",
            "A_DLY": "1'b1",
            "A_DOUT": "mem_dout",
            "A_BM": "mem_wmask",
            "A_BIST_CLK": "1'b0",
            "A_BIST_EN": "1'b0",
            "A_BIST_MEN": "1'b0",
            "A_BIST_WEN": "1'b0",
            "A_BIST_REN": "1'b0",
            "A_BIST_ADDR": "'b0",
            "A_BIST_DIN": "'b0",
            "A_BIST_BM": "'b0"
        }

    def get_ram_libcell(self) -> str:
        """Returns the name of the RAM library cell.

        Returns:
            str: The name of the RAM library cell.
        """
        return self.name


class IHP130_SRAM_1024x64(_IHP130SRAMLibrary):
    def __init__(self):
        super().__init__("1024x64")


class IHP130_SRAM_2048x64(_IHP130SRAMLibrary):
    def __init__(self):
        super().__init__("2048x64")


class IHP130_SRAM_256x48(_IHP130SRAMLibrary):
    def __init__(self):
        super().__init__("256x48")


class IHP130_SRAM_256x64(_IHP130SRAMLibrary):
    def __init__(self):
        super().__init__("256x64")


class IHP130_SRAM_512x64(_IHP130SRAMLibrary):
    def __init__(self):
        super().__init__("512x64")


class IHP130_SRAM_64x64(_IHP130SRAMLibrary):
    def __init__(self):
        super().__init__("64x64")


class IHP130Lambdalib_SinglePort(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_spram", [
            IHP130_SRAM_1024x64,
            IHP130_SRAM_2048x64,
            IHP130_SRAM_256x48,
            IHP130_SRAM_256x64,
            IHP130_SRAM_512x64,
            IHP130_SRAM_64x64])
        self.set_name("ihp130_la_spram")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "ihp130", "libs", "sg13g2_sram")

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
    files.append(os.path.join(os.path.dirname(__file__), "sg13g2_sram",
                              "lambda", f"{spram.name}.v"))
    spram.write_lambdalib(
        files[-1],
        IHP130Lambdalib_SinglePort().techlibs)

    for f in files:
        format_verilog(f, args.verible_bin)
