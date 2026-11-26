import math
import pandas as pd

def fmt(v, dec=None):
    s = f"{v:.{dec}f}" if dec is not None else f"{v:g}"
    return s.replace(".", ",")

def tabelle(csv, spalten, kopf, caption, label, outfile,
            dec=(None, None), marker_rows=()):
    df = pd.read_csv(csv).dropna(how="all").reset_index(drop=True)
    get = lambda c: df.iloc[:, c] if isinstance(c, int) else df[c]
    xs, ys = get(spalten[0]), get(spalten[1])
    zellen = []
    for i, (x, y) in enumerate(zip(xs, ys)):
        stern = r"$^{*}$" if i in marker_rows else ""
        zellen.append((fmt(x, dec[0]), fmt(y, dec[1]) + stern))
    n = len(zellen)
    h = math.ceil(n / 2)
    kopfzeile = f"{kopf[0]} & {kopf[1]} & {kopf[0]} & {kopf[1]} \\\\"
    if marker_rows:
        caption += r" $^{*}$\,Ausreißer (siehe Abschnitt~\ref{sec:hyst})."
    out = []
    out.append(r"\begin{longtable}{rr@{\hspace{2cm}}rr}")
    out.append(r"\caption{" + caption + r"}\label{" + label + r"}\\")
    out.append(r"\toprule"); out.append(kopfzeile); out.append(r"\midrule")
    out.append(r"\endfirsthead")
    out.append(r"\toprule"); out.append(kopfzeile); out.append(r"\midrule")
    out.append(r"\endhead")
    out.append(r"\bottomrule"); out.append(r"\endfoot")
    for i in range(h):
        l = zellen[i]
        r = zellen[i + h] if i + h < n else ("", "")
        out.append(f"{l[0]} & {l[1]} & {r[0]} & {r[1]} \\\\")
    out.append(r"\end{longtable}")
    with open(outfile, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")

tabelle("experiment_1.csv", (0, 1),
        (r"$x$ (cm)", r"$B$ (mT)"),
        "Messwerte der Luftspule (Abschnitt~\\ref{sec:luft}), unkorrigiert.",
        "tab:exp1", "tabelle_exp1.tex")

tabelle("experiment_2.csv", (0, 1),
        (r"$x$ (cm)", r"$B$ (mT)"),
        "Messwerte der Spule mit Eisenkern (Abschnitt~\\ref{sec:eisen}), unkorrigiert.",
        "tab:exp2", "tabelle_exp2.tex")

tabelle("experiment_3.csv", ("I_A", "B_mT"),
        (r"$I$ (A)", r"$B$ (mT)"),
        "Messwerte der Hysterese (Abschnitt~\\ref{sec:hyst}) in chronologischer "
        "Reihenfolge, Rohwerte mit dem Stromvorzeichen der Anzeige (nicht umgepolt).",
        "tab:exp3", "tabelle_exp3.tex",
        dec=(1, 0), marker_rows=(12,))
