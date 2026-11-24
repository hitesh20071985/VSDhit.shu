#!/usr/bin/env python3

import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

WORK_DIR = Path.home() / "VSDBabySoC/work/week4_opensta"

CSV_FILE = WORK_DIR / "csv/babysoc_pvt_timing_summary.csv"
GRAPH_DIR = WORK_DIR / "graphs/lines"

GRAPH_DIR.mkdir(parents=True, exist_ok=True)

if not CSV_FILE.is_file():
    raise FileNotFoundError(f"CSV file not found: {CSV_FILE}")

with CSV_FILE.open(newline="") as f:
    rows = list(csv.DictReader(f))

if len(rows) != 16:
    raise RuntimeError(
        f"Expected 16 PVT corners, found {len(rows)}"
    )

corners = [row["PVT Corner"] for row in rows]

graphs = [
    (
        "Setup Slack (ns)",
        "BabySoC - Setup Slack Across PVT Corners",
        "setup_slack.png"
    ),
    (
        "Overall Hold Slack (ns)",
        "BabySoC - Overall Hold Slack Across PVT Corners",
        "overall_hold_slack.png"
    ),
    (
        "Internal Hold Slack (ns)",
        "BabySoC - Internal Register-to-Register Hold Slack",
        "internal_hold_slack.png"
    ),
    (
        "Setup WNS (ns)",
        "BabySoC - Setup WNS Across PVT Corners",
        "setup_wns.png"
    ),
    (
        "Setup TNS (ns)",
        "BabySoC - Setup TNS Across PVT Corners",
        "setup_tns.png"
    )
]


graphs.extend([
    (
        "Hold WNS (ns)",
        "BabySoC - Hold WNS Across PVT Corners",
        "hold_wns.png"
    ),
    (
        "Hold TNS (ns)",
        "BabySoC - Hold TNS Across PVT Corners",
        "hold_tns.png"
    )
])

for column, title, filename in graphs:

    values = [float(row[column]) for row in rows]

    fig, ax = plt.subplots(figsize=(15, 7))


    x = list(range(len(corners)))

    # Line graph with markers at each PVT corner
    ax.plot(
        x,
        values,
        color="blue",
        linestyle="-",
        linewidth=2,
        marker="o",
        markersize=6,
        label=column
    )

    # Zero-slack reference
    ax.axhline(
        y=0,
        color="red",
        linestyle="--",
        linewidth=1.2,
        label="Zero Slack"
    )

    ax.set_xticks(x)
    ax.set_xticklabels(
        corners,
        rotation=55,
        ha="right"
    )

    ax.set_xlabel("SKY130 PVT Corner")
    ax.set_ylabel(column)
    ax.set_title(title)

    ax.grid(
        True,
        linestyle="--",
        alpha=0.4
    )

    ax.set_axisbelow(True)

    # Annotate timing values
    for xi, value in zip(x, values):
        ax.annotate(
            f"{value:.2f}",
            xy=(xi, value),
            xytext=(0, 8 if value >= 0 else -12),
            textcoords="offset points",
            ha="center",
            va="bottom" if value >= 0 else "top",
            fontsize=8
        )

    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0))

    ax.margins(y=0.15)

    fig.tight_layout()

    output_file = GRAPH_DIR / filename

    fig.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)

    print(f"Generated: {output_file}")

print("\nAll seven PVT timing line graphs generated successfully.")
