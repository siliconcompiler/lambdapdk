// //#############################################################################
// //# Function: And-Or (ao31) Gate                                              #
// //# Copyright: Lambda Project Authors. All rights Reserved.                   #
// //# License:  MIT (see LICENSE file in Lambda repository)                     #
// //#############################################################################
// 
// module la_ao31 #(
//     parameter PROP = "DEFAULT"
// ) (
//     input  a0,
//     input  a1,
//     input  a2,
//     input  b0,
//     output z
// );
// 
//     assign z = (a0 & a1 & a2) | b0;
// 
// endmodule

/* Generated by Yosys 0.38+92 (git sha1 84116c9a3, x86_64-conda-linux-gnu-cc 11.2.0 -fvisibility-inlines-hidden -fmessage-length=0 -march=nocona -mtune=haswell -ftree-vectorize -fPIC -fstack-protector-strong -fno-plt -O2 -ffunction-sections -fdebug-prefix-map=/root/conda-eda/conda-eda/workdir/conda-env/conda-bld/yosys_1708682838165/work=/usr/local/src/conda/yosys-0.38_93_g84116c9a3 -fdebug-prefix-map=/user/projekt_pia/miniconda3/envs/sc=/usr/local/src/conda-prefix -fPIC -Os -fno-merge-constants) */

module la_ao31(a0, a1, a2, b0, z);
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
  sky130_fd_sc_hdll__a31o_1 _0_ (
    .A1(a1),
    .A2(a0),
    .A3(a2),
    .B1(b0),
    .X(z)
  );
endmodule