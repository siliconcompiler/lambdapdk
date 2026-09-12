# Enablement reference

What a lambdapdk PDK and library can declare, and which upstream collateral feeds each
knob. Use this when auditing an update: for every new upstream file the diff surfaces,
find the row it belongs to, then check whether that row is already populated.

## How a dataroot-backed PDK is laid out

```
lambdapdk/<pdk>/
├── __init__.py          pdk_rev, _<PDK>Path (set_dataroot), the PDK class
├── base/                lambdapdk-owned collateral (PEX decks, fill rules, klayout setup)
│   ├── setup/klayout/   .lyt / .lyp we write when upstream ships none
│   ├── pex/openroad/    OpenRCX .rules decks
│   └── dfm/openroad/    fill.json
├── libs/
│   ├── <lib>.py         the library classes
│   └── <lib>/apr/openroad/  pdngen.tcl, global_connect.tcl, tapcell.tcl
└── README.md            optional per-PDK documentation
```

Two dataroots are in play in almost every file:

- `with self.active_dataroot("<pdk>")` — paths are relative to the **upstream** archive
  root. These are what a revision bump can break.
- `with self.active_dataroot("lambdapdk")` — paths are relative to **this repository**.
  A rev bump never breaks these, but new upstream collateral can make one redundant
  (e.g. upstream starts shipping a `.lyt`, so our hand-written one can go).

The `_<PDK>Path` mixin holds `set_dataroot`, and both the PDK and its libraries inherit
it, so the pinned revision is declared exactly once per package.

## PDK-level knobs

| Setter | Upstream collateral that feeds it |
|---|---|
| `set_foundry` / `set_node` / `set_stackup` / `set_wafersize` | process documentation |
| `package.set_version` | the pinned rev, where the PDK tracks it (ihp130, icsprout55) |
| `package.add_doc(kind, path)` | PDFs under `libs.doc/`; kinds seen here: `quickstart`, `signoff` |
| `add_aprtechfileset(tool)` in a `views.lef` fileset | the technology LEF |
| `add_layermapfileset` / `add_displayfileset` | `.map` layermap, KLayout `.lyt` / `.lyp` |
| `set_aprroutinglayers(min, max)` | routable layer range in the tech LEF |
| `add_openroad_pinlayers(vertical, horizontal)` | tech LEF routing directions |
| `set_openroad_rclayers(signal, clock)` | which layer the RC estimate uses pre-route |
| `set_openroad_globalroutingderating(layer, derate)` | per-layer congestion derate; **one entry per routing layer** |
| `add_openroad_rclayer(corner, "routing"\|"via", layer, r, c)` | ITF / OpenRCX decks, or calibration |
| `add_openroad_rccorrection(corner, layer, cap_factor=...)` | `scripts/pex_calibrate_all.py` output |
| `add_pexmodelfileset("openroad", corner)` | OpenRCX `.rules` deck |
| `add_runsetfileset("drc", tool, name)` | `.drc` / `.lydrc` decks |
| `add_runsetfileset("lvs", tool, name)` | `.lvs` / netgen setup |
| `add_runsetfileset("fill", "openroad", "beol")` | `fill.json` |
| `add_klayout_drcparam(name, "key=<value>")` | how the KLayout deck is invoked |
| `add_klayout_hidelayers` | display tuning |
| `set_openroad_rcxmaxlayer` | top layer OpenRCX should extract |
| `set_openroad_detailedroutedisableviagen`, `...viainpinlayers`, `...viarepair` | detailed-route workarounds for a given stack |
| `set_defectdensity` / `set_edgemargin` / `set_scribewidth` / `set_unitcost` | yield/cost modelling |

## Library-level knobs

| Setter | Upstream collateral that feeds it |
|---|---|
| `add_asic_pdk(<PDK>())` | binds the library to its PDK |
| `add_asic_site(name)` | site name in the cell LEF — **a renamed site breaks placement** |
| `add_asic_stackup` | for libraries valid on one stackup only |
| `add_asic_libcornerfileset(corner, model)` | Liberty `.lib` per corner; model is `nldm`/`ccs` |
| `add_asic_pexcornerfileset(corner)` | per-corner parasitic models |
| `add_asic_aprfileset()` | LEF + GDS (`models.physical`), CDL (`models.lvs`), Verilog (`models.sim`) |
| `add_asic_celllist(type, cells)` | types used here: `tie`, `hold`, `filler`, `decap`, `antenna`, `tap`, `endcap`, `clkbuf`, `dontuse`, `physicalonly` |
| `set_yosys_driver_cell` / `set_yosys_buffer_cell` | cell names in the Liberty |
| `set_yosys_tielow_cell` / `set_yosys_tiehigh_cell` | tie cell names and their output pins |
| `set_yosys_abc(max_fanout, max_cap)` | characterization; the cap is usually 4x a small buffer's input cap |
| `set_yosys_tristatebuffer_map` / `set_yosys_adder_map` / `add_yosys_tech_map` | techmap Verilog under `libs/<lib>/techmap/yosys/` |
| `add_yosys_blackbox_fileset` / `add_yosys_synthesis_fileset` | blackbox and synthesis-only views |
| `set_openroad_placement_density` | tuned per library |
| `set_openroad_tielow_cell` / `set_openroad_tiehigh_cell` | as above, for APR |
| `set_openroad_macro_placement_halo(x, y)` | macro keepout |
| `set_openroad_cell_padding` | placement padding |
| `add_openroad_powergridfileset` / `add_openroad_globalconnectfileset` | `pdngen.tcl`, `global_connect.tcl` |
| `set_openroad_tapcells_file` | `tapcell.tcl` |
| `set_openroad_tracks_file` | explicit track definition when the LEF is not enough |
| `add_openroad_multibit_flipflops` | multibit FF cells, if the library gains them |
| `add_openroad_scan_chain_cells` | scan cells, if the library gains them |
| `add_klayout_allowmissingcell` | cells with no GDS (abstract-only) |
| `set_bambu_clock_multiplier` / `set_bambu_device_name` | HLS timing scaling |

## Signals to look for in an upstream diff

| What appears upstream | What it usually means |
|---|---|
| new `lib/` files with a new voltage or temperature in the name | a new timing corner to wire up with `add_asic_libcornerfileset` |
| `*_ccs.lib` alongside the existing `.lib` | CCS models — a second delay model, registered with model name `ccs` |
| a new macro name across `lef/ gds/ lib/ cdl/ verilog/` | a new SRAM or IO macro: a new library class plus a `get_libs()` entry |
| a first `2P` / dual-port macro | may justify a new lambdalib mapping (`Lambdalib_DoublePort`) |
| new `.drc` / `.lvs` / `.lydrc` decks | `add_runsetfileset`, plus `add_klayout_drcparam` for KLayout |
| a `.lyt` / `.lyp` / `.map` where we ship our own under `base/setup/klayout/` | our hand-written version may now be redundant |
| a changed tech LEF | re-check `set_aprroutinglayers`, pin layers, per-layer derating, and rerun PEX calibration |
| an `.itf` / `.nxtgrd` / `.captable` | the source for `add_openroad_rclayer` values |
| a new `*_udp.v` or similar next to the cell Verilog | the sim models may not compile without it |
| a new stackup directory | potentially a whole new PDK object, like GF180's `<n>LM` variants |

## Things a revision bump must keep in sync

- `pdk_rev` and `package.set_version(pdk_rev)` — only where the PDK already ties them
  together (ihp130, icsprout55). GT2N pins a rev but versions the package `"v0"`
  independently; do not change that convention as a side effect.
- Release-asset dataroots (icsprout55) embed both the tag **and** the asset filename.
  Asset names carry dates and change between releases, so a tag bump alone can 404.
- SiliconCompiler's targets in `siliconcompiler/targets/<pdk>_demo.py` import library
  classes by name. Renaming or adding a library class is a change in **two**
  repositories, and CI here will not catch the SC side.
- `lambdapdk/__init__.py`'s `get_pdks()` and `get_libs()` must list every new class, or
  nothing tests it.
- `README.md` has a "Supported PDKs" table and a per-PDK inventory section.
