####################################
# grid for: sky130sram
####################################
define_pdn_grid -name {sky130sram} -voltage_domains {CORE} -macro \
    -orient {R0 R180 MX MY} \
    -halo {1.0 1.0 1.0 1.0} \
    -cells {sky130_sram_2kbyte_1rw1r_.*}
# The macro brings its supplies out as rings: met3 along the top and bottom,
# met4 up the sides. The core grid runs met4 vertically and met5 horizontally,
# so both pairs are needed -- met3/met4 catches the horizontal rings under the
# core's met4 stripes, met4/met5 the vertical rings under its met5 stripes.
add_pdn_connect -grid {sky130sram} -layers {met3 met4}
add_pdn_connect -grid {sky130sram} -layers {met4 met5}
