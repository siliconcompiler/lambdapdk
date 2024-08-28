import pytest
from siliconcompiler import Chip
import lambdalib

from lambdapdk.asap7.libs import asap7sc7p5t, fakeram7
from lambdapdk.freepdk45.libs import nangate45, fakeram45
from lambdapdk.gf180.libs import gf180mcu, gf180io, gf180sram
from lambdapdk.sky130.libs import sky130sc, sky130io, sky130sram


@pytest.mark.parametrize('module,path', [
    (asap7sc7p5t, 'lambdapdk/asap7/libs/{lib_name}/lambda/auxlib'),
    (nangate45, 'lambdapdk/freepdk45/libs/{lib_name}/lambda/auxlib'),
    (sky130sc, 'lambdapdk/sky130/libs/{lib_name}/lambda/auxlib'),
    (gf180mcu, 'lambdapdk/gf180/libs/{lib_name}/lambda/auxlib')
    ])
def test_la_auxlib(module, path):
    libs = module.setup()
    if not isinstance(libs, list):
        libs = [libs]
    for lib in libs:
        lib_name = lib.design
        if "lambdalib" in lib_name:
            continue
        assert lambdalib.check(path.format(lib_name=lib_name), 'auxlib')


@pytest.mark.parametrize('module,path', [
    (asap7sc7p5t, 'lambdapdk/asap7/libs/{lib_name}/lambda/stdlib'),
    (nangate45, 'lambdapdk/freepdk45/libs/{lib_name}/lambda/stdlib'),
    (sky130sc, 'lambdapdk/sky130/libs/{lib_name}/lambda/stdlib'),
    (gf180mcu, 'lambdapdk/gf180/libs/{lib_name}/lambda/stdlib')
    ])
def test_la_stdlib(module, path):
    libs = module.setup()
    if not isinstance(libs, list):
        libs = [libs]
    for lib in libs:
        lib_name = lib.design
        if "lambdalib" in lib_name:
            continue
        assert lambdalib.check(path.format(lib_name=lib_name), 'stdlib')


@pytest.mark.parametrize('path', [
    'lambdapdk/asap7/libs/fakeram7/lambda',
    'lambdapdk/freepdk45/libs/fakeram45/lambda',
    'lambdapdk/sky130/libs/sky130sram/lambda',
    'lambdapdk/gf180/libs/gf180mcu_fd_ip_sram/lambda',
    ])
def test_la_ramlib(path):
    assert lambdalib.check(path, 'ramlib')


@pytest.mark.parametrize('path', [
    'lambdapdk/sky130/libs/sky130io/lambda',
    'lambdapdk/gf180/libs/gf180mcu_fd_io/lambda',
    ])
def test_la_iolib(path):
    assert lambdalib.check(path, 'iolib')


@pytest.mark.parametrize('module', [
    asap7sc7p5t, fakeram7,
    nangate45, fakeram45,
    gf180mcu, gf180io, gf180sram,
    sky130sc, sky130io, sky130sram
])
def test_lambdalib_is_present(module):
    chip = Chip('<lib>')
    chip.use(module)

    has_lambda = False
    for libs in chip.getkeys('library'):
        if libs.startswith('lambdalib_'):
            has_lambda = True

    assert has_lambda, f"{module.__name__} does not have a lambdalib"
