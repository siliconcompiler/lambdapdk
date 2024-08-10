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

  CLKGATETST_X1 u0 (
      .CK (clk),
      .E  (en),
      .SE (te),
      .GCK(eclk_int)
  );

  INV_X1 u1 (
      .A(en),
      .Z(en_bar)
  );
  OR2_X1 u2 (
      .A1(en_bar),
      .A2(eclk_int),
      .Z (eclk)
  );


endmodule
