import argparse
import math

import os.path

from pathlib import Path

from typing import Dict, Tuple

from lambdalib import LambalibTechLibrary
from lambdapdk import LambdaLibrary, _LambdaPath
from lambdalib.ramlib import Dpram, RAMTechLib
from lambdapdk.sky130 import Sky130PDK, _Sky130Data
from lambdapdk.utils import format_verilog

# The OpenRAM macros upstream publishes, minus 'sram_1rw1r_32_256_8_sky130'
# which is known to have issues.
#
# Every one is 1rw1r -- port 0 reads and writes, port 1 only reads -- which is
# the shape la_dpram describes (one write port plus one read port), so that is
# the only mapping here. la_spram wraps la_dpram.
_MACROS = (
    "sky130_sram_1kbyte_1rw1r_32x256_8",
    "sky130_sram_1kbyte_1rw1r_8x1024_8",
    "sky130_sram_2kbyte_1rw1r_32x512_8",
)


class _Sky130_SRAM(LambdaLibrary, RAMTechLib, _Sky130Data):
    '''
    One OpenRAM macro, mapped as the dual-port cell it is.
    '''
    def __init__(self, macro: str):
        super().__init__()
        self.set_name(macro)
        self.package.set_version(self.PDK_VERSION)

        self.add_asic_pdk(Sky130PDK())

        path_base = Path('lambdapdk', 'sky130', 'libs', "sky130sram")
        upstream_path = Path("sky130A", "libs.ref", "sky130_sram_macros")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("models.timing.nldm"):
                # Vendored, not referenced: upstream puts max_transition 0.04 on
                # the addr0/wmask0/addr1 buses of every one of these macros,
                # which no sky130hd cell can drive, so the resizer fails with
                # RSZ-0090 on any design using them. These copies are the
                # upstream liberty at pdk_rev with those three lines removed --
                # regenerate with scripts/patch_sky130sram_maxtran.py. See
                # PATCHES.md.
                self.add_file(path_base / self.name / "nldm" / f"{self.name}_TT_1p8V_25C.lib")
                self.add_asic_libcornerfileset("generic", "nldm")

        with self.active_dataroot("sky130_sram_macros"):
            with self.active_fileset("models.physical"):
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

    def _wmask(self) -> str:
        """Returns the wmask0 expression for this macro's width.

        The write size is 8 bits, so the macro takes one mask bit per byte where
        the lambda wrapper presents one per data bit. The 8-bit macro has a
        single mask bit and takes it unbraced.
        """
        width = self.get_ram_width()
        bits = [f"mem_wmask[{bit}]" for bit in range(width - 8, -1, -8)]
        if len(bits) == 1:
            return bits[0]
        return "{" + ", ".join(bits) + "}"

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

    def get_ram_ports(self) -> Dict[str, str]:
        """Returns the port mapping for the RAM cell.

        There is one map, the dual-port one, because that is what the hardware
        is: the read-write port carries the writes and the read-only port the
        reads, each with its own clock, enable and address. la_spram is built on
        top of la_dpram rather than mapping the macro a second way.

        ``csb0``, ``csb1`` and ``web0`` are active low on these macros -- the
        'b' is the bar -- while the lambda cell's enables are active high, so
        each is inverted here.

        Returns:
            Dict[str, str]: A dictionary mapping port names to their expressions.
        """
        return {
            "clk0": "wr_clk",
            "csb0": "~wr_ce_in",
            "web0": "~we_in",
            "wmask0": self._wmask(),
            "addr0": "wr_mem_addr",
            "din0": "mem_din",
            "dout0": "",
            "clk1": "rd_clk",
            "csb1": "~rd_ce_in",
            "addr1": "rd_mem_addr",
            "dout1": "mem_dout",
        }


class Sky130_SRAM_32x256(_Sky130_SRAM):
    def __init__(self):
        super().__init__("sky130_sram_1kbyte_1rw1r_32x256_8")


class Sky130_SRAM_8x1024(_Sky130_SRAM):
    def __init__(self):
        super().__init__("sky130_sram_1kbyte_1rw1r_8x1024_8")


class Sky130_SRAM_32x512(_Sky130_SRAM):
    def __init__(self):
        super().__init__("sky130_sram_2kbyte_1rw1r_32x512_8")


class Sky130Lambdalib_DualPort(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_dpram", [
            Sky130_SRAM_32x256,
            Sky130_SRAM_8x1024,
            Sky130_SRAM_32x512])
        self.set_name("sky130_la_dpram")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "sky130", "libs", "sky130sram")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_dpram.v")
                self.add_depfileset(Dpram(), "rtl.impl")


class Sky130Lambdalib_SinglePort(LambalibTechLibrary, _LambdaPath):
    """la_spram on top of la_dpram, the way la_spregfile sits on la_spram.

    The macros are 1rw1r, so the single-port cell is the dual-port cell with the
    write port enabled only on a write and the read port only on a read. Mapping
    them a second time would be a second chance to get the active-low controls
    wrong.
    """
    def __init__(self):
        dpram = Sky130Lambdalib_DualPort()

        super().__init__("la_spram", dpram.techlibs)
        self.set_name("sky130_la_spram")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "sky130", "libs", "sky130sram")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_spram.v")
                # The sky130 dpram, not lambdalib's generic one: this adapter
                # instantiates la_dpram, and depending on the generic cell would
                # leave it to an alias that the consumer may never apply --
                # giving the behavioural model instead of the macros.
                self.add_depfileset(dpram, "rtl")


class Sky130Lambdalib_SinglePortRegfile(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        spram = Sky130Lambdalib_SinglePort()

        super().__init__("la_spregfile", spram.techlibs)
        self.set_name("sky130_la_spregfile")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "sky130", "libs", "sky130sram")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_spregfile.v")
                self.add_depfileset(spram, "rtl")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--verible_bin',
                        metavar='<verible>',
                        required=True,
                        help='path to verible-verilog-format')
    args = parser.parse_args()

    # Only la_dpram is generated. la_spram and la_spregfile are hand-written
    # adapters that sit on top of it.
    lambda_dir = os.path.join(os.path.dirname(__file__), "sky130sram", "lambda")

    dpram = Dpram()
    path = os.path.join(lambda_dir, f"{dpram.name}.v")
    dpram.write_lambdalib(path, Sky130Lambdalib_DualPort().techlibs)

    format_verilog(path, args.verible_bin)
