"""Reserva sistémica simple, sin compromiso de unidades (como en el curso).

En cada hora t del período p, la holgura de las centrales elegibles debe cubrir el requerimiento:

    subir:  sum_{g en E} (DispatchUpperLimit[g, t] - DispatchGen[g, t])
            + sum_{s en E y almacenamiento} ChargeStorage[s, t]               >= reserva_subir_mw[p]
    bajar:  sum_{g en E} (DispatchGen[g, t] - mínimo[g, t])      (mínimo = 0 sin compromiso de unidades)
            + sum_{s en E y almacenamiento} (límite de carga - ChargeStorage[s, t]) >= reserva_bajar_mw[p]

E son los proyectos elegibles. Un almacenamiento aporta a subir también dejando de cargar y a bajar
cargando más. No hay variables nuevas: la holgura se calcula con las variables de despacho.

Archivos de entrada:
    reserva_requerimiento.csv   PERIOD, reserva_subir_mw, reserva_bajar_mw
    reserva_elegibles.csv       RESERVE_GEN   (un proyecto por fila)
"""
import os

from pyomo.environ import Constraint, NonNegativeReals, Param, Set


def define_components(m):
    m.RESERVE_GENS = Set(dimen=1, within=m.GENERATION_PROJECTS)
    m.reserva_subir_mw = Param(m.PERIODS, within=NonNegativeReals, default=0.0)
    m.reserva_bajar_mw = Param(m.PERIODS, within=NonNegativeReals, default=0.0)


def define_dynamic_components(m):
    # Sin compromiso de unidades (no_commit) el despacho mínimo es 0; si hubiera un módulo de
    # compromiso, se usa su DispatchLowerLimit.
    # Las funciones auxiliares reciben el modelo como argumento: dentro de las reglas, `m` es la
    # instancia concreta; el `m` de afuera es el modelo abstracto y no se puede consultar.
    def minimo(inst, g, t):
        return inst.DispatchLowerLimit[g, t] if hasattr(inst, 'DispatchLowerLimit') else 0.0

    def carga_almacenamiento(inst, g, t):
        return hasattr(inst, 'ALL_STORAGE_GEN_TPS') and (g, t) in inst.ALL_STORAGE_GEN_TPS

    def reserva_subir(m, t):
        holgura = sum(m.DispatchUpperLimit[g, t] - m.DispatchGen[g, t]
                      for g in m.RESERVE_GENS if (g, t) in m.GEN_TPS)
        dejar_de_cargar = sum(m.ChargeStorage[g, t]
                              for g in m.RESERVE_GENS if carga_almacenamiento(m, g, t))
        return holgura + dejar_de_cargar >= m.reserva_subir_mw[m.tp_period[t]]
    m.Reserva_Subir = Constraint(m.TIMEPOINTS, rule=reserva_subir)

    def reserva_bajar(m, t):
        holgura = sum(m.DispatchGen[g, t] - minimo(m, g, t)
                      for g in m.RESERVE_GENS if (g, t) in m.GEN_TPS)
        cargar_mas = sum(
            m.DispatchUpperLimit[g, t] * m.gen_store_to_release_ratio[g] - m.ChargeStorage[g, t]
            for g in m.RESERVE_GENS if carga_almacenamiento(m, g, t))
        return holgura + cargar_mas >= m.reserva_bajar_mw[m.tp_period[t]]
    m.Reserva_Bajar = Constraint(m.TIMEPOINTS, rule=reserva_bajar)


def load_inputs(m, switch_data, inputs_dir):
    switch_data.load_aug(
        filename=os.path.join(inputs_dir, 'reserva_requerimiento.csv'),
        param=(m.reserva_subir_mw, m.reserva_bajar_mw))
    switch_data.load_aug(
        filename=os.path.join(inputs_dir, 'reserva_elegibles.csv'),
        set=m.RESERVE_GENS)
