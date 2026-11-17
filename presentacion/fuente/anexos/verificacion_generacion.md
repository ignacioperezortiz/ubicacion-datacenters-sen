# Verificación: anexo de generación candidata (`10_generacion.js`)

Todas las cifras las calcula y escribe un script de Python (`anexo_generacion.py`, en el scratchpad de la sesión del 17-nov-2026, corrido con `python -P`), sobre las entradas del caso `SIN_DC` del repositorio `ubicacion-datacenters-sen` (`casos/SIN_DC/inputs/`) y el orden de zonas de `resultados/tablas/zonas.csv`. El `.js` no se editó a mano.

## Definición de candidato

- Candidato = fila de `gen_build_costs.csv` con año de construcción en un período del modelo (`periods.csv`: 2026, 2030, 2035, 2040, 2045, 2050) que **no** está en `gen_build_predetermined.csv`. Resultado: 388 proyectos, 2.118 filas proyecto × período.
- Quedan fuera, por ser predeterminados en períodos del modelo: 12 co-combustiones con NH₃ de Guacolda, 2 reconversiones a biomasa y 1 a gas (2026), y 4 BESS «ley» existentes (2026). Coincide con DATOS_Y_SUPUESTOS.md §4 y §5.2.
- Ningún candidato tiene costo de conexión (`gen_connect_cost_per_mw` = 0) ni costo por energía (`gen_storage_energy_overnight_cost` = 0): todo el costo va por MW, como dice el documento.

## Lámina 1, «Anexo: tecnologías candidatas»

| Columna | Cálculo |
|---|---|
| Zonas | número de `gen_load_zone` distintas entre los proyectos candidatos del grupo |
| Potencial máx. (MW) | por zona y tecnología, suma de `gen_capacity_limit_mw` de los proyectos (clases de recurso y de costo); por zona y grupo, el **mayor** tope entre las duraciones (CSP, baterías, Carnot), sin sumarlas; total = suma sobre zonas. Gas y diésel: se comprueba que todos tienen 10.000 MW por proyecto → «sin límite práctico» (§4.1 del documento) |
| Desde | mínimo `build_year` de las filas candidatas del grupo; CSP 13 h desde 2030, 6 y 9 h desde 2035 |
| Costo 2030 / 2050 | `gen_overnight_cost` / 1.000 (USD/MW → USD/kW) de las filas con `build_year` 2030 o 2050; mín.–máx. si varía; «—» si no hay candidato ese año (hidro de pasada: desde 2035, 3.250 USD/kW) |

Comprobaciones del script:

- En CSP y Carnot el tope por zona es idéntico entre duraciones (assert). En baterías, 1, 2 y 4 h tienen 5.000 o 2.000 MW por zona; 6 y 8 h, entre 100 y 700 MW.
- Solo FV, eólica y CSP 13 h tienen costos distintos entre proyectos en un mismo período; el resto es uniforme.
- Cifras que coinciden con DATOS_Y_SUPUESTOS.md: hidro de pasada 6.313 MW en 8 proyectos desde 2035; BESS 4 h 965 USD/kW en 2030 y 667 en 2050; ciclo combinado 1.053 USD/kW; bombeo desde 2030; biomasa desde 2026; gas, diésel y geotermia desde 2030.

## Láminas 2 y 3, «Anexo: candidatos por zona»

- Celda = potencial del grupo en la zona, con la misma regla de la lámina 1; «✓» para gas natural (ciclo combinado y abierto, mismas 10 zonas, assert) y diésel; «✓ + CCS» donde además hay ciclo combinado con captura (3 zonas); «—» sin candidato.
- Orden norte → sur de `zonas.csv`. Para que cada tabla quepa (≤ 15 filas a 11 pt), los 5 polos PDGE van agrupados en una fila (suma de sus topes) al final de la lámina norte; el detalle por polo está en las notas.
- Control cruzado: la suma de cada columna de la matriz reproduce el total de la lámina 1 (FV 661.787; eólica 53.877; CSP 51.875; baterías 85.000; bombeo 42.278; CAES 52.000 MW).

## Formato

- Altos: tabla 1, 15 filas × 0,31 = 4,65 in; matriz norte 15 × 0,29 = 4,35 in; matriz sur 14 × 0,29 = 4,06 in (≤ 4,8). Anchos suman 12,13 in. Títulos ≤ 45 y subtítulos ≤ 110 caracteres, y celdas en una línea, comprobados por el script.
- Carga: `node -e "console.log(require('./10_generacion.js').length)"` → 3.
