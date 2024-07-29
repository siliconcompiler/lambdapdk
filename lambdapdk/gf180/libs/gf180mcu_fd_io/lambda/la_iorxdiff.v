/*****************************************************************************
 * Function: Digital Differential Receiver IO Cell
 * Copyright: Lambda Project Authors. All rights Reserved.
 * License:  MIT (see LICENSE file in Lambda repository)
 *
 * Docs:
 *
 * ../README.md
 *
 ****************************************************************************/
module la_iorxdiff
  #(
    parameter PROP = "DEFAULT", // cell property
    parameter SIDE = "NO",      // "NO", "SO", "EA", "WE"
    parameter CFGW = 16,        // width of core config bus
    parameter RINGW = 8         // width of io ring
    )
   (// io pad signals
    inout             padp,   // differential pad input (positive)
    inout             padn,   // differential pad input (negative)
    inout             vdd,    // core supply
    inout             vss,    // core ground
    inout             vddio,  // io supply
    inout             vssio,  // io ground
    // core facing signals
    output            zp,     // digital output to core (positive)
    output            zn,     // digital output to core (negative)
    input             ie,     // input enable, 1 = active
    inout [RINGW-1:0] ioring, // generic ioring interface
    input [CFGW-1:0]  cfg     // generic config interface
    );

endmodule
