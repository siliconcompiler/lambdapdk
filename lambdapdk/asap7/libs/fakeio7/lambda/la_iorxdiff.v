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
(* keep_hierarchy *)
module la_iorxdiff #(
    parameter PROP  = "DEFAULT",  // cell property
    parameter SIDE  = "NO",       // "NO", "SO", "EA", "WE"
    parameter CFGW  = 16,         // width of core config bus
    parameter RINGW = 8           // width of io ring
) (  // io pad signals
    inout              padp,    // differential pad input (positive)
    inout              padn,    // differential pad input (negative)
    inout              vdd,     // core supply
    inout              vss,     // core ground
    inout              vddio,   // io supply
    inout              vssio,   // io ground
    // core facing signals
    output             zp,      // digital output to core (positive)
    output             zn,      // digital output to core (negative)
    input              ie,      // input enable, 1 = active
    inout  [RINGW-1:0] ioring,  // generic ioring interface
    input  [ CFGW-1:0] cfg      // generic config interface
);

  generate
    if (SIDE == "NO" | SIDE == "SO") begin : ivertical
      FAKEIO7_DIFFRX_V i0 (
          .PADP(padp),
          .PADN(padn),
          // core
          .ZP(zp),
          .ZN(zn),
          //supplies
          .DVDD(vddio),
          .DVSS(vssio),
          .VDD(vdd),
          .VSS(vss),
          // config
          .IN_ENABLE(ie),
          .PULLDOWN(cfg[0]),
          .PULLUP(cfg[1]),
          // ring signals
          .RING(ioring)
      );
    end else begin : ihorizontal
      FAKEIO7_DIFFRX_H i0 (
          .PADP(padp),
          .PADN(padn),
          // core
          .ZP(zp),
          .ZN(zn),
          //supplies
          .DVDD(vddio),
          .DVSS(vssio),
          .VDD(vdd),
          .VSS(vss),
          // config
          .IN_ENABLE(ie),
          .PULLDOWN(cfg[0]),
          .PULLUP(cfg[1]),
          // ring signals
          .RING(ioring)
      );
    end
  endgenerate

endmodule
