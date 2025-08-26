from pathlib import Path

from lambdapdk import LambdaLibrary
from lambdapdk.ihp130 import IHP130PDK, _IHP130Path


class _IHP130StdCell(LambdaLibrary, _IHP130Path):
    '''
    Standard cell library for IHP130
    '''
    def __init__(self, voltage):
        super().__init__()
        self.set_name(f"sg13g2_stdcell_{voltage}")

        self.add_asic_pdk(IHP130PDK())

        self.add_asic_site("CoreSite")

        lib_path = Path('lambdapdk', "ihp130", 'libs', "sg13g2_stdcell")

        with self.active_dataroot("ihp130"):
            if voltage == "1p2V":
                for corner_name, filename in [
                        ('slow', 'sg13g2_stdcell_slow_1p08V_125C.lib'),
                        ('typical', 'sg13g2_stdcell_typ_1p20V_25C.lib'),
                        ('fast', 'sg13g2_stdcell_fast_1p32V_m40C.lib')]:
                    with self.active_fileset(f"models.timing.{corner_name}.nldm"):
                        self.add_file(f"ihp-sg13g2/libs.ref/sg13g2_stdcell/lib/{filename}")
                        self.add_asic_libcornerfileset(corner_name, "nldm")
            else:
                for corner_name, filename in [
                        ('slow', 'sg13g2_stdcell_slow_1p35V_125C.lib'),
                        ('typical', 'sg13g2_stdcell_typ_1p50V_25C.lib'),
                        ('fast', 'sg13g2_stdcell_fast_1p65V_m40C.lib')]:
                    with self.active_fileset(f"models.timing.{corner_name}.nldm"):
                        self.add_file(f"ihp-sg13g2/libs.ref/sg13g2_stdcell/lib/{filename}")
                        self.add_asic_libcornerfileset(corner_name, "nldm")

            with self.active_fileset("models.spice"):
                self.add_file("ihp-sg13g2/libs.ref/sg13g2_stdcell/spice/sg13g2_stdcell.spice")

        with self.active_dataroot("ihp130"):
            with self.active_fileset("models.physical"):
                self.add_file("ihp-sg13g2/libs.ref/sg13g2_stdcell/lef/sg13g2_stdcell.lef")
                self.add_file("ihp-sg13g2/libs.ref/sg13g2_stdcell/gds/sg13g2_stdcell.gds")
                self.add_asic_aprfileset()

            with self.active_fileset("models.lvs"):
                self.add_file("ihp-sg13g2/libs.ref/sg13g2_stdcell/cdl/sg13g2_stdcell.cdl")
                self.add_asic_aprfileset()

            with self.active_fileset("rtl"):
                self.add_file("ihp-sg13g2/libs.ref/sg13g2_stdcell/verilog/sg13g2_stdcell.v")
                self.add_asic_aprfileset()

        # tie cells
        self.add_asic_celllist('tie', ["sg13g2_tiehi",
                                       "sg13g2_tielo"])

        # hold cells
        self.add_asic_celllist('hold', ["sg13g2_dlygate4sd1_1",
                                        "sg13g2_dlygate4sd2_1",
                                        "sg13g2_dlygate4sd3_1"])

        # filler
        self.add_asic_celllist('filler', ["sg13g2_fill_1",
                                          "sg13g2_fill_2",
                                          "sg13g2_fill_4",
                                          "sg13g2_fill_8"])

        # decap
        self.add_asic_celllist('decap', ["sg13g2_decap_4",
                                         "sg13g2_decap_8"])

        # antenna
        self.add_asic_celllist('antenna', ["sg13g2_antennanp"])

        # Dont use
        self.add_asic_celllist('dontuse', ["sg13g2_lgcp_1",
                                           "sg13g2_sighold",
                                           "sg13g2_slgcp_1",
                                           "sg13g2_dfrbp_2"])

        # Setup for yosys
        with self.active_dataroot("lambdapdk"):
            self.set_yosys_driver_cell("sg13g2_buf_4")
            self.set_yosys_buffer_cell("sg13g2_buf_4", "A", "X")
            self.set_yosys_tielow_cell("sg13g2_tielo", "L_LO")
            self.set_yosys_tiehigh_cell("sg13g2_tiehi", "L_HI")
            self.set_yosys_abc(1000, 17)
            self.set_yosys_tristatebuffer_map(
                lib_path / "techmap" / "yosys" / "cells_tristatebuf.v")
            self.add_yosys_tech_map(lib_path / "techmap" / "yosys" / "cells_latch.v")

        # Setup for OpenROAD
        with self.active_dataroot("lambdapdk"):
            self.set_openroad_placement_density(0.65)
            self.set_openroad_tielow_cell("sg13g2_tielo", "L_LO")
            self.set_openroad_tiehigh_cell("sg13g2_tiehi", "L_HI")
            self.set_openroad_macro_placement_halo(40, 40)
            self.set_openroad_tapcells_file(lib_path / "apr" / "openroad" / "tapcell.tcl")
            self.add_openroad_global_connect_file(
                lib_path / "apr" / "openroad" / "global_connect.tcl")
            self.add_openroad_power_grid_file(lib_path / "apr" / "openroad" / "pdngen.tcl")

        # Setup for bambu
        self.set_bambu_clock_multiplier(1)


class IHP130StdCell_1p2(_IHP130StdCell):
    def __init__(self):
        super().__init__("1p2")


class IHP130StdCell_1p5(_IHP130StdCell):
    def __init__(self):
        super().__init__("1p5")
