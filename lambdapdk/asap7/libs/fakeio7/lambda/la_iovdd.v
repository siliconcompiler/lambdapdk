/*****************************************************************************
 * Function: Core Supply IO Cell
 * Copyright: Lambda Project Authors. All rights Reserved.
 * License:  MIT (see LICENSE file in Lambda repository)
 *
 * Docs:
 *
 * ../README.md
 *
 ****************************************************************************/
module la_iovdd #(
    parameter PROP  = "DEFAULT",  // cell property
    parameter SIDE  = "NO",       // "NO", "SO", "EA", "WE"
    parameter RINGW = 8           // width of io ring
) (
    inout             vdd,    // core supply
    inout             vss,    // core ground
    inout             vddio,  // io supply
    inout             vssio,  // io ground
    inout [RINGW-1:0] ioring  // generic ioring interface
);

  generate
    if (SIDE == "NO" | SIDE == "SO") begin : ivertical
      FAKEIO7_VDD_V i0 (
          .DVDD(vddio),
          .DVSS(vssio),
          .VDD (vdd),
          .VSS (vss),
          .RING(ioring)
      );
    end else begin : ihorizontal
      FAKEIO7_VDD_H i0 (
          .DVDD(vddio),
          .DVSS(vssio),
          .VDD (vdd),
          .VSS (vss),
          .RING(ioring)
      );
    end
  endgenerate

endmodule
