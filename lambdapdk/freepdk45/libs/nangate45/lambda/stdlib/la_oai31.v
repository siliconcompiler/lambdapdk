// //#############################################################################
// //# Function: Or-And-Inverter (oai31) Gate                                    #
// //# Copyright: Lambda Project Authors. All rights Reserved.                   #
// //# License:  MIT (see LICENSE file in Lambda repository)                     #
// //#############################################################################
// 
// module la_oai31 #(parameter PROP = "DEFAULT")   (
//     input  a0,
//     input  a1,
//     input  a2,
//     input  b0,
//     output z
//     );
// 
//    assign z = ~((a0 | a1 | a2) & b0);
// 
// endmodule

/* Generated by Yosys 0.37 (git sha1 a5c7f69ed, clang 14.0.0-1ubuntu1.1 -fPIC -Os) */

module la_oai31(a0, a1, a2, b0, z);
  wire _0_;
  input a0;
  wire a0;
  input a1;
  wire a1;
  input a2;
  wire a2;
  input b0;
  wire b0;
  output z;
  wire z;
  OR2_X4 _1_ (
    .A1(a0),
    .A2(a2),
    .ZN(_0_)
  );
  OAI21_X1 _2_ (
    .A(b0),
    .B1(_0_),
    .B2(a1),
    .ZN(z)
  );
endmodule