#!/usr/bin/env python3

import csv
import re
from pathlib import Path

WORK_DIR = Path.home() / "VSDBabySoC/work/week4_opensta"
REPORT_DIR = WORK_DIR / "reports/pvt"
OUTPUT_DIR = WORK_DIR / "csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CSV_FILE = OUTPUT_DIR / "babysoc_pvt_timing_summary.csv"


def extract_value(path, pattern):
    """Extract a numerical timing value from an OpenSTA report."""
    if not path.is_file():
        raise FileNotFoundError(f"Missing report: {path}")

    text = path.read_text()

    match = re.search(pattern, text, re.MULTILINE)

    if not match:
        raise ValueError(f"Timing value not found in {path}")

    return float(match.group(1))


def corner_details(corner):
    """Extract process, temperature and voltage from corner name."""
    match = re.fullmatch(
        r"(tt|ff|ss)_(n?\d+)C_(\d+)v(\d+)",
        corner
    )

    if not match:
        raise ValueError(f"Invalid PVT corner: {corner}")

    process, temp, voltage_int, voltage_frac = match.groups()

    temperature = int(temp.replace("n", "-"))
    voltage = float(f"{voltage_int}.{voltage_frac}")

    return process.upper(), temperature, voltage


rows = []

for corner_dir in sorted(REPORT_DIR.iterdir()):

    if not corner_dir.is_dir():
        continue

    corner = corner_dir.name

    process, temperature, voltage = corner_details(corner)

    setup_slack = extract_value(
        corner_dir / "worst_setup_slack.rpt",
        r"worst slack max\s+([-+]?\d*\.?\d+)"
    )

    overall_hold = extract_value(
        corner_dir / "worst_hold_slack.rpt",
        r"worst slack min\s+([-+]?\d*\.?\d+)"
    )

    internal_hold = extract_value(
        corner_dir / "internal_hold_timing.rpt",
        r"([-+]?\d*\.?\d+)\s+slack\s+\("
    )

    setup_wns = extract_value(
        corner_dir / "wns.rpt",
        r"wns max\s+([-+]?\d*\.?\d+)"
    )

    setup_tns = extract_value(
        corner_dir / "tns.rpt",
        r"tns max\s+([-+]?\d*\.?\d+)"
    )


    hold_wns = extract_value(
        corner_dir / "hold_wns.rpt",
        r"wns min\s+([-+]?\d*\.?\d+)"
    )

    hold_tns = extract_value(
        corner_dir / "hold_tns.rpt",
        r"tns min\s+([-+]?\d*\.?\d+)"
    )

    rows.append({
        "PVT Corner": corner,
        "Process": process,
        "Temperature (C)": temperature,
        "Voltage (V)": voltage,
        "Setup Slack (ns)": setup_slack,
        "Overall Hold Slack (ns)": overall_hold,
        "Internal Hold Slack (ns)": internal_hold,
        "Setup WNS (ns)": setup_wns,
        "Setup TNS (ns)": setup_tns,
        "Hold WNS (ns)": hold_wns,
        "Hold TNS (ns)": hold_tns,
    })


if len(rows) != 16:
    raise RuntimeError(
        f"Expected 16 PVT corners, found {len(rows)}"
    )

with CSV_FILE.open("w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Successfully processed {len(rows)} PVT corners")
print(f"CSV generated: {CSV_FILE}")

print("\nPVT Timing Summary")
print("-" * 85)

for row in rows:
    print(
        f"{row['PVT Corner']:<18} "
        f"Setup: {row['Setup Slack (ns)']:>8.3f} ns  "
        f"Overall Hold: {row['Overall Hold Slack (ns)']:>8.3f} ns  "
        f"Internal Hold: {row['Internal Hold Slack (ns)']:>8.3f} ns"
    )

