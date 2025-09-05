// Source lambdapdk/sky130/libs/sky130io/lef/sky130_ef_io.lef

(* blackbox *)
module sky130_ef_io__analog_pad (
    inout P_CORE,
    inout VSSA,
    inout VSSD,
    inout AMUXBUS_B,
    inout AMUXBUS_A,
    inout VDDIO_Q,
    inout VDDIO,
    inout VSWITCH,
    inout VSSIO,
    inout VDDA,
    inout VCCD,
    inout VCCHIB,
    inout VSSIO_Q,
    inout P_PAD
);
endmodule

(* blackbox *)
module sky130_ef_io__bare_pad (
    inout PAD
);
endmodule

(* blackbox *)
module sky130_ef_io__com_bus_slice_1um (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__com_bus_slice_5um (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__com_bus_slice_10um (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__com_bus_slice_20um (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__connect_vcchib_vccd_and_vswitch_vddio_slice_20um (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__corner_pad (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__disconnect_vccd_slice_5um (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VSSIO,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__disconnect_vdda_slice_5um (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__gpiov2_pad (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout ANALOG_EN,
    inout ANALOG_POL,
    inout ANALOG_SEL,
    inout ENABLE_H,
    inout ENABLE_INP_H,
    inout ENABLE_VDDA_H,
    inout ENABLE_VDDIO,
    inout ENABLE_VSWITCH_H,
    inout HLD_H_N,
    inout HLD_OVR,
    inout IB_MODE_SEL,
    inout IN,
    inout IN_H,
    inout INP_DIS,
    inout OE_N,
    inout OUT,
    inout PAD,
    inout PAD_A_ESD_0_H,
    inout PAD_A_ESD_1_H,
    inout PAD_A_NOESD_H,
    inout SLOW,
    inout TIE_HI_ESD,
    inout TIE_LO_ESD,
    inout VCCD,
    inout VCCHIB,
    inout VDDA,
    inout VDDIO,
    inout VDDIO_Q,
    inout VSSA,
    inout VSSD,
    inout VSSIO,
    inout VSSIO_Q,
    inout VSWITCH,
    inout VTRIP_SEL,
    inout [2:0] DM
);
endmodule

(* blackbox *)
module sky130_ef_io__gpiov2_pad_wrapped (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout ANALOG_EN,
    inout ANALOG_POL,
    inout ANALOG_SEL,
    inout ENABLE_H,
    inout ENABLE_INP_H,
    inout ENABLE_VDDA_H,
    inout ENABLE_VDDIO,
    inout ENABLE_VSWITCH_H,
    inout HLD_H_N,
    inout HLD_OVR,
    inout IB_MODE_SEL,
    inout IN,
    inout IN_H,
    inout INP_DIS,
    inout OE_N,
    inout OUT,
    inout PAD,
    inout PAD_A_ESD_0_H,
    inout PAD_A_ESD_1_H,
    inout PAD_A_NOESD_H,
    inout SLOW,
    inout TIE_HI_ESD,
    inout TIE_LO_ESD,
    inout VCCD,
    inout VCCHIB,
    inout VDDA,
    inout VDDIO,
    inout VDDIO_Q,
    inout VSSA,
    inout VSSD,
    inout VSSIO,
    inout VSSIO_Q,
    inout VSWITCH,
    inout VTRIP_SEL,
    inout [2:0] DM
);
endmodule

(* blackbox *)
module sky130_ef_io__vccd_hvc_pad (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout DRN_HVC,
    inout SRC_BDY_HVC,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__vccd_lvc_clamped2_pad (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__vccd_lvc_clamped_pad (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__vccd_lvc_pad (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout DRN_LVC1,
    inout DRN_LVC2,
    inout SRC_BDY_LVC1,
    inout SRC_BDY_LVC2,
    inout BDY2_B2B,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__vdda_hvc_clamped_pad (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__vdda_hvc_pad (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout DRN_HVC,
    inout SRC_BDY_HVC,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__vdda_lvc_pad (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout DRN_LVC1,
    inout DRN_LVC2,
    inout SRC_BDY_LVC1,
    inout SRC_BDY_LVC2,
    inout BDY2_B2B,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__vddio_hvc_clamped_pad (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__vddio_hvc_pad (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout DRN_HVC,
    inout SRC_BDY_HVC,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__vddio_lvc_pad (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout DRN_LVC1,
    inout DRN_LVC2,
    inout SRC_BDY_LVC1,
    inout SRC_BDY_LVC2,
    inout BDY2_B2B,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__vssa_hvc_clamped_pad (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__vssa_hvc_pad (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout DRN_HVC,
    inout SRC_BDY_HVC,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__vssa_lvc_pad (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout DRN_LVC1,
    inout DRN_LVC2,
    inout SRC_BDY_LVC1,
    inout SRC_BDY_LVC2,
    inout BDY2_B2B,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__vssd_hvc_pad (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout DRN_HVC,
    inout SRC_BDY_HVC,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__vssd_lvc_clamped2_pad (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__vssd_lvc_clamped_pad (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__vssd_lvc_pad (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout DRN_LVC1,
    inout DRN_LVC2,
    inout SRC_BDY_LVC1,
    inout SRC_BDY_LVC2,
    inout BDY2_B2B,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__vssio_hvc_clamped_pad (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__vssio_hvc_pad (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout DRN_HVC,
    inout SRC_BDY_HVC,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule

(* blackbox *)
module sky130_ef_io__vssio_lvc_pad (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout DRN_LVC1,
    inout DRN_LVC2,
    inout SRC_BDY_LVC1,
    inout SRC_BDY_LVC2,
    inout BDY2_B2B,
    inout VSSA,
    inout VDDA,
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDIO,
    inout VCCD,
    inout VSSIO,
    inout VSSD,
    inout VSSIO_Q
);
endmodule
