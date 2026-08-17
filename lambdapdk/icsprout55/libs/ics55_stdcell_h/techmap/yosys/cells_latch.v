module $_DLATCH_P_(input E, input D, output Q);
    LATHX1H7H _TECHMAP_REPLACE_ (
        .D(D),
        .G(E),
        .Q(Q)
        );
endmodule

module $_DLATCH_N_(input E, input D, output Q);
    LATLX1H7H _TECHMAP_REPLACE_ (
        .D(D),
        .GN(E),
        .Q(Q)
        );
endmodule
