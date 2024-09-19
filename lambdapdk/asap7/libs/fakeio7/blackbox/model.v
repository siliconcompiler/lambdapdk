// Source lambdapdk/asap7/libs/fakeio7/lef/fakeio7.lef

(* blackbox *)
module FAKEIO7_BIDIR_V (
    inout PAD,
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout IN_ENABLE,
    inout OUT_ENABLE,
    inout A,
    inout Z,
    inout PULLDOWN,
    inout PULLUP,
    inout DRIVE0,
    inout DRIVE1,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_POC_V (
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout MODE,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_DVDD_V (
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_DVSS_V (
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_VDDCLAMP_V (
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VDDCLAMP,
    inout VSS,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_VDD_V (
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_VSS_V (
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_ANALOG_V (
    inout PAD,
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout [1:0] RING,
    inout [2:0] AIO
);
endmodule

(* blackbox *)
module FAKEIO7_FILL1_V (
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_FILL5_V (
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_FILL10_V (
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_FILL20_V (
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_BREAKER_V (
    inout DVDDA,
    inout DVDDB,
    inout DVSSA,
    inout DVSSB,
    inout VDDA,
    inout VDDB,
    inout VSS,
    inout [1:0] RINGA,
    inout [1:0] RINGB
);
endmodule

(* blackbox *)
module FAKEIO7_DIFFTX_V (
    inout PADP,
    inout PADN,
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout OUT_ENABLE,
    inout A,
    inout DRIVE0,
    inout DRIVE1,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_DIFFRX_V (
    inout PADP,
    inout PADN,
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout IN_ENABLE,
    inout ZP,
    inout ZN,
    inout PULLDOWN,
    inout PULLUP,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_CORNER (
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_BUMP_SMALL (
    inout PAD
);
endmodule

(* blackbox *)
module FAKEIO7_BUMP_LARGE (
    inout PAD
);
endmodule

(* blackbox *)
module FAKEIO7_BIDIR_H (
    inout PAD,
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout IN_ENABLE,
    inout OUT_ENABLE,
    inout A,
    inout Z,
    inout PULLDOWN,
    inout PULLUP,
    inout DRIVE0,
    inout DRIVE1,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_POC_H (
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout MODE,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_DVDD_H (
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_DVSS_H (
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_VDD_H (
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_VSS_H (
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_ANALOG_H (
    inout PAD,
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout [1:0] RING,
    inout [2:0] AIO
);
endmodule

(* blackbox *)
module FAKEIO7_FILL1_H (
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_FILL5_H (
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_FILL10_H (
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_FILL20_H (
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_BREAKER_H (
    inout DVDDA,
    inout DVDDB,
    inout DVSSA,
    inout DVSSB,
    inout VDDA,
    inout VDDB,
    inout VSS,
    inout [1:0] RINGA,
    inout [1:0] RINGB
);
endmodule

(* blackbox *)
module FAKEIO7_DIFFTX_H (
    inout PADP,
    inout PADN,
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout OUT_ENABLE,
    inout A,
    inout DRIVE0,
    inout DRIVE1,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_DIFFRX_H (
    inout PADP,
    inout PADN,
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    inout IN_ENABLE,
    inout ZP,
    inout ZN,
    inout PULLDOWN,
    inout PULLUP,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_VDDCLAMP_H (
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VDDCLAMP,
    inout VSS,
    inout [1:0] RING
);
endmodule
