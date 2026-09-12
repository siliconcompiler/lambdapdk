# Library module reference

`lambdapdk/<pdk>/libs/<name>.py`. Base class `LambdaLibrary` = `YosysStdCellLibrary` +
`OpenROADStdCellLibrary` + `KLayoutLibrary` + `BambuStdCellLibrary` + `_LambdaPath`.
Mix in the PDK's `_<Foo>Path` too when the library pulls from upstream.

## Skeleton

```python
class _FooStdCell(LambdaLibrary, _FooPath):
    def __init__(self, vt):
        super().__init__()
        self.set_name(f"foo_stdcell_{vt.lower()}")

        self.add_asic_pdk(FooPDK())     # also copies the PDK's stackup onto the library
        self.package.set_version(pdk_rev)
        self.add_asic_site("core7")
        ...

class FooStdCellHVT(_FooStdCell):
    def __init__(self):
        super().__init__("H")
```

Variants (Vt, track height, stackup, memory size) are subclasses of a private base that
takes the variant as a constructor argument. Every public class must be constructible with
**no arguments** — `get_libs()` and `LambalibTechLibrary.alias()` both rely on that.

## Filesets

| Fileset | Contents | Registered with |
| --- | --- | --- |
| `models.timing.<corner>.nldm` | liberty for one corner | `add_asic_libcornerfileset(corner, "nldm")` |
| `models.physical` | cell LEF + GDS | `add_asic_aprfileset()` |
| `models.lvs` | CDL | `add_asic_aprfileset()` |
| `models.gds` | GDS, when it comes from a different dataroot than the LEF | `add_asic_aprfileset()` |
| `models.sim` | behavioral Verilog — the simulation models for the cells | — |
| `rtl` | only when the cells need an RTL wrapper around them | — |
| `models.spice` | SPICE netlist | — |
| `models.blackbox` | blackbox Verilog | `add_yosys_blackbox_fileset("models.blackbox")` |
| `openroad.powergrid` | `pdngen.tcl` | `add_openroad_powergridfileset()` |
| `openroad.globalconnect` | `global_connect.tcl` | `add_openroad_globalconnectfileset()` |

Corner names chosen here (`slow` / `typical` / `fast`) are what the SC demo target's
timing scenarios must reference. `add_asic_pexcornerfileset(corner)` exists for
library-level parasitic corners.

Group `add_file` calls by dataroot: `with self.active_dataroot("foo130"):` for upstream
files, `with self.active_dataroot("lambdapdk"):` for anything this repo authors.
A library may bind several upstream dataroots (icsprout55: repo LEF/CDL/Verilog, plus
per-Vt liberty and GDS release-asset tarballs).

## Cell lists

`add_asic_celllist(type, cells)` — `cells` is a name, a list, or a wildcard pattern.
Valid types (from `siliconcompiler/library.py`):

| Type | Meaning |
| --- | --- |
| `tie` | tie-high / tie-low |
| `filler` | row-continuity fillers |
| `decap` | decoupling capacitor fillers |
| `tap` | well taps (latch-up prevention) |
| `endcap` | row-boundary cells |
| `antenna` | antenna diodes |
| `hold` | delay cells reserved for hold fixing |
| `clkbuf` | clock buffers/inverters |
| `clkgate` | integrated clock gating cells |
| `clklogic` | clock muxes, dividers |
| `dontuse` | cells synthesis must not pick |
| `physicalonly` | no logical function; stripped before LEC/LVS — filler, decap, tap, endcap, antenna belong here too |

What actually belongs in `dontuse` on a new library:

- **Scan chain flops** — scan variants of the flops, which synthesis should not reach for
  on its own; they get swapped in by the scan insertion step, if at all.
- **Sub-1X drive cells** — the `X0P5` / `0p5X` class of cells. They are too weak to drive
  anything real, and letting synthesis pick them produces a netlist that falls apart in
  APR.
- Poorly characterized or foundry-reserved cells.

A cell with liberty but **no Verilog model** is a warning, not a `dontuse` — it means the
gate-level netlist cannot be simulated as-is. Note it in the PDK README and raise it
upstream; do not exclude the cell from synthesis on that basis alone.

Cells with LEF/GDS but no liberty must be in `physicalonly`.

## Yosys

```python
self.set_yosys_driver_cell("BUFX1H7R")
self.set_yosys_buffer_cell("BUFX1H7R", "A", "Y")      # cell, input port, output port
self.set_yosys_tielow_cell("TIELOH7R", "Z")
self.set_yosys_tiehigh_cell("TIEHIH7R", "Z")
self.set_yosys_abc(1000, load)     # clock multiplier (1000 for a 1ns liberty time unit),
                                   # load in fF — conventionally 4x the buffer's input
                                   # pin capacitance; liberty quotes pF, so multiply by 1000
self.add_yosys_tech_map(lib_path / "techmap" / "yosys" / "cells_latch.v")
self.set_yosys_adder_map(lib_path / "techmap" / "yosys" / "cells_adders.v")
self.set_yosys_tristatebuffer_map(...)
self.add_yosys_synthesis_fileset(...)
self.add_yosys_blackbox_fileset("models.blackbox")
```

Techmaps are hand-written per library and live in `libs/<lib>/techmap/yosys/`. Latch and
adder maps are the two almost every library needs; copy the structure from
`freepdk45/libs/nangate45/techmap/yosys/` and retarget the cell and port names.

## OpenROAD

```python
with self.active_fileset("openroad.powergrid"):
    self.add_file(lib_path / "apr" / "openroad" / "pdngen.tcl")
    self.add_openroad_powergridfileset()
with self.active_fileset("openroad.globalconnect"):
    self.add_file(lib_path / "apr" / "openroad" / "global_connect.tcl")
    self.add_openroad_globalconnectfileset()

self.set_openroad_placement_density(0.60)
self.set_openroad_tielow_cell("TIELOH7R", "Z")
self.set_openroad_tiehigh_cell("TIEHIH7R", "Z")
self.set_openroad_macro_placement_halo(5, 5)          # microns
self.set_openroad_tapcells_file(lib_path / "apr" / "openroad" / "tapcells.tcl")
```

Also: `set_openroad_cell_padding(global_place, detailed_place)`,
`set_openroad_tracks_file`, `add_openroad_scan_chain_cells`,
`add_openroad_multibit_flipflops`.

`pdngen.tcl` must match the library's rail pitch and the PDK's routing layers. Getting
the straps wrong produces shorts that only surface in DRC — commit cf52b12 in this repo
is exactly that class of bug on sky130.

## KLayout / Bambu

`add_klayout_allowmissingcell(cell)` for cells absent from the GDS.
`set_bambu_device_name(name)` and `set_bambu_clock_multiplier(factor)` for HLS support
(optional; nangate45 has them).

## IO and SRAM libraries

Same shape, minus synthesis setup. See `sky130/libs/sky130io.py` and
`sky130/libs/sky130sram.py`. IO libraries usually need a blackbox fileset — generate it
with `scripts/make_blackbox.py`, which parses the LEF with `sc_leflib` and emits
`(* blackbox *)` module stubs. SRAM macros additionally implement the `RAMTechLib`
interface; see `references/lambdalib.md`.

## Sanity checks before declaring a library done

- Every signal pin has a routable access point in the LEF (pin metal reachable by a via
  the tech LEF defines). icsprout55 had 50 unroutable pins across 49 cells with the
  stock LEF; the fix was a patched LEF paired with the matching GDS stream.
- The LEF and the GDS describe the same geometry. Pairing a patched LEF with the stock
  stream promises pin metal the layout does not have.
- Liberty cell set is consistent across the corners you register.
- Site name in the library matches the site in the tech LEF.
