"""Resultados de los 6 casos: 3 escenarios de data centers x (base, libre).

Para cada escenario compara el caso base (data centers donde dicen las proyecciones) con el libre
(el modelo elige su ubicación) y escribe tablas en resultados/:
  - costos.csv           costo total en VP y diferencia base - libre (el ahorro de ubicar bien)
  - costos_por_componente.csv   VP de cada componente del objetivo y su diferencia base - libre
  - costos_anuales.csv          costo anual (USD reales del año) por componente y período
  - costos_por_tecnologia.csv   VP por tecnología: inversión, O&M fijo y costo variable
El valor presente (VP) se calcula al año base de financials.csv (2025 desde el 17-nov-2026).
  - ubicacion_dc.csv     MW medios de data centers agregados por zona y período, en cada caso
  - capacidad.csv        capacidad instalada por tecnología y período (MW), base y libre
  - transmision.csv      capacidad por corredor y período (MW), base y libre, y su diferencia
  - precios.csv          precio que paga una carga plana (USD/MWh) por zona y período, caso base
  - operacion.csv        energía no suministrada y emisiones por período (el vertimiento está en analisis.py)
Uso: python scripts/resultados.py
"""
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
CASOS = RAIZ / 'casos'
SALIDA = RAIZ / 'resultados' / 'tablas'
SALIDA.mkdir(parents=True, exist_ok=True)
ESCENARIOS = [e for e in ['PELP_E2', 'CEN', 'PELP_N1', 'PROPIO'] if (CASOS / e).exists()]
REFERENCIA = 'SIN_DC'   # Carbono Neutralidad sin data centers proyectados (solo modo base)
MODOS = ['base', 'libre']


def leer(escenario, modo, archivo):
    ruta = CASOS / escenario / f'outputs_{modo}' / archivo
    return pd.read_csv(ruta) if ruta.exists() else None


# ---- Costos totales y diferencia ----
filas = []
for e in ESCENARIOS:
    costo = {}
    for modo in MODOS:
        ruta = CASOS / e / f'outputs_{modo}' / 'total_cost.txt'
        costo[modo] = float(ruta.read_text()) if ruta.exists() else float('nan')
    filas.append({'escenario': e, 'costo_base_MMUSD': costo['base'] / 1e6, 'costo_libre_MMUSD': costo['libre'] / 1e6,
                  'ahorro_MMUSD': (costo['base'] - costo['libre']) / 1e6,
                  'ahorro_pct': 100 * (costo['base'] - costo['libre']) / costo['base']})
costos = pd.DataFrame(filas)

# ---- Costo extra de los data centers respecto del sistema sin data centers ----
# extra_base  = costo base  - costo sin data centers  (los data centers donde dicen las proyecciones)
# extra_libre = costo libre - costo sin data centers  (los data centers donde conviene)
# El ahorro se expresa sobre el costo total y sobre el costo extra que agregan los data centers.
ruta_ref = CASOS / REFERENCIA / 'outputs_base' / 'total_cost.txt'
costo_ref = float(ruta_ref.read_text()) / 1e6 if ruta_ref.exists() else float('nan')
costos['costo_sin_dc_MMUSD'] = costo_ref
costos['extra_base_MMUSD'] = costos['costo_base_MMUSD'] - costo_ref
costos['extra_libre_MMUSD'] = costos['costo_libre_MMUSD'] - costo_ref
costos['ahorro_pct_del_extra'] = 100 * costos['ahorro_MMUSD'] / costos['extra_base_MMUSD']

# Energía de data centers agregada al modelo, en MWh de VP (para expresar el extra en USD/MWh).
periodos_f = pd.read_csv(CASOS / ESCENARIOS[0] / 'inputs' / 'periods.csv')
fin = pd.read_csv(CASOS / ESCENARIOS[0] / 'inputs' / 'financials.csv').iloc[0]
r, base_y = fin['discount_rate'], fin['base_financial_year']
f_vp = {p.INVESTMENT_PERIOD: (1 - (1 + r) ** -(p.period_end - p.period_start + 1)) / r * (1 + r) ** -(p.period_start - base_y)
        for p in periodos_f.itertuples()}
energia_vp = {}
for e in ESCENARIOS:
    u = leer(e, 'base', 'dc_ubicacion.csv')
    if u is not None:
        energia_vp[e] = (u.groupby('PERIOD')['dc_total_mw'].sum() * 8760 * u.groupby('PERIOD')['dc_total_mw'].sum().index.map(f_vp)).sum()
costos['energia_dc_vp_TWh'] = costos['escenario'].map(energia_vp) / 1e6
costos['extra_base_usd_mwh'] = costos['extra_base_MMUSD'] * 1e6 / (costos['energia_dc_vp_TWh'] * 1e6)
costos['extra_libre_usd_mwh'] = costos['extra_libre_MMUSD'] * 1e6 / (costos['energia_dc_vp_TWh'] * 1e6)
costos.to_csv(SALIDA / 'costos.csv', index=False)
print(f'== Costo total (VP {base_y:.0f}, millones de USD)\n', costos.round(2).to_string(index=False))

# ---- Costos por tipo: componentes del objetivo de Switch ----
NOMBRES = {
    'TotalGenFixedCosts': 'Generación y almacenamiento: inversión + O&M fijo',
    'StorageEnergyFixedCost': 'Almacenamiento: inversión + O&M fijo en energía (MWh)',
    'FuelCostsPerTP': 'Combustible',
    'FuelCostsPerPeriod': 'Combustible',
    'GenVariableOMCostsInTP': 'O&M variable',
    'EmissionsCosts': 'Impuesto al CO2',
    'TxFixedCosts': 'Transmisión: inversión + O&M fijo (incluye la existente)',
    'UnservedLoadPenalty': 'Energía no suministrada (VOLL)',
    'DCCostoAnual': 'Ubicación de data centers (conexión/terreno)',
}
componentes = []
for e in ESCENARIOS:
    for modo in MODOS:
        t = leer(e, modo, 'cost_components.csv')
        if t is not None:
            componentes.append(t.assign(escenario=e, modo=modo))
ref_comp = leer(REFERENCIA, 'base', 'cost_components.csv')
if ref_comp is not None:
    componentes.append(ref_comp.assign(escenario=REFERENCIA, modo='base'))
if componentes:
    componentes = pd.concat(componentes)
    componentes['tipo'] = componentes['component'].map(NOMBRES).fillna(componentes['component'])
    tabla = componentes.pivot_table(index='tipo', columns=['escenario', 'modo'], values='npv_cost', aggfunc='sum') / 1e6
    for e in ESCENARIOS:
        if (e, 'base') in tabla.columns and (e, 'libre') in tabla.columns:
            tabla[(e, 'base - libre')] = tabla[(e, 'base')] - tabla[(e, 'libre')]
            if (REFERENCIA, 'base') in tabla.columns:
                tabla[(e, 'extra base')] = tabla[(e, 'base')] - tabla[(REFERENCIA, 'base')]
                tabla[(e, 'extra libre')] = tabla[(e, 'libre')] - tabla[(REFERENCIA, 'base')]
    orden = ESCENARIOS + [REFERENCIA]
    tabla = tabla.reindex(columns=sorted(tabla.columns, key=lambda c: (orden.index(c[0]), c[1])))
    tabla.loc['TOTAL'] = tabla.sum()
    tabla.to_csv(SALIDA / 'costos_por_componente.csv')
    print(f'\n== Costos por tipo (VP {base_y:.0f}, millones de USD)\n', tabla.round(1).to_string())

# ---- Costo anual por período (USD reales de cada año) ----
anuales = []
for e in ESCENARIOS:
    for modo in MODOS:
        t = leer(e, modo, 'costs_itemized.csv')
        if t is not None:
            anuales.append(t.assign(escenario=e, modo=modo))
if anuales:
    anuales = pd.concat(anuales)
    anuales['tipo'] = anuales['Component'].map(NOMBRES).fillna(anuales['Component'])
    anuales.to_csv(SALIDA / 'costos_anuales.csv', index=False)
    tabla = anuales[anuales.modo == 'base'].pivot_table(index=['escenario', 'tipo'], columns='PERIOD',
                                                         values='AnnualCost_Real', aggfunc='sum') / 1e6
    print('\n== Costo anual por período, casos base (millones de USD reales por año)\n', tabla.round(0).to_string())

# ---- Costos por tecnología (VP del año base) ----
# Factor que lleva un costo anual constante de cada período a VP del año base, con la misma fórmula de Switch
# (financials.py): serie uniforme pagada a fin de año x valor presente del inicio del período.
periodos = pd.read_csv(CASOS / ESCENARIOS[0] / 'inputs' / 'periods.csv')
financiero = pd.read_csv(CASOS / ESCENARIOS[0] / 'inputs' / 'financials.csv').iloc[0]
tasa, anio_base = financiero['discount_rate'], financiero['base_financial_year']
factor_vp = {r.INVESTMENT_PERIOD: (1 - (1 + tasa) ** -(r.period_end - r.period_start + 1)) / tasa
             * (1 + tasa) ** -(r.period_start - anio_base) for r in periodos.itertuples()}
por_tec = []
for e in ESCENARIOS:
    entradas = CASOS / e / 'inputs'
    info = pd.read_csv(entradas / 'gen_info.csv', na_values='.').set_index('GENERATION_PROJECT')
    precio_comb = pd.read_csv(entradas / 'fuel_cost.csv').set_index(['load_zone', 'fuel', 'period'])['fuel_cost']
    impuesto = pd.read_csv(entradas / 'carbon_policies.csv').set_index('PERIOD')['carbon_cost_dollar_per_tco2']
    for modo in MODOS:
        cap_t = leer(e, modo, 'gen_cap.csv')
        anual = leer(e, modo, 'dispatch_gen_annual_summary.csv')   # energía y emisiones anuales por proyecto
        comp = leer(e, modo, 'cost_components.csv')
        if cap_t is None or anual is None:
            continue
        anual['heat_rate'] = anual['generation_project'].map(info['gen_full_load_heat_rate']).fillna(0)
        anual['fuel'] = anual['generation_project'].map(info['gen_energy_source'])
        anual['precio'] = [precio_comb.get((z, f, p), 0.0) for z, f, p in zip(anual['gen_load_zone'], anual['fuel'], anual['period'])]
        anual['combustible'] = anual['Energy_GWh_typical_yr'] * 1000 * anual['heat_rate'] * anual['precio']
        anual['co2'] = anual['DispatchEmissions_tCO2_per_typical_yr'] * anual['period'].map(impuesto)
        anual['f'] = anual['period'].map(factor_vp)
        cap_t['f'] = cap_t['PERIOD'].map(factor_vp)
        fila = pd.DataFrame({
            'inversion': (pd.to_numeric(cap_t['GenCapitalRecovery'], errors='coerce') * cap_t['f']).groupby(cap_t['gen_tech']).sum(),
            'om_fijo': (pd.to_numeric(cap_t['GenFixedOMCosts'], errors='coerce') * cap_t['f']).groupby(cap_t['gen_tech']).sum(),
            'om_variable': (anual['VariableCost_per_yr'] * anual['f']).groupby(anual['gen_tech']).sum(),
            'combustible': (anual['combustible'] * anual['f']).groupby(anual['gen_tech']).sum(),
            'impuesto_co2': (anual['co2'] * anual['f']).groupby(anual['gen_tech']).sum(),
        }).fillna(0) / 1e6
        fila['total'] = fila.sum(axis=1)
        # Control: la suma por tecnología debe reproducir los componentes del objetivo.
        if comp is not None:
            objetivo = comp.set_index('component')['npv_cost'] / 1e6
            for col, nombre in [('combustible', 'FuelCostsPerTP'), ('impuesto_co2', 'EmissionsCosts'),
                                ('om_variable', 'GenVariableOMCostsInTP')]:
                if nombre in objetivo and abs(fila[col].sum() - objetivo[nombre]) > 0.01 * max(1, objetivo[nombre]):
                    print(f'AVISO {e} {modo}: {col} por tecnología {fila[col].sum():.1f} != objetivo {objetivo[nombre]:.1f}')
        por_tec.append(fila.reset_index().rename(columns={'index': 'gen_tech'}).assign(escenario=e, modo=modo))
if por_tec:
    por_tec = pd.concat(por_tec)
    por_tec.to_csv(SALIDA / 'costos_por_tecnologia.csv', index=False)
    tabla = por_tec[por_tec.modo == 'base'].pivot_table(index='gen_tech', columns='escenario', values='total')
    print(f'\n== Costo por tecnología, casos base (VP {anio_base:.0f}, millones de USD)\n',
          tabla.round(0).sort_values(ESCENARIOS[0], ascending=False).to_string())

# ---- Ubicación de los data centers ----
ubic = []
for e in ESCENARIOS:
    for modo in MODOS:
        t = leer(e, modo, 'dc_ubicacion.csv')
        if t is not None:
            ubic.append(t.assign(escenario=e, modo=modo))
if ubic:
    ubic = pd.concat(ubic)
    ubic.to_csv(SALIDA / 'ubicacion_dc.csv', index=False)
    tabla = ubic.pivot_table(index=['escenario', 'modo', 'LOAD_ZONE'], columns='PERIOD', values='dc_total_mw',
                             aggfunc='sum').fillna(0)
    print('\n== Data centers agregados al modelo, fijos + ubicados (MW medios)\n', tabla.round(0).to_string())

# ---- Capacidad por tecnología ----
cap = []
for e in ESCENARIOS:
    for modo in MODOS:
        t = leer(e, modo, 'gen_cap.csv')
        if t is not None:
            cap.append(t.groupby(['gen_tech', 'PERIOD'])['GenCapacity'].sum().rename('MW').reset_index()
                       .assign(escenario=e, modo=modo))
if cap:
    cap = pd.concat(cap)
    cap.to_csv(SALIDA / 'capacidad.csv', index=False)
    dif = cap.pivot_table(index=['escenario', 'gen_tech'], columns=['PERIOD', 'modo'], values='MW', aggfunc='sum')
    cambio = pd.DataFrame({p: dif[(p, 'libre')] - dif[(p, 'base')] for p in sorted({c[0] for c in dif.columns})})
    cambio = cambio[(cambio.abs() > 1).any(axis=1)]
    print('\n== Capacidad: libre - base (MW), tecnologías que cambian\n', cambio.round(0).to_string())

# ---- Transmisión ----
tx = []
for e in ESCENARIOS:
    for modo in MODOS:
        t = leer(e, modo, 'transmission.csv')
        if t is not None:
            tx.append(t[['TRANSMISSION_LINE', 'PERIOD', 'TxCapacityNameplate']].assign(escenario=e, modo=modo))
if tx:
    tx = pd.concat(tx)
    tx.to_csv(SALIDA / 'transmision.csv', index=False)
    dif = tx.pivot_table(index=['escenario', 'TRANSMISSION_LINE'], columns=['PERIOD', 'modo'],
                         values='TxCapacityNameplate')
    cambio = pd.DataFrame({p: dif[(p, 'libre')] - dif[(p, 'base')] for p in sorted({c[0] for c in dif.columns})})
    cambio = cambio[(cambio.abs() > 1).any(axis=1)]
    print('\n== Transmisión: libre - base (MW)\n', cambio.round(0).to_string())

# ---- Precios de una carga plana por zona (caso base) ----
precios = []
for e in ESCENARIOS:
    for modo in MODOS:
        t = leer(e, modo, 'precios_zonales_anuales.csv')
        if t is not None:
            precios.append(t.assign(escenario=e, modo=modo))
if precios:
    precios = pd.concat(precios)
    precios.to_csv(SALIDA / 'precios.csv', index=False)
    p = precios[(precios.escenario == 'PELP_E2') & (precios.modo == 'base')].pivot(
        index='LOAD_ZONE', columns='PERIOD', values='precio_carga_plana_usd_mwh')
    print('\n== Precio de una carga plana, PELP_E2 base (USD/MWh)\n', p.round(1).sort_values(2040).to_string())

# ---- Operación: ENS, emisiones ----
oper = []
for e in ESCENARIOS:
    for modo in MODOS:
        ens = leer(e, modo, 'UnservedLoad.csv')
        resumen = leer(e, modo, 'dispatch_zonal_annual_summary.csv')
        if resumen is None:
            continue
        por_periodo = resumen.groupby('period').agg(
            energia_GWh=('Energy_GWh_typical_yr', 'sum'),
            emisiones_MtCO2=('DispatchEmissions_tCO2_per_typical_yr', lambda s: s.sum() / 1e6)).reset_index()
        por_periodo['ens_MW_max'] = ens.iloc[:, -1].max() if ens is not None else float('nan')
        oper.append(por_periodo.assign(escenario=e, modo=modo))
if oper:
    oper = pd.concat(oper)
    oper.to_csv(SALIDA / 'operacion.csv', index=False)
    print('\n== Operación por período\n', oper.round(2).to_string(index=False))
