from siliconcompiler import Library
from lambdapdk import register_data_source

from pathlib import Path

from lambdapdk import LambdaLibrary, _LambdaPath, LambalibTechLibrary
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
                    self.add_asic_libcornerfileset("typical", "nldm")

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


def setup():
    libs = []
    stackup = '10M'
    corner = 'typical'

    for config in ('64x32', '128x32', '256x32', '256x64', '512x32', '512x64'):
        mem_name = f'fakeram45_{config}'
        lib = Library(mem_name, package='lambdapdk')
        register_data_source(lib)
        path_base = 'lambdapdk/freepdk45/libs/fakeram45'
        lib.add('output', stackup, 'lef', f'{path_base}/lef/{mem_name}.lef')
        lib.add('output', corner, 'nldm', f'{path_base}/nldm/{mem_name}.lib')

        lib.set('option', 'file', 'openroad_pdngen',
                f'{path_base}/apr/openroad/pdngen.tcl')
        lib.set('option', 'file', 'openroad_global_connect',
                f'{path_base}/apr/openroad/global_connect.tcl')

        lib.set('option', 'var', 'klayout_allow_missing_cell', mem_name)

        libs.append(lib)

    lambda_lib = Library('lambdalib_fakeram45', package='lambdapdk')
    register_data_source(lambda_lib)
    lambda_lib.add('option', 'ydir', 'lambdapdk/freepdk45/libs/fakeram45/lambda')
    for lib in libs:
        lambda_lib.use(lib)
        lambda_lib.add('asic', 'macrolib', lib.design)

    libs.append(lambda_lib)

    return libs
