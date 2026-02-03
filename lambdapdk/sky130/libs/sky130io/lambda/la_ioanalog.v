/*****************************************************************************
 * Function: IO analog pass-through cell
 * Copyright: Lambda Project Authors. All rights Reserved.
 * License:  MIT (see LICENSE file in Lambda repository)
 *
 * Docs:
 *
 * aio[0] = pass through from pad (with esd clamp)
 * aio[1] = small series resistance
 * aio[2] = big series resistance
 *
 ****************************************************************************/
(* keep_hierarchy *)
module la_ioanalog #(
    parameter PROP  = "DEFAULT",  // cell type
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

  sky130_ef_io__analog_pad i0 (
      .VDDIO(vddio),
      .VCCD(vdd),
      .VSSD(vss),
      .VSSIO(vssio),
      .VDDIO_Q(ioring[0]),
      .VSWITCH(ioring[1]),
      .VCCHIB(ioring[2]),
      .VSSIO_Q(ioring[3]),
      .AMUXBUS_A(ioring[4]),
      .AMUXBUS_B(ioring[5]),
      .VDDA(ioring[6]),
      .VSSA(ioring[7]),

      .P_PAD (pad),
      .P_CORE(aio[0])
  );


endmodule
