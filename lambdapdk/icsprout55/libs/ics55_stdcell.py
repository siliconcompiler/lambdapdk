from pathlib import Path

from lambdapdk import LambdaLibrary
from lambdapdk.icsprout55 import ICS55PDK, _ICS55Path, pdk_rev


class _ICS55StdCell(LambdaLibrary, _ICS55Path):
    '''
    Standard cell library for ICS55
    '''
    def __init__(self, vt):
        super().__init__()
        self.set_name(f"ics55_stdcell_{vt.lower()}")

        lib_path = Path("lambdapdk", "icsprout55", "libs", f"ics55_stdcell_{vt}")

        self.add_asic_pdk(ICS55PDK())

        self.add_asic_site("core7")

        self.set_dataroot(f"icsprout55-liberty-{vt}",
                          "https://github.com/openecos-projects/icsprout55-pdk/releases/"
                          f"download/{pdk_rev}/ics55_LLSC_H7C{vt}_liberty.tar.bz2",
                          pdk_rev)

        self.set_dataroot(f"icsprout55-gds-{vt}",
                          "https://github.com/openecos-projects/icsprout55-pdk/releases/"
                          f"download/{pdk_rev}/ics55_LLSC_H7C{vt}_gds.tar.bz2",
                          pdk_rev)

        with self.active_dataroot(f"icsprout55-liberty-{vt}"):
            for corner_name, filename in [
                    ('slow', f'ics55_LLSC_H7C{vt}_ss_rcworst_1p08_125_nldm.lib'),
                    ('typical', f'ics55_LLSC_H7C{vt}_typ_tt_1p2_25_nldm.lib'),
                    ('fast', f'ics55_LLSC_H7C{vt}_ss_rcworst_1p2_m40_nldm.lib')]:
                with self.active_fileset(f"models.timing.{corner_name}.nldm"):
                    self.add_file(f"liberty/{filename}")
                    self.add_asic_libcornerfileset(corner_name, "nldm")

        with self.active_dataroot("icsprout55"):
            with self.active_fileset("models.physical"):
                self.add_file("IP/STD_cell/ics55_LLSC_H7C_V1p10C100/"
                              f"ics55_LLSC_H7C{vt}/lef/ics55_LLSC_H7C{vt}.lef")
                self.add_asic_aprfileset()

            with self.active_fileset("models.lvs"):
                self.add_file("IP/STD_cell/ics55_LLSC_H7C_V1p10C100/"
                              f"ics55_LLSC_H7C{vt}/cdl/ics55_LLSC_H7C{vt}.cdl")
                self.add_asic_aprfileset()

            with self.active_fileset("models.sim"):
                self.add_file("IP/STD_cell/ics55_LLSC_H7C_V1p10C100/"
                              f"ics55_LLSC_H7C{vt}/verilog/ics55_LLSC_H7C{vt}.v")
    
        with self.active_dataroot(f"icsprout55-gds-{vt}"):
            with self.active_fileset("models.gds"):
                self.add_file(f"gds/ics55_LLSC_H7C{vt}.gds")
                self.add_asic_aprfileset()

        # tie cells
        self.add_asic_celllist('tie', [f"TIEHIH7{vt}",
                                       f"TIELOH7{vt}"])

        # hold cells
        self.add_asic_celllist('hold', [f"DLY1X2H7{vt}",
                                        f"DLY1X6H7{vt}",
                                        f"DLY2X2H7{vt}",
                                        f"DLY2X6H7{vt}",
                                        f"DLY3X2H7{vt}",
                                        f"DLY3X6H7{vt}",
                                        f"DLY4X2H7{vt}",
                                        f"DLY4X6H7{vt}"])

        # filler
        self.add_asic_celllist('filler', [f"FILLER16H7{vt}",
                                          f"FILLER1H7{vt}",
                                          f"FILLER2H7{vt}",
                                          f"FILLER32H7{vt}",
                                          f"FILLER4H7{vt}",
                                          f"FILLER64H7{vt}",
                                          f"FILLER8H7{vt}"])

        # decap
        self.add_asic_celllist('decap', [f"FILLCAP4H7{vt}",
                                         f"FILLCAP8H7{vt}",
                                         f"FILLCAP16H7{vt}",
                                         f"FILLCAP32H7{vt}"])

        # antenna
        self.add_asic_celllist('antenna', [f"ANT2H7{vt}"])

        # Dont use

        # Setup for yosys
        with self.active_dataroot("lambdapdk"):
            self.set_yosys_driver_cell(f"BUFX4H7{vt}")
            self.set_yosys_buffer_cell(f"BUFX4H7{vt}", "A", "Y")
            self.set_yosys_tielow_cell(f"TIELOH7{vt}", "Z")
            self.set_yosys_tiehigh_cell(f"TIEHIH7{vt}", "Z")
            self.set_yosys_abc(1000, 4.74624)
            self.add_yosys_tech_map(lib_path / "techmap" / "yosys" / "cells_latch.v")
            self.set_yosys_adder_map(lib_path / "techmap" / "yosys" / "cells_adder.v")

        # Setup for OpenROAD
        with self.active_dataroot("lambdapdk"):
            # with self.active_fileset("openroad.powergrid"):
            #     self.add_file(lib_path / "apr" / "openroad" / "pdngen.tcl")
            #     self.add_openroad_powergridfileset()
            with self.active_fileset("openroad.globalconnect"):
                self.add_file(lib_path / "apr" / "openroad" / "global_connect.tcl")
                self.add_openroad_globalconnectfileset()

            self.set_openroad_placement_density(0.65)
            self.set_openroad_tielow_cell(f"TIELOH7{vt}", "Z")
            self.set_openroad_tiehigh_cell(f"TIEHIH7{vt}", "Z")
            self.set_openroad_macro_placement_halo(40, 40)
            # self.set_openroad_tapcells_file(lib_path / "apr" / "openroad" / "tapcell.tcl")

        # Setup for bambu
        # self.set_bambu_clock_multiplier(1)


class ics55_LLSC_H7CL(_ICS55StdCell):
    def __init__(self):
        super().__init__("L")


class ics55_LLSC_H7CR(_ICS55StdCell):
    def __init__(self):
        super().__init__("R")


class ics55_LLSC_H7CH(_ICS55StdCell):
    def __init__(self):
        super().__init__("H")
