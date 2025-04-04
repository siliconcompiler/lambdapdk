// //#############################################################################
// //# Function: Negative edge-triggered static D-type flop-flop                 #
// //# Copyright: Lambda Project Authors. All rights Reserved.                   #
// //# License:  MIT (see LICENSE file in Lambda repository)                     #
// //#############################################################################
// 
// module la_dffnq #(
//     parameter PROP = "DEFAULT"
// ) (
//     input      d,
//     input      clk,
//     output reg q
// );
// 
//     always @(negedge clk) q <= d;
// 
// endmodule

/* Generated by Yosys 0.44 (git sha1 80ba43d26, g++ 11.4.0-1ubuntu1~22.04 -fPIC -O3) */

(* top =  1  *)
(* src = "generated" *)
module la_dffnq (
    d,
    clk,
    q
);
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
  output q;
  wire q;
  INV_X2 _2_ (
      .A (clk),
      .ZN(_0_)
  );
  (* src = "generated" *)
  DFF_X1 _3_ (
      .CK(_0_),
      .D (d),
      .Q (q),
      .QN(_1_)
  );
endmodule
