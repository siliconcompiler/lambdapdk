import os
import siliconcompiler
from lambdapdk import register_data_source
from lambdapdk.ihp130 import register_ihp130_data_source

from pathlib import Path

from lambdapdk import LambdaLibrary
from lambdapdk.ihp130 import IHP130PDK, _IHP130Path


class _IHP130_IOLibrary(LambdaLibrary, _IHP130Path):
    def __init__(self, voltage):
        super().__init__()
        self.set_name(f"sg13g2_io_{voltage}")

        path_base = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        self.add_asic_pdk(IHP130PDK())

        with self.active_dataroot("ihp130"):
            if voltage == "1p2V":
                for corner_name, filename in [
                        ('slow', 'sg13g2_io_slow_1p08V_3p0V_125C.lib'),
                        ('typical', 'sg13g2_io_typ_1p2V_3p3V_25C.lib'),
                        ('fast', 'sg13g2_io_fast_1p32V_3p6V_m40C.lib')]:
                    with self.active_fileset(f"models.timing.{corner_name}.nldm"):
                        self.add_file(f"ihp-sg13g2/libs.ref/sg13g2_io/lib/{filename}")
                        self.add_asic_libcornerfileset(corner_name, "nldm")
            else:
                for corner_name, filename in [
                        ('slow', 'sg13g2_io_slow_1p35V_3p0V_125C.lib'),
                        ('typical', 'sg13g2_io_typ_1p5V_3p3V_25C.lib'),
                        ('fast', 'sg13g2_io_fast_1p65V_3p6V_m40C.lib')]:
                    with self.active_fileset(f"models.timing.{corner_name}.nldm"):
                        self.add_file(f"ihp-sg13g2/libs.ref/sg13g2_io/lib/{filename}")
                        self.add_asic_libcornerfileset(corner_name, "nldm")

            with self.active_fileset("models.spice"):
                self.add_file("ihp-sg13g2/libs.ref/sg13g2_io/spice/sg13g2_io.spi", filetype="spice")

        with self.active_dataroot("ihp130"):
            with self.active_fileset("models.physical"):
                self.add_file("ihp-sg13g2/libs.ref/sg13g2_io/lef/sg13g2_io.lef")
                self.add_file("ihp-sg13g2/libs.ref/sg13g2_io/gds/sg13g2_io.gds")
                self.add_asic_aprfileset()

            with self.active_fileset("models.lvs"):
                self.add_file("ihp-sg13g2/libs.ref/sg13g2_io/cdl/sg13g2_io.cdl")
                self.add_asic_aprfileset()

        self.add_asic_celllist('filler', ['sg13g2_Filler200',
                                          'sg13g2_Filler400',
                                          'sg13g2_Filler1000',
                                          'sg13g2_Filler2000',
                                          'sg13g2_Filler4000',
                                          'sg13g2_Filler10000'])

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("models.blackbox"):
                self.add_file(path_base / "blackbox" / "sg13g2_io.v")
            self.add_yosys_blackbox_fileset("models.blackbox")


class IHP130_IO_1p2(_IHP130_IOLibrary):
    def __init__(self):
        super().__init__("1p2")


class IHP130_IO_1p5(_IHP130_IOLibrary):
    def __init__(self):
        super().__init__("1p5")


def setup():
    '''
    IHP 130 IO Cells
    '''
    libdir = "lambdapdk/ihp130/libs/sg13g2_io"

    lib = siliconcompiler.Library('sg13g2_io', package='ihp130')
    register_ihp130_data_source(lib)
    register_data_source(lib)

    # pdk
    lib.set('option', 'pdk', 'ihp130')

    lib.set('output', 'slow', 'nldm',
            'ihp-sg13g2/libs.ref/sg13g2_io/lib/sg13g2_io_slow_1p08V_3p0V_125C.lib')
    lib.set('output', 'typical', 'nldm',
            'ihp-sg13g2/libs.ref/sg13g2_io/lib/sg13g2_io_typ_1p5V_3p3V_25C.lib')
    lib.set('output', 'fast', 'nldm',
            'ihp-sg13g2/libs.ref/sg13g2_io/lib/sg13g2_io_fast_1p32V_3p6V_m40C.lib')

    for corner in ('slow', 'typical', 'fast'):
        lib.set('output', corner, 'spice',
                'ihp-sg13g2/libs.ref/sg13g2_io/spice/sg13g2_io.spi')

    lib.set('output', '5M2TL', 'lef', 'ihp-sg13g2/libs.ref/sg13g2_io/lef/sg13g2_io.lef')
    lib.set('output', '5M2TL', 'cdl', 'ihp-sg13g2/libs.ref/sg13g2_io/cdl/sg13g2_io.cdl')
    lib.add('output', '5M2TL', 'gds', 'ihp-sg13g2/libs.ref/sg13g2_io/gds/sg13g2_io.gds')

    lib.set('asic', 'cells', 'filler', ['sg13g2_Filler200',
                                        'sg13g2_Filler400',
                                        'sg13g2_Filler1000',
                                        'sg13g2_Filler2000',
                                        'sg13g2_Filler4000',
                                        'sg13g2_Filler10000'])

    lib.set('output', 'blackbox', 'verilog',
            os.path.join(libdir, 'blackbox', 'sg13g2_io.v'), package='lambdapdk')

    lambda_lib = siliconcompiler.Library('lambdalib_sg13g2_io', package='lambdapdk')
    register_data_source(lambda_lib)
    lambda_lib.add('option', 'ydir', os.path.join(libdir, 'lambda'))
    lambda_lib.use(lib)
    lambda_lib.set('asic', 'macrolib', lib.design)

    return [lib, lambda_lib]


#########################
if __name__ == "__main__":
    for lib in setup(siliconcompiler.Chip('<lib>')):
        lib.write_manifest(f'{lib.top()}.json')
