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
add_pdn_stripe -grid {stdcells} -layer {M5} -width {0.12} -spacing {0.072} -pitch {5.904} -offset {0.300} -snap_to_grid
add_pdn_stripe -grid {stdcells} -layer {M6} -width {0.288} -spacing {0.096} -pitch {6.0} -offset {0.513} -snap_to_grid
add_pdn_stripe -grid {stdcells} -layer {M7} -width {0.288} -spacing {2.5} -pitch {10.0} -offset {5.0} -snap_to_grid
add_pdn_connect -grid {stdcells} -layers {M1 M2}
add_pdn_connect -grid {stdcells} -layers {M2 M5}
add_pdn_connect -grid {stdcells} -layers {M5 M6}
add_pdn_connect -grid {stdcells} -layers {M6 M7}
