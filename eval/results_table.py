"""Results table + bar chart template (linear vs RAFT vs RIFE at 10/20/30 min gaps).

RIGHT NOW THE NUMBERS ARE FAKE. To use real numbers:
  1. Replace the values in RESULTS below (same layout), and
  2. Set USING_FAKE_DATA = False.

Run:  python eval/results_table.py            (prints table, saves PNG, shows chart)
      python eval/results_table.py --no-show  (prints table, saves PNG, no window)
"""

import os
import sys

import matplotlib.pyplot as plt
import numpy as np

# ----------------------------------------------------------------------------
# 1. SWAP IN REAL NUMBERS HERE
# ----------------------------------------------------------------------------
USING_FAKE_DATA = True

METHODS = ["Linear", "RAFT", "RIFE"]
GAPS = [10, 20, 30]  # minutes between the two input frames

# RESULTS[metric][method] = [value at 10 min, value at 20 min, value at 30 min]
RESULTS = {
    "MAE": {
        "Linear": [6.1, 9.8, 13.5],
        "RAFT":   [4.9, 7.6, 10.4],
        "RIFE":   [4.4, 6.9, 9.3],
    },
    "RMSE": {
        "Linear": [8.5, 13.2, 17.9],
        "RAFT":   [7.0, 10.6, 14.1],
        "RIFE":   [6.4, 9.7, 12.8],
    },
    "PSNR": {
        "Linear": [30.2, 26.4, 23.6],
        "RAFT":   [32.1, 28.7, 25.9],
        "RIFE":   [33.0, 29.8, 27.0],
    },
    "SSIM": {
        "Linear": [0.82, 0.71, 0.60],
        "RAFT":   [0.87, 0.78, 0.69],
        "RIFE":   [0.89, 0.81, 0.73],
    },
}

# Lower is better for these, higher is better for the rest.
LOWER_IS_BETTER = {"MAE", "RMSE"}
UNITS = {"PSNR": " dB"}
DECIMALS = {"MAE": 2, "RMSE": 2, "PSNR": 2, "SSIM": 3}

OUT_PNG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results_chart.png")

# ----------------------------------------------------------------------------
# 2. TABLE
# ----------------------------------------------------------------------------


def print_table():
    metrics = list(RESULTS)
    tag = "  (FAKE DATA)" if USING_FAKE_DATA else ""
    print(f"\nResults by method and gap{tag}")

    header = f"{'Method':<8}{'Gap':>8}" + "".join(f"{m:>10}" for m in metrics)
    line = "-" * len(header)
    print(line)
    print(header)
    print(line)
    for method in METHODS:
        for gi, gap in enumerate(GAPS):
            row = f"{method:<8}{str(gap) + ' min':>8}"
            for m in metrics:
                row += f"{RESULTS[m][method][gi]:>10.{DECIMALS.get(m, 2)}f}"
            print(row)
        print(line)

    print("Lower is better: " + ", ".join(sorted(LOWER_IS_BETTER)))
    print("Higher is better: " + ", ".join(m for m in metrics if m not in LOWER_IS_BETTER))

    print("\nBest method per metric and gap:")
    for m in metrics:
        picks = []
        for gi, gap in enumerate(GAPS):
            vals = {meth: RESULTS[m][meth][gi] for meth in METHODS}
            best = (min if m in LOWER_IS_BETTER else max)(vals, key=vals.get)
            picks.append(f"{gap} min: {best}")
        print(f"  {m:<5} " + " | ".join(picks))


# ----------------------------------------------------------------------------
# 3. CHART (one panel per metric, bars grouped by gap)
# ----------------------------------------------------------------------------
COLORS = {"Linear": "#9aa0a6", "RAFT": "#4c8bf5", "RIFE": "#e8710a"}


def draw_chart(show=True):
    metrics = list(RESULTS)
    ncols = 2
    nrows = int(np.ceil(len(metrics) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(11, 4.2 * nrows))
    axes = np.atleast_1d(axes).ravel()

    x = np.arange(len(GAPS))
    width = 0.26
    for ax, m in zip(axes, metrics):
        for i, method in enumerate(METHODS):
            vals = RESULTS[m][method]
            bars = ax.bar(
                x + (i - 1) * width, vals, width, label=method, color=COLORS[method]
            )
            ax.bar_label(bars, fmt=f"%.{DECIMALS.get(m, 2)}f", fontsize=7, padding=2)
        arrow = "lower is better" if m in LOWER_IS_BETTER else "higher is better"
        ax.set_title(f"{m} ({arrow})")
        ax.set_xticks(x)
        ax.set_xticklabels([f"{g} min" for g in GAPS])
        ax.set_xlabel("Gap between input frames")
        ax.set_ylabel(m + UNITS.get(m, ""))
        ax.margins(y=0.15)
        ax.spines[["top", "right"]].set_visible(False)
    for ax in axes[len(metrics):]:
        ax.axis("off")

    axes[0].legend(frameon=False)
    title = "Frame interpolation: Linear vs RAFT vs RIFE"
    if USING_FAKE_DATA:
        title += "  [FAKE DATA - placeholder numbers]"
    fig.suptitle(title, fontsize=13, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(OUT_PNG, dpi=150)
    print(f"\nChart saved to: {OUT_PNG}")
    if show:
        plt.show()


if __name__ == "__main__":
    print_table()
    draw_chart(show="--no-show" not in sys.argv)