/*****************************************************************************
 * Function: IO Supply Cut IO Cell (propagates vss, vdd, and ioring)
 * Copyright: Lambda Project Authors. All rights Reserved.
 * License:  MIT (see LICENSE file in Lambda repository)
 *
 * Docs:
 *
 * ../README.md
 *
 ****************************************************************************/
(* keep_hierarchy *)
module la_iocutvddio #(
    parameter PROP  = "DEFAULT",  // cell property
    parameter SIDE  = "NO",       // "NO", "SO", "EA", "WE"
    parameter RINGW = 8           // width of io ring
) (
    // shorted signals
    inout             vss,     // core ground
    inout             vdd,     // core vdd
    inout [RINGW-1:0] ioring,  // io control ring
    // cut signals
    inout             vddio0,  // io/analog supply from section before
    inout             vddio1,  // io/analog supply from next section
    inout             vssio0,  // io/analog ground from section before
    inout             vssio1   // io/analog ground from next section
);

  generate
    if (SIDE == "NO" | SIDE == "SO") begin : ivertical
      FAKEIO7_BREAKER_IO_V i0 (
          .DVDDA(vddio0),
          .DVDDB(vddio1),
          .DVSSA(vssio0),
          .DVSSB(vssio1),
          .VDD  (vdd),
          .VSS  (vss),
          .RING (ioring)
      );
    end else begin : ihorizontal
      FAKEIO7_BREAKER_IO_H i0 (
          .DVDDA(vddio1),
          .DVDDB(vddio0),
          .DVSSA(vssio1),
          .DVSSB(vssio0),
          .VDD  (vdd),
          .VSS  (vss),
          .RING (ioring)
      );
    end
  endgenerate

endmodule
