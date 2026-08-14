####################################
# voltage domains
####################################
set_voltage_domain -name {CORE} -power {VDD} -ground {VSS}
####################################
# standard cell grid
####################################
define_pdn_grid -name {grid} -voltage_domains {CORE} -pins {Metal3}
add_pdn_stripe -grid {grid} -layer {Metal1} -width {0.600} -pitch {3.92} -offset {0} -followpins

set metal3_pitch [expr {([lindex [ord::get_core_area] 3] - [lindex [ord::get_core_area] 1]) / 2}]
if {$metal3_pitch > 89.6} {
    set metal3_pitch 89.6
}

proc snap_grid {value} {
    set grid [[ord::get_db_tech] getManufacturingGrid]
    set dbus [[ord::get_db_tech] getDbUnitsPerMicron]

    set val_dbus [ord::microns_to_dbu $value]
    set val_snapped [expr {$grid * round($val_dbus / $grid)}]

    return [ord::dbu_to_microns $val_snapped]
}

add_pdn_stripe -grid {grid} -layer {Metal3} -width {1.600} -pitch [snap_grid $metal3_pitch] \
    -offset [snap_grid [expr {$metal3_pitch / 4}]]
add_pdn_connect -grid {grid} -layers {Metal1 Metal3}
