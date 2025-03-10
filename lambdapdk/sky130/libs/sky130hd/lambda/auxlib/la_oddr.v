// //#############################################################################
// //# Function: Dual data rate output buffer                                    #
// //# Copyright: Lambda Project Authors. All rights Reserved.                   #
// //# License:  MIT (see LICENSE file in Lambda repository)                     #
// //#############################################################################
// 
// module la_oddr #(
//     parameter PROP = "DEFAULT"
// ) (
//     input  clk,  // clock input
//     input  in0,  // data for clk=0
//     input  in1,  // data for clk=1
//     output out   // dual data rate output
// );
// 
//     //Making in1 stable for clk=1
//     reg in1_sh;
//     always @(clk or in1) if (~clk) in1_sh <= in1;
// 
//     //Using clock as data selector
//     assign out = clk ? in1_sh : in0;
// 
// endmodule

/* Generated by Yosys 0.44 (git sha1 80ba43d26, g++ 11.4.0-1ubuntu1~22.04 -fPIC -O3) */

(* top =  1  *)
(* src = "generated" *)
module la_oddr (
    clk,
    in0,
    in1,
    out
);
  (* src = "generated" *)
  input clk;
  wire clk;
  (* src = "generated" *)
  input in0;
  wire in0;
  (* src = "generated" *)
  input in1;
  wire in1;
  (* src = "generated" *)
  wire in1_sh;
  (* src = "generated" *)
  output out;
  wire out;
  sky130_fd_sc_hd__mux2_4 _0_ (
      .A0(in0),
      .A1(in1_sh),
      .S (clk),
      .X (out)
  );
  (* module_not_derived = 32'b00000000000000000000000000000001 *) (* src = "generated" *)
  sky130_fd_sc_hd__dlxtn_1 _1_ (
      .D(in1),
      .GATE_N(clk),
      .Q(in1_sh)
  );
endmodule
