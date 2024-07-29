/*****************************************************************************
 * Function: Single Port ram
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
 * Technologoy specific implementations of "la_spram" would generally include
 * one ore more hardcoded instantiations of ram modules with a generate
 * statement relying on the "PROP" to select between the list of modules
 * at build time.
 *
 ****************************************************************************/

module la_spram
  #(parameter DW     = 32,          // Memory width
    parameter AW     = 10,          // Address width (derived)
    parameter PROP   = "DEFAULT",   // Pass through variable for hard macro
    parameter CTRLW  = 128,         // Width of asic ctrl interface
    parameter TESTW  = 128          // Width of asic test interface
    )
   (// Memory interface
    input clk, // write clock
    input ce, // chip enable
    input we, // write enable
    input [DW-1:0] wmask, //per bit write mask
    input [AW-1:0] addr, //write address
    input [DW-1:0] din, //write data
    output [DW-1:0] dout, //read output data
    // Power signals
    input vss, // ground signal
    input vdd, // memory core array power
    input vddio, // periphery/io power
    // Generic interfaces
    input [CTRLW-1:0] ctrl, // pass through ASIC control interface
    input [TESTW-1:0] test // pass through ASIC test interface
    );

    // Determine which memory to select
    localparam MEM_PROP = (PROP != "DEFAULT") ? PROP :
      "sky130_sram_1rw1r_64x256_8";

    localparam MEM_WIDTH = 
      (MEM_PROP == "sky130_sram_1rw1r_64x256_8") ? 64 :
      0;
 
    localparam MEM_DEPTH = 
      (MEM_PROP == "sky130_sram_1rw1r_64x256_8") ? 8 :
      0;

    // Create memories
    localparam MEM_ADDRS = 2**(AW - MEM_DEPTH) < 1 ? 1 : 2**(AW - MEM_DEPTH);

    

    generate
      genvar o;
      for (o = 0; o < DW; o = o + 1) begin: OUTPUTS
        wire [MEM_ADDRS-1:0] mem_outputs;
        assign dout[o] = |mem_outputs;
      end

      genvar a;
      for (a = 0; a < MEM_ADDRS; a = a + 1) begin: ADDR
        wire selected;
        wire [MEM_DEPTH-1:0] mem_addr;

        if (MEM_ADDRS == 1) begin: FITS
          assign selected = 1'b1;
          assign mem_addr = addr;
        end else begin: NOFITS
          assign selected = addr[AW-1:MEM_DEPTH] == a;
          assign mem_addr = addr[MEM_DEPTH-1:0];
        end

        genvar n;
        for (n = 0; n < DW; n = n + MEM_WIDTH) begin: WORD
          wire [MEM_WIDTH-1:0] mem_din;
          wire [MEM_WIDTH-1:0] mem_dout;
          wire [MEM_WIDTH-1:0] mem_wmask;

          genvar i;
          for (i = 0; i < MEM_WIDTH; i = i + 1) begin: WORD_SELECT
            if (n + i < DW) begin: ACTIVE
              assign mem_din[i] = din[n + i];
              assign mem_wmask[i] = wmask[n + i];
              assign OUTPUTS[n + i].mem_outputs[a] = selected ? mem_dout[i] : 1'b0;
            end
            else begin: INACTIVE
              assign mem_din[i] = 1'b0;
              assign mem_wmask[i] = 1'b0;
            end
          end

          wire ce_in;
          wire we_in;
          assign ce_in = ce && selected;
          assign we_in = we && selected;
          
          if (MEM_PROP == "sky130_sram_1rw1r_64x256_8") begin: isky130_sram_1rw1r_64x256_8
            sky130_sram_1rw1r_64x256_8 memory (
              .addr0(mem_addr),
              .addr1(mem_addr),
              .clk0(clk),
              .clk1(clk),
              .csb0(ce_in && we_in),
              .csb1(ce_in && ~we_in),
              .din0(mem_din),
              .dout0(),
              .dout1(mem_dout),
              .web0(ce_in && we_in),
              .wmask0({mem_wmask[24], mem_wmask[16], mem_wmask[8], mem_wmask[0]})
            );
          end
        end
      end
    endgenerate
endmodule