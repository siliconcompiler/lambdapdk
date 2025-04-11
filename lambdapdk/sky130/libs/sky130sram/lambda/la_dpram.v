/*****************************************************************************
 * Function: Dual Port RAM (One write port + One read port)
 * Copyright: Lambda Project Authors. All rights Reserved.
 * License:  MIT (see LICENSE file in Lambda repository)
 *
 * Docs:
 *
 * This is a wrapper for selecting from a set of hardened memory macros.
 *
 * A synthesizable reference model is used when the PROP is DEFAULT. The
 * synthesizable model does not implement the cfg and test interface and should
 * only be used for basic testing and for synthesizing for FPGA devices.
 * Advanced ASIC development should rely on complete functional models
 * supplied on a per macro basis.
 *
 * Technologoy specific implementations of "la_dpram" would generally include
 * one or more hardcoded instantiations of RAM modules with a generate
 * statement relying on the "PROP" to select between the list of modules
 * at build time.
 *
 ****************************************************************************/

module la_dpram #(
    parameter DW    = 32,         // Memory width
    parameter AW    = 10,         // address width (derived)
    parameter PROP  = "DEFAULT",  // pass through variable for hard macro
    parameter CTRLW = 128,        // width of asic ctrl interface
    parameter TESTW = 128         // width of asic test interface
) (  // Write port
    input              wr_clk,    // write clock
    input              wr_ce,     // write chip-enable
    input              wr_we,     // write enable
    input  [   DW-1:0] wr_wmask,  // write mask
    input  [   AW-1:0] wr_addr,   // write address
    input  [   DW-1:0] wr_din,    //write data in
    // Read port
    input              rd_clk,    // read clock
    input              rd_ce,     // read chip-enable
    input  [   AW-1:0] rd_addr,   // read address
    output [   DW-1:0] rd_dout,   //read data out
    // Power signal
    input              vss,       // ground signal
    input              vdd,       // memory core array power
    input              vddio,     // periphery/io power
    // Generic interfaces
    input  [CTRLW-1:0] ctrl,      // pass through ASIC control interface
    input  [TESTW-1:0] test       // pass through ASIC test interface
);

  la_dpram_impl #(
      .DW   (DW),
      .AW   (AW),
      .PROP (PROP),
      .CTRLW(CTRLW),
      .TESTW(TESTW)
  ) memory (
      .wr_clk  (wr_clk),
      .wr_ce   (wr_ce),
      .wr_we   (wr_we),
      .wr_wmask(wr_wmask),
      .wr_addr (wr_addr),
      .wr_din  (wr_din),

      .rd_clk (rd_clk),
      .rd_ce  (rd_ce),
      .rd_addr(rd_addr),
      .rd_dout(rd_dout),

      .vss  (vss),
      .vdd  (vdd),
      .vddio(vddio),

      .ctrl(ctrl),
      .test(test)
  );

endmodule
