from pathlib import Path

from siliconcompiler import ASIC
from lambdalib import LambalibTechLibrary
from lambdapdk import LambdaLibrary, _LambdaPath
from lambdapdk.sky130 import Sky130PDK


class Sky130_IOLibrary(LambdaLibrary):
    '''
    Skywater130 I/O library.
    '''
    def __init__(self):
        super().__init__()
        self.set_name("sky130io")

        self.add_asic_pdk(Sky130PDK())

        path_base = Path('lambdapdk', 'sky130', 'libs', "sky130io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("models.timing.nldm"):
                self.add_file(path_base / "nldm" / "sky130_dummy_io.lib")
                self.add_asic_libcornerfileset("generic", "nldm")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("models.physical"):
                self.add_file(path_base / "lef" / "sky130_ef_io.lef")
                self.add_file(path_base / "gds" / "sky130_ef_io.gds")
                self.add_file(path_base / "gds" / "sky130_fd_io.gds")
                self.add_file(path_base / "gds" / "sky130_ef_io__gpiov2_pad_wrapped.gds")
                self.add_asic_aprfileset()

            with self.active_fileset("rtl"):
                self.add_file(path_base / "verilog" / "sky130_ef_io.v")
                self.add_file(path_base / "verilog" / "sky130_fd_io.v")
                self.add_file(path_base / "verilog" / "sky130_ef_io__gpiov2_pad_wrapped.v")
                self.add_file(path_base / "verilog" / "sky130_ef_io__analog_pad.v")

                # TODO defines?

        self.add_asic_celllist('filler', ['sky130_ef_io__com_bus_slice_1um',
                                          'sky130_ef_io__com_bus_slice_5um',
                                          'sky130_ef_io__com_bus_slice_10um',
                                          'sky130_ef_io__com_bus_slice_20um'])

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("models.blackbox"):
                self.add_file(path_base / "blackbox" / "sky130_ef_io.v")
                self.add_file(path_base / "blackbox" / "sky130_fd_io.v")
            self.add_yosys_blackbox_fileset("models.blackbox")


class Sky130Lambdalib_la_ioanalog(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_ioanalog", [Sky130_IOLibrary])
        self.set_name("sky130_la_ioanalog")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "sky130", "libs", "sky130io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_ioanalog.v")


class Sky130Lambdalib_la_iobidir(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iobidir", [Sky130_IOLibrary])
        self.set_name("sky130_la_iobidir")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "sky130", "libs", "sky130io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iobidir.v")


class Sky130Lambdalib_la_ioclamp(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_ioclamp", [Sky130_IOLibrary])
        self.set_name("sky130_la_ioclamp")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "sky130", "libs", "sky130io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_ioclamp.v")


class Sky130Lambdalib_la_iocorner(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iocorner", [Sky130_IOLibrary])
        self.set_name("sky130_la_iocorner")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "sky130", "libs", "sky130io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iocorner.v")


class Sky130Lambdalib_la_ioinput(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_ioinput", [Sky130_IOLibrary])
        self.set_name("sky130_la_ioinput")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "sky130", "libs", "sky130io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_ioinput.v")


class Sky130Lambdalib_la_iorxdiff(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iorxdiff", [Sky130_IOLibrary])
        self.set_name("sky130_la_iorxdiff")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "sky130", "libs", "sky130io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iorxdiff.v")


class Sky130Lambdalib_la_iotxdiff(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iotxdiff", [Sky130_IOLibrary])
        self.set_name("sky130_la_iotxdiff")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "sky130", "libs", "sky130io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iotxdiff.v")


class Sky130Lambdalib_la_iovdd(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovdd", [Sky130_IOLibrary])
        self.set_name("sky130_la_iovdd")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "sky130", "libs", "sky130io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovdd.v")


class Sky130Lambdalib_la_iovdda(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovdda", [Sky130_IOLibrary])
        self.set_name("sky130_la_iovdda")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "sky130", "libs", "sky130io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovdda.v")


class Sky130Lambdalib_la_iovddio(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovddio", [Sky130_IOLibrary])
        self.set_name("sky130_la_iovddio")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "sky130", "libs", "sky130io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovddio.v")


class Sky130Lambdalib_la_iovss(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovss", [Sky130_IOLibrary])
        self.set_name("sky130_la_iovss")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "sky130", "libs", "sky130io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovss.v")


class Sky130Lambdalib_la_iovssa(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovssa", [Sky130_IOLibrary])
        self.set_name("sky130_la_iovssa")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "sky130", "libs", "sky130io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovssa.v")


class Sky130Lambdalib_la_iovssio(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iovssio", [Sky130_IOLibrary])
        self.set_name("sky130_la_iovssio")

        # version
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "sky130", "libs", "sky130io")

        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iovssio.v")


class Sky130LambdaLib_IO(LambalibTechLibrary):
    @classmethod
    def alias(cls, project: ASIC):
        Sky130Lambdalib_la_ioanalog.alias(project)
        Sky130Lambdalib_la_iobidir.alias(project)
        Sky130Lambdalib_la_ioclamp.alias(project)
        Sky130Lambdalib_la_iocorner.alias(project)
        Sky130Lambdalib_la_ioinput.alias(project)
        Sky130Lambdalib_la_iorxdiff.alias(project)
        Sky130Lambdalib_la_iotxdiff.alias(project)
        Sky130Lambdalib_la_iovdd.alias(project)
        Sky130Lambdalib_la_iovdda.alias(project)
        Sky130Lambdalib_la_iovddio.alias(project)
        Sky130Lambdalib_la_iovss.alias(project)
        Sky130Lambdalib_la_iovssa.alias(project)
        Sky130Lambdalib_la_iovssio.alias(project)
