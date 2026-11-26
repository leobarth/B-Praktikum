import numpy as np
import matplotlib.pyplot as plt

# ---------- Parameter (qualitativ, willkürliche Einheiten) ----------
mu0  = 1.0    # in willkürlichen Einheiten, daher B = H + M
Ms   = 1.0    # Sättigungsmagnetisierung
Hc   = 0.4    # Koerzitivfeldstärke der M(H)-Kurve
w    = 0.5    # Breite des Übergangs
Hmax = 2.5

H     = np.linspace(-Hmax, Hmax, 1000)
H_neu = np.linspace(0, Hmax, 500)

# ---------- Magnetisierung ----------
M_auf  = Ms * np.tanh((H - Hc) / w)   # aufsteigender Ast
M_ab   = Ms * np.tanh((H + Hc) / w)   # absteigender Ast
M_neu  = Ms * np.tanh(H_neu / w)      # Neukurve (liegt innerhalb der Schleife)

# ---------- Flussdichte B = mu0 (H + M) ----------
B_auf = mu0 * (H + M_auf)
B_ab  = mu0 * (H + M_ab)
B_neu = mu0 * (H_neu + M_neu)

# Remanenz und Koerzitivfeldstärke von B(H) (Nulldurchgang des absteigenden Asts)
Mr = Ms * np.tanh(Hc / w)
Br = mu0 * Mr
i = np.where(np.diff(np.sign(B_ab)))[0][0]
HcB = H[i] - B_ab[i] * (H[i + 1] - H[i]) / (B_ab[i + 1] - B_ab[i])  # < 0
HcB = abs(HcB)

# ---------- Plot ----------
fig, (axM, axB) = plt.subplots(1, 2, figsize=(11, 4.8))

def achsen(ax, ylabel):
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(1.02, 0, r'$H$', transform=ax.get_yaxis_transform(), va='center')
    ax.text(0, 1.02, ylabel, transform=ax.get_xaxis_transform(), ha='center')

def punkt(ax, x, y, text, offset):
    ax.plot(x, y, 'ko', ms=4, zorder=5)
    ax.annotate(text, (x, y), xytext=offset, textcoords='offset points')

# --- M(H) ---
axM.plot(H, M_auf, 'k-', label='Hystereseschleife')
axM.plot(H, M_ab, 'k-')
axM.plot(H_neu, M_neu, 'C0-', lw=2, label='Neukurve')
axM.axhline(Ms,  color='gray', ls=':', lw=1)
axM.axhline(-Ms, color='gray', ls=':', lw=1)
axM.text(-Hmax, Ms + 0.05, r'$M_\mathrm{s}$', color='gray')
punkt(axM, 0, Mr, r'$M_\mathrm{r}$', (8, -4))
punkt(axM, Hc, 0, r'$H_\mathrm{C}$', (2, -16))
punkt(axM, -Hc, 0, r'$-H_\mathrm{C}$', (-30, 6))
achsen(axM, r'$M$')
axM.set_ylim(-1.4, 1.4)
axM.set_title(r'Magnetisierung $M(H)$')
axM.legend(loc='lower right', frameon=False)

# --- B(H) ---
axB.plot(H, B_auf, 'k-', label='Hystereseschleife')
axB.plot(H, B_ab, 'k-')
axB.plot(H_neu, B_neu, 'C0-', lw=2, label='Neukurve')
punkt(axB, 0, Br, r'$B_\mathrm{r}$', (8, -4))
punkt(axB, HcB, 0, r'$H_\mathrm{C}$', (2, -16))
punkt(axB, -HcB, 0, r'$-H_\mathrm{C}$', (-30, 6))
achsen(axB, r'$B$')
axB.set_title(r'Flussdichte $B(H)=\mu_0\,(H+M)$')
axB.legend(loc='lower right', frameon=False)

fig.tight_layout()
fig.savefig('hysterese_skizze.png', dpi=300, bbox_inches='tight')
plt.show()
