# Sky130 PDK

This directory contains files for the Skywater 130nm open source PDK,
restructured into the format required for SC. These files are tagged with the
latest PDK version number (v0.0.2), although many of the files come from
OpenROAD and OpenLANE, rather than the [golden
copy](https://github.com/google/skywater-pdk-libs-sky130_fd_sc_hd) from Google.

## File sources

### `base/apr/`

`sky130_fd_sc_hd.tlef`

Source: [OpenROAD](https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/blob/2484116345a52074fee4b1755656369a2a9f75ce/flow/platforms/sky130hd/lef/sky130_fd_sc_hd.tlef)

Up-to-date as of commit `2484116`, no modifications.

`sky130_fd_sc_hdll.tlef`

Source: [open_pdks](https://github.com/RTimothyEdwards/open_pdks)

Copied from open_pdks (`sky130_fd_sc_hdll__nom.tlef`) at commit d8bfd6f2a19026ad9b614424c249243b670e2ab2, no modifications.

### `base/setup/klayout/`

`skywater130.lyt`

Source: based on [this
template](https://github.com/RTimothyEdwards/open_pdks/blob/master/sky130/klayout/sky130.lyt)
in the open_pdks repo. This is slightly different from the [version](
https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/blob/master/flow/platforms/sky130hd/sky130hd.lyt)
used by
OpenROAD, although I'm not sure if these differences are significant. This
version is used by OpenLANE (after being run through a script that
populates things like the `TECHNAME` variable), so it seemed like the safer option.

Up-to-date as of commit `b06f0f2`. Modifications:

- Used filled-in version of template post-install
- Adjusted name of LEF file in `<lef-files>` tag

`sky130.lyp`

Source: [open_pdks](https://github.com/RTimothyEdwards/open_pdks/blob/master/sky130/klayout/sky130.lyp)

Up-to-date as of `b06f0f2`.

`fill.json`

Source: [OpenROAD](https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/blob/master/flow/platforms/sky130hd/fill.json)

Up-to-date as of `2484116`.

### `base/setup/magic/`

`skywater130.magicrc`

Adapted from
https://github.com/RTimothyEdwards/open_pdks/blob/master/sky130/magic/sky130.magicrc.
Some contents were removed for simplicity, in particular the paths to reference
cells. These aren't necessary for DRC, just GDS export (which we handle with KLayout).

`sky130A.tech`

Source (filled-in template):
[open_pdks](https://github.com/RTimothyEdwards/open_pdks/blob/master/sky130/magic/sky130.tech).

Up-to-date as of `b06f0f2`.

### `base/setup/netgen/`

`lvs_setup.tcl`

Adapted from
https://github.com/RTimothyEdwards/open_pdks/blob/master/sky130/netgen/sky130_setup.tcl.

Up-to-date as of `b06f0f2`.

### `libs/sky130hd/gds/`

`sky130_fd_sc_hd.gds`

Source: [OpenROAD](https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/blob/master/flow/platforms/sky130hd/gds/sky130_fd_sc_hd.gds)

Up-to-date as of `2484116`.

### `libs/sky130hd/lef/`

`sky130_fd_sc_hd_merged.lef`

Source: [OpenROAD](https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/blob/master/flow/platforms/sky130hd/lef/sky130_fd_sc_hd_merged.lef)

Up-to-date as of `2484116`.

### `libs/sky130hd/nldm/`

`sky130_fd_sc_hd__tt_025C_1v80.lib `

Source: [OpenROAD](https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/blob/master/flow/platforms/sky130hd/lib/sky130_fd_sc_hd__tt_025C_1v80.lib)

Taken from `2484116`, then modified by using OpenROAD's
[markDontUse.py](https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/blob/master/flow/util/markDontUse.py)
to set the dont_use property on the cells specified in `drc_exclude.cells` and
`no_synth.cells` in this [directory](.
https://github.com/RTimothyEdwards/open_pdks/tree/master/sky130/openlane/sky130_fd_sc_hd).

### `libs/sky130hd/verilog/`

`primitives.v` and `sky130_fd_sc_hd.v`

Source: [open_pdks](https://github.com/RTimothyEdwards/open_pdks)

Generated using the open_pdks Makefiles at commit 6d4d11780c40b20ee63cc98e645307a9bf2b2ab8.


### `libs/sky130hdll/cdl/`, `libs/sky130hdll/gds/`, `libs/sky130hdll/verilog/`
Source: [open_pdks](https://github.com/RTimothyEdwards/open_pdks)

Copied from open_pdks at commit d8bfd6f2a19026ad9b614424c249243b670e2ab2, no modifications.

### `libs/sky130hdll/nldm/`
`sky130_fd_sc_hdll__ff_100C_1v95.lib.gz`, `sky130_fd_sc_hdll__ss_n40C_1v44.lib.gz` and `sky130_fd_sc_hdll__tt_025C_1v80.lib.gz`
Source: [open_pdks](https://github.com/RTimothyEdwards/open_pdks)

Copied from open_pdks at commit d8bfd6f2a19026ad9b614424c249243b670e2ab2, no modifications, then gzipped.

### `libs/sky130io/lef/`

`sky130_ef_io.lef`

Source: [open_pdks](https://github.com/RTimothyEdwards/open_pdks)

Every pad carries a
65.4um x 75.4um bond pad plate on met4 and met5, labelled `<PIN>_PAD` in the
GDS, but the vendor LEF only declared a shrunken part of it as the pin and left
the rest inside `OBS`. A bond pad placed on the plate therefore landed on what
the abstract called an obstruction, which a power grid short check reads as the
supply net shorting to the pad instance. The script gives the plate back to the
pin it belongs to and takes it out of `OBS`; nothing else in the file changes.

### `libs/sky130sram/`

`sky130_sram_2kbyte_1rw1r_32x512_8`

Source: [sky130_sram_macros](https://github.com/fossi-foundation/sky130_sram_macros)

Copied at commit 5ad1c96053ee8223fe7e956e314646adfce605dd. One modification: the
three `max_transition : 0.04;` lines the liberty file put on the `addr0`,
`wmask0` and `addr1` buses are removed, so the library's own
`default_max_transition : 0.5` applies to them as it does to every other pin.
0.04ns is simply the top of the characterised slew axis
(`index_1("0.00125, 0.005, 0.04")`), not a design rule, and no sky130hd cell can
drive it -- the best achievable is 0.062ns -- so the resizer fails with RSZ-0090
on any design that instantiates this macro. The macro it replaces carried no
pin-level `max_transition` at all.

Replaces the earlier `sky130_sram_1rw1r_64x256_8`, whose layout overlaps `vdd`
and `gnd` on met3 in 260 places -- two whole power via stacks drawn 0.06um
apart, in columns at x = 164.015 and x = 876.595. The GDS and the LEF agree, so
it is a defect in the macro rather than in its abstract, and a power grid short
check reports every one of them. This macro holds the same 2kbyte and declares
its supplies as four met3/met4 rings on `vccd1`/`vssd1`, which is also why
`apr/openroad/global_connect.tcl` matches those pin names.
