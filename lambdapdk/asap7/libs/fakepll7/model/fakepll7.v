// Blackbox Verilog model for fakepll7
// Parameters hardcoded: NIN=2, NOUT=8, DIVFBW=16, CW=32, SW=32

(* blackbox *)
module fakepll7 (
    // supplies
    inout         VDDA,      // analog supply
    inout         VDD,       // digital core supply
    inout         VDD2,      // aux core supply
    inout         VSS,       // common ground
    
    // clocks
    input  [1:0]  clkin,     // input reference clock(s)
    output [7:0]  clkout,    // output clocks (post divided)
    input         clkfbin,   // feedback clock (optional)
    output        clkfbout,  // feedback clock (optional)
    output        clkvco,    // high frequency vco clock
    
    // standard controls
    input         reset,     // active high async reset
    input         en,        // pll enable
    input         bypass,    // pll bypass
    input  [0:0]  clksel,    // clock select
    
    // dividers and enables
    input  [7:0]  clken,     // output clock enable(s)
    input  [7:0]  divin,     // reference divider
    input  [15:0] divfb,     // feedback divider
    input  [7:0]  divfrac,   // fractional feedback divider
    input  [63:0] divout,    // output divider (8 outputs * 8 bits)
    input  [63:0] phase,     // output phase shift (8 outputs * 8 bits)
    
    // locks
    output        freqlock,  // pll frequency lock
    output        phaselock, // pll phase lock
    
    // per PLL defined signals
    input  [31:0] ctrl,      // controls
    output [31:0] status     // status
);

endmodule
