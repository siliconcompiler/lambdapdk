from siliconcompiler import Library
from lambdapdk import register_data_source


def setup(chip):
    libs = []
    stackup = '10M'

    register_data_source(chip)

    for config in ('64x32', '128x32', '256x32', '256x64', '512x32', '512x64'):
        mem_name = f'fakeram7_{config}'
        lib = Library(chip, mem_name)
        path_base = 'lambdapdk/asap7/libs/fakeram7'
        lib.add('output', stackup, 'lef', f'{path_base}/lef/{mem_name}.lef', package='lambdapdk')

        for corner in ('slow', 'fast', 'typical'):
            lib.add('output', corner, 'nldm', f'{path_base}/nldm/{mem_name}.lib',
                    package='lambdapdk')

        lib.set('option', 'file', 'openroad_pdngen', f'{path_base}/pdngen.tcl', package='lambdapdk')

        lib.set('option', 'var', 'klayout_allow_missing_cell', mem_name)

        libs.append(lib)

    return libs
