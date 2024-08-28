import os
import siliconcompiler
from lambdapdk import register_data_source


def setup():
    '''
    Nangate open standard cell library for FreePDK45.
    '''
    libname = 'nangate45'
    process = 'freepdk45'
    stackup = '10M'
    libtype = '10t'
    version = 'r1p0'
    corner = 'typical'

    lib = siliconcompiler.Library(libname, package='lambdapdk')
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
    lib.set('asic', 'site', libtype, 'FreePDK45_38x28_10R_NP_162NW_34O')

    # timing
    lib.add('output', corner, 'nldm', libdir + '/nldm/NangateOpenCellLibrary_typical.lib')

    # lef
    lib.add('output', stackup, 'lef', libdir + '/lef/NangateOpenCellLibrary.macro.mod.lef')

    # gds
    lib.add('output', stackup, 'gds', libdir + '/gds/NangateOpenCellLibrary.gds')

    # cdl
    lib.add('output', stackup, 'cdl', libdir + '/cdl/NangateOpenCellLibrary.cdl')

    # clock buffers
    lib.add('asic', 'cells', 'clkbuf', "BUF_X4")

    # tie cells
    lib.add('asic', 'cells', 'tie', ["LOGIC1_X1",
                                     "LOGIC0_X1"])

    # hold cells
    lib.add('asic', 'cells', 'hold', "BUF_X1")

    # filler
    lib.add('asic', 'cells', 'filler', ["FILLCELL_X1",
                                        "FILLCELL_X2",
                                        "FILLCELL_X4",
                                        "FILLCELL_X8",
                                        "FILLCELL_X16",
                                        "FILLCELL_X32"])

    # Stupid small cells
    lib.add('asic', 'cells', 'dontuse', ["OAI211_X1"])

    # Tapcell
    lib.add('asic', 'cells', 'tap', "TAPCELL_X1")

    # Endcap
    lib.add('asic', 'cells', 'endcap', "TAPCELL_X1")

    # Techmap
    lib.add('option', 'file', 'yosys_techmap', libdir + '/techmap/yosys/cells_latch.v')
    lib.add('option', 'file', 'yosys_addermap', libdir + '/techmap/yosys/cells_adders.v')

    # Defaults for OpenROAD tool variables
    lib.set('option', 'var', 'openroad_place_density', '0.50')
    lib.set('option', 'var', 'openroad_pad_global_place', '0')
    lib.set('option', 'var', 'openroad_pad_detail_place', '0')
    lib.set('option', 'var', 'openroad_macro_place_halo', ['22.4', '15.12'])
    lib.set('option', 'var', 'openroad_macro_place_channel', ['18.8', '19.95'])

    lib.set('option', 'file', 'openroad_tapcells', libdir + '/apr/openroad/tapcell.tcl')
    lib.set('option', 'file', 'openroad_pdngen', libdir + '/apr/openroad/pdngen.tcl')
    lib.set('option', 'file', 'openroad_global_connect',
            libdir + '/apr/openroad/global_connect.tcl')

    lib.set('option', 'var', 'yosys_abc_clock_multiplier', "1000")  # convert from ns -> ps
    lib.set('option', 'var', 'yosys_abc_constraint_load', "3.898fF")  # BUF_X1 = 0.974659 x 4
    lib.set('option', 'var', 'yosys_driver_cell', "BUF_X4")
    lib.set('option', 'var', 'yosys_buffer_cell', "BUF_X1")
    lib.set('option', 'var', 'yosys_buffer_input', "A")
    lib.set('option', 'var', 'yosys_buffer_output', "Z")
    for tool in ('yosys', 'openroad'):
        lib.set('option', 'var', f'{tool}_tiehigh_cell', "LOGIC1_X1")
        lib.set('option', 'var', f'{tool}_tiehigh_port', "Z")
        lib.set('option', 'var', f'{tool}_tielow_cell', "LOGIC0_X1")
        lib.set('option', 'var', f'{tool}_tielow_port', "Z")

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


#########################
if __name__ == "__main__":
    lib = setup(siliconcompiler.Chip('<lib>'))
    lib.write_manifest(f'{lib.top()}.json')
