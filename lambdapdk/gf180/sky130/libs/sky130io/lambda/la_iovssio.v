module la_iovssio
  #(
    parameter TYPE  = "DEFAULT", // cell type
    parameter SIDE  = "NO",      // "NO", "SO", "EA", "WE"
    parameter RINGW =  8         // width of io ring
    )
   (
    inout 	      vdd, // core supply
    inout 	      vss, // core ground
    inout 	      vddio, // io supply
    inout 	      vssio, // io ground
    inout [RINGW-1:0] ioring // generic io-ring interface
    );

   sky130_ef_io__vssio_hvc_pad
     iovssio (
	      .VDDIO(vddio),
	      .VDDIO_Q(ioring[0]),
	      .VDDA(ioring[6]),
	      .VCCD(vdd),
	      .VSWITCH(ioring[1]),
	      .VCCHIB(ioring[2]),
	      .VSSA(ioring[7]),
	      .VSSD(vss),
	      .VSSIO_Q(ioring[3]),
	      .VSSIO(vssio),
	      .AMUXBUS_A(ioring[4]),
	      .AMUXBUS_B(ioring[5]));

endmodule
