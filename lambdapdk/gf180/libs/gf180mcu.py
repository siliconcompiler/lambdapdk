import siliconcompiler
from lambdapdk import register_data_source


def setup(chip):
    '''
    Skywater130 standard cell library.
    '''

    libs = []
    for libtype, sites in (("7t", "GF018hv5v_mcu_sc7"),
                           ("9t", "GF018hv5v_green_sc9")):
        libname = f'gf180mcu_fd_sc_mcu{libtype}5v0'

        libdir = f"lambdapdk/gf180/libs/{libname}/"

        lib = siliconcompiler.Library(chip, libname, package='lambdapdk')
        register_data_source(lib)

        # pdk
        lib.set('option', 'pdk', 'gf180')

        # footprint/type/sites
        lib.set('asic', 'libarch', libtype)
        lib.set('asic', 'site', libtype, sites)

        # model files
        lib.add('output', 'slow', 'nldm',
                libdir + f'/nldm/gf180mcu_fd_sc_mcu{libtype}5v0__ss_125C_4v50.lib.gz')
        lib.add('output', 'typical', 'nldm',
                libdir + f'/nldm/gf180mcu_fd_sc_mcu{libtype}5v0__tt_025C_5v00.lib.gz')
        lib.add('output', 'fast', 'nldm',
                libdir + f'/nldm/gf180mcu_fd_sc_mcu{libtype}5v0__ff_n40C_5v50.lib.gz')

        for stackup in ("3LM_1TM_6K",
                        "3LM_1TM_9K",
                        "3LM_1TM_11K",
                        "3LM_1TM_30K",
                        "4LM_1TM_6K",
                        "4LM_1TM_9K",
                        "4LM_1TM_11K",
                        "4LM_1TM_30K",
                        "5LM_1TM_9K",
                        "5LM_1TM_11K",
                        "6LM_1TM_9K"):
            lib.add('output', stackup, 'lef', libdir + f'/lef/gf180mcu_fd_sc_mcu{libtype}5v0.lef')
            lib.add('output', stackup, 'cdl', libdir + f'/cdl/gf180mcu_fd_sc_mcu{libtype}5v0.cdl')
            gds_dir = stackup[0:3]
            if gds_dir == "6LM":
                gds_dir = "5LM"
            lib.add('output', stackup, 'gds',
                    libdir + f'/gds/{gds_dir}/gf180mcu_fd_sc_mcu{libtype}5v0.gds.gz')

        # antenna cells
        lib.add('asic', 'cells', 'antenna', f'gf180mcu_fd_sc_mcu{libtype}5v0__antenna')

        # clock buffers
        for size in (1, 2, 3, 4, 8, 12, 16, 20):
            lib.add('asic', 'cells', 'clkbuf', f'gf180mcu_fd_sc_mcu{libtype}5v0__clkbuf_{size}')

        # hold / delay cells
        for variant in ('a', 'b', 'c', 'd'):
            for size in (1, 2, 4):
                lib.add('asic', 'cells', 'hold',
                        f'gf180mcu_fd_sc_mcu{libtype}5v0__dly{variant}_{size}')
                lib.add('asic', 'cells', 'delay',
                        f'gf180mcu_fd_sc_mcu{libtype}5v0__dly{variant}_{size}')

        # Decoupling
        for size in (4, 8, 16, 32, 64):
            lib.add('asic', 'cells', 'decap', f'gf180mcu_fd_sc_mcu{libtype}5v0__fillcap_{size}')

        # filler
        for size in (1, 2, 4, 8, 16, 32, 64):
            lib.add('asic', 'cells', 'filler', f'gf180mcu_fd_sc_mcu{libtype}5v0__fill_{size}')

        # Tapcell
        lib.add('asic', 'cells', 'tap', f'gf180mcu_fd_sc_mcu{libtype}5v0__filltie')

        # Endcap
        lib.add('asic', 'cells', 'endcap', f'gf180mcu_fd_sc_mcu{libtype}5v0__endcap')

        # Dont use
        lib.add('asic', 'cells', 'dontuse', '*_1')

        # tie cells
        lib.add('asic', 'cells', 'tie', [f'gf180mcu_fd_sc_mcu{libtype}5v0__tieh',
                                         f'gf180mcu_fd_sc_mcu{libtype}5v0__tiel'])

        # Defaults for OpenROAD tool variables
        lib.set('option', 'var', 'openroad_place_density', '0.4')
        lib.set('option', 'var', 'openroad_pad_global_place', '1')
        lib.set('option', 'var', 'openroad_pad_detail_place', '0')
        lib.set('option', 'var', 'openroad_macro_place_halo', ['10', '10'])
        lib.set('option', 'var', 'openroad_macro_place_channel', ['20.16', '20.16'])

        # Yosys techmap
        lib.add('option', 'file', 'yosys_techmap', libdir + '/techmap/yosys/cells_latch.v')
        lib.add('option', 'file', 'yosys_addermap', libdir + '/techmap/yosys/cells_adders.v')

        # Openroad specific files
        lib.set('option', 'file', 'openroad_pdngen',
                libdir + '/apr/openroad/pdngen.tcl')
        lib.set('option', 'file', 'openroad_global_connect',
                libdir + '/apr/openroad/global_connect.tcl')
        lib.set('option', 'file', 'openroad_tapcells',
                libdir + '/apr/openroad/tapcell.tcl')

        lib.set('option', 'var', 'openroad_cts_clock_buffer',
                f"gf180mcu_fd_sc_mcu{libtype}5v0__clkbuf_8")
        lib.set('option', 'var', 'openroad_cts_distance_between_buffers', "100")

        lib.set('option', 'var', 'yosys_abc_clock_multiplier', "1000")  # convert from ns -> ps
        lib.set('option', 'var', 'yosys_driver_cell', f"gf180mcu_fd_sc_mcu{libtype}5v0__buf_4")
        lib.set('option', 'var', 'yosys_buffer_cell', f"gf180mcu_fd_sc_mcu{libtype}5v0__buf_4")
        lib.set('option', 'var', 'yosys_buffer_input', "I")
        lib.set('option', 'var', 'yosys_buffer_output', "Z")
        for tool in ('yosys', 'openroad'):
            lib.set('option', 'var', f'{tool}_tiehigh_cell',
                    f"gf180mcu_fd_sc_mcu{libtype}5v0__tieh")
            lib.set('option', 'var', f'{tool}_tiehigh_port', "Z")
            lib.set('option', 'var', f'{tool}_tielow_cell',
                    f"gf180mcu_fd_sc_mcu{libtype}5v0__tiel")
            lib.set('option', 'var', f'{tool}_tielow_port', "ZN")

        libs.append(lib)

    return libs


#########################
if __name__ == "__main__":
    libs = setup(siliconcompiler.Chip('<lib>'))
    for lib in libs:
        lib.write_manifest(f'{lib.top()}.json')
        lib.check_filepaths()