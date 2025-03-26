import os
import siliconcompiler
from lambdapdk import register_data_source


def setup():
    '''
    ASAP7 Fake Chip Collatoral library.
    '''
    libdir = "lambdapdk/asap7/libs/fakekit7/"

    lib = siliconcompiler.Library('asap7_fakekit7', package='lambdapdk')
    register_data_source(lib)

    # pdk
    lib.set('option', 'pdk', 'asap7')
    stackup = '10M'

    lib.set('output', stackup, 'lef', os.path.join(libdir, 'lef/tsv.lef'))

    return lib


#########################
if __name__ == "__main__":
    lib = setup(siliconcompiler.Chip('<lib>'))
    lib.write_manifest(f'{lib.top()}.json')
