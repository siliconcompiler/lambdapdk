####################################
# grid for: sky130sram
####################################
define_pdn_grid -name {sg13g2_sram} -voltage_domains {CORE} -macro \
    -orient {R0 R180 MX MY} \
    -halo {2.0 2.0 2.0 2.0} \
    -cells {RM_IHPSG13_1P_.*}
add_pdn_stripe -grid {sg13g2_sram} -layer {Metal5} -width {2.200} -pitch {22.0} -offset {11.0}
add_pdn_connect -grid {sg13g2_sram} -layers {Metal4 Metal5}
add_pdn_connect -grid {sg13g2_sram} -layers {Metal5 TopMetal1}
