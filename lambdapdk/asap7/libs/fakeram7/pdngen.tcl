####################################
# grid for: fameram7
####################################
define_pdn_grid -name {fameram7} -voltage_domains {CORE} \
    -macro \
    -halo {1.0 1.0 1.0 1.0} \
    -cells {fakeram7_.*}
add_pdn_connect -grid {fameram7} -layers {M4 M5}
