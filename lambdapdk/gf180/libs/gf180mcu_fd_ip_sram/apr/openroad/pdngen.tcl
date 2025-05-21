####################################
# grid for: gf180mcu_fd_ip_sram
####################################
define_pdn_grid -name {gf180mcu_fd_ip_sram} -voltage_domains {CORE} -macro \
    -orient {R0 R180 MX MY} \
    -halo {2.0 2.0 2.0 2.0} \
    -cells {gf180mcu_fd_ip_sram.*}
add_pdn_connect -grid {gf180mcu_fd_ip_sram} -layers {Metal3 Metal4}
