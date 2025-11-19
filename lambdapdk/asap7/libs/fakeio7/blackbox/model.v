// Source lambdapdk/asap7/libs/fakeio7/lef/fakeio7.lef

(* blackbox *)
module FAKEIO7_BIDIR_V (
    inout PAD,
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    input IN_ENABLE,
    input OUT_ENABLE,
    input A,
    output Z,
    input PULLDOWN,
    input PULLUP,
    input DRIVE0,
    input DRIVE1,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_POC_V (
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    input MODE,
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
    input [2:0] AIO
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
    input OUT_ENABLE,
    input A,
    input DRIVE0,
    input DRIVE1,
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
    input IN_ENABLE,
    output ZP,
    output ZN,
    input PULLDOWN,
    input PULLUP,
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
module FAKEIO7_BUMP_PROBE (
    inout PAD
);
endmodule

(* blackbox *)
module FAKEIO7_BUMP_M8_5P0X5P0 (
    inout PAD
);
endmodule

(* blackbox *)
module FAKEIO7_BUMP_M8_5P0X5P0_DUMMY (

);
endmodule

(* blackbox *)
module FAKEIO7_BUMP_M8_2P5X2P5 (
    inout PAD
);
endmodule

(* blackbox *)
module FAKEIO7_BUMP_M8_2P5X2P5_DUMMY (

);
endmodule

(* blackbox *)
module FAKEIO7_BUMP_M8_1P0X1P0 (
    inout PAD
);
endmodule

(* blackbox *)
module FAKEIO7_BUMP_M8_1P0X1P0_DUMMY (

);
endmodule

(* blackbox *)
module FAKEIO7_BUMP_5P0X5P0 (
    inout PAD
);
endmodule

(* blackbox *)
module FAKEIO7_BUMP_5P0X5P0_DUMMY (

);
endmodule

(* blackbox *)
module FAKEIO7_BUMP_12P5 (
    inout PAD
);
endmodule

(* blackbox *)
module FAKEIO7_BUMP_12P5_DUMMY (

);
endmodule

(* blackbox *)
module FAKEIO7_BUMP_15P0 (
    inout PAD
);
endmodule

(* blackbox *)
module FAKEIO7_BUMP_15P0_DUMMY (

);
endmodule

(* blackbox *)
module FAKEIO7_BUMP_30P0 (
    inout PAD
);
endmodule

(* blackbox *)
module FAKEIO7_BUMP_30P0_DUMMY (

);
endmodule

(* blackbox *)
module FAKEIO7_BUMP_50P0 (
    inout PAD
);
endmodule

(* blackbox *)
module FAKEIO7_BUMP_50P0_DUMMY (

);
endmodule

(* blackbox *)
module FAKEIO7_PROBE (
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
    input IN_ENABLE,
    input OUT_ENABLE,
    input A,
    output Z,
    input PULLDOWN,
    input PULLUP,
    input DRIVE0,
    input DRIVE1,
    inout [1:0] RING
);
endmodule

(* blackbox *)
module FAKEIO7_POC_H (
    inout DVDD,
    inout DVSS,
    inout VDD,
    inout VSS,
    input MODE,
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
    input [2:0] AIO
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
    input OUT_ENABLE,
    input A,
    input DRIVE0,
    input DRIVE1,
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
    input IN_ENABLE,
    output ZP,
    output ZN,
    input PULLDOWN,
    input PULLUP,
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
