/*****************************************************************************
 * Function: IO bi-directional buffer
 * Copyright: Lambda Project Authors. All rights Reserved.
 * License:  MIT (see LICENSE file in Lambda repository)
 *
 * Docs:
 *
 * This is a generic cell that defines the standard interface of the lambda
 * bidrectional buffer cell. It is only suitable for FPGA synthesis.
 *
 * ASIC specific libraries will need to use the TYPE field to select an
 * appropriate hardcoded physical cell based on the the process constraints
 * and library composition. For example, modern nodes will usually have
 * different IP cells for the placing cells vvertically or horizontally.
 *
 ****************************************************************************/
(* keep_hierarchy *)
module la_ioinput #(
    parameter PROP  = "DEFAULT",  // cell type
    parameter SIDE  = "NO",       // "NO", "SO", "EA", "WE"
    parameter CFGW  = 16,         // width of core config bus
    parameter RINGW = 8           // width of io ring
) (  // io pad signals
    inout              pad,     // bidirectional pad signal
    inout              vdd,     // core supply
    inout              vss,     // core ground
    inout              vddio,   // io supply
    inout              vssio,   // io ground
    // core facing signals
    output             z,       // output to core
    input              ie,      // input enable, 1 = active
    input              pe,      // pull enable, 1 = enable
    input              ps,      // pull select, 1 = pullup, 0 = pulldown
    input              schmitt, // schmitt cfg, 1 = active
    inout  [RINGW-1:0] ioring,  // generic io-ring interface
    input  [ CFGW-1:0] cfg      // generic config interface
);

  if (PROP=="FIXED") begin
    la_iobidir #(
        .PROP (PROP),
        .SIDE (SIDE),
        .CFGW (CFGW),
        .RINGW(RINGW)
    ) i0 (
        .pad(pad),
        .vdd(vdd),
        .vss(vss),
        .vddio(vddio),
        .vssio(vssio),
        .z(z),
        .ie(1'b1),
        .oe(1'b0),
        .pe(1'b1),
        .ps(1'b0),
        .schmitt(schmitt),
        .fast(1'b0),
        .ds('b0),
        .ioring(ioring),
        .cfg(cfg)
    );
  end
  else begin
    la_iobidir #(
        .PROP (PROP),
        .SIDE (SIDE),
        .CFGW (CFGW),
        .RINGW(RINGW)
    ) i0 (
        .pad(pad),
        .vdd(vdd),
        .vss(vss),
        .vddio(vddio),
        .vssio(vssio),
        .z(z),
        .ie(ie),
        .oe(1'b0),
        .pe(pe),
        .ps(ps),
        .schmitt(schmitt),
        .fast(1'b0),
        .ds('b0),
        .ioring(ioring),
        .cfg(cfg)
    );
  end

endmodule
