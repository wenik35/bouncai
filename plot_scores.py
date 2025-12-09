"""Plot scores from scores_log.txt as a line graph."""

import matplotlib.pyplot as plt
import numpy as np

# Read the scores from file
scores = []
try:
    with open("scores_log.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    score = float(line)
                    scores.append(score)
                except ValueError:
                    # Skip lines that aren't valid numbers
                    pass
except FileNotFoundError:
    print("Error: scores_log.txt not found!")
    exit(1)

if not scores:
    print("No scores found in scores_log.txt")
    exit(1)

print(f"Loaded {len(scores)} scores")
print(f"Min score: {min(scores):.1f}")
print(f"Max score: {max(scores):.1f}")
print(f"Average score: {np.mean(scores):.1f}")

# Create figure and plot
fig, ax = plt.subplots(figsize=(14, 6))

# Plot the scores line
ax.plot(scores, linewidth=1.5, alpha=0.8, color='steelblue')

# Add a rolling average (window of 10 episodes)
if len(scores) >= 10:
    window = 10
    rolling_avg = np.convolve(scores, np.ones(window)/window, mode='valid')
    ax.plot(range(window-1, len(scores)), rolling_avg, linewidth=2, 
            alpha=0.7, color='red', label=f'Rolling avg (window={window})')

# Labels and formatting
ax.set_xlabel('Episode Number', fontsize=12)
ax.set_ylabel('Score', fontsize=12)
ax.set_title('Agent Score over Episodes', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend(fontsize=10)

# Add some statistics to the plot
stats_text = f"Total episodes: {len(scores)}\nMin: {min(scores):.1f}\nMax: {max(scores):.1f}\nAvg: {np.mean(scores):.1f}"
ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
        fontsize=10, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig("scores_plot.png", dpi=150, bbox_inches='tight')
print(f"Plot saved to scores_plot.png")
plt.show()
