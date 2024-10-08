// //#############################################################################
// //# Function: Positive edge-triggered inverting static D-type flop-flop       #
// //# Copyright: Lambda Project Authors. All rights Reserved.                   #
// //# License:  MIT (see LICENSE file in Lambda repository)                     #
// //#############################################################################
// 
// module la_dffqn #(
//     parameter PROP = "DEFAULT"
// ) (
//     input d,
//     input clk,
//     output reg qn
// );
// 
//     always @(posedge clk) qn <= ~d;
// 
// endmodule

/* Generated by Yosys 0.44 (git sha1 80ba43d26, g++ 11.4.0-1ubuntu1~22.04 -fPIC -O3) */

(* top =  1  *)
(* src = "generated" *)
module la_dffqn (
    d,
    clk,
    qn
);
  (* src = "generated" *)
  wire _0_;
  wire _1_;
  (* src = "generated" *)
  input clk;
  wire clk;
  (* src = "generated" *)
  input d;
  wire d;
  (* src = "generated" *)
  output qn;
  wire qn;
  sky130_fd_sc_hdll__inv_2 _2_ (
      .A(d),
      .Y(_0_)
  );
  (* src = "generated" *)
  sky130_fd_sc_hdll__dfrtp_1 _3_ (
      .CLK(clk),
      .D(_0_),
      .Q(qn),
      .RESET_B(_1_)
  );
  sky130_fd_sc_hdll__conb_1 _4_ (.HI(_1_));
endmodule
