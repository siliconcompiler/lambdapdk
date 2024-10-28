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

  sky130_ef_io__gpiov2_pad_wrapped gpio (
      .VDDIO(vddio),
      .VCCD(vdd),
      .VSSD(vss),
      .VSSIO(vssio),
      .VDDIO_Q(ioring[0]),
      .VSWITCH(ioring[1]),
      .VCCHIB(ioring[2]),
      .VSSIO_Q(ioring[3]),
      .AMUXBUS_A(ioring[4]),
      .AMUXBUS_B(ioring[5]),
      .VDDA(ioring[6]),
      .VSSA(ioring[7]),

      .IN(z),
      .OUT(a),
      .OE_N(~oe),
      .INP_DIS(ie),  // disable input when ie low
      .PAD(pad),

      .HLD_H_N(cfg[0]),  // if 0, hold outputs at current state
      .ENABLE_H(cfg[1]),  // if 0, hold outputs at hi-z (used on power-up)
      .ENABLE_INP_H(cfg[2]),  // val doesn't matter when enable_h = 1
      .ENABLE_VDDA_H(cfg[3]),
      .ENABLE_VSWITCH_H(cfg[4]),
      .ENABLE_VDDIO(cfg[5]),
      .IB_MODE_SEL(cfg[6]),  // use vddio based threshold
      .VTRIP_SEL(cfg[7]),  // use cmos threshold
      .SLOW(cfg[8]),
      .HLD_OVR(cfg[9]),  // don't care when hld_h_n = 1
      .ANALOG_EN(cfg[10]),  // disable analog functionality
      .ANALOG_SEL(cfg[11]),  // don't care
      .ANALOG_POL(cfg[12]),  // don't care
      .DM(cfg[15:13]),  // strong pull-up, strong pull-down

      // unused
      .PAD_A_NOESD_H(),
      .PAD_A_ESD_0_H(),
      .PAD_A_ESD_1_H(),
      .IN_H(),
      .TIE_HI_ESD(),
      .TIE_LO_ESD()
  );

endmodule
