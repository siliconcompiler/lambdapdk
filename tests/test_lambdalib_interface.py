import pytest

from lambdapdk.sky130.libs.sky130sram import (
    Sky130Lambdalib_SinglePort,
    Sky130Lambdalib_SinglePortRegfile,
)
from lambdapdk.gf180.libs.gf180sram import (
    GF180Lambdalib_SinglePort,
    GF180Lambdalib_SinglePortRegfile,
)
from lambdapdk.asap7.libs.fakeram7 import (
    FakeRAM7Lambdalib_SinglePort,
    FakeRAM7Lambdalib_DoublePort,
    FakeRAM7Lambdalib_TrueDoublePort,
    FakeRAM7Lambdalib_SinglePortRegfile,
)
from lambdapdk.freepdk45.libs.fakeram45 import (
    FakeRAM45Lambdalib_SinglePort,
    FakeRAM45Lambdalib_SinglePortRegfile,
)
from lambdapdk.ihp130.libs.sg13g2_sram import (
    IHP130Lambdalib_SinglePort,
    IHP130Lambdalib_SinglePortRegfile,
)


# Memory LambalibTechLibrary wrappers. lambdalib's pytest plugin diffs each
# wrapper's interface against the canonical lambda cell it substitutes.
MEMORY_TECHLIBS = [
    Sky130Lambdalib_SinglePort,
    Sky130Lambdalib_SinglePortRegfile,
    GF180Lambdalib_SinglePort,
    GF180Lambdalib_SinglePortRegfile,
    FakeRAM7Lambdalib_SinglePort,
    FakeRAM7Lambdalib_DoublePort,
    FakeRAM7Lambdalib_TrueDoublePort,
    FakeRAM7Lambdalib_SinglePortRegfile,
    FakeRAM45Lambdalib_SinglePort,
    FakeRAM45Lambdalib_SinglePortRegfile,
    IHP130Lambdalib_SinglePort,
    IHP130Lambdalib_SinglePortRegfile,
]


@pytest.mark.parametrize(
    "techlib", MEMORY_TECHLIBS, ids=[cls.__name__ for cls in MEMORY_TECHLIBS])
def test_memory_lambdalib_interface(techlib, assert_lambdalib_techlib_interface):
    assert_lambdalib_techlib_interface(techlib)
