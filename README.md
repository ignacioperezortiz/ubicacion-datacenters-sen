# Ubicación de data centers en el Sistema Eléctrico Nacional

¿Cuánto se ahorra en la planificación del sistema eléctrico chileno si los data centers se ubican donde le conviene al sistema, en vez de donde dicen las proyecciones?

Proyecto del curso **Economía, Resiliencia y Mercados Energéticos** (Universidad Adolfo Ibáñez, 2026-S2).

El estudio usa el modelo de planificación de generación y transmisión [Switch 2.0.9](https://github.com/switch-model/switch) sobre la red de la **PELP 2023–2027** (Ministerio de Energía, escenario Carbono Neutralidad). Le agrega cuatro proyecciones de demanda de data centers y compara tres situaciones:

| Caso | Qué representa |
|---|---|
| Sin data centers | Carbono Neutralidad sin data centers proyectados. Los que ya operan, ~99 MW medios, están dentro de la demanda de la PELP. |
| **Base** | Los data centers proyectados, en las zonas que indican las proyecciones. |
| **Libre** | Los mismos MW y en los mismos años, pero el modelo elige la zona desde 2030. Lo que se conecta en los períodos 2025 y 2027 son proyectos ya comprometidos y queda en su zona. |

**Horizonte.** El modelo parte en 2025, con siete períodos: 2025 (2025–2026), 2027 (2027–2029), 2030, 2035, 2040, 2045 y 2050 (2050–2054). Ninguna inversión que decidió AMEBA, el modelo de la PELP 2023–2027, entra como dato: el modelo decide toda la expansión desde 2025.

## Resultados principales

Valor presente a 2025, en millones de USD, con tasa de 6 %. El sistema sin data centers proyectados cuesta **42.618,8 MMUSD**.

| Escenario de data centers | Costo extra, ubicación proyectada | Costo extra, ubicación óptima | Ahorro | Ahorro / costo extra | Costo extra por MWh de data centers |
|---|---:|---:|---:|---:|---:|
| PELP 2028–2032, E2 | 1.039,9 | 860,8 | 179,1 | 17,2 % | 41,9 → 34,7 USD/MWh |
| Coordinador (CEN 2026) | 4.263,4 | 3.491,5 | 772,0 | 18,1 % | 43,6 → 35,7 USD/MWh |
| PELP 2028–2032, N1 | 3.502,8 | 2.883,2 | 619,7 | 17,7 % | 40,4 → 33,3 USD/MWh |
| Proyección propia (solicitudes CEN) | 16.184,1 | 11.635,1 | 4.549,0 | 28,1 % | 45,2 → 32,5 USD/MWh |

Ubicar bien los data centers evita entre el 17 % y el 28 % del costo que le agregan al sistema, de 11,9 a 14,9 USD por MWh reubicado. Zonas que elige el modelo: Nueva Ancud en los cuatro escenarios; en la proyección propia, también Río Malleco, Pichirropulli y Nueva Puerto Montt y, en 2050, el norte grande (Nueva Pozo Almonte, Nueva Zaldívar, Parinacota y Lagunas), que recibe un tercio de lo reubicable. Las proyecciones los ponen sobre todo en Santiago y Valparaíso. El análisis completo, con la matriz eficiente, la transmisión, las inversiones, los precios y las emisiones, está en **[docs/ANALISIS.md](docs/ANALISIS.md)**.

## Contenido

```
casos/<CASO>/inputs/          entradas de Switch (una carpeta por caso)
casos/<CASO>/outputs_base/    salidas del caso base
casos/<CASO>/outputs_libre/   salidas del caso libre
casos/<CASO>/log_*.txt        registro de cada corrida (tiempos, tamaño del problema)
modulos/                      módulos propios de Switch
scripts/                      corrida, resultados, análisis y gráficos
resultados/tablas/            tablas de resultados (CSV)
resultados/figuras/           gráficos (PNG y SVG)
docs/                         formulación, datos y supuestos, análisis, validación
```

Los casos son `SIN_DC`, `PELP_E2`, `CEN`, `PELP_N1` y `PROPIO`. La demanda de data centers de cada escenario está en `casos/<CASO>/inputs/dc_*.csv`.

**Módulos propios** (`modulos/`):
- `data_centers.py`: demanda de data centers con ubicación fija o elegida por el modelo. El total por período es un dato y un data center no se traslada.
- `reserva_simple.py`: reserva sistémica de subida y bajada, sin compromiso de unidades.
- `limites_transmision.py`: obras de transmisión comprometidas y topes de ampliación de los candidatos de la PELP.
- `topes_tecnologia.py`: tope a los MW nuevos de una tecnología en un período, sumando todas las zonas. No se carga en estos casos: los topes anuales de AMEBA, sumados en los años de cada período, no restringen.
- `precios.py`: exporta los precios marginales por zona y hora a partir de los duales del balance.

**Documentación** (`docs/`):
- [FORMULACION.md](docs/FORMULACION.md): el modelo matemático en la notación del curso.
- [DATOS_Y_SUPUESTOS.md](docs/DATOS_Y_SUPUESTOS.md): de dónde sale cada entrada y por qué.
- [ANALISIS.md](docs/ANALISIS.md): resultados con tablas y gráficos.
- [VALIDACION.md](docs/VALIDACION.md): cómo se validó cada fase.
- [CAMBIOS_2025.md](docs/CAMBIOS_2025.md): qué cambió respecto de la primera versión publicada, que partía en 2026, y por qué.

El repositorio no incluye los datos originales de la PELP ni los scripts que los tradujeron a Switch. Las entradas ya traducidas están en `casos/`, y `docs/DATOS_Y_SUPUESTOS.md` explica cómo se construyeron.

## Cómo replicar el estudio

### 1. Requisitos

- **Python 3.11.**
- **Un solver lineal:**
  - **Gurobi 13** (recomendado). La licencia académica es gratuita en [gurobi.com](https://www.gurobi.com/academia/academic-program-and-licenses/). El estudio se resolvió con él.
  - **HiGHS** (libre, se instala con `highspy`). Es una alternativa, pero bastante más lenta en estos casos; no se midió su tiempo con los casos finales.
- **Memoria:** con Gurobi, el ordenamiento de la barrera llega a unos 20–60 GB de RAM por corrida. Con 64 GB, conviene resolver un caso a la vez.

```bash
python -m venv .venv
```

En Windows:

```bash
.venv\Scripts\activate
```

En Linux o macOS:

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

Con Gurobi, la licencia (`gurobi.lic`) debe estar en la carpeta de usuario, o su ruta en la variable `GRB_LICENSE_FILE`.

### 2. Resolver los casos

Desde la raíz del repositorio. Todos los casos, uno a la vez con 14 hilos (por omisión, el script corre 3 a la vez con 6 hilos, lo que con 7 períodos puede agotar la memoria):

```bash
python scripts/correr_casos.py --paralelo 1 --hilos 14
```

Un solo caso:

```bash
python scripts/correr_casos.py PELP_E2 --modos base libre --paralelo 1 --hilos 14
```

Con HiGHS en vez de Gurobi:

```bash
python scripts/correr_casos.py SIN_DC --modos base --solver appsi_highs
```

El caso `SIN_DC` se resuelve solo en modo base, así que «todos los casos» son 9 corridas. Cada corrida reescribe `casos/<CASO>/outputs_<modo>/` y su log.

**Reproducibilidad exacta.** Con Gurobi y el mismo número de hilos que la corrida original (`hilos` en `resultados/tablas/tiempos_computo.csv`), la solución se reproduce bit a bit. Con otro número de hilos, el costo total es el mismo (diferencia relativa ~1e-16) y la ubicación de los data centers también. Pueden cambiar soluciones alternativas de igual costo: unos MW de almacenamiento entre zonas vecinas con parámetros idénticos, o el reparto del vertimiento. Los archivos horarios pesados (`dispatch.csv` y otros) no están en el repositorio y se regeneran al correr. La opción `--dc-libre-desde 2030` (por omisión) fija en el modo libre la ubicación de los data centers de los períodos anteriores a 2030 (2025 y 2027).

### 3. Regenerar tablas y gráficos

```bash
python scripts/resultados.py
```

```bash
python scripts/tiempos_computo.py
```

```bash
python scripts/analisis.py
```

```bash
python scripts/graficos.py
```

`resultados.py` calcula costos, el costo extra respecto del caso sin data centers, el ahorro, la ubicación, la capacidad, la transmisión y los precios. `analisis.py` agrega la matriz eficiente, las inversiones y la expansión por zona. Los resultados de este repositorio se regeneran sin volver a resolver, porque las salidas ya están incluidas.

## Tiempos de cómputo

Cada caso es un programa lineal de **1,54 millones de restricciones, 1,35 millones de variables y 8,07 millones de coeficientes**. Tras el presolve de Gurobi quedan 0,89 × 1,00 millones. Se resolvió con Gurobi 13.0.3 por barrera, con 8 a 14 hilos, en un computador de 16 núcleos físicos (22 lógicos) y 63 GB de RAM:

| Etapa | Tiempo por corrida |
|---|---|
| Lectura de datos y construcción del modelo (Pyomo) | 20–33 s |
| Barrera de Gurobi | 7–13 min |
| Crossover | 15–55 s |
| Escritura de resultados | 42–77 s |
| **Total por corrida** | **10–18 min** |

- **Estudio completo:** son 9 corridas (sin data centers, más 4 escenarios × base y libre). En serie suman 115 min de reloj. `SIN_DC` y PROPIO base corrieron a la vez, con 8 hilos cada una; las otras 7, de a una y con 14 hilos.
- **Memoria:** con 7 períodos, el ordenamiento de la barrera llega a unos 20–60 GB por corrida. Por eso se recomienda una corrida a la vez (`--paralelo 1`).
- **Detalle por corrida:** en `resultados/tablas/tiempos_computo.csv`.
- **Por qué 6 días típicos:** con 12 días típicos por año, como la PELP 2023–2027, el problema duplica su tamaño y la barrera de Gurobi se queda sin memoria con 63 GB. Por eso se usan 6 días típicos, uno por mes impar, que cuenta también por el mes siguiente, igual que la PELP 2028–2032.

## Supuestos y limitaciones principales

- **Planificación** con previsión perfecta, sin compromiso de unidades ni inercia, con reserva sistémica, de 2025 a 2054 y con valor presente a 2025.
- **Punto de partida:** la capacidad existente es la de los datos de entrada de AMEBA en servicio el 1 de enero de 2025. Lo que AMEBA decidió construir (3.000 MW solares fotovoltaicos y 1.000 MW eólicos en 2025, 92,1 MW de baterías en 2024 y 2.672 MW de transmisión en 2025) vuelve a ser candidato. Las baterías «ley» (2.000 MW) son candidatas a costo 0 desde 2027, y las obras de transmisión comprometidas (enlace de corriente continua Kimal–Lo Aguirre, 2.000 MW, y Río Malleco–Pichirropulli, 660 MW) entran en 2030.
- **Red:** modelo de transporte sin pérdidas. La red de 31 zonas tiene solo 3–4 lazos.
- **Demanda de data centers:** plana, igual al 50 % de la capacidad instalada o solicitada, el mismo factor de la PELP. Las proyecciones del CEN y la propia, que terminan en 2030 y 2032, crecen después 5 % y 8 % anual.
- **Salidas de AMEBA que se usan como dato:** la energía hidro por día típico, el perfil de consumo de hidrógeno y amoníaco y el factor 1,031 de la demanda. Son pendientes documentados.
- **Sin costos de conexión ni de terreno** de los data centers: el ahorro es solo del sistema eléctrico.
- **Escenario propio:** viene de un catastro de solicitudes de conexión al Coordinador Eléctrico Nacional (Acceso Abierto) cruzado con el SEIA, elaborado por Raúl Ugarte (CENTRA UAI), conciliado sin duplicados con la demanda de la PELP y con un catálogo propio de proyectos.

El detalle está en [docs/DATOS_Y_SUPUESTOS.md](docs/DATOS_Y_SUPUESTOS.md).

## Fuentes

- **Ministerio de Energía:** Planificación Energética de Largo Plazo 2023–2027 (Informe Definitivo) y 2028–2032 (Informe Preliminar).
- **Coordinador Eléctrico Nacional:** Proyección de Demanda de Largo Plazo 2026–2046 y Plataforma de Acceso Abierto.
- **Servicio de Evaluación Ambiental:** SEIA.
- **Modelo:** Switch, de Fripp, Johnston, Mileva, Maluenda y otros (licencia Apache 2.0).

## Presentación de avance

La presentación de avance del curso (PPTX y PDF) y el código que la genera desde `resultados/` y `casos/` están en [presentacion/](presentacion/). Cómo regenerarla y editarla: [presentacion/README.md](presentacion/README.md).
