This is the initial release for the ICsprout55 PDK with 747 standard cells in each of three
threshold voltages (`ics55_stdcell_h`, `ics55_stdcell_r`, `ics55_stdcell_l`), on a 7-track 1.4um
`core7` site. It is based on a 55nm bulk CMOS process from ICsprout Integrated Circuit Co., Ltd.,
released with the ECOS team at the Institute of Computing Technology, Chinese Academy of Sciences.

https://github.com/openecos-projects/icsprout55-pdk

Notes:
* Nothing from the PDK is vendored: tech LEF, cell LEF, CDL and Verilog are fetched from the
  repository archive, liberty and GDS from the matching release assets.
* The libraries use the `_ecos` LEF with the `_M2` GDS. The unsuffixed LEF puts every signal pin on
  MET1 in shapes too small for any VIA1 in the tech LEF, leaving 50 pins across 49 cells with no
  access point; `_ecos` adds the MET2 pad and VIA1 that the `_M2` stream carries.
* `base/setup/klayout/icsprout55.lyt` supplies the layer map the PDK does not ship, recovered from
  the released GDS. Drawing geometry is on datatype 1, and MET2/VIA1 are 82/91 rather than the
  intuitive reverse — see the header of the `.lyt`.
* Routing tracks come from the tech LEF, which declares `OFFSET 0` while the cells are drawn on a
  half-pitch grid. Routing completes either way; a half-pitch `make_tracks` override buys about 17%
  fewer vias on a small design.
* The `ss_cworst_1p08_m40` corner is unused — its deck is short cells the other six carry.
* 28 sequential cells have LEF and GDS but no liberty, and 13 liberty cells have no Verilog model.
* Wire capacitance is estimated; the PDK publishes no capacitance data and no OpenRCX deck.
* No DRC deck, LVS deck, SRAM macros or antenna rules are published upstream; the IO library is not
  wired up yet.
