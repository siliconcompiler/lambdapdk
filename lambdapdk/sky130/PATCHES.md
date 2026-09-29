# Sky130 local patches

Sky130 collateral is taken by reference from the published build of the
[open_pdks](https://github.com/RTimothyEdwards/open_pdks) revision pinned as `pdk_rev` in
`_Sky130Data` ([`__init__.py`](__init__.py)) — nothing is copied into this repository. Two files are the exception:
they carry a defect that makes them unusable as shipped, so lambdapdk vendors a corrected copy.

Both corrections are mechanical and scripted, so a `pdk_rev` bump regenerates them rather than
needing the fix re-done by hand. **Both should stop being needed** once upstream takes the fix; when
that happens, delete the vendored file, drop the script, and move the fileset back onto the upstream
dataroot.

| File | Script | Upstream | Status |
|---|---|---|---|
| `libs/sky130io/lef/sky130_ef_io.lef` | [`scripts/patch_sky130io_bondpads.py`](../../scripts/patch_sky130io_bondpads.py) | `RTimothyEdwards/open_pdks` | **to report** |
| `libs/sky130sram/*/nldm/…_TT_1p8V_25C.lib` (×3) | [`scripts/patch_sky130sram_maxtran.py`](../../scripts/patch_sky130sram_maxtran.py) | `fossi-foundation/sky130_sram_macros` | **to report** |

Everything else in `libs/*/` is collateral lambdapdk authors itself — Yosys techmaps, `pdngen.tcl` /
`global_connect.tcl` / `tapcell.tcl`, blackbox Verilog, the generated `lambda/` views — plus the SRAM
*simulation* netlist, which open_pdks does not install (it ships only the LVS one, and the two are
different netlists rather than formatting variants).

## 1. IO bond pads are declared as obstructions

**File:** `libs/sky130io/lef/sky130_ef_io.lef`
**Affects:** 25 of the 39 macros in the upstream LEF.

Every pad carries a 65.4 µm × 75.4 µm bond pad plate on met4/met5, labelled `<PIN>_PAD` in the GDS —
exactly the footprint of `sky130_ef_io__bare_pad`. The upstream LEF declares only a shrunken part of
it as the pin and leaves the rest inside `OBS`. A bond pad placed on the plate therefore lands on
what the abstract calls an obstruction, which a power grid short check reads as the supply net
shorting to the pad instance.

Measured on `sky130_ef_io__vccd_hvc_pad` at the pinned revision: `OBS` covers **100 %** of the plate
area on met4 and 16.9 % on met5. After the patch, 0 % on both.

Only `sky130_ef_io__bare_pad` — which *is* the plate — gets this right upstream.

Note the defect has changed shape rather than been fixed. The 2023 vintage this library was
originally vendored from attached the shrunken rect to the net pin itself (`VCCD`); at the pinned
revision upstream has added a separate `VCCD_PAD` pin, but gave it the same shrunken rect
(60.8 × 60.8 µm) instead of the plate. The script handles both spellings.

The patch gives the plate back to the pin the GDS says it belongs to and subtracts it from `OBS`,
rect by rect so that obstructions not meeting the plate stay exactly as upstream wrote them. Nothing
else in the file changes.

### Regenerating

```bash
PDK=$(ls -d ~/.sc/cache/dataroot/sky130_fd_io-*/)   # or any unpacked open_pdks tree
klayout -b -r scripts/patch_sky130io_bondpads.py \
    -rd lef=$PDK/sky130A/libs.ref/sky130_fd_io/lef/sky130_ef_io.lef \
    -rd gds_dir=$PDK/sky130A/libs.ref/sky130_fd_io/gds \
    -rd out=lambdapdk/sky130/libs/sky130io/lef/sky130_ef_io.lef
```

It prints one line per macro and refuses to guess: a plate whose label resolves to no pin of the
macro, or to more than one, stops the run.

### Reporting upstream

Not yet filed. The report belongs on `RTimothyEdwards/open_pdks` and should say that it affects every
consumer of open_pdks sky130 IO, not just lambdapdk, and that `bare_pad` shows the intended
abstraction. The `OBS` coverage measurement above is the evidence.

## 2. SRAM liberty sets an undrivable `max_transition`

**File:** `libs/sky130sram/<macro>/nldm/…_TT_1p8V_25C.lib`, for all three macros
**Affects:** the `addr0`, `wmask0` and `addr1` buses of every one of them.

Upstream puts `max_transition : 0.04;` on those three buses. 0.04 ns is simply the top of the
characterised slew axis (`index_1("0.00125, 0.005, 0.04")`), not a design rule, and no sky130hd cell
can drive it — the best achievable is 0.062 ns — so the resizer fails with **RSZ-0090** on any design
that instantiates this macro. Removing the three lines lets the library's own
`default_max_transition : 0.5` apply to those buses as it does to every other pin.

The macro this one replaced carried no pin-level `max_transition` at all.

This is the *only* difference between the vendored file and the upstream artifact; the LEF and Verilog of
the same macro are byte-identical, which is why they are referenced rather than copied.

### Regenerating

```bash
PDK=$(ls -d ~/.sc/cache/dataroot/sky130_sram_macros-*/)
for M in sky130_sram_1kbyte_1rw1r_32x256_8 \
         sky130_sram_1kbyte_1rw1r_8x1024_8 \
         sky130_sram_2kbyte_1rw1r_32x512_8; do
  python3 scripts/patch_sky130sram_maxtran.py \
      --input $PDK/sky130A/libs.ref/sky130_sram_macros/lib/${M}_TT_1p8V_25C.lib \
      --output lambdapdk/sky130/libs/sky130sram/$M/nldm/${M}_TT_1p8V_25C.lib
done
```

The script refuses to run if the attribute is not on exactly those three buses, so upstream moving it
is a failure to look at rather than a line silently dropped.

### Reporting upstream

Not yet filed. `fossi-foundation/sky130_sram_macros` is the home; the argument above is the whole
report.

## Generated, not patched: the IO blackboxes

`libs/sky130io/blackbox/*.v` are produced from the LEF by
[`scripts/make_blackbox.py`](../../scripts/make_blackbox.py), so they follow whatever the LEF says
and must be regenerated whenever `pdk_rev` moves. They were stale before this migration — 32 of 39
`ef` macros and 21 of 32 `fd` ones.

```bash
PDK=$(ls -d ~/.sc/cache/dataroot/sky130_fd_io-*/)
python3 scripts/make_blackbox.py \
    --lef lambdapdk/sky130/libs/sky130io/lef/sky130_ef_io.lef \
    --output lambdapdk/sky130/libs/sky130io/blackbox/sky130_ef_io.v
python3 scripts/make_blackbox.py \
    --lef $PDK/sky130A/libs.ref/sky130_fd_io/lef/sky130_fd_io.lef \
    --output lambdapdk/sky130/libs/sky130io/blackbox/sky130_fd_io.v \
    --source 'sky130A/libs.ref/sky130_fd_io/lef/sky130_fd_io.lef @ pdk_rev'
```

The `ef` blackbox is generated from the **patched** LEF, since that is the abstract the flow uses.
`--source` keeps the machine-specific cache path out of the committed header.

Upstream does ship `sky130_fd_io__blackbox.v` and `…_pp.v`, but they are not a substitute: they cover
12 modules against the 32 in the LEF, missing every `overlay_*` cell, and there is no `ef`
equivalent at all.

## Fixed here: the SRAM control polarity

`csb0`, `csb1` and `web0` on the OpenRAM macros are **active low** -- the macro's own Verilog says
"active low chip select" and "active low write control" -- while `la_spram`'s `ce`/`we` are active
high, its reference model writing on `if (ce & we)`. The map this repository carried fed the
active-high expressions straight in:

```verilog
.csb0 (ce_in && we_in),   .csb1 (ce_in && ~we_in),   .web0 (ce_in && we_in),
```

which inverts every control. On a read (`ce=1, we=0`) that selects port 0 *and* puts it in write
mode, so the read writes `din0` into the array, while `csb1=1` leaves the read port deselected. On a
write it deselects port 0 entirely. Reads corrupted memory and writes did not land.

The mapping now inverts each one, and there is only a single map: the macros are 1rw1r, so
`la_dpram` is the cell that matches the hardware and `la_spram` is a hand-written adapter on top of
it -- the same relationship `la_spregfile` already had with `la_spram`. Mapping the macro a second
time would be a second chance to get the polarity wrong.

## Not patched, but not refreshed either: the magic and netgen decks

`base/setup/magic/sky130A.tech` and `base/setup/netgen/lvs_setup.tcl` are still the vendored 2023
copies, even though the upstream `common` archive carries current ones.

SiliconCompiler pins magic at `c7f11d2` — version **8.3.367**, dated **2023-02-16** — in
`siliconcompiler/toolscripts/_tools.json`, with `"auto-update": false` so the dependency bot never
bumps it. Magic HEAD is 8.3.683. SC's `add_version(">=8.3.196")` floor is cleared by the pin, so
nothing warns.

open_pdks stamps the building magic's commit and version into the installed tech file
(`COMMIT_DEFS += -DMAGIC_COMMIT=… -DMAGIC_VERSION=…`), which suggests the pairing is meant to be
close. Handing a 2026 `sky130A.tech` to a 2023 magic has not been measured — it may only warn — so
the decks stay put until it is. That measurement, and any bump, is SiliconCompiler-side work.

## Known gaps

- **The magic and netgen decks are the 2023 copies.** SiliconCompiler pins magic at `c7f11d2`
  (8.3.367, 2023-02-16) with `"auto-update": false`, while magic HEAD is 8.3.683. Pairing a current
  `sky130A.tech` with that magic has not been measured, so the decks stay until it is. Details in
  [PATCHES.md](PATCHES.md).
- **Three liberty corners** are registered per standard cell library (`slow`/`typical`/`fast`).
  Upstream ships 18 for hd and 13 for hdll in the same dataroot; adding more costs no extra download.
- **The archives are not subsetted.** SiliconCompiler unpacks each one whole, including the `mag`
  hierarchy no flow here reads and both install variants, so the on-disk cache is far larger than the
  files actually referenced — roughly 2.5 GB across the four sky130 dataroots.
- **The IO `fast` corner uses a 5.50V IO supply.** `sky130io` now carries real characterised timing
  for 26 cells at `slow`/`typical`/`fast`, a consistent 3.3V-IO set (`ss`/100 °C/1.60V/3.00V,
  `tt`/25 °C/1.80V/3.30V) — except `fast`, where upstream characterises no 3.60V corner and 5.50V is
  the only IO supply any `ff` corner is offered at. See `_IO_CORNERS` in `libs/sky130io.py`.
- **Not every IO cell has timing.** 26 of the library's cells are characterised upstream; the rest
  (fillers, bus slices, corner cells) have none there either, so nothing is lost relative to what was
  shipped before.
- **The OpenRCX decks moved upstream, and the RC calibration has not caught up.** The
  `add_openroad_rclayer` / `add_openroad_rccorrection` values in `__init__.py` were measured on
  2026-09-02 by `scripts/pex_calibrate_all.py` against the **2023** decks this repository used to
  vendor, and the coupling tables have moved since — met1 area capacitance goes 3.42844e-05 to
  3.93264e-05, about 15%. Re-run that sweep. Nothing warns if it is not done.
  Upstream builds each corner against three extraction references; the `spef_extractor` deck is the
  one used here, and the one the vendored copies matched.
- **`fill.json` and the Yosys techmaps are not upstream data.** open_pdks installs no OpenROAD fill
  configuration at all — the nearest things it ships are `magic/generate_fill.py`, a different
  mechanism, and a KLayout density *check*. `fill.json` comes from OpenROAD-flow-scripts and stays.
  The techmaps and the `dontuse` list do have `librelane/sky130_fd_sc_hd/` counterparts, but they are
  a different lineage rather than a fresher copy: upstream maps tristates onto `ebufn_2` through
  Yosys's `_TECHMAP_EBUF_N_` hook where this uses `ebufn_1` and `_TECHMAP_REPLACE_`, splits adders
  across three files, and expresses cell exclusions as globs split by stage
  (`synth_excluded.cells` / `pnr_excluded.cells`). Taking that exclusion list wholesale would mark
  this library's own clkbuf, tap, fill, decap and diode cells `dontuse` — they are excluded from
  synthesis upstream but needed in place-and-route.
- **There is no SRAM simulation netlist.** open_pdks installs only the LVS netlist; the separate
  OpenRAM simulation netlist was dropped rather than carried, since nothing here can maintain it.
- **The KLayout `.lyt` stays vendored on purpose.** Upstream's `sky130A.lyt` uses the older LEF/DEF
  reader-options schema (`<routing-suffix>` rather than `<routing-suffix-string>`, no
  `produce-lef-pins`, no `read-lef-with-def`) and points `<lef-files>` at a `merged.lef` this
  repository does not produce. Adopting it would be a regression. The `.lyp` beside it is a plain
  display file, was never modified here, and is now referenced.
