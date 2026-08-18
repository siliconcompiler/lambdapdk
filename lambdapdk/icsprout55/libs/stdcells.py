from pathlib import Path

from lambdapdk import LambdaLibrary
from lambdapdk.icsprout55 import ICS55PDK, _ICS55Path, pdk_rev


class _ICS55StdCell(LambdaLibrary, _ICS55Path):
    '''
    ICsprout55 7-track standard cell library.
    '''
    def __init__(self, vt):
        super().__init__()
        self.set_name(f"ics55_stdcell_{vt.lower()}")

        # Cell suffix: the libraries are named ics55_LLSC_H7C<VT>, the cells inside
        # them are suffixed H7<VT>.
        cell = f"H7{vt}"
        lib = f"ics55_LLSC_H7C{vt}"

        lib_path_common = Path("lambdapdk", "icsprout55", "libs", "ics55_stdcell")
        lib_path = Path("lambdapdk", "icsprout55", "libs", f"ics55_stdcell_{vt.lower()}")

        # PDK
        self.add_asic_pdk(ICS55PDK())

        # version
        self.package.set_version(pdk_rev)

        # site name
        self.add_asic_site("core7")

        # Liberty and GDS are release assets, not part of the repository, so they
        # each need their own dataroot; cloning the repository alone gets neither.
        self.set_dataroot(f"icsprout55-liberty-{vt.lower()}",
                          "https://github.com/openecos-projects/icsprout55-pdk/releases/"
                          f"download/{pdk_rev}/{lib}_liberty.tar.bz2",
                          pdk_rev)
        self.set_dataroot(f"icsprout55-gds-{vt.lower()}",
                          "https://github.com/openecos-projects/icsprout55-pdk/releases/"
                          f"download/{pdk_rev}/{lib}_gds.tar.bz2",
                          pdk_rev)

        with self.active_dataroot(f"icsprout55-liberty-{vt.lower()}"):
            # Seven corners ship; these three are the flow corners. ss_cworst_1p08_m40
            # is deliberately not used: its deck is short cells the other six carry
            # (H is missing ESDFFQX1 and SDFFSRQX2, R is missing ICGNX3), so STA would
            # see a different cell set at that corner than synthesis did.
            for corner_name, filename in [
                    ('slow', f'{lib}_ss_rcworst_1p08_125_nldm.lib'),
                    ('typical', f'{lib}_typ_tt_1p2_25_nldm.lib'),
                    ('fast', f'{lib}_ff_rcbest_1p32_m40_nldm.lib')]:
                with self.active_fileset(f"models.timing.{corner_name}.nldm"):
                    self.add_file(f"liberty/{filename}")
                    self.add_asic_libcornerfileset(corner_name, "nldm")

        with self.active_dataroot("icsprout55"):
            # The unsuffixed LEF gives every signal pin on MET1 only, and the shapes are
            # too small to take any VIA1 the tech LEF defines: OpenROAD finds no access
            # point for 50 pins across 49 cells, among them DFFRQX1 and MUX2X8. The
            # _ecos LEF is that same LEF (same 785 macros, same sizes, same
            # obstructions, nothing removed) plus a MET2 landing pad and a VIA1 on every
            # signal pin - all 785 cells are then accessible. Those added shapes are
            # real geometry in the _M2 stream, which is why the two are paired below.
            with self.active_fileset("models.physical"):
                self.add_file(f"IP/STD_cell/ics55_LLSC_H7C_V1p10C100/{lib}/lef/{lib}_ecos.lef")
                self.add_asic_aprfileset()

            with self.active_fileset("models.lvs"):
                self.add_file(f"IP/STD_cell/ics55_LLSC_H7C_V1p10C100/{lib}/cdl/{lib}.cdl")
                self.add_asic_aprfileset()

            with self.active_fileset("models.sim"):
                self.add_file(f"IP/STD_cell/ics55_LLSC_H7C_V1p10C100/{lib}/verilog/{lib}.v")

        with self.active_dataroot(f"icsprout55-gds-{vt.lower()}"):
            # The _M2 stream is the layout that matches the _ecos LEF: front-end and
            # MET1 geometry identical to the base stream, plus the MET2 pin pads and
            # VIA1s, shape for shape (e.g. DFFRQX0P5 pin D, MET2 0.85 0.425 0.95 0.96
            # and VIA1 0.855 0.655 0.945 0.745 in both). Pairing the _ecos LEF with the
            # base stream would promise pin metal the layout does not have.
            with self.active_fileset("models.gds"):
                self.add_file(f"gds/{lib}_M2.gds")
                self.add_asic_aprfileset()

        # tie cells
        self.add_asic_celllist('tie', [f"TIEHI{cell}",
                                       f"TIELO{cell}"])

        # hold cells
        self.add_asic_celllist('hold', [f"DLY1X2{cell}",
                                        f"DLY1X6{cell}",
                                        f"DLY2X2{cell}",
                                        f"DLY2X6{cell}",
                                        f"DLY3X2{cell}",
                                        f"DLY3X6{cell}",
                                        f"DLY4X2{cell}",
                                        f"DLY4X6{cell}"])

        # filler
        self.add_asic_celllist('filler', [f"FILLER1{cell}",
                                          f"FILLER2{cell}",
                                          f"FILLER4{cell}",
                                          f"FILLER8{cell}",
                                          f"FILLER16{cell}",
                                          f"FILLER32{cell}",
                                          f"FILLER64{cell}"])

        # decap
        self.add_asic_celllist('decap', [f"FILLCAP4{cell}",
                                         f"FILLCAP8{cell}",
                                         f"FILLCAP16{cell}",
                                         f"FILLCAP32{cell}"])

        # antenna
        self.add_asic_celllist('antenna', [f"ANT2{cell}",
                                           f"ANT4{cell}"])

        # well tap / endcap
        self.add_asic_celllist('tap', [f"FILLTAP{cell}"])

        # Cells that carry LEF and GDS but no liberty
        self.add_asic_celllist('physicalonly', [f"ANT2{cell}",
                                                f"ANT4{cell}",
                                                f"FILLER1{cell}",
                                                f"FILLER2{cell}",
                                                f"FILLER4{cell}",
                                                f"FILLER8{cell}",
                                                f"FILLER16{cell}",
                                                f"FILLER32{cell}",
                                                f"FILLER64{cell}",
                                                f"FILLTAP{cell}"])

        # Cells that carry liberty but no Verilog model: synthesis must not emit
        # something that cannot be simulated.
        self.add_asic_celllist('dontuse', [f"DFFNSRX0P5{cell}",
                                           f"DFFSRX0P5{cell}",
                                           f"SDFFSRX0P5{cell}"])

        # Setup for yosys
        with self.active_dataroot("lambdapdk"):
            self.set_yosys_driver_cell(f"BUFX1{cell}")
            self.set_yosys_buffer_cell(f"BUFX1{cell}", "A", "Y")
            self.set_yosys_tielow_cell(f"TIELO{cell}", "Z")
            self.set_yosys_tiehigh_cell(f"TIEHI{cell}", "Z")

            # 4x the BUFX1 input pin capacitance, in fF (liberty is in pF).
            cap_table = {
                'H': 0.00105062,
                'R': 0.000884993,
                'L': 0.000922872
            }
            # Liberty time unit is 1ns.
            self.set_yosys_abc(1000, cap_table[vt] * 1000 * 4)

            self.add_yosys_tech_map(lib_path / "techmap" / "yosys" / "cells_latch.v")
            self.set_yosys_adder_map(lib_path / "techmap" / "yosys" / "cells_adders.v")

        # Setup for OpenROAD
        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("openroad.powergrid"):
                self.add_file(lib_path_common / "apr" / "openroad" / "pdngen.tcl")
                self.add_openroad_powergridfileset()
            with self.active_fileset("openroad.globalconnect"):
                self.add_file(lib_path_common / "apr" / "openroad" / "global_connect.tcl")
                self.add_openroad_globalconnectfileset()

            self.set_openroad_placement_density(0.60)
            self.set_openroad_tielow_cell(f"TIELO{cell}", "Z")
            self.set_openroad_tiehigh_cell(f"TIEHI{cell}", "Z")
            self.set_openroad_macro_placement_halo(5, 5)
            self.set_openroad_tapcells_file(lib_path / "apr" / "openroad" / "tapcells.tcl")


class ICS55StdCellHVT(_ICS55StdCell):
    def __init__(self):
        super().__init__("H")


class ICS55StdCellRVT(_ICS55StdCell):
    def __init__(self):
        super().__init__("R")


class ICS55StdCellLVT(_ICS55StdCell):
    def __init__(self):
        super().__init__("L")
