//#############################################################################
//# Function: Non-inverting buffer with supplies                              #
//# Copyright: Lambda Project Authors. All rights Reserved.                   #
//# License:  MIT (see LICENSE file in Lambda repository)                     #
//#############################################################################

module la_pwrbuf #(
    parameter PROP = "DEFAULT"
) (
    input  vdd,
    input  vss,
    input  a,
    output z
);

  sg13g2_buf_1 u0 (
      .A  (a),
      .X  (z),
      .VSS(vss),
      .VDD(vdd)
  );

endmodule
