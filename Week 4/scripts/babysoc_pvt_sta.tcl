# ============================================================
# BabySoC - PVT Timing Analysis
# OpenSTA 3.1.0
# Technology: SKY130 HD
#
# Usage:
# sta -exit babysoc_pvt_sta.tcl CORNER_NAME
# ============================================================

set PROJECT_DIR [file normalize [file join [file dirname [info script]] ../../..]]
set WORK_DIR "$PROJECT_DIR/work/week4_opensta"
set LIB_DIR "$WORK_DIR/lib/sky130_pvt"

# ------------------------------------------------------------
# 1. Select PVT corner
# ------------------------------------------------------------

if {[info exists ::env(PVT_CORNER)]} {
    set corner $::env(PVT_CORNER)
} else {
    set corner "tt_025C_1v80"
}

set liberty_file "$LIB_DIR/sky130_fd_sc_hd__${corner}.lib"

if {![file exists $liberty_file]} {
    error "Liberty file not found: $liberty_file"
}

puts "============================================"
puts "BabySoC PVT Timing Analysis"
puts "Corner: $corner"
puts "============================================"

# ------------------------------------------------------------
# 2. Load Liberty files
# ------------------------------------------------------------

read_liberty $liberty_file

read_liberty "$WORK_DIR/lib/avsdpll_sta.lib"
read_liberty "$PROJECT_DIR/src/lib/avsddac.lib"

# ------------------------------------------------------------
# 3. Load synthesized BabySoC netlist
# ------------------------------------------------------------

read_verilog "$PROJECT_DIR/output/synth/vsdbabysoc.synth.v"

link_design vsdbabysoc

# ------------------------------------------------------------
# 4. Apply timing constraints
# ------------------------------------------------------------

read_sdc "$WORK_DIR/constraints/babysoc.sdc"

# ------------------------------------------------------------
# 5. Create corner-specific report directory
# ------------------------------------------------------------

set REPORT_DIR "$WORK_DIR/reports/pvt/$corner"

file mkdir $REPORT_DIR

# ------------------------------------------------------------
# 6. Check timing constraints
# ------------------------------------------------------------

check_setup -verbose > "$REPORT_DIR/check_setup.rpt"

# ------------------------------------------------------------
# 7. Setup timing report
# ------------------------------------------------------------

report_checks -path_delay max \
    -fields {slew cap fanout} \
    -digits 4 \
    > "$REPORT_DIR/setup_timing.rpt"

# ------------------------------------------------------------
# 8. Hold timing report
# ------------------------------------------------------------

report_checks -path_delay min \
    -fields {slew cap fanout} \
    -digits 4 \
    > "$REPORT_DIR/hold_timing.rpt"

# ------------------------------------------------------------
# 9. Internal register-to-register hold
# ------------------------------------------------------------

report_checks -path_delay min \
    -from [all_registers -clock_pins] \
    -to [all_registers -data_pins] \
    -fields {slew cap fanout} \
    -digits 4 \
    > "$REPORT_DIR/internal_hold_timing.rpt"

# ------------------------------------------------------------
# 10. Worst slack reports
# ------------------------------------------------------------

report_worst_slack -max \
    > "$REPORT_DIR/worst_setup_slack.rpt"

report_worst_slack -min \
    > "$REPORT_DIR/worst_hold_slack.rpt"

# ------------------------------------------------------------
# 11. WNS and TNS
# ------------------------------------------------------------

report_wns > "$REPORT_DIR/wns.rpt"

report_tns > "$REPORT_DIR/tns.rpt"

puts "============================================"
puts "PVT analysis completed: $corner"
puts "Reports: $REPORT_DIR"

# ------------------------------------------------------------
# 12. Hold WNS and TNS
# ------------------------------------------------------------

report_wns -min > "$REPORT_DIR/hold_wns.rpt"

report_tns -min > "$REPORT_DIR/hold_tns.rpt"

puts "============================================"
