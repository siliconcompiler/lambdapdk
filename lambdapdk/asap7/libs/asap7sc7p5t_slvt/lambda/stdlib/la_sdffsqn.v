// //#############################################################################
// //# Function:  Positive edge-triggered static inverting D-type flop-flop with #
// //             async active low set and scan input                            #
// //# Copyright: Lambda Project Authors. All rights Reserved.                   #
// //# License:   MIT (see LICENSE file in Lambda repository)                    #
// //#############################################################################
// 
// module la_sdffsqn #(
//     parameter PROP = "DEFAULT"
// ) (
//     input      d,
//     input      si,
//     input      se,
//     input      clk,
//     input      nset,
//     output reg qn
// );
// 
//     always @(posedge clk or negedge nset)
//         if (!nset) qn <= 1'b0;
//         else qn <= se ? ~si : ~d;
// 
// endmodule

/* Generated by Yosys 0.44 (git sha1 80ba43d26, g++ 11.4.0-1ubuntu1~22.04 -fPIC -O3) */

(* top =  1  *)
(* src = "generated" *)
module la_sdffsqn (
    d,
    si,
    se,
    clk,
    nset,
    qn
);
  (* src = "generated" *)
  wire _00_;
  wire _01_;
  wire _02_;
  wire _03_;
  wire _04_;
  (* src = "generated" *)
  input clk;
  wire clk;
  (* src = "generated" *)
  input d;
  wire d;
  (* src = "generated" *)
  input nset;
  wire nset;
  (* src = "generated" *)
  output qn;
  wire qn;
  (* src = "generated" *)
  input se;
  wire se;
  (* src = "generated" *)
  input si;
  wire si;
  INVx1_ASAP7_75t_SL _05_ (
      .A(si),
      .Y(_02_)
  );
  NOR2x1_ASAP7_75t_SL _06_ (
      .A(d),
      .B(se),
      .Y(_03_)
  );
  AO21x1_ASAP7_75t_SL _07_ (
      .A1(_02_),
      .A2(se),
      .B (_03_),
      .Y (_00_)
  );
  INVx1_ASAP7_75t_SL _08_ (
      .A(_01_),
      .Y(qn)
  );
  (* src = "generated" *)
  DFFASRHQNx1_ASAP7_75t_SL _09_ (
      .CLK(clk),
      .D(_00_),
      .QN(_01_),
      .RESETN(_04_),
      .SETN(nset)
  );
  TIEHIx1_ASAP7_75t_SL _10_ (.H(_04_));
endmodule
