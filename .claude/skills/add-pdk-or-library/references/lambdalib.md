# lambdalib wrappers

Lambdalib is the Verilog abstraction layer that makes a design portable across PDKs.
A lambdapdk library becomes usable through lambdalib by shipping a `LambalibTechLibrary`
subclass: a small Design that owns the `la_*` Verilog implementation and knows which
technology libraries it pulls in.

Source of truth: `~/lambdalib` (not the stale `.venv` copy).

## The wrapper class

```python
from lambdalib import LambalibTechLibrary
from lambdapdk import _LambdaPath

class FooLambdalib_la_iobidir(LambalibTechLibrary, _LambdaPath):
    def __init__(self):
        super().__init__("la_iobidir", [Foo_IOLibrary])   # lambda cell, techlib classes
        self.set_name("foo_la_iobidir")
        self.package.set_version("v1")

        lib_path = Path("lambdapdk", "foo130", "libs", "foo130io")
        with self.active_dataroot("lambdapdk"):
            with self.active_fileset("rtl"):
                self.add_file(lib_path / "lambda" / "la_iobidir.v")
```

`LambalibTechLibrary.__init__(lambdalib, techlibs, fileset="rtl")`. The classmethod
`alias(project)` is what a target calls; it needs a **zero-argument constructor**.

One wrapper per `la_*` cell. Group them with an aggregator class exposing a classmethod
`alias()` that forwards to each — see `Sky130LambdaLib_IO` at the end of
`lambdapdk/sky130/libs/sky130io.py`.

## Memories

An SRAM macro class additionally subclasses `lambdalib.ramlib.RAMTechLib` and implements:

| Method | Returns |
| --- | --- |
| `get_ram_width()` | data width in bits |
| `get_ram_depth()` | **log2** of the number of words (see `Sky130_SRAM_32x512`) |
| `get_ram_ports()` | dict mapping macro port name → the expression to connect |
| `get_ram_libcell()` | the macro's cell name |
| `get_ram_defaultctrl()` | default value for unused control bits, e.g. `"1'b0"` |
| `get_ram_defaultctrl_width()` | width of that default |

The `la_spram` / `la_spregfile` Verilog is **generated**, not hand-written. Each SRAM
module has a `__main__` block that calls `Spram().write_lambdalib(path, techlibs)` and
then formats the output with Verible:

```bash
python -m lambdapdk.foo130.libs.foo130sram --verible_bin $(which verible-verilog-format)
```

Regenerate and commit the output whenever the macro set changes.

## Standard cell lambda views

`libs/<lib>/lambda/stdlib/` and `lambda/auxlib/` hold generated per-cell mappings
(`freepdk45/libs/nangate45/lambda/stdlib` is the reference). `scripts/generate_lamdbalib.py`
drives generation for the PDKs listed in its `libs` dict, keyed by SC demo target.

Caveat: that script predates the current lambdalib API — it calls `lambdalib.generate` /
`lambdalib.copy`, which no longer exist in `~/lambdalib`. Check the current API before
using it, and update the script rather than working around it. Its `auxlib` section is
still the best record of which `la_*` aux cells each library implements versus leaves
missing; extend that table when you add a PDK.

## Testing

Memory wrappers are interface-checked against the canonical lambda cell by lambdalib's
pytest plugin. Add each new wrapper class to `MEMORY_TECHLIBS` in
`tests/test_lambdalib_interface.py`:

```python
@pytest.mark.parametrize("techlib", MEMORY_TECHLIBS, ids=[c.__name__ for c in MEMORY_TECHLIBS])
def test_memory_lambdalib_interface(techlib, assert_lambdalib_techlib_interface):
    assert_lambdalib_techlib_interface(techlib)
```

The fixture (`lambdalib/reusable_tests/techlib_interface.py`) diffs the wrapper's port
list against the `la_*` cell it substitutes, so a renamed or missing port fails there
rather than at elaboration time in a user's build.
