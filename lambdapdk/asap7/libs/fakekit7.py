import os
import siliconcompiler
from lambdapdk import register_data_source

from pathlib import Path

from lambdapdk import LambdaLibrary
from lambdapdk.asap7 import ASAP7PDK


class FakeKit7Library(LambdaLibrary):
    def __init__(self):
        super().__init__()
        self.set_name("fakekit7")

        self.add_asic_pdk(ASAP7PDK())

        path_base = Path("lambdapdk", "asap7", "libs", "fakekit7")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("models.physical"):
                self.add_file(path_base / "lef" / "tsv.lef")
                self.add_asic_aprfileset()


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
