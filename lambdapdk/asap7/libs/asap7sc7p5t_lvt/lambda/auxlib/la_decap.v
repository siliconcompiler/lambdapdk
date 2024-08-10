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

  DECAPx10_ASAP7_75t_L u0 (
      .VSS(vss),
      .VDD(vdd)
  );

endmodule
