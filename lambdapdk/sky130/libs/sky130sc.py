import os
import siliconcompiler
from lambdapdk import register_data_source


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
                                            f'sky130_fd_sc_{libtype}__clkbuf_6',
                                            f'sky130_fd_sc_{libtype}__clkbuf_8',
                                            f'sky130_fd_sc_{libtype}__clkbuf_12',
                                            f'sky130_fd_sc_{libtype}__clkbuf_16'])

        # hold cells
        lib.add('asic', 'cells', 'hold', [f'sky130_fd_sc_{libtype}__buf_1',
                                          f'sky130_fd_sc_{libtype}__buf_2',
                                          f'sky130_fd_sc_{libtype}__buf_4',
                                          f'sky130_fd_sc_{libtype}__buf_6',
                                          f'sky130_fd_sc_{libtype}__buf_8',
                                          f'sky130_fd_sc_{libtype}__buf_12',
                                          f'sky130_fd_sc_{libtype}__buf_16'])

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
        if libtype == "hd":
            lib.add('option', 'file', 'yosys_addermap', libdir + '/techmap/yosys/cells_adders.v')

        # Openroad specific files
        lib.set('option', 'file', 'openroad_pdngen',
                libdir + '/apr/openroad/pdngen.tcl')
        lib.set('option', 'file', 'openroad_global_connect',
                libdir + '/apr/openroad/global_connect.tcl')
        lib.set('option', 'file', 'openroad_tapcells',
                libdir + '/apr/openroad/tapcell.tcl')

        lib.set('option', 'var', 'openroad_cts_clock_buffer', f"sky130_fd_sc_{libtype}__clkbuf_4")

        lib.set('option', 'var', 'yosys_abc_clock_multiplier', "1000")  # convert from ns -> ps

        cap_table = {
            'hd': 1.872,
            'hdll': 1.911
        }
        lib.set('option', 'var', 'yosys_abc_constraint_load', f"{4 * cap_table[libtype]}fF")

        lib.set('option', 'var', 'yosys_driver_cell', f"sky130_fd_sc_{libtype}__buf_4")
        lib.set('option', 'var', 'yosys_buffer_cell', f"sky130_fd_sc_{libtype}__buf_4")
        lib.set('option', 'var', 'yosys_buffer_input', "A")
        lib.set('option', 'var', 'yosys_buffer_output', "X")
        for tool in ('yosys', 'openroad'):
            lib.set('option', 'var', f'{tool}_tiehigh_cell', f"sky130_fd_sc_{libtype}__conb_1")
            lib.set('option', 'var', f'{tool}_tiehigh_port', "HI")
            lib.set('option', 'var', f'{tool}_tielow_cell', f"sky130_fd_sc_{libtype}__conb_1")
            lib.set('option', 'var', f'{tool}_tielow_port', "LO")

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
