// //#############################################################################
// //# Function: Integrated "Or" Clock Gating Cell                               #
// //# Copyright: Lambda Project Authors. All rights Reserved.                   #
// //# License:  MIT (see LICENSE file in Lambda repository)                     #
// //#############################################################################
// 
// module la_clkicgor #(
//     parameter PROP = "DEFAULT"
// ) (
//     input  clk,  // clock input
//     input  te,   // test enable
//     input  en,   // enable
//     output eclk  // enabled clock output
// );
// 
//     reg en_stable;
// 
//     always @(clk or en or te) if (clk) en_stable <= en | te;
// 
//     assign eclk = clk | ~en_stable;
// 
// endmodule

/* Generated by Yosys 0.38+92 (git sha1 84116c9a3, x86_64-conda-linux-gnu-cc 11.2.0 -fvisibility-inlines-hidden -fmessage-length=0 -march=nocona -mtune=haswell -ftree-vectorize -fPIC -fstack-protector-strong -fno-plt -O2 -ffunction-sections -fdebug-prefix-map=/root/conda-eda/conda-eda/workdir/conda-env/conda-bld/yosys_1708682838165/work=/usr/local/src/conda/yosys-0.38_93_g84116c9a3 -fdebug-prefix-map=/user/projekt_pia/miniconda3/envs/sc=/usr/local/src/conda-prefix -fPIC -Os -fno-merge-constants) */

module la_clkicgor(clk, te, en, eclk);
  wire _0_;
  input clk;
  wire clk;
  output eclk;
  wire eclk;
  input en;
  wire en;
  wire en_stable;
  input te;
  wire te;
  sky130_fd_sc_hdll__or2_1 _1_ (
    .A(te),
    .B(en),
    .X(_0_)
  );
  sky130_fd_sc_hdll__nand2b_1 _2_ (
    .A_N(clk),
    .B(en_stable),
    .Y(eclk)
  );
  sky130_fd_sc_hdll__dlxtp_1 _3_ (
    .D(_0_),
    .GATE(clk),
    .Q(en_stable)
  );
endmodule