# Cambios de la versión con inicio en 2025

La primera versión publicada del estudio partía en 2026, con seis períodos (2026, 2030, …, 2050) y valor presente a 2026, y tomaba como capacidad existente lo que AMEBA, el modelo de la PELP 2023–2027, decidió construir en 2024–2026. Esta versión parte en 2025, con siete períodos y valor presente a 2025, y Switch decide toda la expansión desde 2025.

**Por qué.** Se decidió no usar como dato ninguna inversión decidida por AMEBA: esas inversiones son una salida de su optimización, y tomarlas como capacidad existente fijaba una parte de la expansión que el modelo debe decidir.

## Decisiones

1. **Períodos.** 2025 (2025–2026), 2027 (2027–2029), 2030, 2035, 2040, 2045 y 2050 (2050–2054). Valor presente a 2025, tasa de 6 %. Cada período usa los datos de AMEBA de su año de inicio.
2. **Ninguna inversión de AMEBA como dato.** Vuelven a ser candidatos los 3.000 MW solares FV y 1.000 MW eólicos de 2025, los 92,1 MW de baterías de 8 h en Nueva Pozo Almonte 220 de 2024 (su tope vuelve a 600 MW) y los 2.672 MW de transmisión de 2025 en 7 corredores.
3. **Capacidad existente.** Las unidades de los datos de entrada de AMEBA en servicio el 1 de enero de 2025. Una unidad opera en un período si está en servicio el 1 de enero de su año de inicio. Lo comprometido con fecha entra en el primer período que cumple esa regla: el HVDC Kimal–Lo Aguirre (enero de 2029) entra en 2030.
4. **Baterías «ley»** (Kimal, Nueva Cardones y Cumbres; 2.000 MW). Son candidatas con inversión y O&M fijo nulos desde el período 2027, el primero que parte en 2026 o después. No son predeterminadas.
5. **Topes anuales de FV y eólica de AMEBA.** Valen 0 hasta 2024, 3.000 y 1.000 MW en 2025 y 50.000 MW desde 2026. La decisión 13 fija cómo se aplican.
6. **Salidas de AMEBA que se mantienen como dato:** la energía hidro por día típico, el perfil del consumo de H₂ y NH₃ y el factor 1,031 de la demanda. Quedan documentadas como limitaciones.
7. **Impuesto al CO₂.** Promedio de los años de cada período con la misma regla anual: 0; 3,33; 10; 23,48; 35; 35 y 35 USD/t de 2025 a 2050.
8. **Data centers.** Los escenarios se promedian en los períodos nuevos. La ubicación libre sigue desde 2030, así que lo de los períodos 2025 y 2027 queda comprometido en las zonas proyectadas (antes, solo lo de 2026).
9. **Autocomprobaciones.** Cada parte de la traducción a Switch documentó el cambio y volvió a correr sus comprobaciones ([VALIDACION.md, sección 8](VALIDACION.md#8-inicio-en-2025-autocomprobaciones-de-la-traducción)).
10. **Río Malleco–Pichirropulli** (660 MW, febrero de 2030) entra en el período 2030. Es la única obra a la que no se aplica la regla del 1 de enero.
11. **Crecimiento de los data centers después del horizonte de cada proyección.** CEN: la capacidad crece 3 % anual desde 2031. PROPIO: la demanda total de data centers crece 3 % anual desde 2033; el aumento es carga nueva, reubicable, y en el caso base se reparte entre las zonas proyectadas en proporción a lo solicitado. PELP E2 y N1 no cambian: ya traen crecimiento propio después de 2030. La versión del commit `52e1882` usaba 5 % en CEN y 8 % en PROPIO; se bajaron a 3 % en ambos, y las cifras de este documento son las de 3 %.
12. **Verificación independiente de las entradas** con el inicio en 2025, sin errores.
13. **Topes de FV y eólica por período.** El tope de un período es la suma de los topes anuales de sus años: en 2025–2026 da 53.000 MW FV y 51.000 MW eólicos, que no restringen. Por eso el módulo `topes_tecnologia` no se carga en las corridas; queda disponible con su CSV. Con un tope de 3.000 y 1.000 MW en el período, esa fila acopla todos los proyectos FV y eólicos y la factorización de la barrera supera los 88 GB de memoria; con el ordenamiento AMD cabe, pero tarda unos 60 minutos por corrida.

## Resultados principales, antes y después

Costos en MMUSD. El año base del valor presente pasó de 2026 a 2025 y el horizonte suma el bienio 2025–2026, así que los costos totales no se comparan uno a uno; los cocientes sí.

Costo del sistema sin data centers: **40.538 → 42.619 MMUSD**.

| Escenario | Versión | DC en 2050 (MW) | Reubicable en 2050 | Extra base | Extra libre | Ahorro | Ahorro / extra | Extra por MWh, base → libre (USD/MWh) | Ahorro por MWh reubicado (USD/MWh) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| PELP E2 | Inicio 2026 | 331 | 78 % | 1.100 | 889 | 211 | 19,2 % | 41,7 → 33,7 | 12,0 |
| | Inicio 2025 | 331 | 70 % | 1.040 | 861 | 179 | 17,2 % | 41,9 → 34,7 | 12,4 |
| CEN | Inicio 2026 | 591 | 44 % | 2.816 | 2.541 | 275 | 9,8 % | 45,1 → 40,7 | 11,9 |
| | Inicio 2025 | 1.224 | 69 % | 3.496 | 2.997 | 500 | 14,3 % | 44,1 → 37,8 | 13,4 |
| PELP N1 | Inicio 2026 | 1.081 | 76 % | 3.660 | 2.952 | 708 | 19,3 % | 39,8 → 32,1 | 11,6 |
| | Inicio 2025 | 1.081 | 70 % | 3.503 | 2.883 | 620 | 17,7 % | 40,4 → 33,3 | 11,9 |
| PROPIO | Inicio 2026 | 2.021 | 80 % | 8.034 | 6.252 | 1.783 | 22,2 % | 43,1 → 33,5 | 12,8 |
| | Inicio 2025 | 3.733 | 86 % | 9.724 | 7.322 | 2.402 | 24,7 % | 43,5 → 32,8 | 14,0 |

Zonas que elige el modelo para lo reubicable, en 2050:

| Escenario | Inicio 2026 | Inicio 2025 (MW medios) |
| --- | --- | --- |
| PELP E2 | Nueva Ancud | Nueva Ancud (232) |
| CEN | Nueva Ancud | Nueva Ancud (843) |
| PELP N1 | Nueva Ancud | Nueva Ancud (757) |
| PROPIO | Nueva Ancud, Nueva Puerto Montt, Pichirropulli y Río Malleco | Nueva Ancud (2.397), Pichirropulli (359), Nueva Puerto Montt (294) y Río Malleco (176) |

Tablas: `costos.csv`, `escenarios_dc_resumen.csv` y `ubicacion_dc.csv`.

- **CEN y PROPIO crecen después de su horizonte** (decisión 11). Su demanda de 2050 pasa de 591 a 1.224 MW y de 2.021 a 3.733 MW, con el 69 % y el 86 % reubicable. Por eso su costo extra y su ahorro aumentan, y la parte reubicable de CEN sube de 44 % a 69 %, aunque sigue siendo la menor.
- **PELP E2 y PELP N1 tienen la misma demanda,** pero ahora queda comprometido lo de 2025 y 2027, no solo lo de 2026. Su parte reubicable baja a 70 % y su ahorro, a 179 y 620 MMUSD. El ahorro por MWh reubicado casi no cambia.
- **En PROPIO, la ubicación óptima sigue siendo el sur,** en las mismas cuatro zonas: los 3.226 MW reubicables de 2050 van a Nueva Ancud, Pichirropulli, Nueva Puerto Montt y Río Malleco.
- **Cada corrida tarda 10,0–17,6 minutos** (antes, 8,1–15,6), con 1,54 millones de restricciones y 1,35 millones de variables.

El análisis completo con el inicio en 2025 está en [ANALISIS.md](ANALISIS.md) y las entradas en [DATOS_Y_SUPUESTOS.md](DATOS_Y_SUPUESTOS.md).
