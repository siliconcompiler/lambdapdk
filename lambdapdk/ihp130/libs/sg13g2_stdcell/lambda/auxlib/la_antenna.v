//#############################################################################
//# Function: Antenna Diode                                                   #
//# Copyright: Lambda Project Authors. All rights Reserved.                   #
//# License:  MIT (see LICENSE file in Lambda repository)                     #
//#############################################################################

(* keep_hierarchy *)
module la_antenna #(
    parameter PROP = "DEFAULT"
) (
    input  vss,
    output z
);

  sg13g2_antennanp u0 (
      .A  (z),
      .VSS(vss)
  );

endmodule
