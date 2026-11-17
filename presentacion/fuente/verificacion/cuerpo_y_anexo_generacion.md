# Verificación: cuerpo (diapositivas 9, 10, 12 y 14), anexo de generación y motivación

Verificador independiente, 17-nov-2026. Datos: `<repo>\` (`resultados\tablas\`, `casos\SIN_DC\inputs\`, `docs\`). Recalculado con scripts propios (pandas), sin usar `anexo_generacion.py` ni `mapa_dc_2050_fig.py`. No se editó ningún archivo del deck.

## Resumen de errores

| # | Ítem | Valor en el deck | Valor correcto |
|---|------|------------------|----------------|
| E1 | `build.js`, diap. 14, «Ahorro por tipo de costo», serie «Impuesto al CO₂ y O&M variable», PELP N1 | 58 | **59** (38,37 + 20,27 = 58,63) |
| E2 | Ídem, Propio | 80 | **79** (58,66 + 20,56 = 79,22) |
| E3 | `10_generacion.js`, tabla de tecnologías, Solar FV, potencial | 661.787 | **658.787** (se restan los 3.000 MW FV de 2025) |
| E4 | Ídem, Eólica, potencial | 53.877 | **52.877** (se restan los 1.000 MW eólicos de 2025) |
| E5 | Matrices por zona, 8 celdas FV y 2 eólicas (ver §5.3) | brutas | netas de lo construido en 2025 |

E1–E2: el deck sumó los componentes ya redondeados (38 + 20; 59 + 21). Con el redondeo de la suma, los cuatro sumandos de N1 dan 708 = total; los de Propio dan 1.782 frente a un total de 1.783 (diferencia de redondeo, igual que E2: 89 + 73 + 26 + 24 = 212 frente a 211).

E3–E5: en Switch el tope `gen_capacity_limit_mw` acota la capacidad total del proyecto, incluida la predeterminada (`Max_Build_Potential`: tope ≥ GenCapacity). Diez proyectos candidatos (8 FV, 2 eólicos) traen capacidad predeterminada de 2025 (3.000 MW FV y 1.000 MW eólicos, DATOS_Y_SUPUESTOS §4: «se descuenta del potencial de cada candidato»). El anexo informa la suma bruta de los topes, pero su nota dice «ya está descontado del potencial». O se corrigen las cifras (opción recomendada) o se corrige la nota.

## 1. Diapositiva 10, «Casos de estudio: escenarios de data centers»

| Ítem | Veredicto | Valor correcto / fuente |
|------|-----------|-------------------------|
| Líneas: PELP E2 [74, 225, 273, 292, 312, 331] | OK | `escenarios_dc.csv`, `dc_total_MW` redondeado |
| Líneas: CEN [330, 591, 591, 591, 591, 591] | OK | ídem |
| Líneas: PELP N1 [262, 750, 1023, 1042, 1062, 1081] | OK | ídem |
| Líneas: Propio [355, 1899, 2021, 2021, 2021, 2021] | OK | ídem |
| Barras 2050, RM [282, 528, 282, 1621] | OK | `ubicacion_dc.csv` 2050, base, por región con `zonas.csv` (281,7; 528,4; 281,7; 1.620,7) |
| Barras 2050, Valparaíso [50, 63, 50, 400] | OK | 49,7; 62,6; 49,7; 400,0 |
| Barras 2050, Antofagasta [0, 0, 750, 0] | OK | solo N1 (Kimal220) |
| Nota: El Salto → Polpaico500, Torquemada → Quillota500, Kimal → Kimal220; Propio además AltoJahuel500 | OK | zonas con DC en `ubicacion_dc.csv` (base) |

## 2. Diapositiva 14, «Resultados: expansión del sistema»

| Ítem | Veredicto | Valor correcto / archivo |
|------|-----------|--------------------------|
| Eólica [854, 817, 1988, 3371] | OK | `inversiones_libre_menos_base.csv`, `dif_MW`, grupo Eólica |
| Solar FV [−788, −749, −2005, −3818] | OK | ídem, grupo Solar FV |
| Baterías [−208, 12, −174, −246] | OK | ídem, grupo Baterías |
| Bombeo [−150, −287, −690, −1264] | OK | ídem, grupo Bombeo |
| Transmisión [−2397, −1250, −1626, −4611] | OK | `transmision_libre_menos_base.csv`, suma de `dif_MW` por escenario |
| Inversión gen. y almac. [89, 91, 378, 1435] | OK | `costos_por_componente.csv`, columna «base − libre», fila «Generación y almacenamiento: inversión + O&M fijo» |
| Combustible [73, 117, 205, 129] | OK | ídem, fila Combustible |
| Transmisión [26, 35, 66, 139] | OK | ídem, fila «Transmisión: inversión + O&M fijo» |
| CO₂ + O&M variable, E2 = 24 | OK | 19,93 + 3,58 = 23,51 |
| CO₂ + O&M variable, CEN = 33 | OK | 23,71 + 9,19 = 32,90 |
| CO₂ + O&M variable, N1 = 58 | **ERROR** | **59** (58,63) |
| CO₂ + O&M variable, Propio = 80 | **ERROR** | **79** (79,22) |
| Totales entre paréntesis (211, 275, 708, 1.783) | OK | `costos_por_componente.csv`, TOTAL, «base − libre» |
| Total sin DC 40.538 (diap. 11) | OK | TOTAL SIN_DC = 40.538,2 |

## 3. `graficos\mapa_dc_2050_datos.csv`

| Ítem | Veredicto | Valor correcto |
|------|-----------|----------------|
| 24 filas (4 escenarios × base/libre × región) | OK | mismas 24 combinaciones escenario–modo–región que el recálculo; ninguna sobra ni falta |
| `mw_medios` | OK | diferencia máxima 6e−14 frente a `ubicacion_dc.csv` 2050 agregado por región con `zonas.csv` |
| `mw_capacidad` = `mw_medios` / 0,5 | OK | diferencia máxima 1e−13 |

## 4. Diapositiva 9, «Casos de estudio: sistema modelado»

| Ítem | Veredicto | Respaldo |
|------|-----------|----------|
| (a) 26 barras + 5 polos = 31 zonas | OK | `zonas.csv`: 31 zonas, 26 con `candidata_dc` = True y 5 polos PDGE |
| (a) 34 corredores | OK | `transmission_lines.csv`: 34 filas (29 de red + 5 de enlace a polos, DATOS_Y_SUPUESTOS §6) |
| (b) Lista de tecnologías candidatas | OK, completa | candidatos de `gen_info.csv` (sin predeterminado, construibles 2026–2050): FV, Eólica, CSP 6/9/13 h, Hidro_Pasada_Candidata, Geotermia, Biomasa, GNL_CC, GNL_CA, GNLCCS, Diesel_CA, BESS 1/2/4/6/8 h, Bombeo, CAES_4h, Carnot 4/12 h. Ni más ni menos. («gas» agrupa ciclo combinado, ciclo abierto y con captura) |
| (c) «solo se amplían los corredores existentes» | OK, con matiz | `trans_build_limits.csv` cubre 33 de los 34 corredores, ninguno fuera de `transmission_lines.csv`; FORMULACION §4.5 fija T = 0 fuera de esa lista, así que no hay corredores nuevos entre zonas no listadas. Matiz: 6 de los 34 parten con 0 MW (los 5 enlaces a polos y el HVDC); «existentes» se lee como «de la red de la PELP». Kimal220–LosChangos220 no se amplía (sin topes, `trans_new_build_allowed` = 0) |
| (d) HVDC Kimal–Lo Aguirre en 2030, obra comprometida | OK | corredor Kimal500_AltoJahuel500, mín. = máx. = 2.000 MW en 2030 (`trans_build_limits.csv`); DATOS_Y_SUPUESTOS §6 y FORMULACION §4.5. En el modelo el terminal está en AltoJahuel500 |
| (e) 110 TWh en 2030 y 272 TWh en 2050 | OK | DATOS_Y_SUPUESTOS: 110,5 y 272,2 TWh; recalculado de `loads.csv` de SIN_DC con los pesos de `timeseries.csv`: 110,4 y 272,0 |

## 5. Anexo de generación (`anexos\10_generacion.js`)

Candidatos = proyectos con fila en `gen_build_costs.csv` para un período 2026–2050 que no está en `gen_build_predetermined.csv`. Potencial = suma de `gen_capacity_limit_mw`; en CSP, baterías y Carnot, máximo entre duraciones por zona (como dice la nota).

### 5.1 Tabla de tecnologías

| Tecnología | Zonas | Potencial (MW) | Desde | 2030 (USD/kW) | 2050 (USD/kW) | Veredicto |
|------------|-------|----------------|-------|---------------|---------------|-----------|
| Solar FV | 27 OK | 661.787 bruto; **658.787 neto** | 2026 OK | 628–794 OK | 454–573 OK | **ERROR** en potencial |
| Eólica | 20 OK | 53.877 bruto; **52.877 neto** | 2026 OK | 1.020–1.408 OK | 852–1.192 OK | **ERROR** en potencial |
| CSP (6, 9 y 13 h) | 13 OK | 51.875 OK | 2030 (13 h) OK; 6 y 9 h desde 2035 | 4.800 OK | 2.934–3.906 OK | OK |
| Hidro de pasada | 8 OK | 6.313 OK | 2035 OK | — OK | 3.250 OK | OK |
| Geotermia | 8 OK | 1.682 OK | 2030 OK | 5.689 OK | 4.960 OK | OK |
| Biomasa | 5 OK | 201 OK | 2026 OK | 2.948 OK | 2.761 OK | OK (6 proyectos; Ancoa y Charrúa están en NuevaCharrua500) |
| Gas, ciclo combinado | 10 OK | 10.000 MW por sitio OK | 2030 OK | 1.053 OK | 1.053 OK | OK |
| Gas, ciclo abierto | 10 OK | ídem | 2030 OK | 791 OK | 791 OK | OK |
| Gas con captura | 3 OK | ídem | 2030 OK | 2.370 OK | 1.769 OK | OK |
| Diésel | 4 OK | ídem | 2030 OK | 470 OK | 470 OK | OK |
| Baterías (1–8 h) | 26 OK | 85.000 OK (máx. por zona: 5.000 en 11 zonas del norte, 2.000 en 15) | 2026 OK | 413–1.524 OK | 314–1.144 OK | OK |
| Bombeo | 13 OK | 42.278 OK | 2030 OK | 1.605 OK | 1.605 OK | OK |
| CAES 4 h | 26 OK | 52.000 OK | 2026 OK | 1.014 OK | 899 OK | OK |
| Carnot (4 y 12 h) | 2 OK | 1.242 OK | 2026 OK | 796–1.433 OK | 796–1.433 OK | OK |

### 5.2 Matrices por zona (diapositivas 2 y 3 del anexo)

Se compararon las 27 filas completas (no solo 10 celdas): todas las celdas coinciden con la suma bruta de topes por zona y tecnología, incluidas las marcas ✓ de gas, captura y diésel y la fila «Polos PDGE (5)» (FV 11.558, eólica 2.291, CSP 5.742). Ejemplos: Parinacota bombeo 16.889; Kimal 500 Carnot 853; Los Changos 500 Carnot 389; Concepción biomasa 63; Nueva Charrúa hidro 1.973; Nueva Ancud eólica 11.212; Pichirropulli hidro 1.669; Nueva Puerto Montt bombeo 3.333; Nueva Pan de Azúcar CSP 40; Polpaico hidro 30. Única discrepancia: las 10 celdas de §5.3.

### 5.3 Celdas que cambian si se descuenta lo construido en 2025 (ERROR E5)

| Zona | Tecnología | Deck (bruto) | Correcto (neto) |
|------|------------|--------------|-----------------|
| Kimal 220 | FV | 57.791 | 57.337 |
| Nueva Pozo Almonte 220 | FV | 40.317 | 39.281 |
| Lagunas 220 | FV | 36.307 | 36.232 |
| Nueva Zaldívar 220 | FV | 23.394 | 22.581 |
| Nueva Pan de Azúcar 500 | FV | 26.151 | 25.949 |
| Quillota 500 | FV | 11.274 | 11.198 |
| Candelaria 500 | FV | 11.381 | 11.099 |
| Rapel 500 | FV | 41.577 | 41.515 |
| Los Changos 220 | Eólica | 156 | 71 |
| Parinas 500 | Eólica | 9.994 | 9.078 |

Alternativa si se prefiere dejar las cifras brutas: cambiar en la nota «ya está descontado del potencial» por «el potencial incluye 3.000 MW FV y 1.000 MW eólicos construidos en 2025».

## 6. Motivación (`contenido.js`) frente a las extracciones A y B

| Ítem | Veredicto | Respaldo |
|------|-----------|----------|
| Mundo [269, 361, 416, 946, 1193] TWh (2020, 2023, 2024, 2030*, 2035*) | OK | A y B: IEA 2025, tabla A.1, p. 258 |
| EE. UU. [60, 76, 176, 325, 580] TWh (2014, 2018, 2023, 2028 bajo/alto) | OK | A y B: Shehabi et al. 2024 |
| Notas: 1,9 %, 4,4 %, 6,7–12 %; rango 2035 ~700–1.720 | OK | A y B |
| Reducciones 2025, solar (12 meses) | OK | A y B, CEN 2026b fig. 13 |
| Reducciones 2025, eólica (12 meses) | OK | A y B |
| Total 6.084 GWh | OK | cifra textual del reporte (A y B); la suma de las etiquetas da 6.086 por redondeo |
| Polpaico–Nueva Pan de Azúcar 500, 1.305 h | OK | A y B, tabla 4 |
| Chile: solicitudes [428, 440, 452, 1330, 1818, 3318] y CEN [398, 552, 642, 963, 1281, 1381] | OK, sin contraste en A/B | coincide con `motivacion_grafico.csv` (acumulado 428,4…3.318,4); A y B no extrajeron CEN 2026a fig. 5-13 |
