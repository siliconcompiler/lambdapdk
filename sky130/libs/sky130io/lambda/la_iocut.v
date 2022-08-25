module la_iocut
  #(
    parameter TYPE  = "DEFAULT", // cell type
    parameter SIDE  = "NO",      // "NO", "SO", "EA", "WE"
    parameter RINGW =  8         // width of io ring
    )
   (
    // ground never cut
    inout 	      vss,
    // left side (viewed from center)
    inout 	      vddl, // core
    inout 	      vddiol, // io supply
    inout 	      vssiol, // left io ground
    inout [RINGW-1:0] ioringl, // left ioring
    // right side (viewed from center)
    inout 	      vddr, // core (from center)
    inout 	      vddior, // io supply
    inout 	      vssior, // left io ground
    inout [RINGW-1:0] ioringr // left ioring
    );

endmodule
