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

  gf180mcu_fd_sc_mcu7t5v0__bufz_1 u0 (
      .I (a),
      .EN(oe),
      .Z (z)
  );

endmodule
