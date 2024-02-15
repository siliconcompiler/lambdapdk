/*****************************************************************************
 * Function: IO bi-directional buffer
 * Copyright: Lambda Project Authors. ALl rights Reserved.
 * License:  MIT (see LICENSE file in Lambda repository)
 *
 * Docs:
 *
 * This is a generic cell that defines the standard interface of the lambda
 * bidrectional buffer cell. It is only suitable for FPGA synthesis.
 *
 * ASIC specific libraries will need to use the TYPE field to select an
 * appropriate hardcoded physical cell based on the the process constraints
 * and library composition. For example, modern nodes will usually have
 * different IP cells for the placing cells vvertically or horizontally.
 *
 ****************************************************************************/
module la_ioinput
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
    output 	      z, // output to core
    input 	      ie, // input enable, 1 = active
    inout [RINGW-1:0] ioring, // generic io-ring interface
    input [CFGW-1:0]  cfg // generic config interface
    );

   // to core
   assign z   = ie ? pad : 1'b0;

endmodule
