//#############################################################################
//# Function: Tristate Buffer                                                 #
//# Copyright: Lambda Project Authors. All rights Reserved.                   #
//# License:  MIT (see LICENSE file in Lambda repository)                     #
//#############################################################################

module la_tbuf #(
    parameter PROP = "DEFAULT"
) (
    input  a,
    input  oe,
    output z
);

    assign z = oe ? a : 1'bz;

endmodule
