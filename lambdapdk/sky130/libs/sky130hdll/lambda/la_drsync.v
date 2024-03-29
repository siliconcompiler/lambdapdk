// //#############################################################################
// //# Function: Synchronizer with async reset                                   #
// //# Copyright: Lambda Project Authors. All rights Reserved.                   #
// //# License:  MIT (see LICENSE file in Lambda repository)                     #
// //#############################################################################
// module la_drsync #(
//     parameter PROP = "DEFAULT"
// ) (
//     input  clk,    // clock
//     input  in,     // input data
//     input  nreset, // async active low reset
//     output out     // synchronized data
// );
// 
//     localparam STAGES = 2;
// 
//     reg [STAGES-1:0] shiftreg;
// 
//     always @(posedge clk or negedge nreset)
//         if (!nreset) shiftreg[STAGES-1:0] <= 'b0;
//         else shiftreg[STAGES-1:0] <= {shiftreg[STAGES-2:0], in};
// 
//     assign out = shiftreg[STAGES-1];
// 
// endmodule

/* Generated by Yosys 0.38+92 (git sha1 84116c9a3, x86_64-conda-linux-gnu-cc 11.2.0 -fvisibility-inlines-hidden -fmessage-length=0 -march=nocona -mtune=haswell -ftree-vectorize -fPIC -fstack-protector-strong -fno-plt -O2 -ffunction-sections -fdebug-prefix-map=/root/conda-eda/conda-eda/workdir/conda-env/conda-bld/yosys_1708682838165/work=/usr/local/src/conda/yosys-0.38_93_g84116c9a3 -fdebug-prefix-map=/user/projekt_pia/miniconda3/envs/sc=/usr/local/src/conda-prefix -fPIC -Os -fno-merge-constants) */

module la_drsync(clk, in, nreset, out);
  input clk;
  wire clk;
  input in;
  wire in;
  input nreset;
  wire nreset;
  output out;
  wire out;
  wire \shiftreg[0] ;
  sky130_fd_sc_hdll__dfrtp_1 _0_ (
    .CLK(clk),
    .D(in),
    .Q(\shiftreg[0] ),
    .RESET_B(nreset)
  );
  sky130_fd_sc_hdll__dfrtp_1 _1_ (
    .CLK(clk),
    .D(\shiftreg[0] ),
    .Q(out),
    .RESET_B(nreset)
  );
endmodule
