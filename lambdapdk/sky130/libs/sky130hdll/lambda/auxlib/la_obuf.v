//#############################################################################
//# Function: Single Ended Chip Output Buffer (with ESD protection)           #
//# Copyright: Lambda Project Authors. All rights Reserved.                   #
//# License:  MIT (see LICENSE file in Lambda repository)                     #
//#############################################################################

module la_obuf
  #(parameter PROP = "DEFAULT")
   (
    input  in, // positive input
    output z // output
    );

   assign z = in;

endmodule
