"""Figuras del análisis: PNG (150 dpi) y SVG en resultados/figuras/.

Lee solo las tablas de resultados/tablas (las escriben resultados.py, tiempos_computo.py y
analisis.py; correrlos antes). Cada figura lleva un título con la conclusión, unidades en los ejes y
una nota con la fuente. Las cifras de los títulos se calculan de las tablas, no se escriben a mano.
  a_costo_extra_y_ahorro          costo extra de los data centers, ubicación proyectada frente a óptima
  b_ahorro_relativo               ahorro como % del costo extra, USD/MWh de data centers y por MWh reubicado
  c_ahorro_por_tipo_de_costo      de qué componentes del costo sale el ahorro
  d_matriz_capacidad              capacidad instalada por tecnología y período, en los 9 casos
  d2_capacidad_extra_2050         capacidad que agregan los data centers en 2050 frente al caso sin ellos
  e_inversion_libre_menos_base    MW construidos 2026-2050 por tecnología, libre - base
  f_transmision_por_corredor      MW ampliados por corredor 2026-2050, base frente a libre
  g_ubicacion_dc_por_zona         MW de data centers por zona en 2050, base frente a libre
  h_precio_carga_plana_2040       precio de una carga plana por zona en 2040, sin data centers
  i_demanda_dc                    trayectorias de demanda de data centers
  j_tiempos_computo               tiempo de cómputo de cada corrida, por etapa
Uso: python -I scripts/graficos.py
"""
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter, MaxNLocator

RAIZ = Path(__file__).resolve().parents[1]
TABLAS = RAIZ / 'resultados' / 'tablas'
FIGURAS = RAIZ / 'resultados' / 'figuras'
FIGURAS.mkdir(parents=True, exist_ok=True)

ESCENARIOS = ['PELP_E2', 'CEN', 'PELP_N1', 'PROPIO']   # de menor a mayor demanda de data centers
NOMBRE = {'SIN_DC': 'Sin data centers', 'PELP_E2': 'PELP E2', 'CEN': 'CEN', 'PELP_N1': 'PELP N1', 'PROPIO': 'PROPIO'}
FUENTE = 'Fuente: elaboración propia con Switch 2.0.9, red de 31 zonas de la PELP 2023-2027, escenario Carbono Neutralidad.'
NOTA_LIBRE = 'Libre: el modelo elige la zona de los data centers que se agregan desde 2030; lo de 2026 queda donde dice la proyección.'


# =====================================================================================================
# Estilo: paleta validada (dataviz, modo claro), tinta, grilla y tipografía
# =====================================================================================================
SUPERFICIE = '#fcfcfb'
TINTA, TINTA_2, TENUE = '#0b0b0b', '#52514e', '#898781'
GRILLA, EJE = '#e1e0d9', '#c3c2b7'
CATEGORICA = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300', '#6250d6', '#e34948']
TEXTO_SOBRE = ['#ffffff', '#ffffff', '#ffffff', '#0b0b0b', '#ffffff', '#ffffff', '#ffffff', '#ffffff']
AZUL_CLARO, AZUL_OSCURO = '#86b6ef', '#1c5cab'    # rampa azul, pasos 250 y 550: base -> libre
POSITIVO, NEGATIVO = '#2a78d6', '#e34948'           # polos divergentes azul / rojo
GRIS_DATO = '#c9c7bf'                               # dato de contexto (énfasis: el resto en gris)
COLOR_BASE, COLOR_LIBRE = AZUL_CLARO, AZUL_OSCURO
ETIQUETA_BASE = 'Base: ubicación proyectada'
ETIQUETA_LIBRE = 'Libre: ubicación óptima desde 2030'
FAMILIAS = ['Hidro', 'Gas', 'Eólica', 'Solar', 'Almacenamiento', 'Biomasa y otras', 'Carbón', 'Diésel']
COLOR_FAMILIA = dict(zip(FAMILIAS, CATEGORICA))     # orden fijo de la paleta, igual en todas las figuras

plt.rcParams.update({
    'font.family': ['Segoe UI', 'DejaVu Sans'], 'font.size': 9,
    'figure.facecolor': SUPERFICIE, 'axes.facecolor': SUPERFICIE, 'savefig.facecolor': SUPERFICIE,
    'axes.edgecolor': EJE, 'axes.linewidth': 0.8, 'axes.labelcolor': TINTA_2, 'axes.titlecolor': TINTA,
    'axes.titlesize': 9.5, 'axes.titleweight': 'semibold', 'axes.titlelocation': 'left',
    'axes.spines.top': False, 'axes.spines.right': False,
    'xtick.color': TENUE, 'ytick.color': TENUE, 'xtick.labelcolor': TINTA_2, 'ytick.labelcolor': TINTA_2,
    'xtick.major.size': 0, 'ytick.major.size': 0, 'xtick.major.pad': 4, 'ytick.major.pad': 4,
    'grid.color': GRILLA, 'grid.linewidth': 0.8, 'grid.linestyle': '-',
    'legend.frameon': False, 'legend.fontsize': 8.5, 'svg.fonttype': 'none',
})


def num(valor, decimales=0):
    """Número con separador de miles '.' y decimal ',' (1.234,5)."""
    texto = f'{valor:,.{decimales}f}'
    return texto.replace(',', '_').replace('.', ',').replace('_', '.')


def con_signo(valor, decimales=0):
    return ('+' if valor > 0 else '−' if valor < 0 else '') + num(abs(valor), decimales)


def rango(minimo, maximo, decimales=0):
    """'a–b' con formato español; si al redondear quedan iguales, 'unos a'."""
    a, b = num(minimo, decimales), num(maximo, decimales)
    return f'unos {a}' if a == b else f'{a}–{b}'


FORMATO_MILES = FuncFormatter(lambda v, _: num(v))
FORMATO_DECIMAL = FuncFormatter(lambda v, _: num(v, 0 if float(v).is_integer() else 1))


def figura(ancho, alto, filas=1, columnas=1, titulo_in=0.8, nota_in=0.45, **opciones):
    """Figura con layout restringido y franjas reservadas arriba (título) y abajo (nota)."""
    fig, ejes = plt.subplots(filas, columnas, figsize=(ancho, alto), layout='constrained', **opciones)
    fig.get_layout_engine().set(rect=(0, nota_in / alto, 1, 1 - (titulo_in + nota_in) / alto),
                                w_pad=0.06, h_pad=0.06)
    return fig, ejes


def titular(fig, titulo, subtitulo=None):
    alto = fig.get_figheight()
    fig.text(0.012, 1 - 0.14 / alto, titulo, ha='left', va='top', fontsize=12, fontweight='semibold', color=TINTA)
    if subtitulo:
        fig.text(0.012, 1 - 0.43 / alto, subtitulo, ha='left', va='top', fontsize=9, color=TINTA_2)


def anotar(fig, *lineas):
    alto = fig.get_figheight()
    fig.text(0.012, 0.06 / alto, '\n'.join(lineas + (FUENTE,)), ha='left', va='bottom', fontsize=7.5,
             color=TENUE, linespacing=1.4)


def guardar(fig, nombre):
    fig.savefig(FIGURAS / f'{nombre}.png', dpi=150)
    fig.savefig(FIGURAS / f'{nombre}.svg')
    plt.close(fig)
    print(f'  {nombre}')


def grilla(ax, eje):
    """Grilla fina solo en el eje de valores, detrás de los datos."""
    ax.grid(axis=eje)
    ax.set_axisbelow(True)
    if eje == 'x':
        ax.spines['left'].set_visible(False)
    else:
        ax.spines['bottom'].set_color(EJE)


def manija(texto, color, forma='parche'):
    if forma == 'punto':
        return Line2D([], [], marker='o', linestyle='none', markersize=6, color=color, label=texto)
    if forma == 'linea':
        return Line2D([], [], linewidth=2, color=color, label=texto)
    return Patch(facecolor=color, edgecolor='none', label=texto)


def leyenda(ax_o_fig, entradas, forma='parche', **opciones):
    manijas = [manija(texto, color, forma) for texto, color in entradas]
    return ax_o_fig.legend(handles=manijas, handlelength=1.0, handleheight=0.9, **opciones)


def leyenda_arriba(fig, entradas, forma='parche', ncols=None, con_subtitulo=True):
    """Leyenda en una fila (o más) bajo el título y el subtítulo, alineada a la izquierda."""
    desde_arriba = 0.68 if con_subtitulo else 0.45
    return leyenda(fig, entradas, forma, loc='upper left', bbox_to_anchor=(0.005, 1 - desde_arriba / fig.get_figheight()),
                   ncols=ncols or len(entradas), columnspacing=1.4, borderaxespad=0)


def tabla(nombre, **opciones):
    return pd.read_csv(TABLAS / nombre, **opciones)


costos = tabla('costos.csv').set_index('escenario').loc[ESCENARIOS]
resumen_dc = tabla('escenarios_dc_resumen.csv').set_index('escenario').loc[ESCENARIOS]
zonas = tabla('zonas.csv').set_index('zona')
print('Figuras en resultados/figuras:')


# =====================================================================================================
# (a) Costo extra de los data centers: ubicación proyectada frente a óptima
# =====================================================================================================
# Barra completa = costo extra con la ubicación proyectada (base - sin data centers). Tramo oscuro =
# costo extra con la ubicación óptima (libre - sin data centers). Tramo claro = ahorro (base - libre).
fig, ax = figura(8.2, 4.2, titulo_in=1.05)
y = np.arange(len(ESCENARIOS))[::-1]
alto_barra = 0.5
ax.barh(y, costos['extra_libre_MMUSD'], height=alto_barra, color=COLOR_LIBRE, edgecolor=SUPERFICIE, linewidth=1.2)
ax.barh(y, costos['ahorro_MMUSD'], left=costos['extra_libre_MMUSD'], height=alto_barra, color=COLOR_BASE,
        edgecolor=SUPERFICIE, linewidth=1.2)
maximo = costos['extra_base_MMUSD'].max()
for yi, (e, fila) in zip(y, costos.iterrows()):
    ax.text(fila['extra_libre_MMUSD'] - maximo * 0.012, yi, num(fila['extra_libre_MMUSD']), ha='right', va='center',
            color='white', fontsize=8.5)
    ax.text(fila['extra_base_MMUSD'] + maximo * 0.012, yi,
            f"base {num(fila['extra_base_MMUSD'])}  ·  ahorro {num(fila['ahorro_MMUSD'])} ({num(fila['ahorro_pct_del_extra'])} %)",
            ha='left', va='center', color=TINTA, fontsize=8.5)
ax.set_yticks(y, [f"{NOMBRE[e]}\n{num(resumen_dc.loc[e, 'dc_2050_MW'])} MW en 2050" for e in ESCENARIOS])
ax.set_xlim(0, maximo * 1.45)
ax.xaxis.set_major_formatter(FORMATO_MILES)
ax.set_xlabel('Costo extra frente al sistema sin data centers (millones de USD, VP 2026)')
grilla(ax, 'x')
leyenda_arriba(fig, [('Costo extra con la ubicación óptima (libre)', COLOR_LIBRE),
                     ('Ahorro de ubicar bien (base − libre)', COLOR_BASE)])
titular(fig, f"Ubicar bien los data centers ahorra entre {num(costos['ahorro_MMUSD'].min())} y "
             f"{num(costos['ahorro_MMUSD'].max())} millones de USD",
        'Barra completa: costo extra con la ubicación proyectada (base). Valor presente 2026 a tasa de 6 %.')
anotar(fig, NOTA_LIBRE)
guardar(fig, 'a_costo_extra_y_ahorro')


# =====================================================================================================
# (b) Ahorro relativo: % del costo extra, USD/MWh de data centers y USD por MWh reubicado
# =====================================================================================================
# Tres medidas de escala distinta: tres paneles con su propio eje, nunca un eje doble.
fig, ejes = figura(10.5, 4.0, 1, 3, sharey=True, titulo_in=1.05, nota_in=0.62)
paneles = [
    (ejes[0], 'Ahorro como % del costo extra', '% del costo extra con ubicación proyectada',
     costos['ahorro_pct_del_extra'], lambda v: f'{num(v)} %'),
    (ejes[2], 'Ahorro por MWh reubicado', 'USD por MWh reubicable (VP 2026)',
     resumen_dc['ahorro_usd_por_mwh_reubicable'], lambda v: num(v, 1)),
]
for ax, titulo, etiqueta, valores, formato in paneles:   # medidas del ahorro: otro tono, para no confundir con base/libre
    ax.barh(y, valores, height=0.42, color=CATEGORICA[2])
    for yi, v in zip(y, valores):
        ax.text(v + valores.max() * 0.03, yi, formato(v), ha='left', va='center', color=TINTA, fontsize=8.5)
    ax.set_xlim(0, valores.max() * 1.3)
    ax.xaxis.set_major_locator(MaxNLocator(5, integer=True))
    ax.set_title(titulo)
    ax.set_xlabel(etiqueta)
    grilla(ax, 'x')
ax = ejes[1]
for desplazamiento, columna, color in [(0.17, 'extra_base_usd_mwh', COLOR_BASE), (-0.17, 'extra_libre_usd_mwh', COLOR_LIBRE)]:
    ax.barh(y + desplazamiento, costos[columna], height=0.3, color=color)
    for yi, v in zip(y, costos[columna]):
        ax.text(v + 0.8, yi + desplazamiento, num(v, 1), ha='left', va='center', color=TINTA, fontsize=8)
ax.set_xlim(0, costos['extra_base_usd_mwh'].max() * 1.25)
ax.set_title('Costo extra por MWh de data centers')
ax.set_xlabel('USD por MWh de data centers (VP 2026)')
grilla(ax, 'x')
leyenda_arriba(fig, [(ETIQUETA_BASE, COLOR_BASE), (ETIQUETA_LIBRE, COLOR_LIBRE)])
ejes[0].set_yticks(y, [NOMBRE[e] for e in ESCENARIOS])
por_mwh = resumen_dc['ahorro_usd_por_mwh_reubicable']
titular(fig, f"Ubicar bien recorta entre {num(costos['ahorro_pct_del_extra'].min())} % y "
             f"{num(costos['ahorro_pct_del_extra'].max())} % del costo extra: "
             f"{rango(por_mwh.min(), por_mwh.max(), 1)} USD por cada MWh reubicado",
        'El costo por MWh reparte el costo extra en la energía de data centers 2026-2054, ambos en valor presente 2026.')
menos_reubicable = resumen_dc['reubicable_2050_pct'].idxmin()
anotar(fig, 'MWh reubicable: demanda de data centers agregada después de 2026, la única que el modelo puede ubicar. '
            f"{NOMBRE[menos_reubicable]} reubica solo el {num(resumen_dc.loc[menos_reubicable, 'reubicable_2050_pct'])} % "
            'de su demanda de 2050.')
guardar(fig, 'b_ahorro_relativo')


# =====================================================================================================
# (c) De dónde sale el ahorro, por tipo de costo
# =====================================================================================================
COMPONENTES = {   # nombre en costos_por_componente.csv -> nombre corto, en el orden fijo de la paleta
    'Generación y almacenamiento: inversión + O&M fijo': 'Inversión y O&M fijo de generación y almacenamiento',
    'Combustible': 'Combustible',
    'Transmisión: inversión + O&M fijo (incluye la existente)': 'Transmisión',
    'Impuesto al CO2': 'Impuesto al CO2',
    'O&M variable': 'O&M variable',
}
componentes = tabla('costos_por_componente.csv', header=[0, 1], index_col=0)
ahorro = pd.DataFrame({e: componentes[(e, 'base - libre')] for e in ESCENARIOS}).drop(index='TOTAL')
resto = ahorro.drop(index=list(COMPONENTES))
if (resto.abs() > 0.5).any().any():
    raise ValueError(f'Hay componentes con ahorro distinto de cero sin color asignado:\n{resto}')
ahorro = ahorro.loc[list(COMPONENTES)].rename(index=COMPONENTES)
participacion = 100 * ahorro / ahorro.sum()

fig, ax = figura(8.6, 4.2, titulo_in=1.35)
for yi, e in zip(y, ESCENARIOS):
    izquierda_pos, izquierda_neg = 0.0, 0.0
    for i, (componente, valor) in enumerate(participacion[e].items()):
        inicio = izquierda_pos if valor >= 0 else izquierda_neg + valor
        ax.barh(yi, abs(valor), left=inicio, height=0.5, color=CATEGORICA[i], edgecolor=SUPERFICIE, linewidth=1.5)
        if abs(valor) >= 7:   # la etiqueta solo va dentro si cabe
            ax.text(inicio + abs(valor) / 2, yi, f'{num(valor)} %', ha='center', va='center', fontsize=8,
                    color=TEXTO_SOBRE[i])
        if valor >= 0:
            izquierda_pos += valor
        else:
            izquierda_neg += valor
    ax.text(101.5, yi, f"{num(ahorro[e].sum())} MM USD", ha='left', va='center', color=TINTA, fontsize=8.5)
ax.set_yticks(y, [NOMBRE[e] for e in ESCENARIOS])
ax.set_xlim(min(0, participacion[participacion < 0].sum().min() if (participacion < 0).any().any() else 0), 116)
ax.set_xticks(range(0, 101, 20))
ax.set_xlabel('% del ahorro total (base − libre, VP 2026)')
grilla(ax, 'x')
leyenda_arriba(fig, [(c, CATEGORICA[i]) for i, c in enumerate(COMPONENTES.values())], ncols=3)
inversion_y_combustible = participacion.iloc[:2].sum()
titular(fig, f'Entre {num(inversion_y_combustible.min())} % y {num(inversion_y_combustible.max())} % del ahorro es '
             'menor inversión en generación y menos combustible',
        'Composición del ahorro (base − libre) según los componentes del costo total del sistema.')
anotar(fig, 'A la derecha, el ahorro total en millones de USD. Las etiquetas menores a 7 % se omiten; '
            'los valores están en costos_por_componente.csv.')
guardar(fig, 'c_ahorro_por_tipo_de_costo')


# =====================================================================================================
# (d) Matriz eficiente de capacidad por tecnología y período, en los 9 casos
# =====================================================================================================
matriz = tabla('matriz_generacion.csv')
capacidad = matriz.groupby(['escenario', 'modo', 'periodo', 'familia'])['capacidad_MW'].sum() / 1000   # GW
periodos = sorted(matriz['periodo'].unique())
casos = [('SIN_DC', 'base')] + [(e, m) for e in ESCENARIOS for m in ('base', 'libre')]
tope = capacidad.groupby(['escenario', 'modo', 'periodo']).sum().max()

fig, ejes = figura(8.6, 12.4, 5, 2, sharex=True, sharey=True, titulo_in=0.85, nota_in=0.62)
posiciones = [(0, 0)] + [(1 + i // 2, i % 2) for i in range(8)]
for (e, m), (fila, columna) in zip(casos, posiciones):
    ax = ejes[fila, columna]
    x = np.arange(len(periodos))
    abajo = np.zeros(len(periodos))
    for familia in FAMILIAS:
        valores = np.array([capacidad.get((e, m, p, familia), 0.0) for p in periodos])
        ax.bar(x, valores, bottom=abajo, width=0.55, color=COLOR_FAMILIA[familia], edgecolor=SUPERFICIE, linewidth=0.8)
        abajo += valores
    ax.text(x[-1], abajo[-1] + tope * 0.02, num(abajo[-1]), ha='center', va='bottom', fontsize=8, color=TINTA)
    ax.set_title(NOMBRE[e] if e == 'SIN_DC' else f"{NOMBRE[e]} · {'base' if m == 'base' else 'libre'}")
    ax.set_xticks(x, periodos)
    ax.set_ylim(0, tope * 1.12)
    ax.yaxis.set_major_locator(MaxNLocator(5))
    grilla(ax, 'y')
    if columna == 0:
        ax.set_ylabel('GW instalados')
ejes[0, 1].axis('off')
leyenda(ejes[0, 1], [(f, COLOR_FAMILIA[f]) for f in reversed(FAMILIAS)], loc='center left', ncols=2,
        title='Tecnología (de arriba abajo en la pila)', title_fontsize=8.5, alignment='left')
nueva = tabla('inversiones_por_tecnologia.csv')
decidida = nueva.groupby('familia')['MW_decididos'].sum()
familias_decididas = [f for f in FAMILIAS if decidida.get(f, 0) > 1]
titular(fig, 'La expansión eficiente es eólica, solar y almacenamiento en los 9 casos',
        'Capacidad instalada por tecnología y período (GW). Los data centers agrandan la matriz; su ubicación mueve '
        'el peso entre eólica y solar.')
anotar(fig, f"El modelo solo decide inversión nueva en {', '.join(f.lower() for f in familias_decididas)}; "
            'el resto es parque existente u obra comprometida.',
       'Almacenamiento en MW de descarga (baterías, bombeo). Biomasa y otras: biomasa, biogás, geotermia y cogeneración.')
guardar(fig, 'd_matriz_capacidad')


# =====================================================================================================
# (d2) Capacidad que agregan los data centers en 2050, frente al caso sin data centers
# =====================================================================================================
ultimo = periodos[-1]
cap_ultimo = capacidad.xs(ultimo, level='periodo').unstack('familia').fillna(0)
extra = cap_ultimo.sub(cap_ultimo.loc[('SIN_DC', 'base')], axis=1).drop(index=('SIN_DC', 'base'))
cambian = [f for f in FAMILIAS if (extra[f].abs() > 0.01).any()]
if (extra[cambian] < -0.01).any().any():
    raise ValueError('La figura d2 apila aumentos de capacidad; hay familias que disminuyen frente a SIN_DC')
dc_2050 = resumen_dc['dc_2050_MW'] / 1000
fig, ax = figura(8.4, 4.8, titulo_in=1.05)
filas = [(e, m) for e in ESCENARIOS for m in ('base', 'libre')]
yy = []
for i, (e, m) in enumerate(filas):
    yi = -(i * 1.0 + (i // 2) * 0.6)
    yy.append(yi)
    izquierda = 0.0
    for familia in cambian:
        valor = extra.loc[(e, m), familia]
        ax.barh(yi, valor, left=izquierda, height=0.62, color=COLOR_FAMILIA[familia], edgecolor=SUPERFICIE, linewidth=1.2)
        izquierda += valor
    razon = extra.loc[(e, m)].sum() / dc_2050[e]
    ax.text(izquierda + 0.12, yi, f"{num(extra.loc[(e, m)].sum(), 1)} GW · {num(razon, 1)} MW por MW de data center",
            ha='left', va='center', fontsize=8, color=TINTA)
ax.set_yticks(yy, [f"{NOMBRE[e]} · {m}" for e, m in filas])
ax.set_xlim(0, extra.sum(axis=1).max() * 1.5)
ax.set_xlabel(f'Capacidad adicional en {ultimo} frente al caso sin data centers (GW)')
grilla(ax, 'x')
leyenda_arriba(fig, [(f, COLOR_FAMILIA[f]) for f in cambian])
razon_base = extra.xs('base', level=1).sum(axis=1) / dc_2050
razon_libre = extra.xs('libre', level=1).sum(axis=1) / dc_2050
titular(fig, f'Con ubicación óptima, cada MW de data center exige {rango(razon_libre.min(), razon_libre.max(), 1)} MW '
             f'de capacidad en vez de {rango(razon_base.min(), razon_base.max(), 1)}',
        f'Capacidad instalada en {ultimo} por encima del caso sin data centers, por tecnología. '
        'Almacenamiento en MW de descarga.')
anotar(fig, 'Las demás tecnologías tienen la misma capacidad que en el caso sin data centers.')
guardar(fig, 'd2_capacidad_extra_2050')


# =====================================================================================================
# (e) Cambios en inversión por tecnología, libre - base (MW construidos 2026-2050)
# =====================================================================================================
dif_inv = tabla('inversiones_libre_menos_base.csv')
dif_inv = dif_inv[dif_inv.groupby('grupo')['dif_MW'].transform(lambda s: s.abs().max()) > 1]
grupos = list(dict.fromkeys(dif_inv['grupo']))
alcance = dif_inv['dif_MW'].abs().max() / 1000
fig, ejes = figura(10.2, 3.6, 1, 4, sharey=True, titulo_in=1.05, nota_in=0.62)
yg = np.arange(len(grupos))[::-1]
for ax, e in zip(ejes, ESCENARIOS):
    valores = dif_inv[dif_inv.escenario == e].set_index('grupo')['dif_MW'].reindex(grupos).fillna(0) / 1000
    ax.barh(yg, valores, height=0.5, color=[POSITIVO if v >= 0 else NEGATIVO for v in valores])
    for yi, v in zip(yg, valores):
        if abs(v) >= 0.05:   # bajo 50 MW la barra no se ve y la etiqueta diría ±0,0
            ax.text(v + (0.06 if v >= 0 else -0.06) * alcance, yi, con_signo(v, 1), ha='left' if v >= 0 else 'right',
                    va='center', fontsize=8, color=TINTA)
    ax.axvline(0, color=EJE, linewidth=0.8)
    ax.set_xlim(-alcance * 1.55, alcance * 1.55)
    ax.set_title(NOMBRE[e])
    ax.set_xlabel('GW, libre − base')
    grilla(ax, 'x')
ejes[0].set_yticks(yg, grupos)
leyenda_arriba(fig, [('Se construye más con ubicación óptima', POSITIVO), ('Se construye menos', NEGATIVO)])
eolica = dif_inv[dif_inv.grupo == 'Eólica'].set_index('escenario')['dif_MW'] / 1000
solar = dif_inv[dif_inv.grupo == 'Solar FV'].set_index('escenario')['dif_MW'] / 1000
titular(fig, 'Con ubicación óptima se construye más eólica y menos solar y bombeo',
        f"Capacidad construida 2026-2050, libre − base (GW). Eólica: {con_signo(eolica.min(), 1)} a {con_signo(eolica.max(), 1)} GW; "
        f"solar FV: {con_signo(solar.max(), 1)} a {con_signo(solar.min(), 1)} GW.")
anotar(fig, 'Incluye reposiciones dentro del horizonte (las baterías duran 15 años). Gas, carbón, biomasa e hidro no cambian. '
            'Sin etiqueta: menos de 50 MW.')
guardar(fig, 'e_inversion_libre_menos_base')


# =====================================================================================================
# (f) Transmisión ampliada por corredor (base frente a libre), de norte a sur
# =====================================================================================================
dif_tx = tabla('transmision_libre_menos_base.csv')
visibles = dif_tx.groupby('corredor')[['base_MW', 'libre_MW']].max().max(axis=1) > 1
dif_tx = dif_tx[dif_tx['corredor'].map(visibles)]
orden_corr = dif_tx.drop_duplicates('corredor').sort_values(['orden', 'nombre'])
nombres = list(orden_corr['nombre'])
yc = np.arange(len(nombres))[::-1]
tope_tx = dif_tx[['base_MW', 'libre_MW']].max().max() / 1000
fig, ejes = figura(11.5, 9.4, 1, 4, sharey=True, titulo_in=1.05, nota_in=0.62)
for ax, e in zip(ejes, ESCENARIOS):
    d = dif_tx[dif_tx.escenario == e].set_index('nombre').reindex(nombres)
    base, libre = d['base_MW'].values / 1000, d['libre_MW'].values / 1000
    ax.hlines(yc, np.minimum(base, libre), np.maximum(base, libre), color=EJE, linewidth=2)
    ax.scatter(base, yc, s=26, color=COLOR_BASE, edgecolor=SUPERFICIE, linewidth=1, zorder=3)
    ax.scatter(libre, yc, s=26, color=COLOR_LIBRE, edgecolor=SUPERFICIE, linewidth=1, zorder=3)
    total_base, total_libre = d['base_MW'].sum() / 1000, d['libre_MW'].sum() / 1000
    ax.set_title(f"{NOMBRE[e]}\nbase {num(total_base, 1)} GW · libre {num(total_libre, 1)} GW", fontsize=9)
    ax.set_xlim(0, tope_tx * 1.08)
    ax.set_xlabel('GW ampliados 2026-2050')
    grilla(ax, 'x')
    ax.grid(axis='y', color=GRILLA, linewidth=0.4)
ejes[0].set_yticks(yc, nombres, fontsize=7.5)
ejes[0].set_ylim(-0.8, len(nombres) - 0.2)
leyenda_arriba(fig, [(ETIQUETA_BASE, COLOR_BASE), (ETIQUETA_LIBRE, COLOR_LIBRE)], forma='punto')
ahorro_tx = (dif_tx.groupby('escenario')['base_MW'].sum() - dif_tx.groupby('escenario')['libre_MW'].sum()) / 1000
titular(fig, f'Con ubicación óptima se amplían entre {num(ahorro_tx.min(), 1)} y {num(ahorro_tx.max(), 1)} GW menos '
             'de transmisión',
        'MW agregados a cada corredor entre 2026 y 2050, incluidas las obras comprometidas. Corredores de norte (arriba) a sur.')
ampl = tabla('transmision_ampliaciones.csv')
hvdc = ampl[(ampl.corredor == 'Kimal500_AltoJahuel500') & (ampl.escenario == 'SIN_DC') & (ampl.MW_comprometidos > 0)].iloc[0]
anotar(fig, 'Corredor ordenado por la posición media de sus dos zonas (zonas.csv). Kimal 500 – Alto Jahuel 500 es la línea '
            f"de corriente continua Kimal–Lo Aguirre ({num(hvdc['MW_comprometidos'])} MW comprometidos en {hvdc['periodo']}).")
guardar(fig, 'f_transmision_por_corredor')


# =====================================================================================================
# (g) Ubicación de los data centers por zona en 2050 (base frente a libre), de norte a sur
# =====================================================================================================
ubic = tabla('ubicacion_dc.csv')
ubic = ubic[ubic['PERIOD'] == ultimo]
con_dc = ubic.groupby('LOAD_ZONE')['dc_total_mw'].sum()
zonas_dc = list(zonas.loc[con_dc[con_dc > 0.5].index].sort_values('orden').index)
yz = np.arange(len(zonas_dc))[::-1]
tope_dc = ubic['dc_total_mw'].max()
fig, ejes = figura(10.8, 4.6, 1, 4, sharey=True, titulo_in=1.05, nota_in=0.62)
for ax, e in zip(ejes, ESCENARIOS):
    for desplazamiento, m, color in [(0.18, 'base', COLOR_BASE), (-0.18, 'libre', COLOR_LIBRE)]:
        valores = ubic[(ubic.escenario == e) & (ubic.modo == m)].set_index('LOAD_ZONE')['dc_total_mw'].reindex(zonas_dc).fillna(0)
        ax.barh(yz + desplazamiento, valores, height=0.32, color=color)
        for yi, v in zip(yz, valores):
            if v > 0.5:
                ax.text(v + tope_dc * 0.03, yi + desplazamiento, num(v), ha='left', va='center', fontsize=7.5, color=TINTA)
    ax.set_title(NOMBRE[e])
    ax.set_xlim(0, tope_dc * 1.35)
    ax.set_xlabel(f'MW medios en {ultimo}')
    ax.xaxis.set_major_locator(MaxNLocator(3))
    ax.xaxis.set_major_formatter(FORMATO_MILES)
    grilla(ax, 'x')
ejes[0].set_yticks(yz, [f"{zonas.loc[z, 'nombre']} ({num(zonas.loc[z, 'latitud_aprox_sur'], 1)}° S)" for z in zonas_dc])
leyenda_arriba(fig, [(ETIQUETA_BASE, COLOR_BASE), (ETIQUETA_LIBRE, COLOR_LIBRE)])
titular(fig, 'Libre de elegir, el modelo lleva todo el crecimiento de los data centers al sur',
        f'Data centers por zona en {ultimo} (MW medios), de norte (arriba) a sur. Lo instalado en 2026 se queda donde está.')
anotar(fig, 'Latitud aproximada de cada subestación (zonas.csv). En los 4 escenarios, el 100 % de lo reubicable va a '
            'Río Malleco, Pichirropulli, Nueva Puerto Montt y Nueva Ancud.')
guardar(fig, 'g_ubicacion_dc_por_zona')


# =====================================================================================================
# (h) Precio de una carga plana por zona en 2040 (sin data centers): por qué el sur
# =====================================================================================================
ANIO_PRECIO = 2040
precios = tabla('precios_zonales.csv')
p = precios[(precios.escenario == 'SIN_DC') & (precios.periodo == ANIO_PRECIO)].sort_values('orden')
ubic_todo = tabla('ubicacion_dc.csv')
# Zonas elegidas: donde el modo libre agrega data centers después de 2026. Proyectadas: las del modo base.
ubicado = ubic_todo.pivot_table(index=['escenario', 'modo', 'LOAD_ZONE'], columns='PERIOD', values='dc_ubicado_mw', aggfunc='sum').fillna(0)
aumento = (ubicado[ultimo] - ubicado[periodos[0]])
elegidas = set(aumento[(aumento.index.get_level_values('modo') == 'libre') & (aumento > 0.5)].index.get_level_values('LOAD_ZONE'))
proyectadas = set(ubic_todo.loc[(ubic_todo.modo == 'base') & (ubic_todo.dc_total_mw > 0.5), 'LOAD_ZONE'])
color_zona = [COLOR_LIBRE if z in elegidas else CATEGORICA[1] if z in proyectadas else GRIS_DATO for z in p['zona']]
yp = np.arange(len(p))[::-1]
fig, ax = figura(8.8, 8.2, titulo_in=0.85, nota_in=0.62)
ax.barh(yp, p['precio_carga_plana_usd_mwh'], height=0.62, color=color_zona)
for yi, z, v in zip(yp, p['zona'], p['precio_carga_plana_usd_mwh']):
    if z in elegidas or z in proyectadas:
        ax.text(v + 0.4, yi, num(v, 1), ha='left', va='center', fontsize=8, color=TINTA)
ax.set_yticks(yp, [f"{n} ({num(l, 1)}° S)" for n, l in zip(p['nombre'], zonas.loc[p['zona'], 'latitud_aprox_sur'])],
              fontsize=8)
ax.set_ylim(-0.7, len(p) - 0.3)
ax.set_xlabel(f'USD/MWh de una carga plana en {ANIO_PRECIO}, sistema sin data centers')
grilla(ax, 'x')
leyenda(ax, [('Zonas que elige el modelo (libre)', COLOR_LIBRE), ('Zonas de la proyección (base)', CATEGORICA[1]),
             ('Resto', GRIS_DATO)], loc='lower right')
sur = p[p.zona.isin(elegidas)]['precio_carga_plana_usd_mwh']
base_p = p[p.zona.isin(proyectadas)]['precio_carga_plana_usd_mwh']
titular(fig, f'En {ANIO_PRECIO}, abastecer 1 MW plano cuesta {rango(sur.min(), sur.max())} USD/MWh en el sur '
             f'y {rango(base_p.min(), base_p.max())} donde los ubica la proyección',
        'Promedio horario del costo marginal de la zona (dual del balance): incluye la inversión que exige 1 MW más.')
anotar(fig, 'Zonas de norte (arriba) a sur, con latitud aproximada de su subestación. Los polos PDGE se ubican junto a la '
            'subestación a la que se conectan.')
guardar(fig, 'h_precio_carga_plana_2040')


# =====================================================================================================
# (i) Trayectorias de demanda de data centers de los 4 escenarios
# =====================================================================================================
dc = tabla('escenarios_dc.csv')
fin = periodos[-1] + 5
fig, ax = figura(8.0, 4.5, titulo_in=1.05)
for i, e in enumerate(ESCENARIOS):
    s = dc[dc.escenario == e].set_index('periodo')['dc_total_MW']
    x = list(s.index) + [fin]
    v = list(s.values) + [s.values[-1]]
    ax.step(x, v, where='post', color=CATEGORICA[i], linewidth=2, solid_joinstyle='round', solid_capstyle='round',
            label=NOMBRE[e])
    ax.scatter(s.index, s.values, s=22, color=CATEGORICA[i], edgecolor=SUPERFICIE, linewidth=1.2, zorder=3)
    ax.text(fin + 0.4, v[-1], f"{NOMBRE[e]}  {num(v[-1])} MW", ha='left', va='center', fontsize=8.5, color=TINTA)
ax.set_xlim(periodos[0] - 0.5, fin + 7.5)
ax.set_xticks(periodos + [fin])
ax.set_ylim(0, dc['dc_total_MW'].max() * 1.12)
ax.yaxis.set_major_formatter(FORMATO_MILES)
ax.set_ylabel('MW medios de data centers')
ax.spines['bottom'].set_bounds(periodos[0] - 0.5, fin)
grilla(ax, 'y')
leyenda_arriba(fig, [(NOMBRE[e], CATEGORICA[i]) for i, e in enumerate(ESCENARIOS)], forma='linea')
pelp_e2, propio = dc[dc.periodo == periodos[-1]].set_index('escenario')['dc_total_MW'].loc[['PELP_E2', 'PROPIO']]
titular(fig, f'Los escenarios van de {num(pelp_e2)} a {num(propio)} MW medios de data centers en {periodos[-1]}',
        'Demanda plana de data centers en cada período del modelo (fija + ubicable).')
fijo_propio = ubic_todo[(ubic_todo.escenario == 'PROPIO') & (ubic_todo.modo == 'base') & (ubic_todo.PERIOD == periodos[-1])]
anotar(fig, 'Cada valor rige todo su período (2026-2029, 2030-2034, …, 2050-2054). PROPIO incluye '
            f"{num(fijo_propio['dc_fijo_mw'].sum())} MW de data centers con ubicación fija (dc_fijo.csv).")
guardar(fig, 'i_demanda_dc')


# =====================================================================================================
# (j) Tiempos de cómputo de cada corrida, por etapa
# =====================================================================================================
t = tabla('tiempos_computo.csv')
t['caso'] = pd.Categorical(t['escenario'] + '|' + t['modo'], [f'{e}|{m}' for e, m in casos], ordered=True)
t = t.sort_values('caso')
ETAPAS = {
    'Lectura y construcción del modelo (Switch)': (t['lectura_datos_s'] + t['construccion_modelo_s']) / 60,
    'Gurobi: presolve y barrera': (t['gurobi_total_s'] - t['crossover_s']) / 60,
    'Gurobi: crossover': t['crossover_s'] / 60,
    'Traspaso del modelo a Gurobi y de vuelta': (t['solver_switch_s'] - t['gurobi_total_s']) / 60,
    'Posproceso y escritura de salidas': t['posproceso_s'] / 60,
}
ETAPAS['Otros (arranque)'] = (t['reloj_total_min'] - sum(ETAPAS.values())).clip(lower=0)
yt = np.arange(len(t))[::-1]
fig, ax = figura(8.6, 5.0, titulo_in=1.35)
izquierda = np.zeros(len(t))
for i, (etapa, minutos) in enumerate(ETAPAS.items()):
    ax.barh(yt, minutos.values, left=izquierda, height=0.55, color=CATEGORICA[i], edgecolor=SUPERFICIE, linewidth=1)
    izquierda += minutos.values
for yi, (_, fila), total in zip(yt, t.iterrows(), izquierda):
    ax.text(total + 0.2, yi, f"{num(fila['reloj_total_min'], 1)} min · {int(fila['hilos'])} hilos", ha='left',
            va='center', fontsize=8, color=TINTA)
ax.set_yticks(yt, [NOMBRE[e] if e == 'SIN_DC' else f'{NOMBRE[e]} · {m}' for e, m in zip(t['escenario'], t['modo'])])
ax.set_xlim(0, t['reloj_total_min'].max() * 1.3)
ax.xaxis.set_major_locator(MaxNLocator(5, integer=True))
ax.set_xlabel('Minutos de reloj por corrida')
grilla(ax, 'x')
leyenda_arriba(fig, [(etapa, CATEGORICA[i]) for i, etapa in enumerate(ETAPAS)], ncols=3)
barrera = (ETAPAS['Gurobi: presolve y barrera'] / t['reloj_total_min'].values)
titular(fig, f"Cada corrida tarda {rango(t['reloj_total_min'].min(), t['reloj_total_min'].max())} min; "
             f"entre {num(100 * barrera.min())} % y {num(100 * barrera.max())} % es el presolve y la barrera de Gurobi",
        f"Tiempo de reloj por etapa, de los logs de Switch y Gurobi {tabla('entorno_computo.csv')['gurobi_version'].iloc[0]} "
        '(método de barrera).')
anotar(fig, f"Problema de {num(t['filas'].iloc[0] / 1e6, 2)} M filas × {num(t['columnas'].iloc[0] / 1e6, 2)} M columnas "
            f"({num(t['no_ceros'].iloc[0] / 1e6, 1)} M no ceros). Corridas simultáneas en lotes, con 4 a 8 hilos cada una: "
            'el tiempo de reloj no es comparable entre lotes.')
guardar(fig, 'j_tiempos_computo')
