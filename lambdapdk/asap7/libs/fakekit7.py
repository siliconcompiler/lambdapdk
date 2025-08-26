from pathlib import Path

from lambdapdk import LambdaLibrary
from lambdapdk.asap7 import ASAP7PDK


class FakeKit7Library(LambdaLibrary):
    '''
    ASAP7 Fake Chip Collatoral library.
    '''
    def __init__(self):
        super().__init__()
        self.set_name("fakekit7")

        self.add_asic_pdk(ASAP7PDK())

        path_base = Path("lambdapdk", "asap7", "libs", "fakekit7")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("models.physical"):
                self.add_file(path_base / "lef" / "tsv.lef")
                self.add_asic_aprfileset()
