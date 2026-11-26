import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. CSV auslesen
# Falls deine Datei Semikolons und Kommazahlen hat, nutze z.B.:
# df = pd.read_csv("hysterese.csv", sep=";", decimal=",")
df = pd.read_csv("experiment_3.csv")

# Leere Zeilen oder reine NaN-Zeilen entfernen, falls beim Tippen welche entstehen
df = df.dropna(how="all").reset_index(drop=True)

I = df["I_A"].to_numpy()
B = df["B_mT"].to_numpy()
H = df["H_Am"].to_numpy() if "H_Am" in df.columns else np.zeros_like(B)

# 2. Prüfen, ob H brauchbare Werte enthält, sonst B(I) als Fallback plotten
if np.allclose(H, 0):
  print("Hinweis: H ist überall ~0 -> plotte stattdessen B(I).")
  x = I
  x_label = "Spulenstrom I (A)"
  title = "Hystereseverlauf B(I) (Fallback, da H = 0)"
else:
  x = H
  x_label = "Magnetische Feldstärke H (A/m)"
  title = "Hysteresekurve B(H) des Eisenkerns"

# 3. Plotten in exakter Messreihenfolge (nicht sortieren!)
fig, ax = plt.subplots(figsize=(7.5, 5.5), dpi=150)

ax.plot(
    x,
    B,
    marker="o",
    markersize=4,
    linewidth=1.5,
    color="#1f77b4",
    label="Messwerte (chronologisch)",
)

# Startpunkt markieren (hilft beim Nachvollziehen der Sättigung -> Schleife)
ax.scatter(
    x[0], B[0], color="red", zorder=5, label="Startpunkt (Sättigung)"
)

# Nullachsen einzeichnen
ax.axhline(0, color="black", linewidth=0.9, alpha=0.7)
ax.axvline(0, color="black", linewidth=0.9, alpha=0.7)

ax.set_title(title)
ax.set_xlabel(x_label)
ax.set_ylabel("Magnetische Flussdichte B (mT)")
ax.grid(True, linestyle="--", alpha=0.4)
ax.legend()

fig.tight_layout()
plt.savefig("hysterese_b_h.png")
plt.show()
