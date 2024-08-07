// //#############################################################################
// //# Function: 2-Input one-hot mux                                             #
// //# Copyright: Lambda Project Authors. All rights Reserved.                   #
// //# License:  MIT (see LICENSE file in Lambda repository)                     #
// //#############################################################################
// 
// module la_dmux2
//   #(parameter PROP = "DEFAULT")
//    (
//     input  sel1,
//     input  sel0,
//     input  in1,
//     input  in0,
//     output out
//     );
// 
//    assign out = (sel0 & in0) |
// 		(sel1 & in1);
// 
// endmodule

/* Generated by Yosys 0.37 (git sha1 a5c7f69ed, clang 14.0.0-1ubuntu1.1 -fPIC -Os) */

module la_dmux2(sel1, sel0, in1, in0, out);
  wire _0_;
  input in0;
  wire in0;
  input in1;
  wire in1;
  output out;
  wire out;
  input sel0;
  wire sel0;
  input sel1;
  wire sel1;
  gf180mcu_fd_sc_mcu7t5v0__aoi22_2 _1_ (
    .A1(in0),
    .A2(sel0),
    .B1(in1),
    .B2(sel1),
    .ZN(_0_)
  );
  gf180mcu_fd_sc_mcu7t5v0__clkinv_2 _2_ (
    .I(_0_),
    .ZN(out)
  );
endmodule
