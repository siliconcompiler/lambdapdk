// //#############################################################################
// //# Function: And-Or-Inverter (aoi211) Gate                                   #
// //# Copyright: Lambda Project Authors. All rights Reserved.                   #
// //# License:  MIT (see LICENSE file in Lambda repository)                     #
// //#############################################################################
// 
// module la_aoi211 #(parameter PROP = "DEFAULT")  (
//    input  a0,
//    input  a1,
//    input  b0,
//    input  c0,
//    output z
//    );
// 
//    assign z = ~((a0 & a1) | b0 | c0);
// 
// endmodule

/* Generated by Yosys 0.37 (git sha1 a5c7f69ed, clang 14.0.0-1ubuntu1.1 -fPIC -Os) */

module la_aoi211(a0, a1, b0, c0, z);
  input a0;
  wire a0;
  input a1;
  wire a1;
  input b0;
  wire b0;
  input c0;
  wire c0;
  output z;
  wire z;
  AOI211_X1 _0_ (
    .A(b0),
    .B(c0),
    .C1(a1),
    .C2(a0),
    .ZN(z)
  );
endmodule
