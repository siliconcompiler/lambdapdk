/* Generated by Yosys 0.37 (git sha1 a5c7f69ed, clang 14.0.0-1ubuntu1.1 -fPIC -Os) */

module la_clkmux2(clk0, clk1, sel0, sel1, nreset, out);
  wire _0_;
  wire _1_;
  wire _2_;
  wire _3_;
  wire _4_;
  input clk0;
  wire clk0;
  input clk1;
  wire clk1;
  wire \ienb.z ;
  wire \iensync.a ;
  wire \iensync.z ;
  wire \igate[0].en_stable ;
  wire \igate[1].en ;
  wire \igate[1].en_stable ;
  wire \isel[1].z ;
  wire \isync[0].shiftreg[0] ;
  wire \isync[1].shiftreg[0] ;
  input nreset;
  wire nreset;
  output out;
  wire out;
  input sel0;
  wire sel0;
  input sel1;
  wire sel1;
  INV_X1 _5_ (
    .A(\igate[1].en ),
    .ZN(_0_)
  );
  NAND2_X1 _6_ (
    .A1(_0_),
    .A2(sel0),
    .ZN(\ienb.z )
  );
  AND2_X1 _7_ (
    .A1(sel1),
    .A2(\iensync.a ),
    .ZN(\isel[1].z )
  );
  AOI22_X2 _8_ (
    .A1(\igate[0].en_stable ),
    .A2(clk0),
    .B1(\igate[1].en_stable ),
    .B2(clk1),
    .ZN(_1_)
  );
  INV_X1 _9_ (
    .A(_1_),
    .ZN(out)
  );
  DFFR_X1 \iensync.a_$_DFF_PN0__Q  (
    .CK(clk0),
    .D(\isync[0].shiftreg[0] ),
    .Q(\iensync.a ),
    .QN(\iensync.z ),
    .RN(nreset)
  );
  DLL_X1 \igate[0].en_stable_DLL_X1_Q  (
    .D(\iensync.z ),
    .GN(clk0),
    .Q(\igate[0].en_stable )
  );
  DFFR_X1 \igate[1].en_$_DFF_PN0__Q  (
    .CK(clk1),
    .D(\isync[1].shiftreg[0] ),
    .Q(\igate[1].en ),
    .QN(_2_),
    .RN(nreset)
  );
  DLL_X1 \igate[1].en_stable_DLL_X1_Q  (
    .D(\igate[1].en ),
    .GN(clk1),
    .Q(\igate[1].en_stable )
  );
  DFFR_X1 \isync[0].shiftreg_$_DFF_PN0__Q  (
    .CK(clk0),
    .D(\ienb.z ),
    .Q(\isync[0].shiftreg[0] ),
    .QN(_3_),
    .RN(nreset)
  );
  DFFR_X1 \isync[1].shiftreg_$_DFF_PN0__Q  (
    .CK(clk1),
    .D(\isel[1].z ),
    .Q(\isync[1].shiftreg[0] ),
    .QN(_4_),
    .RN(nreset)
  );
endmodule