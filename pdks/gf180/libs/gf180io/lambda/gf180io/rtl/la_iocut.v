module la_iocut
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


   //TODO: selecct cut cell based on type
   gf180mcu_fd_io__brk2
     iocut (.VSS(vss));

endmodule
