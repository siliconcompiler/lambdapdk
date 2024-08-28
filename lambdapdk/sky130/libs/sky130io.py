import os
import siliconcompiler
from lambdapdk import register_data_source


def setup():
    '''
    Skywater130 I/O library.
    '''
    process = 'skywater130'
    libname = 'sky130io'
    stackup = '5M1LI'

    lib = siliconcompiler.Library(libname, package='lambdapdk')
    register_data_source(lib)

    libdir = os.path.join('lambdapdk', 'sky130', 'libs', libname)

    # pdk
    lib.set('option', 'pdk', process)

    for corner in ['slow', 'typical', 'fast']:
        # Only one corner provided
        lib.set('output', corner, 'nldm', os.path.join(libdir, 'nldm', 'sky130_dummy_io.lib'))
    lib.set('output', stackup, 'lef', os.path.join(libdir, 'lef', 'sky130_ef_io.lef'))

    # Need both GDS files: ef relies on fd one
    lib.add('output', stackup, 'gds', os.path.join(libdir, 'gds', 'sky130_ef_io.gds'))
    lib.add('output', stackup, 'gds', os.path.join(libdir, 'gds', 'sky130_fd_io.gds'))
    lib.add('output', stackup, 'gds', os.path.join(libdir, 'gds',
                                                   'sky130_ef_io__gpiov2_pad_wrapped.gds'))

    lib.set('asic', 'cells', 'filler', ['sky130_ef_io__com_bus_slice_1um',
                                        'sky130_ef_io__com_bus_slice_5um',
                                        'sky130_ef_io__com_bus_slice_10um',
                                        'sky130_ef_io__com_bus_slice_20um'])

    lib.set('output', 'blackbox', 'verilog', os.path.join(libdir, 'blackbox', 'sky130_ef_io.v'))
    lib.add('output', 'blackbox', 'verilog', os.path.join(libdir, 'blackbox', 'sky130_fd_io.v'))

    lambda_lib = siliconcompiler.Library(f'lambdalib_{libname}', package='lambdapdk')
    register_data_source(lambda_lib)
    lambda_lib.add('option', 'ydir', 'lambdapdk/sky130/libs/sky130io/lambda')
    lambda_lib.use(lib)
    lambda_lib.set('asic', 'macrolib', lib.design)

    return [lib, lambda_lib]


#########################
if __name__ == "__main__":
    for lib in setup(siliconcompiler.Chip('<lib>')):
        lib.write_manifest(f'{lib.top()}.json')
