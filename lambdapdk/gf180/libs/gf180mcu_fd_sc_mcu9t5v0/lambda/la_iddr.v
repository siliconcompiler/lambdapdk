/* Generated by Yosys 0.37 (git sha1 a5c7f69ed, clang 14.0.0-1ubuntu1.1 -fPIC -Os) */

module la_iddr(clk, in, outrise, outfall);
  input clk;
  wire clk;
  input in;
  wire in;
  wire inrise;
  output outfall;
  wire outfall;
  output outrise;
  wire outrise;
  wire outrise_gf180mcu_fd_sc_mcu9t5v0__latq_1_Q_E;
  gf180mcu_fd_sc_mcu9t5v0__clkinv_2 _0_ (
    .I(clk),
    .ZN(outrise_gf180mcu_fd_sc_mcu9t5v0__latq_1_Q_E)
  );
  gf180mcu_fd_sc_mcu9t5v0__dffq_2 \inrise_$_DFF_P__Q  (
    .CLK(clk),
    .D(in),
    .Q(inrise)
  );
  gf180mcu_fd_sc_mcu9t5v0__dffnq_2 \outfall_$_DFF_N__Q  (
    .CLKN(clk),
    .D(in),
    .Q(outfall)
  );
  gf180mcu_fd_sc_mcu9t5v0__latq_1 outrise_gf180mcu_fd_sc_mcu9t5v0__latq_1_Q (
    .D(inrise),
    .E(outrise_gf180mcu_fd_sc_mcu9t5v0__latq_1_Q_E),
    .Q(outrise)
  );
endmodule