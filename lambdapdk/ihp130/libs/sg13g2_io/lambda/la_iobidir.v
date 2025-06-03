module la_iobidir #(
    parameter PROP  = "DEFAULT",  // cell type
    parameter SIDE  = "NO",       // "NO", "SO", "EA", "WE"
    parameter CFGW  = 16,         // width of core config bus
    parameter RINGW = 8           // width of io ring
) (  // io pad signals
    inout              pad,     // bidirectional pad signal
    inout              vdd,     // core supply
    inout              vss,     // core ground
    inout              vddio,   // io supply
    inout              vssio,   // io ground
    // core facing signals
    input              a,       // input from core
    output             z,       // output to core
    input              ie,      // input enable, 1 = active
    input              oe,      // output enable, 1 = active
    input              pe,      // pull enable, 1 = enable
    input              ps,      // pull select, 1 = pullup, 0 = pulldown
    inout  [RINGW-1:0] ioring,  // generic io ring
    input  [ CFGW-1:0] cfg      // generic config interface
);

  //TODO: implement cell type (with and without drive)

  sg13g2_IOPadInOut30mA gpio (
      .pad(pad),
      .c2p(a),
      .p2c(z),
      .c2p_en(oe),
      .iovdd(vddio),
      .iovss(vssio),
      .vdd(vdd),
      .vss(vss)
  );

endmodule
