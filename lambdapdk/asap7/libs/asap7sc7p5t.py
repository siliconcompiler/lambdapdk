from pathlib import Path

from lambdapdk import LambdaLibrary
from lambdapdk.asap7 import ASAP7PDK


class _ASAP7SC7p5Base(LambdaLibrary):
    '''
    ASAP 7 7.5-track standard cell library.
    '''
    def __init__(self, vt, suffix):
        super().__init__()
        self.set_name(f"asap7sc7p5t_{vt}")

        # version
        self.set_version("28")

        # PDK
        self.add_asic_pdk(ASAP7PDK())

        # site name
        self.add_asic_site('asap7sc7p5t')

        # tie cells
        self.add_asic_celllist('tie', [f"TIEHIx1_ASAP7_75t_{suffix}",
                                       f"TIELOx1_ASAP7_75t_{suffix}"])

        # filler
        self.add_asic_celllist('filler', [f"FILLER_ASAP7_75t_{suffix}",
                                          f"FILLERxp5_ASAP7_75t_{suffix}"])

        # decap
        self.add_asic_celllist('decap', [f"DECAPx1_ASAP7_75t_{suffix}",
                                         f"DECAPx2_ASAP7_75t_{suffix}",
                                         f"DECAPx4_ASAP7_75t_{suffix}",
                                         f"DECAPx6_ASAP7_75t_{suffix}",
                                         f"DECAPx10_ASAP7_75t_{suffix}"])

        # Stupid small cells
        self.add_asic_celllist('dontuse', ["*x1p*_ASAP7*",
                                           "*xp*_ASAP7*",
                                           "SDF*",
                                           "ICG*"])

        # Tapcell
        self.add_asic_celllist('tap', f"TAPCELL_ASAP7_75t_{suffix}")

        # Endcap
        self.add_asic_celllist('endcap', f"DECAPx1_ASAP7_75t_{suffix}")

        lib_path = Path("lambdapdk", "asap7", "libs", f"asap7sc7p5t_{vt}")

        # General filelists
        with self.active_dataroot("lambdapdk"):
            for corner_name, lib_corner in [
                    ('typical', 'TT'),
                    ('fast', 'FF'),
                    ('slow', 'SS')]:

                for lib_type in ('AO', 'INVBUF', 'OA', 'SEQ', 'SIMPLE'):
                    with self.active_fileset(f"models.timing.{corner_name}.nldm.{lib_type}"):
                        self.add_file(lib_path / "nldm" /
                                      f"asap7sc7p5t_{lib_type}_{suffix}VT_{lib_corner}_nldm.lib.gz")
                        self.add_asic_libcornerfileset(corner_name, "nldm")

            with self.active_fileset("models.spice"):
                self.add_file(lib_path / "netlist" / f"asap7sc7p5t_28_{suffix}.sp")

            with self.active_fileset("models.physical"):
                self.add_file(lib_path / "lef" / f"asap7sc7p5t_28_{suffix}.lef")
                self.add_file(lib_path / "gds" / f"asap7sc7p5t_28_{suffix}.gds.gz")
                self.add_asic_aprfileset()

            with self.active_fileset("models.lvs"):
                self.add_file(lib_path / "netlist" / f"asap7sc7p5t_28_{suffix}.cdl")
                self.add_asic_aprfileset()

        # Setup for yosys
        with self.active_dataroot("lambdapdk"):
            self.set_yosys_driver_cell(f"BUFx2_ASAP7_75t_{suffix}")
            self.set_yosys_buffer_cell(f"BUFx2_ASAP7_75t_{suffix}", "A", "Y")
            self.set_yosys_tielow_cell(f"TIELOx1_ASAP7_75t_{suffix}", "L")
            self.set_yosys_tiehigh_cell(f"TIEHIx1_ASAP7_75t_{suffix}", "H")

            cap_table = {  # BUFx2_ASAP7_75t_, fF
                'R': "2.308",
                'L': "2.383",
                'SL': "2.464"
            }
            self.set_yosys_abc(1, cap_table[suffix])
            self.set_yosys_adder_map(lib_path / "techmap" / "yosys" / "cells_adders.v")
            self.add_yosys_tech_map(lib_path / "techmap" / "yosys" / "cells_latch.v")

        # Setup for openroad
        with self.active_dataroot("lambdapdk"):
            self.set_openroad_placement_density(0.60)
            self.set_openroad_tielow_cell(f"TIELOx1_ASAP7_75t_{suffix}", "L")
            self.set_openroad_tiehigh_cell(f"TIEHIx1_ASAP7_75t_{suffix}", "H")
            self.set_openroad_macro_placement_halo(5, 5)
            self.set_openroad_tracks_file(lib_path / "apr" / "openroad" / "tracks.tcl")
            self.set_openroad_tapcells_file(lib_path / "apr" / "openroad" / "tapcells.tcl")
            self.add_openroad_global_connect_file(lib_path / "apr" / "openroad" /
                                                  "global_connect.tcl")
            self.add_openroad_power_grid_file(lib_path / "apr" / "openroad" / "pdngen.tcl")

        # Setup for bambu
        self.set_bambu_device_name("asap7-WC")
        self.set_bambu_clock_multiplier(0.001)


class ASAP7SC7p5RVT(_ASAP7SC7p5Base):
    def __init__(self):
        super().__init__("rvt", "R")


class ASAP7SC7p5LVT(_ASAP7SC7p5Base):
    def __init__(self):
        super().__init__("lvt", "L")


class ASAP7SC7p5SLVT(_ASAP7SC7p5Base):
    def __init__(self):
        super().__init__("slvt", "SL")
