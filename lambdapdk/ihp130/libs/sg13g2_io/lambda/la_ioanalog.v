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

  sg13g2_IOPadAnalog ioanalog (
      .padres(aio[0]),
      .iovdd(vddio),
      .iovss(vssio),
      .vdd(vdd),
      .vss(vss)
  );

endmodule
