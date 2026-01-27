/**************************************************************************
 * Function: Digital Bidirectional IO Buffer
 * Copyright: Lambda Project Authors. All rights Reserved.
 * License:  MIT (see LICENSE file in Lambda repository)
 *
 * Docs:
 *
 * ../README.md
 *
 *************************************************************************/
module la_iobidir #(
    parameter PROP  = "DEFAULT",  // cell property
    parameter SIDE  = "NO",       // "NO", "SO", "EA", "WE"
    parameter CFGW  = 16,         // width of core config bus
    parameter RINGW = 8           // width of io ring
) (  // io pad signals
    inout              pad,     // bidirectional pad signal
    inout              vdd,     // core supply
    inout              vss,     // core ground
    inout              vddio,   // io supply
    inout              vssio,   // io ground
    // core facing signals
    input              a,       // input from core
    output             z,       // output to core
    input              ie,      // input enable, 1 = active
    input              oe,      // output enable, 1 = active
    input              pe,      // pull enable, 1 = enable
    input              ps,      // pull select, 1 = pullup, 0 = pulldown
    input              schmitt, // schmitt cfg, 1 = active
    input              fast,    // 1 = fast slew rate
    input  [1:0]       ds,      // drive strength, 0=weakest
    inout  [RINGW-1:0] ioring,  // generic io ring
    input  [ CFGW-1:0] cfg      // generic config interface
);

  generate
    if (SIDE == "NO" | SIDE == "SO") begin : ivertical
      FAKEIO7_BIDIR_V i0 (  // pad
          .PAD(pad),
          // core signals
          .Z(z),
          .A(a),
          //supplies
          .DVDD(vddio),
          .DVSS(vssio),
          .VDD(vdd),
          .VSS(vss),
          // config
          .OUT_ENABLE(oe),
          .IN_ENABLE(ie),
          .PULLDOWN(pe & ~ps),
          .PULLUP(pe & ps),
          .DRIVE0(ds[0]),
          .DRIVE1(ds[1]),
          // ring signals
          .RING(ioring)
      );
    end // block: ivertical
      else
        begin: ihorizontal
      FAKEIO7_BIDIR_H i0 (  // pad
          .PAD(pad),
          // core signals
          .Z(z),
          .A(a),
          //supplies
          .DVDD(vddio),
          .DVSS(vssio),
          .VDD(vdd),
          .VSS(vss),
          // config
          .OUT_ENABLE(oe),
          .IN_ENABLE(ie),
          .PULLDOWN(pe & ~ps),
          .PULLUP(pe & ps),
          .DRIVE0(ds[0]),
          .DRIVE1(ds[1]),
          // ring signals
          .RING(ioring)
      );
    end  // block: ihorizontal
  endgenerate

endmodule
