"""Resuelve los casos de Switch: escenarios de data centers x modos (base y libre).

Cada corrida usa por omisión Gurobi (gurobipy 13, requiere licencia) con barrera y un número fijo de
hilos, para poder correr varias a la vez sin que compitan por todos los núcleos; --solver appsi_highs
usa HiGHS. Escribe el log de cada corrida en casos/<escenario>/log_<modo>.txt, las salidas en
casos/<escenario>/outputs_<modo>/ y una línea por corrida en casos/corrida_registro.txt.

Uso: python scripts/correr_casos.py [escenario ...] [--modos base libre] [--paralelo 3] [--hilos 6]
     [--solver gurobi_direct|appsi_highs] [--dc-libre-desde 2030]
"""
import argparse
import shutil
import sys
import os
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SWITCH = shutil.which('switch') or sys.exit('No se encontró el comando switch: instala los requisitos (README).')

parser = argparse.ArgumentParser()
parser.add_argument('escenarios', nargs='*', default=['SIN_DC', 'PELP_E2', 'CEN', 'PELP_N1', 'PROPIO'])
parser.add_argument('--modos', nargs='+', default=['base', 'libre'])
parser.add_argument('--paralelo', type=int, default=3)
parser.add_argument('--hilos', type=int, default=6)
parser.add_argument('--casos', default='casos', help='carpeta con un subdirectorio por escenario')
parser.add_argument('--dc-libre-desde', type=int, default=2030,
                    help='en modo libre, los períodos anteriores quedan con la ubicación base (comprometidos)')
parser.add_argument('--solver', default='gurobi_direct', help='gurobi_direct (recomendado) o appsi_highs (gratuito, más lento)')
args = parser.parse_args()
opciones_solver = f'Method=2 Threads={args.hilos}' if 'gurobi' in args.solver else f'threads={args.hilos}'


def correr(escenario, modo):
    caso = RAIZ / args.casos / escenario
    log = caso / f'log_{modo}.txt'
    comando = [str(SWITCH), 'solve', '--inputs-dir', 'inputs', '--outputs-dir', f'outputs_{modo}',
               '--solver', args.solver, '--dc-modo', modo, '--verbose', '--stream-solver',
               '--suffixes', 'dual',
               '--solver-options-string', opciones_solver,
               '--dc-libre-desde', str(args.dc_libre_desde)]
    entorno = dict(os.environ, PYTHONPATH=str(RAIZ), PYTHONUNBUFFERED='1')
    inicio = time.time()
    with open(log, 'w', encoding='utf-8') as salida:
        resultado = subprocess.run(comando, cwd=caso, env=entorno, stdout=salida, stderr=subprocess.STDOUT)
    minutos = (time.time() - inicio) / 60
    costo = caso / f'outputs_{modo}' / 'total_cost.txt'
    texto = costo.read_text().strip() if costo.exists() and resultado.returncode == 0 else 'sin solución'
    linea = f'{escenario:8} {modo:5}  código {resultado.returncode}  {minutos:5.1f} min  costo total {texto}'
    print(linea, flush=True)
    with open(RAIZ / 'casos' / 'corrida_registro.txt', 'a', encoding='utf-8') as registro:
        registro.write(linea + '\n')
    return escenario, modo, resultado.returncode, minutos, texto


trabajos = [(e, m) for m in args.modos for e in args.escenarios]
with ThreadPoolExecutor(max_workers=args.paralelo) as pool:
    resultados = list(pool.map(lambda t: correr(*t), trabajos))
