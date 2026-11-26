import numpy as np
import matplotlib.pyplot as plt

# ---------- Parameter ----------
mu0 = 4 * np.pi * 1e-7      # Vs/(Am)
n   = 500                   # Gesamtwindungszahl
I   = 2.5                   # A
D   = 0.055                 # m
R   = D / 2                 # m
l_vorb = 0.080              # m, Spulenlänge laut Aufgabe 14
l_vers = 0.072              # m, Spulenlänge laut Versuchsanleitung (5.2)

def H_achse(z, l):
    """Feldstärke auf der Symmetrieachse einer endlichen Zylinderspule (Gl. 2.14)."""
    zp = z + l / 2
    zm = z - l / 2
    return n * I / (2 * l) * (zp / np.sqrt(R**2 + zp**2) - zm / np.sqrt(R**2 + zm**2))

z = np.linspace(-0.07, 0.07, 1000)     # Intervall ±7 cm
z_cm = z * 100

H_vorb = H_achse(z, l_vorb)
H_vers = H_achse(z, l_vers)

# ---------- Kontrollausgabe ----------
for name, l in [("l = 8,0 cm", l_vorb), ("l = 7,2 cm", l_vers)]:
    H0 = H_achse(0.0, l)
    He = H_achse(l / 2, l)
    print(f"{name}: H(0) = {H0:.0f} A/m (B = {mu0*H0*1e3:.2f} mT), "
          f"H(l/2) = {He:.0f} A/m ({He/H0:.0%} von H(0))")

# ---------- Plot ----------
fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(z_cm, H_vorb, 'C0-', lw=2, label=r'$l=8{,}0\,$cm (Aufgabe 14)')
ax.plot(z_cm, H_vers, 'C1--', lw=2, label=r'$l=7{,}2\,$cm (Versuchsspule)')

# Spulenenden der 8-cm-Spule
for x in (-l_vorb / 2 * 100, l_vorb / 2 * 100):
    ax.axvline(x, color='gray', ls=':', lw=1)
ax.text(l_vorb / 2 * 100 + 0.1, 0.03 * H_vorb.max(), 'Spulenende',
        rotation=90, color='gray', va='bottom', ha='left')

# Maximum markieren
H0 = H_achse(0.0, l_vorb)
ax.plot(0, H0, 'ko', ms=4, zorder=5)
ax.annotate(rf'$H(0)\approx{H0/1000:.1f}\,$kA/m',
            (0, H0), xytext=(12, -22), textcoords='offset points')

ax.set_xlabel(r'Ort $z$ auf der Symmetrieachse (cm)')
ax.set_ylabel(r'Magnetische Feldstärke $H$ (A/m)')
ax.set_title(r'Feldstärke auf der Achse einer endlichen Zylinderspule',
             pad=34)
ax.set_xlim(-7, 7)
ax.set_ylim(0, 1.1 * H_vers.max())
ax.grid(True, ls='--', alpha=0.5)
ax.legend(loc='lower center', frameon=True)

# Zweite y-Achse: B = mu0 * H in mT
sec = ax.secondary_yaxis('right',
                         functions=(lambda H: mu0 * H * 1e3,
                                    lambda B: B / (mu0 * 1e3)))
sec.set_ylabel(r'Flussdichte $B=\mu_0H$ (mT)')

fig.tight_layout()
fig.savefig('hz_spule.png', dpi=300, bbox_inches='tight')
plt.show()
