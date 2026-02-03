from pathlib import Path

from lambdalib import LambalibTechLibrary
from lambdapdk import LambdaLibrary, _LambdaPath
from lambdapdk.asap7 import ASAP7PDK


class FakePLL7Library(LambdaLibrary):
    '''
    ASAP7 Fake PLL library.
    '''
    def __init__(self):
        super().__init__()
        self.set_name("fakepll7")

        self.add_asic_pdk(ASAP7PDK())

        path_base = Path("lambdapdk", "asap7", "libs", "fakepll7")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("models.physical"):
                self.add_file(path_base / "lef" / "fakepll7.lef")
                self.add_asic_aprfileset()

            with self.active_fileset("models.blackbox"):
                self.add_file(path_base / "model" / "fakepll7.v")
            self.add_yosys_blackbox_fileset("models.blackbox")


class FakePLL7Lambdalib_la_pll(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_pll", [FakePLL7Library])
        self.set_name("fakepll7_la_pll")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "asap7", "libs", "fakepll7")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_pll.v")
