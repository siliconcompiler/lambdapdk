module \$_TBUF_ (input A, input E, output Y);
  TBUF_X1 _TECHMAP_REPLACE_ (
    .A(A),
    .Z(Y),
    .EN(E));
endmodule
