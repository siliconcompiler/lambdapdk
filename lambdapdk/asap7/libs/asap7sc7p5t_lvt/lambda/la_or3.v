/* Generated by Yosys 0.37 (git sha1 a5c7f69ed, clang 14.0.0-1ubuntu1.1 -fPIC -Os) */

module la_or3(a, b, c, z);
  input a;
  wire a;
  input b;
  wire b;
  input c;
  wire c;
  output z;
  wire z;
  OR3x2_ASAP7_75t_L _0_ (
    .A(b),
    .B(a),
    .C(c),
    .Y(z)
  );
endmodule