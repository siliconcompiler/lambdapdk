//#############################################################################
//# Function: Differential Chip Input Buffer (with ESD protection)            #
//# Copyright: Lambda Project Authors. All rights Reserved.                   #
//# License:  MIT (see LICENSE file in Lambda repository)                     #
//#############################################################################

module la_idiff
  #(
    parameter PROP = "DEFAULT",
    parameter DIFF = 0         // differential buffer if value > 0
    )
   (
    input  in, // positive input
    input  inb, // negative input
    output z // output
    );

   if(DIFF)
     assign z = (in & ~inb)  | // for proper diff inputs
                (~in & ~inb);  // fail on non diff input
   else
     assign z = in;

endmodule
