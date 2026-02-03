/*****************************************************************************
 * Function: Corner IO Cell
 * Copyright: Lambda Project Authors. All rights Reserved.
 * License:  MIT (see LICENSE file in Lambda repository)
 *
 * Docs:
 *
 * ../README.md
 *
 ****************************************************************************/
(* keep_hierarchy *)
module la_iocorner #(
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

  FAKEIO7_CORNER i0 (
      .DVDD(vddio),
      .DVSS(vssio),
      .VDD (vdd),
      .VSS (vss),
      .RING(ioring)
  );

endmodule
