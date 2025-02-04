####################################
# grid for: sky130sram
####################################
define_pdn_grid -name {sg13g2_sram_R0} -voltage_domains {CORE} -macro \
    -orient {R0 MX MY} \
    -halo {1.0 1.0 1.0 1.0} \
    -cells {RM_IHPSG13_1P_.*}
add_pdn_stripe -grid {sg13g2_sram_R0} -layer {TopMetal1} -width {2.000} -pitch {20.0} -offset {1.0}
add_pdn_connect -grid {sg13g2_sram_R0} -layers {Metal4 TopMetal1}
add_pdn_connect -grid {sg13g2_sram_R0} -layers {TopMetal1 TopMetal2}

define_pdn_grid -name {sg13g2_sram_R180} -voltage_domains {CORE} -macro \
    -orient {R180} \
    -halo {1.0 1.0 1.0 1.0} \
    -cells {RM_IHPSG13_1P_.*}
add_pdn_stripe -grid {sg13g2_sram_R180} -layer {Metal5} -width {2.200} -pitch {22.0} -offset {11.0}
add_pdn_connect -grid {sg13g2_sram_R180} -layers {Metal4 Metal5}
add_pdn_connect -grid {sg13g2_sram_R180} -layers {Metal5 TopMetal1}
add_pdn_connect -grid {sg13g2_sram_R180} -layers {TopMetal1 TopMetal2}
