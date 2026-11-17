# Datos para gráficos de motivación (verificación independiente B, 17-nov-2026)

Extracción con PyMuPDF (texto y etiquetas vectoriales). Páginas = índice del PDF (1-based); en IEA coincide con el folio impreso; en LBNL el folio impreso es PDF − 1.

## 1. Mundo — IEA (2025), *Energy and AI* (`mundo_iea_twh.csv`)

| Año | Caso | TWh | Pág. | Cita |
|---|---|---|---|---|
| 2020 | histórico | 269 | 258 | Tabla A.1 «Electricity consumption (TWh) Total 269 361 416 946 1 193» |
| 2023 | histórico | 361 | 258 | ídem (p. 71: «Consuming around 360 TWh of electricity in 2023») |
| 2024 | histórico | 416 | 258 | ídem; p. 49: «around 415 terawatt hours (TWh), or about 1.5% of global electricity consumption in 2024» |
| 2030 | Base | 946 | 258 | ídem; p. 49: «electricity consumption from data centres rises to around 945 TWh by 2030» |
| 2035 | Base | 1 193 | 258 | ídem; p. 14: «Base Case sees global data centre electricity consumption rising to around 1 200 TWh by 2035» |
| 2030 / 2035 | Lift-Off | 1 264 / 1 719 | 258 | Tabla A.1; p. 49: «consumption reaches over 1 260 TWh by 2030» |
| 2030 / 2035 | High Efficiency | 792 / 972 | 258 | Tabla A.1; p. 49: «consumption reaches around 800 TWh by 2030» |
| 2030 / 2035 | Headwinds | 669 / 707 | 258 | Tabla A.1; p. 49: «In the Headwinds Case, it reaches around 670 TWh» |
| 2035 | rango | 700–1 720 | 49 | «By 2035, the spread of uncertainty widens further, spanning 700 TWh to 1 720 TWh» (p. 15 dice «700 to 1 700 TWh») |

Otros: EE. UU. 2020/2023/2024/2030 = 108/154/183/426 TWh (Tabla A.4, p. 260); crecimiento ~12 %/año desde 2017 (p. 14); ~3 % del consumo mundial en 2030 (p. 63). Las Figuras 2.11 (p. 64) y 2.14 (p. 67) son vectoriales pero solo traen ejes, sin rótulos de datos.

## 2. Estados Unidos — Shehabi et al. (2024), LBNL (`eeuu_lbnl_twh.csv`)

| Año | TWh | % consumo EE. UU. | Pág. PDF | Cita |
|---|---|---|---|---|
| 2014–2016 | ~60 | — | 7, 52 | «annual energy use remained stable between 2014–2016 at about 60 TWh» |
| 2018 | ~76 | 1,9 % | 7, 52 | «by 2018 data centers consumed about 76 TWh, representing 1.9%» |
| 2023 | 176 | 4,4 % | 8, 52 | «reaching 176 TWh by 2023, representing 4.4% of total U.S. electricity consumption» |
| 2028 | 325–580 | 6,7–12,0 % | 8, 52 | «low and high end of roughly 325 and 580 TWh in 2028» |

Notas: p. 58 dice «approximately 178 TWh in 2023» (inconsistencia interna con 176). 2028 equivale a 74–132 GW con 50 % de utilización (p. 8). **No disponibles como texto:** 2017, 2019–2022 y el rango 2024; la Figura ES-1 (p. 7) y la Figura 5.5 (p. 52) son imágenes raster.

## 3. Chile — CEN (2026b), Reporte anual de desempeño 2025

### (a) Reducciones ERV 2025 por mes (`chile_reducciones_erv_mensual_gwh.csv`), p. 16, Figura 13

Cita del total: «alcanzando un total acumulado anual de 6.084 GWh» (p. 16; también p. 6).
Rótulos vectoriales de la Figura 13; la asignación de serie se verificó por color (verde = Eólica, naranja = Solar, igual a los marcadores de la leyenda).

| Mes | Eólica | Solar | Total |
|---|---|---|---|
| ene | 148 | 505 | 653 |
| feb | 102 | 300 | 402 |
| mar | 125 | 430 | 555 |
| abr | 66 | 271 | 337 |
| may | 57 | 132 | 189 |
| jun | 69 | 218 | 287 |
| jul | 50 | 170 | 220 |
| ago | 166 | 328 | 494 |
| sept | 173 | 426 | 599 |
| oct | 211 | 520 | 731 |
| nov | 251 | 554 | 805 |
| dic | 215 | 599 | 814 |
| **Año** | **1 633** | **4 453** | **6 086** (texto: 6.084; diferencia por redondeo) |

**No disponible:** desglose por zona o región (el texto solo dice congestiones «de la zona norte y sur»).

### (b) Tabla 4, horas de congestión 2025 (`chile_tabla4_congestion_horas.csv`), p. 17

Cita: «Tabla 4: Líneas de transmisión con eventos de congestión durante el año 2025.» La tabla tiene exactamente 6 filas:

| Línea | Eventos | Horas |
|---|---|---|
| El Peñón 110 → La Ruca 110 | 338 | 2.771 |
| Lastarria 220 → Ciruelos 220 | 290 | 1.797 |
| Polpaico 500 → Nueva Pan de Azúcar 500 | 319 | 1.305 |
| Kimal 220 → María Elena 220 | 143 | 1.057 |
| Charrúa 154 → Los Ángeles 154 | 169 | 710 |
| Charrúa 220 → Santa Clara 220 | 152 | 587 |

### (c) CMg mensual 2025 (Figuras 7–10, p. 11)

**No impreso como texto.** Las Figuras 7 (Crucero 220 kV, norte) y 9 (Quillota 220 kV, centro) solo traen como rótulo la **variación % respecto del mismo mes de 2024** y los ejes (Crucero 0–140; Quillota 0–120 USD/MWh). Esas variaciones están en `chile_cmg_var_pct_vs_2024.csv`. Ojo: en Crucero, sept/oct/nov salen en una sola línea («77,4% 71,4% 65,3%»), así que el orden se asumió de izquierda a derecha. Los valores absolutos en USD/MWh habría que medirlos en la geometría del gráfico o pedirlos al CEN (por ejemplo, la base de costos marginales reales).
