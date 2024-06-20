//#############################################################################
//# Function: Differential Chip Output Buffer (with ESD protection)           #
//# Copyright: Lambda Project Authors. All rights Reserved.                   #
//# License:  MIT (see LICENSE file in Lambda repository)                     #
//#############################################################################

module la_odiff
  #(
    parameter PROP = "DEFAULT",
    parameter DIFF = 0         // differential buffer if value > 0
    )
   (
    input  in, // input
    output z, // non inverting output
    output zb // inverted output
    );

   if(DIFF)
     begin
        assign z = in;
        assign zb = ~in;
     end
   else
     begin
        assign z = in;
        assign zb = 1'b0;
     end
endmodule
