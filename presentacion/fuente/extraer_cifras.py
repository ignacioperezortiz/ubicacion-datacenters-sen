"""Extrae de las tablas de resultados del estudio todas las cifras que usa la presentación y las escribe
en cifras.json, que lee build.js. Así las láminas de casos y resultados no tienen números escritos a mano.

Uso: python -I extraer_cifras.py [<carpeta del repositorio> [cifras.json]]
Por omisión usa el repositorio que contiene este archivo (<repo>/presentacion/fuente/).
"""
import json
import sys
from pathlib import Path

import pandas as pd

REPO = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[2]
SALIDA = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).with_name('cifras.json')
T = REPO / 'resultados' / 'tablas'
ESC = ['PELP_E2', 'CEN', 'PELP_N1', 'PROPIO']
ETIQ = {'PELP_E2': 'PELP E2', 'CEN': 'CEN', 'PELP_N1': 'PELP N1', 'PROPIO': 'Propio'}
DC_LIBRE_DESDE = 2030

leer = lambda nombre: pd.read_csv(T / nombre)
cif = {'escenarios': [ETIQ[e] for e in ESC]}

# ---- Tiempo: períodos y año base ----
entradas = REPO / 'casos' / 'SIN_DC' / 'inputs'
periodos = pd.read_csv(entradas / 'periods.csv')
cif['periodos'] = [int(p) for p in periodos['INVESTMENT_PERIOD']]
cif['periodos_rango'] = [f"{int(a)}–{int(b)}" for a, b in zip(periodos['period_start'], periodos['period_end'])]
cif['anio_base'] = int(pd.read_csv(entradas / 'financials.csv')['base_financial_year'].iloc[0])

# ---- Costos: costo extra y ahorro ----
costos = leer('costos.csv').set_index('escenario').loc[ESC]
cif['costo_sin_dc'] = float(costos['costo_sin_dc_MMUSD'].iloc[0])
cif['extra_base'] = costos['extra_base_MMUSD'].round(0).tolist()
cif['extra_libre'] = costos['extra_libre_MMUSD'].round(0).tolist()
cif['ahorro'] = costos['ahorro_MMUSD'].round(0).tolist()
cif['ahorro_pct_extra'] = costos['ahorro_pct_del_extra'].round(0).tolist()
cif['extra_usd_mwh_base'] = costos['extra_base_usd_mwh'].round(0).tolist()
cif['extra_usd_mwh_libre'] = costos['extra_libre_usd_mwh'].round(0).tolist()
res_dc = leer('escenarios_dc_resumen.csv').set_index('escenario').loc[ESC]
cif['ahorro_usd_mwh_reubicable'] = res_dc['ahorro_usd_por_mwh_reubicable'].round(1).tolist()
cif['reubicable_2050_pct'] = res_dc['reubicable_2050_pct'].round(0).tolist()

# ---- Escenarios de data centers: MW medios por período y ubicación proyectada al último período ----
esc_dc = leer('escenarios_dc.csv')
cif['dc_total_por_periodo'] = {ETIQ[e]: esc_dc[esc_dc['escenario'] == e].sort_values('periodo')['dc_total_MW'].round(0).tolist()
                               for e in ESC}
ubic = leer('ubicacion_dc.csv')
zonas = leer('zonas.csv')
ultimo = cif['periodos'][-1]
u = ubic[ubic['PERIOD'] == ultimo].merge(zonas[['zona', 'nombre', 'region', 'orden']], left_on='LOAD_ZONE', right_on='zona')
reg = u[u['modo'] == 'base'].groupby(['escenario', 'region'])['dc_total_mw'].sum().unstack(fill_value=0).reindex(ESC, fill_value=0)
cif['ubicacion_proyectada_region'] = {r: reg[r].round(0).tolist() for r in reg.columns}

# ---- Ubicación por zona en el último período: proyectada -> óptima ----
tabla = u.pivot_table(index=['orden', 'nombre', 'region'], columns=['escenario', 'modo'], values='dc_total_mw', aggfunc='sum')
filas = []
for (orden, nombre, region), fila in tabla.sort_index().iterrows():
    celdas = []
    for e in ESC:
        b = fila.get((e, 'base'), float('nan'))
        l = fila.get((e, 'libre'), float('nan'))
        b, l = (0 if pd.isna(b) else b), (0 if pd.isna(l) else l)
        celdas.append('–' if b < 0.5 and l < 0.5 else f'{b:,.0f} → {l:,.0f}'.replace(',', '.'))
    filas.append({'zona': f'{nombre.rsplit(" ", 1)[0]} ({region})', 'celdas': celdas})
cif['ubicacion_por_zona'] = filas

# ---- Capacidad construida al último período, libre - base ----
inv = leer('inversiones_libre_menos_base.csv')
cap = {}
for grupo, nombre in [('Eólica', 'Eólica'), ('Solar FV', 'Solar FV'), ('Baterías', 'Baterías'), ('Bombeo', 'Bombeo')]:
    sub = inv[inv['grupo'] == grupo].set_index('escenario').reindex(ESC)['dif_MW'].fillna(0)
    cap[nombre] = sub.round(0).tolist()
tx = leer('transmision_libre_menos_base.csv').groupby('escenario')['dif_MW'].sum().reindex(ESC)
cap['Transmisión'] = tx.round(0).tolist()
cif['cambio_capacidad'] = cap

# ---- Ahorro por tipo de costo (base - libre) ----
comp = pd.read_csv(T / 'costos_por_componente.csv', header=[0, 1, 2], index_col=0)
comp.columns = pd.MultiIndex.from_tuples([(a, b) for a, b, _ in comp.columns])
def comp_ahorro(filas_tipo):
    return [round(sum(float(comp.loc[f, (e, 'base - libre')]) for f in filas_tipo), 0) for e in ESC]
cif['ahorro_componentes'] = {
    'Inversión en generación y almacenamiento': comp_ahorro(['Generación y almacenamiento: inversión + O&M fijo',
                                                             'Almacenamiento: inversión + O&M fijo en energía (MWh)']),
    'Combustible': comp_ahorro(['Combustible']),
    'Transmisión': comp_ahorro(['Transmisión: inversión + O&M fijo (incluye la existente)']),
    'Impuesto al CO₂ y O&M variable': comp_ahorro(['Impuesto al CO2', 'O&M variable']),
    'Energía no suministrada': comp_ahorro(['Energía no suministrada (VOLL)']),
}

# ---- Capacidad nueva por MW de data center y emisiones ----
rc = leer('resumen_casos.csv').set_index(['escenario', 'modo'])
nueva = lambda e, m: rc.loc[(e, m), 'generacion_nueva_MW'] + rc.loc[(e, m), 'almacenamiento_nuevo_MW']
dc_ult = {e: rc.loc[(e, 'base'), 'dc_2050_MW'] for e in ESC}
cif['mw_nuevos_por_mw_dc_base'] = [round((nueva(e, 'base') - nueva('SIN_DC', 'base')) / dc_ult[e], 1) for e in ESC]
cif['mw_nuevos_por_mw_dc_libre'] = [round((nueva(e, 'libre') - nueva('SIN_DC', 'base')) / dc_ult[e], 1) for e in ESC]
cif['emisiones_menos_libre_Mt'] = [round(rc.loc[(e, 'base'), 'emisiones_acumuladas_MtCO2'] - rc.loc[(e, 'libre'), 'emisiones_acumuladas_MtCO2'], 1) for e in ESC]
cif['dc_ultimo_periodo'] = [round(dc_ult[e], 0) for e in ESC]

# ---- Precio de una carga plana en 2040 sin data centers: zonas elegidas frente a proyectadas ----
pz = leer('precios_zonales.csv')
p40 = pz[(pz['escenario'] == 'SIN_DC') & (pz['modo'] == 'base') & (pz['periodo'] == 2040)].set_index('zona')['precio_carga_plana_usd_mwh']
fijo_hasta = max(p for p in cif['periodos'] if p < DC_LIBRE_DESDE)
elegidas, proyectadas = set(), set()
for e in ESC:
    sub = ubic[ubic['escenario'] == e]
    piv = sub.pivot_table(index='LOAD_ZONE', columns=['modo', 'PERIOD'], values='dc_ubicado_mw', aggfunc='sum').fillna(0)
    libre_ult = piv.get(('libre', ultimo), pd.Series(dtype=float))
    libre_fijo = piv.get(('libre', fijo_hasta), pd.Series(0, index=piv.index))
    elegidas |= set(libre_ult[(libre_ult - libre_fijo.reindex(libre_ult.index, fill_value=0)) > 1].index)
    base_ult = piv.get(('base', ultimo), pd.Series(dtype=float))
    proyectadas |= set(base_ult[base_ult > 1].index)
cif['zonas_elegidas'] = sorted(elegidas)
cif['zonas_proyectadas'] = sorted(proyectadas)
cif['precio_2040_elegidas'] = [round(p40.reindex(sorted(elegidas)).min(), 1), round(p40.reindex(sorted(elegidas)).max(), 1)]
cif['precio_2040_proyectadas'] = [round(p40.reindex(sorted(proyectadas)).min(), 1), round(p40.reindex(sorted(proyectadas)).max(), 1)]

# ---- Tamaño del problema y tiempos de cómputo ----
tc = leer('tiempos_computo.csv')
cif['filas'] = int(tc['filas'].max())
cif['columnas'] = int(tc['columnas'].max())
cif['minutos_corrida'] = [round(float(tc['reloj_total_min'].min())), round(float(tc['reloj_total_min'].max()))]
cif['n_corridas'] = int(len(tc))

# ---- Corredores en su tope de ampliación en todos los casos, y macrozona de las zonas elegidas ----
trl = leer('transmision_libre_menos_base.csv')
en_tope = trl.groupby('nombre')[['sin_dc_en_tope', 'base_en_tope', 'libre_en_tope']].all().all(axis=1)
cif['corredores_en_tope_todos'] = sorted(en_tope[en_tope].index)
macro = zonas.set_index('zona')['macrozona']
cif['macrozonas_elegidas'] = sorted(set(macro.reindex(sorted(elegidas)).dropna()))
# De esos, los que traen energía del sur hacia el centro: algún extremo en el Centro-Sur o el Sur y ninguno en el norte.
# Son los que explican por qué conviene ubicar en el sur (un corredor en Antofagasta no lo explica).
extremos = trl.drop_duplicates('nombre').set_index('nombre')['corredor'].str.split('_')
cif['corredores_sur_en_tope_todos'] = [
    n for n in cif['corredores_en_tope_todos']
    if any(macro.get(z) in ('Centro-Sur', 'Sur') for z in extremos[n])
    and not any(macro.get(z) in ('Norte Grande', 'Norte Chico') for z in extremos[n])]
# Zonas elegidas por escenario y su macrozona, y precio de 2040 por macrozona elegida
por_esc = {}
for e in ESC:
    sub = ubic[ubic['escenario'] == e]
    piv = sub.pivot_table(index='LOAD_ZONE', columns=['modo', 'PERIOD'], values='dc_ubicado_mw', aggfunc='sum').fillna(0)
    libre_ult = piv.get(('libre', ultimo), pd.Series(dtype=float))
    libre_fijo = piv.get(('libre', fijo_hasta), pd.Series(0, index=piv.index)).reindex(libre_ult.index, fill_value=0)
    zs = sorted(libre_ult[(libre_ult - libre_fijo) > 1].index)
    por_esc[ETIQ[e]] = sorted(set(macro.reindex(zs).dropna()))
cif['macrozonas_por_escenario'] = por_esc
cif['precio_2040_por_macrozona'] = {m: [round(p40.reindex([z for z in sorted(elegidas) if macro.get(z) == m]).min(), 1),
                                        round(p40.reindex([z for z in sorted(elegidas) if macro.get(z) == m]).max(), 1)]
                                    for m in cif['macrozonas_elegidas']}
# Otros cambios de capacidad grandes (|libre - base| >= 500 MW) fuera de las 5 tecnologías del gráfico
otros = inv[~inv['grupo'].isin(['Eólica', 'Solar FV', 'Baterías', 'Bombeo'])]
otros = otros[otros['dif_MW'].abs() >= 500]
cif['otros_cambios_capacidad'] = [{'escenario': ETIQ[r.escenario], 'grupo': r.grupo, 'dif_MW': round(float(r.dif_MW), 0)}
                                  for r in otros.itertuples() if r.escenario in ETIQ]

SALIDA.write_text(json.dumps(cif, ensure_ascii=False, indent=1), encoding='utf-8')
print('cifras escritas en', SALIDA)
