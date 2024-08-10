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

  ANTENNA_X1 u0 (
      .A  (z),
      .VSS(vss)
  );

endmodule
