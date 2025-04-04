// //#############################################################################
// //# Function: Positive edge-triggered static D-type flop-flop with scan input #
// //#                                                                           #
// //# Copyright: Lambda Project Authors. All rights Reserved.                   #
// //# License:  MIT (see LICENSE file in Lambda repository)                     #
// //#############################################################################
// 
// module la_sdffq #(
//     parameter PROP = "DEFAULT"
// ) (
//     input      d,
//     input      si,
//     input      se,
//     input      clk,
//     output reg q
// );
// 
//     always @(posedge clk) q <= se ? si : d;
// 
// endmodule

/* Generated by Yosys 0.44 (git sha1 80ba43d26, g++ 11.4.0-1ubuntu1~22.04 -fPIC -O3) */

(* top =  1  *)
(* src = "generated" *)
module la_sdffq (
    d,
    si,
    se,
    clk,
    q
);
  (* src = "generated" *)
  wire _0_;
  (* src = "generated" *)
  input clk;
  wire clk;
  (* src = "generated" *)
  input d;
  wire d;
  (* src = "generated" *)
  output q;
  wire q;
  (* src = "generated" *)
  input se;
  wire se;
  (* src = "generated" *)
  input si;
  wire si;
  gf180mcu_fd_sc_mcu9t5v0__mux2_2 _1_ (
      .I0(d),
      .I1(si),
      .S (se),
      .Z (_0_)
  );
  (* src = "generated" *)
  gf180mcu_fd_sc_mcu9t5v0__dffq_2 _2_ (
      .CLK(clk),
      .D  (_0_),
      .Q  (q)
  );
endmodule
