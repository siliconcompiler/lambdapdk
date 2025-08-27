from pathlib import Path

from lambdapdk import LambdaLibrary
from lambdapdk.asap7 import ASAP7PDK


class FakeIO7Library(LambdaLibrary):
    '''
    ASAP7 Fake I/O library.
    '''
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
