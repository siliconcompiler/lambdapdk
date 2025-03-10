// //#############################################################################
// //# Function: 4-Input Inverting Mux                                           #
// //# Copyright: Lambda Project Authors. All rights Reserved.                   #
// //# License:  MIT (see LICENSE file in Lambda repository)                     #
// //#############################################################################
// 
// module la_muxi4 #(
//     parameter PROP = "DEFAULT"
// ) (
//     input  d0,
//     input  d1,
//     input  d2,
//     input  d3,
//     input  s0,
//     input  s1,
//     output z
// );
// 
//     assign z = ~((d0 & ~s1 & ~s0) | (d1 & ~s1 & s0) | (d2 & s1 & ~s0) | (d3 & s1 & s0));
// 
// endmodule

/* Generated by Yosys 0.44 (git sha1 80ba43d26, g++ 11.4.0-1ubuntu1~22.04 -fPIC -O3) */

(* top =  1  *)
(* src = "generated" *)
module la_muxi4 (
    d0,
    d1,
    d2,
    d3,
    s0,
    s1,
    z
);
  wire _00_;
  wire _01_;
  wire _02_;
  wire _03_;
  wire _04_;
  wire _05_;
  (* src = "generated" *)
  input d0;
  wire d0;
  (* src = "generated" *)
  input d1;
  wire d1;
  (* src = "generated" *)
  input d2;
  wire d2;
  (* src = "generated" *)
  input d3;
  wire d3;
  (* src = "generated" *)
  input s0;
  wire s0;
  (* src = "generated" *)
  input s1;
  wire s1;
  (* src = "generated" *)
  output z;
  wire z;
  INVx1_ASAP7_75t_SL _06_ (
      .A(s0),
      .Y(_04_)
  );
  OR2x2_ASAP7_75t_SL _07_ (
      .A(s0),
      .B(d2),
      .Y(_05_)
  );
  OA211x2_ASAP7_75t_SL _08_ (
      .A1(_04_),
      .A2(d3),
      .B (_05_),
      .C (s1),
      .Y (_00_)
  );
  OR2x2_ASAP7_75t_SL _09_ (
      .A(s0),
      .B(d0),
      .Y(_01_)
  );
  INVx1_ASAP7_75t_SL _10_ (
      .A(s1),
      .Y(_02_)
  );
  OA211x2_ASAP7_75t_SL _11_ (
      .A1(_04_),
      .A2(d1),
      .B (_01_),
      .C (_02_),
      .Y (_03_)
  );
  NOR2x2_ASAP7_75t_SL _12_ (
      .A(_00_),
      .B(_03_),
      .Y(z)
  );
endmodule
