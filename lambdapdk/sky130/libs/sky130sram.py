from pathlib import Path

from lambdalib import LambalibTechLibrary
from lambdapdk import LambdaLibrary, _LambdaPath
from lambdapdk.sky130 import Sky130PDK


class Sky130_SRAM_64x256(LambdaLibrary):
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
            self.add_openroad_power_grid_file(path_base / "apr" / "openroad" / "pdngen.tcl")
            self.add_openroad_global_connect_file(
                path_base / "apr" / "openroad" / "global_connect.tcl")


class Sky130Lambdalib_SinglePort(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_spram", [
            Sky130_SRAM_64x256])
        self.set_name("sky130_la_spram")

        # version
        self.set_version("v1")

        lib_path = Path("lambdapdk", "sky130", "libs", "sky130sram")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_spram.v")
