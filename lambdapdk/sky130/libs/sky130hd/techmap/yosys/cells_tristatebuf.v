module \$_TBUF_ (input A, input E, output Y);
  sky130_fd_sc_hd__ebufn_1 _TECHMAP_REPLACE_ (
    .A(A),
    .Z(Y),
    .TE_B(~E));
endmodule
