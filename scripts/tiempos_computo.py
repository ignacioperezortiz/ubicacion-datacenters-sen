"""Tiempos de cómputo y tamaño del problema de cada corrida (lee los logs de Switch y Gurobi).

Para cada caso (escenario x modo) extrae:
  - lectura de datos y construcción del modelo (s), según Switch;
  - tamaño del problema antes y después del presolve de Gurobi (filas, columnas, no ceros);
  - hilos usados, iteraciones de barrera, tiempo de barrera, de crossover y total de Gurobi (s);
  - tiempo total en el solver según Switch (incluye pasar el modelo a Gurobi) y posproceso (s);
  - tiempo de reloj de la corrida completa (min), del registro del lanzador (salida/corrida_*.txt).
Escribe resultados/<casos>/tiempos_computo.csv y un resumen en pantalla.
Uso: python scripts/tiempos_computo.py
"""
import re
import sys
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
CASOS = RAIZ / 'casos'
SALIDA = RAIZ / 'resultados' / 'tablas'
SALIDA.mkdir(parents=True, exist_ok=True)

PATRONES = {
    'lectura_datos_s': r'Data read in ([\d.]+) s',
    'construccion_modelo_s': r'Model instance constructed in ([\d.]+) s',
    'hilos': r'using up to (\d+) threads',
    'filas': r'Optimize a model with (\d+) rows',
    'columnas': r'Optimize a model with \d+ rows, (\d+) columns',
    'no_ceros': r'columns and (\d+) nonzeros',
    'filas_presolve': r'Presolved: (\d+) rows',
    'columnas_presolve': r'Presolved: \d+ rows, (\d+) columns',
    'iteraciones_barrera': r'Barrier solved model in (\d+) iterations',
    'barrera_s': r'Barrier solved model in \d+ iterations and ([\d.]+) seconds',
    'crossover_s': r'Crossover time: ([\d.]+) seconds',
    'gurobi_total_s': r'Solved in \d+ iterations and ([\d.]+) seconds',
    'solver_switch_s': r'Total time spent in solver: ([\d.]+) s',
    'posproceso_s': r'Completed post-solve processing in ([\d.]+) s',
}

# Tiempo de reloj y concurrencia, desde los registros del lanzador (última corrida de cada caso).
reloj = {}
# Los registros se leen en orden de nombre (corrida_1_..., corrida_2_..., corrida_registro.txt): la
# corrida más reciente de cada caso queda al final y es la que vale.
for registro in sorted((RAIZ / 'casos').glob('corrida_*.txt'), key=lambda p: p.name):
    lineas = [l for l in registro.read_text(encoding='utf-8').splitlines() if 'código' in l]
    for l in lineas:
        m = re.match(r'(\S+)\s+(\S+)\s+código (\d+)\s+([\d.]+) min', l)
        if m:
            reloj[(m.group(1), m.group(2))] = (float(m.group(4)), len(lineas), registro.name)

filas = []
for log in sorted(CASOS.glob('*/log_*.txt')):
    modo = log.stem.replace('log_', '')
    if modo not in ('base', 'libre'):
        continue   # logs de versiones anteriores (p. ej. _sin_llenado, _todo_libre)
    texto = log.read_text(encoding='utf-8', errors='ignore')
    fila = {'escenario': log.parent.name, 'modo': modo}
    for nombre, patron in PATRONES.items():
        m = re.search(patron, texto)
        fila[nombre] = float(m.group(1)) if m else None
    minutos, _, registro = reloj.get((log.parent.name, modo), (None, None, None))
    fila['reloj_total_min'] = minutos
    fila['registro_lanzador'] = registro
    filas.append(fila)

tabla = pd.DataFrame(filas)
tabla.to_csv(SALIDA / 'tiempos_computo.csv', index=False)
columnas = ['escenario', 'modo', 'hilos', 'registro_lanzador', 'construccion_modelo_s', 'barrera_s',
            'crossover_s', 'gurobi_total_s', 'solver_switch_s', 'posproceso_s', 'reloj_total_min']
print(tabla[columnas].round(1).to_string(index=False))
print('\nTamaño del problema (filas x columnas, no ceros), antes y después del presolve:')
print(tabla[['escenario', 'modo', 'filas', 'columnas', 'no_ceros', 'filas_presolve', 'columnas_presolve']]
      .astype({c: 'Int64' for c in ['filas', 'columnas', 'no_ceros', 'filas_presolve', 'columnas_presolve']})
      .to_string(index=False))
print(f"\nSuma del tiempo de reloj de las {tabla['reloj_total_min'].notna().sum()} corridas: "
      f"{tabla['reloj_total_min'].sum():.0f} min (si se corrieran una tras otra, con los mismos hilos)")
