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
