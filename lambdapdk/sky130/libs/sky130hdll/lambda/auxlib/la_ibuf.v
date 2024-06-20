//#############################################################################
//# Function: Single Ended Chip Input Buffer (with ESD protection)            #
//# Copyright: Lambda Project Authors. All rights Reserved.                   #
//# License:  MIT (see LICENSE file in Lambda repository)                     #
//#############################################################################

module la_ibuf
  #(parameter PROP = "DEFAULT")
   (
    input  in, // positive input
    output z // output
    );

   assign z = in;

endmodule
