# PDK module reference

`lambdapdk/<pdk>/__init__.py`. Base class `LambdaPDK` (`lambdapdk/__init__.py`) =
`KLayoutPDK` + `OpenROADPDK` + `_LambdaPath`, so every PDK gets the SC `PDK` schema,
both tool mixins, and the `lambdapdk` dataroot.

## Dataroots

`_LambdaPath` registers the `lambdapdk` dataroot, resolved by `PythonPathResolver` with
`python_module_path_append=".."` — so it points at the **repo root**, and paths written
against it start with the `lambdapdk` package dir:

```python
pdk_path = Path("lambdapdk", "foo130", "base")
with self.active_dataroot("lambdapdk"):
    self.add_file(pdk_path / "setup" / "klayout" / "foo130.lyt", filetype="layermap")
```

When installed from a wheel it falls back to the GitHub archive for the matching version
tag (or git SHA for a dev build).

Upstream collateral gets its own dataroot, declared in a mixin so both the PDK class and
the library classes can bind it:

```python
pdk_rev = 'v1.10.102'          # tag, release, or commit SHA — never a branch

class _FooPath(_LambdaPath):
    def __init__(self):
        super().__init__()
        self.set_dataroot("foo130",
                          f"https://github.com/org/foo-pdk/archive/refs/tags/{pdk_rev}.tar.gz",
                          pdk_rev)
```

`set_dataroot(name, path, tag=None, clobber=False)`. `path` may be a local dir, a file
(its parent is used), a `git+https://…` URL, or an archive URL. Declare one dataroot per
distribution channel — icsprout55 needs three (repo archive, liberty release asset, GDS
release asset) because the release assets are not in the repo.

## Metadata

```python
self.set_name("foo130")          # the name ASIC.set_pdk() takes
self.set_foundry("Foo Foundry")  # or "virtual" for an academic/fake kit
self.package.set_version(pdk_rev)
self.set_node(130)               # nm
self.set_stackup("5M1TM")        # the string libraries must match via add_asic_stackup
self.set_wafersize(300)          # mm, optional
```

Also available (all optional, used by `calc_yield()` / `calc_dpw()`):
`set_unitcost`, `set_defectdensity`, `set_scribewidth(x, y)`, `set_edgemargin`.

The class **docstring is published documentation** (`docs/reference_manual/predef_modules/pdks.rst`
renders it). Describe the process, what the kit contains, and end with a `Sources:` list.

## Filesets

A fileset is a named bag of files; a registration call then tells a tool to consume it.
Conventional names in this repo:

| Fileset | Contents | Registered with |
| --- | --- | --- |
| `views.lef` | tech LEF | `add_aprtechfileset(tool)` for openroad, klayout, magic |
| `klayout.techmap` | `.lyt` (`filetype="layermap"`), `.lyp` (`filetype="display"`) | `add_layermapfileset("klayout", "def", "klayout")` + `add_displayfileset("klayout")` |
| `layermap` | standalone layer map | `add_layermapfileset("klayout", "def", "gds", fileset="layermap")` |
| `magic.drc` / `klayout.drc.<deck>` | DRC deck | `add_runsetfileset("drc", tool, name)` |
| `netgen.lvs` | LVS setup | `add_runsetfileset("lvs", "netgen", "basic")` |
| `openroad.fill` | `fill.json` (`filetype="fill"`) | `add_runsetfileset("fill", "openroad", "beol")` |
| `openroad.pex.<corner>` | OpenRCX `.rules` (`filetype="openrcx"`) | `add_pexmodelfileset("openroad", corner)` |

Other PDK-level registrations: `add_devmodelfileset(tool, type, …)`,
`add_waiverfileset(type, tool, name, …)`.

`filetype` is inferred from the extension via `siliconcompiler.utils.get_default_iomap()`
(`.lef`→lef, `.lib`/`.ccs`→liberty, `.gds`→gds, `.cdl`→cdl, `.sp`/`.spice`→spice,
`.v`/`.vh`→verilog, `.tcl`→tcl, `.def`→def…). Pass `filetype=` explicitly whenever the
extension lies — `.lyt`→`layermap`, `.lyp`→`display`, `.tech`→`tech`, `.rules`→`openrcx`,
`.json`→`fill`, a SPICE netlist used as an LVS deck→`cdl`.

## Routing and OpenROAD

```python
self.set_aprroutinglayers(min="MET2", max="MET5")   # bottom layer is usually rails-only
self.set_openroad_rclayers(signal="MET3", clock="MET4")
self.add_openroad_pinlayers(vertical="MET4", horizontal="MET3")
for layer, derate in [...]:
    self.set_openroad_globalroutingderating(layer, derate)   # fraction of tracks usable
```

Also on `OpenROADPDK`: `set_openroad_rcxmaxlayer`, `set_openroad_processnode`,
`set_openroad_detailedroutedisableviagen`, `set_openroad_detailedrouteviarepair`,
`set_openroad_detailedrouteviainpinlayers`.

## PEX / RC

`add_openroad_rclayer(corner, layertype, layer, resistance, capacitance=None)` —
`layertype` is `"routing"` or `"via"`. Resistance is Ω/µm at minimum width for routing,
Ω/cut for a via (capacitance forced to `None`). Capacitance is **F/µm**, which is why
every module defines `pF = 1e-12` and writes `1.07e-4 * pF`.

These seed pre-route estimation only. Three ways they get produced here, best first:

1. **Measured** — `scripts/pex_calibrate_all.py` sweeps `bench_wires` against the PDK's
   OpenRCX deck and pools a design-survey correction (sky130). Pair with
   `add_openroad_rccorrection(corner, layer, cap_factor=…)`.
2. **Derived from a vendor interconnect file** — GT2N computes R/µm and C/µm from the
   StarRC `.itf`; the derivation is written out in the comment block.
3. **Estimated** — icsprout55 takes R from the tech LEF `RESISTANCE RPERSQ` / min `WIDTH`
   and estimates C, because the kit publishes none.

State which of the three you used, in a comment, with the arithmetic. If there is an
OpenRCX deck, register it as `openroad.pex.<corner>` and use it for signoff; if there is
none, still create an empty `openroad.pex` fileset so the OpenROAD driver is satisfied
(`self.get("fileset", "openroad.pex", field="schema")` then `add_pexmodelfileset`), as
icsprout55 does.

## KLayout

`set_klayout_units(units)`, `add_klayout_hidelayers(layer)` (hide cell-outline and
areaid layers that otherwise paint over the whole layout), `add_klayout_drcparam(deck, param)`.

If upstream ships no layer map, author `base/setup/klayout/<pdk>.lyt` yourself and record
in its header how the layer numbers were recovered — streamout is impossible without it.
