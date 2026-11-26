import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
from matplotlib.lines import Line2D

# ---------- Unsicherheitsannahmen (bei Bedarf anpassen) ----------
ABS_I = 0.05    # A,  halbe Anzeigeauflösung (0,1 A)
ABS_B = 0.05    # mT, halbe Anzeigeauflösung (0,1 mT)
REL_I = 0.03    # relative Geräteunsicherheit Strom (Annahme, bitte prüfen!)
REL_B = 0.03    # relative Geräteunsicherheit Flussdichte (Annahme, bitte prüfen!)

# ---------- Ausreißer ----------
# Automatische Erkennung: Abweichung vom Mittel der Nachbarpunkte in mT.
SCHWELLE = 150
# Alternativ manuell (0-basierte Zeilennummern der CSV), z. B. [23]. None = automatisch.
AUSREISSER_ZEILEN = None

VORZEICHEN_UMKEHREN = False   # True: B -> -B (Sondenorientierung)

# ---------- Daten ----------
df = pd.read_csv("experiment_3.csv").dropna(how="all").reset_index(drop=True)
I = df["I_A"].to_numpy(dtype=float)
B = df["B_mT"].to_numpy(dtype=float)
if VORZEICHEN_UMKEHREN:
    B = -B
n = len(I)

valid = np.ones(n, dtype=bool)
if AUSREISSER_ZEILEN is None:
    while True:                      # iterativ: jeweils der größte Ausreißer
        idx = np.where(valid)[0]
        if len(idx) < 3:
            break
        dev = np.zeros(n)
        for j in range(1, len(idx) - 1):
            k = idx[j]
            dev[k] = abs(B[k] - 0.5 * (B[idx[j - 1]] + B[idx[j + 1]]))
        k = dev.argmax()
        if dev[k] > SCHWELLE:
            valid[k] = False
        else:
            break
else:
    valid[list(AUSREISSER_ZEILEN)] = False

for k in np.where(~valid)[0]:
    print(f"Ausreißer: Zeile {k}, I = {I[k]} A, B = {B[k]} mT")

Iv, Bv = I[valid], B[valid]

# ---------- Unsicherheiten ----------
ux_k = np.sqrt((REL_I * np.abs(Iv))**2 + ABS_I**2)   # Körper (quadratisch)
uy_k = np.sqrt((REL_B * np.abs(Bv))**2 + ABS_B**2)
ux_w = REL_I * np.abs(Iv) + ABS_I                    # Docht (linear, Worst Case)
uy_w = REL_B * np.abs(Bv) + ABS_B

# ---------- Auswertung: Nulldurchgänge pro Ast ----------
def schnitt(a, b):
    """Werte von b, wo a (linear interpoliert) null wird."""
    res = []
    for k in range(len(a) - 1):
        if a[k] == 0:
            res.append(b[k])
        elif a[k] * a[k + 1] < 0:
            t = a[k] / (a[k] - a[k + 1])
            res.append(b[k] + t * (b[k + 1] - b[k]))
    return res

imin = int(np.argmin(Iv))                 # Umkehrpunkt (kleinster Strom)
aeste = {"Ast 1 (Strom sinkend)": (Iv[:imin + 1], Bv[:imin + 1]),
         "Ast 2 (Strom steigend)": (Iv[imin:], Bv[imin:])}
Br, Ic = [], []
for name, (i_a, b_a) in aeste.items():
    br, ic = schnitt(i_a, b_a), schnitt(b_a, i_a)
    print(f"{name}: B bei I=0: {np.round(br, 2)} mT | I bei B=0: {np.round(ic, 3)} A")
    if len(br) == 1 and len(ic) == 1:
        Br.append(br[0]); Ic.append(ic[0])
if len(Br) == 2:
    print(f"B(I=0): Offset (Mittel) = {np.mean(Br):.2f} mT, halbe Differenz = {abs(Br[0]-Br[1])/2:.2f} mT")
    print(f"I(B=0): Offset (Mittel) = {np.mean(Ic):.3f} A,  halbe Differenz = {abs(Ic[0]-Ic[1])/2:.3f} A")
else:
    print("Hinweis: nicht genau ein Nulldurchgang pro Ast -> Werte von Hand prüfen.")

# ---------- Plot ----------
farbe = "#1f77b4"
fig, ax = plt.subplots(figsize=(7.5, 5.5), dpi=150)

ax.errorbar(Iv, Bv, xerr=ux_w, yerr=uy_w, fmt="none", ecolor=farbe,
            elinewidth=0.8, capsize=2, zorder=2)
for x0, y0, dx, dy in zip(Iv, Bv, ux_k, uy_k):
    ax.add_patch(Rectangle((x0 - dx, y0 - dy), 2 * dx, 2 * dy,
                           facecolor=farbe, edgecolor=farbe, alpha=0.3, lw=0.8, zorder=3))
ax.plot(Iv, Bv, marker="o", markersize=3.5, lw=1.3, color=farbe, zorder=4)
ax.scatter(Iv[0], Bv[0], color="red", zorder=6)
if (~valid).any():
    ax.scatter(I[~valid], B[~valid], marker="x", s=60, color="red", zorder=6)

ax.axhline(0, color="black", lw=0.9, alpha=0.7)
ax.axvline(0, color="black", lw=0.9, alpha=0.7)
ax.set_title("Hystereseverlauf $B(I)$ des Eisenkerns (Querspaltsonde)")
ax.set_xlabel("Spulenstrom $I$ (A)")
ax.set_ylabel("Magnetische Flussdichte $B$ (mT)")
ax.grid(True, ls="--", alpha=0.4)

handles = [
    Line2D([], [], marker="o", color=farbe, ms=4, lw=1.3, label="Messwerte (chronologisch)"),
    Line2D([], [], marker="o", color="red", ls="", ms=6, label="Startpunkt"),
    Patch(facecolor=farbe, edgecolor=farbe, alpha=0.3, label="Körper: ±u (quadratische Summe)"),
    Line2D([], [], color=farbe, marker="|", ms=6, lw=0.8, label="Docht: ±u (lineare Summe)"),
]
if (~valid).any():
    handles.insert(2, Line2D([], [], marker="x", color="red", ls="", ms=7,
                             label="Ausreißer (nicht ausgewertet)"))
ax.legend(handles=handles, fontsize=8, loc="upper right")

fig.tight_layout()
plt.savefig("hysterese_b_h.png", dpi=300)
plt.show()
