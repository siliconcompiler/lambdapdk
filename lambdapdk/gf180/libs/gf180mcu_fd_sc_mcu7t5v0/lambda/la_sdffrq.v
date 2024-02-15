/* Generated by Yosys 0.37 (git sha1 a5c7f69ed, clang 14.0.0-1ubuntu1.1 -fPIC -Os) */

module la_sdffrq(d, si, se, clk, nreset, q);
  input clk;
  wire clk;
  input d;
  wire d;
  input nreset;
  wire nreset;
  output q;
  wire q;
  wire \q_$_DFF_PN0__Q_D ;
  input se;
  wire se;
  input si;
  wire si;
  gf180mcu_fd_sc_mcu7t5v0__mux2_2 _0_ (
    .I0(d),
    .I1(si),
    .S(se),
    .Z(\q_$_DFF_PN0__Q_D )
  );
  gf180mcu_fd_sc_mcu7t5v0__dffrnq_2 \q_$_DFF_PN0__Q  (
    .CLK(clk),
    .D(\q_$_DFF_PN0__Q_D ),
    .Q(q),
    .RN(nreset)
  );
endmodule