from siliconcompiler import Chip, Library
from lambdapdk import register_data_source

from pathlib import Path

from lambdapdk import LambdaLibrary, _LambdaPath, LambalibTechLibrary
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
                for corner_name in ['slow', 'typical', 'fast']:
                    self.add_asic_libcornerfileset(corner_name, "nldm")

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


def setup():
    libs = []
    stackup = '5M1LI'

    for config in ('64x256',):
        mem_name = f'sky130_sram_1rw1r_{config}_8'
        lib = Library(mem_name, package='lambdapdk')
        register_data_source(lib)
        path_base = 'lambdapdk/sky130/libs/sky130sram'
        lib.add('output', stackup, 'lef', f'{path_base}/{mem_name}/lef/{mem_name}.lef.gz')
        lib.add('output', stackup, 'gds', f'{path_base}/{mem_name}/gds/{mem_name}.gds')
        lib.add('output', stackup, 'cdl', f'{path_base}/{mem_name}/spice/{mem_name}.lvs.sp')

        for corner in ('slow', 'fast', 'typical'):
            lib.add('output', corner, 'nldm',
                    f'{path_base}/{mem_name}/nldm/{mem_name}_TT_1p8V_25C.lib')
            lib.add('output', corner, 'spice', f'{path_base}/{mem_name}/spice/{mem_name}.sp')

        lib.set('option', 'file', 'openroad_pdngen',
                f'{path_base}/apr/openroad/pdngen.tcl')
        lib.set('option', 'file', 'openroad_global_connect',
                f'{path_base}/apr/openroad/global_connect.tcl')

        libs.append(lib)

    lambda_lib = Library('lambdalib_sky130sram', package='lambdapdk')
    register_data_source(lambda_lib)
    lambda_lib.add('option', 'ydir', 'lambdapdk/sky130/libs/sky130sram/lambda')
    for lib in libs:
        lambda_lib.use(lib)
        lambda_lib.add('asic', 'macrolib', lib.design)

    libs.append(lambda_lib)

    return libs


#########################
if __name__ == "__main__":
    for lib in setup(Chip('<lib>')):
        lib.write_manifest(f'{lib.top()}.json')
