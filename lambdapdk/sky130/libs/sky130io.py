from pathlib import Path

from lambdapdk import LambdaLibrary
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
