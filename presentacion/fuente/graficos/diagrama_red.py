"""Diagrama unifilar de la red modelada (26 barras, 5 polos PDGE, 34 corredores).

Modelo de transporte: los corredores solo tienen límite de capacidad.
Coordenadas en pulgadas; la vertical sigue el orden norte-sur de las barras
(rango), no la latitud.
"""
import csv
import itertools
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D

SALIDA = Path(__file__).resolve().parent  # <repo>/presentacion/fuente/graficos
REPO = SALIDA.parents[2]

SALIDA.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- fuente
disponibles = {f.name for f in font_manager.fontManager.ttflist}
fuente = next(f for f in ["Calibri", "Carlito", "Arial"] if f in disponibles)
plt.rcParams.update({"font.family": fuente, "font.size": 7.5, "svg.fonttype": "none"})

# ---------------------------------------------------------------- datos
with open(REPO / "resultados" / "tablas" / "zonas.csv", encoding="utf-8") as f:
    zonas = list(csv.DictReader(f))
with open(REPO / "casos" / "SIN_DC" / "inputs" / "transmission_lines.csv", encoding="utf-8") as f:
    corredores = list(csv.DictReader(f))

barras = [z for z in zonas if not z["zona"].startswith("PDGE-")]
polos = [z for z in zonas if z["zona"].startswith("PDGE-")]
barras.sort(key=lambda z: int(z["orden"]))
rango = {z["zona"]: i for i, z in enumerate(barras)}      # 0 = más al norte
nombre = {z["zona"]: z["nombre"] for z in zonas}

# ---------------------------------------------------------------- geometría
ANCHO, ALTO = 5.5, 5.0
Y_TOP, Y_BOT = 4.86, 0.14
DY = (Y_TOP - Y_BOT) / (len(barras) - 1)
HW = 0.22                    # media longitud de la barra
S = 2.0                      # columna troncal 500 kV
R = 3.5                      # columna norte 220 kV
X_HVDC = 1.45


def y(zona, d=0.0):
    """Altura de la barra (d en fracciones de fila, positivo hacia el sur)."""
    return Y_TOP - (rango[zona] + d) * DY


# x del centro de cada barra y lado de su etiqueta
pos = {}
for z in barras:
    pos[z["zona"]] = [S, "der"]
for z in ["Parinacota220", "NuevaPozoAlmonte220", "Lagunas220", "Kimal220", "NuevaZaldivar220"]:
    pos[z] = [R, "der"]
pos["LosChangos220"] = [R - 0.25, "izq"]
pos["Quillota500"] = [S + 0.6, "der"]
pos["Rapel500"] = [S + 0.6, "der"]
pos["Concepcion500"] = [S + 0.6, "der"]
pos["Candelaria500"] = [S - 0.6, "izq"]


def x(zona, dx=0.0):
    return pos[zona][0] + dx


# Trazado ortogonal de cada corredor (lista de puntos). Una entrada por corredor.
def recta(a, b, dx_a=0.0):
    """Vertical directa entre dos barras de la misma columna."""
    return [(x(a, dx_a), y(a)), (x(a, dx_a), y(b))]


def zeta(a, dxa, b, dxb, d_mid):
    """Baja/sube desde a, cruza en horizontal a la fila intermedia y entra en b."""
    ym = y(a, d_mid)
    return [(x(a, dxa), y(a)), (x(a, dxa), ym), (x(b, dxb), ym), (x(b, dxb), y(b))]


trazado = {
    # norte 220 kV
    "NuevaPozoAlmonte220_Parinacota220": recta("NuevaPozoAlmonte220", "Parinacota220"),
    "NuevaPozoAlmonte220_Lagunas220": recta("NuevaPozoAlmonte220", "Lagunas220"),
    "Lagunas220_Kimal220": recta("Lagunas220", "Kimal220"),
    "Kimal500_Kimal220": zeta("Kimal220", -0.18, "Kimal500", +0.15, +0.5),
    "Kimal220_LosChangos220": recta("Kimal220", "LosChangos220", -0.08),
    "Kimal220_NuevaZaldivar220": recta("Kimal220", "NuevaZaldivar220", +0.15),
    "LosChangos220_NuevaZaldivar220": zeta("LosChangos220", -0.05, "NuevaZaldivar220", -0.02, +0.5),
    "LosChangos500_LosChangos220": zeta("LosChangos500", +0.15, "LosChangos220", -0.15, +0.5),
    "Parinas500_NuevaZaldivar220": zeta("Parinas500", +0.15, "NuevaZaldivar220", -0.15, -0.5),
    # troncal 500 kV
    "Kimal500_LosChangos500": recta("Kimal500", "LosChangos500"),
    "LosChangos500_Parinas500": recta("LosChangos500", "Parinas500"),
    "Parinas500_Cumbre500": recta("Parinas500", "Cumbre500"),
    "Cumbre500_NuevaCardones500": recta("Cumbre500", "NuevaCardones500"),
    "NuevaCardones500_NuevaMaitencillo500": recta("NuevaCardones500", "NuevaMaitencillo500"),
    "NuevaMaitencillo500_NuevaPandeAzucar500": recta("NuevaMaitencillo500", "NuevaPandeAzucar500"),
    "NuevaPandeAzucar500_Polpaico500": recta("NuevaPandeAzucar500", "Polpaico500"),
    "Quillota500_Polpaico500": zeta("Quillota500", -0.1, "Polpaico500", +0.15, +0.5),
    "Polpaico500_AltoJahuel500": recta("Polpaico500", "AltoJahuel500"),
    "Candelaria500_AltoJahuel500": zeta("AltoJahuel500", -0.08, "Candelaria500", +0.1, +0.5)[::-1],
    "Rapel500_AltoJahuel500": zeta("AltoJahuel500", +0.12, "Rapel500", -0.05, +0.5)[::-1],
    "AltoJahuel500_Ancoa500": recta("AltoJahuel500", "Ancoa500"),
    "Ancoa500_NuevaCharrua500": recta("Ancoa500", "NuevaCharrua500"),
    "Concepcion500_NuevaCharrua500": zeta("Concepcion500", -0.1, "NuevaCharrua500", +0.15, +0.5),
    "NuevaCharrua500_Mulchen500": recta("NuevaCharrua500", "Mulchen500"),
    "RioMalleco500_Mulchen500": recta("Mulchen500", "RioMalleco500"),
    "RioMalleco500_Pichirropulli500": recta("RioMalleco500", "Pichirropulli500"),
    "Pichirropulli500_NuevaPuertoMontt500": recta("Pichirropulli500", "NuevaPuertoMontt500"),
    "NuevaPuertoMontt500_NuevaAncud500": recta("NuevaPuertoMontt500", "NuevaAncud500"),
    # HVDC Kimal - Lo Aguirre (cap. existente 0, entra en 2030), por el costado oeste
    "Kimal500_AltoJahuel500": [(x("Kimal500", -0.17), y("Kimal500")),
                               (x("Kimal500", -0.17), y("Kimal500", 0.5)),
                               (X_HVDC, y("Kimal500", 0.5)),
                               (X_HVDC, y("AltoJahuel500", -0.5)),
                               (x("AltoJahuel500", -0.17), y("AltoJahuel500", -0.5)),
                               (x("AltoJahuel500", -0.17), y("AltoJahuel500"))],
}

# Polos PDGE: cuadrado abierto unido a su barra (dos sobre Kimal 500, el resto a la izquierda)
LADO = 0.06
polo_xy = {
    "PDGE-TOC-A1": (x("Kimal500", -0.10), y("Kimal500", -0.5)),
    "PDGE-TOC-A2": (x("Kimal500", +0.04), y("Kimal500", -0.5)),
}
for p, b in [("PDGE-ANF-B1", "LosChangos500"), ("PDGE-ANF-B2", "Parinas500"),
             ("PDGE-ANF-B3", "Cumbre500")]:
    polo_xy[p] = (x(b) - HW - 0.13, y(b))
for c in corredores:
    a, b = c["trans_lz1"], c["trans_lz2"]
    if a.startswith("PDGE-"):
        px, py = polo_xy[a]
        if abs(py - y(b)) < 1e-9:      # a la izquierda: tramo horizontal
            trazado[c["TRANSMISSION_LINE"]] = [(px + LADO / 2, py), (x(b) - HW, py)]
        else:                          # encima: tramo vertical
            trazado[c["TRANSMISSION_LINE"]] = [(px, py - LADO / 2), (px, y(b))]

# ---------------------------------------------------------------- dibujo
fig = plt.figure(figsize=(ANCHO, ALTO))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, ANCHO)
ax.set_ylim(0, ALTO)
ax.axis("off")

dibujados = []
for corredor, pts in trazado.items():
    xs, ys = zip(*pts)
    if corredor == "Kimal500_AltoJahuel500":
        ax.plot(xs, ys, color="black", lw=0.9, ls=(0, (4, 2.5)), solid_capstyle="butt", zorder=2)
    else:
        ax.plot(xs, ys, color="black", lw=0.6, zorder=2)
    dibujados.append(corredor)

textos = []
for z in barras:
    k = z["zona"]
    xc, lado = pos[k]
    ax.plot([xc - HW, xc + HW], [y(k), y(k)], color="black", lw=2.6,
            solid_capstyle="butt", zorder=3)
    if lado == "der":
        t = ax.text(xc + HW + 0.05, y(k), nombre[k], ha="left", va="center", zorder=4)
    else:
        t = ax.text(xc - HW - 0.05, y(k), nombre[k], ha="right", va="center", zorder=4)
    textos.append(t)

for p in polos:
    px, py = polo_xy[p["zona"]]
    ax.add_patch(plt.Rectangle((px - LADO / 2, py - LADO / 2), LADO, LADO, fill=True,
                               facecolor="white", edgecolor="black", lw=0.7, zorder=4))

# etiqueta del HVDC, girada sobre el tramo vertical
y_mid = (y("Kimal500", 0.5) + y("AltoJahuel500", -0.5)) / 2
textos.append(ax.text(X_HVDC - 0.06, y_mid, "HVDC (2030)", rotation=90, ha="right",
                      va="center", fontsize=7.5))

# macrozonas en el margen izquierdo
GRIS = "#7a7a7a"
for mz, grupo in itertools.groupby(barras, key=lambda z: z["macrozona"]):
    grupo = list(grupo)
    y1, y2 = y(grupo[0]["zona"], -0.3), y(grupo[-1]["zona"], +0.3)
    ax.plot([0.30, 0.30], [y1, y2], color=GRIS, lw=0.6)
    textos.append(ax.text(0.24, (y1 + y2) / 2, mz, rotation=90, ha="right", va="center",
                          fontsize=7, color=GRIS))

# leyenda
manejadores = [
    Line2D([], [], color="black", lw=2.6, solid_capstyle="butt"),
    Line2D([], [], ls="none", marker="s", markersize=4.3, markerfacecolor="white",
           markeredgecolor="black", markeredgewidth=0.7),
    Line2D([], [], color="black", lw=0.6),
    Line2D([], [], color="black", lw=0.9, ls=(0, (4, 2.5))),
]
etiquetas = ["Barra", "Polo de generación (PDGE)", "Corredor (modelo de transporte)",
             "HVDC comprometido (2030)"]
leyenda = ax.legend(manejadores, etiquetas, loc="lower right", bbox_to_anchor=(0.995, 0.01),
                    frameon=False, fontsize=7.5, handlelength=2.2, handletextpad=0.6,
                    labelspacing=0.55, borderaxespad=0.0)

# ---------------------------------------------------------------- verificación
ids_csv = [c["TRANSMISSION_LINE"] for c in corredores]
assert len(ids_csv) == len(set(ids_csv)) == 34, len(ids_csv)
assert sorted(dibujados) == sorted(ids_csv), set(ids_csv) ^ set(dibujados)
assert len(dibujados) == len(set(dibujados))
for c in corredores:                      # cada trazado empieza/termina en sus barras
    pts = trazado[c["TRANSMISSION_LINE"]]
    for zona in (c["trans_lz1"], c["trans_lz2"]):
        if zona.startswith("PDGE-"):
            continue
        assert any(abs(py - y(zona)) < 1e-9 and abs(px - x(zona)) <= HW + 1e-9
                   for px, py in (pts[0], pts[-1])), (c["TRANSMISSION_LINE"], zona)
assert len(barras) == 26 and len(polos) == 5

# solapes: textos entre sí y textos contra segmentos/barras
fig.canvas.draw()
rend = fig.canvas.get_renderer()
inv = ax.transData.inverted()
cajas = []
for t in textos:
    bb = t.get_window_extent(rend).transformed(inv)
    cajas.append((t.get_text(), bb.x0, bb.y0, bb.x1, bb.y1))
lb = leyenda.get_window_extent(rend).transformed(inv)
cajas.append(("<leyenda>", lb.x0, lb.y0, lb.x1, lb.y1))

problemas = []
for (n1, *a), (n2, *b) in itertools.combinations(cajas, 2):
    if a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]:
        problemas.append(f"texto-texto: {n1} / {n2}")

segmentos = []
for corredor, pts in trazado.items():
    segmentos += [(corredor, p, q) for p, q in zip(pts, pts[1:])]
for z in barras:
    k = z["zona"]
    segmentos.append((f"barra {k}", (x(k) - HW, y(k)), (x(k) + HW, y(k))))
for n, x0, y0, x1, y1 in cajas:
    for corredor, (ax_, ay_), (bx_, by_) in segmentos:
        sx0, sx1 = sorted((ax_, bx_))
        sy0, sy1 = sorted((ay_, by_))
        if sx0 < x1 and x0 < sx1 + 1e-9 and sy0 < y1 and y0 < sy1 + 1e-9:
            if sx0 <= x1 and sx1 >= x0 and sy0 <= y1 and sy1 >= y0:
                problemas.append(f"texto-linea: {n} / {corredor}")
    if x0 < 0 or x1 > ANCHO or y0 < 0 or y1 > ALTO:
        problemas.append(f"fuera de la figura: {n}")
print("fuente:", fuente)
print(f"barras={len(barras)} polos={len(polos)} corredores={len(dibujados)} (csv={len(ids_csv)})")
print("problemas:", problemas or "ninguno")

fig.savefig(SALIDA / "diagrama_red.png", dpi=300, facecolor="white")
fig.savefig(SALIDA / "diagrama_red.svg", facecolor="white")
print("ok", SALIDA)
