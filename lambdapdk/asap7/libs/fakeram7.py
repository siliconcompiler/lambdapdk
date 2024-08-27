from siliconcompiler import Library
from lambdapdk import register_data_source


def setup():
    libs = []
    stackup = '10M'

    for config in ('64x32', '128x32', '256x32', '256x64', '512x32', '512x64'):
        mem_name = f'fakeram7_{config}'
        lib = Library(mem_name, package='lambdapdk')
        register_data_source(lib)
        path_base = 'lambdapdk/asap7/libs/fakeram7'
        lib.add('output', stackup, 'lef', f'{path_base}/lef/{mem_name}.lef')

        for corner in ('slow', 'fast', 'typical'):
            lib.add('output', corner, 'nldm', f'{path_base}/nldm/{mem_name}.lib')

        lib.set('option', 'file', 'openroad_pdngen', f'{path_base}/pdngen.tcl')

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
