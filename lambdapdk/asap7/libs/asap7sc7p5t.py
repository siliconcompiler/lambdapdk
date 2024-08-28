import os
import siliconcompiler
from lambdapdk import register_data_source


def _setup_lib(libname, suffix):
    lib = siliconcompiler.Library(libname, package='lambdapdk')
    register_data_source(lib)

    process = 'asap7'
    stackup = '10M'
    libtype = '7p5t'
    rev = '28'
    corners = {'typical': 'TT',
               'fast': 'FF',
               'slow': 'SS'}

    libdir = os.path.join('lambdapdk', process, 'libs', libname)

    # rev
    lib.set('package', 'version', rev)

    # todo: remove later
    lib.set('option', 'pdk', process)

    # timing
    for corner_name, lib_corner in corners.items():
        for lib_type in ('AO', 'INVBUF', 'OA', 'SEQ', 'SIMPLE'):
            lib.add('output', corner_name, 'nldm',
                    libdir + f'/nldm/asap7sc7p5t_{lib_type}_{suffix}VT_{lib_corner}_nldm.lib.gz')
        # spice
        lib.add('output', corner_name, 'spice', libdir + f'/netlist/asap7sc7p5t_28_{suffix}.sp')

    # lef
    lib.add('output', stackup, 'lef', libdir + f'/lef/asap7sc7p5t_28_{suffix}.lef')

    # gds
    lib.add('output', stackup, 'gds', libdir + f'/gds/asap7sc7p5t_28_{suffix}.gds.gz')

    # cdl
    lib.add('output', stackup, 'cdl', libdir + f'/netlist/asap7sc7p5t_28_{suffix}.cdl')

    # lib arch
    lib.set('asic', 'libarch', libtype)

    # site name
    lib.set('asic', 'site', libtype, 'asap7sc7p5t')

    # clock buffers
    lib.add('asic', 'cells', 'clkbuf', f"BUFx2_ASAP7_75t_{suffix}")

    # tie cells
    lib.add('asic', 'cells', 'tie', [f"TIEHIx1_ASAP7_75t_{suffix}",
                                     f"TIELOx1_ASAP7_75t_{suffix}"])

    # hold cells
    lib.add('asic', 'cells', 'hold', f"BUFx2_ASAP7_75t_{suffix}")

    # filler
    lib.add('asic', 'cells', 'filler', [f"FILLER_ASAP7_75t_{suffix}",
                                        f"FILLERxp5_ASAP7_75t_{suffix}"])

    # decap
    lib.add('asic', 'cells', 'decap', [f"DECAPx1_ASAP7_75t_{suffix}",
                                       f"DECAPx1_ASAP7_75t_{suffix}",
                                       f"DECAPx3_ASAP7_75t_{suffix}",
                                       f"DECAPx6_ASAP7_75t_{suffix}",
                                       f"DECAPx10_ASAP7_75t_{suffix}"])

    # Stupid small cells
    lib.add('asic', 'cells', 'dontuse', ["*x1p*_ASAP7*",
                                         "*xp*_ASAP7*",
                                         "SDF*",
                                         "ICG*"])

    # Tapcell
    lib.add('asic', 'cells', 'tap', f"TAPCELL_ASAP7_75t_{suffix}")

    # Endcap
    lib.add('asic', 'cells', 'endcap', f"DECAPx1_ASAP7_75t_{suffix}")

    # Yosys techmap
    lib.add('option', 'file', 'yosys_techmap', libdir + '/techmap/yosys/cells_latch.v')
    lib.add('option', 'file', 'yosys_addermap', libdir + '/techmap/yosys/cells_adders.v')
    lib.set('option', 'file', 'yosys_dff_liberty',
            libdir + f'/nldm/asap7sc7p5t_SEQ_{suffix}VT_SS_nldm.lib.gz')

    # Defaults for OpenROAD tool variables
    lib.set('option', 'var', 'openroad_place_density', '0.60')
    lib.set('option', 'var', 'openroad_pad_global_place', '0')
    lib.set('option', 'var', 'openroad_pad_detail_place', '0')
    lib.set('option', 'var', 'openroad_macro_place_halo', ['10', '10'])
    lib.set('option', 'var', 'openroad_macro_place_channel', ['12', '12'])

    lib.set('option', 'var', 'openroad_cts_clock_buffer', f"BUFx4_ASAP7_75t_{suffix}")
    lib.set('option', 'var', 'openroad_cts_distance_between_buffers', "60")

    lib.set('option', 'var', 'yosys_abc_clock_multiplier', "1")  # convert from ps -> ps

    cap_table = {  # BUFx2_ASAP7_75t_
        'R': 0.506500,
        'L': 0.519810,
        'SL': 0.533411
    }
    lib.set('option', 'var', 'yosys_abc_constraint_load', f"{4 * cap_table[suffix]}fF")
    lib.set('option', 'var', 'yosys_driver_cell', f"BUFx2_ASAP7_75t_{suffix}")
    lib.set('option', 'var', 'yosys_buffer_cell', f"BUFx2_ASAP7_75t_{suffix}")
    lib.set('option', 'var', 'yosys_buffer_input', "A")
    lib.set('option', 'var', 'yosys_buffer_output', "Y")
    for tool in ('yosys', 'openroad'):
        lib.set('option', 'var', f'{tool}_tiehigh_cell', f"TIEHIx1_ASAP7_75t_{suffix}")
        lib.set('option', 'var', f'{tool}_tiehigh_port', "H")
        lib.set('option', 'var', f'{tool}_tielow_cell', f"TIELOx1_ASAP7_75t_{suffix}")
        lib.set('option', 'var', f'{tool}_tielow_port', "L")

    # Openroad APR setup files
    lib.set('option', 'file', 'openroad_tracks', libdir + '/apr/openroad/tracks.tcl')
    lib.set('option', 'file', 'openroad_tapcells', libdir + '/apr/openroad/tapcells.tcl')
    lib.set('option', 'file', 'openroad_pdngen', libdir + '/apr/openroad/pdngen.tcl')
    lib.set('option', 'file', 'openroad_global_connect',
            libdir + '/apr/openroad/global_connect.tcl')

    libs = [lib]
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


def setup():
    '''
    ASAP 7 7.5-track standard cell library.
    '''
    all_libs = {
        'asap7sc7p5t_rvt': 'R',
        'asap7sc7p5t_lvt': 'L',
        'asap7sc7p5t_slvt': 'SL'
    }

    libs = []
    for libname, suffix in all_libs.items():
        libs.extend(_setup_lib(libname, suffix))

    return libs


#########################
if __name__ == "__main__":
    for lib in setup(siliconcompiler.Chip('<lib>')):
        register_data_source(lib)
        lib.check_filepaths()
