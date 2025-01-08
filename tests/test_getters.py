import pytest
from siliconcompiler import Chip
import lambdapdk

from lambdapdk import asap7, freepdk45, sky130, gf180, ihp130, interposer
from lambdapdk.asap7.libs import asap7sc7p5t, fakeram7, fakeio7
from lambdapdk.freepdk45.libs import nangate45, fakeram45
from lambdapdk.sky130.libs import sky130sc, sky130io, sky130sram
from lambdapdk.gf180.libs import gf180mcu, gf180io, gf180sram
from lambdapdk.ihp130.libs import sg13g2_stdcell, sg13g2_sram
from lambdapdk.interposer.libs import bumps as interposer_bumps


all_libs = [
    asap7sc7p5t, fakeram7, fakeio7,  # asap7
    nangate45, fakeram45,  # freepdk45
    sky130sc, sky130io, sky130sram,  # sky130
    gf180mcu, gf180io, gf180sram,  # gf180
    sg13g2_stdcell, sg13g2_sram,  # ihp130
    interposer_bumps  # interposer
]


@pytest.mark.parametrize('pdk', [asap7, freepdk45, sky130, gf180, ihp130, interposer])
def test_pdk(pdk):
    chip = Chip('<pdk>')
    chip.use(pdk)
    pdks = lambdapdk.get_pdks()
    for pdk in chip.getkeys('pdk'):
        assert pdk in pdks, f'{pdk} not in getter list'


@pytest.mark.parametrize('lib', all_libs)
def test_lib(lib):
    chip = Chip('<lib>')
    chip.use(lib)
    libs = lambdapdk.get_libs()
    for lib in chip.getkeys('library'):
        assert lib in libs, f'{lib} not in getter list'


def test_get_docs_pdks():
    assert len(lambdapdk.get_pdks()) == len(lambdapdk.get_docs_pdks())


def test_get_docs_libraries():
    assert len(all_libs) == len(lambdapdk.get_docs_libraries())
