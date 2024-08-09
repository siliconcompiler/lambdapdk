/*****************************************************************************
 * Function: Digital Differential Transmitter IO Cell
 * Copyright: Lambda Project Authors. All rights Reserved.
 * License:  MIT (see LICENSE file in Lambda repository)
 *
 * Docs:
 *
 * ../README.md
 *
 ****************************************************************************/
module la_iotxdiff #(
    parameter PROP  = "DEFAULT",  // cell property
    parameter SIDE  = "NO",       // "NO", "SO", "EA", "WE"
    parameter CFGW  = 16,         // width of core config bus
    parameter RINGW = 8           // width of io ring
) (  // io pad signals
    inout             padp,    // differential pad output (positive)
    inout             padn,    // differential pad output (negative)
    inout             vdd,     // core supply
    inout             vss,     // core ground
    inout             vddio,   // io supply
    inout             vssio,   // io ground
    // core facing signals
    input             a,       // input from core
    input             oe,      // output enable, 1 = active
    inout [RINGW-1:0] ioring,  // generic ioring interface
    input [ CFGW-1:0] cfg      // generic config interface
);

  generate
    if (SIDE == "NO" | SIDE == "SO") begin : ivertical
      FAKEIO7_DIFFTX_V i0 (
          .PADP(padp),
          .PADN(padn),
          // core
          .A(a),
          //supplies
          .DVDD(vddio),
          .DVSS(vssio),
          .VDD(vdd),
          .VSS(vss),
          // config
          .OUT_ENABLE(oe),
          .DRIVE0(cfg[2]),
          .DRIVE1(cfg[3]),
          // ring signals
          .RING(ioring)
      );
    end else begin : ihorizontal
      FAKEIO7_DIFFTX_H i0 (
          .PADP(padp),
          .PADN(padn),
          // core
          .A(a),
          //supplies
          .DVDD(vddio),
          .DVSS(vssio),
          .VDD(vdd),
          .VSS(vss),
          // config
          .OUT_ENABLE(oe),
          .DRIVE0(cfg[2]),
          .DRIVE1(cfg[3]),
          // ring signals
          .RING(ioring)
      );
    end
  endgenerate

endmodule
