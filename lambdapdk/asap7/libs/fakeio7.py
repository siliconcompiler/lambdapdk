import os
import siliconcompiler
from lambdapdk import register_data_source

from pathlib import Path

from lambdapdk import LambdaLibrary
from lambdapdk.asap7 import ASAP7PDK


class FakeIO7Library(LambdaLibrary):
    def __init__(self):
        super().__init__()
        self.set_name("fakeio7")

        self.add_asic_pdk(ASAP7PDK())

        path_base = Path("lambdapdk", "asap7", "libs", "fakeio7")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("models.physical"):
                self.add_file(path_base / "lef" / "fakeio7.lef")
                self.add_asic_aprfileset()

            with self.active_fileset("models.blackbox"):
                self.add_file(path_base / "blackbox" / "model.v")
            self.add_yosys_blackbox_fileset("models.blackbox")


def setup():
    '''
    ASAP7 Fake I/O library.
    '''
    libdir = "lambdapdk/asap7/libs/fakeio7/"

    lib = siliconcompiler.Library('asap7_fakeio7', package='lambdapdk')
    register_data_source(lib)

    # pdk
    lib.set('option', 'pdk', 'asap7')
    stackup = '10M'

    lib.set('output', stackup, 'lef', os.path.join(libdir, 'lef/fakeio7.lef'))

    lib.set('output', 'blackbox', 'verilog', os.path.join(libdir, 'blackbox', 'model.v'))

    lambda_lib = siliconcompiler.Library('lambdalib_iolib_asap7', package='lambdapdk')
    register_data_source(lambda_lib)
    lambda_lib.add('option', 'ydir', os.path.join(libdir, 'lambda'))
    lambda_lib.use(lib)
    lambda_lib.set('asic', 'macrolib', lib.design)

    return [lib, lambda_lib]


#########################
if __name__ == "__main__":
    for lib in setup(siliconcompiler.Chip('<lib>')):
        lib.write_manifest(f'{lib.top()}.json')
