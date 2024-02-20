import os
import siliconcompiler
from lambdapdk import register_data_source


def setup(chip):
    '''
    GloabalFoundries 180 I/O library.
    '''
    libdir = "lambdapdk/gf180/libs/gf180mcu_fd_io/"

    libs = []
    for substack in ("3LM", "4LM", "5LM"):
        lib = siliconcompiler.Library(chip, f'gf180mcu_fd_io_{substack}', package='lambdapdk')
        register_data_source(lib)

        # pdk
        lib.set('option', 'pdk', 'gf180')

        lib.set('output', 'slow', 'nldm',
                os.path.join(libdir, 'nldm/gf180mcu_fd_io__ss_125C_2v97.lib.gz'))
        lib.set('output', 'typical', 'nldm',
                os.path.join(libdir, 'nldm/gf180mcu_fd_io__tt_025C_3v30.lib.gz'))
        lib.set('output', 'fast', 'nldm',
                os.path.join(libdir, 'nldm/gf180mcu_fd_io__ff_125C_3v63.lib.gz'))

        for corner in ('slow', 'typical', 'fast'):
            lib.set('output', corner, 'spice',
                    os.path.join(libdir, f'spice/{substack}/gf180mcu_fd_io.spice'))

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
            if substack != stackup_start:
                continue
            lib.set('output', stackup, 'lef',
                    os.path.join(libdir, f'lef/{stackup_start}/gf180mcu_fd_io.lef'))
            lib.set('output', stackup, 'cdl', os.path.join(libdir, 'cdl/gf180mcu_fd_io.cdl'))

            lib.add('output', stackup, 'gds',
                    os.path.join(libdir, f'gds/{stackup_start}/gf180mcu_fd_io.gds.gz'))

        lib.set('asic', 'cells', 'filler', ['gf180mcu_fd_io__fill1',
                                            'gf180mcu_fd_io__fill5',
                                            'gf180mcu_fd_io__fill10',
                                            'gf180mcu_fd_io__fillnc'])

        lib.set('option', 'ydir', os.path.join(libdir, 'lambda'))
        lib.set('option', 'idir', os.path.join(libdir, 'lambda'))

        libs.append(lib)

    return libs


#########################
if __name__ == "__main__":
    lib = setup(siliconcompiler.Chip('<lib>'))
    lib.write_manifest(f'{lib.top()}.json')
    lib.check_filepaths()
