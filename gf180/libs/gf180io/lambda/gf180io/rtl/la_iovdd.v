module la_iovdd
  #(
    parameter TYPE = "DEFAULT" // cell type
    )
   (
    inout 	vdd, // core supply
    inout 	vss, // core ground
    inout 	vddio, // io supply
    inout 	vssio, // io ground
    inout [7:0] ioring // generic io-ring interface
    );

   gf180mcu_fd_io__dvdd
     iovdd (.DVDD(vddio),
	    .DVSS(vssio),
	    .VSS(vss));

endmodule
