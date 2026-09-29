/*****************************************************************************
 * Function: Single Port RAM
 * Copyright: Lambda Project Authors. All rights Reserved.
 * License:  MIT (see LICENSE file in Lambda repository)
 *
 * Docs:
 *
 * The sky130 memory macros are 1rw1r -- one read-write port and one read-only
 * port -- so the dual port cell is the one that matches the hardware, and this
 * single port cell is built on top of it rather than mapping the macros a
 * second way. The same relationship la_spregfile has with la_spram.
 *
 * The write port is enabled only on a write and the read port only on a read,
 * so exactly one of the macro's two ports is selected in any cycle. Both see
 * the same address, which is the only address this cell has.
 *
 ****************************************************************************/

(* keep_hierarchy *)
module la_spram #(parameter DW = 32,          // Memory width
                  parameter AW = 10,          // Address width (derived)
                  parameter BYTEMASK = 0,     // 1=byte mask, 0=bit mask
                  parameter PROP = "DEFAULT", // variable for hard macro
                  parameter CTRLW = 32,       // width of ctrl interface
                  parameter STATUSW = 32      // width of status interface
                  )
   (// Memory interface
    input                            clk,     // write clock
    input                            ce,      // chip enable
    input                            we,      // write enable
    input [(BYTEMASK?DW/8 : DW)-1:0] wmask,   // bit or byte write mask
    input [AW-1:0]                   addr,    // write address
    input [DW-1:0]                   din,     // write data
    output [DW-1:0]                  dout,    // read output data
    // Technology interfaces
    input                            selctrl, // selects control interface
    input [CTRLW-1:0]                ctrl,    // pass through control interface
    output [STATUSW-1:0]             status   // pass through status interface
    );

   la_dpram #(.DW      (DW),
              .AW      (AW),
              .BYTEMASK(BYTEMASK),
              .PROP    (PROP),
              .CTRLW   (CTRLW),
              .STATUSW (STATUSW))
   memory (
           // write port, taken only on a write
           .wr_clk     (clk),
           .wr_ce      (ce & we),
           .wr_we      (we),
           .wr_wmask   (wmask),
           .wr_addr    (addr),
           .wr_din     (din),
           // read port, taken only on a read
           .rd_clk     (clk),
           .rd_ce      (ce & ~we),
           .rd_addr    (addr),
           .rd_dout    (dout),
           // macro interface
           .selctrl    (selctrl),
           .ctrl       (ctrl),
           .status     (status));

endmodule
