from pathlib import Path

from siliconcompiler import ASIC
from lambdalib import LambalibTechLibrary
from lambdapdk import LambdaLibrary, _LambdaPath
from lambdapdk.gf180 import _GF180Data, variant, GF180_3LM_1TM_6K_7t, \
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


# The IO cells, one LEF each upstream. 'ef' is the Efabless-generated wrapper
# that open_pdks builds alongside the foundry 'fd' cells.
_IO_CELLS = (
    "gf180mcu_ef_io__bi_t",
    "gf180mcu_fd_io__asig_5p0",
    "gf180mcu_fd_io__bi_24t",
    "gf180mcu_fd_io__bi_t",
    "gf180mcu_fd_io__brk2",
    "gf180mcu_fd_io__brk5",
    "gf180mcu_fd_io__cor",
    "gf180mcu_fd_io__dvdd",
    "gf180mcu_fd_io__dvss",
    "gf180mcu_fd_io__fill1",
    "gf180mcu_fd_io__fill10",
    "gf180mcu_fd_io__fill5",
    "gf180mcu_fd_io__fillnc",
    "gf180mcu_fd_io__in_c",
    "gf180mcu_fd_io__in_s",
)


class _GF180IOLibrary(LambdaLibrary, _GF180Data):
    '''
    GloabalFoundries 180 I/O library.
    '''
    def __init__(self, stackup):
        super().__init__()
        self.set_name(f"gf180mcu_fd_io_{stackup}")
        self.package.set_version(self.PDK_VERSION)

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

        upstream_path = Path(variant(stackup), "libs.ref", "gf180mcu_fd_io")

        with self.active_dataroot("gf180mcu_fd_io"):
            # Upstream ships 12 corners uncompressed; these three are the set
            # this library has always registered.
            for corner_name, filename in [
                    ('slow', 'gf180mcu_fd_io__ss_125C_2v97.lib'),
                    ('typical', 'gf180mcu_fd_io__tt_025C_3v30.lib'),
                    ('fast', 'gf180mcu_fd_io__ff_125C_3v63.lib')]:
                with self.active_fileset(f"models.timing.{corner_name}.nldm"):
                    self.add_file(upstream_path / "lib" / filename)
                    self.add_asic_libcornerfileset(corner_name, "nldm")

            with self.active_fileset("models.spice"):
                self.add_file(upstream_path / "spice" / "gf180mcu_fd_io.spice")

            with self.active_fileset("models.physical"):
                # One LEF per cell, not the single merged file this used to
                # vendor. That merged LEF declared every macro *twice* -- 28
                # MACRO statements for 14 cells, in all three stackups -- and
                # was missing gf180mcu_ef_io__bi_t, which upstream ships.
                for cell in _IO_CELLS:
                    self.add_file(upstream_path / "lef" / f"{cell}.lef")
                self.add_file(upstream_path / "gds" / "gf180mcu_fd_io.gds")
                self.add_file(upstream_path / "gds" / "gf180mcu_ef_io.gds")
                self.add_asic_aprfileset()

            with self.active_fileset("models.lvs"):
                self.add_file(upstream_path / "cdl" / "gf180mcu_fd_io.cdl")
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


class GF180Lambdalib_la_iovdd_3LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovdd", [GF180_IO_3LM])
        self.set_name("gf180_3LM_la_iovdd")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovdd.v")


class GF180Lambdalib_la_iocorner_3LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iocorner", [GF180_IO_3LM])
        self.set_name("gf180_3LM_la_iocorner")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iocorner.v")


class GF180Lambdalib_la_iotxdiff_3LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iotxdiff", [GF180_IO_3LM])
        self.set_name("gf180_3LM_la_iotxdiff")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iotxdiff.v")


class GF180Lambdalib_la_ioanalog_3LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_ioanalog", [GF180_IO_3LM])
        self.set_name("gf180_3LM_la_ioanalog")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_ioanalog.v")


class GF180Lambdalib_la_ioinput_3LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_ioinput", [GF180_IO_3LM])
        self.set_name("gf180_3LM_la_ioinput")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_ioinput.v")


class GF180Lambdalib_la_iocut_3LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iocut", [GF180_IO_3LM])
        self.set_name("gf180_3LM_la_iocut")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iocut.v")


class GF180Lambdalib_la_iovss_3LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovss", [GF180_IO_3LM])
        self.set_name("gf180_3LM_la_iovss")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovss.v")


class GF180Lambdalib_la_iovddio_3LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovddio", [GF180_IO_3LM])
        self.set_name("gf180_3LM_la_iovddio")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovddio.v")


class GF180Lambdalib_la_iovssio_3LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovssio", [GF180_IO_3LM])
        self.set_name("gf180_3LM_la_iovssio")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovssio.v")


class GF180Lambdalib_la_iovdda_3LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovdda", [GF180_IO_3LM])
        self.set_name("gf180_3LM_la_iovdda")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovdda.v")


class GF180Lambdalib_la_iovssa_3LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovssa", [GF180_IO_3LM])
        self.set_name("gf180_3LM_la_iovssa")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovssa.v")


class GF180Lambdalib_la_iorxdiff_3LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iorxdiff", [GF180_IO_3LM])
        self.set_name("gf180_3LM_la_iorxdiff")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iorxdiff.v")


class GF180Lambdalib_la_iobidir_3LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iobidir", [GF180_IO_3LM])
        self.set_name("gf180_3LM_la_iobidir")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iobidir.v")


class GF180Lambdalib_IO_3LM(LambalibTechLibrary):
    @classmethod
    def alias(cls, project: ASIC):
        GF180Lambdalib_la_iovdd_3LM.alias(project)
        GF180Lambdalib_la_iocorner_3LM.alias(project)
        GF180Lambdalib_la_iotxdiff_3LM.alias(project)
        GF180Lambdalib_la_ioanalog_3LM.alias(project)
        GF180Lambdalib_la_ioinput_3LM.alias(project)
        GF180Lambdalib_la_iocut_3LM.alias(project)
        GF180Lambdalib_la_iovss_3LM.alias(project)
        GF180Lambdalib_la_iovddio_3LM.alias(project)
        GF180Lambdalib_la_iovssio_3LM.alias(project)
        GF180Lambdalib_la_iovdda_3LM.alias(project)
        GF180Lambdalib_la_iovssa_3LM.alias(project)
        GF180Lambdalib_la_iorxdiff_3LM.alias(project)
        GF180Lambdalib_la_iobidir_3LM.alias(project)


class GF180Lambdalib_la_iovdd_4LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovdd", [GF180_IO_4LM])
        self.set_name("gf180_4LM_la_iovdd")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovdd.v")


class GF180Lambdalib_la_iocorner_4LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iocorner", [GF180_IO_4LM])
        self.set_name("gf180_4LM_la_iocorner")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iocorner.v")


class GF180Lambdalib_la_iotxdiff_4LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iotxdiff", [GF180_IO_4LM])
        self.set_name("gf180_4LM_la_iotxdiff")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iotxdiff.v")


class GF180Lambdalib_la_ioanalog_4LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_ioanalog", [GF180_IO_4LM])
        self.set_name("gf180_4LM_la_ioanalog")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_ioanalog.v")


class GF180Lambdalib_la_ioinput_4LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_ioinput", [GF180_IO_4LM])
        self.set_name("gf180_4LM_la_ioinput")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_ioinput.v")


class GF180Lambdalib_la_iocut_4LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iocut", [GF180_IO_4LM])
        self.set_name("gf180_4LM_la_iocut")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iocut.v")


class GF180Lambdalib_la_iovss_4LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovss", [GF180_IO_4LM])
        self.set_name("gf180_4LM_la_iovss")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovss.v")


class GF180Lambdalib_la_iovddio_4LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovddio", [GF180_IO_4LM])
        self.set_name("gf180_4LM_la_iovddio")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovddio.v")


class GF180Lambdalib_la_iovssio_4LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovssio", [GF180_IO_4LM])
        self.set_name("gf180_4LM_la_iovssio")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovssio.v")


class GF180Lambdalib_la_iovdda_4LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovdda", [GF180_IO_4LM])
        self.set_name("gf180_4LM_la_iovdda")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovdda.v")


class GF180Lambdalib_la_iovssa_4LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovssa", [GF180_IO_4LM])
        self.set_name("gf180_4LM_la_iovssa")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovssa.v")


class GF180Lambdalib_la_iorxdiff_4LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iorxdiff", [GF180_IO_4LM])
        self.set_name("gf180_4LM_la_iorxdiff")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iorxdiff.v")


class GF180Lambdalib_la_iobidir_4LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iobidir", [GF180_IO_4LM])
        self.set_name("gf180_4LM_la_iobidir")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iobidir.v")


class GF180Lambdalib_IO_4LM(LambalibTechLibrary):
    @classmethod
    def alias(cls, project: ASIC):
        GF180Lambdalib_la_iovdd_4LM.alias(project)
        GF180Lambdalib_la_iocorner_4LM.alias(project)
        GF180Lambdalib_la_iotxdiff_4LM.alias(project)
        GF180Lambdalib_la_ioanalog_4LM.alias(project)
        GF180Lambdalib_la_ioinput_4LM.alias(project)
        GF180Lambdalib_la_iocut_4LM.alias(project)
        GF180Lambdalib_la_iovss_4LM.alias(project)
        GF180Lambdalib_la_iovddio_4LM.alias(project)
        GF180Lambdalib_la_iovssio_4LM.alias(project)
        GF180Lambdalib_la_iovdda_4LM.alias(project)
        GF180Lambdalib_la_iovssa_4LM.alias(project)
        GF180Lambdalib_la_iorxdiff_4LM.alias(project)
        GF180Lambdalib_la_iobidir_4LM.alias(project)


class GF180Lambdalib_la_iovdd_5LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovdd", [GF180_IO_5LM])
        self.set_name("gf180_5LM_la_iovdd")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovdd.v")


class GF180Lambdalib_la_iocorner_5LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iocorner", [GF180_IO_5LM])
        self.set_name("gf180_5LM_la_iocorner")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iocorner.v")


class GF180Lambdalib_la_iotxdiff_5LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iotxdiff", [GF180_IO_5LM])
        self.set_name("gf180_5LM_la_iotxdiff")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iotxdiff.v")


class GF180Lambdalib_la_ioanalog_5LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_ioanalog", [GF180_IO_5LM])
        self.set_name("gf180_5LM_la_ioanalog")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_ioanalog.v")


class GF180Lambdalib_la_ioinput_5LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_ioinput", [GF180_IO_5LM])
        self.set_name("gf180_5LM_la_ioinput")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_ioinput.v")


class GF180Lambdalib_la_iocut_5LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iocut", [GF180_IO_5LM])
        self.set_name("gf180_5LM_la_iocut")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iocut.v")


class GF180Lambdalib_la_iovss_5LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovss", [GF180_IO_5LM])
        self.set_name("gf180_5LM_la_iovss")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovss.v")


class GF180Lambdalib_la_iovddio_5LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovddio", [GF180_IO_5LM])
        self.set_name("gf180_5LM_la_iovddio")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovddio.v")


class GF180Lambdalib_la_iovssio_5LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovssio", [GF180_IO_5LM])
        self.set_name("gf180_5LM_la_iovssio")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovssio.v")


class GF180Lambdalib_la_iovdda_5LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovdda", [GF180_IO_5LM])
        self.set_name("gf180_5LM_la_iovdda")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovdda.v")


class GF180Lambdalib_la_iovssa_5LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovssa", [GF180_IO_5LM])
        self.set_name("gf180_5LM_la_iovssa")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovssa.v")


class GF180Lambdalib_la_iorxdiff_5LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iorxdiff", [GF180_IO_5LM])
        self.set_name("gf180_5LM_la_iorxdiff")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iorxdiff.v")


class GF180Lambdalib_la_iobidir_5LM(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iobidir", [GF180_IO_5LM])
        self.set_name("gf180_5LM_la_iobidir")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "gf180", "libs", "gf180mcu_fd_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iobidir.v")


class GF180Lambdalib_IO_5LM(LambalibTechLibrary):
    @classmethod
    def alias(cls, project: ASIC):
        GF180Lambdalib_la_iovdd_5LM.alias(project)
        GF180Lambdalib_la_iocorner_5LM.alias(project)
        GF180Lambdalib_la_iotxdiff_5LM.alias(project)
        GF180Lambdalib_la_ioanalog_5LM.alias(project)
        GF180Lambdalib_la_ioinput_5LM.alias(project)
        GF180Lambdalib_la_iocut_5LM.alias(project)
        GF180Lambdalib_la_iovss_5LM.alias(project)
        GF180Lambdalib_la_iovddio_5LM.alias(project)
        GF180Lambdalib_la_iovssio_5LM.alias(project)
        GF180Lambdalib_la_iovdda_5LM.alias(project)
        GF180Lambdalib_la_iovssa_5LM.alias(project)
        GF180Lambdalib_la_iorxdiff_5LM.alias(project)
        GF180Lambdalib_la_iobidir_5LM.alias(project)
