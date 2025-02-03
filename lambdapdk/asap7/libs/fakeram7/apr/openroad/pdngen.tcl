####################################
# grid for: fameram7
####################################
define_pdn_grid -name {fameram7} -voltage_domains {CORE} \
    -macro \
    -halo {1.0 1.0 1.0 1.0} \
    -cells {fakeram7_.*}
add_pdn_stripe -grid {fameram7} -layer M5 -width 0.12 -pitch 0.6
add_pdn_connect -grid {fameram7} -layers {M4 M5}
add_pdn_connect -grid {fameram7} -layers {M5 M6}
