(* keep_hierarchy *)
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
    input              schmitt, // schmitt cfg, 1 = active
    input              fast,    // 1 = fast slew rate
    input  [1:0]       ds,      // drive strength, 0=weakest
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
      .CS(schmitt),
      .PDRV0(ds[0]),
      .PDRV1(ds[1]),
      .PD(ps & ~ps),
      .PU(ps & ps),
      .SL(fast),
      .DVDD(vddio),
      .DVSS(vssio),
      .VDD(vdd),
      .VSS(vss)
  );

endmodule
