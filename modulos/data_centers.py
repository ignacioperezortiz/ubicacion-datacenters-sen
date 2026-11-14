"""Demanda de data centers con ubicación fija (caso base) o elegida por el modelo (caso libre).

La demanda de data centers es una carga plana: el mismo valor en todas las horas de un período.
Se divide en dos partes:

- Parte comprometida (data centers que ya operan o ya tienen sitio): siempre fija en su zona.
- Parte ubicable: el total del sistema en cada período es un dato, pero su reparto entre zonas
  candidatas es una variable de decisión en el caso libre y un dato en el caso base.

Formulación (p: período, z: zona candidata, t: hora del período p):

    DCUbicado[z, p] >= 0                                   MW medios instalados en z al período p
    sum_z DCUbicado[z, p] = dc_libre_mw[p]                 el total ubicable es un dato
    DCUbicado[z, p] >= DCUbicado[z, p_anterior]            un data center no se traslada
    DCUbicado[z, p] <= dc_max_mw[z]                        si la zona tiene límite
    caso base: DCUbicado[z, p] = dc_base_mw[z, p]          la ubicación es la proyectada

    carga en el balance de la zona z en la hora t:  dc_fijo_mw[z, p] + DCUbicado[z, p]
    costo anual del período p:  sum_z dc_costo_anual_usd_mw[z] * DCUbicado[z, p]   (0 por omisión)

Archivos de entrada (en la carpeta inputs):
    dc_fijo.csv        LOAD_ZONE, PERIOD, dc_fijo_mw          (opcional)
    dc_libre.csv       PERIOD, dc_libre_mw
    dc_candidatas.csv  DC_ZONE, dc_max_mw (opcional), dc_costo_anual_usd_mw (opcional)
    dc_base.csv        DC_ZONE, PERIOD, dc_base_mw             (obligatorio en modo base)

Opción de línea de comandos: --dc-modo {base, libre}  (por omisión: base)
Salida: dc_ubicacion.csv con la carga de data centers por zona y período.
"""
import os

from pyomo.environ import (BuildCheck, Constraint, Expression, NonNegativeReals, Param, Set,
                           Var, value)


def define_arguments(argparser):
    argparser.add_argument(
        '--dc-modo', choices=['base', 'libre'], default='base',
        help='base: data centers donde dicen las proyecciones; libre: el modelo elige su ubicación.')
    argparser.add_argument(
        '--dc-libre-desde', type=int, default=None,
        help='En modo libre, los períodos anteriores a este año quedan con la ubicación base '
             '(data centers ya comprometidos). Por omisión, todos los períodos son libres.')


def define_components(m):
    # ---- Conjuntos y datos ----
    m.DC_ZONES = Set(dimen=1, within=m.LOAD_ZONES, doc='Zonas candidatas para la parte ubicable')
    m.dc_fijo_mw = Param(m.LOAD_ZONES, m.PERIODS, within=NonNegativeReals, default=0.0)
    m.dc_libre_mw = Param(m.PERIODS, within=NonNegativeReals, default=0.0)
    m.dc_max_mw = Param(m.DC_ZONES, within=NonNegativeReals, default=float('inf'))
    m.dc_costo_anual_usd_mw = Param(m.DC_ZONES, within=NonNegativeReals, default=0.0)
    m.dc_base_mw = Param(m.DC_ZONES, m.PERIODS, within=NonNegativeReals, default=0.0)

    # ---- Variable de ubicación (MW medios acumulados en cada zona) ----
    m.DCUbicado = Var(m.DC_ZONES, m.PERIODS, within=NonNegativeReals)

    # En el caso base la ubicación completa es dato, así que esta suma es redundante y se omite
    # (evita infactibilidades por redondeo entre dc_base y dc_libre).
    def total_ubicable(m, p):
        if m.options.dc_modo == 'base':
            return Constraint.Skip
        return sum(m.DCUbicado[z, p] for z in m.DC_ZONES) == m.dc_libre_mw[p]
    m.DC_Total_Ubicable = Constraint(m.PERIODS, rule=total_ubicable)

    def sin_traslado(m, z, p):
        anterior = m.PERIODS.prev(p) if p != m.PERIODS.first() else None
        if anterior is None:
            return Constraint.Skip
        return m.DCUbicado[z, p] >= m.DCUbicado[z, anterior]
    m.DC_Sin_Traslado = Constraint(m.DC_ZONES, m.PERIODS, rule=sin_traslado)

    def limite_zona(m, z, p):
        if m.dc_max_mw[z] == float('inf'):
            return Constraint.Skip
        return m.DCUbicado[z, p] <= m.dc_max_mw[z]
    m.DC_Limite_Zona = Constraint(m.DC_ZONES, m.PERIODS, rule=limite_zona)

    def ubicacion_base(m, z, p):
        comprometido = m.options.dc_libre_desde is not None and p < m.options.dc_libre_desde
        if m.options.dc_modo != 'base' and not comprometido:
            return Constraint.Skip
        return m.DCUbicado[z, p] == m.dc_base_mw[z, p]
    m.DC_Ubicacion_Base = Constraint(m.DC_ZONES, m.PERIODS, rule=ubicacion_base)

    # ---- Carga de data centers en el balance de cada zona y hora ----
    def carga(m, z, t):
        p = m.tp_period[t]
        ubicada = m.DCUbicado[z, p] if z in m.DC_ZONES else 0.0
        return m.dc_fijo_mw[z, p] + ubicada
    m.DCCarga = Expression(m.LOAD_ZONES, m.TIMEPOINTS, rule=carga)
    m.Zone_Power_Withdrawals.append('DCCarga')

    # ---- Comprobación de datos en el caso base ----
    # La ubicación base debe sumar el total ubicable de cada período (tolerancia 1e-3 MW) y no puede
    # decrecer entre períodos; si dc_base.csv falta, la suma da 0 y la comprobación lo detiene.
    def chequeo_base(m):
        if m.options.dc_modo != 'base':
            return True
        for p in m.PERIODS:
            suma = sum(m.dc_base_mw[z, p] for z in m.DC_ZONES)
            if abs(suma - m.dc_libre_mw[p]) > 1e-3:
                raise ValueError(f'dc_base suma {suma:.4f} MW en {p}, pero dc_libre es {m.dc_libre_mw[p]:.4f}')
            if p != m.PERIODS.first():
                anterior = m.PERIODS.prev(p)
                for z in m.DC_ZONES:
                    if m.dc_base_mw[z, p] < m.dc_base_mw[z, anterior] - 1e-6:
                        raise ValueError(f'dc_base decrece en {z} entre {anterior} y {p}')
        return True
    m.DC_Chequeo_Base = BuildCheck(rule=chequeo_base)

    # ---- Costo anual asociado a la ubicación (conexión, terreno; 0 si no se informa) ----
    m.DCCostoAnual = Expression(
        m.PERIODS,
        rule=lambda m, p: sum(m.dc_costo_anual_usd_mw[z] * m.DCUbicado[z, p] for z in m.DC_ZONES))
    m.Cost_Components_Per_Period.append('DCCostoAnual')


def load_inputs(m, switch_data, inputs_dir):
    switch_data.load_aug(
        filename=os.path.join(inputs_dir, 'dc_fijo.csv'), optional=True,
        param=(m.dc_fijo_mw,))
    switch_data.load_aug(
        filename=os.path.join(inputs_dir, 'dc_libre.csv'),
        param=(m.dc_libre_mw,))
    switch_data.load_aug(
        filename=os.path.join(inputs_dir, 'dc_candidatas.csv'),
        index=m.DC_ZONES,
        optional_params=('dc_max_mw', 'dc_costo_anual_usd_mw'),
        param=(m.dc_max_mw, m.dc_costo_anual_usd_mw))
    switch_data.load_aug(
        filename=os.path.join(inputs_dir, 'dc_base.csv'), optional=True,
        param=(m.dc_base_mw,))


def post_solve(m, outdir):
    with open(os.path.join(outdir, 'dc_ubicacion.csv'), 'w', encoding='utf-8') as f:
        f.write('LOAD_ZONE,PERIOD,dc_fijo_mw,dc_ubicado_mw,dc_total_mw\n')
        for z in m.LOAD_ZONES:
            for p in m.PERIODS:
                fijo = value(m.dc_fijo_mw[z, p])
                ubicado = value(m.DCUbicado[z, p]) if z in m.DC_ZONES else 0.0
                if fijo + ubicado > 1e-6:
                    f.write(f'{z},{p},{fijo:.3f},{ubicado:.3f},{fijo + ubicado:.3f}\n')
