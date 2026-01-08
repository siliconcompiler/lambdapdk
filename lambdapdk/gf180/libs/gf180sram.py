import argparse
import math

import os.path

from pathlib import Path

from typing import Dict, Tuple

from lambdalib import LambalibTechLibrary
from lambdapdk import LambdaLibrary, _LambdaPath
from lambdalib.ramlib import Spram, RAMTechLib
from lambdapdk.gf180 import GF180_3LM_1TM_6K_7t, \
    GF180_3LM_1TM_6K_9t, \
    GF180_3LM_1TM_9K_7t, \
    GF180_3LM_1TM_9K_9t, \
    GF180_3LM_1TM_11K_7t, \
    GF180_3LM_1TM_11K_9t, \
    GF180_3LM_1TM_30K_7t, \
    GF180_3LM_1TM_30K_9t, \
    GF180_4LM_1TM_6K_7t, \
    GF180_4LM_1TM_6K_9t, \
    GF180_4LM_1TM_9K_7t, \
    GF180_4LM_1TM_9K_9t, \
    GF180_4LM_1TM_11K_7t, \
    GF180_4LM_1TM_11K_9t, \
    GF180_4LM_1TM_30K_7t, \
    GF180_4LM_1TM_30K_9t, \
    GF180_5LM_1TM_9K_7t, \
    GF180_5LM_1TM_9K_9t, \
    GF180_5LM_1TM_11K_7t, \
    GF180_5LM_1TM_11K_9t, \
    GF180_6LM_1TM_9K_7t, \
    GF180_6LM_1TM_9K_9t
from lambdapdk.utils import format_verilog


class _GF180SRAMLibrary(LambdaLibrary, RAMTechLib):
    def __init__(self, config):
        super().__init__()
        self.set_name(f"gf180mcu_fd_ip_sram__sram{config}m8wm1")

        self.add_asic_pdk(GF180_3LM_1TM_6K_7t(), default=False)
        self.add_asic_pdk(GF180_3LM_1TM_6K_9t(), default=False)
        self.add_asic_pdk(GF180_3LM_1TM_9K_7t(), default=False)
        self.add_asic_pdk(GF180_3LM_1TM_9K_9t(), default=False)
        self.add_asic_pdk(GF180_3LM_1TM_11K_7t(), default=False)
        self.add_asic_pdk(GF180_3LM_1TM_11K_9t(), default=False)
        self.add_asic_pdk(GF180_3LM_1TM_30K_7t(), default=False)
        self.add_asic_pdk(GF180_3LM_1TM_30K_9t(), default=False)
        self.add_asic_pdk(GF180_4LM_1TM_6K_7t(), default=False)
        self.add_asic_pdk(GF180_4LM_1TM_6K_9t(), default=False)
        self.add_asic_pdk(GF180_4LM_1TM_9K_7t(), default=False)
        self.add_asic_pdk(GF180_4LM_1TM_9K_9t(), default=False)
        self.add_asic_pdk(GF180_4LM_1TM_11K_7t(), default=False)
        self.add_asic_pdk(GF180_4LM_1TM_11K_9t(), default=False)
        self.add_asic_pdk(GF180_4LM_1TM_30K_7t(), default=False)
        self.add_asic_pdk(GF180_4LM_1TM_30K_9t(), default=False)
        self.add_asic_pdk(GF180_5LM_1TM_9K_7t(), default=False)
        self.add_asic_pdk(GF180_5LM_1TM_9K_9t(), default=False)
        self.add_asic_pdk(GF180_5LM_1TM_11K_7t(), default=False)
        self.add_asic_pdk(GF180_5LM_1TM_11K_9t(), default=False)
        self.add_asic_pdk(GF180_6LM_1TM_9K_7t(), default=False)
        self.add_asic_pdk(GF180_6LM_1TM_9K_9t(), default=False)

        path_base = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_ip_sram")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("models.physical"):
                self.add_file(path_base / "lef" / f"{self.name}.lef")
                self.add_file(path_base / "gds" / f"{self.name}.gds.gz")
                self.add_asic_aprfileset()

            with self.active_fileset("models.lvs"):
                self.add_file(path_base / "cdl" / f"{self.name}.cdl")
                self.add_asic_aprfileset()

            for corner_name, filename in [
                    ('slow', f'{self.name}__ss_125C_4v50.lib.gz'),
                    ('typical', f'{self.name}__tt_025C_5v00.lib.gz'),
                    ('fast', f'{self.name}__ff_n40C_5v50.lib.gz')]:
                with self.active_fileset(f"models.timing.nldm.{corner_name}"):
                    self.add_file(path_base / "nldm" / filename)
                    self.add_asic_libcornerfileset(corner_name, "nldm")

            with self.active_fileset("models.spice"):
                self.add_file(path_base / "spice" / f"{self.name}.spice")

            with self.active_fileset("openroad.powergrid"):
                self.add_file(path_base / "apr" / "openroad" / "pdngen.tcl")
                self.add_openroad_powergridfileset()
            with self.active_fileset("openroad.globalconnect"):
                self.add_file(path_base / "apr" / "openroad" / "global_connect.tcl")

    def __ram_props(self) -> Tuple[int, int]:
        """Returns the RAM properties (width, depth) based on the configuration."""
        size = self.name.split('_')[-1][4:-5]
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
            "CLK": "clk",
            "CEN": "~ce_in",
            "GWEN": "~we_in",
            "WEN": "~mem_wmask",
            "A": "mem_addr",
            "D": "mem_din",
            "Q": "mem_dout"
        }

    def get_ram_libcell(self) -> str:
        """Returns the name of the RAM library cell.

        Returns:
            str: The name of the RAM library cell.
        """
        return self.name


class GF180_SRAM_64x8(_GF180SRAMLibrary):
    def __init__(self):
        super().__init__("64x8")


class GF180_SRAM_128x8(_GF180SRAMLibrary):
    def __init__(self):
        super().__init__("128x8")


class GF180_SRAM_256x8(_GF180SRAMLibrary):
    def __init__(self):
        super().__init__("256x8")


class GF180_SRAM_512x8(_GF180SRAMLibrary):
    def __init__(self):
        super().__init__("512x8")


class GF180Lambdalib_SinglePort(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_spram", [
            GF180_SRAM_64x8,
            GF180_SRAM_128x8,
            GF180_SRAM_256x8,
            GF180_SRAM_512x8])
        self.set_name("gf180_la_spram")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_ip_sram")

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
    files.append(os.path.join(os.path.dirname(__file__), "gf180mcu_fd_ip_sram",
                              "lambda", f"{spram.name}.v"))
    spram.write_lambdalib(
        files[-1],
        GF180Lambdalib_SinglePort().techlibs)

    for f in files:
        format_verilog(f, args.verible_bin)
