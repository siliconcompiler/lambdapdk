/*****************************************************************************
 * Function: IO analog pass-through cell
 * Copyright: Lambda Project Authors. ALl rights Reserved.
 * License:  MIT (see LICENSE file in Lambda repository)
 *
 * Docs:
 *
 * aio[0] = pass through from pad (with esd clamp)
 * aio[1] = small series resistance
 * aio[2] = big series resistance
 *
 ****************************************************************************/
module la_ioanalog
  #(
    parameter TYPE = "DEFAULT", // cell type
    parameter SIDE  = "NO",     // "NO", "SO", "EA", "WE"
    parameter RINGW =  8        // width of io ring
    )
   (// io pad signals
    inout 	      pad, // bidirectional pad signal
    inout 	      vdd, // core supply
    inout 	      vss, // core ground
    inout 	      vddio, // io supply
    inout 	      vssio, // io ground
    inout [RINGW-1:0] ioring, // generic io-ring interface
    // core interface
    inout [2:0]       aio // analog core signal
    );


`ifdef VERILATOR
   // TODO!: input only for verilator bases simulation
   assign aio[0] = pad;
   assign aio[1] = pad;
   assign aio[2] = pad;

`else
   tran t0(pad, aio[0]);
   tran t1(pad, aio[1]);
   tran t2(pad, aio[2]);
`endif

endmodule
