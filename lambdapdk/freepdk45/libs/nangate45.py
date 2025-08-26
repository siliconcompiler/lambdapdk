from pathlib import Path

from lambdapdk import LambdaLibrary

from lambdapdk.freepdk45 import FreePDK45PDK


class Nangate45(LambdaLibrary):
    '''
    Nangate open standard cell library for FreePDK45.
    '''
    def __init__(self):
        super().__init__()
        self.set_name("nangate45")

        # version
        self.set_version("r1p0")

        self.add_asic_pdk(FreePDK45PDK())

        self.add_asic_site("FreePDK45_38x28_10R_NP_162NW_34O")

        # clock buffers
        self.add_asic_celllist("clkbuf", ["CLKBUF_X1",
                                          "CLKBUF_X2",
                                          "CLKBUF_X3"])

        # tie cells
        self.add_asic_celllist("tie", ["LOGIC0_X1",
                                       "LOGIC1_X1"])

        # filler
        self.add_asic_celllist("filler", ["FILLCELL_X1",
                                          "FILLCELL_X2",
                                          "FILLCELL_X4",
                                          "FILLCELL_X8",
                                          "FILLCELL_X16",
                                          "FILLCELL_X32"])

        # Dont use for synthesis
        self.add_asic_celllist("dontuse", "OAI211_X1")

        # Tapcell
        self.add_asic_celllist("tap", "TAPCELL_X1")

        # Endcap
        self.add_asic_celllist("endcap", "TAPCELL_X1")

        lib_path = Path("lambdapdk", "freepdk45", "libs", "nangate45")

        # General filelists
        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("models.timing.nldm"):
                self.add_file(lib_path / "nldm" / "NangateOpenCellLibrary_typical.lib")
                self.add_asic_libcornerfileset("typical", "nldm")

            with self.active_fileset("models.physical"):
                self.add_file(lib_path / "lef" / "NangateOpenCellLibrary.macro.mod.lef")
                self.add_file(lib_path / "gds" / "NangateOpenCellLibrary.gds")
                self.add_asic_aprfileset()

            with self.active_fileset("models.lvs"):
                self.add_file(lib_path / "cdl" / "NangateOpenCellLibrary.cdl")
                self.add_asic_aprfileset()

        # Setup for yosys
        with self.active_dataroot("lambdapdk"):
            self.set_yosys_driver_cell("BUF_X4")
            self.set_yosys_buffer_cell("BUF_X1", "A", "Z")
            self.set_yosys_tielow_cell("LOGIC0_X1", "Z")
            self.set_yosys_tiehigh_cell("LOGIC1_X1", "Z")
            self.set_yosys_abc(1000, 3.899)
            self.set_yosys_tristatebuffer_map(
                lib_path / "techmap" / "yosys" / "cells_tristatebuf.v")
            self.set_yosys_adder_map(lib_path / "techmap" / "yosys" / "cells_adders.v")
            self.add_yosys_tech_map(lib_path / "techmap" / "yosys" / "cells_latch.v")

        # Setup for openroad
        with self.active_dataroot("lambdapdk"):
            self.set_openroad_placement_density(0.50)
            self.set_openroad_tielow_cell("LOGIC0_X1", "Z")
            self.set_openroad_tiehigh_cell("LOGIC1_X1", "Z")
            self.set_openroad_macro_placement_halo(22.4, 15.12)
            self.set_openroad_tapcells_file(lib_path / "apr" / "openroad" / "tapcell.tcl")
            self.add_openroad_global_connect_file(
                lib_path / "apr" / "openroad" / "global_connect.tcl")
            self.add_openroad_power_grid_file(lib_path / "apr" / "openroad" / "pdngen.tcl")

        # Setup for bambu
        self.set_bambu_device_name("nangate45")
        self.set_bambu_clock_multiplier(1)
