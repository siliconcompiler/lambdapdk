import os.path
from siliconcompiler.schema_support.pathschema import PathSchema

from siliconcompiler.package import PythonPathResolver

from siliconcompiler.tools.klayout import KLayoutPDK
from siliconcompiler.tools.openroad import OpenROADPDK

from siliconcompiler.tools.yosys import YosysStdCellLibrary
from siliconcompiler.tools.openroad import OpenROADStdCellLibrary
from siliconcompiler.tools.bambu import BambuStdCellLibrary
from siliconcompiler.tools.klayout import KLayoutLibrary

__version__ = "0.2.0-rc7"


class _LambdaPath(PathSchema):
    def __init__(self):
        super().__init__()
        PythonPathResolver.set_dataroot(
            self,
            "lambdapdk",
            "lambdapdk",
            "https://github.com/siliconcompiler/lambdapdk/archive/refs/tags/",
            alternative_ref=f"v{__version__}",
            python_module_path_append="..")


class LambdaPDK(KLayoutPDK, OpenROADPDK, _LambdaPath):
    def __init__(self):
        super().__init__()


class LambdaLibrary(YosysStdCellLibrary,
                    OpenROADStdCellLibrary,
                    KLayoutLibrary,
                    BambuStdCellLibrary,
                    _LambdaPath):
    def __init__(self):
        super().__init__()


def get_pdks():
    '''
    Returns a list of pdks in lambdapdk
    '''

    from lambdapdk.asap7 import ASAP7PDK
    from lambdapdk.freepdk45 import FreePDK45PDK
    from lambdapdk.sky130 import Sky130PDK
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
    from lambdapdk.ihp130 import IHP130PDK
    from lambdapdk.interposer import Interposer_3ML_0400, \
        Interposer_3ML_0800, \
        Interposer_3ML_2000, \
        Interposer_3ML_0400_2000, \
        Interposer_4ML_0400, \
        Interposer_4ML_0800, \
        Interposer_4ML_2000, \
        Interposer_4ML_0400_2000, \
        Interposer_5ML_0400, \
        Interposer_5ML_0800, \
        Interposer_5ML_2000, \
        Interposer_5ML_0400_2000

    return set([
        ASAP7PDK(),
        FreePDK45PDK(),
        Sky130PDK(),
        IHP130PDK(),
        GF180_3LM_1TM_6K_7t(),
        GF180_3LM_1TM_6K_9t(),
        GF180_3LM_1TM_9K_7t(),
        GF180_3LM_1TM_9K_9t(),
        GF180_3LM_1TM_11K_7t(),
        GF180_3LM_1TM_11K_9t(),
        GF180_3LM_1TM_30K_7t(),
        GF180_3LM_1TM_30K_9t(),
        GF180_4LM_1TM_6K_7t(),
        GF180_4LM_1TM_6K_9t(),
        GF180_4LM_1TM_9K_7t(),
        GF180_4LM_1TM_9K_9t(),
        GF180_4LM_1TM_11K_7t(),
        GF180_4LM_1TM_11K_9t(),
        GF180_4LM_1TM_30K_7t(),
        GF180_4LM_1TM_30K_9t(),
        GF180_5LM_1TM_9K_7t(),
        GF180_5LM_1TM_9K_9t(),
        GF180_5LM_1TM_11K_7t(),
        GF180_5LM_1TM_11K_9t(),
        GF180_6LM_1TM_9K_7t(),
        GF180_6LM_1TM_9K_9t(),
        Interposer_3ML_0400(),
        Interposer_3ML_0800(),
        Interposer_3ML_2000(),
        Interposer_3ML_0400_2000(),
        Interposer_4ML_0400(),
        Interposer_4ML_0800(),
        Interposer_4ML_2000(),
        Interposer_4ML_0400_2000(),
        Interposer_5ML_0400(),
        Interposer_5ML_0800(),
        Interposer_5ML_2000(),
        Interposer_5ML_0400_2000()
    ])


def get_pdk_names():
    '''
    Returns a list of pdks in lambdapdk
    '''

    return set([pdk.name for pdk in get_pdks()])


def get_libs():
    '''
    Returns a list of libraries in lambdapdk
    '''

    from lambdapdk.asap7.libs.asap7sc7p5t import ASAP7SC7p5RVT, ASAP7SC7p5SLVT, ASAP7SC7p5LVT
    from lambdapdk.asap7.libs.fakeio7 import FakeIO7Library, \
        FakeIO7Lambdalib_la_iovdd, \
        FakeIO7Lambdalib_la_iopoc, \
        FakeIO7Lambdalib_la_iocorner, \
        FakeIO7Lambdalib_la_iotxdiff, \
        FakeIO7Lambdalib_la_ioanalog, \
        FakeIO7Lambdalib_la_ioinput, \
        FakeIO7Lambdalib_la_iocut, \
        FakeIO7Lambdalib_la_iovss, \
        FakeIO7Lambdalib_la_iovddio, \
        FakeIO7Lambdalib_la_iovssio, \
        FakeIO7Lambdalib_la_iovdda, \
        FakeIO7Lambdalib_la_iovssa, \
        FakeIO7Lambdalib_la_ioclamp, \
        FakeIO7Lambdalib_la_iorxdiff, \
        FakeIO7Lambdalib_la_iobidir
    from lambdapdk.asap7.libs.fakekit7 import FakeKit7Library
    from lambdapdk.asap7.libs.fakeram7 import \
        FakeRAM7_dp_64x32, \
        FakeRAM7_sp_64x32, \
        FakeRAM7_dp_128x32, \
        FakeRAM7_sp_128x32, \
        FakeRAM7_dp_256x32, \
        FakeRAM7_sp_256x32, \
        FakeRAM7_dp_256x64, \
        FakeRAM7_sp_256x64, \
        FakeRAM7_dp_512x32, \
        FakeRAM7_sp_512x32, \
        FakeRAM7_dp_512x64, \
        FakeRAM7_sp_512x64, \
        FakeRAM7_dp_512x128, \
        FakeRAM7_sp_512x128, \
        FakeRAM7_dp_1024x32, \
        FakeRAM7_sp_1024x32, \
        FakeRAM7_dp_1024x64, \
        FakeRAM7_sp_1024x64, \
        FakeRAM7_dp_2048x32, \
        FakeRAM7_sp_2048x32, \
        FakeRAM7_dp_2048x64, \
        FakeRAM7_sp_2048x64, \
        FakeRAM7_dp_4096x32, \
        FakeRAM7_sp_4096x32, \
        FakeRAM7_dp_4096x64, \
        FakeRAM7_sp_4096x64, \
        FakeRAM7_dp_8192x32, \
        FakeRAM7_sp_8192x32, \
        FakeRAM7_dp_8192x64, \
        FakeRAM7_sp_8192x64, \
        FakeRAM7Lambdalib_SinglePort, \
        FakeRAM7Lambdalib_DoublePort
    from lambdapdk.freepdk45.libs.nangate45 import Nangate45
    from lambdapdk.freepdk45.libs.fakeram45 import \
        FakeRAM45_64x32, \
        FakeRAM45_128x32, \
        FakeRAM45_256x32, \
        FakeRAM45_256x64, \
        FakeRAM45_512x32, \
        FakeRAM45_512x64, \
        FakeRAM45Lambdalib_SinglePort
    from lambdapdk.gf180.libs.gf180io import GF180_IO_3LM, GF180_IO_4LM, GF180_IO_5LM, \
        GF180Lambdalib_la_iovdd_3LM, \
        GF180Lambdalib_la_iocorner_3LM, \
        GF180Lambdalib_la_iotxdiff_3LM, \
        GF180Lambdalib_la_ioanalog_3LM, \
        GF180Lambdalib_la_ioinput_3LM, \
        GF180Lambdalib_la_iocut_3LM, \
        GF180Lambdalib_la_iovss_3LM, \
        GF180Lambdalib_la_iovddio_3LM, \
        GF180Lambdalib_la_iovssio_3LM, \
        GF180Lambdalib_la_iovdda_3LM, \
        GF180Lambdalib_la_iovssa_3LM, \
        GF180Lambdalib_la_iorxdiff_3LM, \
        GF180Lambdalib_la_iobidir_3LM, \
        GF180Lambdalib_la_iovdd_4LM, \
        GF180Lambdalib_la_iocorner_4LM, \
        GF180Lambdalib_la_iotxdiff_4LM, \
        GF180Lambdalib_la_ioanalog_4LM, \
        GF180Lambdalib_la_ioinput_4LM, \
        GF180Lambdalib_la_iocut_4LM, \
        GF180Lambdalib_la_iovss_4LM, \
        GF180Lambdalib_la_iovddio_4LM, \
        GF180Lambdalib_la_iovssio_4LM, \
        GF180Lambdalib_la_iovdda_4LM, \
        GF180Lambdalib_la_iovssa_4LM, \
        GF180Lambdalib_la_iorxdiff_4LM, \
        GF180Lambdalib_la_iobidir_4LM, \
        GF180Lambdalib_la_iovdd_5LM, \
        GF180Lambdalib_la_iocorner_5LM, \
        GF180Lambdalib_la_iotxdiff_5LM, \
        GF180Lambdalib_la_ioanalog_5LM, \
        GF180Lambdalib_la_ioinput_5LM, \
        GF180Lambdalib_la_iocut_5LM, \
        GF180Lambdalib_la_iovss_5LM, \
        GF180Lambdalib_la_iovddio_5LM, \
        GF180Lambdalib_la_iovssio_5LM, \
        GF180Lambdalib_la_iovdda_5LM, \
        GF180Lambdalib_la_iovssa_5LM, \
        GF180Lambdalib_la_iorxdiff_5LM, \
        GF180Lambdalib_la_iobidir_5LM
    from lambdapdk.gf180.libs.gf180mcu import GF180_MCU_7T_3LMLibrary, \
        GF180_MCU_7T_4LMLibrary, \
        GF180_MCU_7T_5LMLibrary, \
        GF180_MCU_7T_6LMLibrary, \
        GF180_MCU_9T_3LMLibrary, \
        GF180_MCU_9T_4LMLibrary, \
        GF180_MCU_9T_5LMLibrary, \
        GF180_MCU_9T_6LMLibrary
    from lambdapdk.gf180.libs.gf180sram import GF180_SRAM_64x8, \
        GF180_SRAM_128x8, \
        GF180_SRAM_256x8, \
        GF180_SRAM_512x8, \
        GF180Lambdalib_SinglePort
    from lambdapdk.ihp130.libs.sg13g2_io import IHP130_IO_1p2, IHP130_IO_1p5, \
        IHP130Lambdalib_la_iovdd_1p2, \
        IHP130Lambdalib_la_iocorner_1p2, \
        IHP130Lambdalib_la_iotxdiff_1p2, \
        IHP130Lambdalib_la_ioanalog_1p2, \
        IHP130Lambdalib_la_ioinput_1p2, \
        IHP130Lambdalib_la_iovss_1p2, \
        IHP130Lambdalib_la_iovddio_1p2, \
        IHP130Lambdalib_la_iovssio_1p2, \
        IHP130Lambdalib_la_iovdda_1p2, \
        IHP130Lambdalib_la_iovssa_1p2, \
        IHP130Lambdalib_la_iorxdiff_1p2, \
        IHP130Lambdalib_la_iobidir_1p2, \
        IHP130Lambdalib_la_iovdd_1p5, \
        IHP130Lambdalib_la_iocorner_1p5, \
        IHP130Lambdalib_la_iotxdiff_1p5, \
        IHP130Lambdalib_la_ioanalog_1p5, \
        IHP130Lambdalib_la_ioinput_1p5, \
        IHP130Lambdalib_la_iovss_1p5, \
        IHP130Lambdalib_la_iovddio_1p5, \
        IHP130Lambdalib_la_iovssio_1p5, \
        IHP130Lambdalib_la_iovdda_1p5, \
        IHP130Lambdalib_la_iovssa_1p5, \
        IHP130Lambdalib_la_iorxdiff_1p5, \
        IHP130Lambdalib_la_iobidir_1p5
    from lambdapdk.ihp130.libs.sg13g2_sram import \
        IHP130_SRAM_1024x64, IHP130_SRAM_2048x64, \
        IHP130_SRAM_256x48, IHP130_SRAM_256x64, \
        IHP130_SRAM_512x64, IHP130_SRAM_64x64, \
        IHP130Lambdalib_SinglePort
    from lambdapdk.ihp130.libs.sg13g2_stdcell import IHP130StdCell_1p2, IHP130StdCell_1p5
    from lambdapdk.interposer.libs.bumps import BumpLibrary
    from lambdapdk.sky130.libs.sky130io import Sky130_IOLibrary, \
        Sky130Lambdalib_la_ioanalog, \
        Sky130Lambdalib_la_iobidir, \
        Sky130Lambdalib_la_ioclamp, \
        Sky130Lambdalib_la_iocorner, \
        Sky130Lambdalib_la_ioinput, \
        Sky130Lambdalib_la_iorxdiff, \
        Sky130Lambdalib_la_iotxdiff, \
        Sky130Lambdalib_la_iovdd, \
        Sky130Lambdalib_la_iovdda, \
        Sky130Lambdalib_la_iovddio, \
        Sky130Lambdalib_la_iovss, \
        Sky130Lambdalib_la_iovssa, \
        Sky130Lambdalib_la_iovssio
    from lambdapdk.sky130.libs.sky130sc import Sky130_SCHDLibrary, Sky130_SCHDLLLibrary
    from lambdapdk.sky130.libs.sky130sram import Sky130_SRAM_64x256, Sky130Lambdalib_SinglePort

    return set([
        ASAP7SC7p5RVT(), ASAP7SC7p5SLVT(), ASAP7SC7p5LVT(),
        FakeIO7Library(), FakeKit7Library(),
        FakeRAM7_dp_64x32(),
        FakeRAM7_sp_64x32(),
        FakeRAM7_dp_128x32(),
        FakeRAM7_sp_128x32(),
        FakeRAM7_dp_256x32(),
        FakeRAM7_sp_256x32(),
        FakeRAM7_dp_256x64(),
        FakeRAM7_sp_256x64(),
        FakeRAM7_dp_512x32(),
        FakeRAM7_sp_512x32(),
        FakeRAM7_dp_512x64(),
        FakeRAM7_sp_512x64(),
        FakeRAM7_dp_512x128(),
        FakeRAM7_sp_512x128(),
        FakeRAM7_dp_1024x32(),
        FakeRAM7_sp_1024x32(),
        FakeRAM7_dp_1024x64(),
        FakeRAM7_sp_1024x64(),
        FakeRAM7_dp_2048x32(),
        FakeRAM7_sp_2048x32(),
        FakeRAM7_dp_2048x64(),
        FakeRAM7_sp_2048x64(),
        FakeRAM7_dp_4096x32(),
        FakeRAM7_sp_4096x32(),
        FakeRAM7_dp_4096x64(),
        FakeRAM7_sp_4096x64(),
        FakeRAM7_dp_8192x32(),
        FakeRAM7_sp_8192x32(),
        FakeRAM7_dp_8192x64(),
        FakeRAM7_sp_8192x64(),
        FakeRAM7Lambdalib_SinglePort(),
        FakeRAM7Lambdalib_DoublePort(),
        Nangate45(),
        FakeRAM45_64x32(),
        FakeRAM45_128x32(),
        FakeRAM45_256x32(),
        FakeRAM45_256x64(),
        FakeRAM45_512x32(),
        FakeRAM45_512x64(),
        FakeRAM45Lambdalib_SinglePort(),
        GF180_IO_3LM(), GF180_IO_4LM(), GF180_IO_5LM(),
        GF180_MCU_7T_3LMLibrary(),
        GF180_MCU_7T_4LMLibrary(),
        GF180_MCU_7T_5LMLibrary(),
        GF180_MCU_7T_6LMLibrary(),
        GF180_MCU_9T_3LMLibrary(),
        GF180_MCU_9T_4LMLibrary(),
        GF180_MCU_9T_5LMLibrary(),
        GF180_MCU_9T_6LMLibrary(),
        GF180_SRAM_64x8(),
        GF180_SRAM_128x8(),
        GF180_SRAM_256x8(),
        GF180_SRAM_512x8(),
        GF180Lambdalib_SinglePort(),
        IHP130_IO_1p2(), IHP130_IO_1p5(),
        IHP130_SRAM_1024x64(), IHP130_SRAM_2048x64(),
        IHP130_SRAM_256x48(), IHP130_SRAM_256x64(),
        IHP130_SRAM_512x64(), IHP130_SRAM_64x64(),
        IHP130Lambdalib_SinglePort(),
        IHP130StdCell_1p2(), IHP130StdCell_1p5(),
        BumpLibrary(),
        Sky130_IOLibrary(),
        Sky130_SCHDLibrary(), Sky130_SCHDLLLibrary(),
        Sky130_SRAM_64x256(), Sky130Lambdalib_SinglePort(),
        Sky130Lambdalib_la_ioanalog(),
        Sky130Lambdalib_la_iobidir(),
        Sky130Lambdalib_la_ioclamp(),
        Sky130Lambdalib_la_iocorner(),
        Sky130Lambdalib_la_ioinput(),
        Sky130Lambdalib_la_iorxdiff(),
        Sky130Lambdalib_la_iotxdiff(),
        Sky130Lambdalib_la_iovdd(),
        Sky130Lambdalib_la_iovdda(),
        Sky130Lambdalib_la_iovddio(),
        Sky130Lambdalib_la_iovss(),
        Sky130Lambdalib_la_iovssa(),
        Sky130Lambdalib_la_iovssio(),
        IHP130Lambdalib_la_iovdd_1p2(),
        IHP130Lambdalib_la_iocorner_1p2(),
        IHP130Lambdalib_la_iotxdiff_1p2(),
        IHP130Lambdalib_la_ioanalog_1p2(),
        IHP130Lambdalib_la_ioinput_1p2(),
        IHP130Lambdalib_la_iovss_1p2(),
        IHP130Lambdalib_la_iovddio_1p2(),
        IHP130Lambdalib_la_iovssio_1p2(),
        IHP130Lambdalib_la_iovdda_1p2(),
        IHP130Lambdalib_la_iovssa_1p2(),
        IHP130Lambdalib_la_iorxdiff_1p2(),
        IHP130Lambdalib_la_iobidir_1p2(),
        IHP130Lambdalib_la_iovdd_1p5(),
        IHP130Lambdalib_la_iocorner_1p5(),
        IHP130Lambdalib_la_iotxdiff_1p5(),
        IHP130Lambdalib_la_ioanalog_1p5(),
        IHP130Lambdalib_la_ioinput_1p5(),
        IHP130Lambdalib_la_iovss_1p5(),
        IHP130Lambdalib_la_iovddio_1p5(),
        IHP130Lambdalib_la_iovssio_1p5(),
        IHP130Lambdalib_la_iovdda_1p5(),
        IHP130Lambdalib_la_iovssa_1p5(),
        IHP130Lambdalib_la_iorxdiff_1p5(),
        IHP130Lambdalib_la_iobidir_1p5(),
        GF180Lambdalib_la_iovdd_3LM(),
        GF180Lambdalib_la_iocorner_3LM(),
        GF180Lambdalib_la_iotxdiff_3LM(),
        GF180Lambdalib_la_ioanalog_3LM(),
        GF180Lambdalib_la_ioinput_3LM(),
        GF180Lambdalib_la_iocut_3LM(),
        GF180Lambdalib_la_iovss_3LM(),
        GF180Lambdalib_la_iovddio_3LM(),
        GF180Lambdalib_la_iovssio_3LM(),
        GF180Lambdalib_la_iovdda_3LM(),
        GF180Lambdalib_la_iovssa_3LM(),
        GF180Lambdalib_la_iorxdiff_3LM(),
        GF180Lambdalib_la_iobidir_3LM(),
        GF180Lambdalib_la_iovdd_4LM(),
        GF180Lambdalib_la_iocorner_4LM(),
        GF180Lambdalib_la_iotxdiff_4LM(),
        GF180Lambdalib_la_ioanalog_4LM(),
        GF180Lambdalib_la_ioinput_4LM(),
        GF180Lambdalib_la_iocut_4LM(),
        GF180Lambdalib_la_iovss_4LM(),
        GF180Lambdalib_la_iovddio_4LM(),
        GF180Lambdalib_la_iovssio_4LM(),
        GF180Lambdalib_la_iovdda_4LM(),
        GF180Lambdalib_la_iovssa_4LM(),
        GF180Lambdalib_la_iorxdiff_4LM(),
        GF180Lambdalib_la_iobidir_4LM(),
        GF180Lambdalib_la_iovdd_5LM(),
        GF180Lambdalib_la_iocorner_5LM(),
        GF180Lambdalib_la_iotxdiff_5LM(),
        GF180Lambdalib_la_ioanalog_5LM(),
        GF180Lambdalib_la_ioinput_5LM(),
        GF180Lambdalib_la_iocut_5LM(),
        GF180Lambdalib_la_iovss_5LM(),
        GF180Lambdalib_la_iovddio_5LM(),
        GF180Lambdalib_la_iovssio_5LM(),
        GF180Lambdalib_la_iovdda_5LM(),
        GF180Lambdalib_la_iovssa_5LM(),
        GF180Lambdalib_la_iorxdiff_5LM(),
        GF180Lambdalib_la_iobidir_5LM(),
        FakeIO7Lambdalib_la_iovdd(),
        FakeIO7Lambdalib_la_iopoc(),
        FakeIO7Lambdalib_la_iocorner(),
        FakeIO7Lambdalib_la_iotxdiff(),
        FakeIO7Lambdalib_la_ioanalog(),
        FakeIO7Lambdalib_la_ioinput(),
        FakeIO7Lambdalib_la_iocut(),
        FakeIO7Lambdalib_la_iovss(),
        FakeIO7Lambdalib_la_iovddio(),
        FakeIO7Lambdalib_la_iovssio(),
        FakeIO7Lambdalib_la_iovdda(),
        FakeIO7Lambdalib_la_iovssa(),
        FakeIO7Lambdalib_la_ioclamp(),
        FakeIO7Lambdalib_la_iorxdiff(),
        FakeIO7Lambdalib_la_iobidir()
    ])


def get_lib_names():
    '''
    Returns a list of libraries names in lambdapdk
    '''

    return set([lib.name for lib in get_libs()])


def get_docs_codeurl(file=None):
    base_url = f"https://github.com/siliconcompiler/lambdapdk/blob/v{__version__}"

    if not file:
        return base_url

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def relpath(file):
        file = os.path.abspath(file)
        if file.startswith(root):
            return os.path.relpath(file, root)
        return None

    if os.path.isabs(file):
        file = relpath(file)
        if not file:
            return None

    return f"{base_url}/{file}"
