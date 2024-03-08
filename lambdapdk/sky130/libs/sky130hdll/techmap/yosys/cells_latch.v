module $_DLATCH_N_(input E, input D, output Q);
    sky130_fd_sc_hdll__dlxtn_1 _TECHMAP_REPLACE_ (
        .D(D),
        .GATE_N(E),
        .Q(Q)
        );
endmodule

module $_DLATCH_P_(input E, input D, output Q);
    sky130_fd_sc_hdll__dlxtn_1 _TECHMAP_REPLACE_ (
        .D(D),
        .GATE_N(~E),
        .Q(Q)
        );
endmodule
