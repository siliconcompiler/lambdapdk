// //#############################################################################
// //# Function: Or-And (oa33) Gate                                              #
// //# Copyright: Lambda Project Authors. All rights Reserved.                   #
// //# License:  MIT (see LICENSE file in Lambda repository)                     #
// //#############################################################################
// 
// module la_oa33 #(
//     parameter PROP = "DEFAULT"
// ) (
//     input  a0,
//     input  a1,
//     input  a2,
//     input  b0,
//     input  b1,
//     input  b2,
//     output z
// );
// 
//     assign z = (a0 | a1 | a2) & (b0 | b1 | b2);
// 
// endmodule

/* Generated by Yosys 0.44 (git sha1 80ba43d26, g++ 11.4.0-1ubuntu1~22.04 -fPIC -O3) */

(* top =  1  *)
(* src = "generated" *)
module la_oa33 (
    a0,
    a1,
    a2,
    b0,
    b1,
    b2,
    z
);
  wire _0_;
  wire _1_;
  (* src = "generated" *)
  input a0;
  wire a0;
  (* src = "generated" *)
  input a1;
  wire a1;
  (* src = "generated" *)
  input a2;
  wire a2;
  (* src = "generated" *)
  input b0;
  wire b0;
  (* src = "generated" *)
  input b1;
  wire b1;
  (* src = "generated" *)
  input b2;
  wire b2;
  (* src = "generated" *)
  output z;
  wire z;
  sky130_fd_sc_hd__nor3_1 _2_ (
      .A(a1),
      .B(a0),
      .C(a2),
      .Y(_0_)
  );
  sky130_fd_sc_hd__nor3_1 _3_ (
      .A(b2),
      .B(b1),
      .C(b0),
      .Y(_1_)
  );
  sky130_fd_sc_hd__nor2_1 _4_ (
      .A(_0_),
      .B(_1_),
      .Y(z)
  );
endmodule
