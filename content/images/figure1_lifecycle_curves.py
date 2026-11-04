"""
figure1_lifecycle_curves.py
----------------------------
Reproduces Figure 1 for:
  "Metrics that Drive Decisions: A Lifecycle Framework for Evaluating
   NIH Common Fund Data Ecosystem Investments"

Generates a line/area plot showing how the relative priority of each
evaluation domain shifts across the three lifecycle phases.

Requirements: numpy, matplotlib, scipy
  pip install numpy matplotlib scipy
  (or: uv add numpy matplotlib scipy)

Output: figure1_lifecycle_curves.png  (600 dpi raster)
        figure1_lifecycle_curves.pdf  (vector, for submission)

Both are drawn at Trends Open's print size: 12.7 cm (5 in) wide, the maximum
for a figure with its legend below. No text is smaller than 7 pt at that size.

Run:
  python figure1_lifecycle_curves.py
"""

import matplotlib
matplotlib.use("Agg")  # non-interactive backend — no display required
matplotlib.rcParams["pdf.fonttype"] = 42  # embed TrueType so PDF text stays editable
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.interpolate import PchipInterpolator

# ---------------------------------------------------------------------------
# 1. Data — relative priority of each domain at each lifecycle phase
#    Scale: 0 (low) to 1 (high). Values reflect the paper's core argument.
# ---------------------------------------------------------------------------

# Phase positions on the x-axis (arbitrary units; labels override tick text)
phases = np.array([0.0, 1.0, 2.0])
phase_labels = ["Early\n(Infrastructure &\nCollection)",
                "Mid\n(Active Use\n& Impact)",
                "Late\n(Sustainability\n& Legacy)"]

# Relative priority per domain per phase
priorities = {
    "Public value":                 np.array([0.35, 0.90, 0.55]),
    "Data quality and reusability": np.array([0.85, 0.80, 0.50]),
    "Operations and finance":       np.array([0.85, 0.50, 0.85]),
}

# Colors — Okabe-Ito, safe for colour-vision deficiency (no red/green pair).
# Line style and marker also differ per domain, so the curves stay
# distinguishable in greyscale print.
colors = {
    "Public value":                 "#0072B2",   # blue
    "Data quality and reusability": "#E69F00",   # orange
    "Operations and finance":       "#CC79A7",   # reddish purple
}

linestyles = {
    "Public value":                 "solid",
    "Data quality and reusability": (0, (5, 2)),       # dashed
    "Operations and finance":       (0, (1.2, 1.5)),   # dotted
}

markers = {
    "Public value":                 "o",
    "Data quality and reusability": "s",
    "Operations and finance":       "^",
}

# ---------------------------------------------------------------------------
# 2. Interpolate smooth curves between the three phase anchor points
# ---------------------------------------------------------------------------

x_smooth = np.linspace(0, 2, 300)

interpolated = {}
for name, values in priorities.items():
    interp = PchipInterpolator(phases, values)
    y = interp(x_smooth)
    # Clamp to [0, 1] — PchipInterpolator can occasionally overshoot slightly
    y = np.clip(y, 0.0, 1.0)
    interpolated[name] = y

# ---------------------------------------------------------------------------
# 3. Plot
# ---------------------------------------------------------------------------

FIGURE_WIDTH_CM = 12.7   # Trends Open maximum width, legend below the figure
FIGURE_HEIGHT_CM = 8.2
CM_PER_INCH = 2.54

FONT_PT = 7.5           # tick labels and legend; keep >= 7 pt at print size
AXIS_LABEL_PT = 8.5

fig, ax = plt.subplots(
    figsize=(FIGURE_WIDTH_CM / CM_PER_INCH, FIGURE_HEIGHT_CM / CM_PER_INCH),
    layout="constrained",
)

# Subtle phase background bands
ax.axvspan(-0.3,  0.5, color="#f8f9fa", zorder=0)
ax.axvspan( 0.5,  1.5, color="#ffffff", zorder=0)
ax.axvspan( 1.5,  2.3, color="#f8f9fa", zorder=0)

# Vertical phase dividers
for x in [0.5, 1.5]:
    ax.axvline(x, color="#dee2e6", linewidth=0.75, linestyle="--", zorder=1)

# Curves + filled areas
for name, y in interpolated.items():
    c = colors[name]
    ax.fill_between(x_smooth, 0, y, color=c, alpha=0.12, linewidth=0, zorder=2)
    ax.plot(x_smooth, y, color=c, linestyle=linestyles[name],
            linewidth=1.75, zorder=3, label=name)
    # Anchor point markers
    ax.scatter(phases, priorities[name],
               color=c, marker=markers[name],
               s=30, zorder=4, edgecolors="white", linewidths=0.8)

# ---------------------------------------------------------------------------
# 4. Axes and labels
# ---------------------------------------------------------------------------

ax.set_xlim(-0.3, 2.3)
ax.set_ylim(-0.04, 1.04)

ax.set_xticks(phases)
ax.set_xticklabels(phase_labels, fontsize=FONT_PT)
ax.set_yticks([0.0, 0.5, 1.0])
ax.set_yticklabels(["Low", "Medium", "High"], fontsize=FONT_PT)

ax.set_ylabel("Relative Priority", fontsize=AXIS_LABEL_PT, labelpad=6)
ax.set_xlabel("Lifecycle Phase", fontsize=AXIS_LABEL_PT, labelpad=6)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#adb5bd")
ax.spines["bottom"].set_color("#adb5bd")
ax.tick_params(axis="both", colors="#495057")
ax.yaxis.label.set_color("#495057")
ax.xaxis.label.set_color("#495057")

# ---------------------------------------------------------------------------
# 5. Legend — above the plot, top center
# ---------------------------------------------------------------------------

# Line + marker handles, so the legend keys match the curves in greyscale too
handles = [
    Line2D([], [], color=colors[n], linestyle=linestyles[n], linewidth=1.75,
           marker=markers[n], markersize=5, markeredgecolor="white",
           markeredgewidth=0.6, label=n)
    for n in priorities
]
fig.legend(handles=handles, loc="outside upper center",
           ncol=3, frameon=False, fontsize=FONT_PT,
           handlelength=2.4, columnspacing=1.2)

# ---------------------------------------------------------------------------
# 6. Save
# ---------------------------------------------------------------------------

# No bbox_inches="tight": it would change the canvas away from the print width.
for ext in ("png", "pdf"):
    fname = f"figure1_lifecycle_curves.{ext}"
    fig.savefig(fname, dpi=600, facecolor="white", edgecolor="none",
                metadata={"CreationDate": None} if ext == "pdf" else None)
    print(f"Saved: {fname}")

print("Done.")
