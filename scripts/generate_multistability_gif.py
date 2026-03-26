import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from pathlib import Path

"""
Creates a stylized hysteresis / multistability GIF for README usage.
This is intentionally repository-friendly: moderate size, clean axes, no custom fonts.
Replace the synthetic branches with your real CSV data if desired.
"""

OUT = Path(__file__).resolve().parents[1] / "readme_assets" / "gif_multistability.gif"
OUT.parent.mkdir(parents=True, exist_ok=True)

# Synthetic but CQT-style hysteresis branches
F = np.linspace(0.0, 1.0, 120)
upper = 1.05 + 0.35 * np.tanh(8 * (F - 0.35))
lower = 0.18 + 0.10 * np.tanh(8 * (F - 0.65)) + 0.08 * F

fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=90)
ax.set_xlim(0, 1.0)
ax.set_ylim(0, 1.7)
ax.set_xlabel("Drive parameter F*")
ax.set_ylabel(r"Stationary amplitude $|\alpha|$")
ax.set_title("CQT: Multistability / Hysteresis")
ax.grid(True, alpha=0.25)

ax.plot(F, upper, lw=2, alpha=0.35, label="upper branch")
ax.plot(F, lower, lw=2, alpha=0.35, label="lower branch")
point_up, = ax.plot([], [], 'o', ms=8)
point_dn, = ax.plot([], [], 'o', ms=8)
trace_up, = ax.plot([], [], '-', lw=2)
trace_dn, = ax.plot([], [], '-', lw=2)
text = ax.text(0.03, 0.95, "", transform=ax.transAxes, va='top')
ax.legend(loc="lower right")

n = len(F)

def update(frame):
    if frame < n:
        i = frame
        point_up.set_data([F[i]], [upper[i]])
        trace_up.set_data(F[:i+1], upper[:i+1])
        point_dn.set_data([], [])
        trace_dn.set_data([], [])
        text.set_text("up-sweep")
    else:
        i = frame - n
        Fr = F[::-1]
        lowr = lower[::-1]
        point_up.set_data([F[-1]], [upper[-1]])
        trace_up.set_data(F, upper)
        point_dn.set_data([Fr[i]], [lowr[i]])
        trace_dn.set_data(Fr[:i+1], lowr[:i+1])
        text.set_text("down-sweep")
    return point_up, point_dn, trace_up, trace_dn, text

ani = FuncAnimation(fig, update, frames=2*n, interval=40, blit=True)
ani.save(OUT, writer=PillowWriter(fps=12))
print(f"saved: {OUT}")
