import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Experiment 1: Feldmessgerät mit longitudinaler Hallsonde in Luftspule

df = pd.read_csv("experiment_1.csv")
x = df.iloc[:, 0].to_numpy()
y = df.iloc[:, 1].to_numpy()

y_label = "Magnetische Flussdichte B (mT)"
title = "Experiment 1: B-Feld der Luftspule (longitudinale Hallsonde)"

fig, ax = plt.subplots(figsize=(8, 5), dpi=150)

ax.plot(x, y, marker="o", markersize=4, linewidth=1.5, color="#1f77b4",
    label="Messdaten",)
ax.set_title(title)
ax.set_xlabel("Abstand vom Spulenmittelpunkt (cm)")
ax.set_ylabel(y_label)
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend()

fig.tight_layout()
plt.savefig("experiment_1_plot.png", dpi=300)
plt.show()
