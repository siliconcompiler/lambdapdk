from siliconcompiler import DesignSchema
from lambdapdk import register_data_source

from pathlib import Path

from lambdapdk import LambdaLibrary, _LambdaPath, LambalibTechLibrary
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
                    self.add_asic_libcornerfileset("typical", "nldm")

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


def setup():
    libs = []
    stackup = '10M'

    for config in ('64x32', '128x32', '256x32', '256x64',
                   '512x32', '512x64', '512x128',
                   '1024x32', '1024x64',
                   '2048x32', '2048x64',
                   '4096x32', '4096x64',
                   '8192x32', '8192x64'):
        for ramtype in ('dp', 'sp'):
            mem_name = f'fakeram7_{ramtype}_{config}'
            lib = Library(mem_name, package='lambdapdk')
            register_data_source(lib)
            path_base = 'lambdapdk/asap7/libs/fakeram7'
            lib.add('output', stackup, 'lef', f'{path_base}/lef/{mem_name}.lef')

            for corner in ('slow', 'fast', 'typical'):
                lib.add('output', corner, 'nldm', f'{path_base}/nldm/{mem_name}.lib')

            lib.set('option', 'file', 'openroad_pdngen',
                    f'{path_base}/apr/openroad/pdngen.tcl')
            lib.set('option', 'file', 'openroad_global_connect',
                    f'{path_base}/apr/openroad/global_connect.tcl')

            lib.set('option', 'var', 'klayout_allow_missing_cell', mem_name)

            libs.append(lib)

    lambda_lib = Library('lambdalib_fakeram7', package='lambdapdk')
    register_data_source(lambda_lib)
    lambda_lib.add('option', 'ydir', 'lambdapdk/asap7/libs/fakeram7/lambda')
    for lib in libs:
        lambda_lib.use(lib)
        lambda_lib.add('asic', 'macrolib', lib.design)

    libs.append(lambda_lib)

    return libs
