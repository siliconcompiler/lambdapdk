####################################
# grid for: sg13g2_sram_R0
####################################
define_pdn_grid -name {sg13g2_sram_R0} -voltage_domains {CORE} -macro \
    -orient {R0 R180 MX MY} \
    -halo {1.0 1.0 1.0 1.0} \
    -cells {RM_IHPSG13_1P_.*}
add_pdn_stripe -grid {sg13g2_sram_R0} -layer {Metal5} -width {2.200} -pitch {20.0} -offset {1.0}
add_pdn_connect -grid {sg13g2_sram_R0} -layers {Metal4 Metal5}
add_pdn_connect -grid {sg13g2_sram_R0} -layers {Metal5 TopMetal1}

####################################
# grid for: sg13g2_sram_R90
####################################
define_pdn_grid -name {sg13g2_sram_R90} -voltage_domains {CORE} -macro \
    -orient {R90 R270 MXR90 MYR90} \
    -halo {1.0 1.0 1.0 1.0} \
    -cells {RM_IHPSG13_1P_.*}
add_pdn_stripe -grid {sg13g2_sram_R90} -layer {TopMetal1} -width {2.000} -pitch {22.0} \
    -offset {11.0}
add_pdn_connect -grid {sg13g2_sram_R90} -layers {Metal4 TopMetal1}
add_pdn_connect -grid {sg13g2_sram_R90} -layers {TopMetal1 TopMetal2}
