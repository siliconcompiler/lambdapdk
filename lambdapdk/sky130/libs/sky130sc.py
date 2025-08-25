import os
import siliconcompiler
from lambdapdk import register_data_source

from pathlib import Path

from lambdapdk import LambdaLibrary
from lambdapdk.sky130 import Sky130PDK


class _Sky130_SCLibrary(LambdaLibrary):
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


def setup():
    '''
    Skywater130 standard cell library.
    '''
    process = 'skywater130'
    stackup = '5M1LI'
    version = 'v0_0_2'

    dontuse = {
        'hd': [
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
            'sky130_fd_sc_hd__lpflow_lsbuf_lh_isowell_tap_4'
        ],
        'hdll': [
            'sky130_fd_sc_hdll__inputiso0p_1',
            'sky130_fd_sc_hdll__inputiso0n_1',
            'sky130_fd_sc_hdll__inputiso1p_1',
            'sky130_fd_sc_hdll__inputiso1n_1',
            'sky130_fd_sc_hdll__isobufsrc_1',
            'sky130_fd_sc_hdll__isobufsrc_2',
            'sky130_fd_sc_hdll__isobufsrc_4',
            'sky130_fd_sc_hdll__isobufsrc_8',
            'sky130_fd_sc_hdll__isobufsrc_16',
        ]
    }

    libs = []
    for libtype, sites, slow_v in (("hd", ["unithd", "unithddbl"], "1v40"),
                                   ("hdll", ["unithd", "unithddbl"], "1v44")):

        # This name can later be expanded to the full sky130_fd_sc_{libtype}
        libname = f"sky130{libtype}"
        libdir = os.path.join('lambdapdk', 'sky130', 'libs', libname)

        lib = siliconcompiler.Library(libname, package='lambdapdk')
        register_data_source(lib)

        # version
        lib.set('package', 'version', version)

        # pdk
        lib.set('option', 'pdk', process)

        # footprint/type/sites
        lib.set('asic', 'libarch', libtype)
        lib.set('asic', 'site', libtype, sites)

        # model files
        lib.add('output', 'slow', 'nldm',
                libdir + f'/nldm/sky130_fd_sc_{libtype}__ss_n40C_{slow_v}.lib.gz')
        lib.add('output', 'typical', 'nldm',
                libdir + f'/nldm/sky130_fd_sc_{libtype}__tt_025C_1v80.lib.gz')
        lib.add('output', 'fast', 'nldm',
                libdir + f'/nldm/sky130_fd_sc_{libtype}__ff_100C_1v95.lib.gz')

        lib.add('output', stackup, 'lef', libdir + f'/lef/sky130_fd_sc_{libtype}_merged.lef')
        lib.add('output', stackup, 'gds', libdir + f'/gds/sky130_fd_sc_{libtype}.gds')
        lib.add('output', stackup, 'cdl', libdir + f'/cdl/sky130_fd_sc_{libtype}.cdl')

        lib.add('output', 'rtl', 'verilog', libdir + f'/verilog/sky130_fd_sc_{libtype}.v')
        lib.add('output', 'rtl', 'verilog', libdir + '/verilog/primitives.v')

        # antenna cells
        lib.add('asic', 'cells', 'antenna', f'sky130_fd_sc_{libtype}__diode_2')

        # clock buffers
        lib.add('asic', 'cells', 'clkbuf', [f'sky130_fd_sc_{libtype}__clkbuf_1',
                                            f'sky130_fd_sc_{libtype}__clkbuf_2',
                                            f'sky130_fd_sc_{libtype}__clkbuf_4',
                                            f'sky130_fd_sc_{libtype}__clkbuf_8',
                                            f'sky130_fd_sc_{libtype}__clkbuf_16'])
        if libtype == "hdll":
            lib.add('asic', 'cells', 'clkbuf', [f'sky130_fd_sc_{libtype}__clkbuf_6',
                                                f'sky130_fd_sc_{libtype}__clkbuf_12'])

        # hold cells
        lib.add('asic', 'cells', 'hold', [f'sky130_fd_sc_{libtype}__dlygate4sd1_1',
                                          f'sky130_fd_sc_{libtype}__dlygate4sd2_1',
                                          f'sky130_fd_sc_{libtype}__dlygate4sd3_1'])
        if libtype == "hd":
            lib.add('asic', 'cells', 'hold', [f'sky130_fd_sc_{libtype}__dlymetal6s2s_1',
                                              f'sky130_fd_sc_{libtype}__dlymetal6s4s_1',
                                              f'sky130_fd_sc_{libtype}__dlymetal6s6s_1'])

        # filler
        lib.add('asic', 'cells', 'filler', [f'sky130_fd_sc_{libtype}__fill_1',
                                            f'sky130_fd_sc_{libtype}__fill_2',
                                            f'sky130_fd_sc_{libtype}__fill_4',
                                            f'sky130_fd_sc_{libtype}__fill_8'])

        # Tapcell
        lib.add('asic', 'cells', 'tap', f'sky130_fd_sc_{libtype}__tapvpwrvgnd_1')

        # Endcap
        lib.add('asic', 'cells', 'endcap', f'sky130_fd_sc_{libtype}__decap_4')

        lib.add('asic', 'cells', 'dontuse', [
            f'sky130_fd_sc_{libtype}__probe_p_8',
            f'sky130_fd_sc_{libtype}__probec_p_8'
        ])
        lib.add('asic', 'cells', 'dontuse', dontuse[libtype])

        # tie cells
        lib.add('asic', 'cells', 'tie', f'sky130_fd_sc_{libtype}__conb_1')

        # Defaults for OpenROAD tool variables
        lib.set('option', 'var', 'openroad_place_density', '0.60')
        lib.set('option', 'var', 'openroad_pad_global_place', '0')
        lib.set('option', 'var', 'openroad_pad_detail_place', '0')
        lib.set('option', 'var', 'openroad_macro_place_halo', ['40', '40'])
        lib.set('option', 'var', 'openroad_macro_place_channel', ['80', '80'])

        # Yosys techmap
        # TODO: separate this out properly for the different libraries
        lib.add('option', 'file', 'yosys_techmap', libdir + '/techmap/yosys/cells_latch.v')
        lib.add('option', 'file', 'yosys_tbufmap', libdir + '/techmap/yosys/cells_tristatebuf.v')
        if libtype == "hd":
            lib.add('option', 'file', 'yosys_addermap', libdir + '/techmap/yosys/cells_adders.v')

        # Openroad specific files
        lib.set('option', 'file', 'openroad_pdngen',
                libdir + '/apr/openroad/pdngen.tcl')
        lib.set('option', 'file', 'openroad_global_connect',
                libdir + '/apr/openroad/global_connect.tcl')
        lib.set('option', 'file', 'openroad_tapcells',
                libdir + '/apr/openroad/tapcell.tcl')

        lib.set('option', 'var', 'yosys_abc_clock_multiplier', "1000")  # convert from ns -> ps

        cap_table = {
            'hd': "0.011pF",
            'hdll': "0.011pF"
        }
        lib.set('option', 'var', 'yosys_abc_constraint_load', cap_table[libtype])

        lib.set('option', 'var', 'yosys_driver_cell', f"sky130_fd_sc_{libtype}__buf_4")
        lib.set('option', 'var', 'yosys_buffer_cell', f"sky130_fd_sc_{libtype}__buf_4")
        lib.set('option', 'var', 'yosys_buffer_input', "A")
        lib.set('option', 'var', 'yosys_buffer_output', "X")
        for tool in ('yosys', 'openroad'):
            lib.set('option', 'var', f'{tool}_tiehigh_cell', f"sky130_fd_sc_{libtype}__conb_1")
            lib.set('option', 'var', f'{tool}_tiehigh_port', "HI")
            lib.set('option', 'var', f'{tool}_tielow_cell', f"sky130_fd_sc_{libtype}__conb_1")
            lib.set('option', 'var', f'{tool}_tielow_port', "LO")

        # Bambu setup
        lib.set('option', 'var', 'bambu_clock_multiplier', "1")  # convert from ns -> ns

        libs.append(lib)

        std_lambda_lib = siliconcompiler.Library(f'lambdalib_stdlib_{libname}',
                                                 package='lambdapdk')
        register_data_source(std_lambda_lib)
        std_lambda_lib.add('option', 'ydir', libdir + '/lambda/stdlib')
        std_lambda_lib.use(lib)
        std_lambda_lib.set('asic', 'logiclib', lib.design)
        libs.append(std_lambda_lib)
        aux_lambda_lib = siliconcompiler.Library(f'lambdalib_auxlib_{libname}',
                                                 package='lambdapdk')
        register_data_source(aux_lambda_lib)
        aux_lambda_lib.add('option', 'ydir', libdir + '/lambda/auxlib')
        aux_lambda_lib.use(std_lambda_lib)
        aux_lambda_lib.use(lib)
        aux_lambda_lib.set('asic', 'logiclib', lib.design)
        aux_lambda_lib.set('option', 'library', std_lambda_lib.design)
        libs.append(aux_lambda_lib)

    return libs


#########################
if __name__ == "__main__":
    for lib in setup(siliconcompiler.Chip('<lib>')):
        lib.write_manifest(f'{lib.top()}.json')
