import argparse
import math

import os.path

from pathlib import Path

from typing import Dict, Tuple

from lambdalib import LambalibTechLibrary
from lambdapdk import LambdaLibrary, _LambdaPath
from lambdalib.ramlib import Spram, Dpram, Tdpram, RAMTechLib
from lambdapdk.asap7 import ASAP7PDK
from lambdapdk.utils import format_verilog


class _FakeRAM7Library(LambdaLibrary, RAMTechLib):
    def __init__(self, config):
        super().__init__()
        self.set_name(f"fakeram7_{config}")

        self.add_asic_pdk(ASAP7PDK())

        path_base = Path("lambdapdk", "asap7", "libs", "fakeram7")

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

    def __ram_props(self) -> Tuple[str, int, int]:
        """Returns the RAM properties (width, depth) based on the configuration."""
        type, size = self.name.split('_')[-2:]
        width = int(size.split('x')[1])
        depth = int(size.split('x')[0])
        return type, width, depth

    def get_ram_width(self) -> int:
        """Returns the width of the RAM cell.

        Returns:
            int: The width of the RAM cell.
        """
        _, width, _ = self.__ram_props()
        return width

    def get_ram_depth(self) -> int:
        """Returns the depth of the RAM cell.

        Returns:
            int: The depth of the RAM cell.
        """
        _, _, depth = self.__ram_props()
        return int(math.log2(depth))

    def get_ram_ports(self) -> Dict[str, str]:
        """Returns the port mapping for the RAM cell.

        Returns:
            Dict[str, str]: A dictionary mapping port names to their expressions.
        """
        type, _, _ = self.__ram_props()
        if type == "sp":
            return {
                "clk": "clk",
                "addr_in": "mem_addr",
                "ce_in": "ce_in",
                "rd_out": "mem_dout",
                "we_in": "we_in",
                "w_mask_in": "mem_wmask",
                "wd_in": "mem_din"
            }
        if type == "dp":
            return {
                "clk": "wr_clk",
                "addr_in_A": "wr_mem_addr",
                "addr_in_B": "rd_mem_addr",
                "ce_in": "wr_ce_in | rd_ce_in",
                "rd_out_A": "",
                "rd_out_B": "mem_dout",
                "we_in_A": "we_in",
                "we_in_B": "1'b0",
                "w_mask_in_A": "mem_wmask",
                "w_mask_in_B": "'b0",
                "wd_in_A": "mem_din",
                "wd_in_B": "'b0"
            }
        if type == "tdp":
            return {
                "clk_A": "clk_a",
                "clk_B": "clk_b",
                "addr_in_A": "mem_addrA",
                "addr_in_B": "mem_addrB",
                "ce_in_A": "ce_in_A",
                "ce_in_B": "ce_in_B",
                "rd_out_A": "mem_doutA",
                "rd_out_B": "mem_doutB",
                "we_in_A": "we_in_A",
                "we_in_B": "we_in_B",
                "w_mask_in_A": "mem_wmaskA",
                "w_mask_in_B": "mem_wmaskB",
                "wd_in_A": "mem_dinA",
                "wd_in_B": "mem_dinB"
            }

    def get_ram_libcell(self) -> str:
        """Returns the name of the RAM library cell.

        Returns:
            str: The name of the RAM library cell.
        """
        return self.name


class FakeRAM7_tdp_64x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("tdp_64x32")


class FakeRAM7_dp_64x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_64x32")


class FakeRAM7_sp_64x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_64x32")


class FakeRAM7_tdp_128x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("tdp_128x32")


class FakeRAM7_dp_128x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_128x32")


class FakeRAM7_sp_128x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_128x32")


class FakeRAM7_tdp_256x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("tdp_256x32")


class FakeRAM7_dp_256x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_256x32")


class FakeRAM7_sp_256x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_256x32")


class FakeRAM7_tdp_256x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("tdp_256x64")


class FakeRAM7_dp_256x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_256x64")


class FakeRAM7_sp_256x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_256x64")


class FakeRAM7_tdp_512x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("tdp_512x32")


class FakeRAM7_dp_512x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_512x32")


class FakeRAM7_sp_512x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_512x32")


class FakeRAM7_tdp_512x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("tdp_512x64")


class FakeRAM7_dp_512x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_512x64")


class FakeRAM7_sp_512x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_512x64")


class FakeRAM7_tdp_512x128(_FakeRAM7Library):
    def __init__(self):
        super().__init__("tdp_512x128")


class FakeRAM7_dp_512x128(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_512x128")


class FakeRAM7_sp_512x128(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_512x128")


class FakeRAM7_tdp_1024x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("tdp_1024x32")


class FakeRAM7_dp_1024x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_1024x32")


class FakeRAM7_sp_1024x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_1024x32")


class FakeRAM7_tdp_1024x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("tdp_1024x64")


class FakeRAM7_dp_1024x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_1024x64")


class FakeRAM7_sp_1024x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_1024x64")


class FakeRAM7_tdp_2048x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("tdp_2048x32")


class FakeRAM7_dp_2048x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_2048x32")


class FakeRAM7_sp_2048x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_2048x32")


class FakeRAM7_tdp_2048x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("tdp_2048x64")


class FakeRAM7_dp_2048x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_2048x64")


class FakeRAM7_sp_2048x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_2048x64")


class FakeRAM7_tdp_4096x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("tdp_4096x32")


class FakeRAM7_dp_4096x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_4096x32")


class FakeRAM7_sp_4096x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_4096x32")


class FakeRAM7_tdp_4096x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("tdp_4096x64")


class FakeRAM7_dp_4096x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_4096x64")


class FakeRAM7_sp_4096x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_4096x64")


class FakeRAM7_tdp_8192x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("tdp_8192x32")


class FakeRAM7_dp_8192x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_8192x32")


class FakeRAM7_sp_8192x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_8192x32")


class FakeRAM7_tdp_8192x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("tdp_8192x64")


class FakeRAM7_dp_8192x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_8192x64")


class FakeRAM7_sp_8192x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_8192x64")


class FakeRAM7Lambdalib_SinglePort(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_spram", [
            FakeRAM7_sp_64x32,
            FakeRAM7_sp_128x32,
            FakeRAM7_sp_256x32,
            FakeRAM7_sp_256x64,
            FakeRAM7_sp_512x32,
            FakeRAM7_sp_512x64,
            FakeRAM7_sp_512x128,
            FakeRAM7_sp_1024x32,
            FakeRAM7_sp_1024x64,
            FakeRAM7_sp_2048x32,
            FakeRAM7_sp_2048x64,
            FakeRAM7_sp_4096x32,
            FakeRAM7_sp_4096x64,
            FakeRAM7_sp_8192x32,
            FakeRAM7_sp_8192x64])
        self.set_name("fakeram7_la_spram")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "asap7", "libs", "fakeram7")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_spram.v")
                self.add_depfileset(Spram(), "rtl.impl")


class FakeRAM7Lambdalib_DoublePort(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_dpram", [
            FakeRAM7_dp_64x32,
            FakeRAM7_dp_128x32,
            FakeRAM7_dp_256x32,
            FakeRAM7_dp_256x64,
            FakeRAM7_dp_512x32,
            FakeRAM7_dp_512x64,
            FakeRAM7_dp_512x128,
            FakeRAM7_dp_1024x32,
            FakeRAM7_dp_1024x64,
            FakeRAM7_dp_2048x32,
            FakeRAM7_dp_2048x64,
            FakeRAM7_dp_4096x32,
            FakeRAM7_dp_4096x64,
            FakeRAM7_dp_8192x32,
            FakeRAM7_dp_8192x64])
        self.set_name("fakeram7_la_dpram")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "asap7", "libs", "fakeram7")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_dpram.v")
                self.add_depfileset(Dpram(), "rtl.impl")


class FakeRAM7Lambdalib_TrueDoublePort(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_tdpram", [
            FakeRAM7_tdp_64x32,
            FakeRAM7_tdp_128x32,
            FakeRAM7_tdp_256x32,
            FakeRAM7_tdp_256x64,
            FakeRAM7_tdp_512x32,
            FakeRAM7_tdp_512x64,
            FakeRAM7_tdp_512x128,
            FakeRAM7_tdp_1024x32,
            FakeRAM7_tdp_1024x64,
            FakeRAM7_tdp_2048x32,
            FakeRAM7_tdp_2048x64,
            FakeRAM7_tdp_4096x32,
            FakeRAM7_tdp_4096x64,
            FakeRAM7_tdp_8192x32,
            FakeRAM7_tdp_8192x64])
        self.set_name("fakeram7_la_tdpram")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "asap7", "libs", "fakeram7")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_tdpram.v")
                self.add_depfileset(Tdpram(), "rtl.impl")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--verible_bin',
                        metavar='<verible>',
                        required=True,
                        help='path to verible-verilog-format')
    args = parser.parse_args()

    files = []

    spram = Spram()
    files.append(os.path.join(os.path.dirname(__file__), "fakeram7", "lambda", f"{spram.name}.v"))
    spram.write_lambdalib(
        files[-1],
        FakeRAM7Lambdalib_SinglePort().techlibs)
    dpram = Dpram()
    files.append(os.path.join(os.path.dirname(__file__), "fakeram7", "lambda", f"{dpram.name}.v"))
    dpram.write_lambdalib(
        files[-1],
        FakeRAM7Lambdalib_DoublePort().techlibs)
    tdpram = Tdpram()
    files.append(os.path.join(os.path.dirname(__file__), "fakeram7", "lambda", f"{tdpram.name}.v"))
    tdpram.write_lambdalib(
        files[-1],
        FakeRAM7Lambdalib_TrueDoublePort().techlibs)

    for f in files:
        format_verilog(f, args.verible_bin)
