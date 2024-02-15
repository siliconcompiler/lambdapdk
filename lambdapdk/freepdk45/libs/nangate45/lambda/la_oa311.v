/* Generated by Yosys 0.37 (git sha1 a5c7f69ed, clang 14.0.0-1ubuntu1.1 -fPIC -Os) */

module la_oa311(a0, a1, a2, b0, c0, z);
  wire _0_;
  wire _1_;
  input a0;
  wire a0;
  input a1;
  wire a1;
  input a2;
  wire a2;
  input b0;
  wire b0;
  input c0;
  wire c0;
  output z;
  wire z;
  NOR3_X4 _2_ (
    .A1(a1),
    .A2(a0),
    .A3(a2),
    .ZN(_0_)
  );
  NAND2_X1 _3_ (
    .A1(b0),
    .A2(c0),
    .ZN(_1_)
  );
  NOR2_X1 _4_ (
    .A1(_0_),
    .A2(_1_),
    .ZN(z)
  );
endmodule