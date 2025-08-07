import os
import siliconcompiler
from lambdapdk import register_data_source

from pathlib import Path

from lambdapdk import LambdaLibrary
from lambdapdk.gf180 import GF180_3LM_1TM_6K_7t, \
    GF180_3LM_1TM_6K_9t, \
    GF180_3LM_1TM_9K_7t, \
    GF180_3LM_1TM_9K_9t, \
    GF180_3LM_1TM_11K_7t, \
    GF180_3LM_1TM_11K_9t, \
    GF180_3LM_1TM_30K_7t, \
    GF180_3LM_1TM_30K_9t, \
    GF180_4LM_1TM_6K_7t, \
    GF180_4LM_1TM_6K_9t, \
    GF180_4LM_1TM_9K_7t, \
    GF180_4LM_1TM_9K_9t, \
    GF180_4LM_1TM_11K_7t, \
    GF180_4LM_1TM_11K_9t, \
    GF180_4LM_1TM_30K_7t, \
    GF180_4LM_1TM_30K_9t, \
    GF180_5LM_1TM_9K_7t, \
    GF180_5LM_1TM_9K_9t, \
    GF180_5LM_1TM_11K_7t, \
    GF180_5LM_1TM_11K_9t


class _GF180IOLibrary(LambdaLibrary):
    def __init__(self, stackup):
        super().__init__()
        self.set_name(f"gf180mcu_fd_io_{stackup}")

        path_base = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        if stackup == "3LM":
            self.add_asic_pdk(GF180_3LM_1TM_6K_7t(), default=False)
            self.add_asic_pdk(GF180_3LM_1TM_6K_9t(), default=False)
            self.add_asic_pdk(GF180_3LM_1TM_9K_7t(), default=False)
            self.add_asic_pdk(GF180_3LM_1TM_9K_9t(), default=False)
            self.add_asic_pdk(GF180_3LM_1TM_11K_7t(), default=False)
            self.add_asic_pdk(GF180_3LM_1TM_11K_9t(), default=False)
            self.add_asic_pdk(GF180_3LM_1TM_30K_7t(), default=False)
            self.add_asic_pdk(GF180_3LM_1TM_30K_9t(), default=False)
        elif stackup == "4LM":
            self.add_asic_pdk(GF180_4LM_1TM_6K_7t(), default=False)
            self.add_asic_pdk(GF180_4LM_1TM_6K_9t(), default=False)
            self.add_asic_pdk(GF180_4LM_1TM_9K_7t(), default=False)
            self.add_asic_pdk(GF180_4LM_1TM_9K_9t(), default=False)
            self.add_asic_pdk(GF180_4LM_1TM_11K_7t(), default=False)
            self.add_asic_pdk(GF180_4LM_1TM_11K_9t(), default=False)
            self.add_asic_pdk(GF180_4LM_1TM_30K_7t(), default=False)
            self.add_asic_pdk(GF180_4LM_1TM_30K_9t(), default=False)
        elif stackup == "5LM":
            self.add_asic_pdk(GF180_5LM_1TM_9K_7t(), default=False)
            self.add_asic_pdk(GF180_5LM_1TM_9K_9t(), default=False)
            self.add_asic_pdk(GF180_5LM_1TM_11K_7t(), default=False)
            self.add_asic_pdk(GF180_5LM_1TM_11K_9t(), default=False)
        else:
            raise ValueError(f"{stackup} is not supported")

        with self.active_dataroot("lambdapdk"):
            for corner_name, filename in [
                    ('slow', 'gf180mcu_fd_io__ss_125C_2v97.lib.gz'),
                    ('typical', 'gf180mcu_fd_io__tt_025C_3v30.lib.gz'),
                    ('fast', 'gf180mcu_fd_io__ff_125C_3v63.lib.gz')]:
                with self.active_fileset(f"models.timing.{corner_name}.nldm"):
                    self.add_file(path_base / "nldm" / filename)
                    self.add_asic_libcornerfileset(corner_name, "nldm")

            with self.active_fileset("models.spice"):
                self.add_file(path_base / "spice" / stackup / "gf180mcu_fd_io.spice")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("models.physical"):
                self.add_file(path_base / "lef" / stackup / "gf180mcu_fd_io.lef")
                self.add_file(path_base / "gds" / stackup / "gf180mcu_fd_io.gds.gz")
                self.add_asic_aprfileset()

            with self.active_fileset("models.lvs"):
                self.add_file(path_base / "cdl" / "gf180mcu_fd_io.cdl")
                self.add_asic_aprfileset()

        self.add_asic_celllist("filler", [
            'gf180mcu_fd_io__fill1',
            'gf180mcu_fd_io__fill5',
            'gf180mcu_fd_io__fill10',
            'gf180mcu_fd_io__fillnc'])

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("models.blackbox"):
                self.add_file(path_base / "blackbox" / f"{stackup}.v")
            self.add_yosys_blackbox_fileset("models.blackbox")


class GF180_IO_3LM(_GF180IOLibrary):
    def __init__(self):
        super().__init__("3LM")


class GF180_IO_4LM(_GF180IOLibrary):
    def __init__(self):
        super().__init__("4LM")


class GF180_IO_5LM(_GF180IOLibrary):
    def __init__(self):
        super().__init__("5LM")


def setup():
    '''
    GloabalFoundries 180 I/O library.
    '''
    libdir = "lambdapdk/gf180/libs/gf180mcu_fd_io/"

    libs = []
    for substack in ("3LM", "4LM", "5LM"):
        lib = siliconcompiler.Library(f'gf180mcu_fd_io_{substack}', package='lambdapdk')
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

        lib.set('output', 'blackbox', 'verilog',
                os.path.join(libdir, 'blackbox', f'{stackup_start}.v'))

        libs.append(lib)

    lambda_lib = siliconcompiler.Library('lambdalib_gf180mcu_fd_io', package='lambdapdk')
    register_data_source(lambda_lib)
    lambda_lib.add('option', 'ydir', 'lambdapdk/gf180/libs/gf180mcu_fd_io/lambda')
    lambda_lib.use(lib)
    lambda_lib.set('asic', 'macrolib', lib.design)

    return [*libs, lambda_lib]


#########################
if __name__ == "__main__":
    for lib in setup(siliconcompiler.Chip('<lib>')):
        lib.write_manifest(f'{lib.top()}.json')
