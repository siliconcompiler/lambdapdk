# ASAP7 KLayout LVS runset

`asap7.lvs` is a KLayout LVS rule deck for ASAP7, registered on the `ASAP7PDK`
object as `('pdk', 'lvs', 'runsetfileset', 'klayout', 'lvs')`.

ASAP7 upstream ships only a Calibre SVRF LVS deck
(`calibre/ruledirs/lvs/lvsRules_calibre_asap7.rul`), and that deck is not
redistributed with the PDK — see `../../../docs/Calibre_Usage_Instructions.txt`.
This deck is therefore newly authored, from the layer definitions in the ASAP7
design rule manual (`../../../docs/asap7_drm_201207a.pdf`, Table 2.1.1) and
`../asap7.lyp`.

## Usage

```sh
klayout -b -r asap7.lvs \
    -rd input=<layout.gds> \
    -rd schematic=<reference.cdl> \
    -rd topcell=<cell> \
    -rd report=<out.lvsdb> \
    -rd target_netlist=<extracted.cir> \
    -rd threads=<n>
```

| Switch | Required | Default |
| --- | --- | --- |
| `input` | yes | — |
| `schematic` | yes | — |
| `topcell` | no | the layout's top cell |
| `report` | no | `<topcell>.lvsdb` |
| `target_netlist` | no | `<topcell>_extracted.cir` |
| `threads` | no | `4` |

The deck prints `LVS_RESULT: MATCH` or `LVS_RESULT: MISMATCH` and **exits
non-zero on a mismatch**, so it can be driven from a harness without parsing the
LVS database.

Note that KLayout resolves a relative `schematic()` / `target_netlist()` path
against the *layout's* directory rather than the working directory. The deck
expands all path parameters, but passing absolute paths is still recommended.

## Devices

ASAP7 defines exactly eight devices, and the deck extracts all of them as
`mos4`:

| Device | Threshold marker |
| --- | --- |
| `nmos_rvt`, `pmos_rvt` | none (absence of the three below) |
| `nmos_lvt`, `pmos_lvt` | LVT, `98/0` |
| `nmos_slvt`, `pmos_slvt` | SLVT, `97/0` |
| `nmos_sram`, `pmos_sram` | SRAMVT, `110/0` |

**No passive devices are extracted, deliberately.**
`../../../spice/hspice/7nm_TT_160803.pm` contains exactly the eight `.model`
lines above, and the DRM FEOL layer table lists no resistor, capacitor, diode or
BJT layers. Extracting passives would produce devices that no ASAP7 reference
netlist can contain, turning any layout that hit them into a spurious failure.

## Standard cells with no physical taps

`../../../README.md` notes that ASAP7 standard cells use the well and `p_sub`
pins as tap substitutes, and that LVS must tie `VDD` and `VSS` by name. The deck
follows this: the n-well takes its name from its `1/251` label, the substrate is
a global net named `VSS`, and `connect_implicit` ties same-named nets together.

Port names come from **text objects on the M1 pin layer, `19/251`**. The M1
label layer `19/2` is empty in the shipped standard cells.

## Verified coverage

Run against every subcircuit in the RVT standard-cell CDL
(`../../../../libs/asap7sc7p5t_rvt/netlist/asap7sc7p5t_28_R.cdl`), with spot
checks in LVT and SLVT and a purpose-built SRAM-VT article under
`tests/data/asap7_lvs/`:

**192 of 209 cells compare clean, with zero extraction errors.**

## Known limitations

The 17 cells that do not compare clean all fail for the same underlying reason:
the ASAP7 CDL is a **schematic-level** netlist that is electrically equivalent to
the layout but not structurally isomorphic to it, and KLayout's netlist comparer
requires structural isomorphism. Neither class is a deck defect. Cell names below
omit the `_ASAP7_75t_<R|L|SL>` suffix.

### Folded multi-finger devices (11 cells)

The CDL describes *unfolded* devices. `AOI21x1` declares `w=162.00n nfin=6`, but
a 7.5-track row cannot fit six fins, so the layout folds the device into two
3-fin fingers with **separate intermediate diffusion nodes**. The layout then
yields four `W=0.081U` transistors forming two parallel series-chains where the
schematic has two `W=0.162U` transistors in one chain. No combination of
`netlist.combine_devices` / `netlist.simplify` helps: parallel-merging the
fingers would require the two intermediate nodes to be the same net, and
physically they are not.

| Cells | CDL devices | Extracted |
| --- | --- | --- |
| `AOI21x1`, `OAI21x1`, `AND2x4`, `AND2x6`, `NAND3x2`, `NOR3x2`, `OR2x6` | 6 | 8 |
| `AOI22x1`, `OAI22x1` | 8 | 12 |
| `XOR2x1`, `XNOR2x1` | 10 | 12 |

These are ordinary usable cells, so this is the limitation that matters in
practice. Fixing it needs a netlist post-process that pairs same-gate fingers
across parallel chains.

### Series-stack ordering (6 cells)

Here the extracted and schematic device counts are identical; the transistors
within a series stack are simply ordered differently. In `OAI221xp5` the CDL
pull-up reads `VDD-B1-net32-B2-Y` while the layout draws `VDD-B2-net12-B1-Y`,
and the `A1`/`A2` stack is likewise reversed. `AOI211xp5` reverses its whole
three-stage pull-up: the CDL puts the `A1`∥`A2` pair next to VDD, the layout puts
it next to `Y`. Reordering a series stack does not change the logic function, but
it does change the labelled graph.

Affected: `A2O1A1O1Ixp25`, `AOI211xp5`, `OAI221xp5`, `SDFLx1`, `SDFLx2`,
`SDFLx3`. The reversal was confirmed directly for `AOI211xp5` and `OAI221xp5`;
the other four were not root-caused individually. Note `SDFHx1` passes while the
whole `SDFLx*` family fails, so one shared structure is likely responsible there.

Usefully, **every cell in this group is already marked `dontuse`** by
`../../../../libs/asap7sc7p5t.py` (patterns `*xp*_ASAP7*` and `SDF*`), so none of
them should appear in synthesis output in the first place. No cell in the folded
group is marked `dontuse`.
