module la_iofill
  #(parameter TYPE = "DEFAULT", // cell type
    parameter SIDE  = "NO",      // "NO", "SO", "EA", "WE"
    parameter RINGW =  8         // width of io ring
    )
   (
    inout 	vdd, // core supply
    inout 	vss, // core ground
    inout 	vddio, // io supply
    inout 	vssio, // io ground
    inout [RINGW-1:0] ioring // generic io-ring interface
    );

   // TODO: Use type to select fill size
   gf180mcu_fd_io__fill1
     iovdd (.DVDD(vddio),
	    .DVSS(vssio),
	    .VDD(vdd),
	    .VSS(vss));

endmodule
