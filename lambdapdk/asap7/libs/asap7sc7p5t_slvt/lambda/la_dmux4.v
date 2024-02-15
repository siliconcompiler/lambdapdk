/* Generated by Yosys 0.37 (git sha1 a5c7f69ed, clang 14.0.0-1ubuntu1.1 -fPIC -Os) */

module la_dmux4(sel3, sel2, sel1, sel0, in3, in2, in1, in0, out);
  wire _0_;
  wire _1_;
  input in0;
  wire in0;
  input in1;
  wire in1;
  input in2;
  wire in2;
  input in3;
  wire in3;
  output out;
  wire out;
  input sel0;
  wire sel0;
  input sel1;
  wire sel1;
  input sel2;
  wire sel2;
  input sel3;
  wire sel3;
  AO22x1_ASAP7_75t_SL _2_ (
    .A1(in0),
    .A2(sel0),
    .B1(in2),
    .B2(sel2),
    .Y(_0_)
  );
  AO22x1_ASAP7_75t_SL _3_ (
    .A1(in1),
    .A2(sel1),
    .B1(in3),
    .B2(sel3),
    .Y(_1_)
  );
  OR2x2_ASAP7_75t_SL _4_ (
    .A(_0_),
    .B(_1_),
    .Y(out)
  );
endmodule