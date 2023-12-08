import os
import siliconcompiler
from lambdapdk import register_data_source


def setup(chip):
    '''
    GloabalFoundries 180 I/O library.
    '''
    libdir = "lambdapdk/gf180/libs/gf180mcu_fd_io/"

    lib = siliconcompiler.Library(chip, 'gf180mcu_fd_io', package='lambdapdk')
    register_data_source(lib)

    # pdk
    lib.set('option', 'pdk', 'gf180')

    lib.set('output', 'slow', 'nldm',
            os.path.join(libdir, 'nldm/gf180mcu_fd_io__ss_125C_2v97.lib.gz'))
    lib.set('output', 'typical', 'nldm',
            os.path.join(libdir, 'nldm/gf180mcu_fd_io__tt_025C_3v30.lib.gz'))
    lib.set('output', 'fast', 'nldm',
            os.path.join(libdir, 'nldm/gf180mcu_fd_io__ff_125C_3v63.lib.gz'))

    for stackup in ("3LM_1TM_6K",
                    "3LM_1TM_9K",
                    "3LM_1TM_11K",
                    "3LM_1TM_30K",
                    "4LM_1TM_6K",
                    "4LM_1TM_9K",
                    "4LM_1TM_11K",
                    "4LM_1TM_30K",
                    "5LM_1TM_9K",
                    "5LM_1TM_11K"):
        stackup_start = stackup[0:3]
        lib.set('output', stackup, 'lef',
                os.path.join(libdir, f'lef/{stackup_start}/gf180mcu_fd_io.lef'))
        lib.set('output', stackup, 'cdl', os.path.join(libdir, 'cdl/gf180mcu_fd_io.cdl'))

        # Need both GDS files: ef relies on fd one
        lib.add('output', stackup, 'gds',
                os.path.join(libdir, f'gds/{stackup_start}/gf180mcu_fd_io.gds.gz'))

    lib.set('asic', 'cells', 'filler', ['gf180mcu_fd_io__fill1',
                                        'gf180mcu_fd_io__fill5',
                                        'gf180mcu_fd_io__fill10',
                                        'gf180mcu_fd_io__fillnc'])

    lib.set('option', 'ydir', os.path.join(libdir, 'lambda'))
    lib.set('option', 'idir', os.path.join(libdir, 'lambda'))

    return lib


#########################
if __name__ == "__main__":
    lib = setup(siliconcompiler.Chip('<lib>'))
    lib.write_manifest(f'{lib.top()}.json')
    lib.check_filepaths()
