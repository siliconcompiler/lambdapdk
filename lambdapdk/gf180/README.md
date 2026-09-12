# GF180MCU PDK

The GlobalFoundries 180nm MCU open source PDK, wired into SiliconCompiler.

**Cell libraries are fetched, not vendored.** Liberty, LEF, GDS, CDL, SPICE and Verilog for the
standard cells, the IO and the memories are referenced out of the published build of the
[open_pdks](https://github.com/RTimothyEdwards/open_pdks) revision pinned as `pdk_rev` in
`_GF180Data` ([`__init__.py`](__init__.py)).

The PDK and every library report that revision's date, `2026-08-27`, as their package version
(`PDK_VERSION` on the dataroot mixin) — so a manifest says which pin a run used.

| Dataroot | Provides |
|---|---|
| `gf180mcu_fd_sc_mcu7t5v0` | 7-track standard cells |
| `gf180mcu_fd_sc_mcu9t5v0` | 9-track standard cells |
| `gf180mcu_fd_io` | IO cells |
| `gf180mcu_fd_ip_sram` | SRAM macros |
| `common` | the shared `libs.tech` tree — Xyce device models |

## Variants, and why the technology files are still vendored

open_pdks builds **four** install variants, one per metal stack:

| variant | stackup |
|---|---|
| `gf180mcuA` | `3LM_1TM_30K` |
| `gf180mcuB` | `4LM_1TM_11K` |
| `gf180mcuC` | `5LM_1TM_9K` |
| `gf180mcuD` | `5LM_1TM_11K` |

This PDK exposes **eleven** stackups (3/4/5/6LM × 6K/9K/11K/30K) across 22 classes, so seven of them
have no upstream counterpart. The tech LEFs come from the gf180mcu-pdk repository, which ships every
stackup whether or not open_pdks installs it.

That is why `base/apr/` stays vendored *in full* rather than partly referenced: upstream's tech LEFs
also declare `Pwell` and `Nwell` layers the vendored ones do not, so sourcing four stackups upstream
and seven locally would give different layer sets depending on which stackup a design picks.

Only the GDS depends on the variant. The cell LEF, the liberty, the CDL and the SPICE netlist are
byte-identical across all four, and the SRAM macros are identical in every view — all 76 files — so
`library_path()` picks a variant from the metal count and everything else follows it.

## What this repository still holds

| Path | What |
|---|---|
| `base/apr/` | tech LEFs for all 11 stackups, and the 5LM/6LM layer maps |
| `base/pex/openroad/` | 48 OpenRCX decks |
| `base/setup/magic/`, `base/setup/netgen/` | DRC and LVS decks — **not refreshed**, see below |
| `base/setup/klayout/` | layer map, display, DRC rule decks, PCell macros |
| `libs/*/apr/openroad/` | `pdngen_*.tcl`, `global_connect.tcl`, `tapcell.tcl` |
| `libs/*/techmap/yosys/` | adder, latch and tristate techmaps |
| `libs/gf180mcu_fd_io/blackbox/` | generated from the LEFs by `scripts/make_blackbox.py` |
| `libs/*/lambda/` | generated lambdalib views |

## Known gaps

- **The magic and netgen decks are the vendored copies.** Upstream ships `gf180mcuA.tech`,
  `gf180mcuA.magicrc` and `gf180mcuA_setup.tcl`, but SiliconCompiler pins magic at `c7f11d2`
  (8.3.367, 2023-02-16) while magic HEAD is 8.3.683. The same block applies as for sky130 — see
  `lambdapdk/sky130/PATCHES.md`.
- **The OpenRCX decks are not upstream.** open_pdks publishes extraction rules for `gf180mcuC` and
  `gf180mcuD` only — 2 variants — against the 48 stackup/option/corner decks here.
- **The KLayout DRC decks are a different lineage.** Upstream has one `gf180mcu.drc` entry point with
  rule decks as `.rb`; this repository splits it into `gf180mcu.drc`, `gf180mcu_antenna.drc` and
  `gf180mcu_density.drc` with rule decks as `.drc`, which is the shape the SC runsets expect.
- **Three liberty corners** are registered per library. Upstream ships 15 for the standard cells and
  12 for the IO in the same dataroot; adding more costs no extra download.
- **The archives are not subsetted.** SiliconCompiler unpacks each one whole, including the `mag`
  hierarchy no flow here reads and all four install variants.

## Licensing

Apache 2.0, as upstream.
