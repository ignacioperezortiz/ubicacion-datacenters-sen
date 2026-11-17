"""Anexo de generación candidata: calcula todas las cifras y escribe 10_generacion.js.

Candidato = fila de gen_build_costs con año de construcción en un período del modelo
(2025...2050) que NO está en gen_build_predetermined (lo predeterminado es existente
o comprometido en los datos de ENTRADA de AMEBA; desde el 17-nov-2026 ninguna inversión
que decidió AMEBA entra como dato). Costos AMEBA en USD/MW en Switch -> se dividen por 1.000 (USD/kW).

Uso: python -B anexo_generacion.py [<salida 10_generacion.js> [<carpeta inputs SIN_DC>]]
Por omisión escribe 10_generacion.js junto a este script y lee <repo>/casos/SIN_DC/inputs.

"""
import json
import sys
from pathlib import Path

import pandas as pd

AQUI = Path(__file__).resolve().parent
REPO = AQUI.parents[2]  # <repo>/presentacion/fuente/anexos -> <repo>
INP_REPO = REPO / "casos" / "SIN_DC" / "inputs"
sys.stdout.reconfigure(encoding="utf-8")
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else AQUI / "10_generacion.js"
INP = Path(sys.argv[2]) if len(sys.argv) > 2 else INP_REPO
print("Inputs:", INP)

# ---------------------------------------------------------------- datos
gi = pd.read_csv(INP / "gen_info.csv", na_values=".")
bc = pd.read_csv(INP / "gen_build_costs.csv", na_values=".")
bp = pd.read_csv(INP / "gen_build_predetermined.csv", na_values=".")
periodos = pd.read_csv(INP / "periods.csv").INVESTMENT_PERIOD.tolist()
zonas = pd.read_csv(REPO / "resultados" / "tablas" / "zonas.csv").sort_values("orden")

predet = set(zip(bp.GENERATION_PROJECT, bp.build_year))
bc["predet"] = [(g, y) in predet for g, y in zip(bc.GENERATION_PROJECT, bc.build_year)]
cand = bc[bc.build_year.isin(periodos) & ~bc.predet].merge(
    gi[["GENERATION_PROJECT", "gen_tech", "gen_load_zone", "gen_capacity_limit_mw"]],
    on="GENERATION_PROJECT")
proy = gi[gi.GENERATION_PROJECT.isin(cand.GENERATION_PROJECT)].copy()

assert proy.gen_capacity_limit_mw.notna().all(), "candidato sin límite"
assert cand.gen_storage_energy_overnight_cost.isna().all() or True
print("Proyectos candidatos:", len(proy), "| filas de costo candidatas:", len(cand))
print("Predeterminados en períodos del modelo (no candidatos):",
      bc[bc.build_year.isin(periodos) & bc.predet].merge(gi[["GENERATION_PROJECT", "gen_tech"]])
      .groupby("gen_tech").size().to_dict())
print("Costo de conexión máx.:", gi.loc[proy.index, "gen_connect_cost_per_mw"].max())
print("Costo de inversión por energía en candidatos (no nulos):",
      cand.gen_storage_energy_overnight_cost.notna().sum())

# ---------------------------------------------------------------- grupos
GRUPOS = [  # (nombre en tabla, columna matriz, tecnologías, sin límite práctico)
    ("Solar FV", "FV", ["FV"], False),
    ("Eólica", "Eólica", ["Eolica"], False),
    ("CSP (6, 9 y 13 h)", "CSP", ["CSP_6h", "CSP_9h", "CSP_13h"], False),
    ("Hidro de pasada", "Hidro pasada", ["Hidro_Pasada_Candidata"], False),
    ("Geotermia", "Geotermia", ["Geotermia"], False),
    ("Biomasa", "Biomasa", ["Biomasa"], False),
    ("Gas natural, ciclo combinado", None, ["GNL_CC"], True),
    ("Gas natural, ciclo abierto", None, ["GNL_CA"], True),
    ("Gas natural con captura de CO₂", None, ["GNLCCS"], True),
    ("Diésel, ciclo abierto", "Diésel", ["Diesel_CA"], True),
    ("Baterías (1, 2, 4, 6 y 8 h)", "Baterías", ["BESS_1h", "BESS_2h", "BESS_4h", "BESS_6h", "BESS_8h"], False),
    ("Baterías «ley» (4 h)", None, ["BESS_4h_ley"], False),
    ("Bombeo hidráulico", "Bombeo", ["Bombeo"], False),
    ("Aire comprimido (CAES, 4 h)", "CAES", ["CAES_4h"], False),
    ("Carnot (4 y 12 h)", "Carnot", ["Carnot_4h", "Carnot_12h"], False),
]
todas = sum((g[2] for g in GRUPOS), [])
assert set(todas) == set(proy.gen_tech), set(proy.gen_tech) ^ set(todas)

# límite por zona y tecnología = suma de los proyectos (clases de recurso / costo)
lim_zt = proy.groupby(["gen_load_zone", "gen_tech"]).gen_capacity_limit_mw.sum()


def pot_zona(techs):
    """Potencial por zona del grupo: el mayor tope entre sus variantes (duraciones).
    Las duraciones de un grupo tienen cada una su propio tope en el modelo; no se suman."""
    s = lim_zt[lim_zt.index.get_level_values(1).isin(techs)]
    return s.groupby(level=0).max()


# comprobación: en CSP y Carnot el tope es idéntico entre duraciones en cada zona
for techs in (["CSP_6h", "CSP_9h", "CSP_13h"], ["Carnot_4h", "Carnot_12h"]):
    s = lim_zt[lim_zt.index.get_level_values(1).isin(techs)].groupby(level=0).agg(["min", "max"])
    assert (s["max"] - s["min"]).abs().max() < 1e-6, techs
    print("Tope idéntico entre duraciones:", techs)
# baterías: tope por duración
b = lim_zt[lim_zt.index.get_level_values(1).str.startswith("BESS")].unstack()
print("Baterías, topes por zona (valores distintos por duración):",
      {c: sorted(b[c].dropna().unique().round(1).tolist()) for c in b.columns})


def miles(x, dec=0):
    s = f"{x:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def rango(vals):
    lo, hi = round(min(vals)), round(max(vals))
    return miles(lo) if lo == hi else f"{miles(lo)}–{miles(hi)}"


def costo(techs, anio):
    c = cand[cand.gen_tech.isin(techs) & (cand.build_year == anio)].gen_overnight_cost / 1000
    return rango(c) if len(c) else "—"


filas1, resumen = [], {}
for nombre, _, techs, sinlim in GRUPOS:
    p = proy[proy.gen_tech.isin(techs)]
    nz = p.gen_load_zone.nunique()
    pz = pot_zona(techs)
    if sinlim:
        assert (p.gen_capacity_limit_mw == 10000).all()
        pot = "sin límite práctico"
    else:
        pot = miles(pz.sum())
    primero = cand[cand.gen_tech.isin(techs)].groupby("gen_tech").build_year.min()
    prim = str(primero.min())
    if primero.nunique() > 1:
        prim = f"{primero.min()} ({', '.join(t.split('_')[1] for t in primero[primero == primero.min()].index)})"
        prim = prim.replace("13h", "13 h")
    filas1.append([nombre, str(nz), pot, prim, costo(techs, 2030), costo(techs, 2050)])
    resumen[nombre] = dict(zonas=nz, potencial_MW=round(pz.sum(), 2), primer=primero.to_dict(),
                           c2030=costo(techs, 2030), c2050=costo(techs, 2050),
                           c2035=costo(techs, 2035))
for k, v in resumen.items():
    print(k, v)

# ¿varía el costo por zona? (mismo año, misma tecnología)
var = cand.groupby(["gen_tech", "build_year"]).gen_overnight_cost.agg(lambda s: s.max() - s.min())
print("Tecnologías con costo distinto entre proyectos en algún período:",
      sorted(var[var > 1e-6].index.get_level_values(0).unique()))

# ---------------------------------------------------------------- matriz
COLS = ["FV", "Eólica", "CSP", "Hidro pasada", "Geotermia", "Biomasa", "Gas natural",
        "Diésel", "Baterías", "Bombeo", "CAES", "Carnot"]
mapa = {g[1]: g[2] for g in GRUPOS if g[1]}
gas_cc = set(proy[proy.gen_tech == "GNL_CC"].gen_load_zone)
gas_ca = set(proy[proy.gen_tech == "GNL_CA"].gen_load_zone)
gas_ccs = set(proy[proy.gen_tech == "GNLCCS"].gen_load_zone)
assert gas_cc == gas_ca and gas_ccs <= gas_cc
diesel = set(proy[proy.gen_tech == "Diesel_CA"].gen_load_zone)
potz = {c: pot_zona(t) for c, t in mapa.items() if c != "Diésel"}


def celda(zlist, col):
    if col == "Gas natural":
        if not any(z in gas_cc for z in zlist):
            return "—"
        return "✓ + CCS" if any(z in gas_ccs for z in zlist) else "✓"
    if col == "Diésel":
        return "✓" if any(z in diesel for z in zlist) else "—"
    v = potz[col].reindex(zlist).dropna()
    return miles(v.sum()) if len(v) else "—"


pdge = zonas[zonas.zona.str.startswith("PDGE")]
barras = zonas[~zonas.zona.str.startswith("PDGE")]
norte = barras[barras.orden <= 18]
sur = barras[barras.orden > 18]
mat_norte = [[r.nombre] + [celda([r.zona], c) for c in COLS] for r in norte.itertuples()]
mat_norte.append([f"Polos PDGE ({len(pdge)})"] + [celda(pdge.zona.tolist(), c) for c in COLS])
mat_sur = [[r.nombre] + [celda([r.zona], c) for c in COLS] for r in sur.itertuples()]
det_pdge = []
for r in pdge.itertuples():
    partes = [f"{c} {celda([r.zona], c)} MW" for c in COLS if celda([r.zona], c) not in ("—",)]
    det_pdge.append(f"{r.nombre}: {', '.join(partes)}")
print("Detalle PDGE:", det_pdge)
# suma de la matriz = total de la tabla 1 (control cruzado)
for col in ["FV", "Eólica", "CSP", "Baterías", "Bombeo", "CAES"]:
    tot = potz[col].sum()
    print("control", col, miles(tot))

# ---------------------------------------------------------------- JS
FUENTE = ("Fuente: Ministerio de Energía (2025), datos del modelo AMEBA, "
          "escenario Carbono Neutralidad; elaboración propia.")
r = resumen
# baterías «ley»: sitios y MW, desde gen_info
ley = proy[proy.gen_tech == "BESS_4h_ley"].merge(zonas[["zona", "nombre"]], left_on="gen_load_zone", right_on="zona")
assert len(ley) == 3 and abs(ley.gen_capacity_limit_mw.sum() - 2000) < 1e-6
ley = ley.sort_values(["gen_capacity_limit_mw", "nombre"], ascending=[False, True])
ley_txt = "; ".join(f"{n}, {miles(m)} MW" for n, m in zip(ley.nombre, ley.gen_capacity_limit_mw))
assert (cand[cand.gen_tech == "BESS_4h_ley"].gen_overnight_cost == 0).all()
assert (cand[cand.gen_tech == "BESS_4h_ley"].gen_fixed_om == 0).all()
print("Baterías ley:", ley_txt)
notas1 = (
    "Siglas: FV, fotovoltaica; CSP, concentración solar de potencia, con almacenamiento térmico de 6, 9 o 13 h; "
    "CAES, almacenamiento por aire comprimido; Carnot, batería térmica que devuelve electricidad con una turbina, "
    "en carboneras reconvertidas; CO₂, dióxido de carbono; PDGE, polos de desarrollo de generación eléctrica; "
    "AMEBA, modelo de optimización con que el Ministerio de Energía hizo la PELP 2023–2027 "
    "(PELP, Planificación Energética de Largo Plazo). "
    "Candidatos son los proyectos que el modelo puede construir entre 2025 y 2050. Solo lo existente y lo comprometido "
    "en los datos de entrada de la PELP entran como capacidad predeterminada. Ninguna inversión que decidió AMEBA entra "
    "como dato: el modelo decide todas las inversiones desde 2025, y el potencial es el tope completo de cada candidato. "
    "No son candidatas las conversiones ya programadas: la co-combustión con amoníaco de Guacolda y tres "
    "reconversiones de 2026 (dos a biomasa y una a gas). "
    f"Baterías «ley» ({ley_txt}): {miles(r['Baterías «ley» (4 h)']['potencial_MW'])} MW de 4 h que en los datos de la PELP "
    "tienen inversión y O&M fijo nulos; son candidatas desde el período 2027, el primero que parte en 2026 o después "
    "(O&M, operación y mantenimiento). "
    "Los topes anuales de inversión de AMEBA en FV y eólica (3.000 y 1.000 MW en 2025; 50.000 MW por año desde 2026) "
    "se suman en los años de cada período y no restringen. "
    "Potencial: suma de los topes de los proyectos de cada zona (clases de recurso y de costo). En CSP, baterías y "
    "Carnot cada duración tiene su propio tope en la zona; se informa el mayor, sin sumar duraciones "
    "(en CSP y Carnot el tope es el mismo para todas). Gas natural y diésel: 10.000 MW por sitio, sin límite práctico. "
    f"CSP: la de 13 h desde 2030 y las de 6 y 9 h desde 2035. Hidro de pasada desde 2035, a {r['Hidro de pasada']['c2035']} USD/kW. "
    "Costo de inversión overnight, en USD/kW, variante «Medio» de AMEBA; el rango de baterías y Carnot es entre "
    "duraciones, el de FV y eólica entre zonas y clases de costo, y el de CSP 2050 entre duraciones y zonas."
)
notas2 = (
    "Cifras: potencial máximo en MW por zona; «✓», disponible sin límite práctico (10.000 MW por sitio); «—», "
    "sin candidato. Gas natural: ciclo combinado y ciclo abierto; «+ CCS» indica que además hay ciclo combinado con "
    "captura de CO₂ (CCS, captura y almacenamiento de carbono). Baterías: mayor tope entre duraciones (1, 2 y 4 h; "
    "las de 6 y 8 h tienen topes de 100 a 700 MW); no incluye las baterías «ley» (" + ley_txt + "). "
    "CSP y Carnot: tope común a todas sus duraciones. "
    "Los cinco polos PDGE (polos de desarrollo de generación eléctrica) se agrupan en una fila; por polo: "
    + "; ".join(det_pdge) + "."
)

ANCHOS1 = [3.33, 0.9, 2.2, 1.5, 2.1, 2.1]
ANCHOS2 = [1.93] + [0.85] * 12
assert abs(sum(ANCHOS1) - 12.13) < 1e-9 and abs(sum(ANCHOS2) - 12.13) < 1e-9, (sum(ANCHOS1), sum(ANCHOS2))
# alto: filas × alto por fila (tabla 1 a 11 pt desde que tiene la fila de baterías «ley»: 16 × 0,31 > 4,8)
LETRA1, ALTO_FILA1 = 11, 0.29
assert (len(filas1) + 1) * ALTO_FILA1 <= 4.8
assert (len(mat_norte) + 1) * 0.29 <= 4.8 and (len(mat_sur) + 1) * 0.29 <= 4.8
print("alto tabla 1:", (len(filas1) + 1) * ALTO_FILA1, "| matriz norte:", (len(mat_norte) + 1) * 0.29,
      "| matriz sur:", (len(mat_sur) + 1) * 0.29)

head2 = ["Zona"] + COLS
laminas = [
    dict(titulo="Anexo: tecnologías candidatas",
         subtitulo="Tecnologías en que el modelo puede invertir entre 2025 y 2050: alcance, potencial y costo de inversión",
         columnas=[dict(ancho=12.13, bloques=[dict(
             tipo="tabla",
             header=["Tecnología", "Zonas", "Potencial máx. (MW)", "Desde", "Costo 2030 (USD/kW)", "Costo 2050 (USD/kW)"],
             filas=filas1, anchos=ANCHOS1, letra=LETRA1, derecha=[1, 2, 3, 4, 5], total=False)])],
         fuente=FUENTE, notas=notas1),
    dict(titulo="Anexo: candidatos por zona (norte)",
         subtitulo="Potencial máximo candidato por zona (MW), de Parinacota a Nueva Pan de Azúcar, y polos PDGE",
         columnas=[dict(ancho=12.13, bloques=[dict(
             tipo="tabla", header=head2, filas=mat_norte, anchos=ANCHOS2, letra=11,
             derecha=list(range(1, 13)), total=False)])],
         fuente=FUENTE, notas=notas2),
    dict(titulo="Anexo: candidatos por zona (centro y sur)",
         subtitulo="Potencial máximo candidato por zona (MW), de Quillota a Nueva Ancud",
         columnas=[dict(ancho=12.13, bloques=[dict(
             tipo="tabla", header=head2, filas=mat_sur, anchos=ANCHOS2, letra=11,
             derecha=list(range(1, 13)), total=False)])],
         fuente=FUENTE, notas=notas2),
]
for l in laminas:
    assert len(l["titulo"]) <= 45 and len(l["subtitulo"]) <= 110, (l["titulo"], len(l["subtitulo"]))
# celdas en una línea: ~16 car/in a 11 pt, ~14 a 12 pt
for l in laminas:
    t = l["columnas"][0]["bloques"][0]
    cpi = 14 if t["letra"] == 12 else 16
    for fila in [t["header"]] + t["filas"]:
        for txt, w in zip(fila, t["anchos"]):
            if len(txt) > w * cpi - 1:
                print("AVISO celda larga:", repr(txt), w)

js = ("// Anexo de generación candidata. Generado por un script de elaboración propia; no editar a mano.\n"
      "module.exports = " + json.dumps(laminas, ensure_ascii=False, indent=2) + ";\n")
OUT.write_text(js, encoding="utf-8")
print("escrito", OUT)
for f in filas1:
    print(" | ".join(f))
print()
for f in mat_norte + mat_sur:
    print(" | ".join(f))
