from pathlib import Path

from lambdalib import LambalibTechLibrary
from lambdapdk import LambdaLibrary, _LambdaPath
from lambdapdk.freepdk45 import FreePDK45PDK


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

            self.add_openroad_power_grid_file(path_base / "apr" / "openroad" / "pdngen.tcl")
            self.add_openroad_global_connect_file(
                path_base / "apr" / "openroad" / "global_connect.tcl")

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
        self.set_version("v1")

        lib_path = Path("lambdapdk", "freepdk45", "libs", "fakeram45")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_spram.v")
