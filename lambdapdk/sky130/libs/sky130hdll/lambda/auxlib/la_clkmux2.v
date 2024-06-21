//#############################################################################
//# Function: 2-Input Glitch-Free Clock Mux                                   #
//# Copyright: Lambda Project Authors. All rights Reserved.                   #
//# License:  MIT (see LICENSE file in Lambda repository)                     #
//#############################################################################

module la_clkmux2 #(
    parameter PROP = "DEFAULT"  // cell property
) (
    input  clk0,
    input  clk1,
    input  sel0,
    input  sel1,
    input  nreset,
    output out
);

    wire [1:0] maskb;
    wire [1:0] en;
    wire       enb;
    wire [1:0] ensync;
    wire       ensyncb;
    wire [1:0] clkg;

    // invert mask (2)
    la_inv iinv[1:0] (
        .a({ensync[0], ensync[1]}),
        .z(maskb[1:0])
    );

    // clock enable (2)
    la_and2 isel[1:0] (
        .a({sel1, sel0}),
        .b(maskb[1:0]),
        .z(en[1:0])
    );

    la_inv ienb (
        .a(en[0]),
        .z(enb)
    );

    // synchronizers (2)
    la_drsync isync[1:0] (
        .clk({clk1, clk0}),
        .nreset({nreset, nreset}),
        .in({en[1], enb}),
        .out({ensync[1], ensyncb})
    );

    la_inv iensync (
        .a(ensyncb),
        .z(ensync[0])
    );

    // glith free clock gate (2)
    la_clkicgand igate[1:0] (
        .clk ({clk1, clk0}),
        .te  (2'b00),
        .en  (ensync[1:0]),
        .eclk(clkg[1:0])
    );

    // final clock or (1)
    la_clkor2 iorclk (
        .a(clkg[0]),
        .b(clkg[1]),
        .z(out)
    );

endmodule  // la_clkmux2
