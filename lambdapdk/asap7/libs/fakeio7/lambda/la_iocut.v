/*****************************************************************************
 * Function: Supply Ring Cut IO Cell
 * Copyright: Lambda Project Authors. All rights Reserved.
 * License:  MIT (see LICENSE file in Lambda repository)
 *
 * Docs:
 *
 * ../README.md
 *
 ****************************************************************************/
module la_iocut #(
    parameter PROP  = "DEFAULT",  // cell property
    parameter SIDE  = "NO",       // "NO", "SO", "EA", "WE"
    parameter RINGW = 8           // width of io ring
) (
    // ground never cut
    inout vss
);

  generate
    if (SIDE == "NO" | SIDE == "SO") begin : ivertical
      FAKEIO7_BREAKER_V i0 (
          .DVDDA(),
          .DVDDB(),
          .DVSSA(),
          .DVSSB(),
          .VDDA (),
          .VDDB (),
          .VSS  (vss),
          .RINGA(),
          .RINGB()
      );
    end // block: ivertical
      else
        begin: ihorizontal
      FAKEIO7_BREAKER_H i0 (
          .DVDDA(),
          .DVDDB(),
          .DVSSA(),
          .DVSSB(),
          .VDDA (),
          .VDDB (),
          .VSS  (vss),
          .RINGA(),
          .RINGB()
      );
    end  // block: ivertical
  endgenerate
endmodule
