# Verificación de los anexos de transmisión y data centers

Generado el 17-11-2026 por `anexos_tx_dc.py` (`python -P`, inputs del modelo con inicio en 2025), que calcula todas las cifras y escribe `20_transmision.js` y `30_data_centers.js`. Cada cifra de las láminas sale de las filas de abajo.

## Datos de entrada

- Inputs del modelo (inicio 2025): `casos`
  - `SIN_DC/inputs/transmission_lines.csv`, `trans_build_limits.csv`, `trans_params.csv`, `financials.csv`, `periods.csv` (los de transmisión son idénticos en los 5 casos, comprobado por hash);
  - `<CASO>/inputs/dc_base.csv`, `dc_fijo.csv`, `dc_libre.csv` para PELP_E2, PELP_N1, CEN y PROPIO;
  - `presentacion/fuente/datos/resumen_escenarios_dc.csv` (resumen del script de escenarios, copia del modelo);
  - `presentacion/fuente/datos/inversion_ameba_hasta_2025.csv` y, solo para documentar el cambio, `presentacion/fuente/datos/transmission_lines_antes_inicio_2025.csv` (copias del modelo);
  - reglas: `CAMBIO_INICIO_2025.md` del modelo, `DATOS_Y_SUPUESTOS.md` (secciones 6 y 8) del repositorio.
- Repositorio: las rutas de esta lista son relativas a su raíz.
- Catastro del equipo: filas ya extraídas en `presentacion/fuente/datos/campus_escenario_propio.csv` (el catastro privado no estaba disponible).
- Solo para verificar el origen de la capacidad existente: `presentacion/fuente/datos/lineas_ameba_a_corredores.csv` (trazabilidad de las 161 líneas AMEBA).

## Comprobaciones automáticas

El script se detiene si falla alguna. Todas pasaron:

- transmission_lines.csv de PELP_E2 es idéntico al de SIN_DC
- trans_build_limits.csv de PELP_E2 es idéntico al de SIN_DC
- trans_params.csv de PELP_E2 es idéntico al de SIN_DC
- transmission_lines.csv de PELP_N1 es idéntico al de SIN_DC
- trans_build_limits.csv de PELP_N1 es idéntico al de SIN_DC
- trans_params.csv de PELP_N1 es idéntico al de SIN_DC
- transmission_lines.csv de CEN es idéntico al de SIN_DC
- trans_build_limits.csv de CEN es idéntico al de SIN_DC
- trans_params.csv de CEN es idéntico al de SIN_DC
- transmission_lines.csv de PROPIO es idéntico al de SIN_DC
- trans_build_limits.csv de PROPIO es idéntico al de SIN_DC
- trans_params.csv de PROPIO es idéntico al de SIN_DC
- 34 corredores: 29 de red y 5 enlaces PDGE
- las dos láminas cubren los 29 corredores de red, sin repetir
- trans_build_limits solo nombra corredores de transmission_lines (no hay corredores nuevos)
- el único corredor sin filas de ampliación es Kimal220_LosChangos220
- Kimal220_LosChangos220 tiene trans_new_build_allowed = 0
- 231 filas: 33 corredores ampliables × 7 períodos
- el tope acumulado es no decreciente en todos los corredores
- obras comprometidas: Kimal500_AltoJahuel500 2.000 MW y RioMalleco500_Pichirropulli500 660 MW, ambas en 2030
- de los 29 corredores de red, solo Kimal500_AltoJahuel500 parte con 0 MW
- Kimal500_AltoJahuel500 no puede construirse en 2025 ni en 2027 (tope 0)
- los 5 enlaces PDGE parten en 0 MW con tope 99.999 MW en todos los períodos
- costo de los enlaces PDGE: 1 USD/MW
- eficiencia 1 (sin pérdidas) en los 34 corredores
- costo por MW = trans_terrain_multiplier (largo 1 km y 1 USD/MW-km)
- 28 corredores de red ampliables
- patrón de tope más frecuente: (500.0, 500.0, 500.0, 2000.0, 3500.0, 3500.0, 4500.0) en 19 corredores
- costo por MW entre 17.950 y 625.600 USD/MW
- vida 40 años, tasa 6 %, sin O&M
- factor de anualidad FRC(6 %, 40) = 0.066462
- todos los corredores ampliables (salvo el HVDC) pueden ampliarse desde 2025
- ningún corredor ampliable de red (salvo el HVDC) tiene tope 0 en 2025
- polos PDGE: ANF-B1, ANF-B2, ANF-B3, TOC-A1, TOC-A2
- PELP_E2: suma de dc_base = dc_libre en los 7 períodos y dc_libre + dc_fijo = resumen de escenarios
- PELP_N1: suma de dc_base = dc_libre en los 7 períodos y dc_libre + dc_fijo = resumen de escenarios
- CEN: suma de dc_base = dc_libre en los 7 períodos y dc_libre + dc_fijo = resumen de escenarios
- PROPIO: suma de dc_base = dc_libre en los 7 períodos
- E2, N1 y CEN reconstruidos desde las trayectorias anuales (promedio por período − 99), con CEN +3 %/año desde 2031
- E2: 0 en 2025 (sin crecimiento sobre los 99 existentes); 85 % Polpaico500 y 15 % Quillota500 desde 2027
- N1 = E2 + Kimal220 (37,5 / 225 / 525 / 750 MW medios)
- CEN por zona: Polpaico500 = capacidad × 1.225/1.381 × 50 % − 84,15 y Quillota500 = × 155/1.381 × 50 % − 14,85
- 35 solicitudes vigentes con fecha = 4.233,4 MW, igual a la hoja Cronograma MW
- regla 1: 12 solicitudes existentes, 428,4 MW
- regla 2: repetidas [2718, 2853] (ACS Santiago I alim. 2, 14 MW; Ascenty SCL4 detenida, sin MW)
- 2 vigentes sin MW informado (2711 y 2740), fuera
- 19 solicitudes nuevas incluidas, 3.791 MW
- existentes + repetidas + sin MW + incluidas = 4.233,4 MW del cronograma
- la clase de cada fila de campus_escenario_propio.csv coincide con la que dan las reglas 1 y 2
- 15 campus (grupos del catastro) con solicitudes incluidas
- 16 campus, 3.811 MW solicitados
- por zona: Polpaico500 1.648, AltoJahuel500 1.363, Quillota500 800 MW solicitados (tabla de la sección 8.5)
- 14 subestaciones de conexión distintas (sin contar la conexión en distribución de Cirion)
- MW medios acumulados 2025–2032: 0, 16, 22, 454, 698, 1.448, 1.755,5, 1.905,5 (tabla de la sección 8.5)
- base del crecimiento: 99 + 115,2 + 1.905,5 = 2.119,7 MW medios en 2032
- promedio por período de la trayectoria anual (con +3 %/año desde 2033) = dc_libre de PROPIO, a 2·10⁻³ MW
- reparto por zona y período = dc_base de PROPIO (el aumento desde 2033 se reparte como lo solicitado en 2032)
- existentes: 348,4 MW en Lampa/Colina/Quilicura y 80 en San Bernardo/Padre Hurtado
- llenado 115,2 MW medios = 93,69 Polpaico500 + 21,51 AltoJahuel500 (dc_fijo 2030)
- rampa 20 %/año desde 2026: promedio 2025–2026 = 11,52 y 2027–2029 = 69,12 MW medios; 115,2 desde 2030
- 2.896 MW solicitados al 2030 (= 2 × 1.448)
- 428,4 × 50 % = 214,2 MW medios

## Cifras y su origen

| Sección | Cifra | Cómo se obtuvo |
|---|---|---|
| Transmisión | 38.519 MW existentes en los 29 corredores de red | suma de `existing_trans_cap` de `transmission_lines.csv` sin los 5 enlaces PDGE |
| Transmisión | 38.519 MW existentes en los 29 corredores de red | `existing_trans_cap` de las entradas; lo que AMEBA construyó hasta 2025 (2.672,1 MW en 7 corredores) no es dato |
| Transmisión | tope típico 500/500/500/2.000/3.500/3.500/4.500 MW en 19 de 28 corredores | patrón más frecuente de `max_build_mw` por período en `trans_build_limits.csv`: Ancoa500_NuevaCharrua500, Candelaria500_AltoJahuel500, Concepcion500_NuevaCharrua500, Cumbre500_NuevaCardones500, Kimal220_NuevaZaldivar220, Kimal500_LosChangos500, Lagunas220_Kimal220, LosChangos220_NuevaZaldivar220, LosChangos500_Parinas500, NuevaPozoAlmonte220_Lagunas220, NuevaPozoAlmonte220_Parinacota220, NuevaPuertoMontt500_NuevaAncud500, Parinas500_Cumbre500, Parinas500_NuevaZaldivar220, Pichirropulli500_NuevaPuertoMontt500, Polpaico500_AltoJahuel500, Quillota500_Polpaico500, Rapel500_AltoJahuel500, RioMalleco500_Mulchen500 |
| Transmisión | 17.950 a 625.600 USD/MW; FRC = 0.0665 | mín. y máx. de `trans_terrain_multiplier` (× largo 1 km × 1 USD/MW-km) en los 28 corredores ampliables; FRC = i / (1 − (1 + i)^−40) con i = 6 % de `financials.csv` y vida de `trans_params.csv` |
| Transmisión | anualidad 1.193 a 41.578 USD/MW-año | costo × FRC (solo notas) |
| Transmisión (tabla) | Alto Jahuel 500 – Ancoa 500: existente 4.000; obra —; ampliación máx. 2050 6.000 | `AltoJahuel500_Ancoa500`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Ancoa 500 – Nueva Charrúa 500: existente 3.000; obra —; ampliación máx. 2050 4.500 | `Ancoa500_NuevaCharrua500`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Candelaria 500 – Alto Jahuel 500: existente 680; obra —; ampliación máx. 2050 4.500 | `Candelaria500_AltoJahuel500`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Concepción 500 – Nueva Charrúa 500: existente 260; obra —; ampliación máx. 2050 4.500 | `Concepcion500_NuevaCharrua500`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Cumbre 500 – Nueva Cardones 500: existente 2.090; obra —; ampliación máx. 2050 4.500 | `Cumbre500_NuevaCardones500`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Kimal 220 – Los Changos 220: existente 900; obra —; ampliación máx. 2050 0 | `Kimal220_LosChangos220`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Kimal 220 – Nueva Zaldívar 220: existente 815; obra —; ampliación máx. 2050 4.500 | `Kimal220_NuevaZaldivar220`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Kimal 500 – Alto Jahuel 500: existente 0; obra 2.000 MW (2030); ampliación máx. 2050 6.000 | `Kimal500_AltoJahuel500`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Kimal 500 – Kimal 220: existente 1.500; obra —; ampliación máx. 2050 5.300 | `Kimal500_Kimal220`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Kimal 500 – Los Changos 500: existente 1.590; obra —; ampliación máx. 2050 4.500 | `Kimal500_LosChangos500`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Lagunas 220 – Kimal 220: existente 789; obra —; ampliación máx. 2050 4.500 | `Lagunas220_Kimal220`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Los Changos 220 – Nueva Zaldívar 220: existente 525; obra —; ampliación máx. 2050 4.500 | `LosChangos220_NuevaZaldivar220`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Los Changos 500 – Los Changos 220: existente 1.500; obra —; ampliación máx. 2050 4.300 | `LosChangos500_LosChangos220`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Los Changos 500 – Parinas 500: existente 1.500; obra —; ampliación máx. 2050 4.500 | `LosChangos500_Parinas500`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Nueva Cardones 500 – Nueva Maitencillo 500: existente 2.368; obra —; ampliación máx. 2050 5.500 | `NuevaCardones500_NuevaMaitencillo500`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Nueva Charrúa 500 – Mulchén 500: existente 1.540; obra —; ampliación máx. 2050 6.000 | `NuevaCharrua500_Mulchen500`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Nueva Maitencillo 500 – Nueva Pan de Azúcar 500: existente 2.375; obra —; ampliación máx. 2050 5.500 | `NuevaMaitencillo500_NuevaPandeAzucar500`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Nueva Pan de Azúcar 500 – Polpaico 500: existente 2.500; obra —; ampliación máx. 2050 5.500 | `NuevaPandeAzucar500_Polpaico500`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Nueva Pozo Almonte 220 – Lagunas 220: existente 662; obra —; ampliación máx. 2050 4.500 | `NuevaPozoAlmonte220_Lagunas220`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Nueva Pozo Almonte 220 – Parinacota 220: existente 450; obra —; ampliación máx. 2050 4.500 | `NuevaPozoAlmonte220_Parinacota220`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Nueva Puerto Montt 500 – Nueva Ancud 500: existente 660; obra —; ampliación máx. 2050 4.500 | `NuevaPuertoMontt500_NuevaAncud500`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Parinas 500 – Cumbre 500: existente 1.500; obra —; ampliación máx. 2050 4.500 | `Parinas500_Cumbre500`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Parinas 500 – Nueva Zaldívar 220: existente 660; obra —; ampliación máx. 2050 4.500 | `Parinas500_NuevaZaldivar220`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Pichirropulli 500 – Nueva Puerto Montt 500: existente 805; obra —; ampliación máx. 2050 4.500 | `Pichirropulli500_NuevaPuertoMontt500`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Polpaico 500 – Alto Jahuel 500: existente 1.880; obra —; ampliación máx. 2050 4.500 | `Polpaico500_AltoJahuel500`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Quillota 500 – Polpaico 500: existente 1.803; obra —; ampliación máx. 2050 4.500 | `Quillota500_Polpaico500`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Rapel 500 – Alto Jahuel 500: existente 394; obra —; ampliación máx. 2050 4.500 | `Rapel500_AltoJahuel500`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Río Malleco 500 – Mulchén 500: existente 1.290; obra —; ampliación máx. 2050 4.500 | `RioMalleco500_Mulchen500`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión (tabla) | Río Malleco 500 – Pichirropulli 500: existente 483; obra 660 MW (2030); ampliación máx. 2050 6.160 | `RioMalleco500_Pichirropulli500`: `existing_trans_cap`; filas con `min_build_mw` > 0; `max_build_mw` de 2050 (0 si no tiene filas). Redondeo a MW |
| Transmisión | 20–40 % más flujo norte–centro con transporte (solo notas) | DATOS_Y_SUPUESTOS §9, Limitaciones |
| Transmisión | Kimal 500 – Alto Jahuel 500 nace con el HVDC en 2030 | `existing_trans_cap` = 0 y `max_build_mw` = 0 en 2025 y 2027; `min_build_mw` = `max_build_mw` = 2.000 en 2030 |
| Transmisión | «Típico» de la tabla de ejemplo | patrón más frecuente de `max_build_mw` (ver arriba) |
| Transmisión | HVDC: tope acumulado 0 / 0 / 2.000 / 3.500 / 5.000 / 5.000 / 6.000 MW; mínimo 2.000 en 2030 | `trans_build_limits.csv`, filas de `Kimal500_AltoJahuel500` |
| Data centers | PELP_E2: 0,0 / 99,0 / 224,8 / 272,8 / 292,4 / 311,9 / 331,5 MW medios | por período: `dc_libre_mw` + suma de `dc_fijo_mw` de las zonas (inputs nuevos); igual a la suma de `dc_base_mw` + fija; igual a `agregado_al_modelo_mw` de `resumen_escenarios_dc.csv` |
| Data centers | PELP_N1: 37,5 / 324,0 / 749,8 / 1.022,8 / 1.042,4 / 1.061,9 / 1.081,5 MW medios | por período: `dc_libre_mw` + suma de `dc_fijo_mw` de las zonas (inputs nuevos); igual a la suma de `dc_base_mw` + fija; igual a `agregado_al_modelo_mw` de `resumen_escenarios_dc.csv` |
| Data centers | CEN: 138,3 / 381,7 / 633,7 / 750,4 / 885,6 / 1.042,5 / 1.224,3 MW medios | por período: `dc_libre_mw` + suma de `dc_fijo_mw` de las zonas (inputs nuevos); igual a la suma de `dc_base_mw` + fija; igual a `agregado_al_modelo_mw` de `resumen_escenarios_dc.csv` |
| Data centers | PROPIO: 19,5 / 460,5 / 1.937,7 / 2.360,5 / 2.752,2 / 3.206,3 / 3.732,8 MW medios | por período: `dc_libre_mw` + suma de `dc_fijo_mw` de las zonas (inputs nuevos); igual a la suma de `dc_base_mw` + fija |
| Data centers | Propio, fija: 11,5 / 69,1 / 115,2 / 115,2 / 115,2 / 115,2 / 115,2 | suma de `dc_fijo_mw` de PROPIO por período |
| Data centers | reconstrucción de E2, N1 y CEN | E2: RM+Valparaíso 99 (2025 y 2026), 297 (2030), 364 (2035), 450 (2057) MW medios con interpolación lineal; promedio de los años del período − 99. N1: E2 + 75 MW medios por año desde 2026 hasta 750. CEN: 398, 552, 642, 963, 1.281 y 1.381 MW de capacidad en 2025–2030 y 1.381 × 1,03^(año − 2030) desde 2031 (`CRECIMIENTO_CEN` del script de escenarios), × 50 % × 1.380/1.381 (reparto RM 1.225 + Valparaíso 155), − 99. Coinciden con `dc_libre.csv` a 10⁻³ MW |
| Data centers | E2 85 % / 15 %; N1 + Kimal 220; CEN RM 1.225 MW y Valparaíso 155 MW (al 2030) | cocientes de `dc_base_mw` por zona; CEN: promedio de capacidad × 1.225/1.381 (o 155/1.381) × 0,5, − 84,15 (o − 14,85) |
| Propio | 4.233,4 MW = 428,4 existentes + 14 repetidos + 0 sin MW + 3.791 incluidos | hoja «Solicitudes CEN» del catastro, Vigente = «Sí» y con fecha estimada (35 solicitudes, igual a la fila Total de «Cronograma MW»); regla 1: año ≤ 2025; regla 2: mismo grupo, misma S/E, misma fecha y misma potencia o sin MW (IDs 2853 y 2718; DC Valparaíso 1 y 2 tienen 200 y 100 MW: dos edificios); sin MW: IDs 2711 y 2740 |
| Propio (tabla) | Estado y fecha estimada de cada campus | columnas «Categoría estado» (En tramitación, Detenida, Autorizada (por declarar en construcción) → autorizada, Declarada en construcción → en construcción) y «Fecha estimada de conexión» de cada solicitud incluida; S/E y tensión desde «Subestación de conexión» y «Tensión (kV)»; zona según la tabla de ubicación de §8.5 |
| Propio (tabla) | Quilicura, dos alimentadores (Scala): 24 MW, Polpaico500 | CEN 2216 «Nuevo Alimentador 23 kV Scala en S/E Chacabuco», Chacabuco 23 kV, 12 MW, 31-03-2026, en construcción; CEN 2847 «Nuevo Alimentador 23 kV Scala2 en S/E Quilicura», Quilicura 23 kV, 12 MW, 31-05-2027, autorizada |
| Propio (tabla) | DC Valparaíso 1 y 2 (FR Data): 300 MW, Quillota500 | CEN 2377 «DC Valparaiso 1», La Pólvora 220 kV, 200 MW, 01-04-2028, en tramitación; CEN 2378 «DC Valparaiso 2», La Pólvora 220 kV, 100 MW, 01-04-2028, en tramitación |
| Propio (tabla) | DC Santiago I y II (ACS): 54 MW, Polpaico500 | CEN 2856 «ACS DC SANTIAGO I Alimentador No.1», Chacabuco 23 kV, 14 MW, 31-07-2028, en tramitación; CEN 2855 «ACS DC SANTIAGO II», Punta Verde 110 kV, 40 MW, 31-07-2029, detenida |
| Propio (tabla) | Proyecto Rivera (Inmobiliaria STPA): 200 MW, AltoJahuel500 | CEN 3005 «Proyecto Rivera», Bajos de Mena 110 kV, 200 MW, 30-09-2028, en tramitación |
| Propio (tabla) | SCL4 (Ascenty): 150 MW, Polpaico500 | CEN 2719 «Data Center Santiago Chile 4 (SCL4)», Punta Verde 110 kV, 150 MW, 04-12-2028, en tramitación |
| Propio (tabla) | Campus Norte, etapa II (Eléc. Chicureo): 200 MW, Polpaico500 | CEN 2850 «Datacenter Campus Norte Etapa II», Chicureo 220 kV, 200 MW, 31-12-2028, en tramitación |
| Propio (tabla) | SC1 (SAE Ladera Sur): 300 MW, Polpaico500 | CEN 2426 «Data Center SC1 (exBESS Ladera Sur 1)», Manuel Rodríguez 220 kV, 300 MW, 30-03-2029, detenida |
| Propio (tabla) | San Bernardo, ampliación (ODATA): 48 MW, AltoJahuel500 | CEN 2823 «Odata San Bernardo Expansión», Odata San Bernardo 110 kV, 48 MW, 30-03-2029, autorizada |
| Propio (tabla) | DC Hermes (Mytilineos): 100 MW, Polpaico500 | CEN 3119 «DC Hermes», Nueva Lampa 220 kV, 100 MW, 31-12-2029, en tramitación |
| Propio (tabla) | SC2 (RTB Energy): 500 MW, Polpaico500 | CEN 3088 «Data Center SC2», Polpaico 500 kV, 500 MW, 01-07-2030, en tramitación |
| Propio (tabla) | Noviciado I (Ignis): 500 MW, AltoJahuel500 | CEN 3065 «Data Center Noviciado I», Lo Aguirre 500 kV, 500 MW, 01-11-2030, en tramitación |
| Propio (tabla) | Pacífico 33-S (Ignis): 500 MW, Quillota500 | CEN 3103 «DATACENTER PACÍFICO 33-S», La Pólvora 220 kV, 500 MW, 29-11-2030, en tramitación |
| Propio (tabla) | Lo Aguirre y Lo Aguirre A (Lader Energy): 525 MW, AltoJahuel500 | CEN 3096 «Data Center Lo Aguirre», Lo Aguirre 500 kV, 500 MW, 31-01-2031, en tramitación; CEN 3131 «Data Center Lo Aguirre A», Lo Prado 44 kV, 25 MW, 31-01-2031, en tramitación |
| Propio (tabla) | Moreras (Orion Power): 90 MW, AltoJahuel500 | CEN 3165 «Data Center Moreras», Alto Jahuel 110 kV, 90 MW, 31-05-2031, en tramitación |
| Propio (tabla) | Mega Data Center Lampa, etapa 2 (Scala): 300 MW, Polpaico500 | CEN 2879 «AMPLIACION MEGA DATA CENTER LAMPA ETAPA 2», Santa Teresa 220 kV, 300 MW, 15-10-2032, autorizada |
| Propio (tabla) | SAN2 (Cirion): 20 MW, Polpaico500 | catálogo propio; DATOS_Y_SUPUESTOS §8.5, regla 3: Quilicura, 20 MW en 2026, conexión en distribución |
| Propio | MW medios = 50 % de los MW solicitados; +3 %/año desde 2033 | carga plana desde el año de la fecha estimada (año completo); acumulado anual 0 (2025), 16 … 1.905,5 (2032); desde 2033, + 2.119,7 × (1,03^(año − 2032) − 1), repartido como lo solicitado en 2032 (`CRECIMIENTO` del script del escenario propio); promedio de los años del período = `dc_libre.csv` (8,0; 391,3; 1.822,5; 2.245,3; 2.637,0; 3.091,1; 3.617,6) y, por zona, `dc_base.csv` |
| Propio | llenado 115,2 = 428,4 × 50 % − 99; 93,7 Polpaico 500 y 21,5 Alto Jahuel 500; 11,5 en 2025–2026 y 69,1 en 2027–2029 | MW de las 12 existentes por comuna (Lampa, Colina, Quilicura → Polpaico500; San Bernardo, Padre Hurtado → AltoJahuel500); rampa 0, 20, 40, 60 y 80 % en 2025–2029; coincide con `dc_fijo.csv` |

## Formato

El script comprueba en cada lámina: título ≤ 45 caracteres, subtítulo ≤ 110, anchos de columna (12,13 in o 11,68 in en total), suma de anchos de cada tabla, alto apilado ≤ 4,8 in (filas de 0,29/0,31 in a 11/12 pt, viñetas y texto con la fórmula de `build.js`) y que cada celda quepa en una línea (16/14 caracteres por pulgada a 11/12 pt, descontando 0,17 in de márgenes).

Altos calculados (in) por lámina y columna:

- Anexo: corredores de transmisión (norte): [4.64, 2.61]
- Anexo: corredores de transmisión (centro-sur): [4.35, 1.91]
- Anexo: ampliación de la transmisión: [3.4, 3.5]
- Anexo: escenarios de data centers: [4.18]
- Anexo: escenario propio, campus (1/2): [4.14]
- Anexo: escenario propio, campus (2/2): [3.93]

## Hecho sobre los corredores

El modelo solo amplía los 34 corredores de `transmission_lines.csv` (Switch indexa `BuildTx` por esos corredores y `trans_build_limits.csv` no nombra otros); no crea corredores entre otros pares de zonas. Matiz: de los 29 corredores de red, 28 tienen capacidad existente; Kimal 500 – Alto Jahuel 500 parte en 0 MW, no puede construirse en 2025 ni en 2027 y nace con la obra comprometida (HVDC, 2.000 MW en 2030), después de la cual puede ampliarse hasta 6.000 MW acumulados. Los 5 enlaces PDGE también parten en 0 MW, con tope 99.999 MW. En AMEBA, toda línea candidata o comprometida cae en uno de los 34 corredores, y el único corredor de red sin línea existente es el del HVDC. Kimal 220 – Los Changos 220 no se puede ampliar.

## Observaciones

- Las capacidades de las tablas de corredores se redondean a MW: los 29 existentes redondeados suman 38.519 MW, frente al total exacto de 38.519 MW que se da en el texto.
- El HVDC Kimal–Lo Aguirre figura con 2.000 MW, la capacidad que le asignan los datos de la PELP 2023–2027 y con la que corre el modelo. Las notas de la lámina de motivación del cuerpo hablan de 3.000 MW (el proyecto); no es un error del anexo, pero conviene no mezclarlas al responder.
- Campus = grupo «Proyecto / campus» del catastro (15 grupos con solicitudes incluidas) más Cirion SAN2. Cuatro campus agrupan dos solicitudes que se cuentan ambas (dos alimentadores, dos edificios o dos módulos): Quilicura (Scala), DC Santiago I y II (ACS), Lo Aguirre y Lo Aguirre A (Lader Energy) y DC Valparaíso 1 y 2 (FR Data). Las 19 solicitudes y sus MW están en la tabla de arriba.
- La regla 2 se aplicó con un criterio explícito (mismo grupo, misma S/E, misma fecha y misma potencia o sin MW), que reproduce exactamente las dos repetidas que nombra DATOS_Y_SUPUESTOS §8.5.
- Cirion SAN2 no está en el catastro: sus datos (Quilicura, 20 MW, 2026, distribución) salen de DATOS_Y_SUPUESTOS §8.5.
