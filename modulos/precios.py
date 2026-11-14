"""Exporta los precios marginales de energía por zona y hora (duales del balance de cada zona).

El objetivo de Switch está en valor presente al año base, así que el dual del balance de la zona z
en la hora t está en USD de VP por MW. Para llevarlo a USD/MWh del año en que ocurre se divide por
bring_timepoint_costs_to_base_year[t] (peso de la hora en el año x factor que lleva un costo anual
del período a VP), como hace Switch en su módulo de respuesta de demanda.

Requiere correr con --suffixes dual. Escribe:
    precios_nodales.csv      LOAD_ZONE, TIMEPOINT, PERIOD, precio_usd_mwh
    precios_zonales_anuales.csv  LOAD_ZONE, PERIOD, precio_medio_usd_mwh (ponderado por horas),
                                 precio_medio_carga_plana_usd_mwh (= costo de abastecer 1 MW plano)
También exporta el dual del total ubicable de data centers (modo libre), en USD de VP por MW medio.
"""
import os

from pyomo.environ import value


def post_solve(m, outdir):
    if not hasattr(m, 'dual'):
        return
    filas = []
    for z in m.LOAD_ZONES:
        for t in m.TIMEPOINTS:
            restriccion = m.Zone_Energy_Balance[z, t]
            if restriccion not in m.dual:
                continue
            precio = m.dual[restriccion] / value(m.bring_timepoint_costs_to_base_year[t])
            filas.append((z, t, m.tp_period[t], precio, value(m.tp_weight_in_year[t])))
    with open(os.path.join(outdir, 'precios_nodales.csv'), 'w', encoding='utf-8') as f:
        f.write('LOAD_ZONE,TIMEPOINT,PERIOD,precio_usd_mwh\n')
        for z, t, p, precio, _ in filas:
            f.write(f'{z},{t},{p},{precio:.4f}\n')

    # Promedio ponderado por horas = lo que paga una carga plana de 1 MW por MWh.
    acumulado = {}
    for z, t, p, precio, peso in filas:
        suma, horas = acumulado.get((z, p), (0.0, 0.0))
        acumulado[(z, p)] = (suma + precio * peso, horas + peso)
    with open(os.path.join(outdir, 'precios_zonales_anuales.csv'), 'w', encoding='utf-8') as f:
        f.write('LOAD_ZONE,PERIOD,precio_carga_plana_usd_mwh\n')
        for (z, p), (suma, horas) in sorted(acumulado.items()):
            f.write(f'{z},{p},{suma / horas:.4f}\n')

    if hasattr(m, 'DC_Total_Ubicable'):
        with open(os.path.join(outdir, 'dual_dc_total.csv'), 'w', encoding='utf-8') as f:
            f.write('PERIOD,dual_usd_vp_por_mw\n')
            for p in m.PERIODS:
                c = m.DC_Total_Ubicable[p] if p in m.DC_Total_Ubicable else None
                if c is not None and c in m.dual:
                    f.write(f'{p},{m.dual[c]:.4f}\n')
