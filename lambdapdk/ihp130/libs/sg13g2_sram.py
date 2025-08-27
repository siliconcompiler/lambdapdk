from pathlib import Path

from lambdalib import LambalibTechLibrary
from lambdapdk import LambdaLibrary, _LambdaPath
from lambdapdk.ihp130 import IHP130PDK, _IHP130Path


class _IHP130SRAMLibrary(LambdaLibrary, _IHP130Path):
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
            self.add_openroad_power_grid_file(path_base / "apr" / "openroad" / "pdngen.tcl")
            self.add_openroad_global_connect_file(
                path_base / "apr" / "openroad" / "global_connect.tcl")


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
        self.set_version("v1")

        lib_path = Path("lambdapdk", "ihp130", "libs", "sg13g2_sram")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_spram.v")
