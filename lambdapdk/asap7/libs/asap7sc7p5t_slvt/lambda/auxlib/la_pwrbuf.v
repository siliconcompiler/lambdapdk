//#############################################################################
//# Function: Non-inverting buffer with supplies                              #
//# Copyright: Lambda Project Authors. All rights Reserved.                   #
//# License:  MIT (see LICENSE file in Lambda repository)                     #
//#############################################################################

module la_pwrbuf #(
                   parameter PROP = "DEFAULT"
                   )
   (
    input  vdd,
    input  vss,
    input  a,
    output z
    );

BUFx2_ASAP7_75t_SL u0(.A(a), .Y(z), .VSS(vss), .VDD(vdd));

endmodule
