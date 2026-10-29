####################################
# grid for: sky130sram
####################################
define_pdn_grid -name {sky130sram} -voltage_domains {CORE} -macro \
    -orient {R0 R180 MX MY} \
    -halo {1.0 1.0 1.0 1.0} \
    -cells {sky130_sram_.*}
# Every macro in sky130_sram_macros brings its supplies out the same way --
# rings on met3 along the top and bottom, met4 up the sides -- so one grid
# covers all of them, and the pattern has to stay wide enough to match all of
# them. Naming only the 2kbyte part leaves a 1kbyte macro with no grid and its
# supplies unconnected, which fails the power_grid step.
#
# The core grid runs met4 vertically and met5 horizontally, so both connect
# pairs are needed -- met3/met4 catches the horizontal rings under the core's
# met4 stripes, met4/met5 the vertical rings under its met5 stripes.
add_pdn_connect -grid {sky130sram} -layers {met3 met4}
add_pdn_connect -grid {sky130sram} -layers {met4 met5}
