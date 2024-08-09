/*****************************************************************************
 * Function: ESD Clamp IO cell
 * Copyright: Lambda Project Authors. All rights Reserved.
 * License:  MIT (see LICENSE file in Lambda repository)
 *
 * Docs:
 *
 * ../README.md
 *
 ****************************************************************************/
module la_ioclamp #(
    parameter PROP  = "DEFAULT",  // cell property
    parameter SIDE  = "NO",       // "NO", "SO", "EA", "WE"
    parameter RINGW = 8           // width of io ring
) (  // io pad signals
    input             vddclamp,
    inout             vdd,       // core supply
    inout             vss,       // core ground
    inout             vddio,     // io supply
    inout             vssio,     // io ground
    inout [RINGW-1:0] ioring     // generic io ring interface
);

  generate
    if (SIDE == "NO" | SIDE == "SO") begin : ivertical
      FAKEIO7_VDDCLAMP_V i0 (
          .DVDD(vddio),
          .DVSS(vssio),
          .VDDCLAMP(vddclamp),
          .VDD(vdd),
          .VSS(vss),
          .RING(ioring)
      );
    end else begin : ihorizontal
      FAKEIO7_VDDCLAMP_H i0 (
          .DVDD(vddio),
          .DVSS(vssio),
          .VDDCLAMP(vddclamp),
          .VDD(vdd),
          .VSS(vss),
          .RING(ioring)
      );
    end
  endgenerate

endmodule
