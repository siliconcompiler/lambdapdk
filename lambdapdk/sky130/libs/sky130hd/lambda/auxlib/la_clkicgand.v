//#############################################################################
//# Function: Integrated "And" Clock Gating Cell (And)                        #
//# Copyright: Lambda Project Authors. All rights Reserved.                   #
//# License:  MIT (see LICENSE file in Lambda repository)                     #
//#############################################################################

module la_clkicgand #(
    parameter PROP = "DEFAULT"
) (
    input  clk,  // clock input
    input  te,   // test enable
    input  en,   // enable (from positive edge FF)
    output eclk  // enabled clock output
);

    reg en_stable;

    always @(clk or en or te) if (~clk) en_stable <= en | te;

    assign eclk = clk & en_stable;

endmodule
