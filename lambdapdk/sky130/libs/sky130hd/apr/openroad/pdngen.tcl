####################################
# voltage domains
####################################
set_voltage_domain -name {CORE} -power {VDD} -ground {VSS}
####################################
# standard cell grid
####################################
define_pdn_grid -name {grid} -voltage_domains {CORE}
add_pdn_stripe -grid {grid} -layer {met1} -width {0.48} -pitch {5.44} -offset {0} -followpins
set met4_pitch [expr {([lindex [ord::get_core_area] 2] - [lindex [ord::get_core_area] 0]) / 2}]
if {$met4_pitch > 27.140} {
    set met4_pitch 27.140
}
set met5_pitch [expr {([lindex [ord::get_core_area] 3] - [lindex [ord::get_core_area] 1]) / 2}]
if {$met5_pitch > 27.200} {
    set met5_pitch 27.200
}
add_pdn_stripe -grid {grid} -layer {met4} -width {1.600} -pitch $met4_pitch \
    -offset [expr {$met4_pitch / 4}]
add_pdn_stripe -grid {grid} -layer {met5} -width {1.600} -pitch $met5_pitch \
    -offset [expr {$met5_pitch / 4}]
add_pdn_connect -grid {grid} -layers {met1 met4}
add_pdn_connect -grid {grid} -layers {met4 met5}
