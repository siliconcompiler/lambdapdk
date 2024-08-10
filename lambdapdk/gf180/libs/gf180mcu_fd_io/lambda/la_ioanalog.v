module la_ioanalog #(
    parameter PROP  = "DEFAULT",  // cell type
    parameter SIDE  = "NO",       // "NO", "SO", "EA", "WE"
    parameter RINGW = 8           // width of io ring
) (  // io pad signals
    inout             pad,     // bidirectional pad signal
    inout             vdd,     // core supply
    inout             vss,     // core ground
    inout             vddio,   // io supply
    inout             vssio,   // io ground
    inout [RINGW-1:0] ioring,  // generic io-ring interface
    // core interface
    inout [      2:0] aio      // analog core signal
);

  gf180mcu_fd_io__asig_5p0 ioanalog (
      .ASIG5V(aio[0]),
      .DVDD(vddio),
      .DVSS(vssio),
      .VDD(vdd),
      .VSS(vss)
  );

endmodule
