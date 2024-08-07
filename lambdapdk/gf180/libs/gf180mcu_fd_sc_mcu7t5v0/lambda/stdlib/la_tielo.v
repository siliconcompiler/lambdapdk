// //#############################################################################
// //# Function: Tie Low Cell                                                    #
// //# Copyright: Lambda Project Authors. All rights Reserved.                   #
// //# License:  MIT (see LICENSE file in Lambda repository)                     #
// //#############################################################################
// 
// module la_tielo #(parameter PROP = "DEFAULT")  (
//    output z
//    );
// 
//    assign z = 1'b0;
// 
// endmodule

/* Generated by Yosys 0.37 (git sha1 a5c7f69ed, clang 14.0.0-1ubuntu1.1 -fPIC -Os) */

module la_tielo(z);
  output z;
  wire z;
  gf180mcu_fd_sc_mcu7t5v0__tiel _0_ (
    .ZN(z)
  );
endmodule
