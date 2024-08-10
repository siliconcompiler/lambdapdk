//#############################################################################
//# Function: Integrated "Or" Clock Gating Cell                               #
//# Copyright: Lambda Project Authors. All rights Reserved.                   #
//# License:  MIT (see LICENSE file in Lambda repository)                     #
//#############################################################################

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

  sky130_fd_sc_hdll__sdlclkp_1 u0 (
      .CLK (clk),
      .SCE (te),
      .GATE(en),
      .GCLK(eclk_int)
  );

  sky130_fd_sc_hdll__inv_1 u1 (
      .A(en),
      .Y(en_bar)
  );
  sky130_fd_sc_hdll__or2_1 u2 (
      .A(en_bar),
      .B(eclk_int),
      .X(eclk)
  );

endmodule
