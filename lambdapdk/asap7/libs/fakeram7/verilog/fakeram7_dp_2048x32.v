module fakeram7_dp_2048x32
(
   rd_out_A,
   rd_out_B,
   addr_in_A,
   addr_in_B,
   we_in_A,
   we_in_B,
   wd_in_A,
   wd_in_B,
   w_mask_in_A,
   w_mask_in_B,
   clk,
   ce_in
);
   parameter BITS = 32;
   parameter WORD_DEPTH = 2048;
   parameter ADDR_WIDTH = 11;
   parameter corrupt_mem_on_X_p = 1;

   output reg [BITS-1:0]    rd_out_A;
   output reg [BITS-1:0]    rd_out_B;
   input  [ADDR_WIDTH-1:0]  addr_in_A;
   input  [ADDR_WIDTH-1:0]  addr_in_B;
   input                    we_in_A;
   input                    we_in_B;
   input  [BITS-1:0]        wd_in_A;
   input  [BITS-1:0]        wd_in_B;
   input  [BITS-1:0]        w_mask_in_A;
   input  [BITS-1:0]        w_mask_in_B;
   input                    clk;
   input                    ce_in;

   reg    [BITS-1:0]        mem [0:WORD_DEPTH-1];

   integer j;

   always @(posedge clk)
   begin
      if (ce_in)
      begin
         //if ((we_in_A !== 1'b1 && we_in_A !== 1'b0) && corrupt_mem_on_X_p)
         if (corrupt_mem_on_X_p &&
             ((^we_in_A === 1'bx) || (^addr_in_A === 1'bx))
            )
         begin
            // WEN or ADDR is unknown, so corrupt entire array (using unsynthesizeable for loop)
            for (j = 0; j < WORD_DEPTH; j = j + 1)
               mem[j] <= 'x;
            $display("warning: ce_in=1, we_in_A is %b, addr_in_A = %x in fakeram7_dp_2048x32", we_in_A, addr_in_A);
         end
         else if (we_in_A)
         begin
            mem[addr_in_A] <= (wd_in_A & w_mask_in_A) | (mem[addr_in_A] & ~w_mask_in_A);
         end
         //if ((we_in_B !== 1'b1 && we_in_B !== 1'b0) && corrupt_mem_on_X_p)
         if (corrupt_mem_on_X_p &&
             ((^we_in_B === 1'bx) || (^addr_in_B === 1'bx))
            )
         begin
            // WEN or ADDR is unknown, so corrupt entire array (using unsynthesizeable for loop)
            for (j = 0; j < WORD_DEPTH; j = j + 1)
               mem[j] <= 'x;
            $display("warning: ce_in=1, we_in_B is %b, addr_in_B = %x in fakeram7_dp_2048x32", we_in_B, addr_in_B);
         end
         else if (we_in_B)
         begin
            mem[addr_in_B] <= (wd_in_B & w_mask_in_B) | (mem[addr_in_B] & ~w_mask_in_B);
         end
         // read
         rd_out_A <= mem[addr_in_A];
         rd_out_B <= mem[addr_in_B];
      end
      else
      begin
         // Make sure read fails if ce_in is low
         rd_out_A <= 'x;
         rd_out_B <= 'x;
      end
   end

   // Timing check placeholders (will be replaced during SDF back-annotation)
   reg notifier;
   specify
      // Delay from clk to rd_out
      (posedge clk *> rd_out_A) = (0, 0);
      // Delay from clk to rd_out
      (posedge clk *> rd_out_B) = (0, 0);

      // Timing checks
      $width     (posedge clk,            0, 0, notifier);
      $width     (negedge clk,            0, 0, notifier);
      $period    (posedge clk,            0,    notifier);
      $setuphold (posedge clk, we_in_A,     0, 0, notifier);
      $setuphold (posedge clk, ce_in_A,     0, 0, notifier);
      $setuphold (posedge clk, addr_in_A,   0, 0, notifier);
      $setuphold (posedge clk, wd_in_A,     0, 0, notifier);
      $setuphold (posedge clk, w_mask_in_A, 0, 0, notifier);
      $setuphold (posedge clk, we_in_B,     0, 0, notifier);
      $setuphold (posedge clk, ce_in_B,     0, 0, notifier);
      $setuphold (posedge clk, addr_in_B,   0, 0, notifier);
      $setuphold (posedge clk, wd_in_B,     0, 0, notifier);
      $setuphold (posedge clk, w_mask_in_B, 0, 0, notifier);
   endspecify

endmodule
