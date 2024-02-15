/* Generated by Yosys 0.37 (git sha1 a5c7f69ed, clang 14.0.0-1ubuntu1.1 -fPIC -Os) */

module la_dffqn(d, clk, qn);
  wire _0_;
  input clk;
  wire clk;
  input d;
  wire d;
  output qn;
  wire qn;
  wire \qn_$_DFF_P__Q_D ;
  INV_X1 _1_ (
    .A(d),
    .ZN(\qn_$_DFF_P__Q_D )
  );
  DFF_X1 \qn_$_DFF_P__Q  (
    .CK(clk),
    .D(\qn_$_DFF_P__Q_D ),
    .Q(qn),
    .QN(_0_)
  );
endmodule