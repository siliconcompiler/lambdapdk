/******************************************************************************
 * Function: PLL
 * Copyright: Lambda Project Authors. All rights Reserved.
 * License:  MIT (see LICENSE file in Lambda repository)
 *
 * NOTE: The generic PLL interface was derived by reviewing a number of
 * publicly open source PLLs and FPGA IP datasheets as well as LLM
 * prompting.
 *
 * Basic operation of all output clocks:
 *
 * freq_vco = freq_clkin * (divfb / divin)
 * freq_clkout = freq_vco / (divout)
 *
 * In real ASIC design the la_pll is replaced by an actual PLL implementation.
 *
 * A coarse simulation model is available in testbench/la_pll_model.v
 * For exact simulation behavior, use the actual designer supplied
 * mixed signal simulation model.
 *
 * DIVIN corresponds exactly to "N" (0 is an illegal value).
 * DIVFB corresponds exactly to "M" (0 is an illegal value).
 *
 *******************************************************************************/
module la_pll
  #(
    // defaults updated to match the fixed 'fakepll7' macro configuration
    parameter      NIN = 2,          // number of input reference clocks
    parameter      NOUT = 8,         // number of output clocks
    parameter      DIVINW = 8,       // input divider width
    parameter      DIVFBW = 16,      // feedback divider width
    parameter      DIVFRACW = 8,     // fractional feedback divider width
    parameter      DIVOUTW = 8,      // output divider width
    parameter      PHASEW = 8,       // phase shift adjust width
    parameter      CW = 32,          // control vector width
    parameter      SW = 32,          // status vector width
    parameter      PROP = "",        // cell property
    parameter real FREF = 25.0       // clkin frequency (MHz)
    )
   (
    // supplies
    inout                        vdda,      // analog supply
    inout                        vdd,       // digital core supply
    inout                        vddaux,    // aux core supply
    inout                        vss,       // common ground

    // clocks
    input [NIN-1:0]              clkin,     // input reference clock(s)
    output [NOUT-1:0]            clkout,    // output clocks (post divided)
    input                        clkfbin,   // feedback clock (optional)
    output                       clkfbout,  // feedback clock (optional)
    output                       clkvco,    // high frequency vco clock

    // standard controls
    input                        reset,     // active high async reset
    input                        en,        // pll enable
    input                        bypass,    // pll bypass
    input [(NIN>1?$clog2(NIN):1)-1:0] clksel,    // clock select

    // dividers and enables
    input [NOUT-1:0]             clken,     // output clock enable(s)
    input [DIVINW-1:0]           divin,     // reference divider
    input [DIVFBW-1:0]           divfb,     // feedback divider
    input [DIVFRACW-1:0]         divfrac,   // fractional feedback divider
    input [NOUT*DIVOUTW-1:0]     divout,    // output divider
    input [NOUT*PHASEW-1:0]      phase,     // output phase shift

    // locks
    output                       freqlock,  // pll frequency lock
    output                       phaselock, // pll phase lock

    // per PLL defined signals
    input [CW-1:0]               ctrl,      // controls
    output [SW-1:0]              status     // status
    );
// =========================================================================
    // 1. HARD MACRO "fakepll7" CONSTANTS
    // =========================================================================
    localparam FM_NIN      = 2;
    localparam FM_NOUT     = 8;
    localparam FM_DIVINW   = 8;
    localparam FM_DIVFBW   = 16;
    localparam FM_DIVFRACW = 8;
    localparam FM_DIVOUTW  = 8;
    localparam FM_PHASEW   = 8;
    localparam FM_CW       = 32;
    localparam FM_SW       = 32;

    // Derived Fixed Widths for Buses
    localparam FM_DIVOUT_BITS = FM_NOUT * FM_DIVOUTW; // 64
    localparam FM_PHASE_BITS  = FM_NOUT * FM_PHASEW;  // 64
    localparam FM_CLKSEL_BITS = 1; // $clog2(2)

    // =========================================================================
    // 2. INTERMEDIATE WIRES (Sized for the Hard Macro)
    // =========================================================================
    wire [FM_NIN-1:0]         w_clkin;
    wire [FM_NOUT-1:0]        w_clkout;
    wire [FM_CLKSEL_BITS-1:0] w_clksel;
    wire [FM_NOUT-1:0]        w_clken;
    wire [FM_DIVINW-1:0]      w_divin;
    wire [FM_DIVFBW-1:0]      w_divfb;
    wire [FM_DIVFRACW-1:0]    w_divfrac;
    wire [FM_DIVOUT_BITS-1:0] w_divout;
    wire [FM_PHASE_BITS-1:0]  w_phase;
    wire [FM_CW-1:0]          w_ctrl;
    wire [FM_SW-1:0]          w_status;

    // =========================================================================
    // 3. ADAPTATION LOGIC (Shim)
    // =========================================================================

    // --- Inputs: Logic to drive the Macro ---
    // Rule: If Wrapper < Macro, Pad with 0s. If Wrapper > Macro, Truncate.

    // clkin
    assign w_clkin = (NIN < FM_NIN) ? { {(FM_NIN-NIN){1'b0}}, clkin } : clkin[FM_NIN-1:0];

    // clksel (Special case for calculated width)
    localparam W_CLKSEL_W = (NIN>1?$clog2(NIN):1);
    assign w_clksel = (W_CLKSEL_W < FM_CLKSEL_BITS) ? { {(FM_CLKSEL_BITS-W_CLKSEL_W){1'b0}}, clksel } : clksel[FM_CLKSEL_BITS-1:0];

    // clken
    assign w_clken = (NOUT < FM_NOUT) ? { {(FM_NOUT-NOUT){1'b0}}, clken } : clken[FM_NOUT-1:0];

    // divin
    assign w_divin = (DIVINW < FM_DIVINW) ? { {(FM_DIVINW-DIVINW){1'b0}}, divin } : divin[FM_DIVINW-1:0];

    // divfb
    assign w_divfb = (DIVFBW < FM_DIVFBW) ? { {(FM_DIVFBW-DIVFBW){1'b0}}, divfb } : divfb[FM_DIVFBW-1:0];

    // divfrac
    assign w_divfrac = (DIVFRACW < FM_DIVFRACW) ? { {(FM_DIVFRACW-DIVFRACW){1'b0}}, divfrac } : divfrac[FM_DIVFRACW-1:0];

    // divout (Flattened Bus)
    localparam P_DIVOUT_BITS = NOUT * DIVOUTW;
    assign w_divout = (P_DIVOUT_BITS < FM_DIVOUT_BITS) ? { {(FM_DIVOUT_BITS-P_DIVOUT_BITS){1'b0}}, divout } : divout[FM_DIVOUT_BITS-1:0];

    // phase (Flattened Bus)
    localparam P_PHASE_BITS = NOUT * PHASEW;
    assign w_phase = (P_PHASE_BITS < FM_PHASE_BITS) ? { {(FM_PHASE_BITS-P_PHASE_BITS){1'b0}}, phase } : phase[FM_PHASE_BITS-1:0];

    // ctrl
    assign w_ctrl = (CW < FM_CW) ? { {(FM_CW-CW){1'b0}}, ctrl } : ctrl[FM_CW-1:0];

    // --- Outputs: Logic to drive the Wrapper Ports ---
    // Rule: If Wrapper > Macro, drive MSBs to 0. If Wrapper < Macro, Truncate.

    // clkout
    assign clkout = (NOUT > FM_NOUT) ? { {(NOUT-FM_NOUT){1'b0}}, w_clkout } : w_clkout[NOUT-1:0];

    // status
    assign status = (SW > FM_SW) ? { {(SW-FM_SW){1'b0}}, w_status } : w_status[SW-1:0];
  
    fakepll7 pll (
        // Supplies
        .VDDA       (vdda),
        .VDD        (vdd),
        .VDD2       (vddaux),
        .VSS        (vss),
        .clkin      (w_clkin),
        .clkout     (w_clkout),
        .clkfbin    (clkfbin),   // Single bit, direct connect
        .clkfbout   (clkfbout),  // Single bit, direct connect
        .clkvco     (clkvco),    // Single bit, direct connect
        .reset      (reset),     // Single bit, direct connect
        .en         (en),        // Single bit, direct connect
        .bypass     (bypass),    // Single bit, direct connect
        .clksel     (w_clksel),
        .clken      (w_clken),
        .divin      (w_divin),
        .divfb      (w_divfb),
        .divfrac    (w_divfrac),
        .divout     (w_divout),
        .phase      (w_phase),
        .freqlock   (freqlock),  // Single bit, direct connect
        .phaselock  (phaselock), // Single bit, direct connect
        .ctrl       (w_ctrl),
        .status     (w_status)
    );

endmodule
