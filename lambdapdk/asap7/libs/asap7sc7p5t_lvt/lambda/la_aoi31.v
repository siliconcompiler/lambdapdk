/* Generated by Yosys 0.37 (git sha1 a5c7f69ed, clang 14.0.0-1ubuntu1.1 -fPIC -Os) */

module la_aoi31(a0, a1, a2, b0, z);
  wire _0_;
  input a0;
  wire a0;
  input a1;
  wire a1;
  input a2;
  wire a2;
  input b0;
  wire b0;
  output z;
  wire z;
  AND3x1_ASAP7_75t_L _1_ (
    .A(a1),
    .B(a0),
    .C(a2),
    .Y(_0_)
  );
  NOR2x1_ASAP7_75t_L _2_ (
    .A(b0),
    .B(_0_),
    .Y(z)
  );
endmodule