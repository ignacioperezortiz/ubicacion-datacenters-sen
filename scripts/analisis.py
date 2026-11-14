"""Tablas de análisis de la expansión eficiente del SEN, con y sin data centers.

Complementa a resultados.py (costos, ubicación, precios, tiempos) con tablas de la expansión del
sistema en los 9 casos: SIN_DC y los 4 escenarios de data centers en modo base y libre.
Escribe en resultados/tablas/:
  - zonas.csv                            orden norte -> sur de las 31 zonas, latitud aproximada y macrozona
  - escenarios_dc.csv                    demanda de data centers por período: total, comprometida y reubicable
  - escenarios_dc_resumen.csv            por escenario: demanda, energía en VP y ahorro por MWh
  - matriz_generacion.csv                capacidad (MW) y energía (GWh/año) por grupo de tecnología y período
  - inversiones_por_tecnologia.csv       MW construidos en cada período: comprometidos y decididos por el modelo
  - inversiones_libre_menos_base.csv     MW construidos por grupo, base y libre, y su diferencia por período
  - transmision_ampliaciones.csv         MW ampliados por corredor y período, e inversión overnight
  - transmision_libre_menos_base.csv     ampliación 2026-2050 por corredor, base y libre, y su diferencia
  - expansion_por_zona.csv               MW nuevos de generación y almacenamiento por zona y período
  - expansion_zona_libre_menos_base.csv  MW nuevos 2026-2050 por zona, base y libre, y su diferencia
  - expansion_por_macrozona.csv          MW nuevos 2026-2050 por macrozona, en los 9 casos
  - emisiones_vertimiento.csv            emisiones, demanda, vertimiento y energía no suministrada por período
  - balance_por_macrozona.csv            inyección, demanda y exportación neta de energía por macrozona y período
  - precios_zonales.csv                  precio de una carga plana por zona y período, en los 9 casos
  - precio_dc.csv                        precio medio de una carga plana en las zonas con data centers
  - resumen_casos.csv                    indicadores principales de cada caso
  - entorno_computo.csv                  procesador, versión de Gurobi e hilos de cada corrida (de los logs)

Solo lee archivos del repositorio, con rutas relativas a su raíz: casos/<CASO>/inputs y
casos/<CASO>/outputs_<modo>. No usa las salidas horarias pesadas (dispatch.csv y otras), que no están
en el repositorio: usa los resúmenes anuales, gen_cap.csv, BuildGen.csv, BuildTx.csv, SpillHydro.csv
y load_balance.csv.
Uso: python -I scripts/analisis.py
"""
import re
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
CASOS = RAIZ / 'casos'
SALIDA = RAIZ / 'resultados' / 'tablas'
SALIDA.mkdir(parents=True, exist_ok=True)

ESCENARIOS = ['PELP_E2', 'CEN', 'PELP_N1', 'PROPIO']   # de menor a mayor demanda de data centers
REFERENCIA = 'SIN_DC'                                  # Carbono Neutralidad sin data centers (solo base)
CASOS_MODOS = [(REFERENCIA, 'base')] + [(e, m) for e in ESCENARIOS for m in ('base', 'libre')]
ENTRADAS = CASOS / REFERENCIA / 'inputs'               # los datos comunes son iguales en los 5 casos


def leer(escenario, modo, archivo, **opciones):
    """Lee una salida de Switch de un caso."""
    return pd.read_csv(CASOS / escenario / f'outputs_{modo}' / archivo, **opciones)


def guardar(tabla, nombre):
    """Escribe una tabla redondeada a 3 decimales (suficiente para MW, GWh y millones de USD)."""
    tabla.round(3).to_csv(SALIDA / nombre, index=False, encoding='utf-8')
    print(f'  {nombre:40} {len(tabla):6d} filas')


# =====================================================================================================
# 1. Orden geográfico de las zonas (norte -> sur)
# =====================================================================================================
# Los datos de entrada no traen coordenadas. Cada zona es una subestación del SEN; su latitud
# aproximada (grados sur, redondeada a 0,1°) se toma de la ubicación conocida de la subestación.
# Los polos de desarrollo de generación (PDGE) no son subestaciones: se ubican junto a la subestación a
# la que se conectan en transmission_lines.csv. Cuando dos zonas comparten sitio (Kimal 220/500,
# Los Changos 500/220) el orden entre ellas es arbitrario. Lo que importa es el orden, no el decimal.
ZONAS = [
    # zona,                  nombre,                     latitud, región,        macrozona
    ('Parinacota220',        'Parinacota 220',            18.5, 'Arica y Parinacota', 'Norte Grande'),
    ('NuevaPozoAlmonte220',  'Nueva Pozo Almonte 220',    20.3, 'Tarapacá',      'Norte Grande'),
    ('Lagunas220',           'Lagunas 220',               21.0, 'Tarapacá',      'Norte Grande'),
    ('Kimal220',             'Kimal 220',                 22.3, 'Antofagasta',   'Norte Grande'),
    ('Kimal500',             'Kimal 500',                 22.3, 'Antofagasta',   'Norte Grande'),
    ('PDGE-TOC-A1',          'Polo Tocopilla A1',         22.3, 'Antofagasta',   'Norte Grande'),
    ('PDGE-TOC-A2',          'Polo Tocopilla A2',         22.3, 'Antofagasta',   'Norte Grande'),
    ('LosChangos500',        'Los Changos 500',           23.1, 'Antofagasta',   'Norte Grande'),
    ('LosChangos220',        'Los Changos 220',           23.1, 'Antofagasta',   'Norte Grande'),
    ('PDGE-ANF-B1',          'Polo Antofagasta B1',       23.1, 'Antofagasta',   'Norte Grande'),
    ('NuevaZaldivar220',     'Nueva Zaldívar 220',        24.3, 'Antofagasta',   'Norte Grande'),
    ('Parinas500',           'Parinas 500',               25.0, 'Antofagasta',   'Norte Grande'),
    ('PDGE-ANF-B2',          'Polo Antofagasta B2',       25.0, 'Antofagasta',   'Norte Grande'),
    ('Cumbre500',            'Cumbre 500',                26.4, 'Atacama',       'Norte Chico'),
    ('PDGE-ANF-B3',          'Polo Antofagasta B3',       26.4, 'Atacama',       'Norte Chico'),
    ('NuevaCardones500',     'Nueva Cardones 500',        27.5, 'Atacama',       'Norte Chico'),
    ('NuevaMaitencillo500',  'Nueva Maitencillo 500',     28.6, 'Atacama',       'Norte Chico'),
    ('NuevaPandeAzucar500',  'Nueva Pan de Azúcar 500',   30.0, 'Coquimbo',      'Norte Chico'),
    ('Quillota500',          'Quillota 500',              32.9, 'Valparaíso',    'Centro'),
    ('Polpaico500',          'Polpaico 500',              33.1, 'Metropolitana', 'Centro'),
    ('AltoJahuel500',        'Alto Jahuel 500',           33.7, 'Metropolitana', 'Centro'),
    ('Candelaria500',        'Candelaria 500',            34.0, "O'Higgins",     'Centro'),
    ('Rapel500',             'Rapel 500',                 34.0, "O'Higgins",     'Centro'),
    ('Ancoa500',             'Ancoa 500',                 35.8, 'Maule',         'Centro-Sur'),
    ('Concepcion500',        'Concepción 500',            36.8, 'Biobío',        'Centro-Sur'),
    ('NuevaCharrua500',      'Nueva Charrúa 500',         37.0, 'Biobío',        'Centro-Sur'),
    ('Mulchen500',           'Mulchén 500',               37.7, 'Biobío',        'Centro-Sur'),
    ('RioMalleco500',        'Río Malleco 500',           38.0, 'Araucanía',     'Sur'),
    ('Pichirropulli500',     'Pichirropulli 500',         40.0, 'Los Ríos',      'Sur'),
    ('NuevaPuertoMontt500',  'Nueva Puerto Montt 500',    41.4, 'Los Lagos',     'Sur'),
    ('NuevaAncud500',        'Nueva Ancud 500',           41.9, 'Los Lagos',     'Sur'),
]
zonas = pd.DataFrame(ZONAS, columns=['zona', 'nombre', 'latitud_aprox_sur', 'region', 'macrozona'])
zonas.insert(0, 'orden', range(1, len(zonas) + 1))
zonas_modelo = set(pd.read_csv(ENTRADAS / 'load_zones.csv')['LOAD_ZONE'])
if set(zonas['zona']) != zonas_modelo:
    raise ValueError(f'El orden geográfico no calza con load_zones.csv: {set(zonas.zona) ^ zonas_modelo}')
candidatas = set(pd.read_csv(ENTRADAS / 'dc_candidatas.csv')['DC_ZONE'])
zonas['candidata_dc'] = zonas['zona'].isin(candidatas)
ORDEN = zonas.set_index('zona')['orden']
info_zona = zonas.set_index('zona')[['nombre', 'orden', 'macrozona']]


# =====================================================================================================
# 2. Grupos de tecnología
# =====================================================================================================
# familia: 8 grupos para los gráficos (un color por familia); grupo: el detalle de las tablas.
GRUPOS = {
    'FV': ('Solar', 'Solar FV'),
    'CSP_6h': ('Solar', 'Solar CSP'), 'CSP_9h': ('Solar', 'Solar CSP'), 'CSP_13h': ('Solar', 'Solar CSP'),
    'Eolica': ('Eólica', 'Eólica'),
    'Hidro_Embalse': ('Hidro', 'Hidro embalse'),
    'Hidro_Pasada': ('Hidro', 'Hidro pasada'),
    'Hidro_Pasada_Candidata': ('Hidro', 'Hidro pasada'),
    'Biomasa': ('Biomasa y otras', 'Biomasa y biogás'),
    'Biogas': ('Biomasa y otras', 'Biomasa y biogás'),
    'Geotermia': ('Biomasa y otras', 'Geotermia'),
    'Cogeneracion': ('Biomasa y otras', 'Cogeneración'),
    'GNL_CC': ('Gas', 'Gas ciclo combinado'),
    'GNL_CA': ('Gas', 'Gas ciclo abierto y motores'),
    'Motor_GNL': ('Gas', 'Gas ciclo abierto y motores'),
    'GNLCCS': ('Gas', 'Gas con captura de CO2'),
    'Carbon': ('Carbón', 'Carbón'),
    'Cofiring_NH3': ('Carbón', 'Carbón con co-combustión de amoníaco'),
    'Diesel_CA': ('Diésel', 'Diésel'),
    'Motor_Diesel': ('Diésel', 'Diésel'),
    'Bombeo': ('Almacenamiento', 'Bombeo'),
    'CAES_4h': ('Almacenamiento', 'Aire comprimido y Carnot'),
    'Carnot_4h': ('Almacenamiento', 'Aire comprimido y Carnot'),
    'Carnot_12h': ('Almacenamiento', 'Aire comprimido y Carnot'),
}
FAMILIAS = ['Hidro', 'Gas', 'Eólica', 'Solar', 'Almacenamiento', 'Biomasa y otras', 'Carbón', 'Diésel']
RENOVABLES = {'Hidro', 'Eólica', 'Solar'} | {'Biomasa y biogás', 'Geotermia'}   # familias y grupos


def grupo_de(tecnologia):
    """(familia, grupo) de una tecnología de Switch; las baterías van todas al grupo Baterías."""
    if tecnologia.startswith('BESS_'):
        return 'Almacenamiento', 'Baterías'
    if tecnologia not in GRUPOS:
        raise KeyError(f'Tecnología sin grupo asignado: {tecnologia}')
    return GRUPOS[tecnologia]


gen_info = pd.read_csv(ENTRADAS / 'gen_info.csv', na_values='.').set_index('GENERATION_PROJECT')
proyectos = pd.DataFrame({
    'gen_tech': gen_info['gen_tech'],
    'zona': gen_info['gen_load_zone'],
    'familia': [grupo_de(t)[0] for t in gen_info['gen_tech']],
    'grupo': [grupo_de(t)[1] for t in gen_info['gen_tech']],
    'es_almacenamiento': gen_info['gen_storage_efficiency'].notna(),
    'es_variable': gen_info['gen_is_variable'] == 1,
    'disponibilidad': 1 - gen_info['gen_forced_outage_rate'].fillna(0),
})


# =====================================================================================================
# 3. Períodos, horas representativas y factores de valor presente
# =====================================================================================================
# Cada hora representativa pesa tp_weight_in_year = duración x días que representa / años del período,
# igual que en Switch (timescales.py). Con eso, sum(MW x peso) / 1000 = GWh por año típico del período.
periodos = pd.read_csv(ENTRADAS / 'periods.csv')
periodos['anios'] = periodos['period_end'] - periodos['period_start'] + 1
ANIOS = periodos.set_index('INVESTMENT_PERIOD')['anios']
PERIODOS = list(ANIOS.index)
financiero = pd.read_csv(ENTRADAS / 'financials.csv').iloc[0]
tasa, anio_base = financiero['discount_rate'], financiero['base_financial_year']
# Factor que lleva un costo anual constante de cada período a VP del año base (como financials.py)
FACTOR_VP = {p.INVESTMENT_PERIOD: (1 - (1 + tasa) ** -p.anios) / tasa * (1 + tasa) ** -(p.period_start - anio_base)
             for p in periodos.itertuples()}

series = pd.read_csv(ENTRADAS / 'timeseries.csv')
series['peso'] = series['ts_duration_of_tp'] * series['ts_scale_to_period'] / series['ts_period'].map(ANIOS)
horas = pd.read_csv(ENTRADAS / 'timepoints.csv')
horas = horas.merge(series[['TIMESERIES', 'ts_period', 'peso']], left_on='timeseries', right_on='TIMESERIES')
horas = horas.rename(columns={'ts_period': 'periodo'})[['timepoint_id', 'timestamp', 'periodo', 'peso']]
if not (horas.groupby('periodo')['peso'].sum().round(6) == 8760).all():
    raise ValueError('Los pesos de las horas representativas no suman 8760 h por año')


def periodo_de(anio):
    """Período de inversión que contiene un año de construcción."""
    for p in periodos.itertuples():
        if p.period_start <= anio <= p.period_end:
            return p.INVESTMENT_PERIOD
    return None


print('Tablas de análisis en resultados/tablas:')
guardar(zonas, 'zonas.csv')


# =====================================================================================================
# 4. Escenarios de data centers: demanda total, comprometida y reubicable
# =====================================================================================================
# Demanda de un período = parte fija (dc_fijo) + parte ubicable (dc_libre). En modo libre, lo ubicado en
# 2026 queda donde lo pone la proyección y un data center no se traslada, así que solo es reubicable lo
# que se agrega después de 2026: dc_libre[p] - dc_libre[2026]. El resto es comprometido.
costo_total = {(e, m): float((CASOS / e / f'outputs_{m}' / 'total_cost.txt').read_text()) / 1e6
               for e, m in CASOS_MODOS}
filas = []
for e in ESCENARIOS:
    entradas = CASOS / e / 'inputs'
    libre = pd.read_csv(entradas / 'dc_libre.csv').set_index('PERIOD')['dc_libre_mw']
    fijo = pd.read_csv(entradas / 'dc_fijo.csv').groupby('PERIOD')['dc_fijo_mw'].sum().reindex(PERIODOS, fill_value=0)
    for p in PERIODOS:
        reubicable = libre[p] - libre[PERIODOS[0]]
        filas.append({'escenario': e, 'periodo': p, 'dc_total_MW': fijo[p] + libre[p],
                      'dc_comprometido_MW': fijo[p] + libre[PERIODOS[0]], 'dc_reubicable_MW': reubicable,
                      'dc_energia_GWh_anio': (fijo[p] + libre[p]) * 8.76,
                      'dc_energia_vp_TWh': (fijo[p] + libre[p]) * 8760 * FACTOR_VP[p] / 1e6,
                      'dc_reubicable_vp_TWh': reubicable * 8760 * FACTOR_VP[p] / 1e6})
    # Control: los MW de data centers que reporta el modelo son los mismos en base y libre.
    for m in ('base', 'libre'):
        ubicados = leer(e, m, 'dc_ubicacion.csv').groupby('PERIOD')['dc_total_mw'].sum()
        esperado = fijo + libre
        if (ubicados - esperado).abs().max() > 0.01:
            raise ValueError(f'{e} {m}: dc_ubicacion.csv no suma la demanda de data centers de las entradas')
escenarios_dc = pd.DataFrame(filas)
escenarios_dc['dc_reubicable_pct'] = 100 * escenarios_dc['dc_reubicable_MW'] / escenarios_dc['dc_total_MW']
guardar(escenarios_dc, 'escenarios_dc.csv')

# Resumen por escenario: ahorro de ubicar bien (base - libre), por MWh de data centers y por MWh
# reubicable, ambos con la energía en VP 2026 (la misma tasa con que Switch descuenta los costos).
resumen_dc = escenarios_dc.groupby('escenario', sort=False).agg(
    dc_2026_MW=('dc_total_MW', 'first'), dc_2050_MW=('dc_total_MW', 'last'),
    reubicable_2050_MW=('dc_reubicable_MW', 'last'), reubicable_2050_pct=('dc_reubicable_pct', 'last'),
    energia_dc_vp_TWh=('dc_energia_vp_TWh', 'sum'), energia_reubicable_vp_TWh=('dc_reubicable_vp_TWh', 'sum'))
resumen_dc['costo_base_MMUSD'] = [costo_total[(e, 'base')] for e in resumen_dc.index]
resumen_dc['costo_libre_MMUSD'] = [costo_total[(e, 'libre')] for e in resumen_dc.index]
resumen_dc['ahorro_MMUSD'] = resumen_dc['costo_base_MMUSD'] - resumen_dc['costo_libre_MMUSD']
resumen_dc['ahorro_usd_por_mwh_dc'] = resumen_dc['ahorro_MMUSD'] / resumen_dc['energia_dc_vp_TWh']
resumen_dc['ahorro_usd_por_mwh_reubicable'] = resumen_dc['ahorro_MMUSD'] / resumen_dc['energia_reubicable_vp_TWh']
guardar(resumen_dc.reset_index(), 'escenarios_dc_resumen.csv')


# =====================================================================================================
# 5. Matriz de generación: capacidad instalada y energía por grupo de tecnología y período
# =====================================================================================================
# Capacidad: GenCapacity de gen_cap.csv (MW de potencia; para almacenamiento, MW de descarga) y
# GenStorageCapacity (MWh). Energía: dispatch_gen_annual_summary.csv. Para el almacenamiento se reporta
# la descarga como energía y la carga aparte, porque su energía neta es negativa (pérdidas).
matriz, detalle_energia = [], []
for e, m in CASOS_MODOS:
    cap = leer(e, m, 'gen_cap.csv', na_values='.')
    cap = cap.join(proyectos[['familia', 'grupo']], on='GENERATION_PROJECT')
    cap_g = cap.groupby(['PERIOD', 'familia', 'grupo']).agg(
        capacidad_MW=('GenCapacity', 'sum'), almacenamiento_MWh=('GenStorageCapacity', 'sum'))
    anual = leer(e, m, 'dispatch_gen_annual_summary.csv')
    anual = anual.join(proyectos[['familia', 'grupo', 'es_almacenamiento']], on='generation_project')
    anual['energia_GWh'] = anual['Energy_GWh_typical_yr'].where(~anual['es_almacenamiento'],
                                                                anual['Discharge_GWh_typical_yr'])
    anual['carga_GWh'] = anual['Store_GWh_typical_yr'].where(anual['es_almacenamiento'], 0.0)
    anual['emisiones_MtCO2'] = anual['DispatchEmissions_tCO2_per_typical_yr'] / 1e6
    ene_g = anual.groupby(['period', 'familia', 'grupo'])[['energia_GWh', 'carga_GWh', 'emisiones_MtCO2']].sum()
    ene_g.index.names = cap_g.index.names
    tabla = cap_g.join(ene_g, how='outer').fillna(0).reset_index().rename(columns={'PERIOD': 'periodo'})
    matriz.append(tabla.assign(escenario=e, modo=m))
    detalle_energia.append(anual.assign(escenario=e, modo=m))
matriz = pd.concat(matriz)
# Participación en la generación (sin contar la descarga de almacenamiento, que no es energía nueva)
generacion = matriz[matriz.familia != 'Almacenamiento'].groupby(['escenario', 'modo', 'periodo'])['energia_GWh'].sum()
matriz['participacion_generacion_pct'] = (
    100 * matriz['energia_GWh'] / matriz.set_index(['escenario', 'modo', 'periodo']).index.map(generacion))
matriz.loc[matriz.familia == 'Almacenamiento', 'participacion_generacion_pct'] = float('nan')
matriz['familia'] = pd.Categorical(matriz['familia'], FAMILIAS, ordered=True)
matriz = matriz.sort_values(['escenario', 'modo', 'periodo', 'familia', 'grupo'])
columnas = ['escenario', 'modo', 'periodo', 'familia', 'grupo', 'capacidad_MW', 'almacenamiento_MWh',
            'energia_GWh', 'carga_GWh', 'participacion_generacion_pct', 'emisiones_MtCO2']
guardar(matriz[columnas], 'matriz_generacion.csv')


# =====================================================================================================
# 6. Inversiones nuevas: MW construidos en cada período
# =====================================================================================================
# BuildGen.csv trae los MW construidos por proyecto y año de construcción (incluye los existentes, con
# años anteriores a 2026). Un año de construcción se asigna al período que lo contiene (p. ej. 2033 ->
# 2030). gen_build_predetermined.csv dice qué parte es obra comprometida (fija en el modelo); el resto
# lo decide el modelo. BuildStorageEnergy.csv trae los MWh de almacenamiento construidos.
predet = pd.read_csv(ENTRADAS / 'gen_build_predetermined.csv', na_values='.')
predet = predet.set_index(['GENERATION_PROJECT', 'build_year'])['build_gen_predetermined']
construcciones = []
for e, m in CASOS_MODOS:
    obra = leer(e, m, 'BuildGen.csv')
    obra.columns = ['proyecto', 'anio', 'MW']
    obra = obra[obra['anio'] >= PERIODOS[0]].copy()
    energia = leer(e, m, 'BuildStorageEnergy.csv')
    energia.columns = ['proyecto', 'anio', 'MWh']
    obra = obra.merge(energia, on=['proyecto', 'anio'], how='left').fillna({'MWh': 0.0})
    obra['periodo'] = obra['anio'].map(periodo_de)
    obra['MW_comprometidos'] = [predet.get((g, a), 0.0) for g, a in zip(obra['proyecto'], obra['anio'])]
    obra['MW_comprometidos'] = obra[['MW_comprometidos', 'MW']].min(axis=1)
    obra['MW_decididos'] = obra['MW'] - obra['MW_comprometidos']
    obra = obra.join(proyectos[['gen_tech', 'zona', 'familia', 'grupo']], on='proyecto')
    construcciones.append(obra.assign(escenario=e, modo=m))
construcciones = pd.concat(construcciones)
construcciones['tipo'] = construcciones['familia'].map(lambda f: 'Almacenamiento' if f == 'Almacenamiento' else 'Generación')

inversiones = (construcciones.groupby(['escenario', 'modo', 'periodo', 'familia', 'grupo'])
               [['MW', 'MW_comprometidos', 'MW_decididos', 'MWh']].sum().reset_index()
               .rename(columns={'MW': 'MW_construidos', 'MWh': 'MWh_almacenamiento'}))
inversiones = inversiones[inversiones['MW_construidos'] > 0.001]
guardar(inversiones, 'inversiones_por_tecnologia.csv')

# Diferencia libre - base por grupo: total 2026-2050 y por período (columnas dif_<período>)
mw = construcciones.pivot_table(index=['escenario', 'familia', 'grupo'], columns=['modo', 'periodo'],
                                values='MW', aggfunc='sum', fill_value=0.0)
filas = []
for (e, familia, grupo), fila in mw.iterrows():
    if e == REFERENCIA:
        continue
    registro = {'escenario': e, 'familia': familia, 'grupo': grupo,
                'sin_dc_MW': mw.loc[(REFERENCIA, familia, grupo), 'base'].sum()
                if (REFERENCIA, familia, grupo) in mw.index else 0.0,
                'base_MW': fila['base'].sum(), 'libre_MW': fila['libre'].sum()}
    registro['dif_MW'] = registro['libre_MW'] - registro['base_MW']
    for p in PERIODOS:
        registro[f'dif_{p}'] = fila.get(('libre', p), 0.0) - fila.get(('base', p), 0.0)
    filas.append(registro)
dif_inv = pd.DataFrame(filas)
dif_inv = dif_inv[(dif_inv[['base_MW', 'libre_MW']].abs() > 0.5).any(axis=1)]
dif_inv['orden_familia'] = dif_inv['familia'].map(FAMILIAS.index)
dif_inv = dif_inv.sort_values(['escenario', 'orden_familia', 'grupo']).drop(columns='orden_familia')
guardar(dif_inv, 'inversiones_libre_menos_base.csv')


# =====================================================================================================
# 7. Transmisión: ampliación por corredor y período
# =====================================================================================================
# BuildTx.csv: MW agregados a cada corredor en cada período (incluye obras comprometidas, que en
# trans_build_limits.csv son min_build_mw). Inversión overnight = MW x costo por MW del corredor
# (trans_capital_cost_per_mw_km x largo x multiplicador de terreno, como en Switch), sin descontar.
lineas = pd.read_csv(ENTRADAS / 'transmission_lines.csv').set_index('TRANSMISSION_LINE')
parametros_tx = pd.read_csv(ENTRADAS / 'trans_params.csv').iloc[0]
usd_por_mw = (parametros_tx['trans_capital_cost_per_mw_km'] * lineas['trans_length_km']
              * lineas['trans_terrain_multiplier'])
limites_tx = pd.read_csv(ENTRADAS / 'trans_build_limits.csv')
limites = limites_tx.set_index(['TRANSMISSION_LINE', 'PERIOD'])['min_build_mw']
# max_build_mw es acumulado (modulos/limites_transmision.py): el del último período es el tope total
tope_tx = limites_tx[limites_tx['PERIOD'] == limites_tx['PERIOD'].max()].set_index('TRANSMISSION_LINE')['max_build_mw']
# Corredor de norte a sur: zona del norte primero; orden del corredor = promedio del orden de sus zonas
corredores = pd.DataFrame({'zona_1': lineas['trans_lz1'], 'zona_2': lineas['trans_lz2']})
corredores['orden'] = (corredores['zona_1'].map(ORDEN) + corredores['zona_2'].map(ORDEN)) / 2
norte = corredores['zona_1'].map(ORDEN) <= corredores['zona_2'].map(ORDEN)
corredores['zona_norte'] = corredores['zona_1'].where(norte, corredores['zona_2'])
corredores['zona_sur'] = corredores['zona_2'].where(norte, corredores['zona_1'])
corredores['nombre'] = (corredores['zona_norte'].map(info_zona['nombre']) + ' – '
                        + corredores['zona_sur'].map(info_zona['nombre']))
corredores['capacidad_existente_MW'] = lineas['existing_trans_cap']
corredores['usd_por_MW'] = usd_por_mw

tx = []
for e, m in CASOS_MODOS:
    t = leer(e, m, 'BuildTx.csv')
    t.columns = ['corredor', 'periodo', 'MW_ampliados']
    tx.append(t.assign(escenario=e, modo=m))
tx = pd.concat(tx)
tx['MW_comprometidos'] = [limites.get((c, p), 0.0) for c, p in zip(tx['corredor'], tx['periodo'])]
tx['inversion_overnight_MMUSD'] = tx['MW_ampliados'] * tx['corredor'].map(usd_por_mw) / 1e6
tx = tx.join(corredores[['nombre', 'zona_norte', 'zona_sur', 'orden']], on='corredor')
columnas = ['escenario', 'modo', 'corredor', 'nombre', 'zona_norte', 'zona_sur', 'orden', 'periodo',
            'MW_ampliados', 'MW_comprometidos', 'inversion_overnight_MMUSD']
guardar(tx.loc[tx['MW_ampliados'] > 0.01, columnas].sort_values(['escenario', 'modo', 'orden', 'periodo']),
        'transmision_ampliaciones.csv')

# Libre - base por corredor: total 2026-2050, primer período con ampliación y diferencia por período
total_tx = tx.pivot_table(index='corredor', columns=['escenario', 'modo'], values='MW_ampliados', aggfunc='sum')
inv_tx = tx.pivot_table(index='corredor', columns=['escenario', 'modo'], values='inversion_overnight_MMUSD', aggfunc='sum')
por_periodo = tx.pivot_table(index=['corredor', 'periodo'], columns=['escenario', 'modo'], values='MW_ampliados')
primer = tx[tx['MW_ampliados'] > 1].groupby(['corredor', 'escenario', 'modo'])['periodo'].min()
ampliables = [c for c in corredores.sort_values('orden').index if c in total_tx.index]   # trans_new_build_allowed = 1
filas = []
for e in ESCENARIOS:
    for c in ampliables:
        registro = {'escenario': e, 'corredor': c, 'nombre': corredores.loc[c, 'nombre'],
                    'orden': corredores.loc[c, 'orden'],
                    'capacidad_existente_MW': corredores.loc[c, 'capacidad_existente_MW'],
                    'ampliacion_maxima_MW': tope_tx.get(c, float('nan')),
                    'sin_dc_MW': total_tx.loc[c, (REFERENCIA, 'base')],
                    'base_MW': total_tx.loc[c, (e, 'base')], 'libre_MW': total_tx.loc[c, (e, 'libre')]}
        registro['dif_MW'] = registro['libre_MW'] - registro['base_MW']
        registro['base_inversion_MMUSD'] = inv_tx.loc[c, (e, 'base')]
        registro['libre_inversion_MMUSD'] = inv_tx.loc[c, (e, 'libre')]
        registro['dif_inversion_MMUSD'] = registro['libre_inversion_MMUSD'] - registro['base_inversion_MMUSD']
        registro['primer_periodo_base'] = primer.get((c, e, 'base'))
        registro['primer_periodo_libre'] = primer.get((c, e, 'libre'))
        for p in PERIODOS:
            registro[f'dif_{p}'] = por_periodo.loc[(c, p), (e, 'libre')] - por_periodo.loc[(c, p), (e, 'base')]
        filas.append(registro)
dif_tx = pd.DataFrame(filas)
dif_tx = dif_tx[(dif_tx[['sin_dc_MW', 'base_MW', 'libre_MW']] > 0.5).any(axis=1)]
for caso in ['sin_dc', 'base', 'libre']:   # corredor ampliado hasta su tope (holgura menor a 1 MW)
    dif_tx[f'{caso}_en_tope'] = dif_tx[f'{caso}_MW'] >= dif_tx['ampliacion_maxima_MW'] - 1
guardar(dif_tx, 'transmision_libre_menos_base.csv')


# =====================================================================================================
# 8. Expansión por zona: MW nuevos de generación y almacenamiento (2026-2050)
# =====================================================================================================
por_zona = (construcciones.groupby(['escenario', 'modo', 'zona', 'periodo', 'tipo', 'familia'])['MW'].sum()
            .reset_index())
por_zona = por_zona[por_zona['MW'] > 0.001].join(info_zona, on='zona')
por_zona = por_zona[['escenario', 'modo', 'zona', 'nombre', 'orden', 'macrozona', 'periodo', 'tipo', 'familia', 'MW']]
guardar(por_zona.sort_values(['escenario', 'modo', 'orden', 'periodo', 'tipo']), 'expansion_por_zona.csv')

total_zona = construcciones.pivot_table(index='zona', columns=['escenario', 'modo', 'tipo'], values='MW',
                                        aggfunc='sum', fill_value=0.0)
filas = []
for e in ESCENARIOS:
    for z in zonas['zona']:
        registro = {'escenario': e, 'zona': z, 'nombre': info_zona.loc[z, 'nombre'],
                    'orden': info_zona.loc[z, 'orden'], 'macrozona': info_zona.loc[z, 'macrozona']}
        for tipo, corto in [('Generación', 'gen'), ('Almacenamiento', 'alm')]:
            valor = lambda caso, modo: total_zona[(caso, modo, tipo)].get(z, 0.0) if (caso, modo, tipo) in total_zona else 0.0
            registro[f'{corto}_sin_dc_MW'] = valor(REFERENCIA, 'base')
            registro[f'{corto}_base_MW'] = valor(e, 'base')
            registro[f'{corto}_libre_MW'] = valor(e, 'libre')
            registro[f'{corto}_dif_MW'] = registro[f'{corto}_libre_MW'] - registro[f'{corto}_base_MW']
        filas.append(registro)
dif_zona = pd.DataFrame(filas)
guardar(dif_zona, 'expansion_zona_libre_menos_base.csv')

macro = construcciones.join(info_zona['macrozona'], on='zona')
macro = macro.pivot_table(index=['escenario', 'modo', 'macrozona'], columns='tipo', values='MW', aggfunc='sum',
                          fill_value=0.0).reset_index()
macro['orden'] = macro['macrozona'].map({m: i for i, m in enumerate(zonas['macrozona'].unique(), 1)})
macro = macro.rename(columns={'Generación': 'generacion_MW', 'Almacenamiento': 'almacenamiento_MW'})
guardar(macro.sort_values(['escenario', 'modo', 'orden'])[
    ['escenario', 'modo', 'macrozona', 'orden', 'generacion_MW', 'almacenamiento_MW']], 'expansion_por_macrozona.csv')


# =====================================================================================================
# 9. Emisiones, demanda, vertimiento y energía no suministrada por período
# =====================================================================================================
# Vertimiento de solar y eólica = energía disponible - energía despachada. La disponible se calcula
# igual que el límite de despacho de Switch (no_commit.py): capacidad x (1 - tasa de falla forzada) x
# factor de planta de cada hora, ponderado por el peso de la hora. El vertimiento hídrico es el agua no
# turbinada (SpillHydro.csv) más lo no despachado de las centrales de pasada candidatas (variables).
factores = pd.read_csv(ENTRADAS / 'variable_capacity_factors.csv')
factores = factores.merge(horas[['timepoint_id', 'periodo', 'peso']], left_on='timepoint', right_on='timepoint_id')
factores['MWh_por_MW'] = factores['gen_max_capacity_factor'] * factores['peso']
disponible_por_MW = factores.groupby(['GENERATION_PROJECT', 'periodo'])['MWh_por_MW'].sum()

filas, balances_macro = [], []
for e, m in CASOS_MODOS:
    anual = next(d for d in detalle_energia if d['escenario'].iat[0] == e and d['modo'].iat[0] == m)
    variables = anual[anual['generation_project'].map(proyectos['es_variable'])].copy()
    clave = pd.MultiIndex.from_arrays([variables['generation_project'], variables['period']])
    variables['disponible_GWh'] = (variables['GenCapacity_MW'] * variables['generation_project'].map(proyectos['disponibilidad'])
                                   * disponible_por_MW.reindex(clave).fillna(0).values / 1000)
    variables['vertido_GWh'] = variables['disponible_GWh'] - variables['Energy_GWh_typical_yr']
    if variables['vertido_GWh'].min() < -1e-3:
        raise ValueError(f'{e} {m}: despacho mayor que lo disponible en algún proyecto variable')
    vert = variables.groupby(['period', 'familia'])[['disponible_GWh', 'vertido_GWh']].sum()

    derrame = leer(e, m, 'SpillHydro.csv')
    derrame.columns = ['proyecto', 'timepoint', 'MW']
    derrame = derrame.merge(horas, left_on='timepoint', right_on='timepoint_id')
    derrame_GWh = (derrame['MW'] * derrame['peso']).groupby(derrame['periodo']).sum() / 1000

    balance = leer(e, m, 'load_balance.csv').merge(horas[['timestamp', 'periodo', 'peso']], on='timestamp')
    ponderado = lambda columna: (balance[columna] * balance['peso']).groupby(balance['periodo']).sum() / 1000
    demanda, dc, ens, carga = ponderado('zone_demand_mw'), ponderado('DCCarga'), ponderado('UnservedLoad'), ponderado('StorageNetCharge')
    inyeccion = ponderado('ZoneTotalCentralDispatch')
    emisiones = leer(e, m, 'emissions.csv').set_index('PERIOD')['AnnualEmissions_tCO2_per_yr'] / 1e6

    # Balance por macrozona: TXPowerNet es la potencia neta que entra a la zona por transmisión
    # (importación - exportación); la exportación neta es su opuesto.
    balance['macrozona'] = balance['load_zone'].map(info_zona['macrozona'])
    for columna in ['ZoneTotalCentralDispatch', 'StorageNetCharge', 'zone_demand_mw', 'DCCarga', 'TXPowerNet']:
        balance[columna + '_GWh'] = balance[columna] * balance['peso'] / 1000
    por_macro = balance.groupby(['periodo', 'macrozona'])[
        ['ZoneTotalCentralDispatch_GWh', 'StorageNetCharge_GWh', 'zone_demand_mw_GWh', 'DCCarga_GWh', 'TXPowerNet_GWh']].sum()
    por_macro = pd.DataFrame({
        'inyeccion_GWh': por_macro['ZoneTotalCentralDispatch_GWh'],
        'carga_almacenamiento_GWh': por_macro['StorageNetCharge_GWh'],
        'demanda_sin_dc_GWh': por_macro['zone_demand_mw_GWh'], 'demanda_dc_GWh': por_macro['DCCarga_GWh'],
        'exportacion_neta_GWh': -por_macro['TXPowerNet_GWh']}).reset_index()
    balances_macro.append(por_macro.assign(escenario=e, modo=m))

    gen = anual[~anual['es_almacenamiento']]
    for p in PERIODOS:
        generacion_p = gen.loc[gen['period'] == p, 'Energy_GWh_typical_yr'].sum()
        renovable_p = gen.loc[(gen['period'] == p) & (gen['familia'].isin(RENOVABLES) | gen['grupo'].isin(RENOVABLES)),
                              'Energy_GWh_typical_yr'].sum()
        # Control del balance anual: inyecciones - carga de almacenamiento = demanda + data centers - ENS
        desbalance = inyeccion[p] - carga[p] - (demanda[p] + dc[p] - ens[p])
        if abs(desbalance) > 1:
            raise ValueError(f'{e} {m} {p}: el balance anual no cierra ({desbalance:.1f} GWh)')
        v = lambda familia, col: vert[col].get((p, familia), 0.0)
        disponible_vre = v('Solar', 'disponible_GWh') + v('Eólica', 'disponible_GWh')
        vertido_vre = v('Solar', 'vertido_GWh') + v('Eólica', 'vertido_GWh')
        filas.append({
            'escenario': e, 'modo': m, 'periodo': p, 'anios_periodo': ANIOS[p],
            'emisiones_MtCO2_anio': emisiones[p],
            'demanda_sin_dc_GWh': demanda[p], 'demanda_dc_GWh': dc[p], 'demanda_total_GWh': demanda[p] + dc[p],
            'generacion_GWh': generacion_p, 'renovable_pct': 100 * renovable_p / generacion_p,
            'carga_almacenamiento_GWh': carga[p],
            'perdidas_almacenamiento_GWh': carga[p] - (inyeccion[p] - generacion_p),
            'vertimiento_solar_GWh': v('Solar', 'vertido_GWh'), 'vertimiento_eolico_GWh': v('Eólica', 'vertido_GWh'),
            'vertimiento_solar_eolico_pct': 100 * vertido_vre / disponible_vre if disponible_vre else 0.0,
            'vertimiento_hidro_GWh': derrame_GWh.get(p, 0.0) + v('Hidro', 'vertido_GWh'),
            'energia_no_suministrada_GWh': ens[p],
        })
operacion = pd.DataFrame(filas)
guardar(operacion, 'emisiones_vertimiento.csv')

balances_macro = pd.concat(balances_macro)
balances_macro['orden'] = balances_macro['macrozona'].map({m: i for i, m in enumerate(zonas['macrozona'].unique(), 1)})
balances_macro = balances_macro.sort_values(['escenario', 'modo', 'periodo', 'orden'])
guardar(balances_macro[['escenario', 'modo', 'periodo', 'macrozona', 'orden', 'inyeccion_GWh', 'carga_almacenamiento_GWh',
                        'demanda_sin_dc_GWh', 'demanda_dc_GWh', 'exportacion_neta_GWh']], 'balance_por_macrozona.csv')


# =====================================================================================================
# 10. Precios: carga plana por zona y precio medio en las zonas con data centers
# =====================================================================================================
# precio_carga_plana_usd_mwh (de modulos/precios.py) es el promedio de los duales del balance de la
# zona, ponderado por horas: lo que cuesta abastecer 1 MW plano adicional en esa zona, incluida la
# inversión que el modelo tendría que hacer para ello (es un modelo de expansión).
precios = []
for e, m in CASOS_MODOS:
    t = leer(e, m, 'precios_zonales_anuales.csv')
    t.columns = ['zona', 'periodo', 'precio_carga_plana_usd_mwh']
    precios.append(t.assign(escenario=e, modo=m))
precios = pd.concat(precios).join(info_zona, on='zona')
precios = precios[['escenario', 'modo', 'zona', 'nombre', 'orden', 'macrozona', 'periodo', 'precio_carga_plana_usd_mwh']]
guardar(precios.sort_values(['escenario', 'modo', 'periodo', 'orden']), 'precios_zonales.csv')

# Precio medio de las zonas con data centers, ponderado por sus MW, en el propio caso y en SIN_DC
precio_ref = precios[precios.escenario == REFERENCIA].set_index(['zona', 'periodo'])['precio_carga_plana_usd_mwh']
filas = []
for e in ESCENARIOS:
    for m in ('base', 'libre'):
        ubic = leer(e, m, 'dc_ubicacion.csv').rename(columns={'LOAD_ZONE': 'zona', 'PERIOD': 'periodo'})
        propio = precios[(precios.escenario == e) & (precios.modo == m)].set_index(['zona', 'periodo'])['precio_carga_plana_usd_mwh']
        clave = pd.MultiIndex.from_arrays([ubic['zona'], ubic['periodo']])
        ubic['precio_caso'] = propio.reindex(clave).values
        ubic['precio_sin_dc'] = precio_ref.reindex(clave).values
        for p, g in ubic.groupby('periodo'):
            peso = g['dc_total_mw']
            filas.append({'escenario': e, 'modo': m, 'periodo': p, 'dc_MW': peso.sum(),
                          'precio_dc_usd_mwh': (g['precio_caso'] * peso).sum() / peso.sum(),
                          'precio_sin_dc_en_zonas_dc_usd_mwh': (g['precio_sin_dc'] * peso).sum() / peso.sum()})
guardar(pd.DataFrame(filas), 'precio_dc.csv')


# =====================================================================================================
# 11. Resumen por caso
# =====================================================================================================
ultimo = PERIODOS[-1]
filas = []
for e, m in CASOS_MODOS:
    cap = matriz[(matriz.escenario == e) & (matriz.modo == m) & (matriz.periodo == ultimo)]
    op = operacion[(operacion.escenario == e) & (operacion.modo == m)].set_index('periodo')
    obra = construcciones[(construcciones.escenario == e) & (construcciones.modo == m)]
    ampl = tx[(tx.escenario == e) & (tx.modo == m)]
    dc = escenarios_dc[(escenarios_dc.escenario == e) & (escenarios_dc.periodo == ultimo)]
    filas.append({
        'escenario': e, 'modo': m,
        'costo_total_MMUSD': costo_total[(e, m)],
        'costo_extra_vs_sin_dc_MMUSD': costo_total[(e, m)] - costo_total[(REFERENCIA, 'base')],
        f'dc_{ultimo}_MW': dc['dc_total_MW'].sum(),
        f'capacidad_generacion_{ultimo}_MW': cap.loc[cap.familia != 'Almacenamiento', 'capacidad_MW'].sum(),
        f'capacidad_almacenamiento_{ultimo}_MW': cap.loc[cap.familia == 'Almacenamiento', 'capacidad_MW'].sum(),
        f'capacidad_almacenamiento_{ultimo}_MWh': cap.loc[cap.familia == 'Almacenamiento', 'almacenamiento_MWh'].sum(),
        f'eolica_{ultimo}_MW': cap.loc[cap.familia == 'Eólica', 'capacidad_MW'].sum(),
        f'solar_{ultimo}_MW': cap.loc[cap.familia == 'Solar', 'capacidad_MW'].sum(),
        f'renovable_{ultimo}_pct': op.loc[ultimo, 'renovable_pct'],
        'generacion_nueva_MW': obra.loc[obra.tipo == 'Generación', 'MW'].sum(),
        'almacenamiento_nuevo_MW': obra.loc[obra.tipo == 'Almacenamiento', 'MW'].sum(),
        'transmision_ampliada_MW': ampl['MW_ampliados'].sum(),
        'transmision_inversion_overnight_MMUSD': ampl['inversion_overnight_MMUSD'].sum(),
        'emisiones_acumuladas_MtCO2': (op['emisiones_MtCO2_anio'] * op['anios_periodo']).sum(),
        f'vertimiento_solar_eolico_{ultimo}_pct': op.loc[ultimo, 'vertimiento_solar_eolico_pct'],
        'vertimiento_solar_eolico_acumulado_TWh': ((op['vertimiento_solar_GWh'] + op['vertimiento_eolico_GWh'])
                                                   * op['anios_periodo']).sum() / 1000,
    })
guardar(pd.DataFrame(filas), 'resumen_casos.csv')


# =====================================================================================================
# 12. Entorno de cómputo de cada corrida (de los logs de Switch y Gurobi)
# =====================================================================================================
PATRONES = {
    'gurobi_version': r'Gurobi Optimizer version (\S+)',
    'procesador': r'CPU model: ([^,\n]+)',
    'nucleos_fisicos': r'Thread count: (\d+) physical cores',
    'procesadores_logicos': r'physical cores, (\d+) logical processors',
    'hilos': r'using up to (\d+) threads',
    'metodo': r'Set parameter Method to value (\d+)',
}
filas = []
for e, m in CASOS_MODOS:
    texto = (CASOS / e / f'log_{m}.txt').read_text(encoding='utf-8', errors='ignore')
    fila = {'escenario': e, 'modo': m}
    for nombre, patron in PATRONES.items():
        hallado = re.search(patron, texto)
        fila[nombre] = hallado.group(1).strip() if hallado else None
    filas.append(fila)
guardar(pd.DataFrame(filas), 'entorno_computo.csv')
