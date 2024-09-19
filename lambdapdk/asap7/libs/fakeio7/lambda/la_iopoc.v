/*****************************************************************************
 * Function: Power-On Control IO Cell
 * Copyright: Lambda Project Authors. All rights Reserved.
 * License:  MIT (see LICENSE file in Lambda repository)
 *
 * Docs:
 *
 * ../README.md
 *
 ****************************************************************************/
module la_iopoc #(
    parameter PROP  = "DEFAULT",  // cell property
    parameter SIDE  = "NO",       // "NO", "SO", "EA", "WE"
    parameter CFGW = 16,        // width of core config bus
    parameter RINGW = 8           // width of io ring
) (
    inout             vdd,    // core supply
    inout             vss,    // core ground
    inout             vddio,  // io supply
    inout             vssio,  // io ground
    inout [RINGW-1:0] ioring, // generic ioring interface
    input [CFGW-1:0]  cfg    // generic config interface
);

  generate
    if (SIDE == "NO" | SIDE == "SO") begin : ivertical
      FAKEIO7_POC_V i0 (
          .MODE(1'b1),
          //supplies
          .DVDD(vddio),
          .DVSS(vssio),
          .VDD (vdd),
          .VSS (vss),
          // ring signals
          .RING(ioring)
      );
    end else begin : ihorizontal
      FAKEIO7_POC_H i0 (
          .MODE(1'b1),
          //supplies
          .DVDD(vddio),
          .DVSS(vssio),
          .VDD (vdd),
          .VSS (vss),
          // ring signals
          .RING(ioring)
      );
    end
  endgenerate

endmodule
