import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from pathlib import Path

"""
Noise-seeded switching in a bistable one-dimensional potential.
Good README visual for robustness and threshold-triggered transitions.
"""

OUT = Path(__file__).resolve().parents[1] / "readme_assets" / "gif_noise_switching.gif"
OUT.parent.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(7)
N = 180
DT = 0.035
x = -1.2
xs = []
for i in range(N):
    drift = x - x**3 + 0.18*np.sin(i/30)
    noise = 0.20 * rng.normal()
    x += DT * drift + np.sqrt(DT) * noise
    xs.append(x)
xs = np.array(xs)
t = np.arange(N) * DT

fig, ax = plt.subplots(figsize=(7.2, 4.0), dpi=90)
ax.set_xlim(t.min(), t.max())
ax.set_ylim(-1.8, 1.8)
ax.set_xlabel("time")
ax.set_ylabel("state")
ax.set_title("CQT: Noise-seeded attractor switching")
ax.grid(True, alpha=0.25)
ax.axhline(-1, ls='--', alpha=0.4)
ax.axhline( 1, ls='--', alpha=0.4)
line, = ax.plot([], [], lw=2)
pt, = ax.plot([], [], 'o', ms=7)
text = ax.text(0.02, 0.95, "", transform=ax.transAxes, va='top')

def update(frame):
    i = frame + 1
    line.set_data(t[:i], xs[:i])
    pt.set_data([t[i-1]], [xs[i-1]])
    well = 'upper attractor' if xs[i-1] > 0 else 'lower attractor'
    text.set_text(well)
    return line, pt, text

ani = FuncAnimation(fig, update, frames=N-1, interval=25, blit=True)
ani.save(OUT, writer=PillowWriter(fps=12))
print(f"saved: {OUT}")
