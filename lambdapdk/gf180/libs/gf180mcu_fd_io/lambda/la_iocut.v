module la_iocut #(
    parameter PROP  = "DEFAULT",  // cell type
    parameter SIDE  = "NO",       // "NO", "SO", "EA", "WE"
    parameter RINGW = 8           // width of io ring
) (
    // ground never cut
    inout             vss,
    // left side (viewed from center)
    inout             vdd0,     // core
    inout             vddio0,   // io supply
    inout             vssio0,   // left io ground
    inout [RINGW-1:0] ioring0,  // left ioring
    // right side (viewed from center)
    inout             vdd1,     // core (from center)
    inout             vddio1,   // io supply
    inout             vssio1,   // left io ground
    inout [RINGW-1:0] ioring1   // left ioring
);


  //TODO: select cut cell based on type
  gf180mcu_fd_io__brk2 iocut (.VSS(vss));

endmodule
