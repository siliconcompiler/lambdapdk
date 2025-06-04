####################################
# grid for: fakeram45_rotated
####################################
define_pdn_grid -name {fakeram45} -voltage_domains {CORE} -macro \
    -orient {R0 R180 MX MY} \
    -halo {2.0 2.0 2.0 2.0} \
    -cells {fakeram45_.*}
add_pdn_stripe -grid {fakeram45} -layer {metal4} -width {0.93} -pitch {10.0} -offset {2}
add_pdn_stripe -grid {fakeram45} -layer {metal5} -width {0.93} -pitch {10.0} -offset {2}
add_pdn_stripe -grid {fakeram45} -layer {metal6} -width {0.93} -pitch {20.0} -offset {2}
add_pdn_connect -grid {fakeram45} -layers {metal3 metal4}
add_pdn_connect -grid {fakeram45} -layers {metal4 metal5}
add_pdn_connect -grid {fakeram45} -layers {metal5 metal6}
add_pdn_connect -grid {fakeram45} -layers {metal6 metal7}
