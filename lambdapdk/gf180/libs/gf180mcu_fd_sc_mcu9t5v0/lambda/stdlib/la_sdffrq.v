// //#############################################################################
// //# Function:  Positive edge-triggered static D-type flop-flop with async     #
// //#            active low reset and scan input                                #
// //# Copyright: Lambda Project Authors. All rights Reserved.                   #
// //# License:   MIT (see LICENSE file in Lambda repository)                    #
// //#############################################################################
// 
// module la_sdffrq #(
//     parameter PROP = "DEFAULT"
// ) (
//     input      d,
//     input      si,
//     input      se,
//     input      clk,
//     input      nreset,
//     output reg q
// );
// 
//     always @(posedge clk or negedge nreset)
//         if (!nreset) q <= 1'b0;
//         else q <= se ? si : d;
// 
// endmodule

/* Generated by Yosys 0.44 (git sha1 80ba43d26, g++ 11.4.0-1ubuntu1~22.04 -fPIC -O3) */

(* top =  1  *)
(* src = "generated" *)
module la_sdffrq (
    d,
    si,
    se,
    clk,
    nreset,
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
  input nreset;
  wire nreset;
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
  gf180mcu_fd_sc_mcu9t5v0__dffrnq_2 _2_ (
      .CLK(clk),
      .D  (_0_),
      .Q  (q),
      .RN (nreset)
  );
endmodule
