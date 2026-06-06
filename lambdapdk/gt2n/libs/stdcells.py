from pathlib import Path

from lambdapdk import LambdaLibrary
from lambdapdk.gt2n import GT2NPDK, _GT2NPath


class _GT2NBase(LambdaLibrary, _GT2NPath):
    '''
    GT2N 6-track standard cell library.
    '''
    def __init__(self, vt, width):
        super().__init__()
        self.set_name(f"gt2n_stdcells_w{width}_{vt}")

        # version
        self.package.set_version("r0")

        # PDK
        self.add_asic_pdk(GT2NPDK())

        # site name
        self.add_asic_site('gt2_6t')

        # tie cells
        self.add_asic_celllist('tie', [f"gt2_6t_tiehigh_w{width}_{vt}",
                                       f"gt2_6t_tielow_w{width}_{vt}"])

        # filler
        self.add_asic_celllist('filler', [f"gt2_6t_filler_w{width}_{vt}"])

        # Tapcell
        self.add_asic_celllist('tap', f"gt2_6t_tapbspdn_w{width}_{vt}")

        # Cells with actual view
        self.add_asic_celllist('physicalonly', [f"gt2_6t_tapbspdn_w{width}_{vt}"])

        lib_path_common = Path("lambdapdk", "gt2n", "libs", "gt2_6t")
        lib_path = Path("lambdapdk", "gt2n", "libs", f"gt2_6t_w{width}_{vt}")

        # General filelists
        with self.active_dataroot("gt2n"):
            corner_name, lib_corner = 'typical', 'tt'

            with self.active_fileset(f"models.timing.{corner_name}.nldm"):
                self.add_file(f"lib/{lib_corner}/gt2_6t_w{width}_{vt}_{lib_corner}_0p7v25c.lib")
                self.add_asic_libcornerfileset(corner_name, "nldm")

            with self.active_fileset("models.spice.tt"):
                self.add_file(f"device/tt/gt2_w{width}_{vt}_tt.sp")

            with self.active_fileset("models.physical"):
                self.add_file(f"lef/tt/gt2_6t_w{width}_{vt}.lef")
                self.add_file(f"gds/gt2_6t_std_cells_w{width}_{vt}.gds")
                self.add_asic_aprfileset()

            with self.active_fileset("models.lvs"):
                self.add_file(f"cdl/gt2_6t_w{width}_{vt}.cdl")
                self.add_asic_aprfileset()

        # Setup for yosys
        with self.active_dataroot("lambdapdk"):
            self.set_yosys_driver_cell(f"gt2_6t_buf_x1_w{width}_{vt}")
            self.set_yosys_buffer_cell(f"gt2_6t_buf_x1_w{width}_{vt}", "A", "Y")
            self.set_yosys_tielow_cell(f"gt2_6t_tielow_w{width}_{vt}", "Y")
            self.set_yosys_tiehigh_cell(f"gt2_6t_tiehigh_w{width}_{vt}", "Y")

            cap_table = {  # gt2_6t_buf_x1_w31_, pF
                'elvt': 0.0004979,
                'ulvt': 0.0004924,
                'lvt': 0.000488,
                'svt': 0.0004724,
                'hvt': 0.0004555
            }
            self.set_yosys_abc(1, cap_table[vt] * 1000 * 4)

        # Setup for openroad
        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("openroad.powergrid"):
                self.add_file(lib_path_common / "apr" / "openroad" / "pdngen.tcl")
                self.add_openroad_powergridfileset()
            with self.active_fileset("openroad.globalconnect"):
                self.add_file(lib_path_common / "apr" / "openroad" / "global_connect.tcl")
                self.add_openroad_globalconnectfileset()

            self.set_openroad_placement_density(0.40)
            self.set_openroad_tielow_cell(f"gt2_6t_tielow_w{width}_{vt}", "Y")
            self.set_openroad_tiehigh_cell(f"gt2_6t_tiehigh_w{width}_{vt}", "Y")
            self.set_openroad_macro_placement_halo(1, 1)
            self.set_openroad_tapcells_file(lib_path / "apr" / "openroad" / "tapcells.tcl")

        self.add_klayout_allowmissingcell(f"gt2_6t_tapbspdn_w{width}_{vt}")


class GT2N6TW13HVT(_GT2NBase):
    def __init__(self):
        super().__init__("hvt", 13)


class GT2N6TW13SVT(_GT2NBase):
    def __init__(self):
        super().__init__("svt", 13)


class GT2N6TW13LVT(_GT2NBase):
    def __init__(self):
        super().__init__("lvt", 13)


class GT2N6TW13ULVT(_GT2NBase):
    def __init__(self):
        super().__init__("ulvt", 13)


class GT2N6TW13ELVT(_GT2NBase):
    def __init__(self):
        super().__init__("elvt", 13)


class GT2N6TW31HVT(_GT2NBase):
    def __init__(self):
        super().__init__("hvt", 31)


class GT2N6TW31SVT(_GT2NBase):
    def __init__(self):
        super().__init__("svt", 31)


class GT2N6TW31LVT(_GT2NBase):
    def __init__(self):
        super().__init__("lvt", 31)


class GT2N6TW31ULVT(_GT2NBase):
    def __init__(self):
        super().__init__("ulvt", 31)


class GT2N6TW31ELVT(_GT2NBase):
    def __init__(self):
        super().__init__("elvt", 31)
