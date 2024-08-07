// //#############################################################################
// //# Function: Positive edge-triggered inverting static D-type flop-flop       #
// //# Copyright: Lambda Project Authors. All rights Reserved.                   #
// //# License:  MIT (see LICENSE file in Lambda repository)                     #
// //#############################################################################
// 
// module la_dffqn #(parameter PROP = "DEFAULT")   (
//     input  	d,
//     input  	clk,
//     output reg  qn
//     );
// 
//    always @ (posedge clk)
//      qn <= ~d;
// 
// endmodule

/* Generated by Yosys 0.37 (git sha1 a5c7f69ed, clang 14.0.0-1ubuntu1.1 -fPIC -Os) */

module la_dffqn(d, clk, qn);
  wire _0_;
  wire _1_;
  input clk;
  wire clk;
  input d;
  wire d;
  output qn;
  wire qn;
  INV_X1 _2_ (
    .A(d),
    .ZN(_0_)
  );
  DFF_X1 _3_ (
    .CK(clk),
    .D(_0_),
    .Q(qn),
    .QN(_1_)
  );
endmodule
