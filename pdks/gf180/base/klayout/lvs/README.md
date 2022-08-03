# LVS Documentation

Explains how to use the runset.

## Folder Structure

```text
📦runset
 ┣ 📦testing
 ┣ 📜README.md
 ┣ 📜gf_018mcu.lvs
 ┣ 📜gf_018mcu.lyp
 ┗ 📜run_lvs.py
 ```

## Rule Deck Usage

The `run_lvs.py` script takes a gds file and a netlist to run LVS rule deck of GF180 technology with switches to select subsets of all checks.

### **Switches**

1. **GF180MCU**=A   : combined options of metal_level=3, mim_option=A, metal_top=30K, poly_res=1K, and mim_cap=2
2. **GF180MCU**=B   : combined options of metal_level=4, mim_option=B, metal_top=11K, poly_res=1K, and mim_cap=2
3. **GF180MCU**=C   : combined options of metal_level=5, mim_option=B, metal_top=9K,  poly_res=1K, and mim_cap=2

### Usage

```bash
    run_lvs.py (--help| -h)
    run_lvs.py (--design=<layout_path>) (--net=<netlist_path>) (--gf180mcu=<combined_options>) [--thr=<thr>] [--run_mode=<run_mode>] [--metal_top=<metal_top>] [--mim_option=<mim_option>] [--metal_level=<metal_level>] [--poly_res_val=<res_val>] [--mim_cap_val=<cap_val>] [--no_net_names] [--set_spice_comments] [--set_scale] [--set_verbose] [--set_schematic_simplify] [--set_net_only] [--set_top_lvl_pins] [--set_combine] [--set_purge] [--set_purge_nets]
```

Example:

```bash
    python3 run_lvs.py --path=testing/extraction_checking/sample_nmos_3p3.gds --net=sample_nmos_3p3.spice --thr=16 --gf180mcu=B --set_verbose --set_spice_comments
```

### Options

`--help -h`                         Print this help message.

`--design=<layout_path>`            The input GDS file path.

`--net=<netlist_path>`              The input netlist file path.

`--thr=<thr>`                       The number of threads used in run.

`run_mode=<run_mode>`               Select klayout mode Allowed modes (flat , deep, tiling). [default: flat]

`--gf180mcu=<combined_options>`     Select combined options of metal_top, mim_option, and metal_level. Allowed values (A, B, C).

`--no_net_names`                    Discard net names in extracted netlist.

`--set_spice_comments`              Set netlist comments in extracted netlist.

`--set_scale`                       Set scale of 1e6 in extracted netlist.

`--set_verbose`                     Set verbose mode.

`--set_schematic_simplify`          Set schematic simplification in input netlist.

`--set_net_only`                    Set netlist object creation only in extracted netlist.

`--set_top_lvl_pins`                Set top level pins only in extracted netlist.

`--set_combine`                     Set netlist combine only in extracted netlist.

`--set_purge`                       Set netlist purge all only in extracted netlist.

`--set_purge_nets`                  Set netlist purge nets only in extracted netlist.

### **LVS Outputs**

Final results will appear at the end of the run logs.

The output files are :

1. An extracted netlist (`<your_design_name>.cir`).

2. Database file (`<your_design_name>..lvdb`) for comparison results. you could view it on your file using klayout.
