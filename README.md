# Ubicación de data centers en el Sistema Eléctrico Nacional

¿Cuánto se ahorra en la planificación del sistema eléctrico chileno si los data centers se ubican donde le conviene al sistema, en vez de donde dicen las proyecciones?

Proyecto del curso **Economía, Resiliencia y Mercados Energéticos** (Universidad Adolfo Ibáñez, 2026-S2).

El estudio usa el modelo de planificación de generación y transmisión [Switch 2.0.9](https://github.com/switch-model/switch) sobre la red de la **PELP 2023–2027** (Ministerio de Energía, escenario Carbono Neutralidad). Le agrega cuatro proyecciones de demanda de data centers y compara tres situaciones:

| Caso | Qué representa |
|---|---|
| Sin data centers | Carbono Neutralidad sin data centers proyectados. Los que ya operan, ~99 MW medios, están dentro de la demanda de la PELP. |
| **Base** | Los data centers proyectados, en las zonas que indican las proyecciones. |
| **Libre** | Los mismos MW y en los mismos años, pero el modelo elige la zona desde 2030. Lo que se conecta antes de 2030 son proyectos ya comprometidos y queda en su zona. |

## Resultados principales

Valor presente a 2026, en millones de USD, con tasa de 6 %. El sistema sin data centers proyectados cuesta **40.538 MMUSD**.

| Escenario de data centers | Costo extra, ubicación proyectada | Costo extra, ubicación óptima | Ahorro | Ahorro / costo extra | Costo extra por MWh de data centers |
|---|---:|---:|---:|---:|---:|
| PELP 2028–2032, E2 | 1.100 | 889 | 211 | 19 % | 42 → 34 USD/MWh |
| Coordinador (CEN 2026) | 2.816 | 2.541 | 275 | 10 % | 45 → 41 USD/MWh |
| PELP 2028–2032, N1 | 3.660 | 2.952 | 708 | 19 % | 40 → 32 USD/MWh |
| Proyección propia (solicitudes CEN) | 8.034 | 6.252 | 1.783 | 22 % | 43 → 34 USD/MWh |

Ubicar bien los data centers evita entre el 10 % y el 22 % del costo que le agregan al sistema. El modelo los lleva al sur (principalmente Nueva Ancud y, con más carga, Puerto Montt, Pichirropulli y Río Malleco), donde la energía es más barata para una carga plana; las proyecciones los ponen en Santiago y Valparaíso. El análisis completo, con la matriz eficiente, la transmisión, las inversiones, los precios y las emisiones, está en **[docs/ANALISIS.md](docs/ANALISIS.md)**.

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
- `precios.py`: exporta los precios marginales por zona y hora a partir de los duales del balance.

**Documentación** (`docs/`):
- [FORMULACION.md](docs/FORMULACION.md): el modelo matemático en la notación del curso.
- [DATOS_Y_SUPUESTOS.md](docs/DATOS_Y_SUPUESTOS.md): de dónde sale cada entrada y por qué.
- [ANALISIS.md](docs/ANALISIS.md): resultados con tablas y gráficos.
- [VALIDACION.md](docs/VALIDACION.md): cómo se validó cada fase.

El repositorio no incluye los datos originales de la PELP ni los scripts que los tradujeron a Switch. Las entradas ya traducidas están en `casos/`, y `docs/DATOS_Y_SUPUESTOS.md` explica cómo se construyeron.

## Cómo replicar el estudio

### 1. Requisitos

- **Python 3.11.**
- **Un solver lineal:**
  - **Gurobi 13** (recomendado). La licencia académica es gratuita en [gurobi.com](https://www.gurobi.com/academia/academic-program-and-licenses/). El estudio se resolvió con él.
  - **HiGHS** (libre, se instala con `highspy`). Es una alternativa, pero bastante más lenta en estos casos; no se midió su tiempo con los casos finales.
- **Memoria:** unos 8–10 GB de RAM por corrida.

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

Desde la raíz del repositorio. Todos los casos, 3 a la vez con 6 hilos cada uno:

```bash
python scripts/correr_casos.py --paralelo 3 --hilos 6
```

Un solo caso:

```bash
python scripts/correr_casos.py PELP_E2 --modos base libre
```

Con HiGHS en vez de Gurobi:

```bash
python scripts/correr_casos.py SIN_DC --modos base --solver appsi_highs
```

El caso `SIN_DC` se resuelve solo en modo base, así que «todos los casos» son 9 corridas. Cada corrida reescribe `casos/<CASO>/outputs_<modo>/` y su log.

**Reproducibilidad exacta.** Con Gurobi y el mismo número de hilos que la corrida original (`hilos` en `resultados/tablas/tiempos_computo.csv`), la solución se reproduce bit a bit. Con otro número de hilos, el costo total es el mismo (diferencia relativa ~1e-16) y la ubicación de los data centers también. Pueden cambiar soluciones alternativas de igual costo: unos MW de almacenamiento entre zonas vecinas con parámetros idénticos, o el reparto del vertimiento. Los archivos horarios pesados (`dispatch.csv` y otros) no están en el repositorio y se regeneran al correr. La opción `--dc-libre-desde 2030` (por omisión) fija la ubicación de los data centers antes de 2030 en el modo libre.

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

Cada caso es un programa lineal de **1,35 millones de restricciones, 1,18 millones de variables y 6,9 millones de coeficientes**. Tras el presolve de Gurobi quedan 0,78 × 0,88 millones. Se resolvió con Gurobi 13.0.3 por barrera, en un computador de 16 núcleos físicos (22 lógicos) y 63 GB de RAM:

| Etapa | Tiempo por corrida |
|---|---|
| Lectura de datos y construcción del modelo (Pyomo) | ~20 s |
| Barrera de Gurobi | 5–11 min |
| Crossover | 17–58 s |
| Escritura de resultados | ~45–65 s |
| **Total por corrida** | **8 min** sola con 8 hilos; **13–16 min** con 3–4 corridas simultáneas |

- **Estudio completo:** son 9 corridas (sin data centers, más 4 escenarios × base y libre). En serie suman ~114 min de reloj. En tandas de 3–4 corridas simultáneas toman ~45 min.
- **Detalle por corrida:** en `resultados/tablas/tiempos_computo.csv`.
- **Por qué 6 días típicos:** con 12 días típicos por año, como la PELP 2023–2027, el problema duplica su tamaño y la barrera de Gurobi se queda sin memoria con 63 GB. Por eso se usan 6 días típicos, uno por mes impar, que cuenta también por el mes siguiente, igual que la PELP 2028–2032.

## Supuestos y limitaciones principales

- **Planificación** con previsión perfecta, sin compromiso de unidades ni inercia, con reserva sistémica.
- **Red:** modelo de transporte sin pérdidas. La red de 31 zonas tiene solo 3–4 lazos.
- **Demanda de data centers:** plana, igual al 50 % de la capacidad instalada o solicitada, el mismo factor de la PELP.
- **Sin costos de conexión ni de terreno** de los data centers: el ahorro es solo del sistema eléctrico.
- **Escenario propio:** viene de un catastro de solicitudes de conexión al Coordinador Eléctrico Nacional (Acceso Abierto) cruzado con el SEIA, elaborado por Raúl Ugarte (CENTRA UAI), conciliado sin duplicados con la demanda de la PELP y con un catálogo propio de proyectos.

El detalle está en [docs/DATOS_Y_SUPUESTOS.md](docs/DATOS_Y_SUPUESTOS.md).

## Fuentes

- **Ministerio de Energía:** Planificación Energética de Largo Plazo 2023–2027 (Informe Definitivo) y 2028–2032 (Informe Preliminar).
- **Coordinador Eléctrico Nacional:** Proyección de Demanda de Largo Plazo 2026–2046 y Plataforma de Acceso Abierto.
- **Servicio de Evaluación Ambiental:** SEIA.
- **Modelo:** Switch, de Fripp, Johnston, Mileva, Maluenda y otros (licencia Apache 2.0).
