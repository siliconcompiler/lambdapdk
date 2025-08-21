from lambdapdk import register_data_source

from pathlib import Path

from lambdapdk import LambdaLibrary, _LambdaPath, LambalibTechLibrary
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
    GF180_5LM_1TM_11K_9t, \
    GF180_6LM_1TM_9K_7t, \
    GF180_6LM_1TM_9K_9t


class _GF180SRAMLibrary(LambdaLibrary):
    def __init__(self, config):
        super().__init__()
        self.set_name(f"gf180mcu_fd_ip_sram__sram{config}m8wm1")

        self.add_asic_pdk(GF180_3LM_1TM_6K_7t(), default=False)
        self.add_asic_pdk(GF180_3LM_1TM_6K_9t(), default=False)
        self.add_asic_pdk(GF180_3LM_1TM_9K_7t(), default=False)
        self.add_asic_pdk(GF180_3LM_1TM_9K_9t(), default=False)
        self.add_asic_pdk(GF180_3LM_1TM_11K_7t(), default=False)
        self.add_asic_pdk(GF180_3LM_1TM_11K_9t(), default=False)
        self.add_asic_pdk(GF180_3LM_1TM_30K_7t(), default=False)
        self.add_asic_pdk(GF180_3LM_1TM_30K_9t(), default=False)
        self.add_asic_pdk(GF180_4LM_1TM_6K_7t(), default=False)
        self.add_asic_pdk(GF180_4LM_1TM_6K_9t(), default=False)
        self.add_asic_pdk(GF180_4LM_1TM_9K_7t(), default=False)
        self.add_asic_pdk(GF180_4LM_1TM_9K_9t(), default=False)
        self.add_asic_pdk(GF180_4LM_1TM_11K_7t(), default=False)
        self.add_asic_pdk(GF180_4LM_1TM_11K_9t(), default=False)
        self.add_asic_pdk(GF180_4LM_1TM_30K_7t(), default=False)
        self.add_asic_pdk(GF180_4LM_1TM_30K_9t(), default=False)
        self.add_asic_pdk(GF180_5LM_1TM_9K_7t(), default=False)
        self.add_asic_pdk(GF180_5LM_1TM_9K_9t(), default=False)
        self.add_asic_pdk(GF180_5LM_1TM_11K_7t(), default=False)
        self.add_asic_pdk(GF180_5LM_1TM_11K_9t(), default=False)
        self.add_asic_pdk(GF180_6LM_1TM_9K_7t(), default=False)
        self.add_asic_pdk(GF180_6LM_1TM_9K_9t(), default=False)

        path_base = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_ip_sram")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("models.physical"):
                self.add_file(path_base / "lef" / f"{self.name}.lef")
                self.add_file(path_base / "gds" / f"{self.name}.gds.gz")
                self.add_asic_aprfileset()

            with self.active_fileset("models.lvs"):
                self.add_file(path_base / "cdl" / f"{self.name}.cdl")
                self.add_asic_aprfileset()

            for corner_name, filename in [
                    ('slow', f'{self.name}__ss_125C_4v50.lib.gz'),
                    ('typical', f'{self.name}__tt_025C_5v00.lib.gz'),
                    ('fast', f'{self.name}__ff_n40C_5v50.lib.gz')]:
                with self.active_fileset(f"models.timing.nldm.{corner_name}"):
                    self.add_file(path_base / "nldm" / filename)
                    self.add_asic_libcornerfileset(corner_name, "nldm")

            with self.active_fileset("models.spice"):
                self.add_file(path_base / "spice" / f"{self.name}.spice")

            self.add_openroad_power_grid_file(path_base / "apr" / "openroad" / "pdngen.tcl")
            self.add_openroad_global_connect_file(
                path_base / "apr" / "openroad" / "global_connect.tcl")


class GF180_SRAM_64x8(_GF180SRAMLibrary):
    def __init__(self):
        super().__init__("64x8")


class GF180_SRAM_128x8(_GF180SRAMLibrary):
    def __init__(self):
        super().__init__("128x8")


class GF180_SRAM_256x8(_GF180SRAMLibrary):
    def __init__(self):
        super().__init__("256x8")


class GF180_SRAM_512x8(_GF180SRAMLibrary):
    def __init__(self):
        super().__init__("512x8")


class GF180Lambdalib_SinglePort(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_spram", [
            GF180_SRAM_64x8,
            GF180_SRAM_128x8,
            GF180_SRAM_256x8,
            GF180_SRAM_512x8])
        self.set_name("gf180_la_spram")

        # version
        self.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_ip_sram")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_spram.v")


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

        lib.set('option', 'file', 'openroad_pdngen',
                f'{path_base}/apr/openroad/pdngen.tcl')
        lib.set('option', 'file', 'openroad_global_connect',
                f'{path_base}/apr/openroad/global_connect.tcl')

        libs.append(lib)

    lambda_lib = Library('lambdalib_gf180sram', package='lambdapdk')
    register_data_source(lambda_lib)
    lambda_lib.add('option', 'ydir', 'lambdapdk/gf180/libs/gf180mcu_fd_ip_sram/lambda')
    for lib in libs:
        lambda_lib.use(lib)
        lambda_lib.add('asic', 'macrolib', lib.design)

    libs.append(lambda_lib)

    return libs
