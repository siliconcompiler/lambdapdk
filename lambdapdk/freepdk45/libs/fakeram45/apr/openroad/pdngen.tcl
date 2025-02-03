####################################
# grid for: fakeram45_rotated
####################################
define_pdn_grid -name {fakeram45} -voltage_domains {CORE} -macro \
    -orient {R0 R180 MX MY} \
    -halo {2.0 2.0 2.0 2.0} \
    -cells {fakeram45_.*}
add_pdn_stripe -grid {fakeram45} -layer {metal5} -width {0.93} -pitch {10.0} -offset {2}
add_pdn_stripe -grid {fakeram45} -layer {metal6} -width {0.93} -pitch {10.0} -offset {2}
add_pdn_connect -grid {fakeram45} -layers {metal4 metal5}
add_pdn_connect -grid {fakeram45} -layers {metal5 metal6}
add_pdn_connect -grid {fakeram45} -layers {metal6 metal7}
####################################
# grid for: fakeram45_rotated
####################################
define_pdn_grid -name {fakeram45_rotated} -voltage_domains {CORE} -macro \
    -orient {R90 R270 MXR90 MYR90} \
    -halo {2.0 2.0 2.0 2.0} \
    -cells {fakeram45_.*}
add_pdn_stripe -grid {fakeram45_rotated} -layer {metal6} -width {0.93} -pitch {40.0} -offset {2}
add_pdn_connect -grid {fakeram45_rotated} -layers {metal4 metal6}
add_pdn_connect -grid {fakeram45_rotated} -layers {metal6 metal7}
