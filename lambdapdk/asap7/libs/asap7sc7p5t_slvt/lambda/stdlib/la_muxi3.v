// //#############################################################################
// //# Function: 3-Input Inverting Mux                                           #
// //# Copyright: Lambda Project Authors. All rights Reserved.                   #
// //# License:  MIT (see LICENSE file in Lambda repository)                     #
// //#############################################################################
// 
// module la_muxi3 #(
//     parameter PROP = "DEFAULT"
// ) (
//     input  d0,
//     input  d1,
//     input  d2,
//     input  s0,
//     input  s1,
//     output z
// );
// 
//     assign z = ~((d0 & ~s0 & ~s1) | (d1 & s0 & ~s1) | (d2 & s1));
// 
// endmodule

/* Generated by Yosys 0.40 (git sha1 a1bb0255d, g++ 11.4.0-1ubuntu1~22.04 -fPIC -Os) */

module la_muxi3(d0, d1, d2, s0, s1, z);
  wire _00_;
  wire _01_;
  wire _02_;
  wire _03_;
  wire _04_;
  input d0;
  wire d0;
  input d1;
  wire d1;
  input d2;
  wire d2;
  input s0;
  wire s0;
  input s1;
  wire s1;
  output z;
  wire z;
  INVx1_ASAP7_75t_SL _05_ (
    .A(d2),
    .Y(_02_)
  );
  INVx1_ASAP7_75t_SL _06_ (
    .A(d0),
    .Y(_03_)
  );
  INVx1_ASAP7_75t_SL _07_ (
    .A(s1),
    .Y(_04_)
  );
  NAND2x1_ASAP7_75t_SL _08_ (
    .A(s0),
    .B(d1),
    .Y(_00_)
  );
  OA211x2_ASAP7_75t_SL _09_ (
    .A1(s0),
    .A2(_03_),
    .B(_04_),
    .C(_00_),
    .Y(_01_)
  );
  AO21x1_ASAP7_75t_SL _10_ (
    .A1(s1),
    .A2(_02_),
    .B(_01_),
    .Y(z)
  );
endmodule