//#############################################################################
//# Function: Integrated "Or" Clock Gating Cell                               #
//# Copyright: Lambda Project Authors. All rights Reserved.                   #
//# License:  MIT (see LICENSE file in Lambda repository)                     #
//#############################################################################

(* keep_hierarchy *)
module la_clkicgor #(
    parameter PROP = "DEFAULT"
) (
    input  clk,  // clock input
    input  te,   // test enable
    input  en,   // enable
    output eclk  // enabled clock output
);

  // reg en_stable;

  // always @(clk or en or te) if (clk) en_stable <= en | te;

  // assign eclk = clk | ~en_stable;

  wire eclk_int;
  wire en_bar;

  gf180mcu_fd_sc_mcu9t5v0__icgtp_1 u0 (
      .CLK(clk),
      .E  (en),
      .TE (te),
      .Q  (eclk_int)
  );

  gf180mcu_fd_sc_mcu9t5v0__inv_1 u1 (
      .I (en),
      .ZN(en_bar)
  );
  gf180mcu_fd_sc_mcu9t5v0__or2_1 u2 (
      .A1(en_bar),
      .A2(eclk_int),
      .Z (eclk)
  );


endmodule
