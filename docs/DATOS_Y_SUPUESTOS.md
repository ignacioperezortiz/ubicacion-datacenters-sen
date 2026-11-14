# Datos y supuestos

De dónde sale cada entrada de `casos/*/inputs/` y por qué se tomó cada supuesto. La formulación está en [FORMULACION.md](FORMULACION.md); la validación de estos datos, en [VALIDACION.md](VALIDACION.md).

Siglas: PELP, Planificación Energética de Largo Plazo; AMEBA, modelo de optimización con que el Ministerio de Energía hizo la PELP 2023–2027; CEN, Coordinador Eléctrico Nacional; SEIA, Sistema de Evaluación de Impacto Ambiental; PDGE, polos de desarrollo de generación eléctrica; FV, fotovoltaica; CSP, concentración solar de potencia; BESS, baterías; CAES, aire comprimido; HVDC, enlace de corriente continua en alta tensión; ENS, energía no suministrada; VOLL, valor de la carga perdida; FOR, tasa de falla forzada; O&M, operación y mantenimiento; FP, factor de planta; MW medios, potencia media anual.

---

## 1. Fuentes

| Fuente | Qué se toma | Dónde |
|---|---|---|
| Ministerio de Energía, PELP 2023–2027, Informe Definitivo (22-abr-2025), escenario Carbono Neutralidad: entradas y salidas del modelo eléctrico AMEBA | Todo el sistema eléctrico: red, demanda, generación, almacenamiento, costos, reserva, impuesto al CO₂ | https://energia.gob.cl/pelp |
| Ministerio de Energía, PELP 2028–2032, Informe Preliminar (jul-2026): datos de entrada del modelo eléctrico (PyPSA-CL, red de 234 nodos) | Trayectorias de data centers de los escenarios E2 y N1, y la red de 234 nodos para asignarlas a zonas | https://energia.gob.cl/pelp |
| CEN, *Proyección de Demanda de Largo Plazo SEN 2026–2046* (oct-2026), sección 5.7.2 y figura 5-13 | Capacidad de data centers identificada al 2030 | https://www.coordinador.cl/wp-content/uploads/2026/10/20261007-INF-proy-demanda-26-46-v01.pdf |
| Catastro de data centers de Raúl Ugarte (CENTRA UAI), con datos al 13-nov-2026: solicitudes de conexión al CEN (plataforma de Acceso Abierto) y proyectos del SEIA | Escenario `PROPIO` | https://accesoabierto.coordinador.cl/ y https://seia.sea.gob.cl/busqueda/buscarProyecto.php |
| Catálogo propio de data centers en Chile (SEIA, prensa y empresas) | Contraste del catastro; un proyecto adicional (Cirion SAN2) | SEIA; Cirion: https://press.ciriontechnologies.com/en/2026/04/29/tier-iii-design-certification-san2-data-center/ |

**Por qué AMEBA.** Es el último informe definitivo de la PELP y publica las entradas y las salidas completas de su modelo eléctrico. Eso permitió traducir los datos a Switch y verificar la traducción contra la propia solución de AMEBA, barra por barra y hora por hora. La PELP 2028–2032 todavía es preliminar; de ella solo se usan las cargas de data centers y su red de 234 nodos para ubicarlas.

**Variantes de los datos AMEBA** (Carbono Neutralidad): demanda `rumbo_CN`; precios de combustibles `PComb_Ref`; costos de inversión `Medio`; perfiles renovables `climate_change_projections`; hidrología MIROC-ESM-CHEM.

**Unidades.** Los CSV de AMEBA no declaran unidades; se determinaron con evidencia:

- **Inversión** (`gen_inv_cost`, `branch_inv_cost`): USD/kW, es decir, miles de USD por MW. En la salida `Transmision_anual.csv`, el costo de inversión en millones de USD es exactamente capacidad (MW) × `branch_inv_cost` / 1.000 en las 402 obras del escenario. Las curvas de costo de baterías del Informe Definitivo (figuras 21 y 22, en USD/kW) coinciden con la variante `Medio`: BESS 4 h, 1.114 USD/kW en 2026 y 667 en 2050. Los órdenes de magnitud calzan: FV 662, eólica 1.173 y ciclo combinado a gas 1.053 USD/kW en 2030. En Switch se multiplican por 1.000.
- **O&M fijo** (`fom_cost`): USD/kW-año, por orden de magnitud (confianza media; ninguna salida lo reporta). Se multiplica por 1.000.
- **Costo variable**: USD/MWh. La identidad precio × tasa de calor + O&M variable reproduce el costo variable de la salida de AMEBA en las 276 térmicas y los seis años de datos.

---

## 2. Red y tiempo

**Por qué esta red.** Se usa la red de la PELP 2023–2027, por recomendación del ayudante del curso, y no la de 234 nodos de la PELP 2028–2032. Es un modelo simplificado acorde al curso, y con 31 zonas cada caso se resuelve en minutos.

**Zonas: 31.** Son las 26 barras eléctricas de AMEBA (500 kV y algunas de 220 kV en el norte) y los 5 polos PDGE. Las 6 barras auxiliares de hidrógeno y amoníaco (`*_H2`, `*_NH3`) no son zonas: su consumo se carga en la barra eléctrica que las alimenta.

**Períodos: 6.** 2026 (2026–2029), 2030, 2035, 2040, 2045 y 2050 (2050–2054). Cada período usa los datos AMEBA de su año de inicio, el «año de datos»; AMEBA tiene datos anuales hasta 2035 y luego cada 5 años. Hay dos excepciones, que usan el promedio de los años del período: el impuesto al CO₂ (sección 7) y los data centers (sección 8).

**Días típicos: 6 por período**, los de los meses impares. AMEBA representa cada mes con un día de 24 bloques horarios. Cada día que se conserva (enero, marzo, mayo, julio, septiembre y noviembre) representa también al mes siguiente: su peso es (días del mes + días del mes siguiente) × años del período. Febrero tiene siempre 28 días, como en AMEBA, y cada período suma 8.760 h por año. Son 144 horas por año, la misma resolución del modelo de la PELP 2028–2032.

**Por qué 6 y no 12 días.** Con 12 días el problema tiene 2,68 millones de restricciones, 2,35 millones de variables y 13,8 millones de coeficientes. La barrera de Gurobi se quedó sin memoria en un equipo de 63 GB, y el simplex dual seguía sin converger a los 110 minutos. Con 6 días el problema es la mitad (1,35 millones de restricciones) y cada caso se resuelve en 8 a 16 minutos.

Efecto de usar 6 días sobre los insumos (mes par igual al impar anterior):

- demanda: −0,04 a −0,09 %;
- energía hidro: +4,9 % en 2035, +4,6 % en 2045, +6,6 % en 2050 y −1,8 % en 2030;
- FP eólico: −5,3 % en 2035 y −1,2 a −1,4 % en 2030 y 2040–2045.

---

## 3. Demanda

$$
D_{z,t}=1{,}031\times\sum(\text{cargas eléctricas conectadas de }z)+\sum(\text{flujo AMEBA de }z\text{ hacia sus barras de H}_2\text{ y NH}_3)
$$

- **Cargas incluidas.** Todas las conectadas: nodales, clientes regulados y no regulados, y electromovilidad (138 cargas con serie). Los factores de `factor.csv` no se aplican: las series ya traen el crecimiento, y la solución de AMEBA abastece exactamente 1,031 × la serie en todas las barras.
- **Factor 1,031.** Es uniforme en todas las barras y bloques de los años de datos; se encontró rehaciendo el balance de cada barra en la solución de AMEBA (generación neta de servicios auxiliares, almacenamiento, flujos y ENS). No figura en ningún archivo de entrada. Como AMEBA resuelve la red con pérdidas nulas, se interpreta como un margen de pérdidas (hipótesis). Con él, Switch, sin pérdidas, abastece la misma energía que AMEBA.
- **Hidrógeno y amoníaco.** Tres barras (LosChangos500, Polpaico500 y NuevaCharrua500) alimentan cada una una barra auxiliar de H₂ y otra de NH₃. Su consumo entra como carga fija en la barra eléctrica, igual al flujo que AMEBA mandó por cada enlace en cada hora. Así se conservan la energía y la forma horaria (el H₂ sigue un perfil solar) que dimensionaron la red y la generación de AMEBA. Las cargas planas desconectadas `L_*_H2_ESS` y `L_*_NH3_ESS` son una copia de la misma energía y no se incluyen.
- **Energía resultante** (TWh/año): 100,4 (2026), 110,5 (2030), 154,2 (2035), 181,9 (2040), 226,0 (2045) y 272,2 (2050). H₂ y NH₃ son 1,6 TWh en 2026 y 108,6 TWh en 2050 (40 %). Sumar todas las columnas del archivo de demanda da 369 TWh en 2050, pero eso cuenta el hidrógeno dos veces; AMEBA abastece 272 TWh.
- La demanda **ya incluye los data centers que operan hoy** (sección 8.1).

---

## 4. Generación

**Regla común: servicios auxiliares descontados.** El balance de AMEBA solo cierra con generación neta de servicios auxiliares (entre 2,0 y 2,6 % de la bruta en los años de datos). Switch trabaja en neto:

- térmicas: la disponibilidad incluye $(1-\text{auxserv})$, y la tasa de calor y el O&M variable se dividen por $(1-\text{auxserv})$, para que el costo y las emisiones por MWh neto sean los de AMEBA;
- FV, eólica y CSP: el perfil de cada central se multiplica por $(1-\text{auxserv})$ antes de agregar;
- hidro: la energía de cada día es la generación AMEBA neta.

Potencias, límites y costos por MW quedan en bruto.

**Inversiones de AMEBA hasta 2025: existentes.** El primer período del modelo es 2026, así que lo que AMEBA decidió construir antes ya es pasado. Entra como capacidad predeterminada, sin costo de inversión, y se descuenta del potencial de cada candidato:

- 3.000 MW FV y 1.000 MW eólicos construidos en 2025;
- 92,1 MW de BESS construidos en 2024;
- 2.000 MW de BESS «ley», que AMEBA construye enteros en 2026 a costo 0, como comprometidos;
- 2.672 MW de transmisión en 7 corredores (sección 6).

### 4.1 Térmica

- **Proyectos.** 276 centrales individuales: 226 existentes o comprometidas y 50 candidatas.
- **Entradas y retiros.** Una central opera en un período si está en servicio el 1 de enero de su año de inicio. El retiro es la fecha más temprana entre `end_time` y la fecha en que la serie de potencia máxima (`pmax.zip`) la lleva a 0. Esa serie trae el cierre del carbón: 1.573 MW en 2026, 1.297 MW en 2030 y 0 desde 2035; Guacolda pasa por etapas de co-combustión con amoníaco (275 MW en 2030 y 701 MW desde 2035).
- **Disponibilidad.** Una tasa de falla equivalente que combina la falla forzada, el mantenimiento promedio del año y los servicios auxiliares. La capacidad disponible neta queda a ±0,1 % de la de AMEBA.
- **Combustibles.** Uno por central, con su precio por año de datos y su intensidad de CO₂, de modo que las emisiones de Switch dan generación bruta × emisión de AMEBA. 28 centrales sin costo de combustible ni emisiones (geotermia, biomasa residual, calor residual) van sin combustible.
- **Candidatos.** Gas natural licuado (ciclo combinado, ciclo abierto, con captura de carbono), diésel y geotermia desde 2030; biomasa desde 2026. Los de gas y diésel tienen 10.000 MW por sitio: en la práctica, sin límite. AMEBA no construyó térmicas en este escenario.
- **Excluidas.** 23 unidades fuera de servicio el 1-ene-2026 y 5 desconectadas en AMEBA (dos condensadores síncronos y la reconversión de Santa María a amoníaco, que el informe no menciona).

### 4.2 Solar FV y eólica

- **Existentes.** Un proyecto por zona y tecnología, con el perfil ponderado por capacidad disponible: 7.699 MW FV y 3.939 MW eólicos, más lo construido en 2025. Se excluyen 1.582 MW de unidades desconectadas que AMEBA lista pero no despacha. AMEBA no retira ninguna central, así que llevan vida de 100 años.
- **Candidatos.** Se agrupan por zona, tecnología, clase de costo y primer período permitido. Dentro de cada grupo se parten en **clases de recurso**: las unidades se ordenan por FP y una clase se divide mientras su rango de FP supere el 12 % (FV) o el 15 % (eólica) de su FP medio. La regla usa solo datos de entrada. Sin clases, el grupo promediaba los mejores sitios con los peores, y la energía de lo que AMEBA construyó quedaba hasta 7,5 % bajo AMEBA en eólica (2030); con clases queda dentro de ±1 % en todos los años.
- **Costos.** Inversión `Medio` del año de datos de cada período; O&M fijo 0 y vida eólica de 50 años, como en AMEBA.

### 4.3 CSP: perfil fijo

AMEBA modela la CSP con campo solar, almacenamiento térmico y turbina. En Switch es un generador variable cuyo perfil es la salida de una regla fija: de día el campo alimenta la turbina y el excedente llena el almacenamiento; desde la puesta de sol se descarga a plena potencia hasta vaciarse. Es la representación más simple que respeta el recurso, el múltiplo solar, el tamaño del almacenamiento y la turbina, y escala con la capacidad construida. Un almacenamiento de Switch cargaría desde la red y no desde su propio campo. Se pierde la flexibilidad horaria: Switch solo puede recortar. AMEBA no construye CSP en este escenario; la única existente es Cerro Dominador (110 MW).

---

## 5. Hidro y almacenamiento

### 5.1 Hidro existente: energía de AMEBA por día típico

- **Proyectos.** 21, uno por zona y tipo (5 de embalse y 16 de pasada), con 7.935 MW, igual que AMEBA.
- **Energía.** La potencia media de cada día típico es la generación que AMEBA despachó ese mes, neta de servicios auxiliares. Con los 12 meses, la energía anual coincide con AMEBA al 0,0 %; con 6 días cambia como se indica en la sección 2. Es la misma en todos los escenarios: la hidro puede mover su energía dentro del día, pero no entre meses.
- **«Embalse» quiere decir regulada.** Incluye las 10 centrales de embalse y 17 centrales aguas abajo de un embalse (1.559 MW), que en AMEBA siguen hora a hora el despacho del embalse. Su mínimo horario es el mínimo que AMEBA despachó.
- **Pasada.** Mínimo de 0,9 × la media del día: casi plana. Con el mínimo observado, Switch podría usarla como almacenamiento.
- **Candidatas.** 8 proyectos de pasada (6.313 MW, desde 2035), como generación variable con el caudal de la hidrología MIROC. AMEBA no construyó ninguna.

### 5.2 Almacenamiento con duración fija

- **Existente.** 26 proyectos, 4.063 MW y 16.232 MWh entregables, incluidos los 2.000 MW «ley» y los 92,1 MW de 2024.
- **Candidatos.** BESS de 1, 2, 4, 6 y 8 h; CAES de 4 h; baterías Carnot de 4 y 12 h en carboneras reconvertidas; bombeo hidráulico desde 2030.
- **Duración fija.** Cada candidato tiene su razón energía/potencia y todo su costo va por MW.
- **Energía entregable.** En AMEBA el estado de carga baja en descarga/eficiencia de descarga, así que la energía entregable con el estanque lleno es la energía nominal × eficiencia de descarga. Por eso una batería «de 4 h» queda con 3,84 h.
- **Eficiencia de ida y vuelta.** Es el producto de las de carga y descarga: BESS 0,92; bombeo 0,81; CAES 0,59; Carnot 0,36.
- **Bombeo.** Su energía se topa en 12 h, lo que no restringe con un ciclo diario. AMEBA también opera el almacenamiento con ciclo diario.
- **Costo de referencia.** BESS de 4 h: 965 USD/kW en 2030, unos 241 USD/kWh.

---

## 6. Transmisión

- **Red de transporte sin pérdidas.** Las 161 líneas de AMEBA quedan en 34 corredores: 29 de red y 5 de enlace a los polos PDGE. Las líneas paralelas se suman en un solo corredor, porque Switch ignora la capacidad de un segundo tramo entre las mismas zonas. Se excluyen 6 enlaces a barras de H₂/NH₃ y 2 líneas desconectadas. La eficiencia es 1 (sección 3).
- **Existente.** 38.519 MW, más 2.672 MW que AMEBA construyó en 2025.
- **Obras comprometidas** (`trans_build_limits.csv`):
  - **HVDC Kimal–Alto Jahuel, desde 2030.** Es el HVDC Kimal–Lo Aguirre, de 2.000 MW en AMEBA, con fecha enero de 2029. El período 2026 se representa con los datos de 2026, cuando no existe, así que entra en el período 2030. La red de AMEBA lleva su terminal a la barra AltoJahuel500.
  - Río Malleco–Pichirropulli, 660 MW, en 2030.
- **Topes acumulados.** Cada corredor puede ampliarse hasta la suma de sus candidatos disponibles hasta ese período. Los candidatos de AMEBA entran en 2025 (aquí, 2026), 2035, 2040 y 2050. Kimal220–LosChangos220 no tiene candidatos y no se amplía. La expansión que hizo AMEBA cabe en estos topes en todos los corredores y períodos.
- **Costos.** Costo overnight por corredor = `branch_inv_cost` × 1.000 USD/MW (entre 17.950 y 625.600 USD/MW), anualizado con vida de 40 años al 6 %, sin O&M, como en AMEBA. La evidencia de la unidad está en `Transmision_anual.csv` (sección 1). Los enlaces PDGE cuestan 1 USD/MW, como en AMEBA.
- **Red existente.** Switch cobra la anualidad de toda la capacidad, también la existente y la comprometida: unos 188 MUSD/año en 2026–2029 y 279 MUSD/año desde 2030. Es un costo constante que no cambia ninguna decisión y se cancela en las diferencias entre casos.
- **Fuera del modelo.** Los enlaces que AMEBA construye hacia las barras de H₂/NH₃ (19.892 MW, unos 995 MUSD) no existen en Switch, porque esa demanda se carga en la barra eléctrica.

---

## 7. Reserva, CO₂, ENS y finanzas

- **Reserva sistémica.** AMEBA usa un área única (SEN): primaria 331/85 MW y secundaria 220/322 MW (subir/bajar), constantes. Se suman en 551 MW de subida y 407 MW de bajada. Dan reserva los 104 proyectos que contienen al menos una unidad con reserva en AMEBA: 60 térmicos (existentes y geotermia candidata), 6 hidro que agrupan las 15 centrales con reserva, 34 CSP y 4 baterías Carnot. Cada uno aporta toda su holgura (sin el tope por unidad de AMEBA). Ni FV, ni eólica, ni BESS aportan reserva en AMEBA.
- **Impuesto al CO₂: promedio del período.** AMEBA lo cobra año a año: 0 hasta 2027, 5 USD/t desde 2028 y 35 USD/t desde 2040. Con el valor del año de inicio, el período 2026 tendría 0 y el 2035 tendría 15,8 USD/t, aunque dentro de ese período llega a 31,1. Como el impuesto cambia los precios relativos entre zonas, que es lo que decide la ubicación, se usa el promedio de cada período: 2,5; 10; 23,48; 35; 35 y 35 USD/t.
- **ENS.** 650 USD/MWh, el VOLL de AMEBA (igual para las 153 cargas).
- **Finanzas.** Tasa de descuento e interés de 6 %, la de AMEBA; valor presente a 2026.

---

## 8. Data centers

### 8.1 Lo que ya está en la demanda

Los data centers que operan hoy suman unos **99 MW medios**: los 198 MW instalados en 2024 que la PELP 2028–2032 toma como punto de partida, al 50 % de utilización. El CEN estima 0,9 TWh en 2025, unos 103 MW medios. La demanda de la PELP 2023–2027 se proyecta desde consumos históricos por barra, así que se supone que ya los incluye. Para no contarlos dos veces, **en todos los escenarios** se agrega solo lo que supera ese nivel: 84,15 MW medios en Polpaico500 y 14,85 en Quillota500, el reparto de la PELP 2028–2032. Con los archivos publicados no se puede confirmar que la demanda los incluya.

### 8.2 Escenarios

Carga media agregada al modelo por encima de lo existente, en MW medios. Cada período usa el **promedio** de la trayectoria anual en sus años, y no el valor del año de inicio: 2026–2029 es el tramo de crecimiento más rápido, y el año de inicio subestimaría la carga del período hasta en 43 %.

| Período | `PELP_E2` | `PELP_N1` | `CEN` | `PROPIO`, ubicable | `PROPIO`, fija | `PROPIO`, total |
|---|---:|---:|---:|---:|---:|---:|
| 2026 | 74,2 | 261,8 | 330,4 | 297,5 | 57,6 | 355,1 |
| 2030 | 224,8 | 749,8 | 591,0 | 1.784,0 | 115,2 | 1.899,2 |
| 2035 | 272,8 | 1.022,8 | 591,0 | 1.905,5 | 115,2 | 2.020,7 |
| 2040 | 292,4 | 1.042,4 | 591,0 | 1.905,5 | 115,2 | 2.020,7 |
| 2045 | 311,9 | 1.061,9 | 591,0 | 1.905,5 | 115,2 | 2.020,7 |
| 2050 | 331,5 | 1.081,5 | 591,0 | 1.905,5 | 115,2 | 2.020,7 |

- La carga total de data centers del sistema es la de la tabla más los 99 MW existentes.
- En `PELP_E2`, `PELP_N1` y `CEN`, toda la carga agregada es ubicable.
- En `PROPIO`, la parte fija es el llenado de campus ya conectados (sección 8.5) y no se mueve en ningún caso.
- El caso `SIN_DC` no agrega nada (sección 8.6).

**Ubicación base** (dónde la ponen las proyecciones), desde 2035, en % del total agregado o en MW medios:

| Escenario | Polpaico500 | Quillota500 | AltoJahuel500 | Kimal220 |
|---|---|---|---|---|
| `PELP_E2` | 85 % | 15 % | — | — |
| `PELP_N1` | como E2 | como E2 | — | 75 MW medios en 2026, 375 en 2030 y 750 desde 2035 (promedio por período: 187,5; 525; 750) |
| `CEN` | 89 % | 11 % | — | — |
| `PROPIO` | 824 + 93,7 fija | 400 | 681,5 + 21,5 fija | — |

Las zonas candidatas del caso libre son las 26 barras eléctricas; los polos PDGE no lo son, porque son polos de generación sin ubicación propia. No hay tope por zona ni costo de conexión o de terreno.

### 8.3 `PELP_E2` y `PELP_N1`: PELP 2028–2032

La PELP 2028–2032 trae los data centers como tres cargas planas (el mismo valor todas las horas del año), cada una en un nodo de su red de 234 nodos:

| Carga | Nodo PELP 2028–2032 | Zona del modelo |
|---|---|---|
| Región Metropolitana | S/E El Salto 220 kV (Huechuraba) | Polpaico500 |
| Valparaíso | S/E Torquemada 110 kV (Concón) | Quillota500 |
| Antofagasta (solo N1) | S/E Kimal 220 kV (María Elena) | Kimal220 |

- **Trayectoria.** RM + Valparaíso: 99 MW medios en 2026, 297 en 2030, 364 en 2035 y 450 en 2057, siempre 85 % / 15 %. Es idéntica en los escenarios E1, E2, E3 y N2. N1 agrega Antofagasta: 75 MW más por año desde 2026 hasta 750 MW en 2035.
- **E2 y N1.** E2 es el escenario de demanda media. En N1, el informe agrega la carga de Antofagasta como medida para aprovechar el vertimiento del norte; coincide en nodo y tamaño con el campus de IA anunciado en Kimal.
- **Asignación a zonas.** La hicieron dos agentes por separado, con métodos distintos, y llegaron a la misma zona en los tres nodos:
  - uno con distancia geográfica, camino de menor reactancia, reactancia efectiva y reparto de Kron en la red de 234 nodos;
  - otro con el camino eléctrico de cada nodo, factores de distribución de un flujo DC y la zona en que AMEBA dejó las centrales de esos nodos.
- **El Salto** es el único caso dudoso: está en la malla 220/110 kV de Santiago, casi en empate entre Polpaico500 y AltoJahuel500. Se asigna a Polpaico500 porque su única línea de 220 kV llega a Polpaico, que es también el camino de menor reactancia y la barra más cercana (28 km). De los data centers de la RM que operan o tienen aprobación ambiental con capacidad conocida, ~88 % está en esa zona (Quilicura, Lampa, Colina, Huechuraba).

### 8.4 `CEN`: Coordinador Eléctrico Nacional

- **Capacidad.** La identificada por el CEN en su Proyección de Demanda 2026–2046 (figura 5-13): 552 MW en 2026, 642 en 2027, 963 en 2028, 1.281 en 2029 y **1.381 MW en 2030**, plana después. El CEN la deja plana porque se agota la cartera de proyectos informados por las empresas.
- **Utilización: 50 %**, la misma con que la PELP pasa de capacidad a demanda. Da 690 MW medios desde 2030.
- **Reparto.** El del CEN al 2030: RM 1.225 MW (a Polpaico500) y Valparaíso 155 MW (a Quillota500). Como esos dos suman 1.380 y no 1.381, el total queda en 690,0 y no en 690,5 MW medios.

### 8.5 `PROPIO`: catastro de solicitudes de conexión

Proyección construida desde proyectos con solicitud de conexión, no desde anuncios. La base es el catastro de **Raúl Ugarte (CENTRA UAI)**: las solicitudes de conexión de data centers al CEN (plataforma de Acceso Abierto) vigentes en su cronograma, que suman 4.233,4 MW, y los proyectos del SEIA. Se complementa con un catálogo propio de 35 proyectos.

**Reglas de conciliación:**

1. **Existentes.** Toda solicitud vigente con conexión hasta 2025 se supone dentro de la demanda (sección 8.1) y no se agrega: 12 solicitudes, 428,4 MW. Las ampliaciones con solicitud propia desde 2026 sí entran.
2. **Un campus, una vez.** Se descartan las alternativas y duplicados: el segundo alimentador de 14 MW del mismo data center (misma subestación y fecha) y una solicitud detenida que repite otra. Aparte, quedan fuera dos solicitudes vigentes que no informan MW.
3. **Catálogo.** Un proyecto del catálogo se suma solo si no corresponde a un grupo del catastro (mismo titular, sitio o subestación; la comuna sola no basta). El único adicional es Cirion SAN2 (Quilicura, 20 MW en 2026), que se conecta en distribución y no aparece en el CEN. Los anuncios sin año de conexión (Atacama Data, campus de Grenergy, Solutions 2) quedan fuera.
4. **Utilización: 50 %** de los MW solicitados, en el año estimado de conexión, como carga plana.

**Resultado:** 19 solicitudes nuevas (3.791 MW) más Cirion = 3.811 MW solicitados, 1.905,5 MW medios desde 2032.

| Año | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 en adelante |
|---|---:|---:|---:|---:|---:|---:|---:|
| MW medios acumulados | 16 | 22 | 454 | 698 | 1.448 | 1.755,5 | 1.905,5 |

**Ubicación por subestación de conexión** (criterio: la barra de 500/220 kV que la abastece, verificada con la red de 234 nodos):

| Zona | MW solicitados | Subestaciones (comuna) |
|---|---:|---|
| Polpaico500 | 1.648 | Chacabuco, Quilicura y Punta Verde (Quilicura); Chicureo (Colina); Nueva Lampa y Santa Teresa (Lampa); Manuel Rodríguez y Polpaico 500 kV (Tiltil); Cirion (Quilicura) |
| AltoJahuel500 | 1.363 | Seccionadora Lo Aguirre 500 kV y Lo Prado (Pudahuel); Bajos de Mena (Puente Alto); Odata San Bernardo; Alto Jahuel 110 kV (Buin) |
| Quillota500 | 800 | La Pólvora 220 kV (Valparaíso) |

**Casos dudosos, decididos por el equipo del proyecto:**

- **Lo Aguirre → AltoJahuel500** (1.025 MW solicitados). Eléctricamente es un empate: Lo Aguirre secciona la línea Polpaico–Alto Jahuel, y el reparto de Kron da 51 % y 47 %. Decide la red de AMEBA, que lleva el terminal del HVDC Kimal–Lo Aguirre a AltoJahuel500. Ponerlos en Polpaico500 los separaría del HVDC con que comparten barra en la realidad.
- **Ignis = 2 proyectos.** Noviciado I (Lo Aguirre) y Pacífico 33-S (La Pólvora), de 500 MW cada uno, tienen otro nombre, otra comuna y otra región.
- **SC1 y SC2 = 2 proyectos.** SC1 (Manuel Rodríguez, 300 MW, detenida) y SC2 (Polpaico, 500 MW) tienen distinto titular, subestación y potencia.

Dos agentes hicieron la conciliación por separado, con las mismas reglas, y llegaron a la misma trayectoria por zona y año, sin ninguna diferencia.

**Llenado de los campus ya conectados: 115,2 MW medios fijos.** Las conexiones existentes (regla 1) suman 428,4 MW. Con la misma utilización de 50 %, a plena ocupación consumirían 214,2 MW medios. Hoy consumen unos 99–103 MW medios, según dos fuentes: la PELP (198 MW instalados × 50 %) y el CEN (0,9 TWh en 2025). La diferencia, 214,2 − 99 = 115,2 MW medios, es crecimiento dentro de conexiones que ya existen y que no aparece en ninguna solicitud nueva.

- **Fija.** Entra como carga fija, porque esos campus ya están construidos: 93,7 MW medios en Polpaico500 (Lampa, Colina, Quilicura) y 21,5 en AltoJahuel500 (San Bernardo, Padre Hurtado), en proporción a sus MW conectados.
- **Rampa.** Sube linealmente hasta 2030, un 20 % por año desde 2026, así que el período 2026 promedia 57,6 MW medios.

**Es una cota superior.** Toma toda la cartera vigente sin probabilidad de realización: en 2030 son 2.896 MW solicitados, frente a los 1.381 MW que identifica el CEN. Según el historial del propio catastro, en las cohortes de 2018–2023 solo el 25 % de los MW solicitados llegó a declararse en construcción. El catastro trae además un escenario con probabilidades que da 695 MW al 2030.

### 8.6 `SIN_DC`

Carbono Neutralidad con la demanda de AMEBA tal cual (que incluye los ~99 MW existentes) y sin carga adicional de data centers. Solo se corre en modo base. Es la referencia para medir el costo extra de los data centers de cada escenario.

---

## 9. Limitaciones

- **Previsión perfecta.** El modelo conoce todo el horizonte. En el caso libre, cada data center va a la zona más barata para toda su vida útil, con los precios futuros que el propio modelo produce.
- **Sin compromiso de unidades ni inercia.** No hay mínimos técnicos, rampas, costos de partida ni tiempos mínimos; el problema es lineal. Algunas centrales que AMEBA opera en su mínimo técnico quedan libres en Switch.
- **Transporte en vez de flujo DC.** No hay leyes de Kirchhoff. En la PELP 2028–2032, un modelo de transporte deja pasar 20–40 % más de flujo norte → centro que el flujo DC, lo que abarata abastecer la RM: el caso base sale más barato de lo que es y el ahorro de ubicar bien queda subestimado por este lado.
- **Sin costos de conexión ni de terreno de los data centers**, y sin tope por zona. El ahorro es solo del sistema eléctrico y, por este lado, una cota superior: el caso libre puede concentrar toda la carga en una o dos zonas sin pagar subestaciones, líneas de conexión ni terreno.
- **Red de 26 barras.** Es la red de AMEBA: agrega subestaciones que en la realidad están separadas (toda la demanda de Santiago está en dos barras, AltoJahuel500 y Polpaico500) y no tiene criterio N−1.
- **6 días típicos.** Más energía hidro en 2035–2050 y menos FP eólico en 2035 (sección 2).
- **Hidro sin embalse entre meses.** La energía mensual es la que despachó AMEBA, la misma en todos los casos.
- **Período 2026 con datos de 2026.** El norte queda sin HVDC en 2026–2029. Por eso la ubicación es fija hasta 2029 (`--dc-libre-desde 2030`).
- **Vida útil por períodos completos** (`--retire late`). Santa María y Guacolda 3–5 (805 MW de carbón) operan 2–3 años más que en AMEBA dentro del período 2030. Afecta igual al caso base y al libre.
- **Carga de data centers plana**, con 50 % de utilización y sin flexibilidad horaria.
- **Reserva simplificada.** Sin tope de reserva por unidad (sección 4.6 de la formulación).
