import pytest
from siliconcompiler import Chip
import os

from lambdapdk import asap7, freepdk45, sky130, gf180, ihp130, interposer
from lambdapdk.asap7.libs import asap7sc7p5t, fakeram7, fakeio7, fakekit7
from lambdapdk.freepdk45.libs import nangate45, fakeram45
from lambdapdk.sky130.libs import sky130sc, sky130io, sky130sram
from lambdapdk.gf180.libs import gf180mcu, gf180io, gf180sram
from lambdapdk.ihp130.libs import sg13g2_stdcell, sg13g2_sram, sg13g2_io
from lambdapdk.interposer.libs import bumps as interposer_bumps

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

from lambdapdk.asap7.libs.asap7sc7p5t import ASAP7SC7p5RVT, ASAP7SC7p5SLVT, ASAP7SC7p5LVT
from lambdapdk.asap7.libs.fakeio7 import FakeIO7Library
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
    FakeRAM7_sp_8192x64
from lambdapdk.freepdk45.libs.nangate45 import Nangate45
from lambdapdk.freepdk45.libs.fakeram45 import \
    FakeRAM45_64x32, \
    FakeRAM45_128x32, \
    FakeRAM45_256x32, \
    FakeRAM45_256x64, \
    FakeRAM45_512x32, \
    FakeRAM45_512x64
from lambdapdk.gf180.libs.gf180io import GF180_IO_3LM, GF180_IO_4LM, GF180_IO_5LM
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
    GF180_SRAM_512x8
from lambdapdk.ihp130.libs.sg13g2_io import IHP130_IO_1p2, IHP130_IO_1p5
from lambdapdk.ihp130.libs.sg13g2_sram import \
    IHP130_SRAM_1024x64, IHP130_SRAM_2048x64, \
    IHP130_SRAM_256x48, IHP130_SRAM_256x64, \
    IHP130_SRAM_512x64, IHP130_SRAM_64x64
from lambdapdk.ihp130.libs.sg13g2_stdcell import IHP130StdCell_1p2, IHP130StdCell_1p5
from lambdapdk.interposer.libs.bumps import BumpLibrary
from lambdapdk.sky130.libs.sky130io import Sky130_IOLibrary
from lambdapdk.sky130.libs.sky130sc import Sky130_SCHDLibrary, Sky130_SCHDLLLibrary
from lambdapdk.sky130.libs.sky130sram import Sky130_SRAM_64x256


@pytest.mark.parametrize('pdk', [
    asap7, freepdk45, sky130, gf180, ihp130,
    interposer])
def test_pdk_paths(pdk):
    chip = Chip('<pdk>')
    chip.use(pdk)
    assert chip.check_filepaths()


@pytest.mark.parametrize('lib', [
    asap7sc7p5t, fakeram7, fakeio7, fakekit7,  # asap7
    nangate45, fakeram45,  # freepdk45
    sky130sc, sky130io, sky130sram,  # sky130
    gf180mcu, gf180io, gf180sram,  # gf180
    sg13g2_stdcell, sg13g2_sram, sg13g2_io,  # ihp130
    interposer_bumps
    ])
def test_lib_paths(lib):
    chip = Chip('<lib>')
    chip.use(lib)
    assert chip.check_filepaths()


def test_symbolic_links():
    def check(path):
        if os.path.basename(path).startswith('.'):
            return

        assert not os.path.islink(path)

    skip = []

    lambda_root = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    for root, dirs, files in os.walk(lambda_root):
        if os.path.basename(root).startswith('.'):
            skip.append(root)
            continue

        if any([root.startswith(d) for d in skip]):
            continue

        for d in dirs:
            check(os.path.join(root, d))
        for f in files:
            check(os.path.join(root, f))


@pytest.mark.parametrize("pdk", [
    ASAP7PDK,
    FreePDK45PDK,
    Sky130PDK,
    IHP130PDK,
    GF180_3LM_1TM_6K_7t,
    GF180_3LM_1TM_6K_9t,
    GF180_3LM_1TM_9K_7t,
    GF180_3LM_1TM_9K_9t,
    GF180_3LM_1TM_11K_7t,
    GF180_3LM_1TM_11K_9t,
    GF180_3LM_1TM_30K_7t,
    GF180_3LM_1TM_30K_9t,
    GF180_4LM_1TM_6K_7t,
    GF180_4LM_1TM_6K_9t,
    GF180_4LM_1TM_9K_7t,
    GF180_4LM_1TM_9K_9t,
    GF180_4LM_1TM_11K_7t,
    GF180_4LM_1TM_11K_9t,
    GF180_4LM_1TM_30K_7t,
    GF180_4LM_1TM_30K_9t,
    GF180_5LM_1TM_9K_7t,
    GF180_5LM_1TM_9K_9t,
    GF180_5LM_1TM_11K_7t,
    GF180_5LM_1TM_11K_9t,
    GF180_6LM_1TM_9K_7t,
    GF180_6LM_1TM_9K_9t,
    Interposer_3ML_0400,
    Interposer_3ML_0800,
    Interposer_3ML_2000,
    Interposer_3ML_0400_2000,
    Interposer_4ML_0400,
    Interposer_4ML_0800,
    Interposer_4ML_2000,
    Interposer_4ML_0400_2000,
    Interposer_5ML_0400,
    Interposer_5ML_0800,
    Interposer_5ML_2000,
    Interposer_5ML_0400_2000])
def test_new_pdks(pdk):
    assert pdk().check_filepaths()


@pytest.mark.parametrize("lib", [
    ASAP7SC7p5RVT, ASAP7SC7p5SLVT, ASAP7SC7p5LVT,
    FakeIO7Library, FakeKit7Library,
    FakeRAM7_dp_64x32,
    FakeRAM7_sp_64x32,
    FakeRAM7_dp_128x32,
    FakeRAM7_sp_128x32,
    FakeRAM7_dp_256x32,
    FakeRAM7_sp_256x32,
    FakeRAM7_dp_256x64,
    FakeRAM7_sp_256x64,
    FakeRAM7_dp_512x32,
    FakeRAM7_sp_512x32,
    FakeRAM7_dp_512x64,
    FakeRAM7_sp_512x64,
    FakeRAM7_dp_512x128,
    FakeRAM7_sp_512x128,
    FakeRAM7_dp_1024x32,
    FakeRAM7_sp_1024x32,
    FakeRAM7_dp_1024x64,
    FakeRAM7_sp_1024x64,
    FakeRAM7_dp_2048x32,
    FakeRAM7_sp_2048x32,
    FakeRAM7_dp_2048x64,
    FakeRAM7_sp_2048x64,
    FakeRAM7_dp_4096x32,
    FakeRAM7_sp_4096x32,
    FakeRAM7_dp_4096x64,
    FakeRAM7_sp_4096x64,
    FakeRAM7_dp_8192x32,
    FakeRAM7_sp_8192x32,
    FakeRAM7_dp_8192x64,
    FakeRAM7_sp_8192x64,
    Nangate45,
    FakeRAM45_64x32,
    FakeRAM45_128x32,
    FakeRAM45_256x32,
    FakeRAM45_256x64,
    FakeRAM45_512x32,
    FakeRAM45_512x64,
    GF180_IO_3LM, GF180_IO_4LM, GF180_IO_5LM,
    GF180_MCU_7T_3LMLibrary,
    GF180_MCU_7T_4LMLibrary,
    GF180_MCU_7T_5LMLibrary,
    GF180_MCU_7T_6LMLibrary,
    GF180_MCU_9T_3LMLibrary,
    GF180_MCU_9T_4LMLibrary,
    GF180_MCU_9T_5LMLibrary,
    GF180_MCU_9T_6LMLibrary,
    GF180_SRAM_64x8,
    GF180_SRAM_128x8,
    GF180_SRAM_256x8,
    GF180_SRAM_512x8,
    IHP130_IO_1p2, IHP130_IO_1p5,
    IHP130_SRAM_1024x64, IHP130_SRAM_2048x64,
    IHP130_SRAM_256x48, IHP130_SRAM_256x64,
    IHP130_SRAM_512x64, IHP130_SRAM_64x64,
    IHP130StdCell_1p2, IHP130StdCell_1p5,
    BumpLibrary,
    Sky130_IOLibrary,
    Sky130_SCHDLibrary, Sky130_SCHDLLLibrary,
    Sky130_SRAM_64x256])
def test_new_libs(lib):
    assert lib().check_filepaths()
