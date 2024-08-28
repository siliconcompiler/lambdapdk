from siliconcompiler import Chip, Library
from lambdapdk import register_data_source


def setup():
    libs = []

    for config in ('64x8', '128x8', '256x8', '512x8'):
        mem_name = f'gf180mcu_fd_ip_sram__sram{config}m8wm1'
        lib = Library(mem_name, package='lambdapdk')
        register_data_source(lib)

        path_base = 'lambdapdk/gf180/libs/gf180mcu_fd_ip_sram'

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
            lib.add('output', stackup, 'lef', f'{path_base}/lef/{mem_name}.lef')
            lib.add('output', stackup, 'gds', f'{path_base}/gds/{mem_name}.gds.gz')
            lib.add('output', stackup, 'cdl', f'{path_base}/cdl/{mem_name}.cdl')

        lib.add('output', 'slow', 'nldm',
                f'{path_base}/nldm/{mem_name}__ss_125C_4v50.lib.gz')
        lib.add('output', 'typical', 'nldm',
                f'{path_base}/nldm/{mem_name}__tt_025C_5v00.lib.gz')
        lib.add('output', 'fast', 'nldm',
                f'{path_base}/nldm/{mem_name}__ff_n40C_5v50.lib.gz')

        for corner in ('slow', 'typical', 'fast'):
            lib.add('output', corner, 'spice',
                    f'{path_base}/spice/{mem_name}.spice')

        lib.set('option', 'file', 'openroad_pdngen', f'{path_base}/pdngen.tcl')

        libs.append(lib)

    lambda_lib = Library('lambdalib_gf180sram', package='lambdapdk')
    register_data_source(lambda_lib)
    lambda_lib.add('option', 'ydir', 'lambdapdk/gf180/libs/gf180mcu_fd_ip_sram/lambda')
    for lib in libs:
        lambda_lib.use(lib)
        lambda_lib.add('asic', 'macrolib', lib.design)

    libs.append(lambda_lib)

    return libs


#########################
if __name__ == "__main__":
    for lib in setup(Chip('<lib>')):
        lib.write_manifest(f'{lib.top()}.json')
