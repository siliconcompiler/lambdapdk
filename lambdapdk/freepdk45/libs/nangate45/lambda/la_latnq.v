/* Generated by Yosys 0.37 (git sha1 a5c7f69ed, clang 14.0.0-1ubuntu1.1 -fPIC -Os) */

module la_latnq(d, clk, q);
  input clk;
  wire clk;
  input d;
  wire d;
  output q;
  wire q;
  DLL_X1 q_DLL_X1_Q (
    .D(d),
    .GN(clk),
    .Q(q)
  );
endmodule