from siliconcompiler import Chip, Library
from lambdapdk import register_data_source


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

        lib.set('option', 'file', 'openroad_pdngen', f'{path_base}/pdngen.tcl')

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
