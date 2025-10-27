/*****************************************************************************
 * Function: True Dual Port RAM (Two write + read ports)
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
 * Technology specific implementations of "la_tdpram" would generally include
 * one or more hardcoded instantiations of RAM modules with a generate
 * statement relying on the "PROP" to select between the list of modules
 * at build time.
 *
 ****************************************************************************/

module la_tdpram_impl #(
    parameter DW    = 32,         // Memory width
    parameter AW    = 10,         // address width (derived)
    parameter PROP  = "DEFAULT",  // pass through variable for hard macro
    parameter CTRLW = 128,        // width of asic ctrl interface
    parameter TESTW = 128         // width of asic test interface
) (  // Write port
    input               clk_a,    // write clock
    input               ce_a,     // write chip-enable
    input               we_a,     // write enable
    input [DW-1:0]      wmask_a,  // write mask
    input [AW-1:0]      addr_a,   // write address
    input [DW-1:0]      din_a,    // write data in
    output reg [DW-1:0] dout_a,   // read data out
    // B port
    input               clk_b,    // write clock
    input               ce_b,     // write chip-enable
    input               we_b,     // write enable
    input [DW-1:0]      wmask_b,  // write mask
    input [AW-1:0]      addr_b,   // write address
    input [DW-1:0]      din_b,    // write data in
    output reg [DW-1:0] dout_b,   // read data out
    // Power signal
    input               vss,      // ground signal
    input               vdd,      // memory core array power
    input               vddio,    // periphery/io power
    // Generic interfaces
    input [CTRLW-1:0]   ctrl,     // pass through ASIC control interface
    input [TESTW-1:0]   test      // pass through ASIC test interface
);

    // Generic RTL RAM
   /* verilator lint_off MULTIDRIVEN */
   reg [DW-1:0]       ram[(2**AW)-1:0];
   /* verilator lint_on MULTIDRIVEN */

   integer            i;

   // Port A write
   always @(posedge clk_a) begin
      for (i = 0; i < DW; i = i + 1) begin
         if (ce_a && we_a && wmask_a[i]) begin
            ram[addr_a][i] <= din_a[i];
         end
      end
   end

   // Port B write
   always @(posedge clk_b) begin
      for (i = 0; i < DW; i = i + 1) begin
         if (ce_b && we_b && wmask_b[i]) begin
            ram[addr_b][i] <= din_b[i];
         end
      end
   end

   // Port A read
   always @(posedge clk_a) begin
      if (ce_a && ~we_a) begin
         dout_a <= ram[addr_a];
      end
   end

   // Port B read
   always @(posedge clk_b) begin
      if (ce_b && ~we_b) begin
         dout_b <= ram[addr_b];
      end
   end

endmodule
