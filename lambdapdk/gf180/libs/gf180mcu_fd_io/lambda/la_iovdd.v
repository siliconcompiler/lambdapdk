module la_iovdd #(
    parameter PROP  = "DEFAULT",  // cell type
    parameter SIDE  = "NO",       // "NO", "SO", "EA", "WE"
    parameter RINGW = 8           // width of io ring
) (
    inout vdd,  // core supply
    inout vss,  // core ground
    inout vddio,  // io supply
    inout vssio,  // io ground
    inout [RINGW-1:0] ioring  // generic io-ring interface
);

  gf180mcu_fd_io__dvdd iovdd (
      .DVDD(vddio),
      .DVSS(vssio),
      .VSS (vss)
  );

endmodule
