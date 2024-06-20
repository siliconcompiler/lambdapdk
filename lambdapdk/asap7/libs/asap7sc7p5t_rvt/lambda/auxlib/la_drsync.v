//#############################################################################
//# Function: Synchronizer with async reset                                   #
//# Copyright: Lambda Project Authors. All rights Reserved.                   #
//# License:  MIT (see LICENSE file in Lambda repository)                     #
//#############################################################################
module la_drsync #(
    parameter PROP = "DEFAULT"
) (
    input  clk,    // clock
    input  in,     // input data
    input  nreset, // async active low reset
    output out     // synchronized data
);

    localparam STAGES = 2;

    reg [STAGES-1:0] shiftreg;

    always @(posedge clk or negedge nreset)
        if (!nreset) shiftreg[STAGES-1:0] <= 'b0;
        else shiftreg[STAGES-1:0] <= {shiftreg[STAGES-2:0], in};

    assign out = shiftreg[STAGES-1];

endmodule
