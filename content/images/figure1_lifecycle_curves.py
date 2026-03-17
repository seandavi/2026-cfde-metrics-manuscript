"""
figure1_lifecycle_curves.py
----------------------------
Reproduces Figure 1 for:
  "Metrics that Drive Decisions: A Lifecycle Framework for Evaluating
   NIH Common Fund Data Ecosystem Investments"

Generates a line/area plot showing how the relative priority of each
evaluation framework shifts across the three lifecycle phases.

Requirements: numpy, matplotlib, scipy
  pip install numpy matplotlib scipy
  (or: uv add numpy matplotlib scipy)

Output: figure1_lifecycle_curves.png  (300 dpi, for submission)
        figure1_lifecycle_curves.pdf  (vector, for editing)

Run:
  python figure1_lifecycle_curves.py
"""

import matplotlib
matplotlib.use("Agg")  # non-interactive backend — no display required
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.interpolate import PchipInterpolator

# ---------------------------------------------------------------------------
# 1. Data — relative priority of each framework at each lifecycle phase
#    Scale: 0 (low) to 1 (high). Values reflect the paper's core argument.
# ---------------------------------------------------------------------------

# Phase positions on the x-axis (arbitrary units; labels override tick text)
phases = np.array([0.0, 1.0, 2.0])
phase_labels = ["Early\n(Infrastructure &\nCollection)",
                "Mid\n(Active Use\n& Impact)",
                "Late\n(Sustainability\n& Legacy)"]

# Relative priority per framework per phase
priorities = {
    "Public Value":               np.array([0.35, 0.90, 0.55]),
    "Scientific Data Quality":    np.array([0.85, 0.80, 0.50]),
    "Operations & Finance":       np.array([0.85, 0.50, 0.85]),
}

# Colors — consistent with the Excalidraw matrix diagram
colors = {
    "Public Value":            "#1971c2",   # blue
    "Scientific Data Quality": "#e8590c",   # orange
    "Operations & Finance":    "#2f9e44",   # green
}

fill_colors = {
    "Public Value":            "#a5d8ff",
    "Scientific Data Quality": "#ffd8a8",
    "Operations & Finance":    "#b2f2bb",
}

markers = {
    "Public Value":            "o",
    "Scientific Data Quality": "s",
    "Operations & Finance":    "^",
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

fig, ax = plt.subplots(figsize=(7, 4.5))

# Subtle phase background bands
ax.axvspan(-0.3,  0.5, color="#f8f9fa", zorder=0)
ax.axvspan( 0.5,  1.5, color="#ffffff", zorder=0)
ax.axvspan( 1.5,  2.3, color="#f8f9fa", zorder=0)

# Vertical phase dividers
for x in [0.5, 1.5]:
    ax.axvline(x, color="#dee2e6", linewidth=1.0, linestyle="--", zorder=1)

# Curves + filled areas
for name, y in interpolated.items():
    c = colors[name]
    fc = fill_colors[name]
    ax.fill_between(x_smooth, 0, y, color=fc, alpha=0.45, zorder=2)
    ax.plot(x_smooth, y, color=c, linewidth=2.5, zorder=3, label=name)
    # Anchor point markers
    ax.scatter(phases, priorities[name],
               color=c, marker=markers[name],
               s=70, zorder=4, edgecolors="white", linewidths=1.2)

# ---------------------------------------------------------------------------
# 4. Axes and labels
# ---------------------------------------------------------------------------

ax.set_xlim(-0.3, 2.3)
ax.set_ylim(-0.04, 1.08)

ax.set_xticks(phases)
ax.set_xticklabels(phase_labels, fontsize=10)
ax.set_yticks([0.0, 0.5, 1.0])
ax.set_yticklabels(["Low", "Medium", "High"], fontsize=9)

ax.set_ylabel("Relative Priority", fontsize=11, labelpad=10)
ax.set_xlabel("Lifecycle Phase", fontsize=11, labelpad=10)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#adb5bd")
ax.spines["bottom"].set_color("#adb5bd")
ax.tick_params(axis="both", colors="#495057")
ax.yaxis.label.set_color("#495057")
ax.xaxis.label.set_color("#495057")

# ---------------------------------------------------------------------------
# 5. Legend — placed inside the plot, top center
# ---------------------------------------------------------------------------

handles = [
    mpatches.Patch(facecolor=fill_colors[n], edgecolor=colors[n],
                   linewidth=1.5, label=n)
    for n in priorities
]
ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, 1.01),
          ncol=3, frameon=False, fontsize=9,
          handlelength=1.5, handleheight=1.0)

# ---------------------------------------------------------------------------
# 6. Figure caption note (as a figure text, not a title)
# ---------------------------------------------------------------------------

fig.text(0.5, -0.04,
         "Figure 1. Relative priority of each evaluation framework shifts across lifecycle phases.\n"
         "Anchor points (markers) represent expert judgment; curves are monotone cubic interpolations.",
         ha="center", va="top", fontsize=8, color="#6c757d",
         wrap=True)

plt.tight_layout()

# ---------------------------------------------------------------------------
# 7. Save
# ---------------------------------------------------------------------------

for ext in ("png", "pdf"):
    fname = f"figure1_lifecycle_curves.{ext}"
    fig.savefig(fname, dpi=300, bbox_inches="tight",
                facecolor="white", edgecolor="none")
    print(f"Saved: {fname}")

print("Done.")
