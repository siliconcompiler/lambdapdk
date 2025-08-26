from pathlib import Path

from lambdapdk import LambdaLibrary
from lambdapdk.ihp130 import IHP130PDK, _IHP130Path


class _IHP130_IOLibrary(LambdaLibrary, _IHP130Path):
    '''
    IHP 130 IO Cells
    '''
    def __init__(self, voltage):
        super().__init__()
        self.set_name(f"sg13g2_io_{voltage}")

        path_base = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        self.add_asic_pdk(IHP130PDK())

        with self.active_dataroot("ihp130"):
            if voltage == "1p2V":
                for corner_name, filename in [
                        ('slow', 'sg13g2_io_slow_1p08V_3p0V_125C.lib'),
                        ('typical', 'sg13g2_io_typ_1p2V_3p3V_25C.lib'),
                        ('fast', 'sg13g2_io_fast_1p32V_3p6V_m40C.lib')]:
                    with self.active_fileset(f"models.timing.{corner_name}.nldm"):
                        self.add_file(f"ihp-sg13g2/libs.ref/sg13g2_io/lib/{filename}")
                        self.add_asic_libcornerfileset(corner_name, "nldm")
            else:
                for corner_name, filename in [
                        ('slow', 'sg13g2_io_slow_1p35V_3p0V_125C.lib'),
                        ('typical', 'sg13g2_io_typ_1p5V_3p3V_25C.lib'),
                        ('fast', 'sg13g2_io_fast_1p65V_3p6V_m40C.lib')]:
                    with self.active_fileset(f"models.timing.{corner_name}.nldm"):
                        self.add_file(f"ihp-sg13g2/libs.ref/sg13g2_io/lib/{filename}")
                        self.add_asic_libcornerfileset(corner_name, "nldm")

            with self.active_fileset("models.spice"):
                self.add_file("ihp-sg13g2/libs.ref/sg13g2_io/spice/sg13g2_io.spi", filetype="spice")

        with self.active_dataroot("ihp130"):
            with self.active_fileset("models.physical"):
                self.add_file("ihp-sg13g2/libs.ref/sg13g2_io/lef/sg13g2_io.lef")
                self.add_file("ihp-sg13g2/libs.ref/sg13g2_io/gds/sg13g2_io.gds")
                self.add_asic_aprfileset()

            with self.active_fileset("models.lvs"):
                self.add_file("ihp-sg13g2/libs.ref/sg13g2_io/cdl/sg13g2_io.cdl")
                self.add_asic_aprfileset()

        self.add_asic_celllist('filler', ['sg13g2_Filler200',
                                          'sg13g2_Filler400',
                                          'sg13g2_Filler1000',
                                          'sg13g2_Filler2000',
                                          'sg13g2_Filler4000',
                                          'sg13g2_Filler10000'])

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("models.blackbox"):
                self.add_file(path_base / "blackbox" / "sg13g2_io.v")
            self.add_yosys_blackbox_fileset("models.blackbox")


class IHP130_IO_1p2(_IHP130_IOLibrary):
    def __init__(self):
        super().__init__("1p2")


class IHP130_IO_1p5(_IHP130_IOLibrary):
    def __init__(self):
        super().__init__("1p5")
