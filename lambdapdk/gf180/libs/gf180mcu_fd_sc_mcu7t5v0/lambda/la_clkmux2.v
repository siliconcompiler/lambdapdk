/* Generated by Yosys 0.37 (git sha1 a5c7f69ed, clang 14.0.0-1ubuntu1.1 -fPIC -Os) */

module la_clkmux2(clk0, clk1, sel0, sel1, nreset, out);
  wire _0_;
  wire _1_;
  input clk0;
  wire clk0;
  input clk1;
  wire clk1;
  wire \ienb.z ;
  wire \iensync.a ;
  wire \iensync.z ;
  wire \igate[0].en_stable ;
  wire \igate[0].en_stable_gf180mcu_fd_sc_mcu7t5v0__latq_1_Q_E ;
  wire \igate[1].en ;
  wire \igate[1].en_stable ;
  wire \igate[1].en_stable_gf180mcu_fd_sc_mcu7t5v0__latq_1_Q_E ;
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
  gf180mcu_fd_sc_mcu7t5v0__clkinv_2 _2_ (
    .I(clk0),
    .ZN(\igate[0].en_stable_gf180mcu_fd_sc_mcu7t5v0__latq_1_Q_E )
  );
  gf180mcu_fd_sc_mcu7t5v0__clkinv_2 _3_ (
    .I(clk1),
    .ZN(\igate[1].en_stable_gf180mcu_fd_sc_mcu7t5v0__latq_1_Q_E )
  );
  gf180mcu_fd_sc_mcu7t5v0__clkinv_2 _4_ (
    .I(\igate[1].en ),
    .ZN(_0_)
  );
  gf180mcu_fd_sc_mcu7t5v0__nand2_2 _5_ (
    .A1(_0_),
    .A2(sel0),
    .ZN(\ienb.z )
  );
  gf180mcu_fd_sc_mcu7t5v0__clkinv_2 _6_ (
    .I(\iensync.a ),
    .ZN(\iensync.z )
  );
  gf180mcu_fd_sc_mcu7t5v0__and2_2 _7_ (
    .A1(\iensync.a ),
    .A2(sel1),
    .Z(\isel[1].z )
  );
  gf180mcu_fd_sc_mcu7t5v0__aoi22_2 _8_ (
    .A1(clk0),
    .A2(\igate[0].en_stable ),
    .B1(\igate[1].en_stable ),
    .B2(clk1),
    .ZN(_1_)
  );
  gf180mcu_fd_sc_mcu7t5v0__clkinv_2 _9_ (
    .I(_1_),
    .ZN(out)
  );
  gf180mcu_fd_sc_mcu7t5v0__dffrnq_2 \iensync.a_$_DFF_PN0__Q  (
    .CLK(clk0),
    .D(\isync[0].shiftreg[0] ),
    .Q(\iensync.a ),
    .RN(nreset)
  );
  gf180mcu_fd_sc_mcu7t5v0__latq_1 \igate[0].en_stable_gf180mcu_fd_sc_mcu7t5v0__latq_1_Q  (
    .D(\iensync.z ),
    .E(\igate[0].en_stable_gf180mcu_fd_sc_mcu7t5v0__latq_1_Q_E ),
    .Q(\igate[0].en_stable )
  );
  gf180mcu_fd_sc_mcu7t5v0__dffrnq_2 \igate[1].en_$_DFF_PN0__Q  (
    .CLK(clk1),
    .D(\isync[1].shiftreg[0] ),
    .Q(\igate[1].en ),
    .RN(nreset)
  );
  gf180mcu_fd_sc_mcu7t5v0__latq_1 \igate[1].en_stable_gf180mcu_fd_sc_mcu7t5v0__latq_1_Q  (
    .D(\igate[1].en ),
    .E(\igate[1].en_stable_gf180mcu_fd_sc_mcu7t5v0__latq_1_Q_E ),
    .Q(\igate[1].en_stable )
  );
  gf180mcu_fd_sc_mcu7t5v0__dffrnq_2 \isync[0].shiftreg_$_DFF_PN0__Q  (
    .CLK(clk0),
    .D(\ienb.z ),
    .Q(\isync[0].shiftreg[0] ),
    .RN(nreset)
  );
  gf180mcu_fd_sc_mcu7t5v0__dffrnq_2 \isync[1].shiftreg_$_DFF_PN0__Q  (
    .CLK(clk1),
    .D(\isel[1].z ),
    .Q(\isync[1].shiftreg[0] ),
    .RN(nreset)
  );
endmodule