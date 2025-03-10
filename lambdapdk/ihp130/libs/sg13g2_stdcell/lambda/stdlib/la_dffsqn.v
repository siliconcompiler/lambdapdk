// //#############################################################################
// //# Function:  Positive edge-triggered static inverting D-type flop-flop with #
// //             async active low set.                                          #
// //# Copyright: Lambda Project Authors. All rights Reserved.                   #
// //# License:   MIT (see LICENSE file in Lambda repository)                    #
// //#############################################################################
// 
// module la_dffsqn #(
//     parameter PROP = "DEFAULT"
// ) (
//     input d,
//     input clk,
//     input nset,
//     output reg qn
// );
// 
//     always @(posedge clk or negedge nset)
//         if (!nset) qn <= 1'b0;
//         else qn <= ~d;
// 
// endmodule

/* Generated by Yosys 0.44 (git sha1 80ba43d26, g++ 11.4.0-1ubuntu1~22.04 -fPIC -O3) */

(* top =  1  *)
(* src = "generated" *)
module la_dffsqn (
    d,
    clk,
    nset,
    qn
);
  (* src = "generated" *)
  wire _0_;
  (* unused_bits = "0" *)
  wire _1_;
  (* src = "generated" *)
  input clk;
  wire clk;
  (* src = "generated" *)
  input d;
  wire d;
  (* src = "generated" *)
  input nset;
  wire nset;
  (* src = "generated" *)
  output qn;
  wire qn;
  sg13g2_inv_2 _2_ (
      .A(d),
      .Y(_0_)
  );
  (* src = "generated" *)
  sg13g2_dfrbp_1 _3_ (
      .CLK(clk),
      .D(_0_),
      .Q(qn),
      .Q_N(_1_),
      .RESET_B(nset)
  );
endmodule
