# Búsqueda bibliográfica: propuesta B

Propuesta para la diapositiva de literatura de la presentación de avance (curso «Economía, Resiliencia y Mercados Energéticos», UAI, 2026-S2). Preparada el 17-nov-2026 a partir de las 58 candidatas de `02-proyecto\revision-literatura\revision-literatura-data-centers.xlsx`. Todas las cifras se verificaron en el PDF o, en un caso, en el texto completo publicado (se indica cuál). Las páginas son las impresas en el documento; entre paréntesis va la página del archivo PDF cuando no coinciden.

Siglas usadas: DC = data center (centro de datos); PELP = Planificación Energética de Largo Plazo (Ministerio de Energía); CEN = Coordinador Eléctrico Nacional; RM = Región Metropolitana; PJM = PJM Interconnection, operador del sistema de 13 estados del este de EE. UU.; HVDC = corriente continua en alta tensión; CCS = captura y almacenamiento de carbono; £ = libras esterlinas.

---

## 1. Estudios elegidos y por qué

| # | Estudio | Qué respalda de nuestro trabajo |
|---|---|---|
| 1 | Onodera, Shiraki y Matsuhashi (2026), Japón | El mismo experimento: expansión de generación, almacenamiento y transmisión con la ubicación de los DC como variable, comparada con la ubicación actual, y la misma métrica (ahorro como % del costo extra que agregan los DC). |
| 2 | Shao, Yu y Wong (2025), PJM (EE. UU.) | Ubicación de DC como decisión de primera etapa dentro de la planificación de generación, almacenamiento y transmisión de un sistema real, con revisión por pares y el ahorro del sistema eléctrico reportado aparte. |
| 3 | Newbery (2026), Gran Bretaña | Señales locacionales y costos de red: cuánto vale ubicar un DC detrás de la congestión (transmisión evitada) y por qué las señales actuales no lo inducen. Da la lectura económica de nuestro ahorro. |

Criterio: cubrir los tres frentes del encargo (planificación con ubicación endógena, modelo de capacidad con esa variable en un sistema real, señales locacionales y costo de red) con estudios sobre DC. Los análogos de electrolizadores quedaron como respaldo (sección 4) porque ninguno aísla el efecto de la ubicación de la carga mejor que estos tres.

---

## 2. Texto propuesto para la diapositiva

**Onodera et al. (2026).** *Strategic data center siting can mitigate trade-offs between decarbonization and digitalization in Japan.*
- Qué hacen: expansión del sistema eléctrico de Japón al 2050 (1.741 nodos municipales) con los DC donde están hoy, donde los ubica el modelo o con restricciones de sitio.
- Resultado: elegir la ubicación reduce entre 16,3 % y 19,7 % el costo extra que agregan los DC (11,6–14,1 % con restricciones de sitio); el modelo los lleva al norte, junto a eólica marina, geotermia y nuclear.
- Uso: mismo diseño (proyectada vs. elegida por el modelo) y misma métrica que nuestro caso base vs. libre.

**Shao, Yu y Wong (2025).** *Stochastic long-term joint decarbonization planning for power systems and data centers: A case study in PJM.*
- Qué hacen: planifican en conjunto, a 15 años, la ubicación de DC y la expansión de generación, almacenamiento y transmisión en PJM (21 zonas).
- Resultado: frente a ubicar los DC sin coordinación y planificar la red después, la inversión del sistema eléctrico baja 11,7 % y el costo de operación 8,3 %.
- Uso: respalda tratar la ubicación como variable de la planificación; nosotros excluimos la inversión de los DC y el caso base es la proyección oficial.

**Newbery (2026).** *Locating data centres efficiently in Britain – reformed transmission charging, energy subsidies or zonal pricing?*
- Qué hace: valora la ubicación de DC detrás de la frontera congestionada Escocia–Inglaterra y compara tres señales locacionales.
- Resultado: 2,2 GW de DC en Escocia evitan un enlace HVDC submarino de 2 GW, unas £15/MWh o £263 millones al año; el cargo locacional a la demanda no premia esa ubicación.
- Uso: lee nuestro ahorro como el valor de una señal locacional que hoy falta.

**Brecha que abordamos:** no encontramos estudios que cuantifiquen para Chile cuánto cuesta al sistema que los DC se ubiquen donde se proyecta, concentrados en la RM, frente a donde conviene al sistema, en un modelo de expansión de generación y transmisión sobre la red de la PELP.

> Si se quiere una cifra en la brecha: 1.381 MW de DC al 2030, ~89 % en la RM (CEN, Proyección de Demanda 2026–2046). Viene de la ficha N° 45 de la planilla; B no la verificó en el PDF del CEN.

---

## 3. Fichas detalladas

### 3.1 Onodera, Shiraki y Matsuhashi (2026)

**Cita APA 7.** Onodera, H., Shiraki, H., & Matsuhashi, K. (2026). Strategic data center siting can mitigate trade-offs between decarbonization and digitalization in Japan. *Cell Reports Sustainability, 3*(9), 100823. https://doi.org/10.1016/j.crsus.2026.100823

**PDF usado.** Versión publicada, acceso abierto (CC BY 4.0): https://www.cell.com/cell-reports-sustainability/pdf/S2949-7906(26)00192-8.pdf → `pdf\onodera2026_crsus_100823.pdf`. El PDF tiene una portada sin numerar, así que la página del archivo es la impresa + 1. Leído completo (texto principal y métodos); el material suplementario (Document S1) no se leyó. Se leyó también el preprint v2 (`pdf\onodera2025_rs-6707312v2.pdf`, https://www.researchsquare.com/article/rs-6707312/latest.pdf), que queda superado (ver sección 5).

**Problema y método.** ¿Cuánto cambia el costo de descarbonizar Japón según dónde se instalen los DC nuevos? Usan ReGRID, un modelo lineal de costo mínimo que optimiza a la vez la expansión y la operación de generación, almacenamiento, transmisión, remoción de CO₂ e hidrógeno, con balance nodal en 1.741 nodos municipales (403 de subestación) y resolución de 6 horas (p. 7–8 (8–9)). No permite nueva térmica, hidro ni nuclear (p. 8 (9)). Comparan tres estrategias para la capacidad nueva de DC: BAU sigue la distribución actual, ILA deja que el modelo ubique solo en zonas industriales que cumplen umbrales de riesgo, latencia (< 50 ms), agua y transporte, y FLEX deja ubicar sin restricciones (p. 2 (3); Tabla 1, p. 9 (10)). Los DC existentes se mantienen (leyenda de la Fig. 4, p. 6 (7)). Todo se compara contra un caso sin DC (NoDC), con tres trayectorias de crecimiento: en el caso medio, de 2,7 GW en 2020 a 15,3 GW en 2050 (p. 8 (9)). Definen además el «costo de integración» de un DC por municipio como el dual de la restricción de balance nodal dividido por su energía anual (p. 9 (10)).

**Resultado principal (cifras verificadas).**
- Con BAU, los DC suben el costo del sistema de 2050 entre 2,5 % y 12,2 % sobre el caso 1,5 °C sin DC. FLEX reduce ese costo adicional en 16,3 %, 19,7 % y 17,9 % (crecimiento bajo, medio y alto), e ILA en 11,7 %, 14,1 % y 11,6 % (p. 5 (6)).
- El costo de integración va de 39,6 a 120,3 USD/MWh según el municipio: el más alto en el área de Tokio y en islas aisladas, el más bajo en el norte (p. 3 (4)).
- Con BAU, el gas con CCS cubre el 60,8 % de la generación adicional; con ILA y FLEX la eólica marina aporta 32,4 y 36,9 TWh frente a 8,9 TWh en BAU (p. 5 (6)).
- Con BAU, el gran Tokio llega a ~9,8 GW de DC al 2050 en el caso medio (p. 4 (5)); con FLEX aparecen polos junto a nuclear (Higashidori, 2.446 MW), eólica marina (Wakkanai, 1.523 MW) y geotermia (Hachimantai, 1.084 MW) (p. 4–5 (5–6)).
- Conclusión de los autores: mantener la concentración metropolitana es la opción más cara (p. 6 (7)).

**Qué tomamos.**
- El diseño experimental: ubicación proyectada (BAU ≈ nuestro modo base) frente a ubicación elegida por el modelo (FLEX ≈ nuestro modo libre), ambas contra un caso sin DC (≈ nuestro `SIN_DC`).
- La métrica: ahorro como % del costo extra que agregan los DC. Es la misma que usamos, así que los órdenes de magnitud se pueden comparar. Nuestros resultados preliminares del 13-nov dan 10–23 % según el escenario; confirmar con las tablas vigentes antes de mostrarlos junto a esta cita.
- El costo de integración por nodo, calculado con los duales del balance, se puede replicar con los duales del balance de carga de nuestro modelo para explicar por qué el modelo elige cada barra.

**En qué nos diferenciamos.**
- Chile y la red zonal de la PELP 2023–2027 (Switch, días típicos) en vez de 1.741 nodos con resolución de 6 horas.
- Nuestro caso base usa las proyecciones oficiales y el catastro de solicitudes; su BAU extrapola la distribución actual.
- Su porcentaje se mide sobre el costo anual de 2050; el nuestro, sobre el valor presente del horizonte completo.
- Ellos no permiten nueva generación térmica, hidro ni nuclear.

---

### 3.2 Shao, Yu y Wong (2025)

**Cita APA 7.** Shao, Z., Yu, N., & Wong, D. (2025). Stochastic long-term joint decarbonization planning for power systems and data centers: A case study in PJM. *International Journal of Electrical Power & Energy Systems, 173*, 111377. https://doi.org/10.1016/j.ijepes.2025.111377

**PDF usado.** Preprint arXiv v1 (29-oct-2025): https://arxiv.org/pdf/2510.25118 → `pdf\shao2025_arXiv2510.25118.pdf`, leído completo; las páginas citadas son las de ese PDF. La versión publicada es de acceso abierto (CC BY 4.0), pero ScienceDirect no entrega el PDF a descargas automáticas. Su texto completo se leyó en la web: el resumen, la Tabla 7 y la sección 6 coinciden cifra por cifra con el preprint.

**Problema y método.** ¿Cuánto se gana planificando en conjunto los DC y el sistema eléctrico? Programa estocástico de dos etapas (entero-mixto) a 15 años, resuelto con descomposición de Benders (p. 1, 3–8). En la primera etapa decide, por nodo y año, la ubicación y el tamaño de los DC (racks y tipo de servidor), la nueva generación (gas, solar, eólica), el almacenamiento, el retiro de carbón y la expansión de transmisión. En la segunda, la operación horaria con flujos por factores de distribución, más el traslado de carga de cómputo entre DC con latencia máxima de 10 ms (p. 4 y 6; Tabla 6, p. 9). Red de PJM simplificada a 21 nodos (zonas de transmisión) y 42 corredores de más de 161 kV, con demanda punta de 173 GW y 2,5 GW iniciales de DC (p. 8). Cada año usa 4 días representativos horarios, con 50 escenarios y tasa de descuento de 4 % (p. 9). La función objetivo suma costos e incluye emisiones con un precio implícito del carbono (p. 6).

**Resultado principal (cifras verificadas).**
- La planificación no conjunta es la de referencia: los DC eligen sitio según intensidad de carbono y precio local, y la red se planifica después según la demanda proyectada (§6.2.1, p. 9). Frente a ella, la conjunta baja la inversión total de 48,76 a 42,60 mil millones USD/año (−12,63 %). La inversión del sistema eléctrico cae de 28,43 a 25,10 (−11,72 %) y la de los DC de 20,33 a 17,50 (−13,93 %). El costo de operación baja de 62,19 a 57,05 mil millones USD/año (−8,25 %) y las emisiones de operación 5,63 % (Tabla 7, p. 10).
- Esa comparación se hizo en una instancia estática de un año, no en los 15 años (p. 10).
- PJM puede alojar hasta 55 GW de demanda punta de DC (p. 1). En el caso de alta demanda al 2040, Dominion (Virginia) recibe 32,5 GW, ComEd (norte de Illinois) 5,9 GW, METED 4,5 GW, EKPC 4,3 GW y OVEC 3,5 GW (§6.6, p. 12).

**Qué tomamos.**
- La ubicación de los DC como variable de inversión en el mismo problema que la expansión de generación y transmisión, en un sistema real.
- La separación entre el ahorro del sistema eléctrico y el de los DC. Nuestro ahorro es comparable con la línea «Power System Investment» (−11,7 %) más la operación, no con el total.
- Su argumento de que la planificación descoordinada lleva a congestión y refuerzos reactivos más caros (p. 1).

**En qué nos diferenciamos.**
- Nuestro caso base es la ubicación proyectada oficialmente, no una ubicación miope por precio y carbono.
- Excluimos la inversión de los DC y no ponemos precio a las emisiones.
- Modelo determinista con trayectoria completa, mientras su comparación clave es de un año.
- Su red es zonal (un nodo por zona, sin congestión interna, limitación que los autores reconocen en p. 13).

---

### 3.3 Newbery (2026)

**Cita APA 7.** Newbery, D. (2026). *Locating data centres efficiently in Britain – reformed transmission charging, energy subsidies or zonal pricing?* (EPRG Working Paper 2623; Cambridge Working Paper in Economics 2681). Energy Policy Research Group, University of Cambridge. https://www.jbs.cam.ac.uk/wp-content/uploads/2026/10/eprg-wp2326.pdf

**PDF usado.** https://www.jbs.cam.ac.uk/wp-content/uploads/2026/10/eprg-wp2326.pdf → `pdf\newbery2026_eprg-wp2326.pdf`. Leído completo (12 páginas). Las dos primeras son portada y resumen, así que la página del archivo es la impresa + 2. Es un working paper sin revisión por pares formal; el autor agradece a un árbitro (nota 1, p. 1 (3)).

**Problema y método.** La eólica escocesa queda lejos de la demanda y se vierte por congestión, mientras los DC se agrupan en torno a Londres. ¿Qué instrumento lleva los DC a donde conviene al sistema? No hay modelo de optimización propio: es un análisis económico-regulatorio con datos del operador británico (NESO) y resultados de un modelo zonal previo del autor. Compara tres instrumentos: (i) reformar los cargos locacionales de transmisión (TNUoS, basados en el costo incremental de largo plazo de la red), (ii) descuentos de energía en zonas con exportación congestionada (AI Growth Zones) y (iii) precios zonales. La métrica es el costo de transmisión evitado por MWh de demanda firme ubicada detrás de la frontera de exportación B6 (Escocia–Inglaterra) (p. 1–2 (3–4)).

**Resultado principal (cifras verificadas).**
- En 2024-25 se vertió el 13 % de la eólica potencial (9,3 de 71,8 TWh), casi todo en Escocia por congestión (p. 3 (5)).
- 2,2 GW de DC firmes en Escocia evitarían construir uno de los enlaces HVDC submarinos de 2 GW (SEGL2, £131.370/MW-año). Eso equivale a unas £15/MWh, o £263 millones al año (p. 5 (7)).
- Si en vez de enlaces submarinos se construyeran líneas terrestres, el beneficio cae a unas £4,68/MWh (p. 7 (9)).
- El cargo locacional de transmisión a la demanda está topado en cero en el norte de Escocia; sin el tope sería −£34,67/kW-año (−£3,97/MWh para una carga de factor 1). El autor califica el efecto de «perverso» porque desalienta ubicar cargas móviles donde sobra renovable (p. 5 (7)).
- Con precios zonales, la ventaja de precio de Escocia sería de £40/MWh si la exportación se congestiona el 33 % de las horas y de £17/MWh si se congestiona el 14 % (p. 8 (10)). Pero los precios zonales futuros son difíciles de predecir y subestiman el costo de la transmisión que evitan (p. 2 (4), p. 8 (10)).
- En Suecia, con precios zonales, solo 12 de 122 DC están en las zonas baratas del norte (SE1 y SE2). El precio zonal por sí solo es una señal débil de ubicación (p. 2 (4)).
- Recomienda cobrar la transmisión según el costo evitado del refuerzo más caro y condicionar el pago a operar a plena carga cuando la exportación está congestionada (p. 8 (10)).

**Qué tomamos.**
- El mecanismo económico que explica nuestro ahorro: una carga firme ubicada detrás de una restricción de exportación absorbe el excedente renovable y evita transmisión.
- La métrica de costo evitado por MWh de DC, que se puede contrastar con nuestro costo extra por MWh de DC según la ubicación.
- El argumento de política para responder la pregunta 1 (por qué los DC no se ubican donde conviene al sistema): las señales de precio de energía no reflejan el costo de la transmisión que se evita, y los cargos de red pueden incluso desincentivar la ubicación eficiente.

**En qué nos diferenciamos.**
- Nosotros optimizamos la expansión de generación y transmisión; él valora la transmisión evitada con el costo de un enlace específico.
- El contexto regulatorio es otro. En Gran Bretaña hay precio único de energía y cargos de transmisión diferenciados por zona. En Chile hay costo marginal nodal y la transmisión se paga con un cargo uniforme a los clientes. Este último punto es contexto nuestro, no del artículo; confirmar en la ley antes de ponerlo en la lámina.

---

## 4. Revisados y no elegidos

| Estudio (N° en la planilla) | ¿PDF leído? | Por qué no |
|---|---|---|
| Valencia Zuluaga, Pang y Watson (2027), N° 3 | Sí, completo: manuscrito LLNL-CONF de la conferencia PSCC 2026 (https://www.osti.gov/servlets/purl/3375389 → `pdf\valenciazuluaga2027_osti3375389.pdf`) | Es la formulación más cercana (ubicación entera de grandes cargas en una expansión nodal estocástica), pero usa sistemas de prueba (IEEE 24 barras sobre San Diego y 500 barras de Carolina del Sur). Los costos se muestran solo en un gráfico normalizado, sin cifras tabuladas, y en los casos de comparación los DC van en las mismas barras que en el caso co-optimizado. Mide el valor de planificar en conjunto, no el costo de una mala ubicación. Sirve como referencia de método si se pregunta por la formulación. |
| Lindner, Geis, Seibold y Brown (2025), PyPSA-DE, N° 53 | Sí, completo (https://arxiv.org/pdf/2510.09414 → `pdf\lindner2025_arXiv2510.09414.pdf`) | El ahorro en transmisión frente al plan alemán (92 mil millones de €2020) mezcla la conexión flexible de la eólica marina (−50,3), menos eólica marina (−7,7), líneas aéreas en vez de soterradas (−18,1) y menos expansión de red (−15,7) (Fig. 5, p. 6). No aísla la ubicación de los electrolizadores. |
| Kay, Reaser y Taylor (2026), N° 10 | No (B no lo leyó) | Según la ficha, compara la ubicación observada con la de mínimo costo, pero solo en operación, sin expansión de generación ni transmisión. |
| vom Scheidt et al. (2022), N° 55 | No | Análogo con electrolizadores y señal nodal, pero con red y parque fijos (solo despacho). |
| Vargas-Ferrer et al. (2025), N° 52 | No | Análogo chileno (SEN, 19 nodos), pero la ubicación del hidrógeno está acotada al norte y se compara por régimen regulatorio, no contra una ubicación proyectada. Útil si se pide una referencia chilena de modelo nodal. |
| Khanal et al. (2026), N° 4 | No | Las ubicaciones de los DC son exógenas: mide la flexibilidad operativa entre sitios dados. |

---

## 5. Correcciones a la planilla de revisión (6-nov)

1. **Onodera et al. ya está publicado y cambió sus cifras.** La ficha N° 1 dice que es un preprint sin versión publicada. Salió en *Cell Reports Sustainability* 3(9), 100823 (25-sep-2026), con el título cambiado: «trade-offs» en vez de «dilemmas». Las cifras del preprint no deben usarse:

   | Indicador | Preprint v2 (2025) | Versión publicada (2026) |
   |---|---|---|
   | Reducción del costo extra con FLEX | 19,1 % (p. 9 (10)) | 16,3 / 19,7 / 17,9 % según crecimiento (p. 5 (6)); «hasta 20 %» en los highlights |
   | Reducción con ILA | 13,5 % | 11,7 / 14,1 / 11,6 % |
   | Alza del costo por DC con BAU | 5,2 % (vs. 1,5 °C sin DC) | 2,5–12,2 % |
   | Costo de integración | 38,4–124,4 USD/MWh | 39,6–120,3 USD/MWh |
   | Gas con CCS en la generación adicional (BAU) | 64,6 % | 60,8 % |
   | Costo del sistema 1,5 °C sin DC | 130,7 mil M USD/año (+62,5 %) | 125,5 mil M USD/año (+62,4 %) |
   | DC en Higashidori (FLEX) | 5.415 MW en un radio de 50 km | 2.446 MW en la comuna |

2. **PyPSA-DE (N° 53): el ahorro no es «92–191 mil M€».** El texto dice que la transmisión baja *en* 92 mil millones *hasta* 191 mil millones de €2020: de 283,1 a 191,3 mil millones (Fig. 5, p. 6; inversión de 191 mil millones en p. 2). El ahorro es de 92 mil millones de €2020, no un rango.

3. **Shao et al. (N° 2):** las cifras de la ficha coinciden con el PDF y con la versión publicada.
