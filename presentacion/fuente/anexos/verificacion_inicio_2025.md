# Verificación de los anexos: cambio a inicio 2025 (17-nov-2026)

> **Versión anterior.** Esta verificación corresponde al crecimiento de 5 % (CEN) y 8 % (PROPIO) del commit `52e1882`. Las cifras vigentes de los anexos, con 3 % anual, están en `verificacion_transmision_dc.md`, que regenera `anexos_tx_dc.py`.

Los anexos se actualizaron al cambio de modelo descrito en `modelo_switch\CAMBIO_INICIO_2025.md` (decisiones 1–13). Los inputs vienen de `modelo_switch (proyecto privado del equipo)\casos_2025\<CASO>\inputs\`. Las comprobaciones de abajo pasan en los dos scripts. La copia del repositorio (`ubicacion-datacenters-sen\casos\`) todavía tiene los inputs anteriores.

- **Respaldo de la versión anterior de los 6 archivos y su verificación:** scratchpad de la sesión, carpeta `bak_anexos_pre_inicio2025\`.
- **No se corrió `construir.ps1`** y no se tocó el .pptx.

## Cómo se regenera

- `python -B anexo_generacion.py 10_generacion.js [<inputs SIN_DC>]`: por omisión lee `casos_2025\SIN_DC\inputs`.
- `python -P anexos_tx_dc.py [<carpeta de casos>]`: por omisión lee `casos_2025`. También reescribe `verificacion_transmision_dc.md`, con todas sus comprobaciones.
- `40_modelo.js` se editó a mano.

## Cifras principales y su origen

| Módulo | Cifra | Origen |
|---|---|---|
| todos | Períodos 2025, 2027, 2030, 2035, 2040, 2045 y 2050; valor presente a 2025 | `periods.csv` (2025–2026, 2027–2029, …, 2050–2054) y `financials.csv` (`base_financial_year` 2025, 6 %) |
| 10 | FV: potencial de 661.787 MW desde 2025 (antes, 658.787 MW desde 2026) | suma de `gen_capacity_limit_mw` de los candidatos. Ya no se descuentan los 3.000 MW de AMEBA. Coincide con `partes\renovables\NOTAS.md` (661.786,6) |
| 10 | Eólica: potencial de 53.877 MW desde 2025 (antes, 52.877 MW) | ídem; renovables: 5.661,7 + 48.215,0 MW |
| 10 | Baterías «ley»: 2.000 MW en 3 zonas, desde 2027, costo 0 en 2030 y 2050 | `gen_info.csv` (`gen_tech` = `BESS_4h_ley`: Kimal 500 con 1.000 MW; Cumbre 500 y Nueva Cardones 500 con 500 MW cada una). El script verifica que `gen_build_costs.csv` tiene inversión y O&M fijo en 0 |
| 10 | «Desde»: FV, eólica, baterías, CAES y Carnot desde 2025; biomasa desde 2027; las demás sin cambio | mínimo de `build_year` de los candidatos por tecnología |
| 10 | Costos de 2030 y 2050 | sin cambio frente a la versión anterior (mismas filas de `gen_build_costs.csv`) |
| 10 | Matriz por zona: sube el potencial FV de Nueva Pozo Almonte 220, Lagunas 220, Kimal 220, Nueva Zaldívar 220, Nueva Pan de Azúcar 500, Quillota 500, Candelaria 500 y Rapel 500. Sube el eólico de Los Changos 220 (71 → 156) y Parinas 500 (9.078 → 9.994). Las suben suman 3.000 MW FV y 1.000 MW eólicos | potencial completo, sin descontar lo que construyó AMEBA; diferencia con la versión respaldada |
| 10 | La tabla 1 pasa a 11 pt (16 filas × 0,29 = 4,64 in) | con la fila «ley», 16 × 0,31 = 4,96 in no cabía |
| 20 | 38.519 MW existentes en los 29 corredores de red (antes, 41.191 MW) | `existing_trans_cap` es igual, corredor a corredor, a las líneas AMEBA `existente` de `lineas_ameba_a_corredores.csv` |
| 20 | 2.672,1 MW de AMEBA hasta 2025, en 7 corredores, que vuelven a ser candidatos | `partes\transmision_reserva\autocomprobacion\inversion_ameba_hasta_2025.csv`; es igual al existente de `casos_6d` menos el nuevo |
| 20 | Tope 2050 = candidatos AMEBA + obra comprometida (sin rebaja) | comprobado en los 28 corredores ampliables; p. ej., Parinas–Cumbre y Nueva Pan de Azúcar–Polpaico ya pueden ampliarse desde 2025 |
| 20 | Tope típico 500 / 500 / 500 / 2.000 / 3.500 / 3.500 / 4.500 MW (19 corredores); HVDC 0 / 0 / 2.000 / 3.500 / 5.000 / 5.000 / 6.000 MW | `trans_build_limits.csv`: 231 filas (33 × 7) |
| 20 | Obras comprometidas: HVDC con 2.000 MW y Río Malleco–Pichirropulli con 660 MW, ambas en 2030 | filas con `min_build_mw` > 0; decisión 10 (`REGLA_1_ENERO = False`) |
| 30 | MW medios agregados por período (2025 … 2050): E2 0,0 / 99,0 / 224,8 / 272,8 / 292,4 / 311,9 / 331,5; CEN 138,3 / 381,7 / 663,5 / 874,2 / 1.143,1 / 1.486,3 / 1.924,2; N1 37,5 / 324,0 / 749,8 / 1.022,8 / 1.042,4 / 1.061,9 / 1.081,5; Propio 19,5 / 460,5 / 2.003,7 / 3.034,0 / 4.504,4 / 6.664,9 / 9.839,4 | `dc_libre` + `dc_fijo` de los inputs nuevos. E2, N1 y CEN coinciden con `escenarios_dc\resumen_escenarios_dc.csv`. Las cuatro series se reconstruyen en forma independiente desde las reglas anuales |
| 30 | CEN: 398 MW de capacidad en 2025 y +5 % anual desde 2031 | `scripts\40_escenarios_dc.py` (`capacidad_cen`, `CRECIMIENTO_CEN`); reconstruido a 10⁻³ MW |
| 30 | Propio: +8 % anual desde 2033 sobre 2.119,7 MW medios (99 + 115,2 + 1.905,5), ubicable y repartido como lo solicitado en 2032 | `scripts\41_escenario_propio.py` (`CRECIMIENTO`); reconstruido por período y por zona a 2·10⁻³ MW |
| 30 | Propio, parte fija: 11,5 (2025–2026), 69,1 (2027–2029) y 115,2 desde 2030 | rampa de 20 %/año desde 2026 sobre 115,2; `dc_fijo.csv` |
| 30 | Lista de campus | sin cambio (16 campus, 3.811 MW) |
| 40 | CO₂: 0; 3,33; 10; 23,48; 35; 35 y 35 USD/t | `carbon_policies.csv` |
| 40 | Reserva: 113 proyectos elegibles | `reserva_elegibles.csv` (113 filas) |
| 40 | 1,54 millones de restricciones, 1,35 millones de variables y 8,07 millones de coeficientes | logs de `casos_2025\*\log_*.txt`: «Optimize a model with 1542355 rows, 1346239 columns and 8072317 nonzeros». Las filas varían entre 1.542.232 y 1.542.355 según el caso, y los coeficientes entre 8.072.244 y 8.072.369 |
| 40 | 6 días típicos | `timepoints.csv`: 1.008 = 6 × 24 × 7 |
| 40 | Eólica de 2025: −6,9 % frente a lo que eligió AMEBA | `partes\renovables\NOTAS.md`, autocomprobación B2 |

## Qué cambió en el texto de `40_modelo.js`

- **Inversión:** el modelo parte en 2025 y decide todas las inversiones; no usa las decisiones de inversión de AMEBA. Existente = en servicio el 1-ene-2025. Las notas listan los 7 períodos.
- **Baterías «ley»:** candidatas a costo 0 desde 2027, no comprometidas.
- **HVDC:** la regla del 1 de enero reemplaza a «el período 2026 usa los datos de 2026». Río Malleco–Pichirropulli también entra en 2030.
- **Notas nuevas:**
  - los topes anuales de FV y eólica no restringen;
  - los pendientes que siguen saliendo de AMEBA (hidro por día típico, H₂/NH₃ y 1,031);
  - el crecimiento de CEN y del escenario propio.
- **Réplica de AMEBA:** las notas aclaran que se hizo con la versión anterior.
- **Optimalidad de la ubicación:** «no verificada en las corridas con inicio en 2025».

## Pendientes

- **`[tiempo]`** en la lámina «Anexo: validación», cómputo: «Gurobi, barrera y crossover: [tiempo] por corrida». Lo llena la sesión principal.
- **Tabla de validación de la lámina 3** (498 celdas, 343 candidatos, 1.880 pares, etc.): describe la validación de la versión anterior y no se tocó. Las entradas nuevas tienen 391 candidatos y 2.346 filas de costo. La verificación nueva (`validacion\inicio_2025_entradas.md`) no da esos conteos.
- **Notas de la lámina 2 sobre 6 frente a 12 días** (efecto sobre los insumos y memoria de 63 GB): son de la versión anterior y no se tocaron.
- **Matriz por zona de `10_generacion.js`:** los encabezados «Hidro pasada» (12 caracteres) y «Gas natural» (11) quedan justo en el límite de 0,85 in a 11 pt. Ya estaban así antes.
