//#############################################################################
//# Function: Tristate Buffer                                                 #
//# Copyright: Lambda Project Authors. All rights Reserved.                   #
//# License:  MIT (see LICENSE file in Lambda repository)                     #
//#############################################################################

module la_tbuf #(
    parameter PROP = "DEFAULT"
) (
    input  a,
    input  oe,
    output z
);

  // assign z = oe ? a : 1'bz;

  sg13g2_ebufn_2 u0 (
      .A(a),
      .TE_B(~oe),
      .Z(z)
  );

endmodule
