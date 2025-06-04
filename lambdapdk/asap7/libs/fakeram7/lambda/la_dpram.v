/*****************************************************************************
 * Function: Dual Port Memory (la_dpram)
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
 * one or more hardcoded instantiations of la_dpram modules with a generate
 * statement relying on the "PROP" to select between the list of modules
 * at build time.
 *
 ****************************************************************************/

module la_dpram #(
    parameter DW    = 32,         // Memory width
    parameter AW    = 10,         // Address width (derived)
    parameter PROP  = "DEFAULT",  // Pass through variable for hard macro
    parameter CTRLW = 128,        // Width of asic ctrl interface
    parameter TESTW = 128         // Width of asic test interface
) (  // Memory interface
     // Write port
    input wr_clk,  // write clock
    input wr_ce,  // write chip-enable
    input wr_we,  // write enable
    input [DW-1:0] wr_wmask,  // write mask
    input [AW-1:0] wr_addr,  // write address
    input [DW-1:0] wr_din,  //write data in
    // Read port
    input rd_clk,  // read clock
    input rd_ce,  // read chip-enable
    input [AW-1:0] rd_addr,  // read address
    output [DW-1:0] rd_dout,  //read data out
    // Power signals
    input vss,  // ground signal
    input vdd,  // memory core array power
    input vddio,  // periphery/io power
    // Generic interfaces
    input [CTRLW-1:0] ctrl,  // pass through ASIC control interface
    input [TESTW-1:0] test  // pass through ASIC test interface
);

  // Total number of bits
  localparam TOTAL_BITS = (2 ** AW) * DW;

  // Determine which memory to select
  localparam MEM_PROP = (PROP != "DEFAULT") ? PROP :
      (AW >= 13) ? (DW >= 64) ? "fakeram7_dp_8192x64" : "fakeram7_dp_8192x32" :
      (AW >= 12) ? (DW >= 64) ? "fakeram7_dp_4096x64" : "fakeram7_dp_4096x32" :
      (AW >= 11) ? (DW >= 64) ? "fakeram7_dp_2048x64" : "fakeram7_dp_2048x32" :
      (AW >= 10) ? (DW >= 64) ? "fakeram7_dp_1024x64" : "fakeram7_dp_1024x32" :
      (AW >= 9) ? (DW >= 128) ? "fakeram7_dp_512x128" : (DW >= 64) ? "fakeram7_dp_512x64" : "fakeram7_dp_512x32" :
      (AW >= 8) ? (DW >= 64) ? "fakeram7_dp_256x64" : "fakeram7_dp_256x32" :
      "fakeram7_dp_128x32";

  localparam MEM_WIDTH = 
      (MEM_PROP == "fakeram7_dp_1024x32") ? 32 :
      (MEM_PROP == "fakeram7_dp_1024x64") ? 64 :
      (MEM_PROP == "fakeram7_dp_128x32") ? 32 :
      (MEM_PROP == "fakeram7_dp_2048x32") ? 32 :
      (MEM_PROP == "fakeram7_dp_2048x64") ? 64 :
      (MEM_PROP == "fakeram7_dp_256x32") ? 32 :
      (MEM_PROP == "fakeram7_dp_256x64") ? 64 :
      (MEM_PROP == "fakeram7_dp_4096x32") ? 32 :
      (MEM_PROP == "fakeram7_dp_4096x64") ? 64 :
      (MEM_PROP == "fakeram7_dp_512x128") ? 128 :
      (MEM_PROP == "fakeram7_dp_512x32") ? 32 :
      (MEM_PROP == "fakeram7_dp_512x64") ? 64 :
      (MEM_PROP == "fakeram7_dp_8192x32") ? 32 :
      (MEM_PROP == "fakeram7_dp_8192x64") ? 64 :
      0;

  localparam MEM_DEPTH = 
      (MEM_PROP == "fakeram7_dp_1024x32") ? 10 :
      (MEM_PROP == "fakeram7_dp_1024x64") ? 10 :
      (MEM_PROP == "fakeram7_dp_128x32") ? 7 :
      (MEM_PROP == "fakeram7_dp_2048x32") ? 11 :
      (MEM_PROP == "fakeram7_dp_2048x64") ? 11 :
      (MEM_PROP == "fakeram7_dp_256x32") ? 8 :
      (MEM_PROP == "fakeram7_dp_256x64") ? 8 :
      (MEM_PROP == "fakeram7_dp_4096x32") ? 12 :
      (MEM_PROP == "fakeram7_dp_4096x64") ? 12 :
      (MEM_PROP == "fakeram7_dp_512x128") ? 9 :
      (MEM_PROP == "fakeram7_dp_512x32") ? 9 :
      (MEM_PROP == "fakeram7_dp_512x64") ? 9 :
      (MEM_PROP == "fakeram7_dp_8192x32") ? 13 :
      (MEM_PROP == "fakeram7_dp_8192x64") ? 13 :
      0;

  generate
    if (MEM_PROP == "SOFT") begin : isoft
      la_dpram_impl #(
          .DW(DW),
          .AW(AW),
          .PROP(PROP),
          .CTRLW(CTRLW),
          .TESTW(TESTW)
      ) memory (
          .clk(clk),
          .ce(ce),
          .we(we),
          .wmask(wmask),
          .addr(addr),
          .din(din),
          .dout(dout),
          .vss(vss),
          .vdd(vdd),
          .vddio(vddio),
          .ctrl(ctrl),
          .test(test)
      );
    end
    if (MEM_PROP != "SOFT") begin : itech
      // Create memories
      localparam MEM_ADDRS = 2 ** (AW - MEM_DEPTH) < 1 ? 1 : 2 ** (AW - MEM_DEPTH);



      genvar o;
      for (o = 0; o < DW; o = o + 1) begin : OUTPUTS
        wire [MEM_ADDRS-1:0] mem_outputs;
        assign rd_dout[o] = |mem_outputs;
      end

      genvar a;
      for (a = 0; a < MEM_ADDRS; a = a + 1) begin : ADDR
        wire we_selected;
        wire re_selected;
        wire [MEM_DEPTH-1:0] wr_mem_addr;
        wire [MEM_DEPTH-1:0] rd_mem_addr;

        if (MEM_ADDRS == 1) begin : FITS
          assign we_selected = 1'b1;
          assign re_selected = 1'b1;
          assign wr_mem_addr = wr_addr;
          assign rd_mem_addr = rd_addr;
        end else begin : NOFITS
          assign we_selected = wr_addr[AW-1:MEM_DEPTH] == a;
          assign re_selected = rd_addr[AW-1:MEM_DEPTH] == a;
          assign wr_mem_addr = wr_addr[MEM_DEPTH-1:0];
          assign rd_mem_addr = rd_addr[MEM_DEPTH-1:0];
        end

        genvar n;
        for (n = 0; n < DW; n = n + MEM_WIDTH) begin : WORD
          wire [MEM_WIDTH-1:0] mem_din;
          wire [MEM_WIDTH-1:0] mem_dout;
          wire [MEM_WIDTH-1:0] mem_wmask;

          genvar i;
          for (i = 0; i < MEM_WIDTH; i = i + 1) begin : WORD_SELECT
            if (n + i < DW) begin : ACTIVE
              assign mem_din[i] = wr_din[n+i];
              assign mem_wmask[i] = wr_wmask[n+i];
              assign OUTPUTS[n+i].mem_outputs[a] = re_selected ? mem_dout[i] : 1'b0;
            end else begin : INACTIVE
              assign mem_din[i]   = 1'b0;
              assign mem_wmask[i] = 1'b0;
            end
          end

          wire wr_ce_in;
          wire rd_ce_in;
          wire we_in;
          assign wr_ce_in = wr_ce && we_selected;
          assign rd_ce_in = rd_ce && re_selected;
          assign we_in = wr_we && we_selected;

          if (MEM_PROP == "fakeram7_dp_512x32") begin : ifakeram7_dp_512x32
            fakeram7_dp_512x32 memory (
                .addr_in_A(wr_mem_addr),
                .addr_in_B(rd_mem_addr),
                .ce_in(wr_ce_in | rd_ce_in),
                .clk(wr_clk),
                .rd_out_A(),
                .rd_out_B(mem_dout),
                .w_mask_in_A(mem_wmask),
                .w_mask_in_B('b0),
                .wd_in_A(mem_din),
                .wd_in_B('b0),
                .we_in_A(we_in),
                .we_in_B(1'b0)
            );
          end
          if (MEM_PROP == "fakeram7_dp_512x64") begin : ifakeram7_dp_512x64
            fakeram7_dp_512x64 memory (
                .addr_in_A(wr_mem_addr),
                .addr_in_B(rd_mem_addr),
                .ce_in(wr_ce_in | rd_ce_in),
                .clk(wr_clk),
                .rd_out_A(),
                .rd_out_B(mem_dout),
                .w_mask_in_A(mem_wmask),
                .w_mask_in_B('b0),
                .wd_in_A(mem_din),
                .wd_in_B('b0),
                .we_in_A(we_in),
                .we_in_B(1'b0)
            );
          end
          if (MEM_PROP == "fakeram7_dp_512x128") begin : ifakeram7_dp_512x128
            fakeram7_dp_512x128 memory (
                .addr_in_A(wr_mem_addr),
                .addr_in_B(rd_mem_addr),
                .ce_in(wr_ce_in | rd_ce_in),
                .clk(wr_clk),
                .rd_out_A(),
                .rd_out_B(mem_dout),
                .w_mask_in_A(mem_wmask),
                .w_mask_in_B('b0),
                .wd_in_A(mem_din),
                .wd_in_B('b0),
                .we_in_A(we_in),
                .we_in_B(1'b0)
            );
          end
          if (MEM_PROP == "fakeram7_dp_256x64") begin : ifakeram7_dp_256x64
            fakeram7_dp_256x64 memory (
                .addr_in_A(wr_mem_addr),
                .addr_in_B(rd_mem_addr),
                .ce_in(wr_ce_in | rd_ce_in),
                .clk(wr_clk),
                .rd_out_A(),
                .rd_out_B(mem_dout),
                .w_mask_in_A(mem_wmask),
                .w_mask_in_B('b0),
                .wd_in_A(mem_din),
                .wd_in_B('b0),
                .we_in_A(we_in),
                .we_in_B(1'b0)
            );
          end
          if (MEM_PROP == "fakeram7_dp_256x32") begin : ifakeram7_dp_256x32
            fakeram7_dp_256x32 memory (
                .addr_in_A(wr_mem_addr),
                .addr_in_B(rd_mem_addr),
                .ce_in(wr_ce_in | rd_ce_in),
                .clk(wr_clk),
                .rd_out_A(),
                .rd_out_B(mem_dout),
                .w_mask_in_A(mem_wmask),
                .w_mask_in_B('b0),
                .wd_in_A(mem_din),
                .wd_in_B('b0),
                .we_in_A(we_in),
                .we_in_B(1'b0)
            );
          end
          if (MEM_PROP == "fakeram7_dp_128x32") begin : ifakeram7_dp_128x32
            fakeram7_dp_128x32 memory (
                .addr_in_A(wr_mem_addr),
                .addr_in_B(rd_mem_addr),
                .ce_in(wr_ce_in | rd_ce_in),
                .clk(wr_clk),
                .rd_out_A(),
                .rd_out_B(mem_dout),
                .w_mask_in_A(mem_wmask),
                .w_mask_in_B('b0),
                .wd_in_A(mem_din),
                .wd_in_B('b0),
                .we_in_A(we_in),
                .we_in_B(1'b0)
            );
          end
          if (MEM_PROP == "fakeram7_dp_1024x32") begin : ifakeram7_dp_1024x32
            fakeram7_dp_1024x32 memory (
                .addr_in_A(wr_mem_addr),
                .addr_in_B(rd_mem_addr),
                .ce_in(wr_ce_in | rd_ce_in),
                .clk(wr_clk),
                .rd_out_A(),
                .rd_out_B(mem_dout),
                .w_mask_in_A(mem_wmask),
                .w_mask_in_B('b0),
                .wd_in_A(mem_din),
                .wd_in_B('b0),
                .we_in_A(we_in),
                .we_in_B(1'b0)
            );
          end
          if (MEM_PROP == "fakeram7_dp_1024x64") begin : ifakeram7_dp_1024x64
            fakeram7_dp_1024x64 memory (
                .addr_in_A(wr_mem_addr),
                .addr_in_B(rd_mem_addr),
                .ce_in(wr_ce_in | rd_ce_in),
                .clk(wr_clk),
                .rd_out_A(),
                .rd_out_B(mem_dout),
                .w_mask_in_A(mem_wmask),
                .w_mask_in_B('b0),
                .wd_in_A(mem_din),
                .wd_in_B('b0),
                .we_in_A(we_in),
                .we_in_B(1'b0)
            );
          end
          if (MEM_PROP == "fakeram7_dp_2048x32") begin : ifakeram7_dp_2048x32
            fakeram7_dp_2048x32 memory (
                .addr_in_A(wr_mem_addr),
                .addr_in_B(rd_mem_addr),
                .ce_in(wr_ce_in | rd_ce_in),
                .clk(wr_clk),
                .rd_out_A(),
                .rd_out_B(mem_dout),
                .w_mask_in_A(mem_wmask),
                .w_mask_in_B('b0),
                .wd_in_A(mem_din),
                .wd_in_B('b0),
                .we_in_A(we_in),
                .we_in_B(1'b0)
            );
          end
          if (MEM_PROP == "fakeram7_dp_2048x64") begin : ifakeram7_dp_2048x64
            fakeram7_dp_2048x64 memory (
                .addr_in_A(wr_mem_addr),
                .addr_in_B(rd_mem_addr),
                .ce_in(wr_ce_in | rd_ce_in),
                .clk(wr_clk),
                .rd_out_A(),
                .rd_out_B(mem_dout),
                .w_mask_in_A(mem_wmask),
                .w_mask_in_B('b0),
                .wd_in_A(mem_din),
                .wd_in_B('b0),
                .we_in_A(we_in),
                .we_in_B(1'b0)
            );
          end
          if (MEM_PROP == "fakeram7_dp_4096x32") begin : ifakeram7_dp_4096x32
            fakeram7_dp_4096x32 memory (
                .addr_in_A(wr_mem_addr),
                .addr_in_B(rd_mem_addr),
                .ce_in(wr_ce_in | rd_ce_in),
                .clk(wr_clk),
                .rd_out_A(),
                .rd_out_B(mem_dout),
                .w_mask_in_A(mem_wmask),
                .w_mask_in_B('b0),
                .wd_in_A(mem_din),
                .wd_in_B('b0),
                .we_in_A(we_in),
                .we_in_B(1'b0)
            );
          end
          if (MEM_PROP == "fakeram7_dp_4096x64") begin : ifakeram7_dp_4096x64
            fakeram7_dp_4096x64 memory (
                .addr_in_A(wr_mem_addr),
                .addr_in_B(rd_mem_addr),
                .ce_in(wr_ce_in | rd_ce_in),
                .clk(wr_clk),
                .rd_out_A(),
                .rd_out_B(mem_dout),
                .w_mask_in_A(mem_wmask),
                .w_mask_in_B('b0),
                .wd_in_A(mem_din),
                .wd_in_B('b0),
                .we_in_A(we_in),
                .we_in_B(1'b0)
            );
          end
          if (MEM_PROP == "fakeram7_dp_8192x32") begin : ifakeram7_dp_8192x32
            fakeram7_dp_8192x32 memory (
                .addr_in_A(wr_mem_addr),
                .addr_in_B(rd_mem_addr),
                .ce_in(wr_ce_in | rd_ce_in),
                .clk(wr_clk),
                .rd_out_A(),
                .rd_out_B(mem_dout),
                .w_mask_in_A(mem_wmask),
                .w_mask_in_B('b0),
                .wd_in_A(mem_din),
                .wd_in_B('b0),
                .we_in_A(we_in),
                .we_in_B(1'b0)
            );
          end
          if (MEM_PROP == "fakeram7_dp_8192x64") begin : ifakeram7_dp_8192x64
            fakeram7_dp_8192x64 memory (
                .addr_in_A(wr_mem_addr),
                .addr_in_B(rd_mem_addr),
                .ce_in(wr_ce_in | rd_ce_in),
                .clk(wr_clk),
                .rd_out_A(),
                .rd_out_B(mem_dout),
                .w_mask_in_A(mem_wmask),
                .w_mask_in_B('b0),
                .wd_in_A(mem_din),
                .wd_in_B('b0),
                .we_in_A(we_in),
                .we_in_B(1'b0)
            );
          end
        end
      end
    end
  endgenerate
endmodule
