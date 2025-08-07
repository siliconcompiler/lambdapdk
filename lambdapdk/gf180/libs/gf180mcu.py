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
    GF180_5LM_1TM_11K_9t, \
    GF180_6LM_1TM_9K_7t, \
    GF180_6LM_1TM_9K_9t


class _GF180_MCULibrary(LambdaLibrary):
    def __init__(self, libtype, stackup):
        super().__init__()
        self.set_name(f"gf180mcu_fd_sc_mcu{libtype}5v0_{stackup}")

        if libtype == "7t":
            if stackup == "3LM":
                self.add_asic_pdk(GF180_3LM_1TM_6K_7t(), default=False)
                self.add_asic_pdk(GF180_3LM_1TM_9K_7t(), default=False)
                self.add_asic_pdk(GF180_3LM_1TM_11K_7t(), default=False)
                self.add_asic_pdk(GF180_3LM_1TM_30K_7t(), default=False)
            elif stackup == "4LM":
                self.add_asic_pdk(GF180_4LM_1TM_6K_7t(), default=False)
                self.add_asic_pdk(GF180_4LM_1TM_9K_7t(), default=False)
                self.add_asic_pdk(GF180_4LM_1TM_11K_7t(), default=False)
                self.add_asic_pdk(GF180_4LM_1TM_30K_7t(), default=False)
            elif stackup == "5LM":
                self.add_asic_pdk(GF180_5LM_1TM_9K_7t(), default=False)
                self.add_asic_pdk(GF180_5LM_1TM_11K_7t(), default=False)
            elif stackup == "6LM":
                self.add_asic_pdk(GF180_6LM_1TM_9K_7t())
            else:
                raise ValueError(f"{stackup} is not supported")

            self.add_asic_site("GF018hv5v_mcu_sc7")
        elif libtype == "9t":
            if stackup == "3LM":
                self.add_asic_pdk(GF180_3LM_1TM_6K_9t(), default=False)
                self.add_asic_pdk(GF180_3LM_1TM_9K_9t(), default=False)
                self.add_asic_pdk(GF180_3LM_1TM_11K_9t(), default=False)
                self.add_asic_pdk(GF180_3LM_1TM_30K_9t(), default=False)
            elif stackup == "4LM":
                self.add_asic_pdk(GF180_4LM_1TM_6K_9t(), default=False)
                self.add_asic_pdk(GF180_4LM_1TM_9K_9t(), default=False)
                self.add_asic_pdk(GF180_4LM_1TM_11K_9t(), default=False)
                self.add_asic_pdk(GF180_4LM_1TM_30K_9t(), default=False)
            elif stackup == "5LM":
                self.add_asic_pdk(GF180_5LM_1TM_9K_9t(), default=False)
                self.add_asic_pdk(GF180_5LM_1TM_11K_9t(), default=False)
            elif stackup == "6LM":
                self.add_asic_pdk(GF180_6LM_1TM_9K_9t())
            else:
                raise ValueError(f"{stackup} is not supported")

            self.add_asic_site("GF018hv5v_green_sc9")
        else:
            raise ValueError(f"{libtype} is not supported")

        lib_path = Path("lambdapdk", "gf180", "libs", f"gf180mcu_fd_sc_mcu{libtype}5v0")

        with self.active_dataroot("lambdapdk"):
            for corner_name, filename in [
                    ('slow', f'gf180mcu_fd_sc_mcu{libtype}5v0__ss_125C_4v50.lib.gz'),
                    ('typical', f'gf180mcu_fd_sc_mcu{libtype}5v0__tt_025C_5v00.lib.gz'),
                    ('fast', f'gf180mcu_fd_sc_mcu{libtype}5v0__ff_n40C_5v50.lib.gz')]:
                with self.active_fileset(f"models.timing.{corner_name}.nldm"):
                    self.add_file(lib_path / "nldm" / filename)
                    self.add_asic_libcornerfileset(corner_name, "nldm")

            with self.active_fileset("models.spice"):
                self.add_file(lib_path / "spice" / f"gf180mcu_fd_sc_mcu{libtype}5v0.spice")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("models.physical"):
                self.add_file(lib_path / "lef" / f"gf180mcu_fd_sc_mcu{libtype}5v0.lef")
                gds_dir = stackup[0:3]
                if gds_dir == "6LM":
                    gds_dir = "5LM"
                self.add_file(lib_path / "gds" / gds_dir / f"gf180mcu_fd_sc_mcu{libtype}5v0.gds.gz")
                self.add_asic_aprfileset()

            with self.active_fileset("models.lvs"):
                self.add_file(lib_path / "cdl" / f"gf180mcu_fd_sc_mcu{libtype}5v0.cdl")
                self.add_asic_aprfileset()

        # antenna cells
        self.add_asic_celllist('antenna', f'gf180mcu_fd_sc_mcu{libtype}5v0__antenna')

        # clock buffers
        for size in (1, 2, 3, 4, 8, 12, 16, 20):
            self.add_asic_celllist('clkbuf', f'gf180mcu_fd_sc_mcu{libtype}5v0__clkbuf_{size}')

        # hold cells
        for variant in ('a', 'b', 'c', 'd'):
            for size in (1, 2, 4):
                self.add_asic_celllist(
                    'hold',
                    f'gf180mcu_fd_sc_mcu{libtype}5v0__dly{variant}_{size}')

        # Decoupling
        for size in (4, 8, 16, 32, 64):
            self.add_asic_celllist('decap', f'gf180mcu_fd_sc_mcu{libtype}5v0__fillcap_{size}')

        # filler
        for size in (1, 2, 4, 8, 16, 32, 64):
            self.add_asic_celllist('filler', f'gf180mcu_fd_sc_mcu{libtype}5v0__fill_{size}')

        # Tapcell
        self.add_asic_celllist('tap', f'gf180mcu_fd_sc_mcu{libtype}5v0__filltie')

        # Endcap
        self.add_asic_celllist('endcap', f'gf180mcu_fd_sc_mcu{libtype}5v0__endcap')

        # Dont use
        self.add_asic_celllist('dontuse', '*_1')

        # tie cells
        self.add_asic_celllist('tie', [f'gf180mcu_fd_sc_mcu{libtype}5v0__tieh',
                                       f'gf180mcu_fd_sc_mcu{libtype}5v0__tiel'])

        # Setup for yosys
        with self.active_dataroot("lambdapdk"):
            cap_table = {  # __buf_4
                '7t': 38,
                '9t': 56
            }
            self.set_yosys_driver_cell(f"gf180mcu_fd_sc_mcu{libtype}5v0__buf_4")
            self.set_yosys_buffer_cell(f"gf180mcu_fd_sc_mcu{libtype}5v0__buf_4", "I", "Z")
            self.set_yosys_tielow_cell(f"gf180mcu_fd_sc_mcu{libtype}5v0__tiel", "Z")
            self.set_yosys_tiehigh_cell(f"gf180mcu_fd_sc_mcu{libtype}5v0__tieh", "Z")
            self.set_yosys_abc(1000, cap_table[libtype])
            self.set_yosys_tristatebuffer_map(
                lib_path / "techmap" / "yosys" / "cells_tristatebuf.v")
            self.set_yosys_adder_map(lib_path / "techmap" / "yosys" / "cells_adders.v")
            self.add_yosys_tech_map(lib_path / "techmap" / "yosys" / "cells_latch.v")

        # Setup for OpenROAD
        with self.active_dataroot("lambdapdk"):
            self.set_openroad_placement_density(0.50)
            self.set_openroad_tielow_cell(f"gf180mcu_fd_sc_mcu{libtype}5v0__tiel", "Z")
            self.set_openroad_tiehigh_cell(f"gf180mcu_fd_sc_mcu{libtype}5v0__tieh", "Z")
            self.set_openroad_macro_placement_halo(15, 15)
            self.set_openroad_tapcells_file(lib_path / "apr" / "openroad" / "tapcell.tcl")
            self.add_openroad_global_connect_file(
                lib_path / "apr" / "openroad" / "global_connect.tcl")
            self.add_openroad_power_grid_file(lib_path / "apr" / "openroad" / "pdngen.tcl")

        # Setup for bambu
        self.set_bambu_clock_multiplier(1)


class GF180_MCU_7T_3LMLibrary(_GF180_MCULibrary):
    def __init__(self):
        super().__init__("7t", "3LM")


class GF180_MCU_7T_4LMLibrary(_GF180_MCULibrary):
    def __init__(self):
        super().__init__("7t", "4LM")


class GF180_MCU_7T_5LMLibrary(_GF180_MCULibrary):
    def __init__(self):
        super().__init__("7t", "5LM")


class GF180_MCU_7T_6LMLibrary(_GF180_MCULibrary):
    def __init__(self):
        super().__init__("7t", "6LM")


class GF180_MCU_9T_3LMLibrary(_GF180_MCULibrary):
    def __init__(self):
        super().__init__("9t", "3LM")


class GF180_MCU_9T_4LMLibrary(_GF180_MCULibrary):
    def __init__(self):
        super().__init__("9t", "4LM")


class GF180_MCU_9T_5LMLibrary(_GF180_MCULibrary):
    def __init__(self):
        super().__init__("9t", "5LM")


class GF180_MCU_9T_6LMLibrary(_GF180_MCULibrary):
    def __init__(self):
        super().__init__("9t", "6LM")


def setup():
    '''
    Skywater130 standard cell library.
    '''

    libs = []
    for libtype, sites in (("7t", "GF018hv5v_mcu_sc7"),
                           ("9t", "GF018hv5v_green_sc9")):
        libname = f'gf180mcu_fd_sc_mcu{libtype}5v0'

        libdir = f"lambdapdk/gf180/libs/{libname}/"

        lib = siliconcompiler.Library(libname, package='lambdapdk')
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

        for corner in ('slow', 'typical', 'fast'):
            lib.add('output', corner, 'spice',
                    libdir + f'/spice/gf180mcu_fd_sc_mcu{libtype}5v0.spice')

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

        # hold cells
        for variant in ('a', 'b', 'c', 'd'):
            for size in (1, 2, 4):
                lib.add('asic', 'cells', 'hold',
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
        lib.set('option', 'var', 'openroad_place_density', '0.50')
        lib.set('option', 'var', 'openroad_pad_global_place', '0')
        lib.set('option', 'var', 'openroad_pad_detail_place', '0')
        lib.set('option', 'var', 'openroad_macro_place_halo', ['15', '15'])
        lib.set('option', 'var', 'openroad_macro_place_channel', ['30.16', '30.16'])

        # Yosys techmap
        lib.add('option', 'file', 'yosys_techmap', libdir + '/techmap/yosys/cells_latch.v')
        lib.add('option', 'file', 'yosys_addermap', libdir + '/techmap/yosys/cells_adders.v')
        lib.add('option', 'file', 'yosys_tbufmap', libdir + '/techmap/yosys/cells_tristatebuf.v')

        # Openroad specific files
        lib.set('option', 'file', 'openroad_pdngen',
                libdir + '/apr/openroad/pdngen.tcl')
        lib.set('option', 'file', 'openroad_global_connect',
                libdir + '/apr/openroad/global_connect.tcl')
        lib.set('option', 'file', 'openroad_tapcells',
                libdir + '/apr/openroad/tapcell.tcl')

        lib.set('option', 'var', 'openroad_cts_distance_between_buffers', "100")

        lib.set('option', 'var', 'yosys_abc_clock_multiplier', "1000")  # convert from ns -> ps

        cap_table = {  # __buf_4
            '7t': "0.038pF",
            '9t': "0.056pF"
        }
        lib.set('option', 'var', 'yosys_abc_constraint_load', cap_table[libtype])
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

        # Bambu setup
        lib.set('option', 'var', 'bambu_clock_multiplier', "1")  # convert from ns -> ns

        libs.append(lib)

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
    libs = setup()
    for lib in libs:
        lib.write_manifest(f'{lib.top()}.json')
        lib.check_filepaths()
