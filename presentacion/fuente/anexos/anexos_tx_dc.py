"""Anexos de transmisión y data centers para la presentación de avance.

Calcula todas las cifras desde las entradas del modelo, el catastro (solo lectura) y escribe:
  fuente/anexos/20_transmision.js
  fuente/anexos/30_data_centers.js
  fuente/anexos/verificacion_transmision_dc.md

Correr con:  python -P anexos_tx_dc.py
"""
import csv
import datetime as dt
import hashlib
import json
import math
import os
import re
import sys
from collections import OrderedDict, defaultdict


sys.stdout.reconfigure(encoding="utf-8")

# Rutas relativas al repositorio: este archivo está en <repo>/presentacion/fuente/anexos/.
AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
DATOS = os.path.abspath(os.path.join(AQUI, "..", "datos"))
OUT = AQUI

# Catastro privado del equipo (no va en el repositorio). Si no está, se usan las filas ya extraídas en
# datos/campus_escenario_propio.csv, que este mismo script escribe cada vez que lee el catastro.
CATASTRO = os.environ.get("CATASTRO_DC_XLSX", os.path.join(DATOS, "Catastro_DataCenters_CEN_SEIA.xlsx"))
CAMPUS_CSV = os.path.join(DATOS, "campus_escenario_propio.csv")
# Copias pequeñas de archivos del modelo Switch que no están en el repositorio (ver presentacion/README.md).
LINEAS_AMEBA = os.path.join(DATOS, "lineas_ameba_a_corredores.csv")

# Uso: python -P anexos_tx_dc.py [<carpeta de casos con <CASO>/inputs>]   (por omisión, <repo>/casos)
CASOS = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, "casos")
CASOS_ANTES_TL = os.path.join(DATOS, "transmission_lines_antes_inicio_2025.csv")  # solo para documentar lo que cambió
RESUMEN_DC = os.path.join(DATOS, "resumen_escenarios_dc.csv")
INV_AMEBA_2025 = os.path.join(DATOS, "inversion_ameba_hasta_2025.csv")
CASOS_DC = ["PELP_E2", "PELP_N1", "CEN", "PROPIO"]
PERIODOS = [int(r["INVESTMENT_PERIOD"]) for r in csv.DictReader(open(os.path.join(CASOS, "SIN_DC", "inputs", "periods.csv"), encoding="utf-8"))]
FIN_PERIODO = {int(r["INVESTMENT_PERIOD"]): int(r["period_end"]) for r in csv.DictReader(open(os.path.join(CASOS, "SIN_DC", "inputs", "periods.csv"), encoding="utf-8"))}
assert PERIODOS == [2025, 2027, 2030, 2035, 2040, 2045, 2050], PERIODOS

FUENTE_TX = "Fuente: Ministerio de Energía (2025), datos del modelo AMEBA; elaboración propia."
FUENTE_DC = "Fuente: Ministerio de Energía (2026a), CEN (2026a), CEN (s. f.); elaboración propia."

VERIF = []  # (sección, cifra, cómo se obtuvo)
CHECKS = []
ALTOS = []


def v(seccion, cifra, como):
    VERIF.append((seccion, cifra, como))


def check(cond, msg):
    if not cond:
        raise SystemExit("FALLA: " + msg)
    CHECKS.append(msg)
    print("ok  ", msg)


# ------------------------------------------------------------------ formato numérico chileno
def fmt(x, dec=0):
    s = f"{x:,.{dec}f}"
    return s.replace(",", "_").replace(".", ",").replace("_", ".")


def leer(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:12]


# ------------------------------------------------------------------ nombres legibles
ZONA = {
    "AltoJahuel500": "Alto Jahuel 500", "Ancoa500": "Ancoa 500", "NuevaCharrua500": "Nueva Charrúa 500",
    "Candelaria500": "Candelaria 500", "Concepcion500": "Concepción 500", "Cumbre500": "Cumbre 500",
    "NuevaCardones500": "Nueva Cardones 500", "Kimal220": "Kimal 220", "LosChangos220": "Los Changos 220",
    "NuevaZaldivar220": "Nueva Zaldívar 220", "Kimal500": "Kimal 500", "Lagunas220": "Lagunas 220",
    "LosChangos500": "Los Changos 500", "Parinas500": "Parinas 500", "NuevaMaitencillo500": "Nueva Maitencillo 500",
    "Mulchen500": "Mulchén 500", "NuevaPandeAzucar500": "Nueva Pan de Azúcar 500", "Polpaico500": "Polpaico 500",
    "NuevaPozoAlmonte220": "Nueva Pozo Almonte 220", "Parinacota220": "Parinacota 220",
    "NuevaPuertoMontt500": "Nueva Puerto Montt 500", "NuevaAncud500": "Nueva Ancud 500",
    "Pichirropulli500": "Pichirropulli 500", "Quillota500": "Quillota 500", "Rapel500": "Rapel 500",
    "RioMalleco500": "Río Malleco 500",
}

# Orden geográfico de norte a sur para las dos láminas de corredores.
NORTE = [
    "NuevaPozoAlmonte220_Parinacota220", "NuevaPozoAlmonte220_Lagunas220", "Lagunas220_Kimal220",
    "Kimal500_Kimal220", "Kimal220_NuevaZaldivar220", "Kimal220_LosChangos220", "Kimal500_LosChangos500",
    "LosChangos500_LosChangos220", "LosChangos220_NuevaZaldivar220", "LosChangos500_Parinas500",
    "Parinas500_NuevaZaldivar220", "Parinas500_Cumbre500", "Cumbre500_NuevaCardones500",
    "NuevaCardones500_NuevaMaitencillo500", "NuevaMaitencillo500_NuevaPandeAzucar500",
]
CENTRO_SUR = [
    "NuevaPandeAzucar500_Polpaico500", "Kimal500_AltoJahuel500", "Quillota500_Polpaico500",
    "Polpaico500_AltoJahuel500", "Candelaria500_AltoJahuel500", "Rapel500_AltoJahuel500",
    "AltoJahuel500_Ancoa500", "Ancoa500_NuevaCharrua500", "Concepcion500_NuevaCharrua500",
    "NuevaCharrua500_Mulchen500", "RioMalleco500_Mulchen500", "RioMalleco500_Pichirropulli500",
    "Pichirropulli500_NuevaPuertoMontt500", "NuevaPuertoMontt500_NuevaAncud500",
]


def nombre_corredor(r):
    return f"{ZONA[r['trans_lz1']]} – {ZONA[r['trans_lz2']]}"


# ------------------------------------------------------------------ alto de bloques (FORMATO.md y build.js)
ROW_H = {11: 0.29, 12: 0.31, 14: 0.34}
CPI = {11: 16, 12: 14, 14: 12}


def alto_texto(txt, fs, w):
    por_linea = max(10, math.floor(w * 168 / fs))
    return math.ceil(len(str(txt)) / por_linea) * fs * 1.25 / 72


def alto_bloque(b, w):
    if b["tipo"] == "tabla":
        fs = b.get("letra", 12)
        n = len(b["filas"]) + (1 if b.get("header") else 0)
        return ROW_H[fs] * n
    if b["tipo"] == "bullets":
        fs = b.get("letra", 14)
        return sum(alto_texto(it["text"] if isinstance(it, dict) else it, fs, w - 0.3) + 0.08 for it in b["items"])
    if b["tipo"] == "texto":
        fs = b.get("letra", 12)
        return alto_texto(b["texto"], fs, w) + 0.05
    if b["tipo"] == "grafico":
        return b.get("alto", 3.2)
    raise ValueError(b["tipo"])


def validar_lamina(lam):
    assert len(lam["titulo"]) <= 45, (lam["titulo"], len(lam["titulo"]))
    assert len(lam["subtitulo"]) <= 110, (lam["subtitulo"], len(lam["subtitulo"]))
    cols = lam["columnas"]
    anchos = [c["ancho"] for c in cols]
    if len(cols) == 1:
        assert abs(anchos[0] - 12.13) < 1e-9, anchos
    else:
        assert abs(sum(anchos) - 11.68) < 1e-9, anchos
    altos = []
    for c in cols:
        h = sum(alto_bloque(b, c["ancho"]) for b in c["bloques"]) + 0.15 * (len(c["bloques"]) - 1)
        altos.append(round(h, 2))
        assert h <= 4.8 + 1e-9, (lam["titulo"], h)
        for b in c["bloques"]:
            if b["tipo"] != "tabla":
                continue
            assert abs(sum(b["anchos"]) - c["ancho"]) < 1e-6, (lam["titulo"], sum(b["anchos"]), c["ancho"])
            fs = b.get("letra", 12)
            for fila in [b["header"]] + b["filas"]:
                assert len(fila) == len(b["anchos"])
                for txt, w in zip(fila, b["anchos"]):
                    cap = (w - 0.17) * CPI[fs]  # 6 pt de margen a cada lado
                    assert len(txt) <= cap, f"celda larga ({len(txt)} > {cap:.0f}): {txt!r} en {lam['titulo']}"
    assert len(lam.get("fuente", "")) <= 120
    ALTOS.append((lam["titulo"], altos))
    print(f"ok   lámina «{lam['titulo']}»: alto por columna {altos} in (máx. 4,8)")


def js(x, ind=0):
    sp = "  " * ind
    if isinstance(x, dict):
        partes = [f"{sp}  {k}: {js(v_, ind + 1)}" for k, v_ in x.items()]
        return "{\n" + ",\n".join(partes) + "\n" + sp + "}"
    if isinstance(x, list):
        if all(not isinstance(e, (dict, list)) for e in x):
            return "[" + ", ".join(json.dumps(e, ensure_ascii=False) for e in x) + "]"
        return "[\n" + ",\n".join(f"{sp}  {js(e, ind + 1)}" for e in x) + "\n" + sp + "]"
    return json.dumps(x, ensure_ascii=False)


def a_js(laminas, cabecera):
    return cabecera + "module.exports = " + js(laminas) + ";\n"


# ================================================================== 1. TRANSMISIÓN
INP = os.path.join(CASOS, "SIN_DC", "inputs")
tl = leer(os.path.join(INP, "transmission_lines.csv"))
tbl = leer(os.path.join(INP, "trans_build_limits.csv"))
tp = leer(os.path.join(INP, "trans_params.csv"))[0]
fin = leer(os.path.join(INP, "financials.csv"))[0]

for c in CASOS_DC:
    for f in ["transmission_lines.csv", "trans_build_limits.csv", "trans_params.csv"]:
        check(sha(os.path.join(INP, f)) == sha(os.path.join(CASOS, c, "inputs", f)),
              f"{f} de {c} es idéntico al de SIN_DC")

lineas = {r["TRANSMISSION_LINE"]: r for r in tl}
pdge = [k for k, r in lineas.items() if r["trans_lz1"].startswith("PDGE") or r["trans_lz2"].startswith("PDGE")]
red = [k for k in lineas if k not in pdge]
check(len(lineas) == 34 and len(pdge) == 5 and len(red) == 29, "34 corredores: 29 de red y 5 enlaces PDGE")
check(sorted(NORTE + CENTRO_SUR) == sorted(red), "las dos láminas cubren los 29 corredores de red, sin repetir")

lim = defaultdict(dict)
for r in tbl:
    lim[r["TRANSMISSION_LINE"]][int(r["PERIOD"])] = (float(r["min_build_mw"]), float(r["max_build_mw"]))
check(set(lim) <= set(lineas), "trans_build_limits solo nombra corredores de transmission_lines (no hay corredores nuevos)")
sin_lim = sorted(set(lineas) - set(lim))
check(sin_lim == ["Kimal220_LosChangos220"], "el único corredor sin filas de ampliación es Kimal220_LosChangos220")
check(lineas["Kimal220_LosChangos220"]["trans_new_build_allowed"] == "0", "Kimal220_LosChangos220 tiene trans_new_build_allowed = 0")
check(len(tbl) == 33 * 7 and all(len(lim[k]) == 7 for k in lim), "231 filas: 33 corredores ampliables × 7 períodos")

# Máximo acumulado no decreciente y mínimo (obras comprometidas)
for k, d in lim.items():
    mx = [d[p][1] for p in PERIODOS]
    assert all(b >= a - 1e-9 for a, b in zip(mx, mx[1:])), k
check(True, "el tope acumulado es no decreciente en todos los corredores")
comprometidas = [(k, p, d[p][0]) for k, d in lim.items() for p in PERIODOS if d[p][0] > 0]
check(sorted(comprometidas) == [("Kimal500_AltoJahuel500", 2030, 2000.0), ("RioMalleco500_Pichirropulli500", 2030, 660.0)],
      "obras comprometidas: Kimal500_AltoJahuel500 2.000 MW y RioMalleco500_Pichirropulli500 660 MW, ambas en 2030")
for k, p, mn in comprometidas:
    assert lim[k][p][1] >= mn

existente = {k: float(lineas[k]["existing_trans_cap"]) for k in lineas}
cero_red = [k for k in red if existente[k] == 0]
check(cero_red == ["Kimal500_AltoJahuel500"], "de los 29 corredores de red, solo Kimal500_AltoJahuel500 parte con 0 MW")
check(lim["Kimal500_AltoJahuel500"][2025] == (0.0, 0.0) and lim["Kimal500_AltoJahuel500"][2027] == (0.0, 0.0),
      "Kimal500_AltoJahuel500 no puede construirse en 2025 ni en 2027 (tope 0)")
check(all(existente[k] == 0 for k in pdge) and all(lim[k][p] == (0.0, 99999.0) for k in pdge for p in PERIODOS),
      "los 5 enlaces PDGE parten en 0 MW con tope 99.999 MW en todos los períodos")
check(all(float(lineas[k]["trans_terrain_multiplier"]) == 1.0 for k in pdge), "costo de los enlaces PDGE: 1 USD/MW")
check(all(lineas[k]["trans_efficiency"] == "1.0" for k in lineas), "eficiencia 1 (sin pérdidas) en los 34 corredores")
check(all(lineas[k]["trans_length_km"] == "1.0" for k in lineas) and tp["trans_capital_cost_per_mw_km"] == "1.0",
      "costo por MW = trans_terrain_multiplier (largo 1 km y 1 USD/MW-km)")

tot_exist = sum(existente[k] for k in red)
v("Transmisión", f"{fmt(tot_exist)} MW existentes en los 29 corredores de red",
  "suma de `existing_trans_cap` de `transmission_lines.csv` sin los 5 enlaces PDGE")

# Lo que AMEBA construyó hasta 2025: antes existente, ahora candidato (documentación)
inv25 = {r["TRANSMISSION_LINE"]: float(r["ameba_construido_hasta_2025_mw"]) for r in leer(INV_AMEBA_2025)}
tot_2025 = sum(inv25.values())
# Verificaciones de trazabilidad contra los datos de AMEBA. El repositorio no publica los datos de la PELP,
# así que solo corren si están los archivos privados (lineas_ameba_a_corredores.csv y las entradas anteriores).
if os.path.exists(LINEAS_AMEBA) and os.path.exists(CASOS_ANTES_TL):
    # Contraste con las líneas AMEBA (trazabilidad de la traducción, solo verificación)
    la = leer(LINEAS_AMEBA)
    ex_ameba = defaultdict(float)
    cand_ameba = defaultdict(float)
    for r in la:
        if r["clase"] == "existente":
            ex_ameba[r["TRANSMISSION_LINE"]] += float(r["max_flow"])
        if r["clase"] == "candidata":
            cand_ameba[r["TRANSMISSION_LINE"]] += float(r["max_flow"])
    clases = defaultdict(int)
    for r in la:
        clases[r["clase"]] += 1
    print("     clases AMEBA:", dict(clases))
    corr_cand = {r["TRANSMISSION_LINE"] for r in la if r["clase"] in ("candidata", "comprometida")}
    check(corr_cand <= set(lineas), "toda línea candidata o comprometida de AMEBA cae en uno de los 34 corredores")
    sin_exist_ameba = sorted(k for k in red if ex_ameba.get(k, 0) == 0)
    check(sin_exist_ameba == ["Kimal500_AltoJahuel500"],
          "en AMEBA, el único corredor de red sin línea existente es Kimal500_AltoJahuel500 (el HVDC)")
    tot_ex_ameba = sum(ex_ameba[k] for k in red)
    check(all(abs(existente[k] - ex_ameba.get(k, 0.0)) < 1e-6 for k in red) and abs(tot_exist - 38519) < 1,
          f"existente = líneas AMEBA de entrada en servicio el 1-ene-2025, corredor a corredor: {fmt(tot_exist)} MW "
          "(nada construido por AMEBA entra como dato)")
    # Los topes ya no se rebajan: tope 2050 = candidatos AMEBA + comprometida
    for k in red:
        if k in lim:
            orig = cand_ameba.get(k, 0.0) + sum(mn for kk, p, mn in comprometidas if kk == k)
            assert abs(orig - lim[k][2050][1]) < 1e-6, (k, orig, lim[k][2050][1])
    check(True, "tope 2050 = candidatos AMEBA + comprometida, en los 28 corredores ampliables (sin rebaja por lo que AMEBA construyó)")
    ex_antes = {r["TRANSMISSION_LINE"]: float(r["existing_trans_cap"]) for r in leer(CASOS_ANTES_TL)}
    dif_antes = {k: ex_antes[k] - existente[k] for k in red if abs(ex_antes[k] - existente[k]) > 1e-6}
    check(abs(sum(dif_antes.values()) - tot_2025) < 1e-3 and set(dif_antes) == set(inv25) and abs(tot_2025 - 2672.1) < 0.1,
          f"lo que AMEBA construyó hasta 2025 ({fmt(tot_2025, 1)} MW en {len(inv25)} corredores) = existente anterior − existente nuevo; "
          "vuelve al potencial candidato")
    for k, x in inv25.items():
        assert lim[k][2025][1] >= x - 1e-6, k
    check(True, "lo que AMEBA construyó hasta 2025 cabe en el tope de 2025 de cada corredor")
    v("Transmisión", f"{fmt(tot_exist)} MW existentes; antes {fmt(sum(ex_antes[k] for k in red))} MW",
      "`existing_trans_cap` (inputs nuevos) igual, corredor a corredor, a las líneas AMEBA clase `existente` de "
      "`lineas_ameba_a_corredores.csv`; los casos anteriores sumaban lo que AMEBA construyó hasta 2025 "
      f"({fmt(tot_2025, 1)} MW, autocomprobación `inversion_ameba_hasta_2025.csv`: {', '.join(sorted(inv25))})")
else:
    print("     (verificación contra las líneas AMEBA omitida: los datos de la PELP no están en el repositorio)")
    v("Transmisión", f"{fmt(tot_exist)} MW existentes en los 29 corredores de red",
      f"`existing_trans_cap` de las entradas; lo que AMEBA construyó hasta 2025 ({fmt(tot_2025, 1)} MW en {len(inv25)} corredores) no es dato")

# Patrón típico de tope acumulado
patrones = defaultdict(list)
for k in red:
    if k in lim:
        patrones[tuple(lim[k][p][1] for p in PERIODOS)].append(k)
tipico, tip_corr = max(patrones.items(), key=lambda kv: len(kv[1]))
n_ampliables = sum(1 for k in red if k in lim)
check(n_ampliables == 28, "28 corredores de red ampliables")
check(tipico == (500.0, 500.0, 500.0, 2000.0, 3500.0, 3500.0, 4500.0), f"patrón de tope más frecuente: {tipico} en {len(tip_corr)} corredores")
v("Transmisión", f"tope típico 500/500/500/2.000/3.500/3.500/4.500 MW en {len(tip_corr)} de 28 corredores",
  "patrón más frecuente de `max_build_mw` por período en `trans_build_limits.csv`: " + ", ".join(sorted(tip_corr)))

# Costos y anualidad
costos = {k: float(lineas[k]["trans_terrain_multiplier"]) for k in red if k in lim}
cmin, cmax = min(costos.values()), max(costos.values())
r_ = float(fin["interest_rate"])
vida = int(tp["trans_lifetime_yrs"])
crf = r_ / (1 - (1 + r_) ** -vida)
check(abs(cmin - 17950) < 1e-6 and abs(cmax - 625600) < 1e-6, f"costo por MW entre {fmt(cmin)} y {fmt(cmax)} USD/MW")
check(vida == 40 and r_ == 0.06 and tp["trans_fixed_om_fraction"] == "0.0", "vida 40 años, tasa 6 %, sin O&M")
check(abs(crf - 0.066462) < 1e-6, f"factor de anualidad FRC(6 %, 40) = {crf:.6f}")
v("Transmisión", f"{fmt(cmin)} a {fmt(cmax)} USD/MW; FRC = {crf:.4f}",
  "mín. y máx. de `trans_terrain_multiplier` (× largo 1 km × 1 USD/MW-km) en los 28 corredores ampliables; "
  "FRC = i / (1 − (1 + i)^−40) con i = 6 % de `financials.csv` y vida de `trans_params.csv`")
v("Transmisión", f"anualidad {fmt(cmin * crf)} a {fmt(cmax * crf)} USD/MW-año", "costo × FRC (solo notas)")


def fila_corredor(k):
    r = lineas[k]
    comp = [(p, mn) for kk, p, mn in comprometidas if kk == k]
    obra = "—" if not comp else "; ".join(f"{fmt(mn)} MW ({p})" for p, mn in comp)
    ampl = lim[k][2050][1] if k in lim else 0.0
    return [nombre_corredor(r), fmt(existente[k]), obra, fmt(ampl)]


for k in red:
    f = fila_corredor(k)
    v("Transmisión (tabla)", f"{f[0]}: existente {f[1]}; obra {f[2]}; ampliación máx. 2050 {f[3]}",
      f"`{k}`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW")

# Suma de las cifras redondeadas frente al total
suma_red = sum(round(existente[k]) for k in red)
print(f"     suma de existentes redondeados: {suma_red} frente a {tot_exist:.2f}")

# Corredores sin ampliación antes de 2035
sin_antes_2035 = sorted(k for k in red if k in lim and lim[k][2030][1] == 0 and k != "Kimal500_AltoJahuel500")
check(sin_antes_2035 == [], "todos los corredores ampliables (salvo el HVDC) pueden ampliarse desde 2025")
pdte_2025 = sorted(k for k in red if k in lim and k != "Kimal500_AltoJahuel500" and lim[k][2025][1] == 0)
check(pdte_2025 == [], "ningún corredor ampliable de red (salvo el HVDC) tiene tope 0 en 2025")
hvdc = lim["Kimal500_AltoJahuel500"]

TABLA_TX = dict(anchos=[3.6, 1.35, 1.65, 1.7], letra=11, derecha=[1, 2, 3])
HEADER_TX = ["Corredor", "Existente (MW)", "Obra comprometida", "Ampliación máx. 2050"]

pdge_txt = ", ".join(sorted({(lineas[k]["trans_lz1"] if lineas[k]["trans_lz1"].startswith("PDGE") else lineas[k]["trans_lz2"]).replace("PDGE-", "") for k in pdge}))
pdge_dest = sorted({ZONA[lineas[k]["trans_lz2"]] for k in pdge})
check(pdge_txt == "ANF-B1, ANF-B2, ANF-B3, TOC-A1, TOC-A2", "polos PDGE: " + pdge_txt)


def y_lista(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " y " + xs[-1]


tx1 = {
    "titulo": "Anexo: corredores de transmisión (norte)",
    "subtitulo": "Corredores de red de Parinacota a Nueva Pan de Azúcar: capacidad inicial, obras y tope de ampliación",
    "columnas": [
        {"ancho": 8.3, "bloques": [dict(tipo="tabla", header=HEADER_TX, filas=[fila_corredor(k) for k in NORTE], **TABLA_TX)]},
        {"ancho": 3.38, "bloques": [{
            "tipo": "bullets", "letra": 12, "items": [
                "Existente: líneas en servicio el 1 de enero de 2025 según los datos de entrada de la PELP",
                "Ampliación máxima: tope acumulado de los candidatos de la PELP hasta 2050",
                "Kimal 220 – Los Changos 220 no tiene candidatos y no se amplía",
                f"Enlaces PDGE: 5 enlaces unen los polos de generación con {y_lista(pdge_dest)}; "
                "parten en 0 MW, sin tope efectivo y con costo de 1 USD/MW",
            ]}]},
    ],
    "fuente": FUENTE_TX,
    "notas": (
        "Siglas: PELP, Planificación Energética de Largo Plazo (aquí, la 2023–2027, escenario Carbono Neutralidad); "
        "AMEBA, modelo de optimización con que el Ministerio de Energía hizo esa PELP; PDGE, polos de desarrollo de "
        "generación eléctrica; HVDC, enlace de corriente continua en alta tensión.\n"
        f"Polos PDGE: {y_lista(pdge_txt.split(', '))}. No son zonas candidatas para data centers.\n"
        f"Las 161 líneas de AMEBA quedan en 34 corredores: 29 de red y 5 de enlace a polos PDGE. Las líneas paralelas "
        f"se suman en un corredor. La capacidad existente de los 29 corredores suma {fmt(tot_exist)} MW: las líneas "
        "de los datos de entrada en servicio el 1 de enero de 2025. Lo que AMEBA decidió construir no es un dato: "
        f"sus {fmt(tot_2025)} MW de 2025, en {len(inv25)} corredores, siguen siendo candidatos y los decide el modelo.\n"
        "Los números se redondean a MW; el nombre de cada corredor sigue el orden de las barras en la PELP."),
}

tx2 = {
    "titulo": "Anexo: corredores de transmisión (centro-sur)",
    "subtitulo": "Corredores de red de Nueva Pan de Azúcar a Nueva Ancud y el HVDC Kimal–Lo Aguirre",
    "columnas": [
        {"ancho": 8.3, "bloques": [dict(tipo="tabla", header=HEADER_TX, filas=[fila_corredor(k) for k in CENTRO_SUR], **TABLA_TX)]},
        {"ancho": 3.38, "bloques": [{
            "tipo": "bullets", "letra": 12, "items": [
                f"HVDC Kimal–Lo Aguirre: en la red de la PELP llega a Alto Jahuel 500; {fmt(hvdc[2030][0])} MW "
                "forzados en 2030 y tope acumulado de "
                f"{fmt(hvdc[2050][1])} MW al 2050",
                "Río Malleco – Pichirropulli: 660 MW forzados en 2030",
                f"Capacidad existente de los 29 corredores: {fmt(tot_exist)} MW",
            ]}]},
    ],
    "fuente": FUENTE_TX,
    "notas": (
        "HVDC: enlace de corriente continua en alta tensión. En la PELP 2023–2027 el HVDC Kimal–Lo Aguirre tiene "
        f"{fmt(hvdc[2030][0])} MW y fecha enero de 2029. Una obra opera en un período si está en servicio el 1 de enero "
        "de su año de inicio; el período 2027 (2027–2029) parte antes, así que el HVDC entra en el período 2030. Antes "
        "de 2030 el corredor Kimal 500 – Alto Jahuel 500 tiene capacidad 0 y no puede ampliarse. Río Malleco – "
        "Pichirropulli tiene fecha 1 de febrero de 2030 y opera 11 de los 12 meses de ese año, así que también entra "
        "en el período 2030.\n"
        f"La ampliación máxima incluye la obra comprometida: en Kimal 500 – Alto Jahuel 500, {fmt(hvdc[2050][1])} MW = "
        f"{fmt(hvdc[2030][0])} MW comprometidos + {fmt(hvdc[2050][1] - hvdc[2030][0])} MW de candidatos; en Río Malleco – "
        f"Pichirropulli, {fmt(lim['RioMalleco500_Pichirropulli500'][2050][1])} MW = 660 + "
        f"{fmt(lim['RioMalleco500_Pichirropulli500'][2050][1] - 660)}.\n"
        f"Existente total de los 29 corredores: {fmt(tot_exist)} MW, en servicio el 1 de enero de 2025; lo que AMEBA "
        "construye desde 2025 no entra como dato."),
}

HDR_EJ = ["Período", "HVDC", "Típico"]
filas_ej = []
for p in PERIODOS:
    mn, mx = hvdc[p]
    h = fmt(mx) + (" (forzada)" if mn > 0 else "")
    filas_ej.append([str(p), h, fmt(tipico[PERIODOS.index(p)])])
tx3 = {
    "titulo": "Anexo: ampliación de la transmisión",
    "subtitulo": "Cómo decide el modelo la capacidad de cada corredor entre 2025 y 2050",
    "columnas": [
        {"ancho": 7.2, "bloques": [{
            "tipo": "bullets", "letra": 14, "items": [
                "Solo se amplían los 34 corredores del modelo (29 de red y 5 enlaces PDGE); no se crean corredores entre otras zonas. "
                "El único de red sin capacidad inicial, Kimal 500 – Alto Jahuel 500, nace con el HVDC en 2030",
                "Ampliación continua, en MW por corredor y período, sin proyectos discretos",
                f"Costo lineal: costo de inversión de la PELP por corredor ({fmt(cmin)} a {fmt(cmax)} USD/MW), "
                f"anualizado a {vida} años y {fmt(r_ * 100)} % (factor {fmt(crf, 4)}), sin O&M",
                "Obras comprometidas forzadas: HVDC Kimal–Lo Aguirre (2.000 MW) y Río Malleco – Pichirropulli (660 MW), en 2030",
                "Tope acumulado por período: suma de los candidatos de la PELP disponibles hasta ese período (entran en 2025, 2035, 2040 y 2050)",
                "Modelo de transporte sin pérdidas: el flujo en cada sentido no supera la capacidad; sin leyes de Kirchhoff",
            ]}]},
        {"ancho": 4.48, "bloques": [
            {"tipo": "texto", "texto": "Tope acumulado de ampliación (MW)", "letra": 12},
            {"tipo": "tabla", "header": HDR_EJ, "filas": filas_ej, "anchos": [1.2, 1.78, 1.5], "letra": 12, "derecha": [1, 2]},
            {"tipo": "texto", "gris": True, "letra": 12, "texto":
                f"HVDC: Kimal 500 – Alto Jahuel 500. Típico: {len(tip_corr)} de los 28 corredores de red ampliables."},
        ]},
    ],
    "fuente": FUENTE_TX,
    "notas": (
        "Siglas: PDGE, polos de desarrollo de generación eléctrica; HVDC, enlace de corriente continua en alta tensión; "
        "O&M, operación y mantenimiento; PELP, Planificación Energética de Largo Plazo 2023–2027.\n"
        "La obra comprometida es un mínimo del período en que entra (incremental); el tope es acumulado, para que un "
        "mismo candidato no se construya una vez por período.\n"
        f"Anualidad: {fmt(cmin * crf)} a {fmt(cmax * crf)} USD/MW-año. Los enlaces PDGE cuestan 1 USD/MW, como en la PELP.\n"
        "El modelo cobra también la anualidad de la capacidad existente y comprometida; es un costo constante que se "
        "cancela al comparar casos.\n"
        "Transporte: en la red de la PELP 2028–2032, un modelo de transporte deja pasar 20–40 % más flujo norte–centro "
        "que un flujo DC; abastecer la Región Metropolitana sale más barato de lo que es."),
}
v("Transmisión", "20–40 % más flujo norte–centro con transporte (solo notas)", "DATOS_Y_SUPUESTOS §9, Limitaciones")
v("Transmisión", "Kimal 500 – Alto Jahuel 500 nace con el HVDC en 2030",
  "`existing_trans_cap` = 0 y `max_build_mw` = 0 en 2025 y 2027; `min_build_mw` = `max_build_mw` = 2.000 en 2030")
v("Transmisión", "«Típico» de la tabla de ejemplo", "patrón más frecuente de `max_build_mw` (ver arriba)")
v("Transmisión", "HVDC: tope acumulado " + " / ".join(fmt(hvdc[p][1]) for p in PERIODOS) + " MW; mínimo 2.000 en 2030",
  "`trans_build_limits.csv`, filas de `Kimal500_AltoJahuel500`")

LAM_TX = [tx1, tx2, tx3]

# ================================================================== 2. DATA CENTERS: escenarios
def leer_dc(caso):
    d = os.path.join(CASOS, caso, "inputs")
    base = defaultdict(dict)
    for r in leer(os.path.join(d, "dc_base.csv")):
        base[r["DC_ZONE"]][int(r["PERIOD"])] = float(r["dc_base_mw"])
    fijo = defaultdict(dict)
    for r in leer(os.path.join(d, "dc_fijo.csv")):
        fijo[r["LOAD_ZONE"]][int(r["PERIOD"])] = float(r["dc_fijo_mw"])
    libre = {int(r["PERIOD"]): float(r["dc_libre_mw"]) for r in leer(os.path.join(d, "dc_libre.csv"))}
    return base, fijo, libre


DC = {c: leer_dc(c) for c in CASOS_DC}
esc = defaultdict(dict)   # resumen del script de escenarios (CEN, E2 y N1): «agregado_al_modelo_mw», a 0,1 MW
with open(RESUMEN_DC, encoding="utf-8") as f:
    filas_res = list(csv.reader(f))
cols_res = list(zip(filas_res[0], filas_res[1]))
for fila in filas_res[3:]:
    for (medida, escn), x in zip(cols_res[1:], fila[1:]):
        if medida == "agregado_al_modelo_mw":
            esc[escn][int(fila[0])] = float(x)

tray = {}
for c in CASOS_DC:
    base, fijo, libre = DC[c]
    tot = {}
    for p in PERIODOS:
        sb = sum(base[z].get(p, 0) for z in base)
        sf = sum(fijo[z].get(p, 0) for z in fijo)
        assert abs(sb - libre[p]) < 1e-3, (c, p, sb, libre[p])
        tot[p] = libre[p] + sf
        if c in esc:
            assert abs(round(tot[p], 1) - esc[c][p]) < 0.051, (c, p, tot[p], esc[c][p])
    tray[c] = tot
    check(True, f"{c}: suma de dc_base = dc_libre en los 7 períodos"
          + (" y dc_libre + dc_fijo = resumen de escenarios" if c in esc else ""))
    v("Data centers", f"{c}: " + " / ".join(fmt(tot[p], 1) for p in PERIODOS) + " MW medios",
      "por período: `dc_libre_mw` + suma de `dc_fijo_mw` de las zonas (inputs nuevos); igual a la suma de `dc_base_mw` + fija"
      + ("; igual a `agregado_al_modelo_mw` de `resumen_escenarios_dc.csv`" if c in esc else ""))
fija_propio = {p: sum(DC["PROPIO"][1][z].get(p, 0) for z in DC["PROPIO"][1]) for p in PERIODOS}
v("Data centers", "Propio, fija: " + " / ".join(fmt(fija_propio[p], 1) for p in PERIODOS),
  "suma de `dc_fijo_mw` de PROPIO por período")

# Reconstrucción independiente de las trayectorias anuales (sección 8 + cambio del 17-nov-2026)
EXIST = 99.0
CRECE_CEN, CRECE_PROPIO = 0.05, 0.08


def prom(serie, p):
    anios = range(p, FIN_PERIODO[p] + 1)
    return sum(serie(a) for a in anios) / len(anios)


def pelp_rmv(a):  # RM + Valparaíso, MW medios: 99 (2025 y 2026), 297 (2030), 364 (2035), 450 (2057), lineal
    pts = [(2025, 99.0), (2026, 99.0), (2030, 297.0), (2035, 364.0), (2057, 450.0)]
    for (a0, y0), (a1, y1) in zip(pts, pts[1:]):
        if a0 <= a <= a1:
            return y0 + (y1 - y0) * (a - a0) / (a1 - a0)
    raise ValueError(a)


def n1_kimal(a):
    return min(750.0, 75.0 * (a - 2025))


CEN_CAP = {2025: 398, 2026: 552, 2027: 642, 2028: 963, 2029: 1281, 2030: 1381}


def cen_cap(a):  # proyección del CEN hasta 2030; desde 2031 crece 5 % anual
    return CEN_CAP[a] if a <= 2030 else 1381 * (1 + CRECE_CEN) ** (a - 2030)


def cen_medios(a):  # 50 % de la capacidad, escalada a RM + Valparaíso = 1.225 + 155 = 1.380
    return 0.5 * cen_cap(a) * 1380 / 1381


for p in PERIODOS:
    assert abs(max(0.0, prom(pelp_rmv, p) - EXIST) - tray["PELP_E2"][p]) < 1e-3, p
    assert abs(max(0.0, prom(pelp_rmv, p) - EXIST) + prom(n1_kimal, p) - tray["PELP_N1"][p]) < 1e-3, p
    assert abs(prom(cen_medios, p) - EXIST - tray["CEN"][p]) < 1e-3, (p, prom(cen_medios, p) - EXIST, tray["CEN"][p])
check(True, "E2, N1 y CEN reconstruidos desde las trayectorias anuales (promedio por período − 99), con CEN +5 %/año desde 2031")
v("Data centers", "reconstrucción de E2, N1 y CEN",
  "E2: RM+Valparaíso 99 (2025 y 2026), 297 (2030), 364 (2035), 450 (2057) MW medios con interpolación lineal; promedio de los años "
  "del período − 99. N1: E2 + 75 MW medios por año desde 2026 hasta 750. CEN: 398, 552, 642, 963, 1.281 y 1.381 MW de "
  "capacidad en 2025–2030 y 1.381 × 1,05^(año − 2030) desde 2031 (`CRECIMIENTO_CEN` del script de escenarios), × 50 % × 1.380/1.381 "
  "(reparto RM 1.225 + Valparaíso 155), − 99. Coinciden con `dc_libre.csv` a 10⁻³ MW")

# Reparto por zona
e2b = DC["PELP_E2"][0]
check(tray["PELP_E2"][2025] == 0 and all(abs(e2b["Polpaico500"][p] / tray["PELP_E2"][p] - 0.85) < 1e-6 for p in PERIODOS[1:]),
      "E2: 0 en 2025 (sin crecimiento sobre los 99 existentes); 85 % Polpaico500 y 15 % Quillota500 desde 2027")
n1b = DC["PELP_N1"][0]
check([n1b["Kimal220"][p] for p in PERIODOS] == [37.5, 225.0, 525.0, 750.0, 750.0, 750.0, 750.0]
      and all(abs(n1b["Polpaico500"][p] - e2b["Polpaico500"][p]) < 1e-9 for p in PERIODOS),
      "N1 = E2 + Kimal220 (37,5 / 225 / 525 / 750 MW medios)")
cenb = DC["CEN"][0]
for p in PERIODOS:
    assert abs(cenb["Polpaico500"][p] - (prom(lambda a: 0.5 * cen_cap(a) * 1225 / 1381, p) - 84.15)) < 1e-3, p
    assert abs(cenb["Quillota500"][p] - (prom(lambda a: 0.5 * cen_cap(a) * 155 / 1381, p) - 14.85)) < 1e-3, p
check(True, "CEN por zona: Polpaico500 = capacidad × 1.225/1.381 × 50 % − 84,15 y Quillota500 = × 155/1.381 × 50 % − 14,85")
v("Data centers", "E2 85 % / 15 %; N1 + Kimal 220; CEN RM 1.225 MW y Valparaíso 155 MW (al 2030)",
  "cocientes de `dc_base_mw` por zona; CEN: promedio de capacidad × 1.225/1.381 (o 155/1.381) × 0,5, − 84,15 (o − 14,85)")

# ================================================================== 3. PROPIO: catastro
# Columnas del catastro que usa el anexo y su nombre en datos/campus_escenario_propio.csv
COL_CSV = OrderedDict([
    ("ID solicitud CEN", "id_solicitud_cen"), ("Grupo (catastro)", "grupo_catastro"),
    ("Proyecto (nombre CEN)", "proyecto_cen"), ("Subestación de conexión", "subestacion_conexion"),
    ("Tensión (kV)", "tension_kv"), ("Comuna", "comuna"), ("Potencia / demanda solicitada (MW)", "potencia_mw"),
    ("Fecha estimada de conexión", "fecha_estimada_conexion"), ("Categoría estado", "categoria_estado"),
])
TOTAL_CRONOGRAMA = (35, 4233.4)  # fila «Total» de la hoja «Cronograma MW»: solicitudes y MW
mw = lambda s: float(s["Potencia / demanda solicitada (MW)"] or 0)

if os.path.exists(CATASTRO):
    import openpyxl  # solo hace falta con el catastro privado
    FUENTE_CATASTRO = "xlsx"
    wb = openpyxl.load_workbook(CATASTRO, read_only=True, data_only=True)
    ws = wb["Solicitudes CEN"]
    rows = list(ws.iter_rows(values_only=True))
    H = {k: i for i, k in enumerate(rows[0])}
    sol = [dict(zip(rows[0], r)) for r in rows[1:] if r[0] is not None]
    cron = list(wb["Cronograma MW"].iter_rows(values_only=True))
    cat = list(wb["Catastro DC"].iter_rows(values_only=True, min_row=5))
    nombre_grupo = {r[0]: r[1] for r in cat if r[0] and str(r[0]).startswith("G")}
    wb.close()

    vig = [s for s in sol if s["Vigente"] == "Sí"]
    con_fecha = [s for s in vig if isinstance(s["Fecha estimada de conexión"], dt.datetime)]
    sin_fecha = [s for s in vig if not isinstance(s["Fecha estimada de conexión"], dt.datetime)]
    tot_cron = [r for r in cron if r[0] == "Total"][0]
    check((tot_cron[1], round(tot_cron[2], 1)) == TOTAL_CRONOGRAMA, "fila Total de «Cronograma MW» = 35 solicitudes y 4.233,4 MW")
    check(len(sin_fecha) == 2 and abs(sum(mw(s) for s in sin_fecha) - 16.6) < 1e-6,
          "2 vigentes sin fecha (alimentadores ODATA, 16,6 MW), fuera del cronograma")
else:
    FUENTE_CATASTRO = "csv"
    print("     catastro no encontrado; se leen las filas ya extraídas de", os.path.relpath(CAMPUS_CSV, REPO))
    con_fecha = []
    for r in leer(CAMPUS_CSV):
        s = {orig: r[col] for orig, col in COL_CSV.items()}
        s["ID solicitud CEN"] = int(s["ID solicitud CEN"])
        s["Tensión (kV)"] = float(s["Tensión (kV)"])
        s["Potencia / demanda solicitada (MW)"] = float(s["Potencia / demanda solicitada (MW)"]) if s["Potencia / demanda solicitada (MW)"] else None
        s["Fecha estimada de conexión"] = dt.datetime.strptime(s["Fecha estimada de conexión"], "%Y-%m-%d")
        s["_clase_csv"] = r["clase"]
        con_fecha.append(s)
    tot_cron = ("Total",) + TOTAL_CRONOGRAMA

check(len(con_fecha) == tot_cron[1] == 35 and abs(sum(mw(s) for s in con_fecha) - tot_cron[2]) < 1e-6,
      f"35 solicitudes vigentes con fecha = {fmt(tot_cron[2], 1)} MW, igual a la hoja Cronograma MW")

# Regla 1: existentes (conexión hasta 2025)
exist = [s for s in con_fecha if s["Fecha estimada de conexión"].year <= 2025]
mw_exist = sum(mw(s) for s in exist)
check(len(exist) == 12 and abs(mw_exist - 428.4) < 1e-6, f"regla 1: {len(exist)} solicitudes existentes, {fmt(mw_exist, 1)} MW")
nuevas = [s for s in con_fecha if s["Fecha estimada de conexión"].year >= 2026]

# Regla 2: un campus, una vez. Repetida = mismo grupo, misma S/E y misma fecha que otra solicitud (se conserva la de menor ID
# con MW; se descarta la otra). Se comprueba que son exactamente las dos que nombra la sección 8.5.
def se_norm(s):
    t = s["Subestación de conexión"].lower()
    t = re.sub(r"\b(s/e|se|seccionadora|kv)\b", " ", t)
    return re.sub(r"\s+", " ", re.sub(r"\d+", " ", t)).strip()


claves = defaultdict(list)
for s in nuevas:
    claves[(s["Grupo (catastro)"], se_norm(s), s["Fecha estimada de conexión"])].append(s)
repetidas = []
for k, ss in claves.items():
    if len(ss) > 1:
        # Repite a otra si además tiene la misma potencia o no informa MW (distinta potencia = otro edificio,
        # como DC Valparaíso 1 y 2). Se conserva la de MW informado y, entre iguales, la de mayor ID.
        ss = sorted(ss, key=lambda s: (-mw(s), -s["ID solicitud CEN"]))
        for s in ss[1:]:
            if mw(s) == 0 or mw(s) == mw(ss[0]):
                repetidas.append(s)
ids_rep = sorted(s["ID solicitud CEN"] for s in repetidas)
check(ids_rep == [2718, 2853], f"regla 2: repetidas {ids_rep} (ACS Santiago I alim. 2, 14 MW; Ascenty SCL4 detenida, sin MW)")
mw_rep = sum(mw(s) for s in repetidas)
nuevas = [s for s in nuevas if s not in repetidas]
sin_mw = [s for s in nuevas if not s["Potencia / demanda solicitada (MW)"]]
check(sorted(s["ID solicitud CEN"] for s in sin_mw) == [2711, 2740], "2 vigentes sin MW informado (2711 y 2740), fuera")
incl = [s for s in nuevas if s not in sin_mw]
mw_incl = sum(mw(s) for s in incl)
check(len(incl) == 19 and abs(mw_incl - 3791) < 1e-6, f"19 solicitudes nuevas incluidas, {fmt(mw_incl)} MW")
check(abs(mw_exist + mw_rep + mw_incl - tot_cron[2]) < 1e-6, "existentes + repetidas + sin MW + incluidas = 4.233,4 MW del cronograma")

# Filas del catastro que usa el escenario PROPIO: las 35 vigentes con fecha, con la clase que les dan las reglas 1 y 2.
clase = {}
for nombre, grupo in [("existente", exist), ("repetida", repetidas), ("sin_mw", sin_mw), ("incluida", incl)]:
    for s_ in grupo:
        clase[s_["ID solicitud CEN"]] = nombre
if FUENTE_CATASTRO == "xlsx":
    os.makedirs(DATOS, exist_ok=True)
    with open(CAMPUS_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["clase"] + list(COL_CSV.values()))
        for s_ in sorted(con_fecha, key=lambda s_: (s_["Fecha estimada de conexión"], s_["ID solicitud CEN"])):
            fila = []
            for orig in COL_CSV:
                x = s_[orig]
                if isinstance(x, dt.datetime):
                    x = f"{x:%Y-%m-%d}"
                elif isinstance(x, float) and x.is_integer():
                    x = int(x)
                fila.append("" if x is None else x)
            w.writerow([clase[s_["ID solicitud CEN"]]] + fila)
    print("     escrito", os.path.relpath(CAMPUS_CSV, REPO))
else:
    check(all(clase[s_["ID solicitud CEN"]] == s_["_clase_csv"] for s_ in con_fecha),
          "la clase de cada fila de campus_escenario_propio.csv coincide con la que dan las reglas 1 y 2")
v("Propio", f"4.233,4 MW = 428,4 existentes + {fmt(mw_rep)} repetidos + 0 sin MW + {fmt(mw_incl)} incluidos",
  "hoja «Solicitudes CEN» del catastro, Vigente = «Sí» y con fecha estimada (35 solicitudes, igual a la fila Total de «Cronograma MW»); "
  "regla 1: año ≤ 2025; regla 2: mismo grupo, misma S/E, misma fecha y misma potencia o sin MW (IDs 2853 y 2718; DC Valparaíso 1 y 2 tienen 200 y 100 MW: dos edificios); sin MW: IDs 2711 y 2740")

# Subestación legible y zona (tabla «Ubicación por subestación» de la sección 8.5)
SE = {  # palabra clave normalizada → (nombre legible, zona)
    "chacabuco": ("Chacabuco", "Polpaico500"), "quilicura": ("Quilicura", "Polpaico500"),
    "punta verde": ("Punta Verde", "Polpaico500"), "chicureo": ("Chicureo", "Polpaico500"),
    "nueva lampa": ("Nueva Lampa", "Polpaico500"), "santa teresa": ("Santa Teresa", "Polpaico500"),
    "manuel rodriguez": ("Manuel Rodríguez", "Polpaico500"), "polpaico": ("Polpaico", "Polpaico500"),
    "lo aguirre": ("Lo Aguirre", "AltoJahuel500"), "lo prado": ("Lo Prado", "AltoJahuel500"),
    "bajos de mena": ("Bajos de Mena", "AltoJahuel500"), "odata san bernardo": ("Odata San Bernardo", "AltoJahuel500"),
    "alto jahuel": ("Alto Jahuel", "AltoJahuel500"),
    "la polvora": ("La Pólvora", "Quillota500"),
}


def ubicar(s):
    n = se_norm(s).replace("ó", "o").replace("í", "i")
    hits = [v_ for k, v_ in SE.items() if k.replace("ó", "o").replace("í", "i") == n]
    assert len(hits) == 1, (s["ID solicitud CEN"], s["Subestación de conexión"], n)
    nom, z = hits[0]
    kv = s["Tensión (kV)"]
    return f"{nom} {int(kv)} kV", z


MES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
ESTADO = {"En tramitación": "en tramitación", "Detenida": "detenida",
          "Autorizada (por declarar en construcción)": "autorizada", "Declarada en construcción": "en construcción"}
CORTO = {  # nombre corto por grupo del catastro: proyecto (titular)
    "G01": "Mega Data Center Lampa, etapa 2 (Scala)", "G03": "San Bernardo, ampliación (ODATA)",
    "G09": "SCL4 (Ascenty)", "G10": "Quilicura, dos alimentadores (Scala)", "G15": "Proyecto Rivera (Inmobiliaria STPA)",
    "G16": "Campus Norte, etapa II (Eléc. Chicureo)", "G19": "DC Hermes (Mytilineos)",
    "G20": "Lo Aguirre y Lo Aguirre A (Lader Energy)", "G21": "Noviciado I (Ignis)", "G22": "Pacífico 33-S (Ignis)",
    "G24": "DC Valparaíso 1 y 2 (FR Data)", "G26": "Moreras (Orion Power)", "G27": "SC2 (RTB Energy)",
    "G28": "SC1 (SAE Ladera Sur)", "G29": "DC Santiago I y II (ACS)",
}
grupos = OrderedDict()
for s in sorted(incl, key=lambda s: (s["Fecha estimada de conexión"], -mw(s))):
    se, z = ubicar(s)
    g = s["Grupo (catastro)"]
    grupos.setdefault(g, []).append(dict(id=s["ID solicitud CEN"], se=se, zona=z, mw=mw(s), fecha=s["Fecha estimada de conexión"],
                                         estado=ESTADO[s["Categoría estado"]], nombre=s["Proyecto (nombre CEN)"]))
check(set(grupos) == set(CORTO), f"{len(grupos)} campus (grupos del catastro) con solicitudes incluidas")


def unir(xs):
    u = list(OrderedDict.fromkeys(xs))
    return y_lista(u)


def se_unir(ss):
    # «Chacabuco 23 kV y Quilicura 23 kV» → «Chacabuco y Quilicura 23 kV» si comparten tensión
    u = list(OrderedDict.fromkeys(ss))
    kvs = {x.rsplit(" ", 2)[1] for x in u}
    if len(u) > 1 and len(kvs) == 1:
        return y_lista([x.rsplit(" ", 2)[0] for x in u]) + " " + kvs.pop() + " kV"
    return y_lista(u)


campus = []
for g, ss in grupos.items():
    zonas = {x["zona"] for x in ss}
    assert len(zonas) == 1, g
    campus.append(dict(
        g=g, nombre=CORTO[g], se=se_unir(x["se"] for x in ss), zona=zonas.pop(), mw=sum(x["mw"] for x in ss),
        estado=unir(x["estado"] for x in ss).capitalize(),
        fecha=unir(f"{MES[x['fecha'].month - 1]}-{x['fecha'].year}" for x in ss), anio=min(x["fecha"] for x in ss),
        detalle="; ".join(f"CEN {x['id']} «{x['nombre']}», {x['se']}, {fmt(x['mw'])} MW, {x['fecha']:%d-%m-%Y}, {x['estado']}" for x in ss)))
# Cirion SAN2: catálogo propio (sección 8.5, regla 3): Quilicura, 20 MW en 2026, distribución → Polpaico500
campus.append(dict(g="Catálogo", nombre="SAN2 (Cirion)", se="Distribución (Quilicura)", zona="Polpaico500", mw=20.0,
                   estado="Sin solicitud al CEN", fecha="2026", anio=dt.datetime(2026, 1, 1),
                   detalle="catálogo propio; DATOS_Y_SUPUESTOS §8.5, regla 3: Quilicura, 20 MW en 2026, conexión en distribución"))
mw_sol = sum(c["mw"] for c in campus)
check(abs(mw_sol - 3811) < 1e-6 and len(campus) == 16, f"16 campus, {fmt(mw_sol)} MW solicitados")
por_zona = defaultdict(float)
for c in campus:
    por_zona[c["zona"]] += c["mw"]
check({k: round(x, 6) for k, x in por_zona.items()} == {"Polpaico500": 1648.0, "AltoJahuel500": 1363.0, "Quillota500": 800.0},
      "por zona: Polpaico500 1.648, AltoJahuel500 1.363, Quillota500 800 MW solicitados (tabla de la sección 8.5)")
n_se = len({x["se"].rsplit(" ", 2)[0] for ss in grupos.values() for x in ss})
check(n_se == 14, f"{n_se} subestaciones de conexión distintas (sin contar la conexión en distribución de Cirion)")
v("Propio (tabla)", "Estado y fecha estimada de cada campus",
  "columnas «Categoría estado» (En tramitación, Detenida, Autorizada (por declarar en construcción) → autorizada, "
  "Declarada en construcción → en construcción) y «Fecha estimada de conexión» de cada solicitud incluida; "
  "S/E y tensión desde «Subestación de conexión» y «Tensión (kV)»; zona según la tabla de ubicación de §8.5")
for c in campus:
    v("Propio (tabla)", f"{c['nombre']}: {fmt(c['mw'])} MW, {c['zona']}", c["detalle"])

# Trayectoria: 50 % de los MW solicitados, desde el año de conexión (año completo), promedio por período
ULTIMO = 2032
LLENADO = 115.2


def solicitado(a, z=None):  # MW medios de lo solicitado, acumulado al año a (0 en 2025)
    return 0.5 * sum(x["mw"] for ss in grupos.values() for x in ss if (z is None or x["zona"] == z) and x["fecha"].year <= a) \
        + (0.5 * 20.0 * (a >= 2026) if z in (None, "Polpaico500") else 0)


total_2032 = EXIST + LLENADO + solicitado(ULTIMO)


def propio_anual(a, z=None):  # desde 2033 la demanda total de data centers crece 8 % anual; el aumento es ubicable
    if a <= ULTIMO:
        return solicitado(a, z)
    cuota = 1.0 if z is None else solicitado(ULTIMO, z) / solicitado(ULTIMO)
    return solicitado(ULTIMO, z) + total_2032 * ((1 + CRECE_PROPIO) ** (a - ULTIMO) - 1) * cuota


anual = {a: propio_anual(a) for a in range(2025, 2055)}
check([anual[a] for a in range(2025, 2033)] == [0, 16, 22, 454, 698, 1448, 1755.5, 1905.5],
      "MW medios acumulados 2025–2032: 0, 16, 22, 454, 698, 1.448, 1.755,5, 1.905,5 (tabla de la sección 8.5)")
check(abs(total_2032 - 2119.7) < 1e-9, "base del crecimiento: 99 + 115,2 + 1.905,5 = 2.119,7 MW medios en 2032")
libre_p = DC["PROPIO"][2]
for p in PERIODOS:
    assert abs(prom(lambda a: anual[a], p) - libre_p[p]) < 2e-3, (p, prom(lambda a: anual[a], p), libre_p[p])
check(True, "promedio por período de la trayectoria anual (con +8 %/año desde 2033) = dc_libre de PROPIO, a 2·10⁻³ MW")
basep = DC["PROPIO"][0]
for z in ["Polpaico500", "AltoJahuel500", "Quillota500"]:
    for p in PERIODOS:
        assert abs(prom(lambda a: propio_anual(a, z), p) - basep[z][p]) < 2e-3, (z, p)
check(True, "reparto por zona y período = dc_base de PROPIO (el aumento desde 2033 se reparte como lo solicitado en 2032)")
v("Propio", "MW medios = 50 % de los MW solicitados; +8 %/año desde 2033",
  "carga plana desde el año de la fecha estimada (año completo); acumulado anual 0 (2025), 16 … 1.905,5 (2032); "
  "desde 2033, + 2.119,7 × (1,08^(año − 2032) − 1), repartido como lo solicitado en 2032 (`CRECIMIENTO` del script del "
  "escenario propio); promedio de los años del período = `dc_libre.csv` (" + "; ".join(fmt(libre_p[p], 1) for p in PERIODOS)
  + ") y, por zona, `dc_base.csv`")

# Llenado de los campus existentes: 428,4 × 50 % − 99 = 115,2, repartido por MW conectados
fill = 0.5 * mw_exist - EXIST
pol_ex = sum(mw(s) for s in exist if s["Comuna"] in ("Lampa", "Colina", "Quilicura"))
aj_ex = sum(mw(s) for s in exist if s["Comuna"] in ("San Bernardo", "Padre Hurtado"))
check(abs(pol_ex + aj_ex - mw_exist) < 1e-6, f"existentes: {fmt(pol_ex, 1)} MW en Lampa/Colina/Quilicura y {fmt(aj_ex)} en San Bernardo/Padre Hurtado")
fp, fa = fill * pol_ex / mw_exist, fill * aj_ex / mw_exist
fijo = DC["PROPIO"][1]
check(abs(fill - 115.2) < 1e-9 and abs(fijo["Polpaico500"][2030] - fp) < 1e-4 and abs(fijo["AltoJahuel500"][2030] - fa) < 1e-4,
      f"llenado {fmt(fill, 1)} MW medios = {fmt(fp, 2)} Polpaico500 + {fmt(fa, 2)} AltoJahuel500 (dc_fijo 2030)")
rampas = {p: prom(lambda a: fill * min(1.0, max(0.0, 0.2 * (a - 2025))), p) for p in PERIODOS}
check(all(abs(rampas[p] - fija_propio[p]) < 1e-3 for p in PERIODOS),
      f"rampa 20 %/año desde 2026: promedio 2025–2026 = {fmt(rampas[2025], 2)} y 2027–2029 = {fmt(rampas[2027], 2)} MW medios; "
      "115,2 desde 2030")
v("Propio", f"llenado {fmt(fill, 1)} = 428,4 × 50 % − 99; {fmt(fp, 1)} Polpaico 500 y {fmt(fa, 1)} Alto Jahuel 500; "
  f"{fmt(rampas[2025], 1)} en 2025–2026 y {fmt(rampas[2027], 1)} en 2027–2029",
  "MW de las 12 existentes por comuna (Lampa, Colina, Quilicura → Polpaico500; San Bernardo, Padre Hurtado → AltoJahuel500); "
  "rampa 0, 20, 40, 60 y 80 % en 2025–2029; coincide con `dc_fijo.csv`")

# ------------------------------------------------------------------ láminas de data centers
ZL = {"Polpaico500": "Polpaico 500", "AltoJahuel500": "Alto Jahuel 500", "Quillota500": "Quillota 500", "Kimal220": "Kimal 220"}
pct_e2 = round(100 * e2b["Polpaico500"][2050] / tray["PELP_E2"][2050])
dc1 = {
    "titulo": "Anexo: escenarios de data centers",
    "subtitulo": "Origen, ubicación base y carga media que cada escenario agrega al modelo",
    "columnas": [{"ancho": 12.13, "bloques": [
        {"tipo": "tabla", "letra": 12, "anchos": [1.1, 3.3, 1.85, 5.88],
         "header": ["Escenario", "Origen", "Paso a MW medios", "Nodo o subestación → zona del modelo"],
         "filas": [
             ["PELP E2", "PELP 2028–2032, escenario E2", "Carga de la PELP",
              f"El Salto 220 kV → Polpaico 500 ({pct_e2} %); Torquemada 110 kV → Quillota 500 ({100 - pct_e2} %)"],
             ["CEN", "Proyección de demanda 2026–2046 del CEN", "50 % de la capacidad",
              "RM → Polpaico 500 (1.225 MW); Valparaíso → Quillota 500 (155 MW), al 2030"],
             ["PELP N1", "PELP 2028–2032, escenario N1", "Carga de la PELP", f"Como E2, más Kimal 220 kV → Kimal 220 ({fmt(n1b['Kimal220'][2035])} MW medios desde 2035)"],
             ["Propio", "Solicitudes de conexión vigentes al CEN", "50 % de lo solicitado",
              "Subestaciones de conexión → Polpaico 500, Alto Jahuel 500 y Quillota 500"],
         ]},
        {"tipo": "tabla", "letra": 12, "anchos": [2.33] + [1.4] * 7, "derecha": [1, 2, 3, 4, 5, 6, 7],
         "header": ["MW medios agregados"] + [str(p) for p in PERIODOS],
         "filas": [[lab] + [fmt(vals[p], 1) for p in PERIODOS] for lab, vals in [
             ("PELP E2", tray["PELP_E2"]), ("CEN", tray["CEN"]), ("PELP N1", tray["PELP_N1"]),
             ("Propio", tray["PROPIO"]), ("Propio, de ella fija", fija_propio)]]},
        {"tipo": "texto", "letra": 12, "gris": True, "texto":
            "Carga por encima de los ~99 MW medios de data centers que ya están en la demanda. Cada período usa el promedio "
            "de la trayectoria anual en sus años (2025 = 2025–2026; 2050 = 2050–2054). Después de su horizonte, CEN crece "
            "5 % anual desde 2031 y Propio 8 % anual desde 2033; E2 y N1 traen su propio crecimiento."},
    ]}],
    "fuente": FUENTE_DC,
    "notas": (
        "Siglas: PELP, Planificación Energética de Largo Plazo; CEN, Coordinador Eléctrico Nacional; RM, Región "
        "Metropolitana; S/E, subestación; MW medios, potencia media anual (carga plana).\n"
        "PELP E2 y N1: la PELP 2028–2032 trae los data centers como cargas planas en nodos de su red de 234 nodos. "
        "RM + Valparaíso: 99 MW medios en 2025 y 2026, 297 en 2030, 364 en 2035 y 450 en 2057, siempre 85 % / 15 %. "
        "N1 agrega Antofagasta (S/E Kimal 220 kV): 75 MW medios más por año desde 2026 hasta 750 en 2035. "
        "El Salto queda casi en empate entre Polpaico 500 y Alto Jahuel 500; se asigna a Polpaico 500 por su línea de 220 kV y la distancia.\n"
        "CEN: capacidad identificada de 398 MW en 2025, 552 en 2026, 642 en 2027, 963 en 2028, 1.281 en 2029 y 1.381 en 2030, "
        "con 50 % de utilización; reparto RM 1.225 MW y Valparaíso 155 MW. La proyección llega a 2030; desde 2031 la "
        f"capacidad crece 5 % anual (supuesto conservador), hasta {fmt(cen_cap(2054))} MW en 2054.\n"
        f"Propio: 3.811 MW solicitados = 1.905,5 MW medios en 2032, más 115,2 MW medios fijos por el llenado de "
        f"campus ya conectados ({fmt(fija_propio[2025], 1)} en promedio en 2025–2026 y {fmt(fija_propio[2027], 1)} en "
        f"2027–2029). Desde 2033 la demanda total de data centers (99 + 115,2 + 1.905,5 = {fmt(total_2032, 1)} MW medios "
        "en 2032) crece 8 % anual; el aumento es carga nueva y ubicable, con ubicación base en proporción a lo solicitado.\n"
        "Se descuentan los ~99 MW medios existentes: 84,15 en Polpaico 500 y 14,85 en Quillota 500. En el caso libre, "
        "el modelo puede mover desde 2030 todo lo que no es fijo; antes de 2030 la ubicación es la base."),
}

HDR_C = ["Campus (titular)", "Subestación", "Zona del modelo", "MW solic.", "Estado (CEN)", "Fecha estimada"]
ANCH_C = [3.15, 2.85, 1.35, 0.9, 2.2, 1.68]


def filas_campus(zonas):
    sel = [c for c in campus if c["zona"] in zonas]
    sel.sort(key=lambda c: (zonas.index(c["zona"]), c["anio"], c["nombre"]))
    return [[c["nombre"], c["se"], ZL[c["zona"]], fmt(c["mw"]), c["estado"], c["fecha"]] for c in sel]


f_pol = filas_campus(["Polpaico500"]) + [["Total Polpaico 500", "", "", fmt(por_zona["Polpaico500"]), "", ""]]
f_resto = filas_campus(["AltoJahuel500", "Quillota500"]) + [["Total de los 16 campus", "", "", fmt(mw_sol), "", ""]]
dc2 = {
    "titulo": "Anexo: escenario propio, campus (1/2)",
    "subtitulo": "Campus con solicitud de conexión vigente desde 2026, uno por fila: zona Polpaico 500",
    "columnas": [{"ancho": 12.13, "bloques": [
        {"tipo": "tabla", "letra": 12, "anchos": ANCH_C, "derecha": [3], "total": True, "header": HDR_C, "filas": f_pol},
        {"tipo": "bullets", "letra": 12, "items": [
            f"Fuera: {len(exist)} solicitudes con conexión hasta 2025 ({fmt(mw_exist, 1)} MW, ya en la demanda), 2 que repiten "
            f"otra del mismo campus ({fmt(mw_rep)} MW) y 2 que no informan MW",
            "Cirion SAN2 se conecta en distribución y no figura en el CEN; los anuncios sin año de conexión no se consideran",
        ]},
    ]}],
    "fuente": FUENTE_DC,
    "notas": (
        "Siglas: CEN, Coordinador Eléctrico Nacional; S/E, subestación; MW solic., MW solicitados en la solicitud de conexión.\n"
        "Base: catastro de solicitudes de conexión de data centers a la plataforma de Acceso Abierto del CEN, al 13-nov-2026, "
        "con las vigentes (no rechazadas ni desistidas) con fecha estimada de conexión: 35 solicitudes, 4.233,4 MW.\n"
        "Un campus aparece una vez. Quilicura (Scala) son dos alimentadores en S/E distintas (12 + 12 MW, 2026 y 2027); "
        "DC Santiago I y II (ACS) son dos edificios (14 + 40 MW). Las repetidas son el segundo alimentador de 14 MW de "
        "DC Santiago I (misma S/E y fecha) y una solicitud detenida de SCL4 sin MW.\n"
        "Zona: la barra de 500/220 kV que abastece la subestación de conexión. SC1 y SC2 tienen distinto titular, "
        "subestación y potencia, y se cuentan como dos campus.\n"
        "Las 2 solicitudes vigentes sin fecha (alimentadores de ODATA, 16,6 MW) son obras de 2022 de un campus existente.\n"
        "Es una cota superior: toma toda la cartera vigente, sin probabilidad de realización."),
}
dc3 = {
    "titulo": "Anexo: escenario propio, campus (2/2)",
    "subtitulo": "Campus con solicitud de conexión vigente desde 2026: zonas Alto Jahuel 500 y Quillota 500",
    "columnas": [{"ancho": 12.13, "bloques": [
        {"tipo": "tabla", "letra": 12, "anchos": ANCH_C, "derecha": [3], "total": True, "header": HDR_C, "filas": f_resto},
        {"tipo": "bullets", "letra": 12, "items": [
            f"MW medios = 50 % de los MW solicitados, como carga plana desde el año estimado de conexión: {fmt(mw_sol)} MW "
            f"solicitados dan {fmt(0.5 * mw_sol, 1)} MW medios en 2032 ({fmt(0.5 * por_zona['Polpaico500'])} en Polpaico 500, "
            f"{fmt(0.5 * por_zona['AltoJahuel500'], 1)} en Alto Jahuel 500 y {fmt(0.5 * por_zona['Quillota500'])} en Quillota 500); "
            "desde 2033 el total de data centers crece 8 % anual",
            f"Llenado de los campus ya conectados: {fmt(mw_exist, 1)} MW × 50 % − 99 = {fmt(fill, 1)} MW medios fijos "
            f"({fmt(fp, 1)} en Polpaico 500 y {fmt(fa, 1)} en Alto Jahuel 500), con rampa de 20 % por año hasta 2030",
        ]},
    ]}],
    "fuente": FUENTE_DC,
    "notas": (
        "Lo Aguirre secciona la línea Polpaico–Alto Jahuel y queda casi en empate eléctrico entre ambas zonas; va a Alto Jahuel 500 "
        "porque la red de la PELP 2023–2027 lleva ahí el terminal del HVDC Kimal–Lo Aguirre (HVDC: enlace de corriente continua en alta tensión).\n"
        "Noviciado I y Pacífico 33-S (Ignis) son dos campus: otro nombre, otra comuna y otra región. Lo Aguirre y Lo Aguirre A "
        "(Lader Energy) son 500 + 25 MW en S/E distintas; DC Valparaíso 1 y 2 (FR Data) son 200 + 100 MW en paños distintos.\n"
        "Una fecha dentro de un año cuenta el año completo; cada período del modelo usa el promedio de sus años "
        f"({fmt(libre_p[2025], 1)} MW medios en 2025–2026, {fmt(libre_p[2027], 1)} en 2027–2029 y {fmt(libre_p[2030], 1)} "
        "en 2030–2034, este último ya con el crecimiento de 2033–2034).\n"
        f"Crecimiento: desde 2033, la demanda total de data centers, {fmt(total_2032, 1)} MW medios en 2032 (99 ya en la "
        "demanda, 115,2 de llenado y 1.905,5 solicitados), crece 8 % anual. El aumento se agrega como carga ubicable y "
        f"su ubicación base sigue el reparto de lo solicitado; en 2050–2054 el escenario agrega {fmt(tray['PROPIO'][2050], 1)} "
        "MW medios.\n"
        "Llenado: las conexiones existentes suman 428,4 MW; al 50 % consumirían 214,2 MW medios, frente a los ~99 que "
        "consumen hoy. La diferencia entra fija, en proporción a los MW conectados por zona.\n"
        "En 2030 la cartera suma 2.896 MW solicitados, frente a 1.381 MW que identifica el CEN."),
}
check(abs(0.5 * sum(c["mw"] for c in campus if c["anio"].year <= 2030) - anual[2030]) < 1e-9 and anual[2030] * 2 == 2896,
      "2.896 MW solicitados al 2030 (= 2 × 1.448)")
check(abs(0.5 * mw_exist - 214.2) < 1e-9, "428,4 × 50 % = 214,2 MW medios")

LAM_DC = [dc1, dc2, dc3]

# ================================================================== validación de formato y escritura
for lam in LAM_TX + LAM_DC:
    validar_lamina(lam)

CAB = ("// {} Generado con un script de cálculo; cifras verificadas en verificacion_transmision_dc.md.\n"
       "// Formato: FORMATO.md. Solo datos: build.js dibuja las láminas.\n")
open(os.path.join(OUT, "20_transmision.js"), "w", encoding="utf-8").write(
    a_js(LAM_TX, CAB.format("Anexos de transmisión.")))
open(os.path.join(OUT, "30_data_centers.js"), "w", encoding="utf-8").write(
    a_js(LAM_DC, CAB.format("Anexos de data centers.")))

# ------------------------------------------------------------------ verificación
rel = lambda x: os.path.relpath(x, REPO).replace(os.sep, "/")
md = ["# Verificación de los anexos de transmisión y data centers", "",
      f"Generado el {dt.date.today():%d-%m-%Y} por `anexos_tx_dc.py` (`python -P`, inputs del modelo con inicio en 2025), que calcula todas las cifras "
      "y escribe `20_transmision.js` y `30_data_centers.js`. Cada cifra de las láminas sale de las filas de abajo.", "",
      "## Datos de entrada", "",
      f"- Inputs del modelo (inicio 2025): `{rel(CASOS)}`",
      "  - `SIN_DC/inputs/transmission_lines.csv`, `trans_build_limits.csv`, `trans_params.csv`, `financials.csv`, `periods.csv` "
      "(los de transmisión son idénticos en los 5 casos, comprobado por hash);",
      "  - `<CASO>/inputs/dc_base.csv`, `dc_fijo.csv`, `dc_libre.csv` para PELP_E2, PELP_N1, CEN y PROPIO;",
      f"  - `{rel(RESUMEN_DC)}` (resumen del script de escenarios, copia del modelo);",
      f"  - `{rel(INV_AMEBA_2025)}` y, solo para documentar el cambio, `{rel(CASOS_ANTES_TL)}` (copias del modelo);",
      "  - reglas: `CAMBIO_INICIO_2025.md` del modelo, `DATOS_Y_SUPUESTOS.md` (secciones 6 y 8) del repositorio.",
      "- Repositorio: las rutas de esta lista son relativas a su raíz.",
      ("- Catastro del equipo (privado), solo lectura con openpyxl (`read_only=True, data_only=True`), hojas «Solicitudes CEN», "
       "«Cronograma MW» y «Catastro DC»; sus 35 filas vigentes con fecha quedan en `presentacion/fuente/datos/campus_escenario_propio.csv`."
       if FUENTE_CATASTRO == "xlsx" else
       f"- Catastro del equipo: filas ya extraídas en `{rel(CAMPUS_CSV)}` (el catastro privado no estaba disponible)."),
      f"- Solo para verificar el origen de la capacidad existente: `{rel(LINEAS_AMEBA)}` (trazabilidad de las 161 líneas AMEBA).", "",
      "## Comprobaciones automáticas", "",
      "El script se detiene si falla alguna. Todas pasaron:", ""]
md += [f"- {c}" for c in CHECKS]
md += ["", "## Cifras y su origen", "", "| Sección | Cifra | Cómo se obtuvo |", "|---|---|---|"]
md += [f"| {a} | {b} | {c.replace('|', '/')} |" for a, b, c in VERIF]
md += ["", "## Formato", "",
       "El script comprueba en cada lámina: título ≤ 45 caracteres, subtítulo ≤ 110, anchos de columna (12,13 in o 11,68 in en total), "
       "suma de anchos de cada tabla, alto apilado ≤ 4,8 in (filas de 0,29/0,31 in a 11/12 pt, viñetas y texto con la fórmula de "
       "`build.js`) y que cada celda quepa en una línea (16/14 caracteres por pulgada a 11/12 pt, descontando 0,17 in de márgenes).", "",
       "Altos calculados (in) por lámina y columna:", ""]
md += [f"- {t}: {h}" for t, h in ALTOS]
md += ["", "## Hecho sobre los corredores", "",
       "El modelo solo amplía los 34 corredores de `transmission_lines.csv` (Switch indexa `BuildTx` por esos corredores y "
       "`trans_build_limits.csv` no nombra otros); no crea corredores entre otros pares de zonas. Matiz: de los 29 corredores de "
       "red, 28 tienen capacidad existente; Kimal 500 – Alto Jahuel 500 parte en 0 MW, no puede construirse en 2025 ni en 2027 y nace con la "
       "obra comprometida (HVDC, 2.000 MW en 2030), después de la cual puede ampliarse hasta 6.000 MW acumulados. Los 5 enlaces "
       "PDGE también parten en 0 MW, con tope 99.999 MW. En AMEBA, toda línea candidata o comprometida cae en uno de los 34 corredores, "
       "y el único corredor de red sin línea existente es el del HVDC. Kimal 220 – Los Changos 220 no se puede ampliar.", "",
       "## Observaciones", "",
       f"- Las capacidades de las tablas de corredores se redondean a MW: los 29 existentes redondeados suman {fmt(suma_red)} MW, "
       f"frente al total exacto de {fmt(tot_exist)} MW que se da en el texto.",
       "- El HVDC Kimal–Lo Aguirre figura con 2.000 MW, la capacidad que le asignan los datos de la PELP 2023–2027 y con la que corre "
       "el modelo. Las notas de la lámina de motivación del cuerpo hablan de 3.000 MW (el proyecto); no es un error del anexo, pero "
       "conviene no mezclarlas al responder.",
       "- Campus = grupo «Proyecto / campus» del catastro (15 grupos con solicitudes incluidas) más Cirion SAN2. Cuatro campus agrupan "
       "dos solicitudes que se cuentan ambas (dos alimentadores, dos edificios o dos módulos): Quilicura (Scala), DC Santiago I y II (ACS), "
       "Lo Aguirre y Lo Aguirre A (Lader Energy) y DC Valparaíso 1 y 2 (FR Data). Las 19 solicitudes y sus MW están en la tabla de arriba.",
       "- La regla 2 se aplicó con un criterio explícito (mismo grupo, misma S/E, misma fecha y misma potencia o sin MW), que reproduce "
       "exactamente las dos repetidas que nombra DATOS_Y_SUPUESTOS §8.5.",
       "- Cirion SAN2 no está en el catastro: sus datos (Quilicura, 20 MW, 2026, distribución) salen de DATOS_Y_SUPUESTOS §8.5.", ""]
open(os.path.join(OUT, "verificacion_transmision_dc.md"), "w", encoding="utf-8").write("\n".join(md))
print("escritos los 3 archivos en", rel(OUT))
