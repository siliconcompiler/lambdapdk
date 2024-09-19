import os
import siliconcompiler
from lambdapdk import register_data_source
from lambdapdk.ihp130 import register_ihp130_data_source


def setup():
    '''
    Nangate open standard cell library for FreePDK45.
    '''
    libname = 'sg13g2_stdcell'
    process = 'ihp130'
    stackup = '5M2TL'
    libtype = '9t'
    version = 'r1p0'

    lib = siliconcompiler.Library(libname, package='ihp130')
    register_ihp130_data_source(lib)
    register_data_source(lib)

    libdir = os.path.join('lambdapdk', process, 'libs', libname)

    # version
    lib.set('package', 'version', version)

    # list of stackups supported
    lib.set('option', 'stackup', stackup)

    # list of pdks supported
    lib.set('option', 'pdk', process)

    # footprint/type/sites
    lib.set('asic', 'libarch', libtype)
    lib.set('asic', 'site', libtype, 'CoreSite')

    # timing
    lib.add('output', 'typ', 'nldm',
            'ihp-sg13g2/libs.ref/sg13g2_stdcell/lib/sg13g2_stdcell_typ_1p20V_25C.lib')
    lib.add('output', 'fast', 'nldm',
            'ihp-sg13g2/libs.ref/sg13g2_stdcell/lib/sg13g2_stdcell_fast_1p32V_m40C.lib')
    lib.add('output', 'slow', 'nldm',
            'ihp-sg13g2/libs.ref/sg13g2_stdcell/lib/sg13g2_stdcell_slow_1p08V_125C.lib')

    # lef
    lib.add('output', stackup, 'lef',
            'ihp-sg13g2/libs.ref/sg13g2_stdcell/lef/sg13g2_stdcell.lef')

    # gds
    lib.add('output', stackup, 'gds',
            'ihp-sg13g2/libs.ref/sg13g2_stdcell/gds/sg13g2_stdcell.gds')

    # cdl
    lib.add('output', stackup, 'cdl',
            'ihp-sg13g2/libs.ref/sg13g2_stdcell/cdl/sg13g2_stdcell.cdl')

    lib.add('output', 'rtl', 'verilog',
            'ihp-sg13g2/libs.ref/sg13g2_stdcell/verilog/sg13g2_stdcell.v')

    # clock buffers
    lib.add('asic', 'cells', 'clkbuf', ["sg13g2_buf_2",
                                        "sg13g2_buf_4"])

    # tie cells
    lib.add('asic', 'cells', 'tie', ["LOGIC1_X1",
                                     "LOGIC0_X1"])

    # hold cells
    lib.add('asic', 'cells', 'hold', ["sg13g2_buf_1",
                                      "sg13g2_buf_4"])

    # filler
    lib.add('asic', 'cells', 'filler', ["sg13g2_fill_1",
                                        "sg13g2_fill_2"])

    # decap
    lib.add('asic', 'cells', 'decap', ["sg13g2_decap_4",
                                       "sg13g2_decap_8"])

    # antenna
    lib.add('asic', 'cells', 'antenna', ["sg13g2_antennanp"])

    # Stupid small cells
    lib.add('asic', 'cells', 'dontuse', ["sg13g2_antennanp",
                                         "sg13g2_lgcp_1",
                                         "sg13g2_sighold",
                                         "sg13g2_slgcp_1",
                                         "sg13g2_dfrbp_2"])

    # Techmap
    lib.add('option', 'file', 'yosys_techmap',
            libdir + '/techmap/yosys/cells_latch.v',
            package='lambdapdk')

    # Defaults for OpenROAD tool variables
    lib.set('option', 'var', 'openroad_place_density', '0.65')
    lib.set('option', 'var', 'openroad_pad_global_place', '0')
    lib.set('option', 'var', 'openroad_pad_detail_place', '0')
    lib.set('option', 'var', 'openroad_macro_place_halo', ['40', '40'])
    lib.set('option', 'var', 'openroad_macro_place_channel', ['80', '80'])

    lib.set('option', 'file', 'openroad_tapcells', libdir + '/apr/openroad/tapcell.tcl',
            package='lambdapdk')
    lib.set('option', 'file', 'openroad_pdngen', libdir + '/apr/openroad/pdngen.tcl',
            package='lambdapdk')
    lib.set('option', 'file', 'openroad_global_connect',
            libdir + '/apr/openroad/global_connect.tcl',
            package='lambdapdk')

    lib.set('option', 'var', 'yosys_abc_clock_multiplier', "1000")  # convert from ns -> ps
    lib.set('option', 'var', 'yosys_abc_constraint_load', "6.0fF")  # BUF_X1 = 0.974659 x 4
    lib.set('option', 'var', 'yosys_driver_cell', "sg13g2_buf_4")
    lib.set('option', 'var', 'yosys_buffer_cell', "sg13g2_buf_4")
    lib.set('option', 'var', 'yosys_buffer_input', "A")
    lib.set('option', 'var', 'yosys_buffer_output', "X")
    for tool in ('yosys', 'openroad'):
        lib.set('option', 'var', f'{tool}_tiehigh_cell', "sg13g2_tiehi")
        lib.set('option', 'var', f'{tool}_tiehigh_port', "L_HI")
        lib.set('option', 'var', f'{tool}_tielow_cell', "sg13g2_tielo")
        lib.set('option', 'var', f'{tool}_tielow_port', "L_LO")

    libs = [lib]
    for libtype in ('stdlib', 'auxlib'):
        lambda_lib = siliconcompiler.Library(f'lambdalib_{libtype}_{libname}',
                                             package='lambdapdk')
        register_data_source(lambda_lib)
        lambda_lib.add('option', 'ydir', libdir + f'/lambda/{libtype}')
        libs.append(lambda_lib)

    return libs


#########################
if __name__ == "__main__":
    lib = setup(siliconcompiler.Chip('<lib>'))
    lib.write_manifest(f'{lib.top()}.json')
