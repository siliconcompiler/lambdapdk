module la_ioanalog
  #(
    parameter TYPE = "DEFAULT" // cell type
    )
   (// io pad signals
    inout 	pad, // bidirectional pad signal
    inout 	vdd, // core supply
    inout 	vss, // core ground
    inout 	vddio, // io supply
    inout 	vssio, // io ground
    inout [7:0] ioring // generic io-ring interface
    );

   gf180mcu_fd_io__asig_5p0
     iovdd (.ASIG5V(pad),
	    .DVDD(vddio),
	    .DVSS(vssio),
	    .VDD(vdd),
	    .VSS(vss));

endmodule
