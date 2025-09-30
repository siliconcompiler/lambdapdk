from pathlib import Path

from siliconcompiler import ASIC
from lambdalib import LambalibTechLibrary
from lambdapdk import LambdaLibrary, _LambdaPath
from lambdapdk.asap7 import ASAP7PDK


class FakeIO7Library(LambdaLibrary):
    '''
    ASAP7 Fake I/O library.
    '''
    def __init__(self):
        super().__init__()
        self.set_name("fakeio7")

        self.add_asic_pdk(ASAP7PDK())

        path_base = Path("lambdapdk", "asap7", "libs", "fakeio7")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("models.physical"):
                self.add_file(path_base / "lef" / "fakeio7.lef")
                self.add_asic_aprfileset()

            with self.active_fileset("models.blackbox"):
                self.add_file(path_base / "blackbox" / "model.v")
            self.add_yosys_blackbox_fileset("models.blackbox")


class FakeIO7Lambdalib_la_iovdd(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovdd", [FakeIO7Library])
        self.set_name("fakeio7_la_iovdd")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "asap7", "libs", "fakeio7")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovdd.v")


class FakeIO7Lambdalib_la_iopoc(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iopoc", [FakeIO7Library])
        self.set_name("fakeio7_la_iopoc")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "asap7", "libs", "fakeio7")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iopoc.v")


class FakeIO7Lambdalib_la_iocorner(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iocorner", [FakeIO7Library])
        self.set_name("fakeio7_la_iocorner")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "asap7", "libs", "fakeio7")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iocorner.v")


class FakeIO7Lambdalib_la_iotxdiff(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iotxdiff", [FakeIO7Library])
        self.set_name("fakeio7_la_iotxdiff")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "asap7", "libs", "fakeio7")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iotxdiff.v")


class FakeIO7Lambdalib_la_ioanalog(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_ioanalog", [FakeIO7Library])
        self.set_name("fakeio7_la_ioanalog")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "asap7", "libs", "fakeio7")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_ioanalog.v")


class FakeIO7Lambdalib_la_ioinput(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_ioinput", [FakeIO7Library])
        self.set_name("fakeio7_la_ioinput")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "asap7", "libs", "fakeio7")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_ioinput.v")


class FakeIO7Lambdalib_la_iocut(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iocut", [FakeIO7Library])
        self.set_name("fakeio7_la_iocut")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "asap7", "libs", "fakeio7")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iocut.v")


class FakeIO7Lambdalib_la_iovss(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovss", [FakeIO7Library])
        self.set_name("fakeio7_la_iovss")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "asap7", "libs", "fakeio7")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovss.v")


class FakeIO7Lambdalib_la_iovddio(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovddio", [FakeIO7Library])
        self.set_name("fakeio7_la_iovddio")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "asap7", "libs", "fakeio7")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovddio.v")


class FakeIO7Lambdalib_la_iovssio(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovssio", [FakeIO7Library])
        self.set_name("fakeio7_la_iovssio")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "asap7", "libs", "fakeio7")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovssio.v")


class FakeIO7Lambdalib_la_iovdda(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovdda", [FakeIO7Library])
        self.set_name("fakeio7_la_iovdda")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "asap7", "libs", "fakeio7")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovdda.v")


class FakeIO7Lambdalib_la_iovssa(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovssa", [FakeIO7Library])
        self.set_name("fakeio7_la_iovssa")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "asap7", "libs", "fakeio7")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovssa.v")


class FakeIO7Lambdalib_la_ioclamp(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_ioclamp", [FakeIO7Library])
        self.set_name("fakeio7_la_ioclamp")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "asap7", "libs", "fakeio7")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_ioclamp.v")


class FakeIO7Lambdalib_la_iorxdiff(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iorxdiff", [FakeIO7Library])
        self.set_name("fakeio7_la_iorxdiff")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "asap7", "libs", "fakeio7")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iorxdiff.v")


class FakeIO7Lambdalib_la_iobidir(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iobidir", [FakeIO7Library])
        self.set_name("fakeio7_la_iobidir")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "asap7", "libs", "fakeio7")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iobidir.v")


class FakeIO7Lambdalib_IO(LambalibTechLibrary):
    @classmethod
    def alias(cls, project: ASIC):
        FakeIO7Lambdalib_la_iovdd.alias(project)
        FakeIO7Lambdalib_la_iopoc.alias(project)
        FakeIO7Lambdalib_la_iocorner.alias(project)
        FakeIO7Lambdalib_la_iotxdiff.alias(project)
        FakeIO7Lambdalib_la_ioanalog.alias(project)
        FakeIO7Lambdalib_la_ioinput.alias(project)
        FakeIO7Lambdalib_la_iocut.alias(project)
        FakeIO7Lambdalib_la_iovss.alias(project)
        FakeIO7Lambdalib_la_iovddio.alias(project)
        FakeIO7Lambdalib_la_iovssio.alias(project)
        FakeIO7Lambdalib_la_iovdda.alias(project)
        FakeIO7Lambdalib_la_iovssa.alias(project)
        FakeIO7Lambdalib_la_ioclamp.alias(project)
        FakeIO7Lambdalib_la_iorxdiff.alias(project)
        FakeIO7Lambdalib_la_iobidir.alias(project)
