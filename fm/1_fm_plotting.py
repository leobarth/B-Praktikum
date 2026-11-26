import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle

# ---------- Unsicherheitsannahmen (bei Bedarf anpassen) ----------
REL_GERAET   = 0.03   # 3 % Geräteunsicherheit (Netzgerät, Hallsonde, Stromanzeige)
ABS_ABLESUNG = 0.5    # mT, halbe Anzeigeauflösung (ganzzahlige Anzeige)
DX           = 0.05   # cm, Positionsunsicherheit auf der Schiene
BOX_BREITE   = 0.30   # cm, nur Darstellung (hat nichts mit DX zu tun)
THEORIE      = True   # Theoriekurve der endlichen Spule einzeichnen

# Spulenparameter für die Theoriekurve
MU0 = 4 * np.pi * 1e-7
N, I, R, L = 500, 2.5, 0.0275, 0.072   # L = 0.080 für Aufgabe 14

# ---------- Daten ----------
df = pd.read_csv("experiment_1.csv")
x = df.iloc[:, 0].to_numpy(dtype=float)
y = df.iloc[:, 1].to_numpy(dtype=float)
order = np.argsort(x)
x, y = x[order], y[order]

# ---------- Unsicherheit in B ----------
u_rel = REL_GERAET * np.abs(y)                    # relativer Geräteanteil
u_abs = np.full_like(y, ABS_ABLESUNG)             # Ablesung/Auflösung
u_pos = np.abs(np.gradient(y, x)) * DX            # Positionsfehler über die Steigung
u_box  = np.sqrt(u_rel**2 + u_abs**2 + u_pos**2)  # Körper: quadratische Summe
u_wick = u_rel + u_abs + u_pos                    # Docht: lineare Summe (Worst Case)

# ---------- Plot ----------
y_label = "Magnetische Flussdichte B (mT)"
title = "Experiment 1: B-Feld der Luftspule (longitudinale Hallsonde)"
farbe = "#1f77b4"

fig, ax = plt.subplots(figsize=(8, 5), dpi=150)

# Docht (Worst Case)
ax.errorbar(x, y, yerr=u_wick, fmt="none", ecolor=farbe,
            elinewidth=1, capsize=2, zorder=2)
# Körper (quadratische Summe)
for xi, yi, ui in zip(x, y, u_box):
    ax.add_patch(Rectangle((xi - BOX_BREITE / 2, yi - ui), BOX_BREITE, 2 * ui,
                           facecolor=farbe, edgecolor=farbe,
                           alpha=0.35, lw=1, zorder=3))
# Messdaten
ax.plot(x, y, marker="o", markersize=4, linewidth=1.5, color=farbe, zorder=4)

# Theorie (endliche Zylinderspule, Gl. 2.14), z in cm, B in mT
if THEORIE:
    z = np.linspace(x.min(), x.max(), 600)
    zp, zm = z / 100 + L / 2, z / 100 - L / 2
    H = N * I / (2 * L) * (zp / np.sqrt(R**2 + zp**2) - zm / np.sqrt(R**2 + zm**2))
    ax.plot(z, MU0 * H * 1e3, "k--", lw=1.2, zorder=1)

handles = [
    Line2D([], [], marker="o", color=farbe, markersize=4, lw=1.5, label="Messdaten"),
    Patch(facecolor=farbe, edgecolor=farbe, alpha=0.35,
          label="Körper: ±u (quadratische Summe)"),
    Line2D([], [], color=farbe, marker="_", markersize=6, lw=1,
           label="Docht: ±u (lineare Summe, Worst Case)"),
]
if THEORIE:
    handles.append(Line2D([], [], color="k", ls="--", lw=1.2,
                          label=f"Theorie (endliche Spule, l = {L*100:.1f} cm)"))

ax.set_title(title)
ax.set_xlabel("Abstand vom Spulenmittelpunkt (cm)")
ax.set_ylabel(y_label)
ax.set_ylim(top=1.35 * (y + u_wick).max())   # Platz für die Legende
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend(handles=handles, loc="upper right", fontsize=8)

fig.tight_layout()
plt.savefig("experiment_1_plot.png", dpi=300)
plt.show()
