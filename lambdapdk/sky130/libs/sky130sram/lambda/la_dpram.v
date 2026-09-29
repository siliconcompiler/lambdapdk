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
 * synthesizable model does not implement the ctrl interface and should
 * only be used for basic testing and for synthesizing for FPGA devices.
 * Advanced ASIC development should rely on complete functional models
 * supplied on a per macro basis.
 *
 * Technology specific implementations of "la_dpram" would generally include
 * one or more hardcoded instantiations of la_dpram modules with a generate
 * statement relying on the "PROP" to select between the list of modules
 * at build time.
 *
 ****************************************************************************/

(* keep_hierarchy *)
module la_dpram #(
    parameter DW       = 32,         // Memory width
    parameter AW       = 10,         // Address width (derived)
    parameter BYTEMASK = 0,          // 1=byte mask, 0=bit mask
    parameter PROP     = "DEFAULT",  // Pass through variable for hard macro
    parameter CTRLW    = 32,         // Width of ctrl interface
    parameter STATUSW  = 32          // Width of status interface
) (  // Memory interface
     // Write port
    input wr_clk,  // write clock
    input wr_ce,  // write chip-enable
    input wr_we,  // write enable
    input [(BYTEMASK?DW/8 : DW)-1:0] wr_wmask,  // bit or byte write mask
    input [AW-1:0] wr_addr,  // write address
    input [DW-1:0] wr_din,  //write data in
    // Read port
    input rd_clk,  // read clock
    input rd_ce,  // read chip-enable
    input [AW-1:0] rd_addr,  // read address
    output [DW-1:0] rd_dout,  //read data out
    // Technology interfaces
    input selctrl,  // selects control interface
    input [CTRLW-1:0] ctrl,  // pass through control interface
    output [STATUSW-1:0] status  // pass through status interface
);

  // Total number of bits
  localparam TOTAL_BITS = (2 ** AW) * DW;

  // Determine which memory to select
  //verilator lint_off WIDTHEXPAND
  localparam MEM_PROP = (PROP != "DEFAULT") ? PROP :
      (AW >= 10) ? "sky130_sram_1kbyte_1rw1r_8x1024_8" :
      (AW >= 9) ? "sky130_sram_2kbyte_1rw1r_32x512_8" :
      "sky130_sram_1kbyte_1rw1r_32x256_8";
  //verilator lint_on WIDTHEXPAND

  localparam MEM_WIDTH = 
      (MEM_PROP == "sky130_sram_1kbyte_1rw1r_32x256_8") ? 32 :
      (MEM_PROP == "sky130_sram_1kbyte_1rw1r_8x1024_8") ? 8 :
      (MEM_PROP == "sky130_sram_2kbyte_1rw1r_32x512_8") ? 32 :
      0;

  localparam MEM_DEPTH = 
      (MEM_PROP == "sky130_sram_1kbyte_1rw1r_32x256_8") ? 8 :
      (MEM_PROP == "sky130_sram_1kbyte_1rw1r_8x1024_8") ? 10 :
      (MEM_PROP == "sky130_sram_2kbyte_1rw1r_32x512_8") ? 9 :
      0;

  generate
    if (MEM_PROP == "SOFT") begin : isoft
      la_dpram_impl #(
          .DW(DW),
          .AW(AW),
          .BYTEMASK(BYTEMASK),
          .PROP(PROP),
          .CTRLW(CTRLW),
          .STATUSW(STATUSW)
      ) memory (
          // Write port
          .wr_clk(wr_clk),
          .wr_ce(wr_ce),
          .wr_we(wr_we),
          .wr_wmask(wr_wmask),
          .wr_addr(wr_addr),
          .wr_din(wr_din),
          // Read port
          .rd_clk(rd_clk),
          .rd_ce(rd_ce),
          .rd_addr(rd_addr),
          .rd_dout(rd_dout),
          // Technology interfaces
          .selctrl(selctrl),
          .ctrl(ctrl),
          .status(status)
      );
    end
    if (MEM_PROP != "SOFT") begin : itech
      // Create memories
      // When AW < MEM_DEPTH, force single-macro case (MEM_ADDRS = 1)
      localparam MEM_ADDRS = (AW >= MEM_DEPTH) ? 2 ** (AW - MEM_DEPTH) : 1;

      // Generate a single bitmask
      wire [DW-1:0] wr_wmask_int;
      genvar gwm;
      if (BYTEMASK) begin : g_wm_byte
        for (gwm = 0; gwm < DW / 8; gwm = gwm + 1) begin : g_wm_lane
          assign wr_wmask_int[gwm*8+:8] = {8{wr_wmask[gwm]}};
        end
      end else begin : g_wm_bit
        assign wr_wmask_int = wr_wmask;
      end

      genvar o;
      for (o = 0; o < DW; o = o + 1) begin : OUTPUTS
        wire [MEM_ADDRS-1:0] mem_outputs;
        assign rd_dout[o] = |mem_outputs;
      end

      genvar a;
      for (a = 0; a < MEM_ADDRS; a = a + 1) begin : ADDR
        wire we_selected;
        wire re_selected;
        reg re_selected_reg;
        wire [MEM_DEPTH-1:0] wr_mem_addr;
        wire [MEM_DEPTH-1:0] rd_mem_addr;

        if (MEM_ADDRS == 1) begin : FITS
          assign we_selected = 1'b1;
          assign re_selected = 1'b1;
          // Handle address width mismatch for write
          if (AW > MEM_DEPTH) begin : ADDR_TRUNCATE_WR
            assign wr_mem_addr = wr_addr[MEM_DEPTH-1:0];
          end
          if (AW == MEM_DEPTH) begin : ADDR_MATCH_WR
            assign wr_mem_addr = wr_addr;
          end
          if (AW < MEM_DEPTH) begin : ADDR_EXTEND_WR
            // Single-macro forced case: zero-extend address to macro width
            assign wr_mem_addr = {{(MEM_DEPTH - AW) {1'b0}}, wr_addr};
          end
          // Handle address width mismatch for read
          if (AW > MEM_DEPTH) begin : ADDR_TRUNCATE_RD
            assign rd_mem_addr = rd_addr[MEM_DEPTH-1:0];
          end
          if (AW == MEM_DEPTH) begin : ADDR_MATCH_RD
            assign rd_mem_addr = rd_addr;
          end
          if (AW < MEM_DEPTH) begin : ADDR_EXTEND_RD
            // Single-macro forced case: zero-extend address to macro width
            assign rd_mem_addr = {{(MEM_DEPTH - AW) {1'b0}}, rd_addr};
          end
        end else begin : NOFITS
          assign we_selected = wr_addr[AW-1:MEM_DEPTH] == a;
          assign re_selected = rd_addr[AW-1:MEM_DEPTH] == a;
          assign wr_mem_addr = wr_addr[MEM_DEPTH-1:0];
          assign rd_mem_addr = rd_addr[MEM_DEPTH-1:0];
        end

        always @(posedge rd_clk) begin
          re_selected_reg <= re_selected;
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
              assign mem_wmask[i] = wr_wmask_int[n+i];
              assign OUTPUTS[n+i].mem_outputs[a] = re_selected_reg ? mem_dout[i] : 1'b0;
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

          if (MEM_PROP == "sky130_sram_1kbyte_1rw1r_32x256_8") begin: isky130_sram_1kbyte_1rw1r_32x256_8
            wire [0:0] mem_ctrl;
            assign mem_ctrl = selctrl ? ctrl[0:0] : 1'b0;
            sky130_sram_1kbyte_1rw1r_32x256_8 memory (
                .addr0 (wr_mem_addr),
                .addr1 (rd_mem_addr),
                .clk0  (wr_clk),
                .clk1  (rd_clk),
                .csb0  (~wr_ce_in),
                .csb1  (~rd_ce_in),
                .din0  (mem_din),
                .dout0 (),
                .dout1 (mem_dout),
                .web0  (~we_in),
                .wmask0({mem_wmask[24], mem_wmask[16], mem_wmask[8], mem_wmask[0]})
            );
          end
          if (MEM_PROP == "sky130_sram_1kbyte_1rw1r_8x1024_8") begin: isky130_sram_1kbyte_1rw1r_8x1024_8
            wire [0:0] mem_ctrl;
            assign mem_ctrl = selctrl ? ctrl[0:0] : 1'b0;
            sky130_sram_1kbyte_1rw1r_8x1024_8 memory (
                .addr0 (wr_mem_addr),
                .addr1 (rd_mem_addr),
                .clk0  (wr_clk),
                .clk1  (rd_clk),
                .csb0  (~wr_ce_in),
                .csb1  (~rd_ce_in),
                .din0  (mem_din),
                .dout0 (),
                .dout1 (mem_dout),
                .web0  (~we_in),
                .wmask0(mem_wmask[0])
            );
          end
          if (MEM_PROP == "sky130_sram_2kbyte_1rw1r_32x512_8") begin: isky130_sram_2kbyte_1rw1r_32x512_8
            wire [0:0] mem_ctrl;
            assign mem_ctrl = selctrl ? ctrl[0:0] : 1'b0;
            sky130_sram_2kbyte_1rw1r_32x512_8 memory (
                .addr0 (wr_mem_addr),
                .addr1 (rd_mem_addr),
                .clk0  (wr_clk),
                .clk1  (rd_clk),
                .csb0  (~wr_ce_in),
                .csb1  (~rd_ce_in),
                .din0  (mem_din),
                .dout0 (),
                .dout1 (mem_dout),
                .web0  (~we_in),
                .wmask0({mem_wmask[24], mem_wmask[16], mem_wmask[8], mem_wmask[0]})
            );
          end
        end
      end
      // Drive status to zero by default for tech-specific memories
      assign status = {STATUSW{1'b0}};
    end
  endgenerate

endmodule
