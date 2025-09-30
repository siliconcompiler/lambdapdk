from pathlib import Path

from siliconcompiler import ASIC
from lambdalib import LambalibTechLibrary
from lambdapdk import LambdaLibrary, _LambdaPath
from lambdapdk.ihp130 import IHP130PDK, _IHP130Path


class _IHP130_IOLibrary(LambdaLibrary, _IHP130Path):
    '''
    IHP 130 IO Cells
    '''
    def __init__(self, voltage):
        super().__init__()
        self.set_name(f"sg13g2_io_{voltage}")

        path_base = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        self.add_asic_pdk(IHP130PDK())

        with self.active_dataroot("ihp130"):
            if voltage == "1p2V":
                for corner_name, filename in [
                        ('slow', 'sg13g2_io_slow_1p08V_3p0V_125C.lib'),
                        ('typical', 'sg13g2_io_typ_1p2V_3p3V_25C.lib'),
                        ('fast', 'sg13g2_io_fast_1p32V_3p6V_m40C.lib')]:
                    with self.active_fileset(f"models.timing.{corner_name}.nldm"):
                        self.add_file(f"ihp-sg13g2/libs.ref/sg13g2_io/lib/{filename}")
                        self.add_asic_libcornerfileset(corner_name, "nldm")
            else:
                for corner_name, filename in [
                        ('slow', 'sg13g2_io_slow_1p35V_3p0V_125C.lib'),
                        ('typical', 'sg13g2_io_typ_1p5V_3p3V_25C.lib'),
                        ('fast', 'sg13g2_io_fast_1p65V_3p6V_m40C.lib')]:
                    with self.active_fileset(f"models.timing.{corner_name}.nldm"):
                        self.add_file(f"ihp-sg13g2/libs.ref/sg13g2_io/lib/{filename}")
                        self.add_asic_libcornerfileset(corner_name, "nldm")

            with self.active_fileset("models.spice"):
                self.add_file("ihp-sg13g2/libs.ref/sg13g2_io/spice/sg13g2_io.spi", filetype="spice")

        with self.active_dataroot("ihp130"):
            with self.active_fileset("models.physical"):
                self.add_file("ihp-sg13g2/libs.ref/sg13g2_io/lef/sg13g2_io.lef")
                self.add_file("ihp-sg13g2/libs.ref/sg13g2_io/gds/sg13g2_io.gds")
                self.add_asic_aprfileset()

            with self.active_fileset("models.lvs"):
                self.add_file("ihp-sg13g2/libs.ref/sg13g2_io/cdl/sg13g2_io.cdl")
                self.add_asic_aprfileset()

        self.add_asic_celllist('filler', ['sg13g2_Filler200',
                                          'sg13g2_Filler400',
                                          'sg13g2_Filler1000',
                                          'sg13g2_Filler2000',
                                          'sg13g2_Filler4000',
                                          'sg13g2_Filler10000'])

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("models.blackbox"):
                self.add_file(path_base / "blackbox" / "sg13g2_io.v")
            self.add_yosys_blackbox_fileset("models.blackbox")


class IHP130_IO_1p2(_IHP130_IOLibrary):
    def __init__(self):
        super().__init__("1p2")


class IHP130_IO_1p5(_IHP130_IOLibrary):
    def __init__(self):
        super().__init__("1p5")


class IHP130Lambdalib_la_iovdd_1p2(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovdd", [IHP130_IO_1p2])
        self.set_name("ihp130_1p2_la_iovdd")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovdd.v")


class IHP130Lambdalib_la_iocorner_1p2(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iocorner", [IHP130_IO_1p2])
        self.set_name("ihp130_1p2_la_iocorner")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iocorner.v")


class IHP130Lambdalib_la_iotxdiff_1p2(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iotxdiff", [IHP130_IO_1p2])
        self.set_name("ihp130_1p2_la_iotxdiff")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iotxdiff.v")


class IHP130Lambdalib_la_ioanalog_1p2(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_ioanalog", [IHP130_IO_1p2])
        self.set_name("ihp130_1p2_la_ioanalog")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_ioanalog.v")


class IHP130Lambdalib_la_ioinput_1p2(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_ioinput", [IHP130_IO_1p2])
        self.set_name("ihp130_1p2_la_ioinput")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_ioinput.v")


class IHP130Lambdalib_la_iovss_1p2(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovss", [IHP130_IO_1p2])
        self.set_name("ihp130_1p2_la_iovss")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovss.v")


class IHP130Lambdalib_la_iovddio_1p2(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovddio", [IHP130_IO_1p2])
        self.set_name("ihp130_1p2_la_iovddio")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovddio.v")


class IHP130Lambdalib_la_iovssio_1p2(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovssio", [IHP130_IO_1p2])
        self.set_name("ihp130_1p2_la_iovssio")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovssio.v")


class IHP130Lambdalib_la_iovdda_1p2(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovdda", [IHP130_IO_1p2])
        self.set_name("ihp130_1p2_la_iovdda")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovdda.v")


class IHP130Lambdalib_la_iovssa_1p2(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovssa", [IHP130_IO_1p2])
        self.set_name("ihp130_1p2_la_iovssa")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovssa.v")


class IHP130Lambdalib_la_iorxdiff_1p2(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iorxdiff", [IHP130_IO_1p2])
        self.set_name("ihp130_1p2_la_iorxdiff")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iorxdiff.v")


class IHP130Lambdalib_la_iobidir_1p2(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iobidir", [IHP130_IO_1p2])
        self.set_name("ihp130_1p2_la_iobidir")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iobidir.v")


class IHP130LambdaLib_IO_1p2(LambalibTechLibrary):
    @classmethod
    def alias(cls, project: ASIC):
        IHP130Lambdalib_la_iovdd_1p2.alias(project)
        IHP130Lambdalib_la_iocorner_1p2.alias(project)
        IHP130Lambdalib_la_iotxdiff_1p2.alias(project)
        IHP130Lambdalib_la_ioanalog_1p2.alias(project)
        IHP130Lambdalib_la_ioinput_1p2.alias(project)
        IHP130Lambdalib_la_iovss_1p2.alias(project)
        IHP130Lambdalib_la_iovddio_1p2.alias(project)
        IHP130Lambdalib_la_iovssio_1p2.alias(project)
        IHP130Lambdalib_la_iovdda_1p2.alias(project)
        IHP130Lambdalib_la_iovssa_1p2.alias(project)
        IHP130Lambdalib_la_iorxdiff_1p2.alias(project)
        IHP130Lambdalib_la_iobidir_1p2.alias(project)


class IHP130Lambdalib_la_iovdd_1p5(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovdd", [IHP130_IO_1p5])
        self.set_name("ihp130_1p5_la_iovdd")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovdd.v")


class IHP130Lambdalib_la_iocorner_1p5(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iocorner", [IHP130_IO_1p5])
        self.set_name("ihp130_1p5_la_iocorner")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iocorner.v")


class IHP130Lambdalib_la_iotxdiff_1p5(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iotxdiff", [IHP130_IO_1p5])
        self.set_name("ihp130_1p5_la_iotxdiff")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iotxdiff.v")


class IHP130Lambdalib_la_ioanalog_1p5(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_ioanalog", [IHP130_IO_1p5])
        self.set_name("ihp130_1p5_la_ioanalog")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_ioanalog.v")


class IHP130Lambdalib_la_ioinput_1p5(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_ioinput", [IHP130_IO_1p5])
        self.set_name("ihp130_1p5_la_ioinput")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_ioinput.v")


class IHP130Lambdalib_la_iovss_1p5(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovss", [IHP130_IO_1p5])
        self.set_name("ihp130_1p5_la_iovss")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovss.v")


class IHP130Lambdalib_la_iovddio_1p5(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovddio", [IHP130_IO_1p5])
        self.set_name("ihp130_1p5_la_iovddio")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovddio.v")


class IHP130Lambdalib_la_iovssio_1p5(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovssio", [IHP130_IO_1p5])
        self.set_name("ihp130_1p5_la_iovssio")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovssio.v")


class IHP130Lambdalib_la_iovdda_1p5(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovdda", [IHP130_IO_1p5])
        self.set_name("ihp130_1p5_la_iovdda")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovdda.v")


class IHP130Lambdalib_la_iovssa_1p5(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovssa", [IHP130_IO_1p5])
        self.set_name("ihp130_1p5_la_iovssa")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovssa.v")


class IHP130Lambdalib_la_iorxdiff_1p5(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iorxdiff", [IHP130_IO_1p5])
        self.set_name("ihp130_1p5_la_iorxdiff")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iorxdiff.v")


class IHP130Lambdalib_la_iobidir_1p5(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iobidir", [IHP130_IO_1p5])
        self.set_name("ihp130_1p5_la_iobidir")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "ihp130", "libs", "sg13g2_io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iobidir.v")


class IHP130LambdaLib_IO_1p5(LambalibTechLibrary):
    @classmethod
    def alias(cls, project: ASIC):
        IHP130Lambdalib_la_iovdd_1p5.alias(project)
        IHP130Lambdalib_la_iocorner_1p5.alias(project)
        IHP130Lambdalib_la_iotxdiff_1p5.alias(project)
        IHP130Lambdalib_la_ioanalog_1p5.alias(project)
        IHP130Lambdalib_la_ioinput_1p5.alias(project)
        IHP130Lambdalib_la_iovss_1p5.alias(project)
        IHP130Lambdalib_la_iovddio_1p5.alias(project)
        IHP130Lambdalib_la_iovssio_1p5.alias(project)
        IHP130Lambdalib_la_iovdda_1p5.alias(project)
        IHP130Lambdalib_la_iovssa_1p5.alias(project)
        IHP130Lambdalib_la_iorxdiff_1p5.alias(project)
        IHP130Lambdalib_la_iobidir_1p5.alias(project)
