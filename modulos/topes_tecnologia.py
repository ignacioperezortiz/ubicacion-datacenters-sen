"""Topes de inversión por tecnología y período (suma de todas las zonas).

AMEBA limita cada año los MW nuevos de FV y eólica en todo el SEN (max_pv_penetration y
max_wind_penetration). Switch no tiene una restricción así: gen_capacity_limit_mw es por proyecto y
sobre la capacidad en operación. Este módulo impone, para cada fila (tecnología t, período p) del archivo:

    sum_{g: gen_tech[g] = t} BuildGen[g, p] <= max_build_mw[t, p]

Solo suma construcciones NUEVAS del propio período (NEW_GEN_BLD_YRS con build_year = p): las
predeterminadas no cuentan. Un período que no aparece en el archivo no tiene tope.
Cada fila es una restricción independiente. Si se quisiera un tope conjunto para varios gen_tech, habría
que agregar una columna de grupo; hoy no hace falta (FV = 'FV', eólica = 'Eolica').

Archivo de entrada (opcional; sin él, el módulo no agrega nada):
    topes_tecnologia.csv   gen_tech, PERIOD, max_build_mw
"""
import os

from pyomo.environ import Constraint, NonNegativeReals, Param, Set


def define_components(m):
    m.TECH_LIMITED_PERIODS = Set(dimen=2, within=m.GENERATION_TECHNOLOGIES * m.PERIODS)
    m.tech_max_build_mw = Param(m.TECH_LIMITED_PERIODS, within=NonNegativeReals)

    def tope_por_tecnologia(m, t, p):
        nuevos = [m.BuildGen[g, p] for g in m.GENS_BY_TECHNOLOGY[t] if (g, p) in m.NEW_GEN_BLD_YRS]
        if not nuevos:
            return Constraint.Skip
        return sum(nuevos) <= m.tech_max_build_mw[t, p]
    m.Tope_Inversion_Tecnologia = Constraint(m.TECH_LIMITED_PERIODS, rule=tope_por_tecnologia)


def load_inputs(m, switch_data, inputs_dir):
    # La columna se llama max_build_mw, pero el Param no puede llamarse igual (ya existe en
    # modulos.limites_transmision): por eso se indica la selección de columnas explícitamente.
    switch_data.load_aug(
        optional=True,
        filename=os.path.join(inputs_dir, 'topes_tecnologia.csv'),
        select=('gen_tech', 'PERIOD', 'max_build_mw'),
        index=m.TECH_LIMITED_PERIODS,
        param=(m.tech_max_build_mw,))
