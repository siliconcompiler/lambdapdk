from pathlib import Path

from lambdapdk import LambdaLibrary
from lambdapdk.sky130 import Sky130PDK


class _Sky130_SCLibrary(LambdaLibrary):
    '''
    Skywater130 standard cell library.
    '''
    def __init__(self, libtype, slow_v):
        super().__init__()
        self.set_name(f"sky130{libtype}")

        self.set_version("v0_0_2")

        self.add_asic_pdk(Sky130PDK())

        self.add_asic_site(["unithd", "unithddbl"])

        lib_path = Path("lambdapdk", "sky130", "libs", self.name)

        with self.active_dataroot("lambdapdk"):
            for corner_name, filename in [
                    ('slow', f'sky130_fd_sc_{libtype}__ss_n40C_{slow_v}.lib.gz'),
                    ('typical', f'sky130_fd_sc_{libtype}__tt_025C_1v80.lib.gz'),
                    ('fast', f'sky130_fd_sc_{libtype}__ff_100C_1v95.lib.gz')]:
                with self.active_fileset(f"models.timing.{corner_name}.nldm"):
                    self.add_file(lib_path / "nldm" / filename)
                    self.add_asic_libcornerfileset(corner_name, "nldm")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("models.physical"):
                self.add_file(lib_path / "lef" / f"sky130_fd_sc_{libtype}_merged.lef")
                self.add_file(lib_path / "gds" / f"sky130_fd_sc_{libtype}.gds")
                self.add_asic_aprfileset()

            with self.active_fileset("models.lvs"):
                self.add_file(lib_path / "cdl" / f"sky130_fd_sc_{libtype}.cdl")
                self.add_asic_aprfileset()

            with self.active_fileset("rtl"):
                self.add_file(lib_path / "verilog" / f"sky130_fd_sc_{libtype}.v")
                self.add_file(lib_path / "verilog" / "primitives.v")

            # antenna cells
            self.add_asic_celllist('antenna', f'sky130_fd_sc_{libtype}__diode_2')

            # clock buffers
            self.add_asic_celllist('clkbuf', [f'sky130_fd_sc_{libtype}__clkbuf_1',
                                              f'sky130_fd_sc_{libtype}__clkbuf_2',
                                              f'sky130_fd_sc_{libtype}__clkbuf_4',
                                              f'sky130_fd_sc_{libtype}__clkbuf_8',
                                              f'sky130_fd_sc_{libtype}__clkbuf_16'])
            if libtype == "hdll":
                self.add_asic_celllist('clkbuf', [f'sky130_fd_sc_{libtype}__clkbuf_6',
                                                  f'sky130_fd_sc_{libtype}__clkbuf_12'])

            # hold cells
            self.add_asic_celllist('hold', [f'sky130_fd_sc_{libtype}__dlygate4sd1_1',
                                            f'sky130_fd_sc_{libtype}__dlygate4sd2_1',
                                            f'sky130_fd_sc_{libtype}__dlygate4sd3_1'])
            if libtype == "hd":
                self.add_asic_celllist('hold', [f'sky130_fd_sc_{libtype}__dlymetal6s2s_1',
                                                f'sky130_fd_sc_{libtype}__dlymetal6s4s_1',
                                                f'sky130_fd_sc_{libtype}__dlymetal6s6s_1'])

            # filler
            self.add_asic_celllist('filler', [f'sky130_fd_sc_{libtype}__fill_1',
                                              f'sky130_fd_sc_{libtype}__fill_2',
                                              f'sky130_fd_sc_{libtype}__fill_4',
                                              f'sky130_fd_sc_{libtype}__fill_8'])

            # Tapcell
            self.add_asic_celllist('tap', f'sky130_fd_sc_{libtype}__tapvpwrvgnd_1')

            # Endcap
            self.add_asic_celllist('endcap', f'sky130_fd_sc_{libtype}__decap_4')

            self.add_asic_celllist('dontuse', [
                f'sky130_fd_sc_{libtype}__probe_p_8',
                f'sky130_fd_sc_{libtype}__probec_p_8'
            ])

            if libtype == "hd":
                self.add_asic_celllist('dontuse', [
                    'sky130_fd_sc_hd__lpflow_bleeder_1',
                    'sky130_fd_sc_hd__lpflow_clkbufkapwr_1',
                    'sky130_fd_sc_hd__lpflow_clkbufkapwr_16',
                    'sky130_fd_sc_hd__lpflow_clkbufkapwr_2',
                    'sky130_fd_sc_hd__lpflow_clkbufkapwr_4',
                    'sky130_fd_sc_hd__lpflow_clkbufkapwr_8',
                    'sky130_fd_sc_hd__lpflow_clkinvkapwr_1',
                    'sky130_fd_sc_hd__lpflow_clkinvkapwr_16',
                    'sky130_fd_sc_hd__lpflow_clkinvkapwr_2',
                    'sky130_fd_sc_hd__lpflow_clkinvkapwr_4',
                    'sky130_fd_sc_hd__lpflow_clkinvkapwr_8',
                    'sky130_fd_sc_hd__lpflow_decapkapwr_12',
                    'sky130_fd_sc_hd__lpflow_decapkapwr_3',
                    'sky130_fd_sc_hd__lpflow_decapkapwr_4',
                    'sky130_fd_sc_hd__lpflow_decapkapwr_6',
                    'sky130_fd_sc_hd__lpflow_decapkapwr_8',
                    'sky130_fd_sc_hd__lpflow_inputiso0n_1',
                    'sky130_fd_sc_hd__lpflow_inputiso0p_1',
                    'sky130_fd_sc_hd__lpflow_inputiso1n_1',
                    'sky130_fd_sc_hd__lpflow_inputiso1p_1',
                    'sky130_fd_sc_hd__lpflow_inputisolatch_1',
                    'sky130_fd_sc_hd__lpflow_isobufsrc_1',
                    'sky130_fd_sc_hd__lpflow_isobufsrc_16',
                    'sky130_fd_sc_hd__lpflow_isobufsrc_2',
                    'sky130_fd_sc_hd__lpflow_isobufsrc_4',
                    'sky130_fd_sc_hd__lpflow_isobufsrc_8',
                    'sky130_fd_sc_hd__lpflow_isobufsrckapwr_16',
                    'sky130_fd_sc_hd__lpflow_lsbuf_lh_hl_isowell_tap_1',
                    'sky130_fd_sc_hd__lpflow_lsbuf_lh_hl_isowell_tap_2',
                    'sky130_fd_sc_hd__lpflow_lsbuf_lh_hl_isowell_tap_4',
                    'sky130_fd_sc_hd__lpflow_lsbuf_lh_isowell_4',
                    'sky130_fd_sc_hd__lpflow_lsbuf_lh_isowell_tap_1',
                    'sky130_fd_sc_hd__lpflow_lsbuf_lh_isowell_tap_2',
                    'sky130_fd_sc_hd__lpflow_lsbuf_lh_isowell_tap_4'])
            elif libtype == "hdll":
                self.add_asic_celllist('dontuse', [
                    'sky130_fd_sc_hdll__inputiso0p_1',
                    'sky130_fd_sc_hdll__inputiso0n_1',
                    'sky130_fd_sc_hdll__inputiso1p_1',
                    'sky130_fd_sc_hdll__inputiso1n_1',
                    'sky130_fd_sc_hdll__isobufsrc_1',
                    'sky130_fd_sc_hdll__isobufsrc_2',
                    'sky130_fd_sc_hdll__isobufsrc_4',
                    'sky130_fd_sc_hdll__isobufsrc_8',
                    'sky130_fd_sc_hdll__isobufsrc_16'])

            # tie cells
            self.add_asic_celllist('tie', f'sky130_fd_sc_{libtype}__conb_1')

        # Setup for yosys
        with self.active_dataroot("lambdapdk"):
            cap_table = {
                'hd': 11,
                'hdll': 11
            }
            self.set_yosys_driver_cell(f"sky130_fd_sc_{libtype}__buf_4")
            self.set_yosys_buffer_cell(f"sky130_fd_sc_{libtype}__buf_4", "A", "X")
            self.set_yosys_tielow_cell(f"sky130_fd_sc_{libtype}__conb_1", "LO")
            self.set_yosys_tiehigh_cell(f"sky130_fd_sc_{libtype}__conb_1", "HI")
            self.set_yosys_abc(1000, cap_table[libtype])
            self.set_yosys_tristatebuffer_map(
                lib_path / "techmap" / "yosys" / "cells_tristatebuf.v")
            if libtype == "hd":
                self.set_yosys_adder_map(lib_path / "techmap" / "yosys" / "cells_adders.v")
            self.add_yosys_tech_map(lib_path / "techmap" / "yosys" / "cells_latch.v")

        # Setup for OpenROAD
        with self.active_dataroot("lambdapdk"):
            self.set_openroad_placement_density(0.60)
            self.set_openroad_tielow_cell(f"sky130_fd_sc_{libtype}__conb_1", "LO")
            self.set_openroad_tiehigh_cell(f"sky130_fd_sc_{libtype}__conb_1", "HI")
            self.set_openroad_macro_placement_halo(40, 40)
            self.set_openroad_tapcells_file(lib_path / "apr" / "openroad" / "tapcell.tcl")
            self.add_openroad_global_connect_file(
                lib_path / "apr" / "openroad" / "global_connect.tcl")
            self.add_openroad_power_grid_file(lib_path / "apr" / "openroad" / "pdngen.tcl")

        # Setup for bambu
        self.set_bambu_clock_multiplier(1)


class Sky130_SCHDLibrary(_Sky130_SCLibrary):
    def __init__(self):
        super().__init__("hd", "1v40")


class Sky130_SCHDLLLibrary(_Sky130_SCLibrary):
    def __init__(self):
        super().__init__("hdll", "1v44")
