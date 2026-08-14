# ASAP7 KLayout LVS runset

`asap7.lvs` is a KLayout LVS rule deck for ASAP7, registered on the `ASAP7PDK`
object under two deck names that are the same file with different parameters:

| Deck name | Parameters | Use |
| --- | --- | --- |
| `('pdk', 'lvs', 'runsetfileset', 'klayout', 'lvs')` | no `blackbox` | per-cell checks; full hierarchical check of a block |
| `('pdk', 'lvs', 'runsetfileset', 'klayout', 'lvs_blackbox')` | `blackbox=*_ASAP7_75t_*` | one hardened block: its routing and row abutment only |

Note the second is for a *single* block. An array of abutted blocks needs a
`blackbox` glob naming the blocks, not the standard cells — see
[Block-level use](#block-level-use).

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
    -rd threads=<n> \
    -rd run_mode=<deep|flat> \
    -rd blackbox=<glob>[;<glob>...]
```

| Switch | Required | Default |
| --- | --- | --- |
| `input` | yes | — |
| `schematic` | yes | — |
| `topcell` | no | the layout's top cell |
| `report` | no | `<topcell>.lvsdb` |
| `target_netlist` | no | `<topcell>_extracted.cir` |
| `threads` | no | `4` |
| `run_mode` | no | `deep` |
| `blackbox` | no | unset — nothing is black-boxed |

`run_mode=flat` is a debugging aid only. It is impractically slow on anything
larger than a handful of cells (upwards of 20 minutes single-threaded for one
~1300-instance tile).

The deck prints `LVS_RESULT: MATCH` or `LVS_RESULT: MISMATCH` and **exits
non-zero on a mismatch**, so it can be driven from a harness without parsing the
LVS database. When `blackbox` is in effect it additionally prints `LVS_BLACKBOX:`
and `LVS_BLACKBOX_NOTE:` lines, because a black-boxed match is a weaker claim.

Note that KLayout resolves a relative `schematic()` / `target_netlist()` path
against the *layout's* directory rather than the working directory. The deck
expands all path parameters, but passing absolute paths is still recommended.

### Driving it from siliconcompiler

siliconcompiler has no KLayout LVS task, so nothing consumes the runset
automatically — a flow has to build the command line itself. The parameter set is
published as PDK metadata to make that mechanical, in the same shape as KLayout
DRC's `drc_params`:

```python
pdk.get("tool", "klayout", "lvs_params")   # {(deck name, "name=value")}
pdk.add_klayout_lvsparam("lvs", "blackbox=*_ASAP7_75t_*")   # to override
```

Values contain `<...>` placeholders for the flow to substitute: `<input>`,
`<topcell>`, `<report>`, `<threads>` — as on the DRC side — plus `<schematic>`
and `<target_netlist>`. The report is a `.lvsdb`, not a `.lyrdb`.

The `lvs_params` key and `add_klayout_lvsparam` are defined by `LambdaPDK`
(`lambdapdk/__init__.py`), guarded, so they give way if siliconcompiler gains
the same key.

## Black-boxing

`blackbox` takes `;`-separated cell-name globs and drops those cells' contents
from **both** the layout and the reference netlist, leaving only their pins. What
is compared is then the parent's connectivity: whether the routing and the row
abutment implement the netlist.

```sh
klayout -b -r asap7.lvs ... -rd blackbox='*_ASAP7_75t_*'
```

Use it at block level. It is the practical answer to the folded-cell limitation
below — those cells make a hierarchical compare fail on the cell even when the
block is wired correctly — and it also cuts runtime on large arrays.

`blank_circuit` is applied **before** `netlist.simplify`/`netlist.purge`, as the
KLayout manual requires: the flag it sets is what stops an abstract circuit from
being purged. On KLayout 0.28.16 the order was measured to make no difference to
any article in this repository — the black-boxed folded-cell row and a row with
deliberately floating instance pins produce byte-identical `.cir` and `.lvsdb`
either way — so this is a conformance fix, not a fix for an observed failure.

What a black-boxed run **does** check: every net at and above the black-boxed
level, which pin of which instance each net reaches, and therefore the routing
and the abutment. A miswired route is still reported as a mismatch.

What it **does not** check: anything inside the black-boxed cells. Cell internals
are a separate, one-off check — run the deck per cell against the library CDL,
which is what `tests/test_asap7_klayout_lvs.py::test_lvs_stdcell` does.

Two constraints:

* A glob must not match the top cell. Blanking the top cell on both sides leaves
  nothing to compare and the compare then trivially passes, so the deck refuses.
* `blank_circuit` matches case-sensitively and the CDL reader upcases circuit
  names, so the deck applies each glob in both the given and the upper-cased
  spelling. A glob whose letter case is inconsistent with the GDS cell names may
  match only one side, which surfaces as a mismatch.

## Block-level use

Above the cell the check is normally run in **tiers**, and the tier decides what
`blackbox` should name. For a design that hardens blocks separately and then
abuts them into an array:

| Tier | Layout | Netlist | `blackbox` |
| --- | --- | --- | --- |
| block | one hardened block | that block's `write_cdl` | `*_ASAP7_75t_*` — standard cells |
| array | the abutted array | the hierarchical netlist | the *block* cells, e.g. `tile_*` |

At the array tier the thing being checked is block-pin to block-pin: whether
abutment and top-level routing implement the netlist, independent of block
interiors, which the block tier already covered. This is the documented use of
abstract circuits — take out the big IP blocks that were verified separately.

**Blanking standard cells is the wrong glob for an array**, even though it is
what the registered `lvs_blackbox` deck name passes. It does not blank the
blocks, so every block interior is still extracted and compared; blocks are the
granularity an array run needs. `lvs_blackbox` is the deck for a *single hardened
block*, not for an abutted array — at the array tier, pass a `blackbox` glob that
names the blocks.

Blanking is also what makes an array run affordable: a blanked circuit's interior
is never extracted, so the work is skipped rather than done and discarded. The
manual describes `blank_circuit` as acting on the netlist after extraction, but
deep extraction is lazy enough in practice that the saving is real and large.

Two caveats carry over from above. A blanked run is a **weaker claim** than a
plain one — it says nothing about what is inside the blanked cells, which is why
the deck prints `LVS_BLACKBOX_NOTE:`. And an abstract circuit matches on pin
count and pin name, so block pins must actually be **named**: that is what the
`<metal>/251` label stack above is for, and without it an array-level "clean" is
not trustworthy.

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
pins as tap substitutes, and that LVS must tie `VDD` and `VSS` by name. `TAPCELL`
is no exception, so **there is no physical tie between the n-well and the VDD rail
anywhere in the hierarchy**, and the tie has to be made by the deck.

The deck declares both the substrate and the well as *global* nets and also joins
each to the identically named rail:

```ruby
connect_global(sub,   "VSS")
connect_global(nwell, "VDD")
connect_implicit("VDD")
connect_implicit("VSS")
```

Both halves are needed, and this is the part that is easy to get wrong:

* **Label-only (`connect_implicit` alone) breaks above the cell.** Inside a cell
  the well net is labelled VDD on `1/251` and the M1 rail is labelled VDD on
  `19/251`, so the implicit join works and the cell compares clean as a top cell.
  One level up the well net has no label of its own, so the join cannot be made
  there, and KLayout reports the cell's unsatisfied must-connect requirement as an
  extraction error: `[must-connect] In cell <parent>: Must-connect nets VDD of
  circuit <cell> are not connected`. Implicit connections in a subcircuit must be
  resolved at the next level up, physically or by another implicit connection.
* **Global alone leaves duplicate pins.** `connect_global` names the net in every
  circuit, which fixes the extraction error, but the well net and the M1 rail stay
  two distinct same-named nets. Both become pins, so the extracted `INVx1` has six
  pins (`A, VDD, VSS, Y, VSS, VDD`) where its CDL declares four, and no cell
  matches.

Together, the global names the net at every level and the implicit connect unites
it with the rail inside each circuit, which is what satisfies must-connect all the
way to the top cell while keeping the CDL pin list.

The `"VDD"` and `"VSS"` names are deliberately not parameterized: they are the
names the standard cells label their own rails with, so renaming them would break
the in-cell join that the whole scheme rests on.

## Pin labels

Port names come from **text objects on the `<metal>/251` pin layers**, and the
deck connects the whole stack — `19/251` through `90/251` — not just M1's. The M1
label layer `19/2` is empty in the shipped standard cells.

A standard cell only ever needs `19/251`; it labels its pins on M1 and nothing
else. A **block** is the opposite case: its ports are wherever its pin geometry
lands, which for a design that abuts hardened blocks is the upper metals. A tile
whose boundary pins sit on M4 and M5 loses every port name if only `19/251` is
read, and a block whose ports are *all* above M1 loses its pins outright.

This matters for correctness and not only for coverage, because **KLayout treats
unnamed pins as equivalent** while named pins must correspond exactly. An
abstract circuit (see [Black-boxing](#black-boxing)) whose pins went unnamed can
therefore be matched positionally and report a **false clean**. Measured on the
two-inverter M4-pinned article in `tests/test_asap7_klayout_lvs.py`: reading M1
labels alone, the top cell extracts **2 pins** (the rails) against the 6 its
netlist declares, and a netlist with its two inputs *exchanged* still compares
`MATCH`. With the stack connected it is correctly a `MISMATCH`.

## Verified coverage

Run against every subcircuit in the RVT standard-cell CDL
(`../../../../libs/asap7sc7p5t_rvt/netlist/asap7sc7p5t_28_R.cdl`), with spot
checks in LVT and SLVT and a purpose-built SRAM-VT article under
`tests/data/asap7_lvs/`:

**192 of 209 cells compare clean, with zero extraction errors.**

Hierarchy is covered separately: `tests/test_asap7_klayout_lvs.py` builds rows of
abutted instances at test time and compares them against a generated netlist, both
plainly and black-boxed, including negative cases (a miswired route must still be
reported, black-boxed or not).

Block-shaped use is covered by the M4-pinned article in the same file, which
carries its ports up a via stack to `40/0` and names them on `40/251`, as a
hardened block does. It asserts the port names reach the *layout* side of the
LVS database, and that exchanging two of those ports in the netlist is reported
as a mismatch. Note that the extracted `.cir` is no good for such an assertion:
KLayout's SPICE writer numbers pins rather than naming them, so even M1-labelled
rails appear there as `5` and `6`. Read the `.lvsdb` instead.

**Not covered here:** a real multi-block array. The tiered scheme in
[Block-level use](#block-level-use) is exercised only at the scale of rows and a
two-instance block article; the pin counts and runtimes it describes were
measured by a consumer, on designs that do not live in this repository.

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
practice. At block level, `blackbox` sidesteps it — the cell is reduced to its
pins, so its internal structure never enters the compare. Fixing it properly needs
a netlist post-process that pairs same-gate fingers across parallel chains.

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
