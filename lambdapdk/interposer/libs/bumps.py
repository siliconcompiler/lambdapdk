import os
import siliconcompiler

from pathlib import Path

from lambdapdk import register_data_source
from lambdapdk.interposer import stackups

from lambdapdk import LambdaLibrary

from lambdapdk.interposer import Interposer_3ML_0400, \
    Interposer_3ML_0800, \
    Interposer_3ML_2000, \
    Interposer_3ML_0400_2000, \
    Interposer_4ML_0400, \
    Interposer_4ML_0800, \
    Interposer_4ML_2000, \
    Interposer_4ML_0400_2000, \
    Interposer_5ML_0400, \
    Interposer_5ML_0800, \
    Interposer_5ML_2000, \
    Interposer_5ML_0400_2000


class BumpLibrary(LambdaLibrary):
    def __init__(self):
        super().__init__()
        self.set_name("interposer_bumps")

        path_base = Path("lambdapdk", "interposer", "libs", 'bumps')

        self.add_asic_pdk(Interposer_3ML_0400(), default=False)
        self.add_asic_pdk(Interposer_3ML_0800(), default=False)
        self.add_asic_pdk(Interposer_3ML_2000(), default=False)
        self.add_asic_pdk(Interposer_3ML_0400_2000(), default=False)
        self.add_asic_pdk(Interposer_4ML_0400(), default=False)
        self.add_asic_pdk(Interposer_4ML_0800(), default=False)
        self.add_asic_pdk(Interposer_4ML_2000(), default=False)
        self.add_asic_pdk(Interposer_4ML_0400_2000(), default=False)
        self.add_asic_pdk(Interposer_5ML_0400(), default=False)
        self.add_asic_pdk(Interposer_5ML_0800(), default=False)
        self.add_asic_pdk(Interposer_5ML_2000(), default=False)
        self.add_asic_pdk(Interposer_5ML_0400_2000(), default=False)

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("models.physical"):
                self.add_file(path_base / "lef" / "bumps.lef")
                self.add_file(path_base / "gds" / "bumps.gds")
                self.add_asic_aprfileset()


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
