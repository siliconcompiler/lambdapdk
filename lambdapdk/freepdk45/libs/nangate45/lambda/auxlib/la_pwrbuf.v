//#############################################################################
//# Function: Non-inverting buffer with supplies                              #
//# Copyright: Lambda Project Authors. All rights Reserved.                   #
//# License:  MIT (see LICENSE file in Lambda repository)                     #
//#############################################################################

(* keep_hierarchy *)
module la_pwrbuf #(
    parameter PROP = "DEFAULT"
) (
    input  vdd,
    input  vss,
    input  a,
    output z
);

  BUF_X1 u0 (
      .A  (a),
      .Z  (z),
      .VSS(vss),
      .VDD(vdd)
  );

endmodule
