# Búsqueda bibliográfica: propuesta A

Diapositiva de literatura de la presentación de avance del proyecto. La pregunta es cuánto se ahorra en la planificación de generación y transmisión del SEN (Sistema Eléctrico Nacional de Chile) si los data centers se ubican donde le conviene al sistema, en vez de donde dicen las proyecciones.

- **Insumo:** `02-proyecto\revision-literatura\revision-literatura-data-centers.xlsx`, con 58 candidatas.
- **Elegidos:** 3 estudios.
- **Lectura:** los tres PDF se leyeron completos (en `pdf\`).
- **Fecha:** 17-nov-2026.

**Páginas.** «p. X» es el número impreso en el documento y «PDF p. Y» la página del archivo:
- en Shao et al. coinciden;
- en Onodera et al. el PDF suma una portada (PDF = impresa + 1);
- en Newbery el PDF suma portada y resumen (PDF = impresa + 2).

---

## 1. Propuesta para la diapositiva

**Onodera et al. (2026).** *Strategic data center siting can mitigate trade-offs between decarbonization and digitalization in Japan.*
- Usan un modelo de expansión de costo mínimo de Japón (generación, almacenamiento y transmisión, 1.741 nodos municipales) y comparan dos casos al 2050: data centers donde están hoy (Tokio y Osaka) o donde el modelo elige.
- Los data centers suben 5,2 % el costo del sistema. Si el modelo elige la ubicación, ese costo extra baja 19,1 %, y 13,5 % con restricciones de sitio (riesgo sísmico, latencia, zonas industriales).
- Es la misma comparación y la misma métrica que usamos (ahorro como % del costo extra, frente a un caso sin data centers). En el SEN obtenemos 10–22 %.

**Shao, Yu y Wong (2025).** *Stochastic long-term joint decarbonization planning for power systems and data centers: A case study in PJM.*
- Planifican a 15 años en PJM (el mayor operador de red de EE. UU., modelado en 21 zonas). El modelo decide dónde y cuántos data centers instalar, junto con la generación, el almacenamiento y la transmisión.
- Frente a ubicar los data centers sin coordinarse con la red, la inversión del sistema eléctrico baja 11,7 % y el costo de operación 8,3 % (instancia de un año).
- Respalda tratar la ubicación como variable de decisión dentro de la expansión, con red zonal y días representativos, como hacemos con Switch.

**Newbery (2026).** *Locating data centres efficiently in Britain – reformed transmission charging, energy subsidies or zonal pricing?*
- Analiza las señales económicas que orientan dónde se instalan los data centers en Gran Bretaña: los cargos de transmisión, los descuentos de energía por zona y los precios zonales.
- Ubicar 2,2 GW de data centers en Escocia, detrás de la frontera de transmisión congestionada, evitaría un enlace submarino de 2 GW: unas £15/MWh, o £263 millones al año. El cargo de transmisión vigente no premia esa ubicación.
- Explica por qué el mercado no llega solo a la ubicación que conviene al sistema, y lo conecta con la transmisión y los precios nodales y zonales del curso. Nuestro ahorro mide el valor de una señal locacional que hoy no existe en Chile.

**Brecha.** Entre las 58 fuentes revisadas no hay ningún estudio que compare, para Chile, el costo de planificación según dónde se ubiquen los data centers: las proyecciones (PELP y Coordinador) fijan la ubicación de antemano. Nuestro trabajo lo cuantifica con un modelo de expansión de generación y transmisión sobre la red de la PELP, para cuatro proyecciones de demanda.

Notas al pie:
- En Onodera et al., las cifras salen del preprint v2 (2025). Hay que contrastarlas con la versión publicada (ver §2.1).
- Nuestro rango de 10–22 % sale del README del repositorio `ubicacion-datacenters-sen` (13-nov).

---

## 2. Fichas por estudio

### 2.1 Onodera, Shiraki y Matsuhashi: ubicación estratégica en Japón

**Cita APA 7 (versión publicada, la que corresponde citar):**
Onodera, H., Shiraki, H., & Matsuhashi, K. (2026). Strategic data center siting can mitigate trade-offs between decarbonization and digitalization in Japan. *Cell Reports Sustainability, 3*(9), 100823. https://doi.org/10.1016/j.crsus.2026.100823

**Versión leída (preprint):**
Onodera, H., Shiraki, H., & Matsuhashi, K. (2025). *Strategic data center siting can mitigate dilemmas between decarbonization and digitalization in Japan* [Preprint, versión 2, 25-jun-2025]. Research Square. https://doi.org/10.21203/rs.3.rs-6707312/v2

- **PDF usado:** https://www.researchsquare.com/article/rs-6707312/latest.pdf (redirige a la v2). Guardado como `pdf\Onodera2025_rs-6707312_v2.pdf`, de 32 págs.: 17 de texto más figuras, tabla y referencias.
- **Lectura:** completa, salvo el material suplementario, que no viene en el PDF. Las figuras S1–S11, entre ellas la S4 del 19,1 %, no se vieron.
- **Hallazgo nuevo:** la versión publicada no figura en el Excel del 6-nov.
  - Datos (Crossref, OpenAlex): Cell Reports Sustainability, vol. 3, n.º 9, sep-2026, acceso abierto con licencia CC BY 4.0. El título cambió de «dilemmas» a «trade-offs».
  - Descarga: no fue posible, porque cell.com exige una verificación antiscraping que no se intentó saltar.
  - Resumen: el publicado es igual al del preprint y no trae cifras.
  - **Pendiente:** descargarla en el navegador desde https://doi.org/10.1016/j.crsus.2026.100823 y confirmar las cifras de abajo.

**Problema y método**
- **Pregunta:** cuánto cambia el costo de descarbonizar el sistema eléctrico de Japón según dónde se ubiquen los nuevos data centers. Al 2050 pasan de 2,7 a 15,3 GW (caso medio; p. 4, PDF p. 5).
- **Modelo:** ReGRID, de costo mínimo, que optimiza en conjunto la inversión y la operación de generación, almacenamiento, transmisión, remoción de CO₂ e hidrógeno (p. 13, PDF p. 14).
  - **Red:** 1.741 nodos municipales y 403 nodos de subestación (p. 13, PDF p. 14).
  - **Resolución:** pasos de 6 horas, 4 por día durante los 365 días (p. 13, PDF p. 14).
  - **Restricción:** no se permiten nuevas centrales térmicas, hidro ni nucleares (p. 13, PDF p. 14).
- **Tres estrategias** (p. 4, PDF p. 5):
  - **BAU:** mantiene la concentración actual en Tokio y Osaka. El 64,0 % de la superficie de data centers está en el gran Tokio y el 16,8 % en Osaka (p. 7, PDF p. 8).
  - **FLEX:** el modelo elige la ubicación libremente.
  - **ILA:** como FLEX, pero solo en zonas industriales que cumplen umbrales de sismo, tsunami, inundación, tifón, latencia menor a 50 ms, agua y transporte (tabla 1, p. 25, PDF p. 26).
- **Contrafactual NoDC:** un caso sin data centers, para medir el costo que estos agregan (p. 4, PDF p. 5). Los data centers existentes se mantienen (fig. 5, p. 22, PDF p. 23).
- **Costo de integración por municipio:** el dual del balance nodal dividido por la energía del data center (p. 14, PDF p. 15).

**Resultados (preprint v2)**
- **Costo de integración:** varía entre 38,4 y 124,4 USD/MWh según el municipio. Es más alto en Tokio y en las islas aisladas, y más bajo en el norte (p. 6, PDF p. 7).
- **Costo de los data centers (BAU):** sube el costo del sistema 5,2 % frente al caso de 1,5 °C sin data centers, y 8,5 % frente al caso base sin ellos (p. 9, PDF p. 10).
- **Ahorro por ubicación:** FLEX reduce ese costo adicional 19,1 % e ILA 13,5 % (p. 9, PDF p. 10). En la discusión: «hasta 19,1 %» (p. 10, PDF p. 11).
- **Generación adicional:**
  - En BAU, el gas con captura de CO₂ cubre el 64,6 % de la generación adicional.
  - La eólica marina aporta 25,9 TWh en ILA y 30,8 TWh en FLEX, frente a 6,2 TWh en BAU.
  - FLEX reduce 46,7 % el gas con captura (p. 9, PDF p. 10).
- **Dónde ubica FLEX:**
  - junto a la nuclear de Higashidori (5.415 MW de data centers y 5.253 MW nucleares);
  - en Wakkanai (1.563 MW con 2.798 MW de eólica marina) (p. 8, PDF p. 9).
- **Conclusión de los autores:** mantener la concentración metropolitana es «la opción más costosa y riesgosa» (p. 10, PDF p. 11).

**Qué tomamos**
- **El diseño experimental:** sin data centers, ubicación proyectada y ubicación elegida por el modelo. Es el mismo que el nuestro: `SIN_DC`, base y libre.
- **La métrica:** el ahorro como porcentaje del costo extra que agregan los data centers. Su 13,5–19,1 % es directamente comparable con nuestro 10–22 %.
- **Los data centers existentes quedan fijos,** como en nuestro modo libre antes de 2030.
- **El costo de integración por nodo vía duales,** como lectura posible de nuestros precios por zona (`precios.py`).

**En qué nos diferenciamos**
- **Caso base:** usamos proyecciones oficiales chilenas (PELP E2 y N1, Coordinador) y una propia, no la distribución actual.
- **Sistema:** el SEN es hidro-solar, con una red larga norte–sur de 31 zonas.
- **Trayectoria:** usamos 6 días típicos por año y una trayectoria con varios períodos. Ellos usan pasos de 6 horas, 1.741 nodos y reportan sobre todo el año 2050.
- **Expansión:** su modelo no permite nueva térmica, hidro ni nuclear; el nuestro expande con el catálogo de la PELP.

---

### 2.2 Shao, Yu y Wong: planificación conjunta en PJM

**Cita APA 7:**
Shao, Z., Yu, N., & Wong, D. (2025). Stochastic long-term joint decarbonization planning for power systems and data centers: A case study in PJM. *International Journal of Electrical Power & Energy Systems, 173*, 111377. https://doi.org/10.1016/j.ijepes.2025.111377

- **Revista:** IJEPES (International Journal of Electrical Power & Energy Systems, Elsevier), con revisión por pares y acceso abierto (CC BY 4.0).
- **PDF usado:** preprint arXiv:2510.25118v1 (29-oct-2025), https://arxiv.org/pdf/2510.25118. Guardado como `pdf\Shao2025_arXiv2510.25118.pdf`, de 17 págs.
  - La versión de la revista (en línea desde el 5-nov-2025) no se pudo descargar: ScienceDirect devuelve una página antiscraping.
  - arXiv tiene una sola versión, subida una semana antes de la publicación. Las páginas citadas son las del preprint.
- **Lectura:** completa.

**Problema y método**
- **Pregunta:** cómo planificar en conjunto, durante 15 años, los data centers y el sistema eléctrico, y cuánto se gana frente a planificarlos por separado.
- **Modelo:** programa estocástico de dos etapas resuelto con descomposición de Benders (pp. 3–8).
  - **Primera etapa:** decide ubicación, tamaño (racks) y tipo de servidor de los data centers. También decide la expansión de gas, solar, eólica, almacenamiento y transmisión, y el retiro de carbón (pp. 3–4).
  - **Segunda etapa:** resuelve el despacho con flujos linealizados y la transferencia de cómputo entre sitios (pp. 4–6).
- **Red:** 21 zonas de PJM, cada una un nodo, con 42 corredores de más de 161 kV (p. 8). Los data centers quedan en el centro geométrico de cada zona (p. 12).
- **Tiempo y escenarios:** 4 días representativos por año, 50 escenarios y tasa de descuento de 4 % (p. 9).
- **Caso de comparación «no conjunto»** (p. 9): los data centers eligen ubicación y tamaño según la intensidad de carbono y el precio locales, y la red se planifica después según la demanda proyectada.

**Resultados**
- **Capacidad y ubicación:** PJM puede alojar hasta 55 GW de demanda punta de data centers, y las zonas óptimas son Dominion (Virginia) y ComEd (norte de Illinois) (p. 1).
- **Distribución al 2040, caso de alta demanda:** Dominion 32,5 GW y ComEd 5,9 GW (p. 12).
- **Conjunto vs. no conjunto** (tabla 7, p. 10; instancia estática de un año):
  - inversión total de 48,76 a 42,60 miles de millones de USD al año (−12,63 %);
  - inversión del sistema eléctrico de 28,43 a 25,10 (−11,72 %);
  - inversión de los data centers de 20,33 a 17,50 (−13,93 %);
  - costo de operación de 62,19 a 57,05 (−8,25 %).
- **Transmisión:** se invierte por etapas, por ejemplo 2,63 miles de millones de USD en 2030 (p. 10).
- **Peso del carbono:** al subirlo, unos 28 GW de data centers salen de las zonas intensivas en carbono (p. 12).
- **Limitación declarada:** cada zona de PJM es un solo nodo, así que no hay congestión dentro de la zona (p. 13).

**Qué tomamos**
- **El respaldo, con revisión por pares, de que la ubicación de los data centers puede ser una variable del modelo de expansión de generación y transmisión** de un sistema real. Usan red zonal y días representativos, la misma escala de modelación que nuestra versión de Switch (31 zonas, 6 días típicos).
- **La lectura del resultado:** la coordinación baja a la vez la inversión en el sistema eléctrico y el costo de operación.

**En qué nos diferenciamos**
- **Caso de comparación:** el suyo es una ubicación miope por precio y carbono; el nuestro es la ubicación de las proyecciones oficiales.
- **Qué se decide:** en su modelo también se deciden la capacidad, el tipo de servidor y la inversión de los data centers. En el nuestro, los MW y los años son datos; solo cambia la zona, sin costo del data center.
- **Base del porcentaje:** sus porcentajes son sobre la inversión o la operación total del sistema; los nuestros, sobre el costo extra de los data centers. No son comparables uno a uno.
- **Incertidumbre:** el suyo es estocástico; el nuestro, determinista con previsión perfecta.

---

### 2.3 Newbery: señales para ubicar data centers en Gran Bretaña

**Cita APA 7:**
Newbery, D. (2026). *Locating data centres efficiently in Britain – reformed transmission charging, energy subsidies or zonal pricing?* (EPRG Working Paper 2623; Cambridge Working Paper in Economics CWPE2681). Energy Policy Research Group, University of Cambridge. https://www.jbs.cam.ac.uk/wp-content/uploads/2026/10/eprg-wp2326.pdf

- **PDF usado:** el de la URL de arriba, guardado como `pdf\Newbery2026_EPRG2623.pdf`, de 12 págs.
  - La URL dice «2326», pero el documento es el EPRG 2623 / CWPE2681, fechado el 12-oct-2026 (PDF pp. 1 y 3).
  - Es un working paper; en una nota agradece a un árbitro (p. 1).
- **Lectura:** completa.

**Problema y método**
- **Pregunta:** cómo dar señales eficientes para que los data centers se instalen donde sobra viento (Escocia) y no junto a Londres.
- **Opciones que compara:**
  - reformar los cargos de transmisión TNUoS (Transmission Network Use of System, cargos por uso de la red que varían según la ubicación);
  - descuentos de energía en las «AI Growth Zones»;
  - precios zonales.
- **Método:** no tiene modelo de optimización propio. Cuantifica con datos de NESO (el operador del sistema británico), con el costo anualizado de los enlaces submarinos de corriente continua (HVDC) Escocia–Inglaterra y con un modelo zonal previo de Chyong y Newbery.

**Resultados**
- **Vertimiento:** en 2024-25 se vertió el 13 % del viento potencial (9,3 de 71,8 TWh), casi todo en Escocia por la congestión de la frontera B6 (p. 3, PDF p. 5).
- **Inversión en red:** NESO recomendó unos £64 mil millones de inversión, cifra que luego subió a £89 mil millones (p. 4, PDF p. 6).
- **Cargo de transmisión a la demanda:** en el norte de Escocia está topado en cero; sin el tope sería −£34,67/kW-año (−£3,97/MWh). El autor llama «perverso» el efecto, porque desalienta ubicar grandes cargas donde sobra renovable (p. 5, PDF p. 7).
- **Capacidad de la frontera B6:** sube de 6.683 MW en 2026 a 15.354 MW en 2030 (p. 5, PDF p. 7).
- **Enlace evitado:** 2,2 GW de data centers en Escocia evitarían construir un enlace submarino de 2 GW. Con su costo de £131.370/MW-año, el ahorro es de unas £15/MWh, o £263 millones al año (p. 5, PDF p. 7).
- **Si se usan líneas terrestres:** el beneficio cae a unas £4,68/MWh (p. 7, PDF p. 9).
- **Descuento del gobierno:** puede llegar a £24/MWh en Escocia (p. 7, PDF p. 9).
- **Vertimiento al 2030:** sin nueva transmisión, 13,9 TWh, con la frontera congestionada el 33 % de las horas; con toda la transmisión planificada, 7,6 TWh y 14 % (p. 7, PDF p. 9).
- **Ventaja con precios zonales:** Escocia tendría entre £17 y £40/MWh de ventaja (p. 8, PDF p. 10).
- **Suecia:** de 122 data centers, solo 12 están en las zonas norteñas, más baratas. Según el autor, el precio zonal por sí solo es una señal débil de ubicación (p. 2, PDF p. 4).
- **Recomendación:** cobrar la transmisión según el costo evitado del refuerzo más caro, con pago condicionado a operar a plena carga cuando la frontera está congestionada (p. 8, PDF p. 10).

**Qué tomamos**
- **El mecanismo económico:** una carga plana y firme, ubicada detrás de una restricción de transmisión, sustituye red y aprovecha la energía que sobra. Ese es el ahorro que nuestro modelo captura de forma endógena.
- **El argumento de mercado:** sin una señal locacional eficiente, los data centers se agrupan cerca de la demanda. Encaja con los contenidos del curso sobre red de transmisión y precios nodales y zonales.
- **La forma de expresar el resultado** en costo evitado por MWh de data center, como nuestro costo extra de 32–45 USD/MWh.

**En qué nos diferenciamos**
- **Método:** él estima el beneficio con el costo de un enlace concreto; nosotros lo obtenemos de un modelo de expansión de generación y transmisión co-optimizado.
- **Alcance:** no modela la operación horaria ni otras ubicaciones; nosotros cubrimos todo el SEN y varias proyecciones.
- **Moneda y marco regulatorio:** sus cifras están en libras y son del marco británico; no se convierten.

---

## 3. Por qué estos tres

Se buscó cubrir los tres papeles pedidos con lo más cercano a nuestra comparación:

| Papel | Estudio | Por qué |
|---|---|---|
| Referencia metodológica (análogo directo) | Onodera et al. | Comparación casi idéntica: sin data centers, ubicación proyectada y ubicación elegida por el modelo, con el ahorro como % del costo extra. Ahora publicada con revisión por pares. |
| Planificación con ubicación endógena | Shao et al. | Revista con revisión por pares, sistema real y la ubicación de los data centers dentro de la expansión de generación, almacenamiento y transmisión. |
| Señales locacionales y costos de red | Newbery | Explica el mecanismo económico (red evitada, cargos de transmisión, precios zonales) con cifras de un sistema real. Conecta con el curso. |

**No elegidos** (los de relevancia 4–5 más cercanos):
- **Kay, Reaser y Taylor (2026), Dallas Fed WP 2606.**
  - Se leyeron el resumen, la introducción, la sección 6.4 y las conclusiones en `pdf\Kay2026_DallasFed_wp2606.pdf`.
  - Usan un modelo de despacho de corto plazo, sin expansión de generación ni de transmisión. Por eso no respalda una comparación de costos de planificación.
  - Sirve como dato de contexto si sobra espacio: la región del norte de Virginia concentra el 38,8 % del cómputo, y la asignación de mínimo costo de operación le daría el 0,78 % (p. 33, PDF p. 35). Los autores advierten que esa asignación ignora latencia, construcción y conexión (p. 32, PDF p. 34).
  - APA: Kay, O., Reaser, R., & Taylor, R. (2026). *Processing power: The effect of data centers on wholesale electricity markets* (Working Paper No. 2606). Federal Reserve Bank of Dallas. https://doi.org/10.24149/wp2606
- **Valencia Zuluaga, Pang y Watson (2027), EPSR.**
  - Tiene la formulación más parecida.
  - Pero usa sistemas de prueba, y sus casos comparan las mismas ubicaciones, de modo que mide el valor de planificar en conjunto y no el costo de una mala ubicación.
  - Según la ficha del Excel; no leído en esta pasada.
- **Khanal et al. (2026), preprint.**
  - Las ubicaciones son dadas: mide flexibilidad de operación entre sitios, no dónde construir.
  - Según la ficha; no leído.
- **Vargas-Ferrer et al. (2025), Energy Policy.**
  - Es el análogo chileno: ubicación de electrolizadores junto con la transmisión del SEN. Pero trata hidrógeno, no data centers, y restringe la ubicación al norte.
  - Sirve para reforzar la brecha si se quiere nombrar un trabajo chileno.
  - Según la ficha; no leído, así que no se citan cifras.

---

## 4. Verificación y pendientes

- **Chequeo con script:** se revisaron 87 afirmaciones contra el texto extraído de cada PDF, cifra por cifra y en la página indicada, después de quitar la numeración de líneas del preprint de Onodera. Todas aparecen en la página citada.
  - Scripts en el scratchpad de la sesión; no son parte de la entrega.
- **Cifras de nuestro proyecto** (10–22 %; 32–45 USD/MWh; ubicación en el sur): tomadas del README de `<repo>\` (13-nov), sin recalcular.
- **Pendiente 1:** contrastar las cifras de Onodera et al. con la versión publicada (Cell Reports Sustainability, 2026), que hay que descargar en el navegador.
- **Pendiente 2:** antes de mostrarla, toda mención de cada referencia debe pasar por al menos dos verificadores independientes contra el PDF. Este archivo tiene solo la verificación propia.

**Siglas:**
- **SEN:** Sistema Eléctrico Nacional.
- **PELP:** Planificación Energética de Largo Plazo.
- **PJM:** operador de la red del Atlántico medio de EE. UU.
- **IJEPES:** International Journal of Electrical Power & Energy Systems.
- **EPRG:** Energy Policy Research Group, Universidad de Cambridge.
- **NESO:** operador del sistema británico.
- **TNUoS:** cargos por uso de la red de transmisión británica.
- **HVDC:** corriente continua de alta tensión.
- **BAU, FLEX e ILA:** las estrategias de Onodera et al. Mantener la ubicación actual, elegirla libremente, o elegirla con evaluación integrada de sitios.
