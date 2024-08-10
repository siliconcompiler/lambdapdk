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

  ICGx1_ASAP7_75t_SL u0 (
      .CLK(clk),
      .ENA(en),
      .SE (te),
      .GCK(eclk_int)
  );

  INVx1_ASAP7_75t_SL u1 (
      .A(en),
      .Y(en_bar)
  );
  OR2x2_ASAP7_75t_SL u2 (
      .A(en_bar),
      .B(eclk_int),
      .Y(eclk)
  );

endmodule
