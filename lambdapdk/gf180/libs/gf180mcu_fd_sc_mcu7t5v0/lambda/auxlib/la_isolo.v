//#############################################################################
//# Function: Power isolation circuit                                         #
//# Copyright: Lambda Project Authors. All rights Reserved.                   #
//# License:  MIT (see LICENSE file in Lambda repository)                     #
//#############################################################################

module la_isolo #(
    parameter PROP = "DEFAULT"
) (
    input  iso,  // isolation signal
    input  in,   // input
    output out   // out = ~iso & in
);

    assign out = ~iso & in;

endmodule
