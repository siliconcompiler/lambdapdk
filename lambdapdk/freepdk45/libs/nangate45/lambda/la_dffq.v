/* Generated by Yosys 0.37 (git sha1 a5c7f69ed, clang 14.0.0-1ubuntu1.1 -fPIC -Os) */

module la_dffq(d, clk, q);
  wire _0_;
  input clk;
  wire clk;
  input d;
  wire d;
  output q;
  wire q;
  DFF_X1 \q_$_DFF_P__Q  (
    .CK(clk),
    .D(d),
    .Q(q),
    .QN(_0_)
  );
endmodule