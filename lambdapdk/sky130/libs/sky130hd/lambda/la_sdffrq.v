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
  sky130_fd_sc_hd__mux2_4 _0_ (
    .A0(d),
    .A1(si),
    .S(se),
    .X(\q_$_DFF_PN0__Q_D )
  );
  sky130_fd_sc_hd__dfrtp_1 \q_$_DFF_PN0__Q  (
    .CLK(clk),
    .D(\q_$_DFF_PN0__Q_D ),
    .Q(q),
    .RESET_B(nreset)
  );
endmodule