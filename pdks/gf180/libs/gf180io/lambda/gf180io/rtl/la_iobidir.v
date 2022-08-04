module la_iobidir
  #(
    parameter TYPE = "DEFAULT" // cell type
    )
   (// io pad signals
    inout 	 pad, // bidirectional pad signal
    inout 	 vdd, // core supply
    inout 	 vss, // core ground
    inout 	 vddio, // io supply
    inout 	 vssio, // io ground
    // core facing signals
    input 	 a, // input from core
    output 	 z, // output to core
    input 	 ie, // input enable, 1 = active
    input 	 oe, // output enable, 1 = active
    input 	 pe, // weak pull enable, 1 = active
    input 	 ps,// pull select, 1 = pull-up, 0 = pull-down
    input 	 sr, // slewrate enable 1 = fast, 0 = slow
    input [2:0]  ds, // drive strength, 3'b0 = weakest
    input 	 st, // schmitt trigger, 1 = enable
    inout [7:0]  ioring, // generic io-ring interface
    input [31:0] cfg // generic config interface
    );

   //TODO: implement cell type (with and without drive)

   // Cell Function
   // and #1 (Y, PAD, IE);
   // bufif1 #1 (PAD, A, OE);
   // rnmos #1 (PAD, gnd, ~OE && ~PU && PD);
   // rnmos #1 (PAD, pwr, ~OE && PU && ~PD);

   gf180mcu_fd_io__bi_t
     iovdd (.PAD(pad),
	    .A(a),
	    .Y(z),
	    .IE(ie),
	    .OE(oe),
	    .CS(st),
	    .PDRV0(ds[0]),
	    .PDRV1(ds[1]),
	    .PD(ioring[0]),
	    .PU(ioring[1]),
 	    .SL(ioring[2]),
	    .DVDD(vddio),
	    .DVSS(vssio),
	    .VDD(vdd),
	    .VSS(vss));

endmodule
