// //#############################################################################
// //# Function: Dual data rate input buffer                                     #
// //# Copyright: Lambda Project Authors. All rights Reserved.                   #
// //# License:  MIT (see LICENSE file in Lambda repository)                     #
// //#############################################################################
// 
// module la_iddr #(
//     parameter PROP = "DEFAULT"
// ) (
//     input      clk,      // clock
//     input      in,       // data input sampled on both edges of clock
//     output reg outrise,  // rising edge sample
//     output reg outfall   // falling edge sample
// );
// 
//     // Negedge Sample
//     always @(negedge clk) outfall <= in;
// 
//     // Posedge Sample
//     reg inrise;
//     always @(posedge clk) inrise <= in;
// 
//     // Posedge Latch (for hold)
//     always @(clk or inrise) if (~clk) outrise <= inrise;
// 
// endmodule

/* Generated by Yosys 0.44 (git sha1 80ba43d26, g++ 11.4.0-1ubuntu1~22.04 -fPIC -O3) */

(* top =  1  *)
(* src = "generated" *)
module la_iddr (
    clk,
    in,
    outrise,
    outfall
);
  wire _0_;
  wire _1_;
  (* src = "generated" *)
  input clk;
  wire clk;
  (* src = "generated" *)
  input in;
  wire in;
  (* src = "generated" *)
  wire inrise;
  (* src = "generated" *)
  output outfall;
  wire outfall;
  (* src = "generated" *)
  output outrise;
  wire outrise;
  INVx2_ASAP7_75t_L _2_ (
      .A(_0_),
      .Y(outfall)
  );
  INVx2_ASAP7_75t_L _3_ (
      .A(_1_),
      .Y(inrise)
  );
  (* module_not_derived = 32'b00000000000000000000000000000001 *) (* src = "generated" *)
  DLLx1_ASAP7_75t_L _4_ (
      .CLK(clk),
      .D  (inrise),
      .Q  (outrise)
  );
  (* src = "generated" *)
  DFFHQNx1_ASAP7_75t_L _5_ (
      .CLK(clk),
      .D  (in),
      .QN (_1_)
  );
  (* src = "generated" *)
  DFFLQNx1_ASAP7_75t_L _6_ (
      .CLK(clk),
      .D  (in),
      .QN (_0_)
  );
endmodule
