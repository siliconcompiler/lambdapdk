//#############################################################################
//# Function: Footer circuit                                                  #
//# Copyright: Lambda Project Authors. All rights Reserved.                   #
//# License:  MIT (see LICENSE file in Lambda repository)                     #
//#############################################################################

module la_footer #(
    parameter PROP = "DEFAULT"
) (
    input  nsleep,  // 0 = disabled ground
    input  vssin,   // input supply
    output vssout   // gated output supply
);

    // Primitive Device
    nmos m0 (vddout, vddin, nsleep);  //d,s,g

endmodule
