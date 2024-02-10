module la_iocorner
  #(
    parameter TYPE = "DEFAULT", // cell type
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

   gf180mcu_fd_io__cor
     iovss (.DVDD(vddio),
	    .DVSS(vssio),
	    .VDD(vdd),
	    .VSS(vss));

endmodule