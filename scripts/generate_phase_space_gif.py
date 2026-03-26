import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from pathlib import Path

"""
Stylized bistable phase-space animation based on a double-well flow.
Good proxy for README illustration of multiple attractors / basin convergence.
"""

OUT = Path(__file__).resolve().parents[1] / "readme_assets" / "gif_phase_space.gif"
OUT.parent.mkdir(parents=True, exist_ok=True)

# Double-well style dynamics with mild rotation
DT = 0.03
STEPS = 140
INIT = np.array([
    [-1.9,  1.2], [-1.7, -1.0], [-1.2, 1.5], [-0.6, -1.4],
    [ 0.5,  1.6], [ 1.5, -1.3], [ 1.9,  1.0], [ 0.9, -1.6],
])

traj = []
for x0, y0 in INIT:
    xs = [x0]; ys = [y0]
    x, y = x0, y0
    for _ in range(STEPS - 1):
        dx = x - x**3 - 0.35*y
        dy = -0.55*y + 0.25*x
        x += DT * dx
        y += DT * dy
        xs.append(x); ys.append(y)
    traj.append((np.array(xs), np.array(ys)))

fig, ax = plt.subplots(figsize=(5.8, 5.4), dpi=90)
ax.set_xlim(-2.3, 2.3)
ax.set_ylim(-2.0, 2.0)
ax.set_xlabel(r"Re$(\alpha)$")
ax.set_ylabel(r"Im$(\alpha)$")
ax.set_title("CQT: Phase-space attractor convergence")
ax.grid(True, alpha=0.25)
ax.plot([-1, 1], [0, 0], 'x', ms=10, mew=2, alpha=0.7)

lines = [ax.plot([], [], lw=1.8)[0] for _ in traj]
pts = [ax.plot([], [], 'o', ms=5)[0] for _ in traj]

def update(frame):
    for (xs, ys), line, pt in zip(traj, lines, pts):
        i = min(frame, len(xs)-1)
        line.set_data(xs[:i+1], ys[:i+1])
        pt.set_data([xs[i]], [ys[i]])
    return tuple(lines + pts)

ani = FuncAnimation(fig, update, frames=STEPS, interval=30, blit=True)
ani.save(OUT, writer=PillowWriter(fps=12))
print(f"saved: {OUT}")
