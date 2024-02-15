/* Generated by Yosys 0.37 (git sha1 a5c7f69ed, clang 14.0.0-1ubuntu1.1 -fPIC -Os) */

module la_sdffrqn(d, si, se, clk, nreset, qn);
  input clk;
  wire clk;
  input d;
  wire d;
  input nreset;
  wire nreset;
  output qn;
  wire qn;
  wire \qn_$_DFF_PN1__Q_D ;
  input se;
  wire se;
  input si;
  wire si;
  sky130_fd_sc_hd__mux2i_1 _0_ (
    .A0(d),
    .A1(si),
    .S(se),
    .Y(\qn_$_DFF_PN1__Q_D )
  );
  sky130_fd_sc_hd__dfstp_2 \qn_$_DFF_PN1__Q  (
    .CLK(clk),
    .D(\qn_$_DFF_PN1__Q_D ),
    .Q(qn),
    .SET_B(nreset)
  );
endmodule