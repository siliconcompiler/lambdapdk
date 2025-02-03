####################################
# grid for: sky130sram
####################################
define_pdn_grid -name {sky130sram} -voltage_domains {CORE} -macro \
    -orient {R0 R180 MX MY} \
    -halo {2.0 2.0 2.0 2.0} \
    -cells {sky130_sram_1rw1r_.*}
add_pdn_connect -grid {sky130sram} -layers {met3 met4}
