module la_iobidir
  #(
    parameter TYPE  = "DEFAULT", // cell type
    parameter SIDE  = "NO",      // "NO", "SO", "EA", "WE"
    parameter CFGW  =  16,       // width of core config bus
    parameter RINGW =  8         // width of io ring
    )
   (// io pad signals
    inout 	      pad, // bidirectional pad signal
    inout 	      vdd, // core supply
    inout 	      vss, // core ground
    inout 	      vddio, // io supply
    inout 	      vssio, // io ground
    // core facing signals
    input 	      a, // input from core
    output 	      z, // output to core
    input 	      ie, // input enable, 1 = active
    input 	      oe, // output enable, 1 = active
    input 	      pe, // weak pull enable, 1 = active
    input 	      ps,// pull select, 1 = pull-up, 0 = pull-down
    input 	      sr, // slewrate enable 1 = fast, 0 = slow
    input [2:0]       ds, // drive strength, 3'b0 = weakest
    input 	      st, // schmitt trigger, 1 = enable
    inout [RINGW-1:0] ioring, // generic io-ring interface
    input [CFGW-1:0]  cfg // generic config interface inout [RINGW-1:0] ioring,
    );

   // TODO: hook up IO buffer config
   //#  0    = pull_enable (1=enable)
   //#  1    = pull_select (1=pull up)
   //#  2    = slew limiter
   //#  3    = shmitt trigger enable
   //#  4    = ds[0]
   //#  5    = ds[1]
   //#  6    = ds[2]
   //#  7    = ds[3]

   // TODO: should do something with poc signal? maybe this has to do with
   // power-on ramp pins such as enable_h

   // TODO: might need to use "tielo"/"tiehi" signals for some of these instead of
   // 0/1 constants -- see https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/blob/master/flow/designs/sky130hd/coyote_tc/ios.v

   sky130_ef_io__gpiov2_pad_wrapped
     gpio (
	   .IN(z),
	   .OUT(a),
	   .OE_N(oe),
	   .INP_DIS(ie), // disable input when ie low
	   .PAD(pad),
	   .HLD_H_N(cfg[0]), // if 0, hold outputs at current state
	   .ENABLE_H(cfg[1]), // if 0, hold outputs at hi-z (used on power-up)
	   .ENABLE_INP_H(cfg[2]), // val doesn't matter when enable_h = 1
	   .ENABLE_VDDA_H(cfg[3]),
	   .ENABLE_VSWITCH_H(cfg[4]),
	   .ENABLE_VDDIO(cfg[5]),
	   .IB_MODE_SEL(cfg[6]), // use vddio based threshold
	   .VTRIP_SEL(cfg[7]), // use cmos threshold
	   .SLOW(cfg[8]),
	   .HLD_OVR(cfg[9]), // don't care when hld_h_n = 1
	   .ANALOG_EN(cfg[10]), // disable analog functionality
	   .ANALOG_SEL(cfg[11]), // don't care
	   .ANALOG_POL(cfg[12]), // don't care
	   .DM(cfg[15:13]), // strong pull-up, strong pull-down
	   .VDDIO(vddio),
	   .VDDIO_Q(ioring[0]), // level-shift reference for high-voltage output
	   .VDDA(ioring[6]),
	   .VCCD(vdd), // core supply as level-shift reference
	   .VSWITCH(ioring[1]), // not sure what this is for, but seems like vdda = vddio
	   .VCCHIB(ioring[2]),
	   .VSSA(ioring[7]),
	   .VSSD(vss),
	   .VSSIO_Q(ioring[3]),
	   .VSSIO(vssio),
	   // Direction connection from pad to core (unused)
	   .PAD_A_NOESD_H(),
	   .PAD_A_ESD_0_H(),
	   .PAD_A_ESD_1_H(),
	   // Analog stuff (unused)
	   .AMUXBUS_A(ioring[4]),
	   .AMUXBUS_B(ioring[5]),
	   // not sure what this output does, so leave disconnected
	   .IN_H(),
	   // these are used to control enable_inp_h, but we don't care about its val
	   // so leave disconnected
	   .TIE_HI_ESD(),
	   .TIE_LO_ESD()
	   );

endmodule
