import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from pathlib import Path

"""
Animated basin-of-attraction map for a symmetric double-well-like flow.
Parameter changes gently across frames to create a living basin structure.
"""

OUT = Path(__file__).resolve().parents[1] / "readme_assets" / "gif_basins.gif"
OUT.parent.mkdir(parents=True, exist_ok=True)

x = np.linspace(-2.2, 2.2, 180)
y = np.linspace(-2.0, 2.0, 160)
X, Y = np.meshgrid(x, y)

fig, ax = plt.subplots(figsize=(6.2, 5.2), dpi=120)
ax.set_xlabel(r"Re$(\alpha_0)$")
ax.set_ylabel(r"Im$(\alpha_0)$")
ax.set_title("CQT: Basin-of-attraction structure")
img = ax.imshow(np.zeros_like(X), extent=[x.min(), x.max(), y.min(), y.max()], origin='lower', aspect='auto')
text = ax.text(0.02, 0.97, "", transform=ax.transAxes, va='top', color='white')


def classify(mu):
    # proxy classifier creating evolving basin boundaries
    Z = np.tanh(1.7 * X - 0.9 * X**3 + mu * Y - 0.22 * Y**3 + 0.4*np.sin(1.2*X*Y))
    return (Z > 0).astype(float)

frames = np.linspace(-0.7, 0.7, 70)


def update(i):
    mu = frames[i]
    B = classify(mu)
    img.set_data(B)
    img.set_clim(0, 1)
    text.set_text(f"control slice = {mu:+.2f}")
    return img, text

ani = FuncAnimation(fig, update, frames=len(frames), interval=60, blit=True)
ani.save(OUT, writer=PillowWriter(fps=16))
print(f"saved: {OUT}")
