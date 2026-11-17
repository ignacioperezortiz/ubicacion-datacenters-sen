# Verificación independiente: anexos de transmisión, data centers y modelo

17-nov-2026. Fuentes: `casos/SIN_DC/inputs/*.csv`, `casos/<CASO>/inputs/dc_*.csv`, `resultados/tablas/escenarios_dc.csv`, DATOS_Y_SUPUESTOS §2–8, FORMULACION, VALIDACION y el catastro (`Solicitudes CEN` y `Catastro DC`, leído con openpyxl). Los archivos de anexos no se editaron.

## 1. Transmisión (`20_transmision.js`)

| Ítem | Estado | Valor de los datos |
|---|---|---|
| 29 filas de corredores de red (15 norte + 14 centro-sur): existente, obra y ampliación máx. 2050 | OK, las 29 | `existing_trans_cap` redondeado; `max_build_mw` de 2050 (p. ej., Lagunas–Kimal 848,7 → 849 y 4.440,3 → 4.440; Cumbre–N. Cardones 2.535,6 → 2.536 y 4.054,4 → 4.054; Polpaico–A. Jahuel 2.370,1 → 2.370 y 4.009,9 → 4.010) |
| Kimal 220 – Los Changos 220: 900 MW y tope 0 | OK | `trans_new_build_allowed` = 0, sin filas de límites |
| Kimal 500 – Alto Jahuel 500: 0, 2.000 MW (2030), 6.000 | OK | 2026: 0/0; 2030: mín. = máx. = 2.000; 2050: 6.000 |
| Río Malleco – Pichirropulli: 483, 660 MW (2030), 6.160 | OK | 2030: mín. 660 y máx. 1.160 (= 500 + 660); 2050: 6.160 = 660 + 5.500 |
| 6.000 = 2.000 + 4.000 candidatos (HVDC) | OK | incrementos 1.500 + 1.500 + 1.000 |
| Existente de los 29 corredores: 41.191 MW = 38.519 + 2.672 | OK | suma: 41.191,1 MW; DATOS §6 |
| Parinas–Cumbre y N. Pan de Azúcar–Polpaico sin ampliación antes de 2035 | OK | máx. 0 en 2026 y 2030 |
| Enlaces PDGE: 5, 0 MW, tope 99.999, 1 USD/MW | OK | multiplicador 1,0; los extremos de red coinciden con el texto |
| 161 líneas → 34 corredores (29 + 5) | OK | DATOS §6 |
| Rango de costo 17.950 a 625.600 USD/MW | OK | mín. N. Pozo Almonte–Lagunas; máx. Kimal 500–A. Jahuel |
| 40 años, 6 %, factor 0,0665 | OK | 0,066462 |
| Anualidad 1.193 a 41.578 USD/MW-año | OK | 1.193,0 y 41.578,3 |
| Candidatos entran en 2026, 2035, 2040 y 2050 | OK | DATOS §6 (en AMEBA, 2025 → 2026) |
| Mínimo incremental y máximo acumulado | OK | FORMULACION, líneas 177–178 |
| Tabla de topes del HVDC: 0; 2.000 (forzada); 3.500; 5.000; 5.000; 6.000 | OK | `trans_build_limits.csv` |
| Tabla de topes típicos: 500; 500; 2.000; 3.500; 3.500; 4.500 | OK | |
| «Típico: 15 de los 28 corredores de red ampliables» | OK | 15 corredores con ese patrón exacto; 28 de 29 con `new_build_allowed` = 1 |
| HVDC: 2.000 MW, enero de 2029, entra en 2030; terminal en Alto Jahuel 500 | OK | DATOS §6 |
| Anualidad de la red existente cobrada y constante | OK | DATOS §6 |
| «Solo se amplían los 34 corredores del modelo (29 de red y 5 enlaces PDGE)» | ERROR (menor) | Se pueden ampliar 33: Kimal 220 – Los Changos 220 no tiene candidatos (lo dicen la lámina norte y la nota «28 corredores de red ampliables») |
| Transporte: más flujo norte–centro que un flujo DC (PELP 2028–2032) | OK | DATOS §9 (20–40 %) |

## 2. Data centers (`30_data_centers.js`)

| Ítem | Estado | Valor de los datos |
|---|---|---|
| Trayectoria E2: 74,2; 224,8; 272,8; 292,4; 311,9; 331,5 | OK | 74,25; 224,8; 272,818; 292,364; 311,909; 331,455. Observación: 74,25 se redondeó hacia abajo (como en DATOS §8.2) y 261,75 hacia arriba; con redondeo convencional sería 74,3. No se cambia, porque coincide con el documento |
| Trayectoria N1: 261,8; 749,8; 1.022,8; 1.042,4; 1.061,9; 1.081,5 | OK | `escenarios_dc.csv` |
| Trayectoria CEN: 330,4 y 591,0 | OK | 330,439 = 50 % × 859,5 × 1.380/1.381 − 99; 591 = 690 − 99 |
| Trayectoria Propio: 355,1; 1.899,2; 2.020,7 | OK | |
| Propio, fija: 57,6 y 115,2 | OK | 10,7563 + 46,8437; 21,5126 + 93,6874 |
| Nodos → zonas: El Salto → Polpaico 500 (85 %), Torquemada → Quillota 500, Kimal 220 kV → Kimal 220 | OK | DATOS §8.3; `dc_base` |
| CEN: RM → Polpaico 500, Valparaíso → Quillota 500 | OK | 528,35 = 612,5 − 84,15; 62,65 = 77,5 − 14,85 |
| «14 S/E» en Propio | OK | 8 S/E en Polpaico + 5 en Alto Jahuel + 1 (La Pólvora); Cirion entra por distribución |
| Trayectoria PELP: 99, 297, 364 y 450 (2057), 85/15; N1 +75 por año hasta 750 en 2035 | OK | DATOS §8.3; promedios por período 187,5, 525 y 750 en `dc_base` |
| CEN: 552, 642, 963, 1.281 y 1.381; reparto 1.225 / 155 | OK | DATOS §8.4 |
| «Se descuentan los ~99 MW medios existentes: 84,15 en Polpaico 500 y 14,85 en Quillota 500» (nota, a continuación de «Propio») | ERROR (menor) | Vale para E2, N1 y CEN. En Propio, `dc_base` = 50 % de lo solicitado sin descuento (824/681,5/400), y los 99 se restan en el llenado (214,2 − 99) |
| Tabla de campus: 16 campus, nombre, S/E con kV, zona, MW, estado y fecha | OK, las 16 filas | Catastro: Scala 2216/2847 (12 + 12, en construcción/autorizada, mar-2026/may-2027); ACS 2856 (14, Chacabuco 23 kV, jul-2028, en tramitación) y 2855 (40, Punta Verde 110 kV, jul-2029, detenida); SCL4 2719 (150, 110 kV, dic-2028); Chicureo 2850 (200, dic-2028); Hermes 3119 (100, dic-2029); SC1 2426 (300, detenida, mar-2029); SC2 3088 (500, jul-2030); Santa Teresa 2879 (300, 220 kV, autorizada, oct-2032); Rivera 3005 (200, sep-2028); Odata 2823 (48, 110 kV, autorizada, mar-2029); Noviciado 3065 (500, nov-2030); Lader 3096 + 3131 (500 + 25, Lo Aguirre 500 / Lo Prado 44 kV, ene-2031); Moreras 3165 (90, may-2031); FR Data 2377 + 2378 (200 + 100, 220 kV, paños J15 y J18, abr-2028); Pacífico 3103 (500, 220 kV, nov-2030) |
| Totales 1.648 (Polpaico), 1.363 (A. Jahuel), 800 (Quillota), 3.811 | OK | |
| 1.905,5 MW medios = 824 / 681,5 / 400 | OK | `dc_base` desde 2035 |
| 115,2 = 428,4 × 0,5 − 99 = 93,7 / 21,5 | OK | Existentes del catastro: 348,4 MW en zona Polpaico (Nueva Lampa, Colina, Chacabuco) y 80 en Alto Jahuel (Padre Hurtado, Panamericana); 348,4/428,4 × 115,2 = 93,69 |
| Rampa del 20 % por año → 57,6 en 2026–2029 | OK | |
| Exclusiones: 12 conectadas hasta 2025 (428,4 MW), 2 repetidas (14 MW), 2 sin MW | OK | Catastro: 12 solicitudes hasta dic-2025 suman 428,4 MW; repetidas 2853 (14) y 2718 (SCL4 detenida, sin MW); sin MW 2711 y 2740 |
| 35 solicitudes, 4.233,4 MW al 13-nov-2026 | OK | 37 vigentes / 4.250 MW, menos 2 sin fecha (1223, 1224: 16,6 MW) |
| 19 solicitudes nuevas | OK | 10 + 6 + 3 |
| 297,5 (2026–2029) y 1.784 (2030–2034) | OK | (16 + 22 + 454 + 698)/4; (1.448 + 1.755,5 + 3 × 1.905,5)/5 |
| 2.896 MW solicitados en 2030 frente a 1.381 del CEN | OK | |
| Lo Aguirre → Alto Jahuel por el terminal del HVDC; Ignis y SC1/SC2 como dos campus | OK | DATOS §8.5 |
| Subtítulo 1/2: «Campus con solicitud de conexión vigente» | Observación | Incluye SAN2, que no tiene solicitud; la fila y la viñeta lo aclaran |

## 3. Modelo (`40_modelo.js`): muestra de cifras

| Ítem | Estado | Fuente |
|---|---|---|
| Demanda × 1,031 | OK | DATOS §3 |
| Reserva de 551/407 MW = 331 + 220 / 85 + 322; 104 proyectos | OK | DATOS §7 |
| CO₂: 2,5; 10; 23,48; 35; 35; 35; 15,8 y 31,1 | OK | DATOS §7 |
| 3,84 h | OK | DATOS §5.2 |
| VOLL de 650 USD/MWh | OK | DATOS §7 |
| 6 días; 63 GB; 110 min; 144 h | OK | DATOS §2 |
| Efecto de 6 días: −0,04 a −0,09 %; +4,9/+4,6/+6,6/−1,8 %; FP −5,3 % | OK | DATOS §2 |
| Servicios auxiliares de 2,0 a 2,6 % | OK | DATOS §4 |
| 3.000 FV, 1.000 eólica, 92,1 BESS, 2.672 de transmisión; 2.000 MW «ley» | OK | DATOS §4 |
| Clases de recurso: 7,5 % → ±1 %; Cerro Dominador, 110 MW | OK | DATOS §4.2–4.3 |
| 17 de 38 tramos con reactancia por omisión | OK | VALIDACION, línea 51 |
| Tabla de validación: 0,000 %; 498 celdas; 343 / 1.880; 276 × 6, 0,0006; transmisión y almacenamiento, 0,0 %; hidro, 0,00 % | OK | VALIDACION, líneas 72–79 |
| Réplica: FV −15 % y eólica +4 % (2030), ±3 % (2050); transmisión −2 % / +8 %; emisiones 8–34 %; CMg 2–8 | OK | VALIDACION, líneas 156–160 |
| 25 casos y 63 de 63; 12 de 12 ecuaciones (Clases 4, 5, 8, 12 y 13) | OK | VALIDACION, líneas 14 y 36 |
| Clase 8: 7.086 / 1.918 / 2.165 / 0; 109,20; 27,52; 12,56; 4 variantes (D con ENS a 1.000) | OK | FORMULACION, líneas 333–352 |
| 1,35 M restricciones, 1,18 M variables, 6,9 M coeficientes; 5 o 6 hilos; 8–16 min | OK | FORMULACION, línea 407 |
| 2,68 M restricciones con 12 días | OK | DATOS §2 |
| Lista «No validado todavía» | OK | VALIDACION, líneas 198–200 |

## Errores para corregir

1. `20_transmision.js`, lámina «ampliación», primera viñeta. Reemplazar `"Solo se amplían los 34 corredores del modelo (29 de red y 5 enlaces PDGE); no se crean corredores entre otras zonas"` por `"Solo se amplían corredores existentes: 28 de los 29 de red y los 5 enlaces PDGE; no se crean corredores entre otras zonas"`.
2. `30_data_centers.js`, notas de la lámina de escenarios. Reemplazar `"Se descuentan los ~99 MW medios existentes: 84,15 en Polpaico 500 y 14,85 en Quillota 500."` por `"En E2, N1 y CEN se descuentan los ~99 MW medios existentes: 84,15 en Polpaico 500 y 14,85 en Quillota 500; en Propio se descuentan del llenado (214,2 − 99)."`.
