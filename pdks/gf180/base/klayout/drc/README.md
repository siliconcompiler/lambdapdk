# DRC Documentation

Explains how to use the runset.

## Folder Structure

```text
📦drc
 ┣ 📦testing
 ┣ 📜GF180_MCU.lyp
 ┣ 📜README.md
 ┣ 📜gf_018mcu.drc
 ┣ 📜gf_018mcu_antenna.drc
 ┣ 📜gf_018mcu_density.drc
 ┗ 📜run_drc.py
 ```

## Rule Deck Usage

The `run_drc.py` script takes a gds file to run DRC rule decks of GF180 technology with switches to select subsets of all checks.

### **Switches**

1. **FEOL**          : Default is on. Use it for checking Front End Of Line layers (wells, diffusion, polys, contacts).
2. **BEOL**          : Default is on. Use it for checking Back End Of Line layers (metal layers, top metal layer, vias).
3. **BEOL**          : Default is on. Use it for checking Back End Of Line layers (metal layers, top metal layer, vias).
4. **GF180MCU**=A    : combined options of metal_level=3, mim_option=A, metal_top=30K, poly_res=1K, and mim_cap=2
5. **GF180MCU**=B    : combined options of metal_level=4, mim_option=B, metal_top=11K, poly_res=1K, and mim_cap=2
6. **GF180MCU**=C    : combined options of metal_level=5, mim_option=B, metal_top=9K,  poly_res=1K, and mim_cap=2
7. **connectivity**  : Default is off. Use it for check connectivity rules.
8. **DENSITY**       : Default is off. Use it for check density rules.
9. **DENSITY_only**  : Default is off. Use it for check density rules only.
10. **ANTENNA**       : Default is off. Use it to turn on Antenna checks.
11. **ANTENNA_only** : Default is off. Use it to turn on Antenna checks only.
12. **OFFGRID**      : Default is on. Use it for checking off-grid and acute layers (ongrid of 0.005um and angles 45 deg. unless otherwise stated).

### Usage

```bash
    run_drc.py (--help| -h)
    run_drc.py (--path=<file_path>) (--gf180mcu=<combined_options>) [--topcell=<topcell_name>] [--thr=<thr>] [--run_mode=<run_mode>] [--no_feol] [--no_beol] [--connectivity] [--density] [--density_only] [--antenna] [--antenna_only] [--no_offgrid]
```

Example:

```bash
    python3 run_drc.py --path=testing/switch_checking/switch_checking.gds --thr=16 --run_mode=flat --gf180mcu=A --antenna --no_offgrid
```

### Options

`--help -h`                           Print this help message.

`--path=<file_path>`                  The input GDS file path.

`--gf180mcu=<combined_options>`       Select combined options of metal_top, mim_option, and metal_level. Allowed values (A, B, C).
                                      gf180mcu=A: Select  metal_top=30K  mim_option=A  metal_level=3LM
                                      gf180mcu=B: Select  metal_top=11K  mim_option=B  metal_level=4LM
                                      gf180mcu=C: Select  metal_top=9K   mim_option=B  metal_level=5LM

`--topcell=<topcell_name>`            Topcell name to use.

`--thr=<thr>`                         The number of threads used in run.

`--run_mode=<run_mode>`               Select klayout mode Allowed modes (flat , deep, tiling). [default: flat]

`--no_feol`                           Turn off FEOL rules from running.

`--no_beol`                           Turn off BEOL rules from running.

`--connectivity`                      Turn on connectivity rules.

`--density`                           Turn on Density rules.

`--density_only`                      Turn on Density rules only.

`--antenna`                           Turn on Antenna checks.

`--antenna_only`                      Turn on Antenna checks only.

`--no_offgrid`                        Turn off OFFGRID checking rules.

### **DRC Outputs**

Results will appear at the end of the run logs.

The result is a database file (`<your_design_name>.lyrdb`) of all violations in the same directoy of your design. you could view it on your file using klayout.
