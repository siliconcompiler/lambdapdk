// //#############################################################################
// //# Function: Carry Save Adder (4:2) (aka 5:3)                                #
// //# Copyright: Lambda Project Authors. All rights Reserved.                   #
// //# License:  MIT (see LICENSE file in Lambda repository)                     #
// //#############################################################################
// 
// module la_csa42 #(
//     parameter PROP = "DEFAULT"
// ) (
//     input  a,
//     input  b,
//     input  c,
//     input  d,
//     input  cin,
//     output sum,
//     output carry,
//     output cout
// );
// 
//     assign cout   = (a & b) | (b & c) | (a & c);
//     assign sumint = a ^ b ^ c;
//     assign sum    = cin ^ d ^ sumint;
//     assign carry  = (cin & d) | (cin & sumint) | (d & sumint);
// 
// endmodule

/* Generated by Yosys 0.38+92 (git sha1 84116c9a3, x86_64-conda-linux-gnu-cc 11.2.0 -fvisibility-inlines-hidden -fmessage-length=0 -march=nocona -mtune=haswell -ftree-vectorize -fPIC -fstack-protector-strong -fno-plt -O2 -ffunction-sections -fdebug-prefix-map=/root/conda-eda/conda-eda/workdir/conda-env/conda-bld/yosys_1708682838165/work=/usr/local/src/conda/yosys-0.38_93_g84116c9a3 -fdebug-prefix-map=/user/projekt_pia/miniconda3/envs/sc=/usr/local/src/conda-prefix -fPIC -Os -fno-merge-constants) */

module la_csa42(a, b, c, d, cin, sum, carry, cout);
  wire _00_;
  wire _01_;
  wire _02_;
  wire _03_;
  wire _04_;
  wire _05_;
  wire _06_;
  wire _07_;
  wire _08_;
  wire _09_;
  wire _10_;
  wire _11_;
  wire _12_;
  wire _13_;
  input a;
  wire a;
  input b;
  wire b;
  input c;
  wire c;
  output carry;
  wire carry;
  input cin;
  wire cin;
  output cout;
  wire cout;
  input d;
  wire d;
  output sum;
  wire sum;
  sky130_fd_sc_hdll__inv_1 _14_ (
    .A(a),
    .Y(_00_)
  );
  sky130_fd_sc_hdll__inv_1 _15_ (
    .A(d),
    .Y(_05_)
  );
  sky130_fd_sc_hdll__inv_1 _16_ (
    .A(b),
    .Y(_01_)
  );
  sky130_fd_sc_hdll__inv_1 _17_ (
    .A(cin),
    .Y(_06_)
  );
  sky130_fd_sc_hdll__inv_1 _18_ (
    .A(c),
    .Y(_02_)
  );
  sky130_fd_sc_hdll__inv_1 _19_ (
    .A(_04_),
    .Y(_07_)
  );
  sky130_fd_sc_hdll__inv_1 _20_ (
    .A(_09_),
    .Y(sum)
  );
  sky130_fd_sc_hdll__inv_1 _21_ (
    .A(_03_),
    .Y(cout)
  );
  sky130_fd_sc_hdll__inv_1 _22_ (
    .A(_08_),
    .Y(carry)
  );
  sky130_fd_sc_hdll__fa_1 _23_ (
    .A(_00_),
    .B(_01_),
    .CIN(_02_),
    .COUT(_03_),
    .SUM(_04_)
  );
  sky130_fd_sc_hdll__fa_1 _24_ (
    .A(_05_),
    .B(_06_),
    .CIN(_07_),
    .COUT(_08_),
    .SUM(_09_)
  );
  sky130_fd_sc_hdll__ha_1 _25_ (
    .A(d),
    .B(cin),
    .COUT(_10_),
    .SUM(_11_)
  );
  sky130_fd_sc_hdll__ha_1 _26_ (
    .A(a),
    .B(b),
    .COUT(_12_),
    .SUM(_13_)
  );
endmodule