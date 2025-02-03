####################################
# global connections
####################################
add_global_connection -net {VDD} -pin_pattern {VPWR} -power
add_global_connection -net {VDD} -pin_pattern {VPB}
add_global_connection -net {VSS} -pin_pattern {VGND} -ground
add_global_connection -net {VSS} -pin_pattern {VNB}
