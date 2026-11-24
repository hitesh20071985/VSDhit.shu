# ============================================================
# Week 4 - BabySoC Static Timing Analysis
# Tool: OpenSTA
# Technology: SKY130 HD
# Corner: TT, 25C, 1.80V
# ============================================================

set PROJECT_DIR [file normalize [file join [file dirname [info script]] ../../..]]
set WORK_DIR "$PROJECT_DIR/work/week4_opensta"

# ------------------------------------------------------------
# 1. Load Liberty libraries
# ------------------------------------------------------------

read_liberty "$PROJECT_DIR/src/lib/sky130_fd_sc_hd__tt_025C_1v80.lib"
read_liberty "$PROJECT_DIR/work/week4_opensta/lib/avsdpll_sta.lib"
read_liberty "$PROJECT_DIR/src/lib/avsddac.lib"

# ------------------------------------------------------------
# 2. Load synthesized netlist
# ------------------------------------------------------------

read_verilog "$PROJECT_DIR/output/synth/vsdbabysoc.synth.v"

# ------------------------------------------------------------
# 3. Link top-level design
# ------------------------------------------------------------

link_design vsdbabysoc

# ------------------------------------------------------------
# 4. Apply timing constraints
# ------------------------------------------------------------

read_sdc "$WORK_DIR/constraints/babysoc.sdc"

# ------------------------------------------------------------
# 5. Check timing constraints
# ------------------------------------------------------------

check_setup -verbose

# ------------------------------------------------------------
# 6. Generate timing reports
# ------------------------------------------------------------

report_checks -path_delay max \
    -fields {slew cap fanout} \
    -digits 4 \
    > "$WORK_DIR/reports/setup_timing.rpt"

report_checks -path_delay min \
    -fields {slew cap fanout} \
    -digits 4 \
    > "$WORK_DIR/reports/hold_timing.rpt"

report_worst_slack -max \
    > "$WORK_DIR/reports/worst_setup_slack.rpt"

report_worst_slack -min \
    > "$WORK_DIR/reports/worst_hold_slack.rpt"

report_wns \
    > "$WORK_DIR/reports/wns.rpt"

report_tns \
    > "$WORK_DIR/reports/tns.rpt"


# ------------------------------------------------------------
# Internal register-to-register hold timing
# ------------------------------------------------------------

report_checks -path_delay min     -from [all_registers -clock_pins]     -to [all_registers -data_pins]     -fields {slew cap fanout}     -digits 4     > "$WORK_DIR/reports/internal_hold_timing.rpt"

puts "============================================"
puts "BabySoC OpenSTA analysis completed"
puts "Reports directory: $WORK_DIR/reports"
puts "============================================"
