from siliconcompiler import Chip, Library
from lambdapdk import register_data_source
from lambdapdk.ihp130 import register_ihp130_data_source


def setup():
    libs = []
    stackup = '5M2TL'

    for config in ('1024x64', '2048x64', '256x48', '256x64', '512x64', '64x64'):
        mem_name = f'RM_IHPSG13_1P_{config}_c2_bm_bist'
        lib = Library(mem_name, package='ihp130')
        register_ihp130_data_source(lib)
        register_data_source(lib)
        path_base = 'ihp-sg13g2/libs.ref/sg13g2_sram'
        lib.add('output', stackup, 'lef', f'{path_base}/lef/{mem_name}.lef')
        lib.add('output', stackup, 'gds', f'{path_base}/gds/{mem_name}.gds')
        lib.add('output', stackup, 'cdl', f'{path_base}/spice/{mem_name}.cdl')

        lib.add('output', 'typ', 'nldm', f'{path_base}/lib/{mem_name}_typ_1p20V_25C.lib')
        lib.add('output', 'slow', 'nldm', f'{path_base}/lib/{mem_name}_slow_1p08V_125C.lib')
        lib.add('output', 'fast', 'nldm', f'{path_base}/lib/{mem_name}_fast_1p32V_m55C.lib')

        lib.add('output', 'rtl', 'verilog', f'{path_base}/verilog/{mem_name}.v')
        lib.add('output', 'rtl', 'verilog',
                f'{path_base}/verilog/RM_IHPSG13_1P_core_behavioral_bm_bist.v')

        lib.set('option', 'file', 'openroad_pdngen',
                'lambdapdk/ihp130/libs/sg13g2_sram/pdngen.tcl',
                package='lambdapdk')

        libs.append(lib)

    lambda_lib = Library('lambdalib_sg13g2_sram', package='lambdapdk')
    register_data_source(lambda_lib)
    lambda_lib.add('option', 'ydir', 'lambdapdk/ihp130/libs/sg13g2_sram/lambda')
    for lib in libs:
        lambda_lib.use(lib)
        lambda_lib.add('asic', 'macrolib', lib.design)

    libs.append(lambda_lib)

    return libs


#########################
if __name__ == "__main__":
    for lib in setup(Chip('<lib>')):
        lib.write_manifest(f'{lib.top()}.json')
