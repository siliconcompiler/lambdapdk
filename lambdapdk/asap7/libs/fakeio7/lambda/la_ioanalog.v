/*****************************************************************************
 * Function: Analog Passthrough IO cell
 * Copyright: Lambda Project Authors. All rights Reserved.
 * License:  MIT (see LICENSE file in Lambda repository)
 *
 * Docs:
 *
 * ../README.md
 *
 * aio[0] = pass through from pad (with esd clamp)
 * aio[1] = small series resistance
 * aio[2] = big series resistance
 *
 ****************************************************************************/
module la_ioanalog #(
    parameter PROP  = "DEFAULT",  // cell property
    parameter SIDE  = "NO",       // "NO", "SO", "EA", "WE"
    parameter RINGW = 8           // width of io ring
) (  // io pad signals
    inout             pad,     // bidirectional pad signal
    inout             vdd,     // core supply
    inout             vss,     // core ground
    inout             vddio,   // io supply
    inout             vssio,   // io ground
    inout [RINGW-1:0] ioring,  // generic ioring
    // core interface
    inout [      2:0] aio      // analog core signals
);

  generate
    if (SIDE == "NO" | SIDE == "SO") begin : ivertical
      FAKEIO7_ANALOG_V i0 (  // pad
          .PAD (pad),
          // analog core signals
          .AIO (aio),
          // supplies
          .DVDD(vddio),
          .DVSS(vssio),
          .VSS (vss),
          .VDD (vdd),
          // ring signals
          .RING(ioring)
      );
    end // block: ivertical
      else
        begin: ihorizontal
      FAKEIO7_ANALOG_H i0 (  // pad
          .PAD (pad),
          // analog core signals
          .AIO (aio),
          // supplies
          .DVDD(vddio),
          .DVSS(vssio),
          .VSS (vss),
          .VDD (vdd),
          // ring signals
          .RING(ioring)
      );
    end  // block: ihorizontal
  endgenerate

endmodule
