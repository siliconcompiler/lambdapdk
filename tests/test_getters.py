import pytest
from siliconcompiler import Chip
import lambdapdk

from lambdapdk import asap7, freepdk45, sky130, gf180
from lambdapdk.asap7.libs import asap7sc7p5t, fakeram7
from lambdapdk.freepdk45.libs import nangate45, fakeram45
from lambdapdk.sky130.libs import sky130sc, sky130io, sky130sram
from lambdapdk.gf180.libs import gf180mcu, gf180io, gf180sram


@pytest.mark.parametrize('pdk', [asap7, freepdk45, sky130, gf180])
def test_pdk(pdk):
    chip = Chip('<pdk>')
    chip.use(pdk)
    pdks = lambdapdk.get_pdks()
    for pdk in chip.getkeys('pdk'):
        assert pdk in pdks, f'{pdk} not in getter list'


@pytest.mark.parametrize('lib', [
    asap7sc7p5t, fakeram7,  # asap7
    nangate45, fakeram45,  # freepdk45
    sky130sc, sky130io, sky130sram,  # sky130
    gf180mcu, gf180io, gf180sram  # gf180
    ])
def test_lib(lib):
    chip = Chip('<lib>')
    chip.use(lib)
    libs = lambdapdk.get_libs()
    for lib in chip.getkeys('library'):
        assert lib in libs, f'{lib} not in getter list'
