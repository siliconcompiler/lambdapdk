// Source sky130A/libs.ref/sky130_fd_io/lef/sky130_fd_io.lef @ pdk_rev

(* blackbox *)
module sky130_fd_io__corner_bus_overlay (
    inout VSSA,
    inout VSSIO,
    inout VSWITCH,
    inout VSSD,
    inout VSSIO_Q,
    inout VDDIO_Q,
    inout VDDIO,
    inout VDDA,
    inout VCCHIB,
    inout VCCD,
    inout AMUXBUS_A,
    inout AMUXBUS_B
);
endmodule

(* blackbox *)
module sky130_fd_io__hvclampv2 (
    inout vssd,
    inout ogc_hvc,
    inout src_bdy_hvc,
    inout drn_hvc
);
endmodule

(* blackbox *)
module sky130_fd_io__overlay_gpiov2 (
    inout PAD,
    inout VSSIO,
    inout VDDIO,
    inout VCCHIB,
    inout VDDIO_Q,
    inout VCCD,
    inout VSSA,
    inout VSWITCH,
    inout VSSIO_Q,
    inout VSSD,
    inout VDDA,
    inout AMUXBUS_A,
    inout AMUXBUS_B
);
endmodule

(* blackbox *)
module sky130_fd_io__overlay_vccd_hvc (
    inout VDDIO,
    inout VCCHIB,
    inout VSSA,
    inout VDDIO_Q,
    inout VCCD,
    inout VSWITCH,
    inout VSSIO,
    inout VSSIO_Q,
    inout VSSD,
    inout VDDA,
    inout AMUXBUS_A,
    inout AMUXBUS_B
);
endmodule

(* blackbox *)
module sky130_fd_io__overlay_vccd_lvc (
    inout VDDIO_Q,
    inout VDDIO,
    inout VSSA,
    inout VCCHIB,
    inout VCCD,
    inout VDDA,
    inout VSSIO_Q,
    inout VSWITCH,
    inout VSSIO,
    inout VSSD,
    inout AMUXBUS_A,
    inout AMUXBUS_B
);
endmodule

(* blackbox *)
module sky130_fd_io__overlay_vdda_hvc (
    inout VSSA,
    inout VSSIO_Q,
    inout VSSD,
    inout VDDA,
    inout VSSIO,
    inout VCCD,
    inout VCCHIB,
    inout VSWITCH,
    inout VDDIO,
    inout VDDIO_Q,
    inout AMUXBUS_A,
    inout AMUXBUS_B
);
endmodule

(* blackbox *)
module sky130_fd_io__overlay_vdda_lvc (
    inout VSWITCH,
    inout VCCD,
    inout VCCHIB,
    inout VDDA,
    inout VSSD,
    inout VDDIO,
    inout VDDIO_Q,
    inout VSSA,
    inout VSSIO,
    inout VSSIO_Q,
    inout AMUXBUS_B,
    inout AMUXBUS_A
);
endmodule

(* blackbox *)
module sky130_fd_io__overlay_vddio_hvc (
    inout VSSIO,
    inout VSSA,
    inout VDDIO,
    inout VDDIO_Q,
    inout VCCHIB,
    inout VDDA,
    inout VCCD,
    inout VSSIO_Q,
    inout VSWITCH,
    inout VSSD,
    inout AMUXBUS_A,
    inout AMUXBUS_B
);
endmodule

(* blackbox *)
module sky130_fd_io__overlay_vddio_lvc (
    inout VDDIO_Q,
    inout VSSA,
    inout VSSD,
    inout VDDA,
    inout VDDIO,
    inout VCCD,
    inout VCCHIB,
    inout VSWITCH,
    inout VSSIO_Q,
    inout VSSIO,
    inout AMUXBUS_A,
    inout AMUXBUS_B
);
endmodule

(* blackbox *)
module sky130_fd_io__overlay_vssa_hvc (
    inout VDDA,
    inout VCCD,
    inout VDDIO,
    inout VDDIO_Q,
    inout VSSIO,
    inout VSSIO_Q,
    inout VSWITCH,
    inout VCCHIB,
    inout VSSA,
    inout VSSD,
    inout AMUXBUS_B,
    inout AMUXBUS_A
);
endmodule

(* blackbox *)
module sky130_fd_io__overlay_vssa_lvc (
    inout VSWITCH,
    inout VDDIO_Q,
    inout VCCD,
    inout VSSA,
    inout VSSD,
    inout VSSIO,
    inout VSSIO_Q,
    inout VCCHIB,
    inout VDDA,
    inout VDDIO,
    inout AMUXBUS_B,
    inout AMUXBUS_A
);
endmodule

(* blackbox *)
module sky130_fd_io__overlay_vssd_hvc (
    inout VCCD,
    inout VSSA,
    inout VDDA,
    inout VSSD,
    inout VSSIO,
    inout VSSIO_Q,
    inout VSWITCH,
    inout VCCHIB,
    inout VDDIO,
    inout VDDIO_Q,
    inout AMUXBUS_A,
    inout AMUXBUS_B
);
endmodule

(* blackbox *)
module sky130_fd_io__overlay_vssd_lvc (
    inout VSSA,
    inout VDDIO,
    inout VDDIO_Q,
    inout VSSD,
    inout VSSIO,
    inout VSWITCH,
    inout VSSIO_Q,
    inout VDDA,
    inout VCCD,
    inout VCCHIB,
    inout AMUXBUS_B,
    inout AMUXBUS_A
);
endmodule

(* blackbox *)
module sky130_fd_io__overlay_vssio_hvc (
    inout VSSA,
    inout VDDIO,
    inout VDDIO_Q,
    inout VSSD,
    inout VSSIO,
    inout VSWITCH,
    inout VSSIO_Q,
    inout VDDA,
    inout VCCD,
    inout VCCHIB,
    inout AMUXBUS_B,
    inout AMUXBUS_A
);
endmodule

(* blackbox *)
module sky130_fd_io__overlay_vssio_lvc (
    inout VCCD,
    inout VSSA,
    inout VDDA,
    inout VSSD,
    inout VSSIO,
    inout VSSIO_Q,
    inout VSWITCH,
    inout VCCHIB,
    inout VDDIO,
    inout VDDIO_Q,
    inout AMUXBUS_A,
    inout AMUXBUS_B
);
endmodule

(* blackbox *)
module sky130_fd_io__top_amuxsplitv2 (
    inout amuxbus_a_r,
    inout amuxbus_a_l,
    inout vssa,
    inout amuxbus_b_r,
    inout amuxbus_b_l,
    input enable_vdda_h,
    input hld_vdda_h_n,
    input switch_aa_s0,
    input switch_aa_sl,
    input switch_aa_sr,
    input switch_bb_s0,
    input switch_bb_sl,
    input switch_bb_sr,
    inout vdda,
    inout vssd,
    inout vssio_q,
    inout vssio,
    inout vswitch,
    inout vccd,
    inout vddio_q,
    inout vddio,
    inout vcchib
);
endmodule

(* blackbox *)
module sky130_fd_io__top_analog_pad (
    inout vssio,
    inout vccd,
    inout vddio_q,
    inout vssa,
    inout vddio,
    inout vcchib,
    inout vswitch,
    inout vssio_q,
    inout vdda,
    inout vssd,
    inout pad,
    inout amuxbus_b,
    inout amuxbus_a,
    inout pad_core
);
endmodule

(* blackbox *)
module sky130_fd_io__top_gpio_ovtv2 (
    input INP_DIS,
    input VTRIP_SEL,
    input HYS_TRIM,
    input HLD_OVR,
    input ENABLE_H,
    input HLD_H_N,
    input ENABLE_VDDA_H,
    input ANALOG_EN,
    input ENABLE_INP_H,
    output IN,
    output IN_H,
    input VINREF,
    input OUT,
    input ANALOG_POL,
    input ANALOG_SEL,
    input SLOW,
    input OE_N,
    output TIE_HI_ESD,
    output TIE_LO_ESD,
    inout PAD_A_ESD_0_H,
    inout PAD_A_ESD_1_H,
    inout PAD_A_NOESD_H,
    input ENABLE_VSWITCH_H,
    input ENABLE_VDDIO,
    inout VSSA,
    inout VSSIO_Q,
    inout VSSIO,
    inout VCCHIB,
    inout VCCD,
    inout VDDA,
    inout VDDIO,
    inout VSWITCH,
    inout VDDIO_Q,
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout VSSD,
    inout PAD,
    input [2:0] DM,
    input [1:0] IB_MODE_SEL,
    input [1:0] SLEW_CTL
);
endmodule

(* blackbox *)
module sky130_fd_io__top_gpiov2 (
    input ANALOG_EN,
    input HLD_H_N,
    input HLD_OVR,
    input INP_DIS,
    input ENABLE_VDDA_H,
    input VTRIP_SEL,
    input OE_N,
    input OUT,
    input SLOW,
    output TIE_LO_ESD,
    inout PAD_A_ESD_0_H,
    input ANALOG_SEL,
    input ENABLE_INP_H,
    inout PAD_A_ESD_1_H,
    output TIE_HI_ESD,
    input ENABLE_H,
    input IB_MODE_SEL,
    input ENABLE_VSWITCH_H,
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
    inout VSSA,
    inout VSSIO_Q,
    inout PAD_A_NOESD_H,
    inout PAD,
    input ANALOG_POL,
    input ENABLE_VDDIO,
    output IN,
    output IN_H,
    input [2:0] DM
);
endmodule

(* blackbox *)
module sky130_fd_io__top_gpiovrefv2 (
    input ref_sel<4>,
    input ref_sel<3>,
    input ref_sel<1>,
    input vrefgen_en,
    input hld_h_n,
    input enable_h,
    input ref_sel<2>,
    input ref_sel<0>,
    inout vinref,
    inout vddio_q,
    inout vddio,
    inout vssio,
    inout vssa,
    inout vccd,
    inout vcchib,
    inout vswitch,
    inout vssio_q,
    inout vdda,
    inout vssd,
    inout amuxbus_b,
    inout amuxbus_a
);
endmodule

(* blackbox *)
module sky130_fd_io__top_ground_hvc_wpad (
    inout VSSA,
    inout VDDIO,
    inout VCCD,
    inout VCCHIB,
    inout VDDA,
    inout VDDIO_Q,
    inout VSSD,
    inout VSSIO,
    inout VSWITCH,
    inout VSSIO_Q,
    inout G_PAD,
    inout AMUXBUS_B,
    inout AMUXBUS_A,
    inout PADISOR,
    inout PADISOL,
    inout DRN_HVC,
    inout SRC_BDY_HVC,
    inout OGC_HVC,
    inout G_CORE
);
endmodule

(* blackbox *)
module sky130_fd_io__top_ground_lvc_wpad (
    inout PADISOR,
    inout PADISOL,
    inout VSSIO,
    inout VSSA,
    inout VSSIO_Q,
    inout VCCHIB,
    inout VCCD,
    inout VDDA,
    inout VDDIO,
    inout VSWITCH,
    inout VDDIO_Q,
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout VSSD,
    inout G_PAD,
    inout SRC_BDY_LVC1,
    inout SRC_BDY_LVC2,
    inout BDY2_B2B,
    inout DRN_LVC2,
    inout DRN_LVC1,
    inout G_CORE,
    inout OGC_LVC
);
endmodule

(* blackbox *)
module sky130_fd_io__top_hvclamp (
    inout src_bdy_hvc,
    inout drn_hvc,
    inout ogc_hvc
);
endmodule

(* blackbox *)
module sky130_fd_io__top_lvc_b2b (
    inout vssd,
    inout src_bdy_lvc1,
    inout src_bdy_lvc2,
    inout bdy2_b2b,
    inout drn_lvc2,
    inout drn_lvc1,
    inout ogc_lvc
);
endmodule

(* blackbox *)
module sky130_fd_io__top_lvclamp (
    inout ogc_lvc,
    inout drn_lvc,
    inout src_bdy_lvc
);
endmodule

(* blackbox *)
module sky130_fd_io__top_power_hvc_wpad (
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout P_PAD,
    inout DRN_HVC,
    inout OGC_HVC,
    inout P_CORE,
    inout SRC_BDY_HVC,
    inout VCCD,
    inout VCCHIB,
    inout VDDA,
    inout VDDIO,
    inout VDDIO_Q,
    inout VSSA,
    inout VSSD,
    inout VSSIO,
    inout VSSIO_Q,
    inout VSWITCH
);
endmodule

(* blackbox *)
module sky130_fd_io__top_power_hvc_wpadv2 (
    inout PADISOR,
    inout PADISOL,
    inout P_CORE,
    inout DRN_HVC,
    inout SRC_BDY_HVC,
    inout OGC_HVC,
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
module sky130_fd_io__top_power_lvc_wpad (
    inout VSSIO,
    inout VSSA,
    inout VSSIO_Q,
    inout VCCHIB,
    inout VCCD,
    inout VDDA,
    inout VDDIO,
    inout VSWITCH,
    inout VDDIO_Q,
    inout AMUXBUS_A,
    inout AMUXBUS_B,
    inout VSSD,
    inout P_PAD,
    inout SRC_BDY_LVC1,
    inout SRC_BDY_LVC2,
    inout BDY2_B2B,
    inout DRN_LVC2,
    inout DRN_LVC1,
    inout P_CORE,
    inout PADISOR,
    inout PADISOL,
    inout OGC_LVC
);
endmodule

(* blackbox *)
module sky130_fd_io__top_pwrdetv2 (
    input in1_vddd_hv,
    input in2_vddd_hv,
    output out3_vddio_hv,
    output out1_vddio_hv,
    output out2_vddio_hv,
    output out2_vddd_hv,
    output out1_vddd_hv,
    input in1_vddio_hv,
    output vddio_present_vddd_hv,
    output vddd_present_vddio_hv,
    output tie_lo_esd,
    input rst_por_hv_n,
    output out3_vddd_hv,
    input in3_vddio_hv,
    input in2_vddio_hv,
    input in3_vddd_hv,
    inout vssio_q,
    inout vccd,
    inout vddd1,
    inout vssa,
    inout vddio_q,
    inout vddd2,
    inout vssd
);
endmodule

(* blackbox *)
module sky130_fd_io__top_sio_macro (
    input vreg_en_refgen,
    inout amuxbus_a,
    input voh_sel<1>,
    input voh_sel<2>,
    input vref_sel<0>,
    input vref_sel<1>,
    inout amuxbus_b,
    input voh_sel<0>,
    input vohref,
    input ibuf_sel_refgen,
    input enable_vdda_h,
    inout voutref_dft,
    inout pad_a_esd_1_h<0>,
    input ibuf_sel<1>,
    input dft_refgen,
    input hld_h_n_refgen,
    input vtrip_sel_refgen,
    inout vinref_dft,
    inout pad_a_esd_1_h<1>,
    inout pad_a_esd_0_h<1>,
    inout pad_a_esd_0_h<0>,
    inout pad_a_noesd_h<0>,
    inout pad_a_noesd_h<1>,
    input inp_dis<1>,
    input inp_dis<0>,
    output tie_lo_esd<0>,
    output tie_lo_esd<1>,
    input out<1>,
    input out<0>,
    input dm1<0>,
    input dm1<1>,
    input dm1<2>,
    input enable_h,
    input vreg_en<0>,
    input vreg_en<1>,
    input slow<1>,
    input slow<0>,
    input oe_n<0>,
    input oe_n<1>,
    output in_h<1>,
    input dm0<0>,
    output in_h<0>,
    input dm0<1>,
    input dm0<2>,
    output in<0>,
    output in<1>,
    input hld_ovr<1>,
    input hld_ovr<0>,
    input hld_h_n<1>,
    input hld_h_n<0>,
    input ibuf_sel<0>,
    input vtrip_sel<1>,
    input vtrip_sel<0>,
    inout vssd,
    inout vddio_q,
    inout vddio,
    inout vswitch,
    inout vssio,
    inout vdda,
    inout vccd,
    inout vcchib,
    inout vssa,
    inout vssio_q,
    inout pad<1>,
    inout pad<0>
);
endmodule

(* blackbox *)
module sky130_fd_io__top_vrefcapv2 (
    inout cpos,
    inout cneg,
    inout vssio,
    inout vddio_q,
    inout vddio,
    inout vssio_q,
    inout vccd,
    inout vssa,
    inout vcchib,
    inout vswitch,
    inout vdda,
    inout vssd,
    inout amuxbus_b,
    inout amuxbus_a
);
endmodule

(* blackbox *)
module sky130_fd_io__top_xres4v2 (
    inout PULLUP_H,
    input INP_SEL_H,
    input ENABLE_H,
    input EN_VDDIO_SIG_H,
    input DISABLE_PULLUP_H,
    output TIE_HI_ESD,
    output TIE_LO_ESD,
    inout TIE_WEAK_HI_H,
    input ENABLE_VDDIO,
    inout PAD_A_ESD_H,
    input FILT_IN_H,
    output XRES_H_N,
    inout VSSIO,
    inout VSSA,
    inout VDDIO,
    inout VCCD,
    inout VCCHIB,
    inout VDDA,
    inout VDDIO_Q,
    inout VSSD,
    inout VSWITCH,
    inout VSSIO_Q,
    inout PAD,
    inout AMUXBUS_B,
    inout AMUXBUS_A
);
endmodule
