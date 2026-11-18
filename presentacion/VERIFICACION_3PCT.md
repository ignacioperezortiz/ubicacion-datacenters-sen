# Verificación independiente del deck con crecimiento de 3 % anual

17-nov-2026. Deck: `Presentacion de avance - Ubicacion de data centers en el SEN.pptx` y su `.pdf` (ambos de las 23:40). Cambio verificado: CEN y PROPIO crecen 3 % anual después del horizonte de su proyección (CEN desde 2031, PROPIO desde 2033), y se volvieron a correr esos dos escenarios. PELP E2, PELP N1 y SIN_DC no cambiaron (sin diferencias en git).

Fuentes del recálculo:

- `casos\<CASO>\outputs_*\`: `total_cost.txt`, `cost_components.csv`, `costs_itemized.csv`, `DCUbicado.csv`, `BuildGen.csv`, `gen_cap.csv`, `BuildTx.csv`, `transmission.csv`, `emissions.csv` y `precios_zonales_anuales.csv`.
- `casos\<CASO>\inputs\`: `dc_base.csv`, `dc_libre.csv`, `dc_fijo.csv`, `dc_candidatas.csv`, `gen_info.csv`, `gen_build_predetermined.csv`, `trans_build_limits.csv`, `transmission_lines.csv`, `load_zones.csv`, `timepoints.csv`, `periods.csv` y `financials.csv`.
- `presentacion\fuente\datos\campus_escenario_propio.csv`, `casos\corrida_2025.txt` y los `log_*.txt`.

No se usaron `cifras.json` ni el código que arma el deck. Las tablas de `resultados\tablas\` solo se usaron para comparar, y coinciden con el recálculo.

Método. El valor presente usa el factor de Switch: anualidad de fin de año de los años del período × descuento al inicio del período, base 2025, 6 %. Con él, Σ costo anual × factor reproduce `total_cost.txt` al dólar (comprobado en CEN libre y PROPIO base). Las trayectorias de CEN y PROPIO se reconstruyeron desde los datos primarios:

- **CEN:** capacidad 398…1.381 MW (2025–2030), +3 %/año desde 2031, × 0,5, reparto 1.225/1.381 + 155/1.381, − 99.
- **PROPIO:** los 16 campus de las láminas 26 y 27 por año de conexión, × 0,5, más el llenado. Desde 2033, 2.119,7 × 1,03^(año − 2032).

Las dos reproducen `dc_libre.csv` y `dc_base.csv` a 10⁻⁴ MW. La «capacidad nueva» es Σ `BuildGen` de los años 2025–2050, menos lo predeterminado. La transmisión es Σ `BuildTx`, igual a la diferencia de `TxCapacityNameplate` en 2050.

## Cifras y afirmaciones

| Cifra o afirmación | Lámina | Resultado | Valor recalculado |
|---|---|---|---|
| 31 zonas, 34 corredores, 26 barras candidatas | 9, 8 | OK | `load_zones.csv` 31; `transmission_lines.csv` 34; `dc_candidatas.csv` 26 |
| 7 períodos 2025–2054; 6 días típicos × 24 h | 9 | OK | `periods.csv`; 144 timepoints por período |
| Demanda CN 110 TWh (2030) y 272 TWh (2050) | 9 | OK | 110,4 y 272,0 TWh |
| 1,54 M restricciones; 10–18 min por corrida | 9, 30 | OK | 1.542.353 filas; reloj 10,0–17,6 min (`corrida_2025.txt`; CEN 13,8/12,8 y PROPIO 11,3/14,7 de esta noche) |
| 1,35 M variables; 8,07 M coeficientes | 30 | OK | 1.346.239 columnas; 8.072.244 no ceros (log de CEN base) |
| Trayectorias de MW medios (28 puntos del gráfico) | 10 | OK | E2 0/99/225/273/292/312/331; CEN 138/382/634/750/886/1.042/1.224; N1 38/324/750/1.023/1.042/1.062/1.081; Propio 20/460/1.938/2.360/2.752/3.206/3.733 (base = libre por período) |
| Ubicación proyectada 2050 por región (12 barras) | 10 | OK | RM 282/1.090/282/2.973; Valparaíso 50/134/50/759; Antofagasta 0/0/750/0 |
| «3 % anual: CEN desde 2031 y propio desde 2033» | 10, 25, 27, 15 | OK | Reconstruido desde los datos primarios; con 5 % y 8 % daría 1.924,2 y 9.839,4 en 2050, como en la versión anterior |
| Notas: la PELP crece E2 ~1,4 %/año; N1 ~0,4 %/año desde 2035 | 10 (notas) | OK (aprox.) | E2: 1,43 % (total con los 99 existentes, 2030→2050). N1: 0,34 % sobre el total o 0,37 % sobre lo agregado |
| Data centers que ya operan, ~100 MW medios | 10 | OK | 99 (84,15 + 14,85) |
| Sistema sin data centers: 42.619 MMUSD | 11 | OK | 42.618,8 |
| Extra base 1.040 / 3.496 / 3.503 / 9.724 | 11 | OK | 1.039,9 / 3.496,2 / 3.502,8 / 9.724,4 |
| Extra libre 861 / 2.997 / 2.883 / 7.322 (barras) | 11 | OK | 860,8 / 2.996,6 / 2.883,2 / 7.322,5 |
| Ahorro 179 / 500 / 620 / 2.402 | 11, 14, 15 | OK | 179,1 / 499,7 / 619,7 / 2.401,9 |
| % del extra 17 / 14 / 18 / 25 | 11 | OK | 17,23 / 14,29 / 17,69 / 24,70 |
| «Evita entre el 14 % y el 25 % del costo extra» | 11, 15 | OK | 14,3–24,7 % |
| Ahorro por MWh reubicado: 11,9 a 14,0 USD/MWh | 11, 15 | OK | E2 12,38; CEN 13,45; N1 11,87; Propio 14,04. Energía reubicable en VP: 14,48 / 37,15 / 52,20 / 171,04 TWh |
| Notas: reubicable en 2050 70 / 69 / 70 / 86 % | 11 (notas) | OK | 70,1 / 68,8 / 70,0 / 86,4 % |
| Notas: extra por MWh, 40 a 44 (proyectada) y 33 a 38 (óptima) | 11 (notas) | OK | Base 41,9 / 44,1 / 40,4 / 43,5. Libre 34,7 / 37,8 / 33,3 / 32,8 USD/MWh. Energía DC en VP: 24,82 / 79,27 / 86,67 / 223,34 TWh |
| Mapa: 24 etiquetas, capacidad = MW medios / 0,5 | 12 | OK | E2 99/563 → 30/168/465; CEN 268/2.181 → 78/685/1.685; N1 1.500/99/563 → 450/30/168/1.515; Propio 1.519/5.947 → 200/813/351/718/5.383. El PNG del pptx es idéntico (md5) a `mapa_dc_2050.png` |
| Notas: lo reubicable va al sur; en RM, Valparaíso y Antofagasta queda lo conectado antes de 2030 | 12 (notas) | OK | En libre, Polpaico/Quillota/Kimal/Alto Jahuel quedan exactamente en su nivel de 2027 (+ llenado fijo en Propio) |
| Tabla proyectada → óptima por zona (17 pares, 34 valores) | 13 | OK | E2: Quillota 49,7→14,9; Polpaico 281,7→84,2; N. Ancud 0→232,5. CEN: 133,8→39,1; 1.090,5→342,5; 0→842,6. N1: Kimal 750→225; 49,7→14,9; 281,7→84,2; 0→757,5. Propio: 759,4→100,0; 1.658,0→310,4; A. Jahuel 1.315,3→96,2; R. Malleco 0→175,6; Pichirropulli 0→359,1; N. P. Montt 0→294,4; N. Ancud 0→2.397,2 |
| 2040, sin data centers: 23,0–25,3 USD/MWh en el sur y 37,5–38,1 en las zonas proyectadas | 13 | OK | Sur elegido: N. Ancud 22,97, N. P. Montt 23,36, Pichirropulli 24,08, R. Malleco 25,31. Proyectadas: A. Jahuel 37,48, Kimal 220 37,53, Polpaico 38,07, Quillota 38,07 |
| Ancoa–N. Charrúa y Los Changos 220–N. Zaldívar 220 en tope en los 9 casos | 13 | OK (ver observación 2) | Son los únicos dos en tope en 2050 en los 9 casos. Río Malleco–Mulchén llega al tope en 8 de 9 (Propio libre: 4.324 de 4.500) |
| «Todo lo reubicable va al sur en los 4 escenarios» | 13 | OK | En libre, todo lo que sale de las zonas proyectadas va a N. Ancud, N. P. Montt, Pichirropulli y R. Malleco, en todos los períodos |
| Notas: en libre queda lo de antes de 2030 y, en Propio, el llenado | 13 (notas) | OK | Propio libre: Polpaico 216,7 + 93,7; A. Jahuel 74,7 + 21,5; Quillota 100 |
| Cambio de capacidad, óptima − proyectada (eólica / FV / baterías / bombeo) | 14 | OK | E2 +769 / −681 / −121 / −219. CEN +1.851 / −2.093 / −32 / −789. N1 +1.802 / −1.767 / −109 / −678. Propio +4.908 / −7.632 / −836 / −1.633 (MW construidos 2025–2050) |
| Cambio de transmisión −1.997 / −2.566 / −1.651 / −8.075 | 14 | OK | −1.996,6 / −2.566,3 / −1.651,1 / −8.074,8 MW (Σ `BuildTx` = capacidad 2050) |
| Ahorro por componente: inversión gen. + alm. | 14 | OK | 58,6 / 294,9 / 288,2 / 1.726,0 |
| Ahorro por componente: combustible | 14 | OK | 79,4 / 99,9 / 205,6 / 340,0 |
| Ahorro por componente: transmisión | 14 | OK | 21,8 / 70,1 / 65,5 / 229,7 |
| Ahorro por componente: CO₂ + O&M variable | 14 | OK | 19,3 / 34,7 / 60,4 / 106,1 (ENS y costo DC = 0) |
| «En los cuatro escenarios, más eólica y menos FV, baterías, bombeo y transmisión» | 14, 15 | OK | Los 4 signos se cumplen en los 4 escenarios. Ninguna otra tecnología cambia más de 0,5 MW: ya no aparecen el gas de punta ni la CSP de la versión con 8 % |
| Cada MW medio pide 4,2–4,5 MW nuevos, en vez de 5,0–5,6 | 14 | OK | Libre 4,38 / 4,50 / 4,28 / 4,22; base 5,14 / 5,37 / 4,98 / 5,61 |
| Emisiones acumuladas 2025–2054 bajan entre 1,3 y 7,0 Mt CO₂ | 14 | OK | 1,31 / 2,27 / 4,23 / 6,98 Mt |
| «179 a 2.402 millones de USD» | 15 | OK | 179,1 a 2.401,9 |
| «Ubicación óptima en el sur, donde la energía es más barata y los corredores hacia el centro están al tope» | 15 | OK (ver observación 2) | Ancoa–N. Charrúa en tope en todos los períodos de los 9 casos; N. Charrúa–Mulchén en tope 2030–2045 en los 9 |
| Propio llega a 3.733 MW medios en 2050–2054 | 15 | OK | 3.732,76 (3.617,56 ubicable + 115,2 fijo) |
| Japón 16–20 % (Onodera et al., 2026) | 15 | No verificado | Fuera del alcance (no es un resultado); coincide con la lámina 5 |
| Tabla de MW medios agregados (35 celdas) | 25 | OK | Coincide con la suma por período de `DCUbicado` + `dc_fijo` en las 35 celdas (fija: 11,52 / 69,12 / 115,2) |
| CEN: RM → Polpaico 1.225 MW; Valparaíso → Quillota 155 MW | 25 | OK | 0,5 × capacidad × 1.225/1.381 − 84,15 y × 155/1.381 − 14,85 reproduce `dc_base.csv` (2050: 1.090,5 y 133,8) |
| Pie: «CEN crece 3 % desde 2031 y Propio 3 % desde 2033» | 25 | OK | Reconstruido |
| Notas: CEN 398/552/642/963/1.281/1.381; 3 % hasta 2.807 MW en 2054 | 25 (notas) | OK | 1.381 × 1,03²⁴ = 2.807,3 (con el reparto 1.380/1.381, el modelo llega a 2.805,3) |
| Notas: E2 99 / 297 / 364 / 450 (2057), 85/15 %; N1 +75 MW medios/año hasta 750 en 2035 | 25 (notas) | OK | Interpolando, se reproducen los promedios por período (p. ej. E2 2030: 323,8 − 99 = 224,8; N1 Kimal 37,5 / 225 / 525 / 750) |
| Notas: Propio 1.905,5 + 115,2 (11,5; 69,1) + 99 = 2.119,7 | 25, 27 (notas) | OK | Aritmética y `dc_fijo.csv` |
| Total Polpaico 1.648 (9 campus) | 26 | OK | Suma de las filas y de `campus_escenario_propio.csv` |
| Excluidas: 12 hasta 2025 (428,4 MW), 2 repetidas (14 MW), 2 sin MW | 26 | OK | 12 «existente» = 428,4 MW; 2 «repetida» (14 + s/d); 2 «sin_mw» |
| Notas: 35 solicitudes, 4.233,4 MW | 26 (notas) | OK | 35 filas; 428,4 + 3.791 + 14 = 4.233,4 (SAN2 no está en el CEN) |
| 3.811 MW, 16 campus = 1.905,5 MW medios (824 / 681,5 / 400) | 27 | OK | 1.648 + 1.363 + 800; × 0,5 |
| Llenado 428,4 × 50 % − 99 = 115,2 (93,7 / 21,5), rampa de 20 %/año hasta 2030 | 27 | OK | Conectado: Polpaico 348,4 y A. Jahuel 80 MW. Rampa 0/20 % → 11,52; 40/60/80 % → 69,12 |
| Notas: 8,0 / 391,3 / 1.822,5 MW medios por período | 27 (notas) | OK | 8,0 / 391,33 / 1.822,54 (= `dc_libre.csv`) |
| Notas: «en 2050–2054 el escenario agrega 3.732,8 MW medios» | 27 (notas) | OK | 3.732,76 |
| Notas: en 2030 la cartera suma 2.896 MW, frente a 1.381 del CEN | 27 (notas) | OK | 2.896 (y 3.318 del gráfico de la lámina 2 = 2.896 + 428 − 20 + 14) |
| Ubicación libre desde 2030 en 26 barras | 28 | OK | `dc_candidatas.csv`; antes de 2030, libre = base |
| **Notas: «CEN crece 5 % anual desde 2031 y el escenario propio 8 % anual desde 2033»** | **28 (notas)** | **ERROR** | **Debe decir 3 % y 3 %. El texto viene de `presentacion\fuente\anexos\40_modelo.js`, línea 46, que no se actualizó** |
| Ningún texto con 5 % u 8 % de crecimiento | todo el deck y el PDF | ERROR (solo la anterior) | Única aparición: notas de la lámina 28. El PDF no la muestra porque no incluye notas |
| Ningún texto dice que PROPIO ubica data centers en el Norte Grande | todo el deck y el PDF | OK | Sin menciones. «Norte grande» no aparece. Antofagasta/Kimal solo como ubicación proyectada de N1 |
| PDF = pptx | 10–15, 25–27, 30 | OK | El texto extraído del PDF tiene las mismas cifras |

Cifras comprobadas: unas 300 (58 ítems), entre ellas 28 puntos de trayectoria, 34 valores de la tabla por zona, 35 celdas de la tabla de escenarios, 24 etiquetas del mapa, 20 cambios de capacidad y 16 componentes de ahorro.

## Errores

1. **Lámina 28, notas del orador.** Dice «Después del horizonte de cada proyección, CEN crece 5 % anual desde 2031 y el escenario propio 8 % anual desde 2033». Debe decir «3 % anual» en los dos casos. El origen es `presentacion\fuente\anexos\40_modelo.js`, línea 46, que no cambió esta noche. Corregir ahí y regenerar. El PDF no se ve afectado porque no incluye notas.

## Observaciones (no son errores numéricos)

1. **Fuera del deck, con el mismo texto viejo:** `docs\ANALISIS.md`, línea 46 («crece 5 % anual», «crece 8 % anual»). También `presentacion\fuente\anexos\verificacion_inicio_2025.md`, líneas 34–35, aunque ese es un registro de la verificación anterior y puede quedar así.
2. **Lámina 13, «Por qué el sur», viñeta 2, y lámina 15, viñeta 4.** Los Changos 220 – Nueva Zaldívar 220 está en Antofagasta: no es un corredor sur–centro y no explica por qué conviene el sur. Lo que sí respalda el argumento:
   - Ancoa 500 – Nueva Charrúa 500 está en su tope en todos los períodos de los 9 casos.
   - Nueva Charrúa 500 – Mulchén 500 está en su tope de 2030 a 2045 en los 9 casos.
   - Río Malleco – Mulchén llega al tope en 2050 en 8 de 9 casos (en Propio libre queda en 4.324 de 4.500 MW).

   Redacción sugerida: «El corredor Ancoa 500 – Nueva Charrúa 500 está en su tope en todos los períodos de los 9 casos (y Nueva Charrúa 500 – Mulchén 500, de 2030 a 2045)».
3. **Lámina 10, notas.** «La capacidad crece 3 % anual desde 2031 (antes quedaba plana en 1.381 MW)»: «antes» puede leerse como la versión inmediatamente anterior, que usaba 5 %. Sugerido: «(la proyección del CEN termina en 2030 con 1.381 MW)».
4. **Lámina 25, notas.** «Hasta 2.807 MW en 2054» supone 1.381 MW. El modelo reparte 1.225 + 155 = 1.380, así que llega a 2.805 MW. Es un 0,07 %, irrelevante (igual que en la verificación v2).
5. **Lámina 10, notas.** «N1 ~0,4 % anual desde 2035»: da 0,34 % sobre la demanda total de data centers y 0,37 % sobre lo agregado. «~0,4 %» vale solo con la segunda base, y el «~1,4 %» de E2 usa la primera. Es aceptable como aproximación.
6. **Avisos de la v2 que ya no aplican:**
   - El rango «sur» (23,0–25,3) ya no se superpone con el de las zonas proyectadas (37,5–38,1).
   - El Norte Grande ya no aparece en ninguna ubicación óptima.
   - Propio libre ya no construye gas de punta ni deja de construir CSP.
   - La lámina 14 ya dice «MW medio».
   - El eje de la lámina 11 ya usa separador de miles.

## Diagramación (PNG a 110 dpi del PDF, láminas 10–15, 25–27 y 30)

- **Lámina 11, gráfico de barras.** El segmento de ahorro de PELP E2 (179) sigue sin etiqueta. En CEN, la etiqueta blanca «500» ocupa todo el ancho del segmento gris, de borde a borde. La de N1 («620») apenas cabe. La tabla de la derecha da las cifras, así que es menor. Corrección: etiquetas de ahorro por fuera de la barra y en color oscuro, o quitarlas.
- **Lámina 12, mapa.** Hay círculos superpuestos:
  - Propio, proyección: Valparaíso (1.519) queda dentro de la RM (5.947).
  - Propio, óptima: Los Ríos (718) se monta sobre Los Lagos (5.383), y Valparaíso (200) sobre la RM (813).

  Las etiquetas se leen. Es aceptable.
- **Lámina 14.** La barra de baterías de CEN (−32 MW) casi no se ve, lo que es esperable por su tamaño. Sin desbordes.
- **Lámina 30.** «0,0006 USD/MWh» se parte en dos líneas en la columna «Dif. máx.». Es cosmético y ya estaba así.
- **Láminas 10, 13, 15, 25, 26 y 27:** sin textos tapados, desbordes ni gráficos vacíos.

## Correcciones aplicadas después de esta verificación (18-nov-2026)

- **Error 1, lámina 28, notas:** corregido en `fuente\anexos\40_modelo.js`. Ahora dice que CEN y el escenario propio crecen 3 % anual, desde 2031 y 2033.
- **Observación 2, láminas 13 y 15:** el argumento del sur cita solo los corredores en su tope que traen energía del sur al centro. Son los que tienen algún extremo en el Centro-Sur o el Sur y ninguno en el norte (`corredores_sur_en_tope_todos` en `extraer_cifras.py`). Queda «El corredor Ancoa 500 – Nueva Charrúa 500 llega a su tope de ampliación en los 9 casos».
- **Observación 3, lámina 10, notas:** «(la proyección del CEN termina en 2030 con 1.381 MW)».
- **Lámina 12, mapa (18-nov, a pedido de Ignacio):**
  - los círculos miden a lo más 30 pt de diámetro (antes 44) y mantienen el área proporcional a la capacidad;
  - los de regiones vecinas se separan hasta no tocarse, así que ya no hay superposiciones;
  - las cifras no cambian.
- **Sin cambios, por ser menores:** observaciones 4 y 5 y la diagramación de las láminas 11 y 30.
- **Observación 1 (`docs\ANALISIS.md`):** se corrige junto con las cifras de la documentación.
