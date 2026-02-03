//#############################################################################
//# Function: Synchronizer                                                    #
//# Copyright: Lambda Project Authors. All rights Reserved.                   #
//# License:  MIT (see LICENSE file in Lambda repository)                     #
//#############################################################################
(* keep_hierarchy *)
module la_dsync #(
    parameter PROP   = "DEFAULT",
    parameter STAGES = 2,          // synchronizer depth
    parameter RND    = 1
)  // randomize simulation delay
(
    input  clk,  // clock
    input  in,   // input data
    output out   // synchronized data
);

  //    reg [STAGES:0] shiftreg;
  //    always @(posedge clk)
  //      shiftreg[STAGES:0] <= {shiftreg[STAGES-1:0], in};

  // `ifdef SIM
  //    integer        sync_delay;
  //    always @(posedge clk)
  //      sync_delay <= {$random} % 2;
  //    assign out = (|sync_delay & (|RND)) ? shiftreg[STAGES] : shiftreg[STAGES-1];
  // `else
  //    assign out = shiftreg[STAGES-1];
  // `endif

  genvar i;
  generate
    for (i = 0; i < STAGES; i = i + 1) begin : DELAY
      wire reg_in;
      wire reg_out;
      if (i == 0) begin : SEL_IN
        assign reg_in = in;
      end else begin : SEL_PREV
        assign reg_in = reg_out[i-1];
      end

      sky130_fd_sc_hdll__dfxtp_1 u0 (
          .CLK(clk),
          .D  (reg_in),
          .Q  (reg_out)
      );
    end
  endgenerate

  assign out = DELAY[STAGES-1].reg_out;

endmodule
