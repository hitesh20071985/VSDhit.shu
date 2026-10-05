# RTL Design, Synthesis and Verification using Open-Source EDA Tools

This repository documents the practical RTL design, simulation, synthesis, optimization, and verification experiments reproduced as part of the VSD RTL Design and Synthesis learning flow.

The objective is to demonstrate how Verilog RTL moves through simulation, synthesis, technology mapping, optimization, and gate-level verification using open-source EDA tools. The screenshots included in this README are the **actual outputs available in the repository's `Images` folder**.

---

## Contents

1. [Environment and Tool Installation](#1-environment-and-tool-installation)
2. [RTL Simulation using Icarus Verilog and GTKWave](#2-rtl-simulation-using-icarus-verilog-and-gtkwave)
3. [Logic Synthesis using Yosys](#3-logic-synthesis-using-yosys)
4. [Technology Library and Netlist Analysis](#4-technology-library-and-netlist-analysis)
5. [Hierarchical and Flattened Synthesis](#5-hierarchical-and-flattened-synthesis)
6. [Sequential Logic and Flip-Flop Coding Styles](#6-sequential-logic-and-flip-flop-coding-styles)
7. [Combinational and Sequential Optimization](#7-combinational-and-sequential-optimization)
8. [Gate-Level Simulation and Synthesis-Simulation Mismatch](#8-gate-level-simulation-and-synthesis-simulation-mismatch)
9. [Incomplete If and Case Statements](#9-incomplete-if-and-case-statements)
10. [Generate Constructs](#10-generate-constructs)
11. [Ripple-Carry Adder](#11-ripple-carry-adder)
12. [Reproducing the Results](#12-reproducing-the-results)
13. [Key Takeaways](#13-key-takeaways)
14. [References](#14-references)

---

# 1. Environment and Tool Installation

The experiments were reproduced on Ubuntu 22.04 running inside a virtual machine.

### Recommended Host/VM Configuration

| Item | Recommended Configuration |
|---|---|
| Operating System | Ubuntu 22.04 LTS |
| RAM | 8 GB minimum |
| Storage | 100 GB minimum |
| Virtualization | Oracle VirtualBox |
| 3D Acceleration | Disabled if graphical instability is observed |
| RTL Language | Verilog |

The main tools used in this flow are:

- **Yosys** — RTL synthesis and technology mapping
- **Icarus Verilog** — Verilog compilation and simulation
- **GTKWave** — waveform analysis
- **OpenSTA** — static timing analysis
- **ngspice** — SPICE simulation
- **Magic** — layout viewing/editing
- **OpenLANE** — RTL-to-GDS implementation flow
- **Sky130 standard-cell library** — technology library

## Icarus Verilog Installation Verification

```bash
iverilog -V
```

<p align="center">
  <img src="Images/0Iverilog_Installation_Version.png" width="900" alt="Icarus Verilog installation and version output">
</p>

## Yosys Installation Verification

```bash
yosys -V
```

<p align="center">
  <img src="Images/0Yosys_Version_Output.png" width="900" alt="Yosys version output">
</p>

---

# 2. RTL Simulation using Icarus Verilog and GTKWave

RTL simulation checks the functional behaviour of a design before synthesis.

A typical simulation flow is:

```text
Verilog RTL
    +
Testbench
    |
    v
Icarus Verilog
    |
    v
Simulation executable
    |
    v
VCD waveform
    |
    v
GTKWave
```

## GTKWave Interface

After simulation, the generated waveform can be opened with:

```bash
gtkwave <waveform_file>.vcd
```

<p align="center">
  <img src="Images/1GTKwave_GUI_for_TB.png" width="900" alt="GTKWave GUI used for testbench waveform analysis">
</p>

## Good Mux RTL Simulation

A basic 2:1 multiplexer is used to demonstrate the RTL simulation flow.

A representative RTL implementation is:

```verilog
module good_mux (
    input  i0,
    input  i1,
    input  sel,
    output reg y
);

always @(*) begin
    if (sel)
        y = i1;
    else
        y = i0;
end

endmodule
```

Compile the DUT and testbench:

```bash
iverilog good_mux.v tb_good_mux.v
```

Run the simulation:

```bash
./a.out
```

Open the VCD file in GTKWave:

```bash
gtkwave tb_good_mux.vcd
```

### Simulation Output

<p align="center">
  <img src="Images/2Good_Mux_Simulation.png" width="900" alt="Good mux RTL simulation output">
</p>

### RTL and Testbench

<p align="center">
  <img src="Images/3Good_Mux_And_TestBench.png" width="900" alt="Good mux RTL and testbench">
</p>

---

# 3. Logic Synthesis using Yosys

Logic synthesis converts RTL into a gate-level representation while preserving the required logical functionality.

Start Yosys:

```bash
yosys
```

Read the Verilog design:

```text
read_verilog good_mux.v
```

Run synthesis:

```text
synth -top good_mux
```

View the synthesized structure:

```text
show
```

## Good Mux Synthesized Structure

<p align="center">
  <img src="Images/4Good_Mux_Synth.png" width="900" alt="Good mux synthesized structure">
</p>

## Good Mux Synthesized Netlist

A synthesized Verilog netlist can be generated using:

```text
write_verilog good_mux_netlist.v
```

<p align="center">
  <img src="Images/5Good_Mux_Netlist.png" width="900" alt="Good mux synthesized netlist">
</p>

The synthesized implementation does not need to look structurally identical to the RTL. Synthesis can simplify Boolean expressions and select a different gate-level implementation while retaining equivalent behaviour.

---

# 4. Technology Library and Netlist Analysis

Technology mapping uses cells available in the selected standard-cell library.

A Liberty file can be loaded in Yosys using:

```text
read_liberty -lib sky130_fd_sc_hd__tt_025C_1v80.lib
```

The synthesis and mapping flow can then use:

```text
read_verilog good_mux.v
synth -top good_mux
dfflibmap -liberty sky130_fd_sc_hd__tt_025C_1v80.lib
abc -liberty sky130_fd_sc_hd__tt_025C_1v80.lib
write_verilog good_mux_netlist.v
```

> The flow intentionally does not include a separate `clean` command.

## Good 2:1 Mux

<p align="center">
  <img src="Images/9Good2x1Mux.png" width="900" alt="Good 2 to 1 mux">
</p>

## Technology-Mapped Good Mux Netlist

<p align="center">
  <img src="Images/10GoodMux_Netlist.png" width="900" alt="Technology mapped good mux netlist">
</p>

## Netlist without Additional Attributes

<p align="center">
  <img src="Images/11Good_Mux_Noattr_Netlist.png" width="900" alt="Good mux noattr netlist">
</p>

## Sky130 Library

The Sky130 Liberty library contains standard-cell definitions, timing information, drive-strength variants, and other characteristics required for technology-aware synthesis.

<p align="center">
  <img src="Images/12SKY_Library.png" width="900" alt="Sky130 Liberty library">
</p>

Different cell choices represent trade-offs among:

- timing
- output drive
- area
- power
- transition time
- load capability

This is one of the key links between RTL synthesis and **Power, Performance and Area (PPA)**.

---

# 5. Hierarchical and Flattened Synthesis

Complex RTL is normally constructed using multiple modules. Synthesis can preserve these boundaries or flatten them.

## Multiple-Module Synthesis

<p align="center">
  <img src="Images/6Multiple_Modules_Synth.png" width="900" alt="Multiple modules synthesized structure">
</p>

## Hierarchical Netlist

<p align="center">
  <img src="Images/7Multiple_ModulesNetlist.png" width="900" alt="Multiple modules hierarchical netlist">
</p>

## Flattened Netlist

The `flatten` command removes module hierarchy:

```text
flatten
```

<p align="center">
  <img src="Images/8Multiple_Modules_Flatten_Netlist.png" width="900" alt="Flattened multiple modules netlist">
</p>

## Multiple Modules RTL

<p align="center">
  <img src="Images/13_Multiple_Modules.png" width="900" alt="Multiple modules RTL">
</p>

## Multiple Modules Synthesis

<p align="center">
  <img src="Images/14Multiple_ModulesSynth.png" width="900" alt="Multiple modules synthesis">
</p>

## Multiple Modules Netlist

<p align="center">
  <img src="Images/15Multiple_Modules_Netlist.png" width="900" alt="Multiple modules synthesized netlist">
</p>

## Hierarchical Representation

<p align="center">
  <img src="Images/16Multiple_Modules.png" width="900" alt="Multiple modules hierarchical representation">
</p>

## Individual Submodule Synthesis

A submodule can also be synthesized independently by choosing it as the top module.

<p align="center">
  <img src="Images/17AndGateSynthSubModule1.png" width="900" alt="AND gate synthesized from submodule 1">
</p>

Hierarchical synthesis is useful for large and reusable blocks, whereas flattening can expose additional cross-boundary optimization opportunities.

---

# 6. Sequential Logic and Flip-Flop Coding Styles

Flip-flops store state and are fundamental to sequential logic.

Three important coding styles considered here are:

- asynchronous reset
- asynchronous set
- synchronous reset

## DFF Coding Examples

<p align="center">
  <img src="Images/18Dff_AsyncRes_Sync_Reset_Verilog_Code.png" width="900" alt="DFF asynchronous reset and synchronous reset Verilog examples">
</p>

### Asynchronous Reset RTL

```verilog
always @(posedge clk or posedge reset) begin
    if (reset)
        q <= 1'b0;
    else
        q <= d;
end
```

<p align="center">
  <img src="Images/19DFF_Asyncres_Verilog_Code.png" width="900" alt="DFF asynchronous reset Verilog code">
</p>

### Synchronous Reset RTL

```verilog
always @(posedge clk) begin
    if (reset)
        q <= 1'b0;
    else
        q <= d;
end
```

<p align="center">
  <img src="Images/20DFF_SyncRes_Verilog_Code.png" width="900" alt="DFF synchronous reset Verilog code">
</p>

<p align="center">
  <img src="Images/21DFF_Syncres_Verilog_code.png" width="900" alt="DFF synchronous reset code example">
</p>

## Simulation Results

### Asynchronous Reset

<p align="center">
  <img src="Images/22DFF_Asyncres_TB_Output.png" width="900" alt="DFF asynchronous reset testbench output">
</p>

### Asynchronous Set

<p align="center">
  <img src="Images/23DFF_Async_set_TB_Output" width="900" alt="DFF asynchronous set testbench output">
</p>

### Synchronous Reset

<p align="center">
  <img src="Images/24DFF_Sync_reset_TB_Output.png" width="900" alt="DFF synchronous reset testbench output">
</p>

## Synthesized Flip-Flops

### Asynchronous Reset DFF

<p align="center">
  <img src="Images/25Synth_DFF_Asyncres.png" width="900" alt="Synthesized DFF with asynchronous reset">
</p>

### Set-Controlled DFF

<p align="center">
  <img src="Images/26DFF_Sync_Set_Synth.png" width="900" alt="Synthesized DFF with set control">
</p>

### Synchronous Reset DFF

<p align="center">
  <img src="Images/27DFF_Syncres_Synth.png" width="900" alt="Synthesized DFF with synchronous reset">
</p>

The inferred hardware depends directly on the reset/set coding style used in the RTL.

---

# 7. Combinational and Sequential Optimization

Synthesis tools simplify logic while preserving functional behaviour.

Common optimization mechanisms include:

- constant propagation
- Boolean simplification
- unused logic removal
- redundant gate elimination
- sequential constant propagation
- register optimization

## Combinational Optimization Examples

### AND Gate after Optimization

<p align="center">
  <img src="Images/28AND_gate_Post_Optimization.png" width="900" alt="AND gate after optimization">
</p>

### OR Gate after Optimization

<p align="center">
  <img src="Images/29ORGATE_Post_Optimization.png" width="900" alt="OR gate after optimization">
</p>

### Three-Input AND Optimization

<p align="center">
  <img src="Images/30AndGate3input_post_opt.png" width="900" alt="Three input AND gate after optimization">
</p>

### XNOR Optimization

<p align="center">
  <img src="Images/31XNOR_2input_post_optimization.png" width="900" alt="Two-input XNOR after optimization">
</p>

## Counter Optimization

<p align="center">
  <img src="Images/32Counter_Synth_Post_Optimization.png" width="900" alt="Counter synthesis after optimization">
</p>

<p align="center">
  <img src="Images/33Counter_3output_post_optimization.png" width="900" alt="Three-output counter after optimization">
</p>

## Sequential Constant Propagation

### Constant Sequential Example 1 — Simulation

<p align="center">
  <img src="Images/34TB_DFF_Const_sequential1.png" width="900" alt="DFF constant sequential example 1 testbench">
</p>

### Constant Sequential Example 2 — Simulation

<p align="center">
  <img src="Images/35TB_DFF_Const_Sequenctial2.png" width="900" alt="DFF constant sequential example 2 testbench">
</p>

### Constant Sequential Example 1 — Synthesized Result

<p align="center">
  <img src="Images/36Synth_dff_Const1_Synth.png" width="900" alt="DFF constant example 1 synthesized output">
</p>

### Constant Sequential Example 2 — Synthesized Result

<p align="center">
  <img src="Images/37DFF_Const2_Synth.png" width="900" alt="DFF constant example 2 synthesized output">
</p>

### Constant Sequential Example 3 — Simulation

<p align="center">
  <img src="Images/38DFF_Const3_TB.png" width="900" alt="DFF constant example 3 testbench">
</p>

### Constant Sequential Example 3 — Synthesis

<p align="center">
  <img src="Images/39DFF_Const3_Synth.png" width="900" alt="DFF constant example 3 synthesized output">
</p>

## Additional Counter Optimization Results

<p align="center">
  <img src="Images/40counter_Opt_Synth.png" width="900" alt="Optimized counter synthesis">
</p>

<p align="center">
  <img src="Images/41Synth_counter3out_opt.png" width="900" alt="Synthesized optimized three-output counter">
</p>

These experiments demonstrate that synthesis can remove or simplify registers and combinational logic when their values become statically determinable.

---

# 8. Gate-Level Simulation and Synthesis-Simulation Mismatch

Gate-Level Simulation (GLS) verifies the synthesized netlist using technology-library models.

The basic flow is:

```text
Synthesized Netlist
      +
Standard-Cell Models
      +
Testbench
      |
      v
Icarus Verilog
      |
      v
Waveform
      |
      v
GTKWave
```

A representative GLS command is:

```bash
iverilog \
  ../my_lib/verilog_model/primitives.v \
  ../my_lib/verilog_model/sky130_fd_sc_hd.v \
  ternary_operator_mux_net.v \
  tb_ternary_operator_mux.v
```

## Ternary-Operator Mux Testbench

<p align="center">
  <img src="Images/42TB_Ternary_operator_MUX.png" width="900" alt="Ternary operator mux testbench output">
</p>

## Ternary-Operator 2:1 Mux

<p align="center">
  <img src="Images/43Ternary_Operator2x1_Mux.png" width="900" alt="Ternary operator 2 to 1 mux">
</p>

## RTL / Synthesized Behaviour Comparison

<p align="center">
  <img src="Images/44ternary_Operator_Mux_RTL_Not_Matching_with_Placed.png" width="900" alt="Ternary operator mux RTL and synthesized comparison">
</p>

## Missing Sensitivity List — Bad Mux

One important source of synthesis-simulation mismatch is an incomplete sensitivity list.

Problematic example:

```verilog
always @(sel) begin
    if (sel)
        y = i1;
    else
        y = i0;
end
```

Only changes in `sel` trigger the procedural block during simulation even though `i0` and `i1` also influence the output.

### Bad Mux Simulation

<p align="center">
  <img src="Images/45Bad_Mux_TB.png" width="900" alt="Bad mux testbench output">
</p>

<p align="center">
  <img src="Images/46Bad_Mux_TB1.png" width="900" alt="Bad mux additional testbench output">
</p>

The preferred combinational coding style is:

```verilog
always @(*) begin
    if (sel)
        y = i1;
    else
        y = i0;
end
```

## Blocking Assignment Caveat

Statement ordering matters when blocking assignments are used.

Example:

```verilog
always @(*) begin
    d = x & c;
    x = a | b;
end
```

Here `d` can use the previous value of `x` in RTL simulation.

### Synthesized Result

<p align="center">
  <img src="Images/48Blocking_caveat_MUx_Synth.png" width="900" alt="Blocking caveat mux synthesized result">
</p>

### Simulation Result

<p align="center">
  <img src="Images/49Blocking_caveat_TB.png" width="900" alt="Blocking caveat testbench output">
</p>

A safer form is:

```verilog
always @(*) begin
    x = a | b;
    d = x & c;
end
```

---

# 9. Incomplete If and Case Statements

Incomplete assignments in combinational procedural blocks can infer latches.

## Incomplete `if`

### Simulation

<p align="center">
  <img src="Images/50TB_Incomplete_IF.png" width="900" alt="Incomplete if testbench output">
</p>

### Synthesized Result

<p align="center">
  <img src="Images/51Synth_Incomplete_IF.png" width="900" alt="Incomplete if synthesized output">
</p>

## Second Incomplete `if` Example

### Simulation

<p align="center">
  <img src="Images/52TB_incomplete_if2.png" width="900" alt="Second incomplete if testbench output">
</p>

### Synthesized Result

<p align="center">
  <img src="Images/53Synth_Incomp_IF2.png" width="900" alt="Second incomplete if synthesized output">
</p>

## Incomplete `case`

### Simulation

<p align="center">
  <img src="Images/53TB_Incomplete_case.png" width="900" alt="Incomplete case testbench output">
</p>

### Synthesized Result

<p align="center">
  <img src="Images/55Synth_Incomp_case.png" width="900" alt="Incomplete case synthesized output">
</p>

## Complete `case`

A combinational `case` should normally cover all possible selector values or provide a `default` assignment.

Example:

```verilog
always @(*) begin
    case (sel)
        2'b00: y = i0;
        2'b01: y = i1;
        2'b10: y = i2;
        2'b11: y = i3;
        default: y = 1'b0;
    endcase
end
```

### Synthesized Complete Case

<p align="center">
  <img src="Images/56Synth_Complete_case.png" width="900" alt="Complete case synthesized output">
</p>

### Complete Case Simulation

<p align="center">
  <img src="Images/57TB_Complete_case.png" width="900" alt="Complete case testbench output">
</p>

### Additional Complete Case Result

<p align="center">
  <img src="Images/image58.png" width="900" alt="Additional complete case result">
</p>

### Complete Case Example 2 — Synthesis

<p align="center">
  <img src="Images/59Synth_Comp_Case2.png" width="900" alt="Complete case example 2 synthesized output">
</p>

## Bad Case Example

<p align="center">
  <img src="Images/60TB_BAD_CASE.png" width="900" alt="Bad case testbench output">
</p>

The central lesson is that combinational outputs should be assigned for every possible execution path to avoid unintended storage inference.

---

# 10. Generate Constructs

Generate constructs are useful when structurally repeating hardware.

A common pattern is:

```verilog
genvar i;

generate
    for (i = 0; i < N; i = i + 1) begin : GEN_BLOCK
        // replicated hardware
    end
endgenerate
```

## Mux using Generate

### Testbench Output

<p align="center">
  <img src="Images/61TB_Mux_Generate.png" width="900" alt="Mux generate testbench output">
</p>

### Synthesized Result

<p align="center">
  <img src="Images/62Synth_Mux_generate.png" width="900" alt="Mux generate synthesized output">
</p>

## Demux using Generate

<p align="center">
  <img src="Images/63TB_Demux_generate.png" width="900" alt="Demux generate testbench output">
</p>

Unlike a procedural software loop, a synthesizable generate loop elaborates multiple pieces of hardware.

---

# 11. Ripple-Carry Adder

A Ripple-Carry Adder (RCA) is constructed by cascading full-adder stages.

For every bit position:

```text
 A[i] ----\
           \
 B[i] -----> Full Adder -----> SUM[i]
           /
CARRY[i] -/

                    |
                    v
               CARRY[i+1]
```

A one-bit full adder can be described as:

```verilog
module full_adder (
    input  a,
    input  b,
    input  cin,
    output sum,
    output cout
);

assign sum  = a ^ b ^ cin;
assign cout = (a & b) | (b & cin) | (a & cin);

endmodule
```

A parameterized ripple-carry adder can be implemented with `generate`:

```verilog
module ripple_carry_adder #(
    parameter N = 4
)(
    input  [N-1:0] a,
    input  [N-1:0] b,
    input          cin,
    output [N-1:0] sum,
    output         cout
);

wire [N:0] carry;

assign carry[0] = cin;
assign cout = carry[N];

genvar i;

generate
    for (i = 0; i < N; i = i + 1) begin : RCA_STAGE
        full_adder FA (
            .a    (a[i]),
            .b    (b[i]),
            .cin  (carry[i]),
            .sum  (sum[i]),
            .cout (carry[i+1])
        );
    end
endgenerate

endmodule
```

## Ripple-Carry Adder Testbench Result

<p align="center">
  <img src="Images/64TB_Ripple_carry_Adder.png" width="900" alt="Ripple carry adder testbench output">
</p>

The main timing limitation of an RCA is the propagation of carry from one stage to the next.

---

# 12. Reproducing the Results

## Clone the Repository

```bash
git clone https://github.com/hitesh20071985/VSDhit.shu.git
cd VSDhit.shu
```

## Verify the Tools

```bash
yosys -V
iverilog -V
gtkwave --version
sta -version
ngspice --version
magic --version
```

## RTL Simulation Flow

```bash
iverilog <rtl_file.v> <testbench.v>
./a.out
gtkwave <waveform.vcd>
```

## Basic Yosys Synthesis Flow

```bash
yosys
```

Then inside Yosys:

```text
read_verilog <rtl_file.v>
synth -top <top_module>
show
write_verilog <output_netlist.v>
```

## Technology-Mapped Synthesis Flow

```text
read_liberty -lib <library.lib>
read_verilog <rtl_file.v>
synth -top <top_module>
dfflibmap -liberty <library.lib>
abc -liberty <library.lib>
write_verilog <output_netlist.v>
```

## Gate-Level Simulation

```bash
iverilog \
  <primitive_models.v> \
  <standard_cell_models.v> \
  <synthesized_netlist.v> \
  <testbench.v>

./a.out
gtkwave <waveform.vcd>
```

When comparing RTL and gate-level behaviour, verify:

- output functionality
- reset/set operation
- multiplexer selection
- sequential state transitions
- absence of unintended latch behaviour
- consistency between intended RTL functionality and synthesized hardware

---

# 13. Key Takeaways

The experiments in this repository demonstrate the practical relationship among RTL coding style, simulation behaviour, synthesis results, and gate-level implementation.

Important observations include:

- RTL describes hardware behaviour and structure rather than software-style execution.
- RTL simulation should be performed before synthesis to verify intended functionality.
- Synthesis can substantially simplify logic while preserving equivalent functionality.
- Standard-cell libraries determine which technology cells are available for mapping.
- Cell choice directly affects power, performance, and area.
- Hierarchical synthesis preserves design structure, while flattening removes hierarchy and may expose additional optimization.
- Reset and set coding styles determine the type of sequential element inferred by synthesis.
- Constant propagation can remove significant amounts of redundant combinational and sequential logic.
- Incomplete sensitivity lists can produce simulation-synthesis mismatches.
- Improper blocking assignment ordering can create unexpected RTL simulation behaviour.
- Incomplete `if` and `case` statements can infer unintended latches.
- Generate constructs provide a scalable mechanism for structural RTL replication.
- Gate-level simulation provides an additional check that the synthesized implementation behaves consistently with the original RTL intent.

---

# 14. References

- [Yosys Open SYnthesis Suite](https://github.com/YosysHQ/yosys)
- [Icarus Verilog](https://github.com/steveicarus/iverilog)
- [GTKWave](https://gtkwave.sourceforge.net/)
- [OpenSTA](https://github.com/The-OpenROAD-Project/OpenSTA)
- [OpenROAD Project](https://github.com/The-OpenROAD-Project)
- [SkyWater SKY130 PDK](https://github.com/google/skywater-pdk)
- [VSD Open-Source Hardware and RTL Learning Resources](https://github.com/vsdip)

---

## Repository Images

All screenshots referenced in this README are stored in:

```text
Images/
```

The README uses relative paths such as:

```markdown
![Example](Images/2Good_Mux_Simulation.png)
```

This ensures that images render directly when the repository is viewed on GitHub.

---

## Acknowledgement

This repository serves as a practical learning and reproduction record for RTL design, simulation, synthesis, optimization, and verification exercises performed using the VSD training flow and open-source EDA tools.
