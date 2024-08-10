//#############################################################################
//# Function: Antenna Diode                                                   #
//# Copyright: Lambda Project Authors. All rights Reserved.                   #
//# License:  MIT (see LICENSE file in Lambda repository)                     #
//#############################################################################

module la_antenna #(
    parameter PROP = "DEFAULT"
) (
    input  vss,
    output z
);

  sky130_fd_sc_hdll__diode_2 u0 (
      .DIODE(z),
      .VGND (vss)
  );

endmodule
