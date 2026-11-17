# Verificación independiente del deck v2 (inicio 2025)

17-nov-2026. Deck: `Presentacion de avance - Ubicacion de data centers en el SEN.pptx` (pptx de las 20:23:03). Todas las cifras de las láminas 9–15 se recalcularon desde `casos\<CASO>\outputs_*\total_cost.txt`, `costos_anuales.csv` (con el factor de Switch: anualidad de fin de año × descuento al inicio del período, base 2025), `ubicacion_dc.csv`, `escenarios_dc.csv`, `inversiones_libre_menos_base.csv`, `transmision.csv`, `BuildTx.csv`, `emisiones_vertimiento.csv`, `precios_zonales.csv`, `transmision_libre_menos_base.csv` y `tiempos_computo.csv`. No se usó `cifras.json`.

## Cifras y afirmaciones

| Ítem | Lámina | Veredicto | Valor recalculado / corrección |
|---|---|---|---|
| Costo sin DC 42.619 MMUSD | 11 | OK | 42.618,8 |
| Extra base 1.040 / 4.263 / 3.503 / 16.184 | 11 | OK | 1.039,9 / 4.263,4 / 3.502,8 / 16.184,1 |
| Extra libre 861 / 3.491 / 2.883 / 11.635 | 11 | OK | 860,8 / 3.491,5 / 2.883,2 / 11.635,1 |
| Ahorro 179 / 772 / 620 / 4.549 | 11, 15 | OK | 179,1 / 772,0 / 619,7 / 4.549,0 |
| % del extra 17 / 18 / 18 / 28 | 11, 15 | OK | 17,2 / 18,1 / 17,7 / 28,1 |
| Ahorro por MWh reubicado 11,9–14,9 USD/MWh | 11, 15 | OK | E2 12,4; CEN 13,9; N1 11,9; Propio 14,9 |
| Extra por MWh: 40–45 (base) y 32–36 (libre) | 11 (notas) | OK | 40,4–45,2 y 32,5–35,7 |
| Reubicable 2050: 70 / 80 / 70 / 95 % | 11 (notas) | OK | 70,1 / 80,2 / 70,0 / 94,9 |
| Trayectorias DC por período (gráfico) | 10 | OK | coinciden con la suma por período de `ubicacion_dc.csv` (base = libre) |
| Ubicación proyectada 2050 por región | 10 | OK | E2 282/50; CEN 1.712/212; N1 282/50/750; Propio 7.798/2.041 |
| Tabla base → óptima por zona (48 celdas) | 13 | OK | todas coinciden (p. ej. Propio N. Ancud 0 → 4.524; N1 Kimal 750 → 225) |
| Mapa: capacidad por región = MW medios / 0,5 | 12 | OK | `mapa_dc_2050_datos.csv` coincide con `ubicacion_dc.csv` en las 27 filas; etiquetas del PNG iguales |
| Cambio de capacidad: eólica / FV / baterías / bombeo | 14 | OK | E2 +769/−681/−121/−219; CEN +2.876/−3.448/−556/−773; N1 +1.802/−1.767/−109/−678; Propio +11.249/−12.831/−1.796/−1.147 (capacidad construida, `inversiones_libre_menos_base`) |
| Cambio de transmisión | 14 | OK | −1.997 / −6.597 / −1.651 / −14.615 MW (igual con `transmision.csv` 2050 y con `BuildTx.csv`) |
| Ahorro por componente | 14 | OK | Inv. gen.+alm. 59/510/288/3.281; combustible 79/109/206/525; transmisión 22/116/65/548; CO₂+O&M var. 19/38/60/195 |
| MW nuevos por MW de DC: 4,3–4,4 vs 5,0–5,3 | 14 | OK (ver aviso) | libre 4,28–4,38; base 4,98–5,27, por MW **medio** de DC en 2050 |
| Emisiones acumuladas bajan 1,3–10,5 Mt | 14 | OK | 1,31 / 2,21 / 4,23 / 10,52 Mt |
| «Más eólica y menos FV, baterías, bombeo y transmisión» | 14, 15 | OK (ver aviso) | se cumple en los 4 escenarios; en Propio libre además +760 MW de gas ciclo abierto y −2.563 MW de CSP |
| Precio 2040 sin DC: 23,0–37,9 elegidas; 37,5–38,1 proyectadas | 13 | OK numérico; argumento débil | elegidas: sur 23,0–25,3, norte grande 37,3–37,9; proyectadas: Alto Jahuel 37,5, Kimal 37,5, Polpaico/Quillota 38,1 |
| Corredores en tope en los 9 casos | 13 | OK | solo Ancoa–Nueva Charrúa (3.000 + 4.500) y Río Malleco–Mulchén (1.290 + 4.500) |
| Zonas elegidas: norte grande y sur | 12 (notas), 15 | OK (ver aviso) | E2, CEN y N1 solo Nueva Ancud (sur); el norte grande aparece solo en Propio |
| 9.839 MW medios Propio 2050–2054 | 15, 25 | OK | 9.839,4 |
| 31 zonas, 34 corredores, 7 períodos, 6 días × 24 h | 9 | OK | `zonas.csv`, `transmission_lines.csv`, `periods.csv`, 42 series de tiempo |
| Demanda CN 110 TWh (2030) y 272 TWh (2050) | 9 | OK | 110,4 y 272,0 TWh |
| 1,54 M restricciones; 10–18 min por corrida | 9 | OK | 1.542.353 filas; reloj 10,0–17,6 min |
| Tamaño 1,54 M / 1,35 M / 8,07 M | 30 | OK | 1.542.353 / 1.346.239 / 8.072.244 |
| **Tiempo de corrida «[tiempo] por corrida»** | **30** | **ERROR** | marcador sin reemplazar; debe decir «10 a 18 min por corrida» (ya corregido en `anexos\40_modelo.js` a las 20:23:59, después de generar el pptx: falta regenerar) |
| **«valor presente 2026»** en la tabla de términos | **6** | **ERROR** | «Factor que lleva a valor presente 2025…» (`build.js`, línea 311) |
| **«valor presente 2026»** en notas | **4 (notas)** | **ERROR** | «C es el costo total del sistema en valor presente 2025…» (`build.js`, línea 270) |

## Anexos: 20 controles puntuales

| Ítem | Lámina | Veredicto | Fuente |
|---|---|---|---|
| Existente de los 29 corredores 38.519 MW | 22, 23 | OK | `transmission_lines.csv` |
| N. Pozo Almonte–Parinacota 450 MW; Kimal 220–Los Changos 220 900 MW sin ampliación | 22 | OK | idem |
| Ancoa–Nueva Charrúa 3.000; N. Pan de Azúcar–Polpaico 2.500 | 23 | OK | idem |
| Río Malleco–Pichirropulli 483 + 660 (2030), tope 6.160 | 23, 24 | OK | `trans_build_limits.csv` |
| HVDC 0 / 0 / 2.000 forzada / 3.500 / 5.000 / 5.000 / 6.000 | 24 | OK | idem |
| Típico 500/500/500/2.000/3.500/3.500/4.500 en 19 de 28 corredores | 24 | OK | idem |
| Costo 17.950–625.600 USD/MW; factor 0,0665; anualidad 1.193–41.578 | 24 | OK | `transmission_lines.csv`, `trans_params.csv` (40 años) |
| Baterías «ley» 1.000 + 500 + 500 MW, costo 0, desde 2027 | 19, 29 | OK | `gen_info.csv`, `gen_build_costs.csv` |
| ESS_NuevaPozoAlmonte220_8h vuelve a tope 600 MW | (CAMBIO) | OK | `gen_info.csv` |
| Guacolda NH₃ y 3 reconversiones de 2026 predeterminadas | 19 (notas) | OK | `gen_build_predetermined.csv` |
| CO₂ 0; 3,33; 10; 23,48; 35; 35; 35 USD/t | 28, 29 | OK | `carbon_policies.csv` |
| VOLL 650 USD/MWh | 6, 28 | OK | `lost_load_cost.csv` |
| Reserva 551/407 MW, 113 elegibles | 7, 28 | OK | `reserva_requerimiento.csv`, `reserva_elegibles.csv` |
| Base 2025, tasa 6 %, períodos 2025…2050 (2050–2054) | 28 | OK | `financials.csv`, `periods.csv` |
| Tabla MW medios por escenario y período (28 celdas) | 25 | OK | `escenarios_dc.csv` |
| Propio fija 11,5 / 69,1 / 115,2 | 25 | OK | `dc_fijo.csv` (11,52; 69,12; 115,2) |
| CEN +5 %/año desde 2031 | 10, 25 | OK | reproduce 663,5 … 1.924,2 |
| Propio +8 %/año desde 2033 sobre 2.119,7 | 10, 25, 27 | OK | reproduce 9.839,4 en 2050 |
| 3.811 MW = 1.648 + 1.363 + 800; 1.905,5 MW medios; 824 / 681,5 / 400 | 26, 27 | OK | suma de las filas |
| 428,4 × 50 % − 99 = 115,2 (93,7 + 21,5) | 27 | OK | aritmética |

## Consistencia de texto (cuerpo y notas)

- Primer año 2026 o «VP 2026»: solo quedan los dos casos de las láminas 4 (notas) y 6 marcados como ERROR. Las demás menciones de 2026 son fechas reales (solicitudes, reconversiones, rampa de N1) o explican la versión anterior (notas de la lámina 30). Están bien.
- Las inversiones de AMEBA no aparecen como existentes en ninguna lámina. Las láminas 9, 19, 22, 23, 28 y 29 dicen que no son dato.

## Avisos (no son errores numéricos)

1. **Lámina 13, «Por qué esas zonas»:** el rango de las zonas elegidas (23,0–37,9) se superpone con el de las proyectadas (37,5–38,1). En 2040, sin data centers, el norte grande (37,3–37,9) cuesta lo mismo que Alto Jahuel o Kimal (37,5), así que el argumento solo vale para el sur. Redacción sugerida: «En 2040, sin data centers, 1 MW plano cuesta 23,0–25,3 USD/MWh en el sur y 37,5–38,1 en las zonas proyectadas; el norte grande (37,3–37,9) solo lo elige el escenario propio».
2. **Lámina 15, viñeta 4, y notas de la 12:** «norte grande y sur» vale solo para el escenario propio; E2, CEN y N1 eligen únicamente Nueva Ancud. Redacción sugerida: «La ubicación óptima queda en el sur (Nueva Ancud) en los cuatro escenarios y, en el propio, también en el norte grande; fuera de la RM».
3. **Lámina 14, viñeta 1:** en Propio libre se construyen además +760 MW de gas de ciclo abierto y 2.563 MW menos de CSP. Si se quiere completo: «(en el escenario propio, además, +760 MW de gas de punta)».
4. **Lámina 14, viñeta 2:** el denominador es el MW **medio** de data centers en 2050. Por MW instalado (/0,5, como en la lámina 12) serían 2,1–2,2 y 2,5–2,6 MW. Sugerido: «Cada MW medio de data center…».
5. **Lámina 30, tabla de validación y viñeta «Réplica de AMEBA…»:** describe la versión anterior («276 térmicas × 6 años» corresponde a los 6 períodos del inicio en 2026). La nota más nueva de `40_modelo.js` lo aclara, pero el pptx no la tiene y el cuerpo no lo dice. Sugerido: agregar «(versión con inicio en 2026)» bajo la tabla o en la viñeta.
6. **Lámina 25 (notas):** «hasta 4.454 MW en 2054» supone una base de 1.381 MW. `40_escenarios_dc.py` reparte con 1.225/1.381 + 155/1.381, que suman 1.380/1.381, así que el modelo llega a 4.451 MW. Es una diferencia de 0,07 %, irrelevante. El docstring de ese script (línea 9) aún dice «plana después de 2030».
7. **Lámina 3 (notas):** el HVDC Kimal–Lo Aguirre aparece con 3.000 MW (dato real), y en el modelo con 2.000 MW (PELP; láminas 9, 23 y 24). Conviene aclarar «(2.000 MW en los datos de la PELP)».
8. **Lámina 7 (notas):** entre las obras comprometidas solo se nombra el HVDC. Falta Río Malleco–Pichirropulli (660 MW, 2030).

## Diagramación (PNG de `render_v2`)

- **Lámina 11, gráfico de barras:** el segmento de ahorro de PELP E2 (179) no tiene etiqueta visible. En CEN (772) y PELP N1 (620), la etiqueta blanca sobre gris claro desborda el segmento y casi no se lee. Corrección: etiquetas del ahorro en negro y por fuera del extremo de la barra (`dataLabelPosition: "outEnd"`, color oscuro), o quitarlas, porque la tabla de la derecha ya las da. El eje usa «2000» sin separador de miles, a diferencia del resto («1.040»). Corrección: formato `#.##0`.
- **Lámina 12, mapa:** en Propio-Proyección el círculo de Valparaíso (4.083) queda dentro del de la RM (15.596). En Propio-Óptima, Araucanía (1.499) y Los Ríos (1.240) se montan sobre Los Lagos (9.757). Las etiquetas se leen, así que es aceptable. Si se quiere mejorar, desplazar las etiquetas o usar transparencia.
- **Lámina 30:** el texto «[tiempo]» es visible (ver ERROR).
- Láminas 6, 9, 10, 13, 14, 15, 24, 25, 27, 28 y 29: sin desbordes ni solapamientos.
