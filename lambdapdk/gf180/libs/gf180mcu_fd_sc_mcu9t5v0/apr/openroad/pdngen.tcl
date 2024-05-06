####################################
# voltage domains
####################################
set_voltage_domain -name {CORE} -power {VDD} -ground {VSS}
####################################
# standard cell grid
####################################
define_pdn_grid -name {block} -voltage_domains {CORE}
add_pdn_stripe -grid {block} -layer {Metal1} -width {0.900} -pitch {5.040} -offset {0} -followpins

set metal4_pitch [expr {[lindex [ord::get_core_area] 2] - [lindex [ord::get_core_area] 0]}]
if {$metal4_pitch > 44.8} {
    set metal4_pitch 44.8
}
set metal5_pitch [expr {[lindex [ord::get_core_area] 3] - [lindex [ord::get_core_area] 1]}]
if {$metal5_pitch > 89.6} {
    set metal5_pitch 89.6
}

add_pdn_stripe -grid {block} -layer {Metal4} -width {4.480} -pitch $metal4_pitch \
    -offset [expr {$metal4_pitch / 2}]
add_pdn_stripe -grid {block} -layer {Metal5} -width {4.480} -pitch $metal5_pitch \
    -offset [expr {$metal5_pitch / 2}]
add_pdn_connect -grid {block} -layers {Metal1 Metal4} -max_columns {5} \
    -ongrid {Metal2 Metal3 Metal4}
add_pdn_connect -grid {block} -layers {Metal4 Metal5}
