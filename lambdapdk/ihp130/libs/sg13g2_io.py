import os
import siliconcompiler
from lambdapdk import register_data_source
from lambdapdk.ihp130 import register_ihp130_data_source


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
