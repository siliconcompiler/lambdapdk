//#############################################################################
//# Function: Antenna Diode                                                   #
//# Copyright: Lambda Project Authors. All rights Reserved.                   #
//# License:  MIT (see LICENSE file in Lambda repository)                     #
//#############################################################################

module la_antenna #(
    parameter PROP = "DEFAULT"
) (
    input  vss,
    output z
);

gf180mcu_fd_sc_mcu7t5v0__antenna u0(.I(z), .VSS(vss));

endmodule
