import os
import siliconcompiler
from lambdapdk import register_data_source
from lambdapdk.interposer import stackups


def setup():
    '''
    Interposer bump library
    '''
    libdir = "lambdapdk/interposer/libs/bumps/"

    lib = siliconcompiler.Library('interposer_bumps', package='lambdapdk')
    register_data_source(lib)

    # pdk
    lib.set('option', 'pdk', 'interposer')

    for stackup in stackups:
        lib.set('output', stackup, 'lef',
                os.path.join(libdir, 'lef/bumps.lef'))
        lib.add('output', stackup, 'gds',
                os.path.join(libdir, 'gds/bumps.gds'))

    return lib


#########################
if __name__ == "__main__":
    lib = setup(siliconcompiler.Chip('<lib>'))
    lib.write_manifest(f'{lib.top()}.json')
