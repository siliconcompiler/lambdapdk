/* Generated by Yosys 0.37 (git sha1 a5c7f69ed, clang 14.0.0-1ubuntu1.1 -fPIC -Os) */

module la_dffq(d, clk, q);
  wire _0_;
  wire _1_;
  input clk;
  wire clk;
  input d;
  wire d;
  output q;
  wire q;
  INVx2_ASAP7_75t_R _2_ (
    .A(clk),
    .Y(_1_)
  );
  INVx2_ASAP7_75t_R _3_ (
    .A(_0_),
    .Y(q)
  );
  DFFLQNx2_ASAP7_75t_R \q_$_DFF_P__Q  (
    .CLK(_1_),
    .D(d),
    .QN(_0_)
  );
endmodule