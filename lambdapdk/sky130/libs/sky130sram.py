import argparse
import math

import os.path

from pathlib import Path

from typing import Dict, Tuple

from lambdalib import LambalibTechLibrary
from lambdapdk import LambdaLibrary, _LambdaPath
from lambdalib.ramlib import Spram, RAMTechLib
from lambdapdk.sky130 import Sky130PDK, _Sky130Data
from lambdapdk.utils import format_verilog


class Sky130_SRAM_32x512(LambdaLibrary, RAMTechLib, _Sky130Data):
    def __init__(self):
        super().__init__()
        self.set_name('sky130_sram_2kbyte_1rw1r_32x512_8')

        self.add_asic_pdk(Sky130PDK())

        path_base = Path('lambdapdk', 'sky130', 'libs', "sky130sram")

        # The upstream archive carries four OpenRAM macros; this library
        # exposes the 2kbyte part.
        upstream_path = Path("sky130A", "libs.ref", "sky130_sram_macros")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("models.timing.nldm"):
                # Vendored, not referenced: upstream puts max_transition 0.04 on
                # the addr0/wmask0/addr1 buses, which no sky130hd cell can drive,
                # so the resizer fails with RSZ-0090 on any design using this
                # macro. This copy is the upstream liberty at pdk_rev with those
                # three lines removed -- regenerate it with
                # scripts/patch_sky130sram_maxtran.py. See PATCHES.md.
                self.add_file(path_base / self.name / "nldm" / f"{self.name}_TT_1p8V_25C.lib")
                self.add_asic_libcornerfileset("generic", "nldm")

        with self.active_dataroot("sky130_sram_macros"):
            with self.active_fileset("models.physical"):
                # Byte-identical to what this repo used to vendor.
                self.add_file(upstream_path / "lef" / f"{self.name}.lef")
                self.add_file(upstream_path / "gds" / f"{self.name}.gds")
                self.add_asic_aprfileset()

            with self.active_fileset("models.lvs"):
                # The upstream 'spice' view *is* the LVS netlist -- its header
                # says so, and it matches the copy this repo used to vendor
                # except that open_pdks strips the 'u' from the W=/L= device
                # parameters. That stripping is open_pdks' own transform, not
                # drift: fossi-foundation/sky130_sram_macros still writes 0.21u
                # at HEAD. This is the form open_pdks installs and the form its
                # netgen setup is written against.
                self.add_file(upstream_path / "spice" / f"{self.name}.spice",
                              filetype="cdl")
                self.add_asic_aprfileset()

        # There is no 'models.spice' fileset: open_pdks installs only the LVS
        # netlist, and the OpenRAM simulation netlist it omits was dropped rather
        # than carried here, since nothing in this repository can maintain it.

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

    def get_ram_defaultctrl_width(self) -> int:
        return 1

    def get_ram_defaultctrl(self) -> str:
        return "1'b0"

    def get_ram_libcell(self) -> str:
        """Returns the name of the RAM library cell.

        Returns:
            str: The name of the RAM library cell.
        """
        return self.name


class Sky130Lambdalib_SinglePort(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_spram", [
            Sky130_SRAM_32x512])
        self.set_name("sky130_la_spram")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "sky130", "libs", "sky130sram")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_spram.v")
                self.add_depfileset(Spram(), "rtl.impl")


class Sky130Lambdalib_SinglePortRegfile(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_spregfile",
                         Sky130Lambdalib_SinglePort().techlibs)
        self.set_name("sky130_la_spregfile")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "sky130", "libs", "sky130sram")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_spregfile.v")
                self.add_depfileset(Spram(), "rtl")


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
