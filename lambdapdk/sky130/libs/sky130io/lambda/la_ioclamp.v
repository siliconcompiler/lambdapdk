/*****************************************************************************
 * Function: IO ESD clamp cell
 * Copyright: Lambda Project Authors. All rights Reserved.
 * License:  MIT (see LICENSE file in Lambda repository)
 *
 * Docs:
 *
 ****************************************************************************/
module la_ioclamp #(
    parameter PROP  = "DEFAULT",  // cell type
    parameter SIDE  = "NO",       // "NO", "SO", "EA", "WE"
    parameter RINGW = 8           // width of io ring
) (  // io pad signals
    inout             vdd,    // core supply
    inout             vss,    // core ground
    inout             vddio,  // io supply
    inout             vssio,  // io ground
    inout [RINGW-1:0] ioring  // generic io ring interface
);

  sky130_ef_io__vddio_hvc_clamped_pad clamp (
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
      .VSSA(ioring[7])
  );

endmodule
