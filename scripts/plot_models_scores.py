#!/usr/bin/env python3
"""Scan `models/` for `scores_log.txt`, compute rolling averages, and plot them.

Usage:
    python scripts/plot_models_scores.py --models-dir models --window 100 --output scores_plot.png

The script recursively finds `scores_log.txt` files under the given models directory,
parses numeric values from each line, computes a rolling average (window size default 100),
and produces a combined plot saved to `scores_plot.png` (or shown interactively with `--show`).
"""
from pathlib import Path
import argparse
import re
import numpy as np
import matplotlib.pyplot as plt
import sys

NUM_RE = re.compile(r"[-+]?(?:\d*\.\d+|\d+)")


def parse_scores_from_file(path: Path):
    """Return a list of floats parsed from the file's lines."""
    values = []
    try:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                m = NUM_RE.findall(line)
                if not m:
                    continue
                # prefer the first numeric token on the line
                try:
                    values.append(float(m[0]))
                except ValueError:
                    continue
    except Exception:
        return []
    return values


def rolling_average(arr, window):
    arr = np.asarray(arr, dtype=float)
    n = arr.size
    if n == 0:
        return np.array([]), np.array([])
    if n < window:
        # return cumulative average if not enough points
        avg = np.cumsum(arr) / np.arange(1, n + 1)
        xs = np.arange(n)
        return xs, avg
    # moving average (center-right aligned): avg at positions window-1..n-1
    kernel = np.ones(window, dtype=float) / window
    avg = np.convolve(arr, kernel, mode="valid")
    xs = np.arange(window - 1, n)
    return xs, avg


def find_scores_files(models_dir: Path, pattern: str = "scores_log.txt"):
    return sorted(models_dir.rglob(pattern))


def _parse_index_list(s: str, count: int):
    """Parse a user input string like '1,3-5' into a list of zero-based indices.
    Invalid entries are ignored. Indices out of range are clipped.
    """
    s = s.strip()
    if not s:
        return list(range(count))
    parts = [p.strip() for p in s.split(",") if p.strip()]
    inds = set()
    for p in parts:
        if "-" in p:
            try:
                a, b = p.split("-", 1)
                a = int(a) - 1
                b = int(b) - 1
                if a > b:
                    a, b = b, a
                for i in range(max(0, a), min(count - 1, b) + 1):
                    inds.add(i)
            except Exception:
                continue
        else:
            try:
                i = int(p) - 1
                if 0 <= i < count:
                    inds.add(i)
            except Exception:
                continue
    return sorted(inds)


def interactive_choose_series(labels):
    """Present a simple console UI to choose which labels to include.

    Returns a list of selected indices (zero-based). Default (empty input) selects all.
    """
    count = len(labels)
    print("Found the following series:")
    for idx, lab in enumerate(labels, start=1):
        print(f"  {idx:3d}: {lab}")
    print("")
    prompt = (
        "Enter indices to include (e.g. 1,3-5). Leave empty to include all, 'q' to quit: "
    )
    while True:
        ans = input(prompt).strip()
        if ans.lower() in ("q", "quit", "exit"):
            return []
        inds = _parse_index_list(ans, count)
        if inds:
            print(f"Selected {len(inds)} series.")
            return inds
        # if user pressed Enter (ans == ''), _parse_index_list returns all indices
        if ans == "":
            return list(range(count))
        print("No valid selection detected — try again or press Enter to select all.")


def plot_series(series, output, show=False, figsize=(12, 8)):
    fig, ax = plt.subplots(figsize=figsize)
    for label, (xs, ys) in series.items():
        if ys.size == 0:
            continue
        ax.plot(xs, ys, label=label)
    ax.set_xlabel("Episode index")
    ax.set_ylabel("Score (rolling average)")
    ax.legend(loc="best", fontsize="small")
    plt.tight_layout()
    fig.savefig(output)
    print(f"Saved plot to: {output}")
    if show:
        plt.show()


def main():
    p = argparse.ArgumentParser(description="Plot rolling averages from models' scores_log.txt files")
    p.add_argument("--models-dir", default="models", help="Top-level models directory to scan")
    p.add_argument("--pattern", default="scores_log.txt", help="Filename pattern to search for (glob)")
    p.add_argument("--window", type=int, default=100, help="Rolling average window size")
    p.add_argument("--output", default="scores_plot.png", help="Output image path")
    p.add_argument("--show", action="store_true", help="Show plot interactively")
    args = p.parse_args()

    models_dir = Path(args.models_dir)
    if not models_dir.exists():
        print(f"Models directory not found: {models_dir}", file=sys.stderr)
        sys.exit(2)

    files = find_scores_files(models_dir, args.pattern)
    if not files:
        print(f"No files matching '{args.pattern}' found under {models_dir}")
        sys.exit(0)

    # build list of candidate series (labels + file path) without parsing content yet
    candidates = []
    for f in files:
        try:
            label = str(f.parent.relative_to(models_dir))
        except Exception:
            label = f.parent.as_posix()
        candidates.append((label, f))

    # interactive selection before heavy parsing/computation
    selected_indices = interactive_choose_series([c[0] for c in candidates])
    if not selected_indices:
        print("No series selected; exiting.")
        sys.exit(0)

    series = {}
    for idx in selected_indices:
        label, f = candidates[idx]
        scores = parse_scores_from_file(f)
        if not scores:
            print(f"Warning: no numeric scores parsed from {f}")
            continue
        xs, ys = rolling_average(scores, args.window)
        series[label] = (xs, ys)

    if not series:
        print("No numeric scores parsed from found files.")
        sys.exit(0)

    plot_series(series, args.output, show=args.show)


if __name__ == "__main__":
    main()
