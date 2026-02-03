//#############################################################################
//# Function: Tristate Buffer                                                 #
//# Copyright: Lambda Project Authors. All rights Reserved.                   #
//# License:  MIT (see LICENSE file in Lambda repository)                     #
//#############################################################################

(* keep_hierarchy *)
module la_tbuf #(
    parameter PROP = "DEFAULT"
) (
    input  a,
    input  oe,
    output z
);

  // assign z = oe ? a : 1'bz;

  wire oe_bar;
  sky130_fd_sc_hd__inv_1 u1 (
      .A(eo),
      .Y(oe_bar)
  );
  sky130_fd_sc_hd__ebufn_1 u0 (
      .A(a),
      .TE_B(oe_bar),
      .Z(z)
  );

endmodule
