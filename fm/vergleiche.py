import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle

# ---------- Unsicherheitsannahmen (wie in den bisherigen Plots) ----------
REL_GERAET   = 0.03   # 3 % Geräteunsicherheit
ABS_ABLESUNG = 0.5    # mT
DX           = 0.05   # cm Positionsunsicherheit
BOX_BREITE   = 0.30   # cm, nur Darstellung

# ---------- Spulenparameter und Dipol-Normierung ----------
MU0 = 4 * np.pi * 1e-7
N, I, R, L = 500, 2.5, 0.0275, 0.072
Z_NORM = 10.0         # cm, Dipol wird hier auf die endliche Spule normiert
Z_MIN_DIPOL = 3.0     # cm, Dipolkurve nur für |z| >= Z_MIN_DIPOL zeichnen

def B_endlich(z_cm):
    """Endliche Zylinderspule (Gl. 2.14), z in cm, Rückgabe B in mT."""
    z = np.asarray(z_cm, dtype=float) / 100
    zp, zm = z + L / 2, z - L / 2
    H = N * I / (2 * L) * (zp / np.sqrt(R**2 + zp**2) - zm / np.sqrt(R**2 + zm**2))
    return MU0 * H * 1e3

B_norm = float(B_endlich(Z_NORM))
def B_dipol(z_cm):
    """Punktdipol-Näherung ~|z|^-3, bei Z_NORM auf die endliche Spule normiert."""
    return B_norm * (Z_NORM / np.abs(np.asarray(z_cm, dtype=float)))**3

# ---------- Daten ----------
def lade(datei):
    df = pd.read_csv(datei).dropna(how="all")
    x = df.iloc[:, 0].to_numpy(dtype=float)
    y = df.iloc[:, 1].to_numpy(dtype=float)
    o = np.argsort(x)
    return x[o], y[o]

x1, y1 = lade("experiment_1.csv")   # Luftspule
x2, y2 = lade("experiment_2.csv")   # Eisenkern

def unsicherheit(x, y):
    u_rel = REL_GERAET * np.abs(y)
    u_abs = np.full_like(y, ABS_ABLESUNG)
    u_pos = np.abs(np.gradient(y, x)) * DX
    return np.sqrt(u_rel**2 + u_abs**2 + u_pos**2), u_rel + u_abs + u_pos

def kerzen(ax, x, y, farbe, zorder=3):
    u_box, u_wick = unsicherheit(x, y)
    ax.errorbar(x, y, yerr=u_wick, fmt="none", ecolor=farbe,
                elinewidth=1, capsize=2, zorder=zorder)
    for xi, yi, ui in zip(x, y, u_box):
        ax.add_patch(Rectangle((xi - BOX_BREITE / 2, yi - ui), BOX_BREITE, 2 * ui,
                               facecolor=farbe, edgecolor=farbe,
                               alpha=0.35, lw=1, zorder=zorder + 1))
    ax.plot(x, y, marker="o", markersize=4, lw=1.5, color=farbe, zorder=zorder + 2)

C_LUFT, C_EISEN = "#1f77b4", "#ff7f0e"
h_kerze_box = Patch(facecolor="grey", edgecolor="grey", alpha=0.35,
                    label="Körper: ±u (quadr. Summe)")
h_kerze_wick = Line2D([], [], color="grey", marker="_", markersize=6, lw=1,
                      label="Docht: ±u (lineare Summe)")
z_fein = np.linspace(-10.7, 10.7, 800)

# ================= Abbildung A: Luftspule, Theorie, Dipol =================
figA, axA = plt.subplots(figsize=(8, 5), dpi=150)
kerzen(axA, x1, y1, C_LUFT)
axA.plot(z_fein, B_endlich(z_fein), "k--", lw=1.3, zorder=1)
for vorz in (-1, 1):
    zz = np.linspace(Z_MIN_DIPOL, 10.7, 300) * vorz
    axA.plot(zz, B_dipol(zz), color="tab:red", ls=":", lw=1.8, zorder=1)
axA.axvline(0, color="grey", lw=0.6)
axA.set_xlim(-11, 11)
axA.set_ylim(-1, 22)
axA.set_title("Luftspule: Messung, endliche Spule und Punktdipol")
axA.set_xlabel("Abstand vom Spulenmittelpunkt (cm)")
axA.set_ylabel("Magnetische Flussdichte B (mT)")
axA.grid(True, ls="--", alpha=0.5)
axA.legend(handles=[
    Line2D([], [], marker="o", color=C_LUFT, ms=4, lw=1.5, label="Messdaten (Luftspule)"),
    h_kerze_box, h_kerze_wick,
    Line2D([], [], color="k", ls="--", lw=1.3,
           label=f"Theorie endliche Spule (l = {L*100:.1f} cm)"),
    Line2D([], [], color="tab:red", ls=":", lw=1.8,
           label=f"Punktdipol ∝ |z|⁻³ (normiert bei |z| = {Z_NORM:g} cm)"),
], loc="upper right", fontsize=8)
figA.tight_layout()
figA.savefig("vergleich_luftspule.png", dpi=300)

# ================= Abbildung B: Luftspule + Eisenkern =================
figB, axB = plt.subplots(figsize=(8, 5), dpi=150)
kerzen(axB, x1, y1, C_LUFT, zorder=2)
kerzen(axB, x2, y2, C_EISEN, zorder=5)
axB.plot(z_fein, B_endlich(z_fein), "k--", lw=1.3, zorder=1)
axB.axvline(0, color="grey", lw=0.6)
axB.set_xlim(-11, 11)
axB.set_ylim(-1, 34)
axB.set_title("Spule ohne und mit Eisenkern (longitudinale Hallsonde)")
axB.set_xlabel("Abstand vom Spulenmittelpunkt (cm)")
axB.set_ylabel("Magnetische Flussdichte B (mT)")
axB.grid(True, ls="--", alpha=0.5)
axB.legend(handles=[
    Line2D([], [], marker="o", color=C_LUFT, ms=4, lw=1.5, label="Luftspule"),
    Line2D([], [], marker="o", color=C_EISEN, ms=4, lw=1.5, label="Spule mit Eisenkern"),
    h_kerze_box, h_kerze_wick,
    Line2D([], [], color="k", ls="--", lw=1.3,
           label=f"Theorie endliche Spule (l = {L*100:.1f} cm)"),
], loc="upper right", fontsize=8)
figB.tight_layout()
figB.savefig("vergleich_luft_eisen.png", dpi=300)

# ---------- Kontrollwerte für den Text ----------
print(f"B_endlich(0) = {B_endlich(0.0):.2f} mT")
print(f"Normierungswert B_endlich({Z_NORM:g} cm) = {B_norm:.3f} mT")
mu_dip = MU0 * N * I * R**2 / 2 * 1e3   # mT*m^3 -> B = mu_dip/|z|^3 mit z in m
print(f"Dipol mit echtem Moment m = nIπR²: B({Z_NORM:g} cm) = "
      f"{mu_dip / (Z_NORM/100)**3:.3f} mT (Faktor {mu_dip/(Z_NORM/100)**3/B_norm:.2f} zur Normierung)")
for z in (3, 4, 5, 7, 10):
    print(f"|z| = {z:>2} cm: endliche Spule {float(B_endlich(z)):6.2f} mT, "
          f"Dipol {float(B_dipol(z)):6.2f} mT, Verhältnis {float(B_dipol(z)/B_endlich(z)):.2f}")
plt.show()
