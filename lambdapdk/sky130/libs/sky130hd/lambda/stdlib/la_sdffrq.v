// //#############################################################################
// //# Function:  Positive edge-triggered static D-type flop-flop with async     #
// //#            active low reset and scan input                                #
// //# Copyright: Lambda Project Authors. All rights Reserved.                   #
// //# License:   MIT (see LICENSE file in Lambda repository)                    #
// //#############################################################################
// 
// module la_sdffrq #(parameter PROP = "DEFAULT")   (
//     input      d,
//     input      si,
//     input      se,
//     input      clk,
//     input      nreset,
//     output reg q
//     );
// 
//    always @ (posedge clk or negedge nreset)
//      if(!nreset)
//        q <= 1'b0;
//      else
//        q <= se ? si : d;
// 
// endmodule

/* Generated by Yosys 0.37 (git sha1 a5c7f69ed, clang 14.0.0-1ubuntu1.1 -fPIC -Os) */

module la_sdffrq(d, si, se, clk, nreset, q);
  wire _0_;
  input clk;
  wire clk;
  input d;
  wire d;
  input nreset;
  wire nreset;
  output q;
  wire q;
  input se;
  wire se;
  input si;
  wire si;
  sky130_fd_sc_hd__mux2_4 _1_ (
    .A0(d),
    .A1(si),
    .S(se),
    .X(_0_)
  );
  sky130_fd_sc_hd__dfrtp_1 _2_ (
    .CLK(clk),
    .D(_0_),
    .Q(q),
    .RESET_B(nreset)
  );
endmodule
