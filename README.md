# Lambdapdk

[![CI Tests](https://github.com/siliconcompiler/lambdapdk/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/siliconcompiler/lambdapdk/actions/workflows/ci.yml)
[![Wheels](https://github.com/siliconcompiler/lambdapdk/actions/workflows/wheels.yml/badge.svg?branch=main)](https://github.com/siliconcompiler/lambdapdk/actions/workflows/wheels.yml)
[![PyPI](https://img.shields.io/pypi/v/lambdapdk)](https://pypi.org/project/lambdapdk/)
[![Downloads](https://static.pepy.tech/badge/lambdapdk)](https://pepy.tech/project/lambdapdk)
[![GitHub stars](https://img.shields.io/github/stars/siliconcompiler/lambdapdk)](https://github.com/siliconcompiler/lambdapdk/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/siliconcompiler/lambdapdk)](https://github.com/siliconcompiler/lambdapdk/issues)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)


Lambdapdk is a collection of open-source Process Design Kits (PDKs) that enable chip design across multiple technology nodes. Each PDK includes standard cell libraries, I/O libraries, and memory compilers with full integration into the [SiliconCompiler](https://github.com/siliconcompiler/siliconcompiler) build system.

<!-- TODO: Add architecture diagram showing PDK relationship to design flow -->

## Why Lambdapdk?

### Challenges

- PDK setup is complex and error-prone
- Technology-specific designs limit portability
- Commercial PDKs have restrictive licenses
- Scattered PDK sources with inconsistent interfaces

### Solution

- Pre-configured PDKs ready for immediate use
- [Lambdalib](https://github.com/siliconcompiler/lambdalib) mapping enables design portability
- Fully open-source PDKs for research and education
- Unified API across all supported technologies

<!-- TODO: Add flow diagram showing design portability across PDKs -->

## Supported PDKs

| PDK | Node | Libraries | Source |
|-----|------|-----------|--------|
| [ASAP7](lambdapdk/asap7/README.md) | 7nm FinFET | Standard cells (RVT/LVT/SLVT), I/O, SRAM | Arizona State University |
| [FreePDK45](lambdapdk/freepdk45/base/README.md) | 45nm | Nangate standard cells, SRAM | NC State / Nangate |
| [Sky130](lambdapdk/sky130/README.md) | 130nm | Standard cells (HD/HDLL), I/O, SRAM | Google / Skywater |
| [GF180](lambdapdk/gf180/README.md) | 180nm | Standard cells (7T/9T), I/O, SRAM | Google / GlobalFoundries |
| [IHP130](https://github.com/IHP-GmbH/IHP-Open-PDK) | 130nm SiGe | Standard cells, I/O, SRAM | IHP GmbH |
| [Interposer](lambdapdk/interposer/README.md) | Multi-layer | Bump cells for chiplet integration | ZeroASIC |

## Quick Start

### Installation

```bash
pip install lambdapdk
```

### Basic Usage

```python
from siliconcompiler import ASIC, Design
from siliconcompiler.targets import skywater130_demo

# Create design and add source files
design = Design("mydesign")
design.set_topmodule("mydesign", fileset="rtl")
design.add_file("mydesign.v", fileset="rtl")
design.add_file("mydesign.sdc", fileset="sdc")

# Create ASIC project and load target
project = ASIC(design)
project.add_fileset(["rtl", "sdc"])
skywater130_demo(project)

# Run the flow
project.run()
project.summary()
```

Available targets: `asap7_demo`, `freepdk45_demo`, `skywater130_demo`, `gf180_demo`, `ihp130_demo`, `interposer_demo`

## Cell Library Inventory

### ASAP7 (7nm)

Standard cell libraries with three threshold voltage variants:

| Library | Type | Cells | Verilog |
|---------|------|-------|---------|
| [asap7sc7p5t_rvt](lambdapdk/asap7/libs/asap7sc7p5t_rvt) | Regular Vt | ~200 | [verilog](lambdapdk/asap7/libs/asap7sc7p5t_rvt/verilog) |
| [asap7sc7p5t_lvt](lambdapdk/asap7/libs/asap7sc7p5t_lvt) | Low Vt | ~200 | [verilog](lambdapdk/asap7/libs/asap7sc7p5t_lvt/verilog) |
| [asap7sc7p5t_slvt](lambdapdk/asap7/libs/asap7sc7p5t_slvt) | Super Low Vt | ~200 | [verilog](lambdapdk/asap7/libs/asap7sc7p5t_slvt/verilog) |

**Cell categories:** AND, OR, NAND, NOR, XOR, INV, BUF, MUX, DFF, Latch, Adder, Tie, Filler, Decap, Tap

**Memory macros ([fakeram7](lambdapdk/asap7/libs/fakeram7)):**

| Configuration | Verilog |
|--------------|---------|
| Single-port 64x32 to 8192x64 | [verilog](lambdapdk/asap7/libs/fakeram7/verilog) |
| Dual-port 64x32 to 8192x64 | [verilog](lambdapdk/asap7/libs/fakeram7/verilog) |
| True dual-port 64x32 to 8192x64 | [verilog](lambdapdk/asap7/libs/fakeram7/verilog) |

### FreePDK45 (45nm)

| Library | Type | Verilog |
|---------|------|---------|
| [nangate45](lambdapdk/freepdk45/libs/nangate45) | Standard cells | [lambda](lambdapdk/freepdk45/libs/nangate45/lambda/stdlib) |

**Cell categories:** AND, OR, NAND, NOR, XOR, INV, BUF, MUX, DFF, Latch, AOI, OAI, Tie, Filler, Tap

**Memory macros ([fakeram45](lambdapdk/freepdk45/libs/fakeram45)):**

| Configuration | Verilog |
|--------------|---------|
| 64x32 to 512x64 | [verilog](lambdapdk/freepdk45/libs/fakeram45/verilog) |

### Sky130 (130nm)

| Library | Type | Cells | Verilog |
|---------|------|-------|---------|
| [sky130hd](lambdapdk/sky130/libs/sky130hd) | High Density | ~430 unique | [verilog](lambdapdk/sky130/libs/sky130hd/verilog) |
| [sky130hdll](lambdapdk/sky130/libs/sky130hdll) | High Density Low Leakage | ~140 unique | [verilog](lambdapdk/sky130/libs/sky130hdll/verilog) |
| [sky130io](lambdapdk/sky130/libs/sky130io) | I/O cells | Various | [verilog](lambdapdk/sky130/libs/sky130io/verilog) |

**Cell categories:** AND, OR, NAND, NOR, XOR, INV, BUF, MUX, DFF, Latch, AOI, OAI, Delay, Tie, Filler, Decap, Tap, Antenna

**Memory macros ([sky130sram](lambdapdk/sky130/libs/sky130sram)):**

| Configuration | Verilog |
|--------------|---------|
| 1RW1R 64x256 | [verilog](lambdapdk/sky130/libs/sky130sram/sky130_sram_1rw1r_64x256_8/verilog) |

### GF180 (180nm)

| Library | Type | Cells | Verilog |
|---------|------|-------|---------|
| [gf180mcu_fd_sc_mcu7t5v0](lambdapdk/gf180/libs/gf180mcu_fd_sc_mcu7t5v0) | 7-track | ~230 | [verilog](lambdapdk/gf180/libs/gf180mcu_fd_sc_mcu7t5v0/verilog) |
| [gf180mcu_fd_sc_mcu9t5v0](lambdapdk/gf180/libs/gf180mcu_fd_sc_mcu9t5v0) | 9-track | ~230 | [verilog](lambdapdk/gf180/libs/gf180mcu_fd_sc_mcu9t5v0/verilog) |
| [gf180mcu_fd_io](lambdapdk/gf180/libs/gf180mcu_fd_io) | I/O cells | Various | [verilog](lambdapdk/gf180/libs/gf180mcu_fd_io/verilog) |

**Cell categories:** AND, OR, NAND, NOR, XOR, INV, BUF, MUX, DFF, Latch, AOI, OAI, Tristate, Delay, Tie, Filler, Decap, Tap, Antenna

**Memory macros ([gf180sram](lambdapdk/gf180/libs/gf180mcu_fd_ip_sram)):**

| Configuration | Verilog |
|--------------|---------|
| 64x8 to 512x8 | [verilog](lambdapdk/gf180/libs/gf180mcu_fd_ip_sram/verilog) |

### IHP130 (130nm SiGe)

| Library | Type | Verilog |
|---------|------|---------|
| [sg13g2_stdcell](lambdapdk/ihp130/libs/sg13g2_stdcell) | Standard cells | [lambda](lambdapdk/ihp130/libs/sg13g2_stdcell/lambda/stdlib) |
| [sg13g2_io](lambdapdk/ihp130/libs/sg13g2_io) | I/O cells | [blackbox](lambdapdk/ihp130/libs/sg13g2_io/blackbox) |

Note: IHP130 cell views are provided by the [IHP Open PDK](https://github.com/IHP-GmbH/IHP-Open-PDK).

### Interposer

| Library | Type | Description |
|---------|------|-------------|
| [bumps](lambdapdk/interposer/libs/bumps) | Bump cells | Micro-bump cells for chiplet integration |

Stackup variants: 3ML, 4ML, 5ML with 400um, 800um, and 2000um bump pitches.

## Architecture

```
lambdapdk/
├── asap7/           # 7nm FinFET PDK
│   ├── base/        # Technology files, DRC rules
│   └── libs/        # Standard cells, I/O, memory
├── freepdk45/       # 45nm PDK
│   ├── base/
│   └── libs/
├── sky130/          # 130nm PDK
│   ├── base/
│   └── libs/
├── gf180/           # 180nm PDK
│   ├── base/
│   └── libs/
├── ihp130/          # 130nm SiGe PDK
│   ├── base/
│   └── libs/
└── interposer/      # Passive interposer
    ├── base/
    └── libs/
```

## Contributing

We welcome contributions! Please report issues and submit pull requests at:
https://github.com/siliconcompiler/lambdapdk/issues

## License

This project is licensed under the [Apache License 2.0](LICENSE).

Individual PDKs may have additional license terms:

| PDK | License | Details |
|-----|---------|---------|
| ASAP7 | BSD 3-Clause | [LICENSE](lambdapdk/asap7/libs/asap7sc7p5t_rvt/LICENSE) |
| Nangate45 | Nangate Open Cell Library License | [LICENSE](lambdapdk/freepdk45/libs/nangate45/LICENSE) (non-commercial use) |
| Sky130 | Apache 2.0 | Via [open_pdks](https://github.com/RTimothyEdwards/open_pdks) |
| GF180 | Apache 2.0 | Via [gf180mcu-pdk](https://github.com/google/gf180mcu-pdk) |
| IHP130 | Apache 2.0 | Via [IHP-Open-PDK](https://github.com/IHP-GmbH/IHP-Open-PDK) |
| Interposer | Apache 2.0 | Copyright 2024 ZeroASIC Corp |

Copyright 2023 Zero ASIC Corporation
