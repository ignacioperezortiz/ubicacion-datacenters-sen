"""Límites de construcción de transmisión por corredor y período.

Switch permite construir en cualquier corredor con trans_new_build_allowed = 1, en cualquier período.
La PELP solo permite expandir los candidatos, cada uno desde un año mínimo y hasta su capacidad
máxima, y además tiene obras comprometidas con fecha. Este módulo impone:

    BuildTx[tx, p] >= min_build_mw[tx, p]                    obra comprometida que entra en p (incremental)
    sum_{q <= p} BuildTx[tx, q] <= max_build_mw[tx, p]       ampliación total permitida hasta p (acumulada)
    BuildTx[tx, p] = 0                                       si (tx, p) no está en el archivo

Archivo de entrada:
    trans_build_limits.csv   TRANSMISSION_LINE, PERIOD, min_build_mw, max_build_mw
"""
import os

from pyomo.environ import Constraint, NonNegativeReals, Param, Set


def define_components(m):
    m.TX_LIMITED_BLD_YRS = Set(dimen=2, within=m.TRANSMISSION_LINES * m.PERIODS)
    m.min_build_mw = Param(m.TX_LIMITED_BLD_YRS, within=NonNegativeReals, default=0.0)
    m.max_build_mw = Param(m.TX_LIMITED_BLD_YRS, within=NonNegativeReals)

    def minimo_y_sin_candidato(m, tx, p):
        if (tx, p) not in m.TX_LIMITED_BLD_YRS:
            return m.BuildTx[tx, p] == 0
        return m.BuildTx[tx, p] >= m.min_build_mw[tx, p]
    m.Tx_Minimo_Comprometido = Constraint(m.TRANS_BLD_YRS, rule=minimo_y_sin_candidato)

    def maximo_acumulado(m, tx, p):
        if (tx, p) not in m.TX_LIMITED_BLD_YRS:
            return Constraint.Skip
        construido = sum(m.BuildTx[tx, q] for q in m.PERIODS if q <= p and (tx, q) in m.TRANS_BLD_YRS)
        return construido <= m.max_build_mw[tx, p]
    m.Tx_Maximo_Acumulado = Constraint(m.TX_LIMITED_BLD_YRS, rule=maximo_acumulado)


def load_inputs(m, switch_data, inputs_dir):
    switch_data.load_aug(
        filename=os.path.join(inputs_dir, 'trans_build_limits.csv'),
        index=m.TX_LIMITED_BLD_YRS,
        param=(m.min_build_mw, m.max_build_mw))
