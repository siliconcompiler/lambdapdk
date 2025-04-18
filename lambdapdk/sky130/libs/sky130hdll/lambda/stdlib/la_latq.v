// //#############################################################################
// //# Function:  D-type active-high transparent latch                           #
// //# Copyright: Lambda Project Authors. All rights Reserved.                   #
// //# License:   MIT (see LICENSE file in Lambda repository)                    #
// //#############################################################################
// 
// module la_latq #(
//     parameter PROP = "DEFAULT"
// ) (
//     input      d,
//     input      clk,
//     output reg q
// );
// 
//     always @(clk or d) if (clk) q <= d;
// 
// endmodule

/* Generated by Yosys 0.44 (git sha1 80ba43d26, g++ 11.4.0-1ubuntu1~22.04 -fPIC -O3) */

(* top =  1  *)
(* src = "generated" *)
module la_latq (
    d,
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
  sky130_fd_sc_hdll__inv_2 _1_ (
      .A(clk),
      .Y(_0_)
  );
  (* module_not_derived = 32'b00000000000000000000000000000001 *) (* src = "generated" *)
  sky130_fd_sc_hdll__dlxtn_1 _2_ (
      .D(d),
      .GATE_N(_0_),
      .Q(q)
  );
endmodule
