import pytest
from siliconcompiler import Chip

from lambdapdk import asap7, freepdk45, sky130
from lambdapdk.asap7.libs import asap7sc7p5t, fakeram7
from lambdapdk.freepdk45.libs import nangate45, fakeram45
from lambdapdk.sky130.libs import sky130hd, sky130io, sky130sram


@pytest.mark.parametrize('pdk', [asap7, freepdk45, sky130])
def test_pdk_paths(pdk):
    chip = Chip('<pdk>')
    chip.use(pdk)
    assert chip.check_filepaths()


@pytest.mark.parametrize('lib', [
    asap7sc7p5t, fakeram7,  # asap7
    nangate45, fakeram45,  # freepdk45
    sky130hd, sky130io, sky130sram  # sky130
    ])
def test_lib_paths(lib):
    chip = Chip('<lib>')
    chip.use(lib)
    assert chip.check_filepaths()
