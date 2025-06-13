####################################
# voltage domains
####################################
set_voltage_domain -name {CORE} -power {VDD} -ground {VSS}
####################################
# standard cell grid
####################################
define_pdn_grid -name {stdcells} -voltage_domains {CORE} -pins {M7}
add_pdn_stripe -grid {stdcells} -layer {M1} -width {0.018} -pitch {0.54} -offset {0} -followpins
add_pdn_stripe -grid {stdcells} -layer {M2} -width {0.018} -pitch {0.54} -offset {0} -followpins
add_pdn_stripe -grid {stdcells} -layer {M5} -width {0.12} -spacing {0.072} -pitch {5.904} \
    -offset {0.300} -snap_to_grid
add_pdn_stripe -grid {stdcells} -layer {M6} -width {0.288} -spacing {0.096} -pitch {6.0} \
    -offset {0.513} -snap_to_grid

set M7_pitch [expr {([lindex [ord::get_core_area] 2] - [lindex [ord::get_core_area] 0]) / 2}]
if {$M7_pitch > 10.0} {
    set M7_pitch 10.0
}

proc snap_grid {value} {
    set grid [[ord::get_db_tech] getManufacturingGrid]
    set dbus [[ord::get_db_tech] getDbUnitsPerMicron]

    set val_dbus [ord::microns_to_dbu $value]
    set val_snapped [expr {$grid * round($val_dbus / $grid)}]

    return [ord::dbu_to_microns $val_snapped]
}

add_pdn_stripe -grid {stdcells} -layer {M7} -width {0.288} -pitch [snap_grid $metal4_pitch] \
    -offset [snap_grid [expr {$metal4_pitch / 4}]] -snap_to_grid

add_pdn_connect -grid {stdcells} -layers {M1 M2}
add_pdn_connect -grid {stdcells} -layers {M2 M5}
add_pdn_connect -grid {stdcells} -layers {M5 M6}
add_pdn_connect -grid {stdcells} -layers {M6 M7}
