module la_sram_1wr1rd
  #(parameter N      = 32,            // Memory width
    parameter DEPTH  = 32,            // Memory depth
    parameter TYPE   = "DEFAULT",     // pass through variable for hard macro
    parameter REG    = 1,             // adds pipeline stage to RAM
    parameter AW     = $clog2(DEPTH), // address width (derived)
    parameter CFGW   = 128,           // width of config interface
    parameter TESTW  = 128            // width of test interface
    )
   (// write port
    input 	      wr_clk, // write clock
    input 	      wr_ce, // write chip enable
    input 	      wr_we, // write enable
    input [N-1:0]     wr_wmask, // per bit write mask
    input [AW-1:0]    wr_addr,// write address
    input [N-1:0]     wr_din, // write data
    input [N-1:0]     wr_dout, // read back data
    // read port
    input 	      rd_clk, // read clock
    input 	      rd_ce, // read chip enable
    input [AW-1:0]    rd_addr,// read address
    output [N-1:0]    rd_dout,// read output data
    // Power signals
    input 	      vss, // ground signal
    input 	      vdd, // memory core array power
    input 	      vddio, // periphery/io power
    // Generic interfaces
    input [CFGW-1:0]  cfg, // generic config/test interface
    input [TESTW-1:0] test // generic test interface
    );

   generate
      if (TYPE == "sky130_sram_2kbyte_1rw1r_32x512_8")
	begin
	   sky130_sram_2kbyte_1rw1r_32x512_8
	     mem (// write port
		  .clk0(wr_clk),
		  .csb0(wr_ce),
		  .web0(wr_we),
		  .wmask0({wr_mask[24],
			   wr_mask[16],
			   wr_mask[8],
			   wr_mask[0]}),
		  .addr0(wr_addr[8:0]),
		  .din0(wr_din[31:0]),
		  .dout0(wr_dout[31:0]),
		  // read port
		  .clk1(rd_clk),
		  .csb1(rd_ce),
		  .addr1(rd_addr[8:0]),
		  .dout1(rd_dout[31:0]),
		  // power
		  .vccd1(vdd),
		  .vssd1(vss));
	end
   endgenerate
endmodule
