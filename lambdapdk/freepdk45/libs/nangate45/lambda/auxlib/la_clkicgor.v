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

    reg en_stable;

    always @(clk or en or te) if (clk) en_stable <= en | te;

    assign eclk = clk | ~en_stable;

endmodule
