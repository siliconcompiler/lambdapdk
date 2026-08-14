####################################
# voltage domains
####################################
set_voltage_domain -name {CORE} -power {VDD} -ground {VSS}
####################################
# standard cell grid
####################################
define_pdn_grid -name {grid} -voltage_domains {CORE} -pins {Metal4}
add_pdn_stripe -grid {grid} -layer {Metal1} -width {0.600} -pitch {3.92} -offset {0} -followpins

set metal4_pitch [expr {([lindex [ord::get_core_area] 2] - [lindex [ord::get_core_area] 0]) / 2}]
if {$metal4_pitch > 44.8} {
    set metal4_pitch 44.8
}

proc snap_grid {value} {
    set grid [[ord::get_db_tech] getManufacturingGrid]
    set dbus [[ord::get_db_tech] getDbUnitsPerMicron]

    set val_dbus [ord::microns_to_dbu $value]
    set val_snapped [expr {$grid * round($val_dbus / $grid)}]

    return [ord::dbu_to_microns $val_snapped]
}

add_pdn_stripe -grid {grid} -layer {Metal4} -width {1.600} -pitch [snap_grid $metal4_pitch] \
    -offset [snap_grid [expr {$metal4_pitch / 4}]]
add_pdn_connect -grid {grid} -layers {Metal1 Metal4}
