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
    inout  [RINGW-1:0] ioring,  // generic io ring
    input  [ CFGW-1:0] cfg      // generic config interface
);

  //TODO: implement cell type (with and without drive)

  // Cell Function
  // and #1 (Y, PAD, IE);
  // bufif1 #1 (PAD, A, OE);
  // rnmos #1 (PAD, gnd, ~OE && ~PU && PD);
  // rnmos #1 (PAD, pwr, ~OE && PU && ~PD);

  gf180mcu_fd_io__bi_t gpio (
      .PAD(pad),
      .A(a),
      .Y(z),
      .IE(ie),
      .OE(oe),
      .CS(cfg[2]),
      .PDRV0(cfg[0]),
      .PDRV1(cfg[1]),
      .PD(cfg[3]),
      .PU(cfg[4]),
      .SL(cfg[5]),
      .DVDD(vddio),
      .DVSS(vssio),
      .VDD(vdd),
      .VSS(vss)
  );

endmodule
