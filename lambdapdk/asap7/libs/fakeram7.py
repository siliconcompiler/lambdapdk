from pathlib import Path

from lambdalib import LambalibTechLibrary
from lambdapdk import LambdaLibrary, _LambdaPath
from lambdapdk.asap7 import ASAP7PDK


class _FakeRAM7Library(LambdaLibrary):
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

            self.add_openroad_power_grid_file(path_base / "apr" / "openroad" / "pdngen.tcl")
            self.add_openroad_global_connect_file(
                path_base / "apr" / "openroad" / "global_connect.tcl")

            self.add_klayout_allowmissingcell(self.name)


class FakeRAM7_dp_64x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_64x32")


class FakeRAM7_sp_64x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_64x32")


class FakeRAM7_dp_128x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_128x32")


class FakeRAM7_sp_128x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_128x32")


class FakeRAM7_dp_256x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_256x32")


class FakeRAM7_sp_256x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_256x32")


class FakeRAM7_dp_256x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_256x64")


class FakeRAM7_sp_256x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_256x64")


class FakeRAM7_dp_512x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_512x32")


class FakeRAM7_sp_512x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_512x32")


class FakeRAM7_dp_512x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_512x64")


class FakeRAM7_sp_512x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_512x64")


class FakeRAM7_dp_512x128(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_512x128")


class FakeRAM7_sp_512x128(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_512x128")


class FakeRAM7_dp_1024x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_1024x32")


class FakeRAM7_sp_1024x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_1024x32")


class FakeRAM7_dp_1024x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_1024x64")


class FakeRAM7_sp_1024x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_1024x64")


class FakeRAM7_dp_2048x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_2048x32")


class FakeRAM7_sp_2048x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_2048x32")


class FakeRAM7_dp_2048x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_2048x64")


class FakeRAM7_sp_2048x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_2048x64")


class FakeRAM7_dp_4096x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_4096x32")


class FakeRAM7_sp_4096x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_4096x32")


class FakeRAM7_dp_4096x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_4096x64")


class FakeRAM7_sp_4096x64(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_4096x64")


class FakeRAM7_dp_8192x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("dp_8192x32")


class FakeRAM7_sp_8192x32(_FakeRAM7Library):
    def __init__(self):
        super().__init__("sp_8192x32")


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
        self.set_version("v1")

        lib_path = Path("lambdapdk", "asap7", "libs", "fakeram7")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_spram.v")


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
        self.set_version("v1")

        lib_path = Path("lambdapdk", "asap7", "libs", "fakeram7")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_dpram.v")
