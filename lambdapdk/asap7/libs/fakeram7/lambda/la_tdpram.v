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

module la_tdpram #(
    parameter DW    = 32,         // Memory width
    parameter AW    = 10,         // Address width (derived)
    parameter PROP  = "DEFAULT",  // Pass through variable for hard macro
    parameter CTRLW = 128,        // Width of asic ctrl interface
    parameter TESTW = 128         // Width of asic test interface
) (  // Memory interface
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
      (AW >= 13) ? (DW >= 64) ? "fakeram7_tdp_8192x64" : "fakeram7_tdp_8192x32" :
      (AW >= 12) ? (DW >= 64) ? "fakeram7_tdp_4096x64" : "fakeram7_tdp_4096x32" :
      (AW >= 11) ? (DW >= 64) ? "fakeram7_tdp_2048x64" : "fakeram7_tdp_2048x32" :
      (AW >= 10) ? (DW >= 64) ? "fakeram7_tdp_1024x64" : "fakeram7_tdp_1024x32" :
      (AW >= 9) ? (DW >= 128) ? "fakeram7_tdp_512x128" : (DW >= 64) ? "fakeram7_tdp_512x64" : "fakeram7_tdp_512x32" :
      (AW >= 8) ? (DW >= 64) ? "fakeram7_tdp_256x64" : "fakeram7_tdp_256x32" :
      "fakeram7_tdp_128x32";

  localparam MEM_WIDTH = 
      (MEM_PROP == "fakeram7_tdp_1024x32") ? 32 :
      (MEM_PROP == "fakeram7_tdp_1024x64") ? 64 :
      (MEM_PROP == "fakeram7_tdp_128x32") ? 32 :
      (MEM_PROP == "fakeram7_tdp_2048x32") ? 32 :
      (MEM_PROP == "fakeram7_tdp_2048x64") ? 64 :
      (MEM_PROP == "fakeram7_tdp_256x32") ? 32 :
      (MEM_PROP == "fakeram7_tdp_256x64") ? 64 :
      (MEM_PROP == "fakeram7_tdp_4096x32") ? 32 :
      (MEM_PROP == "fakeram7_tdp_4096x64") ? 64 :
      (MEM_PROP == "fakeram7_tdp_512x128") ? 128 :
      (MEM_PROP == "fakeram7_tdp_512x32") ? 32 :
      (MEM_PROP == "fakeram7_tdp_512x64") ? 64 :
      (MEM_PROP == "fakeram7_tdp_8192x32") ? 32 :
      (MEM_PROP == "fakeram7_tdp_8192x64") ? 64 :
      0;

  localparam MEM_DEPTH = 
      (MEM_PROP == "fakeram7_tdp_1024x32") ? 10 :
      (MEM_PROP == "fakeram7_tdp_1024x64") ? 10 :
      (MEM_PROP == "fakeram7_tdp_128x32") ? 7 :
      (MEM_PROP == "fakeram7_tdp_2048x32") ? 11 :
      (MEM_PROP == "fakeram7_tdp_2048x64") ? 11 :
      (MEM_PROP == "fakeram7_tdp_256x32") ? 8 :
      (MEM_PROP == "fakeram7_tdp_256x64") ? 8 :
      (MEM_PROP == "fakeram7_tdp_4096x32") ? 12 :
      (MEM_PROP == "fakeram7_tdp_4096x64") ? 12 :
      (MEM_PROP == "fakeram7_tdp_512x128") ? 9 :
      (MEM_PROP == "fakeram7_tdp_512x32") ? 9 :
      (MEM_PROP == "fakeram7_tdp_512x64") ? 9 :
      (MEM_PROP == "fakeram7_tdp_8192x32") ? 13 :
      (MEM_PROP == "fakeram7_tdp_8192x64") ? 13 :
      0;

  generate
    if (MEM_PROP == "SOFT") begin : isoft
      la_tdpram_impl #(
          .DW(DW),
          .AW(AW),
          .PROP(PROP),
          .CTRLW(CTRLW),
          .TESTW(TESTW)
      ) memory (
          .clk_a(clk_a),
          .ce_a(ce_a),
          .we_a(we_a),
          .wmask_a(wmask_a),
          .addr_a(addr_a),
          .din_a(din_a),
          .dout_a(dout_a),
          .clk_b(clk_b),
          .ce_b(ce_b),
          .we_b(we_b),
          .wmask_b(wmask_b),
          .addr_b(addr_b),
          .din_b(din_b),
          .dout_b(dout_b),
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
        wire [MEM_ADDRS-1:0] mem_outputsA;
        assign dout_a[o] = |mem_outputsA;
        wire [MEM_ADDRS-1:0] mem_outputsB;
        assign dout_b[o] = |mem_outputsB;
      end

      genvar a;
      for (a = 0; a < MEM_ADDRS; a = a + 1) begin : ADDR
        wire selectedA;
        wire selectedB;
        wire [MEM_DEPTH-1:0] mem_addrA;
        wire [MEM_DEPTH-1:0] mem_addrB;

        if (MEM_ADDRS == 1) begin : FITS
          assign selectedA = 1'b1;
          assign selectedB = 1'b1;
          assign mem_addrA = addr_a;
          assign mem_addrB = addr_b;
        end else begin : NOFITS
          assign selectedA = addr_a[AW-1:MEM_DEPTH] == a;
          assign selectedB = addr_b[AW-1:MEM_DEPTH] == a;
          assign mem_addrA = addr_a[MEM_DEPTH-1:0];
          assign mem_addrB = addr_b[MEM_DEPTH-1:0];
        end

        genvar n;
        for (n = 0; n < DW; n = n + MEM_WIDTH) begin : WORD
          wire [MEM_WIDTH-1:0] mem_dinA;
          wire [MEM_WIDTH-1:0] mem_doutA;
          wire [MEM_WIDTH-1:0] mem_wmaskA;
          wire [MEM_WIDTH-1:0] mem_dinB;
          wire [MEM_WIDTH-1:0] mem_doutB;
          wire [MEM_WIDTH-1:0] mem_wmaskB;

          genvar i;
          for (i = 0; i < MEM_WIDTH; i = i + 1) begin : WORD_SELECT
            if (n + i < DW) begin : ACTIVE
              assign mem_dinA[i] = din_a[n+i];
              assign mem_wmaskA[i] = wmask_a[n+i];
              assign OUTPUTS[n+i].mem_outputsA[a] = selectedA ? mem_doutA[i] : 1'b0;
              assign mem_dinB[i] = din_b[n+i];
              assign mem_wmaskB[i] = wmask_b[n+i];
              assign OUTPUTS[n+i].mem_outputsB[a] = selectedB ? mem_doutB[i] : 1'b0;
            end else begin : INACTIVE
              assign mem_dinA[i]   = 1'b0;
              assign mem_wmaskA[i] = 1'b0;
              assign mem_dinB[i]   = 1'b0;
              assign mem_wmaskB[i] = 1'b0;
            end
          end

          wire ce_in_A;
          wire ce_in_B;
          wire we_in_A;
          wire we_in_B;
          assign ce_in_A = ce_a && selectedA;
          assign ce_in_B = ce_b && selectedB;
          assign we_in_A = we_a && selectedA;
          assign we_in_B = we_b && selectedB;

          if (MEM_PROP == "fakeram7_tdp_512x32") begin : ifakeram7_tdp_512x32
            fakeram7_tdp_512x32 memory (
                .addr_in_A(mem_addrA),
                .addr_in_B(mem_addrB),
                .ce_in_A(ce_in_A), .ce_in_B(ce_in_B),
                .clk_A(clk_a), .clk_B(clk_b),
                .rd_out_A(mem_doutA),
                .rd_out_B(mem_doutB),
                .w_mask_in_A(mem_wmaskA),
                .w_mask_in_B(mem_wmaskB),
                .wd_in_A(mem_dinA),
                .wd_in_B(mem_dinB),
                .we_in_A(we_in_A),
                .we_in_B(we_in_B),
            );
          end
          if (MEM_PROP == "fakeram7_tdp_512x64") begin : ifakeram7_tdp_512x64
            fakeram7_tdp_512x64 memory (
                .addr_in_A(mem_addrA),
                .addr_in_B(mem_addrB),
                .ce_in_A(ce_in_A), .ce_in_B(ce_in_B),
                .clk_A(clk_a), .clk_B(clk_b),
                .rd_out_A(mem_doutA),
                .rd_out_B(mem_doutB),
                .w_mask_in_A(mem_wmaskA),
                .w_mask_in_B(mem_wmaskB),
                .wd_in_A(mem_dinA),
                .wd_in_B(mem_dinB),
                .we_in_A(we_in_A),
                .we_in_B(we_in_B),
            );
          end
          if (MEM_PROP == "fakeram7_tdp_512x128") begin : ifakeram7_tdp_512x128
            fakeram7_tdp_512x128 memory (
                .addr_in_A(mem_addrA),
                .addr_in_B(mem_addrB),
                .ce_in_A(ce_in_A), .ce_in_B(ce_in_B),
                .clk_A(clk_a), .clk_B(clk_b),
                .rd_out_A(mem_doutA),
                .rd_out_B(mem_doutB),
                .w_mask_in_A(mem_wmaskA),
                .w_mask_in_B(mem_wmaskB),
                .wd_in_A(mem_dinA),
                .wd_in_B(mem_dinB),
                .we_in_A(we_in_A),
                .we_in_B(we_in_B),
            );
          end
          if (MEM_PROP == "fakeram7_tdp_256x64") begin : ifakeram7_tdp_256x64
            fakeram7_tdp_256x64 memory (
                .addr_in_A(mem_addrA),
                .addr_in_B(mem_addrB),
                .ce_in_A(ce_in_A), .ce_in_B(ce_in_B),
                .clk_A(clk_a), .clk_B(clk_b),
                .rd_out_A(mem_doutA),
                .rd_out_B(mem_doutB),
                .w_mask_in_A(mem_wmaskA),
                .w_mask_in_B(mem_wmaskB),
                .wd_in_A(mem_dinA),
                .wd_in_B(mem_dinB),
                .we_in_A(we_in_A),
                .we_in_B(we_in_B),
            );
          end
          if (MEM_PROP == "fakeram7_tdp_256x32") begin : ifakeram7_tdp_256x32
            fakeram7_tdp_256x32 memory (
                .addr_in_A(mem_addrA),
                .addr_in_B(mem_addrB),
                .ce_in_A(ce_in_A), .ce_in_B(ce_in_B),
                .clk_A(clk_a), .clk_B(clk_b),
                .rd_out_A(mem_doutA),
                .rd_out_B(mem_doutB),
                .w_mask_in_A(mem_wmaskA),
                .w_mask_in_B(mem_wmaskB),
                .wd_in_A(mem_dinA),
                .wd_in_B(mem_dinB),
                .we_in_A(we_in_A),
                .we_in_B(we_in_B),
            );
          end
          if (MEM_PROP == "fakeram7_tdp_128x32") begin : ifakeram7_tdp_128x32
            fakeram7_tdp_128x32 memory (
                .addr_in_A(mem_addrA),
                .addr_in_B(mem_addrB),
                .ce_in_A(ce_in_A), .ce_in_B(ce_in_B),
                .clk_A(clk_a), .clk_B(clk_b),
                .rd_out_A(mem_doutA),
                .rd_out_B(mem_doutB),
                .w_mask_in_A(mem_wmaskA),
                .w_mask_in_B(mem_wmaskB),
                .wd_in_A(mem_dinA),
                .wd_in_B(mem_dinB),
                .we_in_A(we_in_A),
                .we_in_B(we_in_B),
            );
          end
          if (MEM_PROP == "fakeram7_tdp_1024x32") begin : ifakeram7_tdp_1024x32
            fakeram7_tdp_1024x32 memory (
                .addr_in_A(mem_addrA),
                .addr_in_B(mem_addrB),
                .ce_in_A(ce_in_A), .ce_in_B(ce_in_B),
                .clk_A(clk_a), .clk_B(clk_b),
                .rd_out_A(mem_doutA),
                .rd_out_B(mem_doutB),
                .w_mask_in_A(mem_wmaskA),
                .w_mask_in_B(mem_wmaskB),
                .wd_in_A(mem_dinA),
                .wd_in_B(mem_dinB),
                .we_in_A(we_in_A),
                .we_in_B(we_in_B),
            );
          end
          if (MEM_PROP == "fakeram7_tdp_1024x64") begin : ifakeram7_tdp_1024x64
            fakeram7_tdp_1024x64 memory (
                .addr_in_A(mem_addrA),
                .addr_in_B(mem_addrB),
                .ce_in_A(ce_in_A), .ce_in_B(ce_in_B),
                .clk_A(clk_a), .clk_B(clk_b),
                .rd_out_A(mem_doutA),
                .rd_out_B(mem_doutB),
                .w_mask_in_A(mem_wmaskA),
                .w_mask_in_B(mem_wmaskB),
                .wd_in_A(mem_dinA),
                .wd_in_B(mem_dinB),
                .we_in_A(we_in_A),
                .we_in_B(we_in_B),
            );
          end
          if (MEM_PROP == "fakeram7_tdp_2048x32") begin : ifakeram7_tdp_2048x32
            fakeram7_tdp_2048x32 memory (
                .addr_in_A(mem_addrA),
                .addr_in_B(mem_addrB),
                .ce_in_A(ce_in_A), .ce_in_B(ce_in_B),
                .clk_A(clk_a), .clk_B(clk_b),
                .rd_out_A(mem_doutA),
                .rd_out_B(mem_doutB),
                .w_mask_in_A(mem_wmaskA),
                .w_mask_in_B(mem_wmaskB),
                .wd_in_A(mem_dinA),
                .wd_in_B(mem_dinB),
                .we_in_A(we_in_A),
                .we_in_B(we_in_B),
            );
          end
          if (MEM_PROP == "fakeram7_tdp_2048x64") begin : ifakeram7_tdp_2048x64
            fakeram7_tdp_2048x64 memory (
                .addr_in_A(mem_addrA),
                .addr_in_B(mem_addrB),
                .ce_in_A(ce_in_A), .ce_in_B(ce_in_B),
                .clk_A(clk_a), .clk_B(clk_b),
                .rd_out_A(mem_doutA),
                .rd_out_B(mem_doutB),
                .w_mask_in_A(mem_wmaskA),
                .w_mask_in_B(mem_wmaskB),
                .wd_in_A(mem_dinA),
                .wd_in_B(mem_dinB),
                .we_in_A(we_in_A),
                .we_in_B(we_in_B),
            );
          end
          if (MEM_PROP == "fakeram7_tdp_4096x32") begin : ifakeram7_tdp_4096x32
            fakeram7_tdp_4096x32 memory (
                .addr_in_A(mem_addrA),
                .addr_in_B(mem_addrB),
                .ce_in_A(ce_in_A), .ce_in_B(ce_in_B),
                .clk_A(clk_a), .clk_B(clk_b),
                .rd_out_A(mem_doutA),
                .rd_out_B(mem_doutB),
                .w_mask_in_A(mem_wmaskA),
                .w_mask_in_B(mem_wmaskB),
                .wd_in_A(mem_dinA),
                .wd_in_B(mem_dinB),
                .we_in_A(we_in_A),
                .we_in_B(we_in_B),
            );
          end
          if (MEM_PROP == "fakeram7_tdp_4096x64") begin : ifakeram7_tdp_4096x64
            fakeram7_tdp_4096x64 memory (
                .addr_in_A(mem_addrA),
                .addr_in_B(mem_addrB),
                .ce_in_A(ce_in_A), .ce_in_B(ce_in_B),
                .clk_A(clk_a), .clk_B(clk_b),
                .rd_out_A(mem_doutA),
                .rd_out_B(mem_doutB),
                .w_mask_in_A(mem_wmaskA),
                .w_mask_in_B(mem_wmaskB),
                .wd_in_A(mem_dinA),
                .wd_in_B(mem_dinB),
                .we_in_A(we_in_A),
                .we_in_B(we_in_B),
            );
          end
          if (MEM_PROP == "fakeram7_tdp_8192x32") begin : ifakeram7_tdp_8192x32
            fakeram7_tdp_8192x32 memory (
                .addr_in_A(mem_addrA),
                .addr_in_B(mem_addrB),
                .ce_in_A(ce_in_A), .ce_in_B(ce_in_B),
                .clk_A(clk_a), .clk_B(clk_b),
                .rd_out_A(mem_doutA),
                .rd_out_B(mem_doutB),
                .w_mask_in_A(mem_wmaskA),
                .w_mask_in_B(mem_wmaskB),
                .wd_in_A(mem_dinA),
                .wd_in_B(mem_dinB),
                .we_in_A(we_in_A),
                .we_in_B(we_in_B),
            );
          end
          if (MEM_PROP == "fakeram7_tdp_8192x64") begin : ifakeram7_tdp_8192x64
            fakeram7_tdp_8192x64 memory (
                .addr_in_A(mem_addrA),
                .addr_in_B(mem_addrB),
                .ce_in_A(ce_in_A), .ce_in_B(ce_in_B),
                .clk_A(clk_a), .clk_B(clk_b),
                .rd_out_A(mem_doutA),
                .rd_out_B(mem_doutB),
                .w_mask_in_A(mem_wmaskA),
                .w_mask_in_B(mem_wmaskB),
                .wd_in_A(mem_dinA),
                .wd_in_B(mem_dinB),
                .we_in_A(we_in_A),
                .we_in_B(we_in_B),
            );
          end
        end
      end
    end
  endgenerate
endmodule
