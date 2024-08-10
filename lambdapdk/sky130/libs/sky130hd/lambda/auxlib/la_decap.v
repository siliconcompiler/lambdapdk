//#############################################################################
//# Function: Decap Cell                                                      #
//# Copyright: Lambda Project Authors. All rights Reserved.                   #
//# License:  MIT (see LICENSE file in Lambda repository)                     #
//#############################################################################

module la_decap #(
    parameter PROP = "DEFAULT"
) (
    input  vss,
    output vdd
);

  sky130_fd_sc_hd__decap_12 u0 (
      .VGND(vss),
      .VPWR(vdd)
  );

endmodule
