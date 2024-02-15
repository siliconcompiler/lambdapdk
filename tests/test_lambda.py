import pytest
from siliconcompiler import Chip
import lambdalib

from lambdapdk.asap7.libs import asap7sc7p5t
from lambdapdk.freepdk45.libs import nangate45
from lambdapdk.sky130.libs import sky130hd
from lambdapdk.gf180.libs import gf180mcu


@pytest.mark.parametrize('module,path', [
    (asap7sc7p5t, 'lambdapdk/asap7/libs/{lib_name}/lambda'),
    (nangate45, 'lambdapdk/freepdk45/libs/{lib_name}/lambda'),
    (sky130hd, 'lambdapdk/sky130/libs/{lib_name}/lambda'),
    (gf180mcu, 'lambdapdk/gf180/libs/{lib_name}/lambda')
    ])
def test_la_stdlib(module, path):
    libs = module.setup(Chip('<lib>'))
    if not isinstance(libs, list):
        libs = [libs]
    for lib in libs:
        lib_name = lib.design
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
