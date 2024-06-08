//#############################################################################
//# Function: Header circuit                                                  #
//# Copyright: Lambda Project Authors. All rights Reserved.                   #
//# License:  MIT (see LICENSE file in Lambda repository)                     #
//#############################################################################

module la_header #(
    parameter PROP = "DEFAULT"
) (
    input  sleep,  // 1 = disabled vdd
    input  vddin,  // input supply
    output vddout  // gated output supply
);

    // Primitive Device
    pmos m0 (vddout, vssin, sleep);  //d,s,g

endmodule
