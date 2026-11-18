import csv, json, zipfile, math, unicodedata, os
from collections import defaultdict
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Polygon as MPoly
import matplotlib.patheffects as pe

B = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))  # raíz del repositorio
OUT = os.path.dirname(os.path.abspath(__file__))   # carpeta del deck (fuente\graficos), no el repositorio

# ---------------- datos ----------------
zona_region = {r["zona"]: r["region"] for r in csv.DictReader(open(B + r"\resultados\tablas\zonas.csv", encoding="utf-8"))}
medios = defaultdict(float)
for r in csv.DictReader(open(B + r"\resultados\tablas\ubicacion_dc.csv", encoding="utf-8")):
    if r["PERIOD"] == "2050":
        medios[(r["escenario"], r["modo"], zona_region[r["LOAD_ZONE"]])] += float(r["dc_total_mw"])

ESC = [("PELP_E2", "PELP E2"), ("CEN", "CEN"), ("PELP_N1", "PELP N1"), ("PROPIO", "Propio")]
MODOS = [("base", "Proyección"), ("libre", "Óptima")]
for e, _ in ESC:
    tb = sum(v for (ee, m, _), v in medios.items() if ee == e and m == "base")
    tl = sum(v for (ee, m, _), v in medios.items() if ee == e and m == "libre")
    print(f"total {e}: base {tb:.3f}  libre {tl:.3f}  dif {tl - tb:+.4f}  (cap {tb/0.5:.1f})")
    assert abs(tb - tl) < 1e-3 * max(tb, 1), e

filas = []
for e, _ in ESC:
    for m, _ in MODOS:
        for (ee, mm, reg), v in sorted(medios.items(), key=lambda kv: -kv[1]):
            if ee == e and mm == m and v > 1e-6:
                filas.append((e, m, reg, v, v / 0.5))
with open(OUT + r"\mapa_dc_2050_datos.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["escenario", "modo", "region", "mw_medios", "mw_capacidad"])
    for e, m, reg, v, c in filas:
        w.writerow([e, m, reg, f"{v:.3f}", f"{c:.3f}"])

# ---------------- geometría ----------------
def norm(s):
    s = unicodedata.normalize("NFKD", s)
    return "".join(ch for ch in s if ch.isalpha()).lower()

ALIAS = {"santiagometropolitan": "metropolitana", "libertadorgeneralbernardoohi": "ohiggins"}
GEO = os.path.join(OUT, "geo", "gadm41_CHL_1.json.zip")
if not os.path.exists(GEO):
    # Límites regionales de GADM 4.1. Su licencia no permite redistribuirlos: se descargan aquí y geo/ va en .gitignore.
    import urllib.request
    URL_GADM = "https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_CHL_1.json.zip"
    print("descargando", URL_GADM)
    os.makedirs(os.path.dirname(GEO), exist_ok=True)
    urllib.request.urlretrieve(URL_GADM, GEO + ".part")
    os.replace(GEO + ".part", GEO)
z = zipfile.ZipFile(GEO)
gj = json.loads(z.read("gadm41_CHL_1.json").decode("utf-8"))

PHI0 = math.cos(math.radians(31.0))
def proj(lon, lat):
    return lon * PHI0, lat

def ring_area(r):
    a = 0.0
    for (x1, y1), (x2, y2) in zip(r, r[1:] + r[:1]):
        a += x1 * y2 - x2 * y1
    return a / 2

def dp(pts, tol):
    if len(pts) < 3:
        return pts
    stack = [(0, len(pts) - 1)]; keep = [False] * len(pts); keep[0] = keep[-1] = True
    while stack:
        i, j = stack.pop()
        (x1, y1), (x2, y2) = pts[i], pts[j]
        dx, dy = x2 - x1, y2 - y1; L = math.hypot(dx, dy)
        dmax, idx = -1, None
        for k in range(i + 1, j):
            x0, y0 = pts[k]
            d = abs(dy * x0 - dx * y0 + x2 * y1 - y2 * x1) / L if L > 0 else math.hypot(x0 - x1, y0 - y1)
            if d > dmax:
                dmax, idx = d, k
        if idx is not None and dmax > tol:
            keep[idx] = True; stack += [(i, idx), (idx, j)]
    return [p for p, k in zip(pts, keep) if k]

regiones = {}   # clave -> anillos proyectados y simplificados
for ft in gj["features"]:
    k = norm(ft["properties"]["NAME_1"]); k = ALIAS.get(k, k)
    if k.startswith("aysen") or k.startswith("magallanes"):
        continue
    rings = []
    for poly in ft["geometry"]["coordinates"]:
        ext = poly[0]
        cx = sum(p[0] for p in ext) / len(ext)
        if cx < -76.0:            # islas oceánicas (Juan Fernández, Desventuradas, Rapa Nui)
            continue
        r = [proj(x, y) for x, y in ext]
        if abs(ring_area(r)) < 0.01:   # islotes
            continue
        r = dp(r, 0.012)
        if len(r) >= 4:
            rings.append(r)
    regiones[k] = rings
print("regiones:", sorted(regiones))

def rep_point(rings):
    big = max(rings, key=lambda r: abs(ring_area(r)))
    A = ring_area(big); cx = cy = 0.0
    for (x1, y1), (x2, y2) in zip(big, big[1:] + big[:1]):
        c = x1 * y2 - x2 * y1; cx += (x1 + x2) * c; cy += (y1 + y2) * c
    cx /= 6 * A; cy /= 6 * A
    xs = []
    for (x1, y1), (x2, y2) in zip(big, big[1:] + big[:1]):
        if (y1 > cy) != (y2 > cy):
            xs.append(x1 + (cy - y1) * (x2 - x1) / (y2 - y1))
    xs.sort()
    best = max(((xs[i + 1] - xs[i], (xs[i] + xs[i + 1]) / 2) for i in range(0, len(xs) - 1, 2)))
    return best[1], cy

punto = {k: rep_point(v) for k, v in regiones.items()}
allx = [p[0] for v in regiones.values() for r in v for p in r]
ally = [p[1] for v in regiones.values() for r in v for p in r]
X0, X1, Y0, Y1 = min(allx), max(allx), min(ally), max(ally)
print("extent", X0 / PHI0, X1 / PHI0, Y0, Y1)

# ---------------- figura ----------------
for f in ("calibri.ttf", "calibrib.ttf"):
    font_manager.fontManager.addfont(os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", f))
plt.rcParams.update({"font.family": "Calibri", "svg.fonttype": "path", "svg.hashsalt": "ubicacion-dc"})   # SVG reproducible
FP7 = FontProperties(family="Calibri", size=7)

W, H = 12.1, 4.6
LEG_W = 0.95
MAP_TOP, MAP_BOT = 4.00, 0.06
GAP_PAIR = 0.20
PW = (W - LEG_W - 0.05 - 3 * GAP_PAIR) / 8
SC = (MAP_TOP - MAP_BOT) / (Y1 - Y0)            # pulgadas por unidad
# Escala común a los 8 mapas: el círculo más grande mide a lo más ~44 pt de diámetro
CAP_MAX = max(c for *_, c in filas)
K = min(0.30, 44 ** 2 / CAP_MAX)                  # pt^2 por MW (área de scatter)
LEYENDA = (10000, 4000, 1000) if CAP_MAX > 8000 else (2000, 1000, 500)
GRIS, NEGRO = "#8C8C8C", "#111111"

fig = plt.figure(figsize=(W, H))
fig.patch.set_alpha(0)

def fmt(v):
    return f"{int(round(v)):,}".replace(",", ".")

def text_wh(s):
    ext = TextPath((0, 0), s, prop=FP7).get_extents()
    return ext.width, 7 * 0.72    # alto aproximado de cifras (pt)

def box_overlap(a, b):
    dx = min(a[2], b[2]) - max(a[0], b[0]); dy = min(a[3], b[3]) - max(a[1], b[1])
    return dx * dy if dx > 0 and dy > 0 else 0.0

def circ_box_overlap(c, b):
    cx, cy, r = c; rr = r * 0.85
    return box_overlap((cx - rr, cy - rr, cx + rr, cy + rr), b)

x_left = 0.05
for i, (e, etxt) in enumerate(ESC):
    pair_left = x_left + i * (2 * PW + GAP_PAIR)
    fig.text((pair_left + PW) / W, 4.47 / H, etxt, ha="center", va="center", fontsize=11, fontweight="bold")
    for j, (m, mtxt) in enumerate(MODOS):
        L = pair_left + j * PW
        ax = fig.add_axes([L / W, MAP_BOT / H, PW / W, (MAP_TOP - MAP_BOT) / H])
        ax.set_axis_off(); ax.patch.set_alpha(0)
        xa = X0 - 0.03 / SC
        xb = xa + PW / SC
        ax.set_xlim(xa, xb); ax.set_ylim(Y0, Y1)
        fig.text((L + PW / 2) / W, 4.22 / H, mtxt, ha="center", va="center", fontsize=9)
        for k, rings in regiones.items():
            for r in rings:
                ax.add_patch(MPoly(r, closed=True, facecolor="white", edgecolor=GRIS, linewidth=0.4, joinstyle="round"))
        datos = [(norm(reg), c) for (ee, mm, reg, v, c) in filas if ee == e and mm == m]
        datos.sort(key=lambda t: -t[1])
        def to_pt(x, y):
            return ((L + (x - xa) * SC) * 72, (MAP_BOT + (y - Y0) * SC) * 72)
        circles = []
        for reg, c in datos:
            x, y = punto[reg]
            s = K * c
            ax.scatter([x], [y], s=s, c=NEGRO, edgecolors="white", linewidths=0.6, zorder=3 + len(circles))
            px, py = to_pt(x, y)
            circles.append((px, py, math.sqrt(s) / 2 + 0.3))
        placed = []
        pl, pr = L * 72, (L + PW) * 72
        for n, (reg, c) in enumerate(datos):
            px, py, r = circles[n]
            t = fmt(c); tw, th = text_wh(t); g = 1.8
            d = r / math.sqrt(2)
            cands = [
                (r + g, 0, "left", "center"), (-r - g, 0, "right", "center"),
                (d + g, d + g * 0.5, "left", "bottom"), (d + g, -d - g * 0.5, "left", "top"),
                (-d - g, d + g * 0.5, "right", "bottom"), (-d - g, -d - g * 0.5, "right", "top"),
                (0, r + g, "center", "bottom"), (0, -r - g, "center", "top"),
            ]
            best = None
            for ci, (dx, dy, ha, va) in enumerate(cands):
                ax_ = px + dx; ay_ = py + dy
                x0 = ax_ if ha == "left" else (ax_ - tw if ha == "right" else ax_ - tw / 2)
                y0 = ay_ - th / 2 if va == "center" else (ay_ if va == "bottom" else ay_ - th)
                bx = (x0 - 0.8, y0 - 0.8, x0 + tw + 0.8, y0 + th + 0.8)
                cost = sum(box_overlap(bx, p) for p in placed) * 10
                cost += sum(circ_box_overlap(cc, bx) for m2, cc in enumerate(circles) if m2 != n) * 3
                if bx[0] < pl + 1 or bx[2] > pr - 1:
                    cost += 1000
                cost += ci * 0.5
                if best is None or cost < best[0]:
                    best = (cost, ax_, ay_, ha, va, bx)
            cost, ax_, ay_, ha, va, bx = best
            placed.append(bx)
            # va="baseline" desplazado para centrar cifras: usar center_baseline
            fig.text(ax_ / 72 / W, ay_ / 72 / H, t, fontsize=7, ha=ha, va=va,
                     color=NEGRO, zorder=10,
                     path_effects=[pe.withStroke(linewidth=1.6, foreground="white")])
            print(f"{e:8s} {m:5s} {reg:14s} {c:8.1f} -> {t:>6s} pos={ha}/{va} cost={cost:.1f}")

# ---------------- leyenda de tamaños ----------------
lx = W - LEG_W + 0.02
fig.text(lx / W, 1.62 / H, "Capacidad instalada\nen 2050 (MW)", fontsize=8, ha="left", va="bottom", linespacing=1.15)
lax = fig.add_axes([lx / W, 0.25 / H, (LEG_W - 0.05) / W, 1.3 / H])
lax.set_axis_off(); lax.patch.set_alpha(0)
lax.set_xlim(0, (LEG_W - 0.05) * 72); lax.set_ylim(0, 1.3 * 72)
ycur = 1.3 * 72 - 4
cx = math.sqrt(K * LEYENDA[0]) / 2 + 2
for v in LEYENDA:
    dpt = math.sqrt(K * v)
    yc = ycur - dpt / 2
    lax.scatter([cx], [yc], s=K * v, c=NEGRO, edgecolors="white", linewidths=0.6)
    lax.text(cx + math.sqrt(K * LEYENDA[0]) / 2 + 5, yc, fmt(v), fontsize=7, va="center", ha="left")
    ycur = yc - dpt / 2 - 6

fig.savefig(OUT + r"\mapa_dc_2050.png", dpi=300, transparent=True)
fig.savefig(OUT + r"\mapa_dc_2050.svg", transparent=True, metadata={"Date": None})   # sin fecha
print("ok", PW, SC)
