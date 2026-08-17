####################################
# voltage domains
####################################
set_voltage_domain -name {CORE} -power {VDD} -ground {VSS}

####################################
# standard cell grid
####################################
define_pdn_grid -name {grid} -voltage_domains {CORE} -pins {MET5}

# MET1 rails: the cells carry 0.16um wide VDD/VSS abutment pins on MET1.
add_pdn_stripe -grid {grid} -layer {MET1} -width {0.16} -followpins

# MET4 (vertical) and MET5 (horizontal) mesh. The pitch follows the core so that
# small designs still see straps, capped so that large ones do not turn into a
# wall of metal.
set met4_pitch [expr {([lindex [ord::get_core_area] 2] - [lindex [ord::get_core_area] 0]) / 2}]
if {$met4_pitch > 20.0} {
    set met4_pitch 20.0
}
set met5_pitch [expr {([lindex [ord::get_core_area] 3] - [lindex [ord::get_core_area] 1]) / 2}]
if {$met5_pitch > 20.0} {
    set met5_pitch 20.0
}

proc snap_grid {value} {
    set grid [[ord::get_db_tech] getManufacturingGrid]

    set val_dbus [ord::microns_to_dbu $value]
    set val_snapped [expr {$grid * round($val_dbus / $grid)}]

    return [ord::dbu_to_microns $val_snapped]
}

add_pdn_stripe -grid {grid} -layer {MET4} -width {0.40} -spacing {0.40} \
    -pitch [snap_grid $met4_pitch] -offset [snap_grid [expr {$met4_pitch / 2}]]
add_pdn_stripe -grid {grid} -layer {MET5} -width {0.60} -spacing {0.60} \
    -pitch [snap_grid $met5_pitch] -offset [snap_grid [expr {$met5_pitch / 2}]]

add_pdn_connect -grid {grid} -layers {MET1 MET4}
add_pdn_connect -grid {grid} -layers {MET4 MET5}
