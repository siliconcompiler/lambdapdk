/*****************************************************************************
 * Function: XTAL Oscillator IO Cell
 * Copyright: Lambda Project Authors. All rights Reserved.
 * License:  MIT (see LICENSE file in Lambda repository)
 *
 * Docs:
 *
 * ../README.md
 *
 ****************************************************************************/
module la_ioxtal
  #(
    parameter PROP = "DEFAULT", // cell property
    parameter SIDE = "NO",      // "NO", "SO", "EA", "WE"
    parameter CFGW = 16,        // width of core config bus
    parameter RINGW = 8         // width of io ring
    )
   (// io pad signals
    inout             padi,   // xtal input pad
    inout             pado,   // xtal output pad
    inout             vdd,    // core supply
    inout             vss,    // core ground
    inout             vddio,  // io supply
    inout             vssio,  // io ground
    inout [RINGW-1:0] ioring, // generic ioring interface
    input [CFGW-1:0]  cfg,    // generic config interface
    // core interface
    output            z       // clock output to core
    );

   assign z = padi;

endmodule
