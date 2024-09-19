####################################
# voltage domains
####################################
set_voltage_domain -name {CORE} -power {VDD} -ground {VSS}
#####################################
# standard cell grid
####################################
define_pdn_grid -name {grid} -voltage_domains {CORE}
add_pdn_stripe -grid {grid} -layer {Metal1} -width {0.44} -followpins
set met5_pitch [expr {([lindex [ord::get_core_area] 3] - [lindex [ord::get_core_area] 1]) / 2}]
if {$met5_pitch > 75.6} {
    set met5_pitch 75.6
}
add_pdn_stripe -grid {grid} -layer {Metal5} -width {2.200} -pitch $met5_pitch \
    -offset [expr {$met5_pitch / 2}]
set top1_pitch [expr {([lindex [ord::get_core_area] 2] - [lindex [ord::get_core_area] 0]) / 2}]
if {$top1_pitch > 75.6} {
    set top1_pitch 75.6
}
add_pdn_stripe -grid {grid} -layer {TopMetal1} -width {1.800} -pitch $met5_pitch \
    -offset [expr {$met5_pitch / 2}]
add_pdn_connect -grid {grid} -layers {Metal1 Metal5}
add_pdn_connect -grid {grid} -layers {Metal5 TopMetal1}
####################################
