# Validación

Cada fase del trabajo la revisó al menos un agente independiente de quien la hizo. Los revisores recalcularon con código propio, desde las fuentes (archivos de AMEBA, código de Switch, láminas del curso), en vez de reutilizar los scripts revisados. Las dos traducciones con más juicio, la ubicación de los data centers de la PELP 2028–2032 y el escenario propio, se hicieron dos veces por separado y se compararon. Cada hallazgo se corrigió o quedó declarado como limitación en [DATOS_Y_SUPUESTOS.md](DATOS_Y_SUPUESTOS.md).

**Inicio en 2025.** Las fases 1 a 7 se hicieron con la versión del modelo que partía en 2026 y tomaba como existentes las inversiones que AMEBA decidió hasta 2025. El 17-nov-2026 el modelo pasó a partir en 2025, con siete períodos (2025, 2027, 2030, …, 2050) y sin ninguna inversión de AMEBA como dato. La sección 8 resume las autocomprobaciones de la traducción con el inicio en 2025. Las comprobaciones de resultados de las fases 6 y 7 se repitieron sobre las 9 corridas nuevas, salvo la réplica de AMEBA.

Siglas: PELP, Planificación Energética de Largo Plazo; AMEBA, modelo con que se hizo la PELP 2023–2027; CEN, Coordinador Eléctrico Nacional; DC, data centers; ENS, energía no suministrada; VP, valor presente a 2025; HVDC, enlace de corriente continua Kimal–Alto Jahuel; KKT, condiciones de optimalidad de Karush-Kuhn-Tucker; CMg, costo marginal; FP, factor de planta; FV, fotovoltaica; BESS, sistema de almacenamiento en baterías.

## Resumen

| Fase | Qué se comprobó | Resultado | Correcciones principales |
|---|---|---|---|
| 1. Auditoría de datos de la PELP | Cifras y método del análisis previo de ambas PELP | Cifras reproducidas; un error de contabilidad | Contabilidad de anualidades; declarar el sesgo del transporte |
| 2. Formulación | Ejemplo de la Clase 8 en Switch; 6 afirmaciones sobre el código; 12 ecuaciones contra las láminas | Clase 8 reproducida exacta; 6 de 6 y 12 de 12 correctas | Topes de transmisión acumulados por período; reserva propia; 31 zonas |
| 3. Traducción y datos | Cada entrada de Switch contra los datos crudos de AMEBA | Diferencias de 0,000 % en demanda, costos, perfiles, hidro y red | Clases de recurso eólicas. Las inversiones AMEBA de 2025, que esta fase agregó como existentes, se quitaron con el inicio en 2025 |
| 4. Módulos propios | 25 casos mínimos con respuesta a mano; código línea por línea | 63 de 63 comprobaciones | Control del caso base; impuesto al CO₂ promedio; salida de duales |
| 5. Escenarios de DC | Doble traducción independiente | Resultados idénticos | — |
| 6. Resultados | Consistencia interna, réplica de AMEBA, optimalidad de la ubicación | Inicio 2026: consistentes; réplica razonable. Inicio 2025: consistentes; ubicación óptima en los 4 escenarios | Ubicación fija antes de 2030; script de resultados |
| 7. Comparaciones | Costos, ahorros y restricciones de las 9 corridas | Inicio 2026: coinciden a 10⁻¹¹. Inicio 2025: coinciden a 10⁻¹¹ | Tabla de ubicación |
| 8. Inicio en 2025 | Autocomprobaciones de cada parte de la traducción con siete períodos | Demanda, capacidad térmica, hidro y transmisión iguales a AMEBA | Sin inversiones AMEBA como dato; BESS «ley» candidatas; topes de FV y eólica en 2025 |

---

## 1. Auditoría de los datos de la PELP

Antes de modelar se auditaron las entradas y salidas de la PELP 2023–2027 (AMEBA) y de la PELP 2028–2032 (PyPSA-CL), y cómo representan los data centers. Dos agentes la verificaron:

- **Recálculo independiente.** Con código propio y sin ver los scripts de la auditoría, reprodujo los costos de los 5 escenarios de la PELP 2028–2032 (diferencias < 0,01 %), la congestión corredor por corredor y las tres cargas de data centers. Encontró un conteo de corredores errado (324 en vez de 323) y 7 cargas que la propia PELP no carga por un error de nombres.
- **Revisión de método y código.** Encontró un error de contabilidad: las anualidades de inversión se cortaban al final de cada época, lo que subestimaba el costo total unas 2,5 veces. Se corrigió. Además mostró, con los flujos de la propia PELP, que un modelo de transporte deja pasar 20–40 % más de flujo norte → centro que el flujo DC. Esa limitación quedó declarada.

## 2. Formulación

Se validó la formulación del modelo frente al curso y frente al código de Switch 2.0.9.

**Qué se comprobó:**

- **Ejemplo de la Clase 8 en Switch.** Cuatro variantes: sin descuento, con descuento al 7 %, con la inversión como O&M fijo y con ENS. Detalle en [FORMULACION.md](FORMULACION.md), sección 9.
- **Seis afirmaciones sobre el código de Switch**, cada una con un caso mínimo resuelto.
- **Doce ecuaciones** de la formulación contra las láminas de las Clases 4, 5, 8, 12 y 13, leídas desde los archivos de las presentaciones.

**Qué se encontró:**

- **Clase 8.** Se reproduce exactamente en las cuatro variantes: nuclear 7.086, carbón 1.918, gas 2.165 y petróleo 0 MW. Los precios por bloque (109,20; 27,52 y 12,56 USD/MWh) cumplen las condiciones de inversión de la Clase 8. Esto confirma también la fórmula de los precios nodales, incluso con descuento.
- **Seis afirmaciones correctas**, con estos matices:
  - si dos tramos unen las mismas zonas, Switch despacha solo con el primero y cobra ambos; si el segundo es un candidato, nunca se construye; si está escrito en sentido inverso, Switch se detiene;
  - dos reglas de reserva del módulo básico fallan, y el tope de reserva por unidad del módulo avanzado está declarado pero no implementado;
  - la reserva nativa exige el módulo de compromiso de unidades;
  - Switch cobra la anualidad de la transmisión existente;
  - las anualidades se cortan al final del horizonte; equivale a un valor residual solo si la tasa de interés es igual a la de descuento, lo que aquí se cumple.
- **Doce de doce ecuaciones coinciden**, salvo diferencias de notación.
- **Omisiones de la formulación inicial:**
  1. los topes de transmisión deben ser acumulados y por período, con obras comprometidas con fecha;
  2. dos pares de AMEBA tienen tramos escritos en ambos sentidos;
  3. en AMEBA, 17 de 38 tramos existentes tienen una reactancia de 0,2 que parece un valor por omisión, y el HVDC figura como línea alterna: un flujo DC con esas reactancias podría ser peor que el transporte;
  4. si se usara la reserva nativa: sin archivo de capacidades, todos los proyectos dan reserva, incluidas FV y baterías; y el requerimiento proporcional a la demanda no ve la carga de DC;
  5. menores: la red tiene 31 zonas y no ~26; faltaba la disponibilidad en la restricción de reserva; el divisor para pasar a costo horario es 8.760 y no 8.766; la eficiencia del almacenamiento escala el estado de carga.

**Qué se corrigió:**

- Módulo `limites_transmision`, con máximo acumulado y mínimo incremental.
- Corredores que suman los tramos paralelos sin importar su sentido.
- Módulo `reserva_simple`, en vez de la reserva nativa.
- 31 zonas y divisor de 8.760 h.
- Energía de almacenamiento traducida como energía entregable.

El flujo DC no se programó, por el problema de las reactancias (punto 3): el transporte quedó declarado como limitación.

## 3. Traducción y datos

**Traducción con autocomprobación.** La traducción de AMEBA a Switch se hizo en cinco partes por separado, con una especificación común: demanda; térmica; FV, eólica y CSP; hidro y almacenamiento; transmisión y reserva. Cada parte trae autocomprobaciones contra las salidas de AMEBA. Por ejemplo, la demanda reconstruye el balance de cada barra de la solución AMEBA y cierra con residuo menor que 10⁻⁹ MW.

**Validación independiente.** Un agente recalculó cada entrada del caso `PELP_E2` desde los archivos crudos de AMEBA. Usó las tablas de correspondencia unidad → proyecto solo para saber qué agrupa cada proyecto, y antes verificó que fueran coherentes.

| Punto | Resultado | Diferencia máxima |
|---|---|---|
| Demanda | `loads.csv` reproduce la demanda que AMEBA abasteció, por año y por zona; H₂ y NH₃ sin doble conteo | 0,000 %; ≤ 0,14 MWh/año por zona |
| Capacidad existente | Igual a la flota AMEBA no candidata en 498 celdas (año, clase, zona), incluido el cierre del carbón | 0,0 % |
| Costos | 343 candidatos y 1.880 pares (proyecto, período): inversión, O&M fijo, años permitidos, límites y vida; costo variable de 276 térmicas × 6 años | 0,000 %; 0,0006 USD/MWh |
| Perfiles | FV, eólica e hidro candidata idénticos a los crudos | 0,000 % |
| Transmisión | 34 corredores, capacidad existente, obras comprometidas, topes por período y costo por MW | 0,0 % |
| Hidro | Energía anual igual a la generación AMEBA neta, por zona y mes | 0,00 % |
| Almacenamiento | Potencia, energía entregable, eficiencia, razón energía/potencia y disponibilidad | 0,0 % |
| Data centers | Totales por período iguales al resumen de escenarios | redondeo a 0,1 MW |
| Integridad | Reglas de carga de Switch y de los módulos propios | 65 de 66 comprobaciones; el aviso restante es inocuo |

**Qué se encontró:**

1. **Faltaban las inversiones que AMEBA hizo en 2025:** 3.000 MW FV, 1.000 MW eólicos y 2.672 MW de transmisión. Switch las volvía a decidir en 2026, por 3.462 MUSD.
2. **Agrupar los candidatos eólicos bajaba el FP de lo que AMEBA construyó**, hasta −7,5 % en 2030: el grupo promediaba los mejores sitios con los peores.
3. Los enlaces hacia las barras de H₂ y NH₃ no están (unos 995 MUSD de AMEBA).
4. La CSP opera con un horario fijo.
5. La hidro de pasada queda casi plana.
6. Menores: etiquetas de tecnología, fecha de una obra comprometida y regla de vida útil que obliga a usar `--retire late`.

**Qué se corrigió:**

- (1) Las inversiones de 2025 pasaron a existentes. Con el inicio en 2025 se revirtió: son una salida de AMEBA, no un dato, y el modelo las decide (sección 8).
- (2) Los candidatos FV y eólicos se partieron en clases de recurso; la energía de lo que AMEBA construyó quedó dentro de ±1 %.
- (3), (4) y (5) quedaron declarados.
- Después se cambiaron tres cosas más: el impuesto al CO₂ pasó al promedio del período (fase 4), se redujo a 6 días típicos y se agregaron las inversiones de 2025. La fase 6 verificó esos cambios:
  - las tablas de 6 días son un subconjunto exacto de las de 12;
  - las clases eólicas conservan el límite de capacidad (diferencia < 2·10⁻¹² MW) y la energía disponible (≤ 2·10⁻⁵ %).

## 4. Módulos propios

Un agente revisó `data_centers`, `reserva_simple` y `limites_transmision` línea por línea, y el uso que hacen de Switch con los datos de `PELP_E2`.

**Qué se comprobó.** Armó 25 casos mínimos con su respuesta calculada a mano: 63 de 63 comprobaciones coinciden, y 3 casos son infactibles a propósito. También contrastó los datos con las reglas de Switch: cosechas y vidas útiles, anualidades, almacenamiento, hidro, impuesto, ENS y combustibles.

**Qué se encontró:**

| | Hallazgo | Qué se hizo |
|---|---|---|
| Alta | En el caso base, el módulo de DC no verificaba que la ubicación sumara el total ni que existiera `dc_base.csv`; el caso podía correr con otra demanda sin aviso. La versión original, que sí imponía la suma, hacía infactible el caso base por una diferencia de redondeo de 10⁻⁴ MW | **Corregido:** en el caso base la suma se omite y una comprobación detiene la corrida si la ubicación no suma el total (±10⁻³ MW), si decrece o si falta el archivo. El total se escribe como la suma exacta de la ubicación redondeada |
| Alta | La herramienta de diagnóstico de infactibilidad de Switch trae un índice fijo de su ejemplo y falla en cualquier otro modelo | No se usa; la infactibilidad se diagnostica con el registro del solver |
| Media | La reserva se aparta de la formulación: sin tope por unidad, la hidro se cuenta desde 0 y el almacenamiento sin mirar su carga. Con unos 13 GW elegibles frente a 551 MW, probablemente nunca ata | Declarado |
| Media | Con `--retire late`, 805 MW de carbón operan 2–3 años más que en AMEBA en el período 2030 | Declarado; afecta igual a ambos casos |
| Media | El impuesto al CO₂ tomaba el valor del año de inicio: 0 en 2026–2029 y 15,8 USD/t en 2035–2039 | **Corregido:** promedio del período |
| Media | El caso libre usa previsión perfecta, y las zonas no tienen tope ni costo de ubicación | Declarado |
| Media | No hay flujo DC | Declarado |
| Baja | Faltaba exportar el dual del total ubicable y el precio de carga plana por zona | **Corregido:** módulo `precios` |
| Baja | `costs_itemized.csv` da el costo de un año, no del período; la transmisión existente es un costo constante | La métrica se calcula con `total_cost.txt` y como diferencia entre casos |
| Baja | Robustez ante datos que hoy no existen (un corredor no ampliable con fila de límites, una hora sin proyectos de reserva) | No aplica a los datos actuales |

La corrida siempre declara `--dc-modo`, porque sin la opción el módulo corre el caso base sin aviso.

## 5. Escenarios de data centers: doble traducción independiente

**Asignación de la PELP 2028–2032 a las zonas.** Dos agentes, de forma independiente, asignaron las tres cargas de DC de la red de 234 nodos a las 31 zonas del modelo, con métodos distintos:

| | Agente A | Agente B |
|---|---|---|
| Método | Distancia geográfica; camino de menor reactancia; reactancia efectiva; reparto de Kron reduciendo la red a las 26 barras | Camino eléctrico de cada nodo; factores de distribución de un flujo DC; distancia; zona en que AMEBA dejó las centrales del mismo nodo |
| El Salto 220 (RM) | Polpaico500 | Polpaico500 |
| Torquemada 110 (Valparaíso) | Quillota500 | Quillota500 |
| Kimal 220 (Antofagasta, N1) | Kimal220 | Kimal220 |

- Ambos marcaron El Salto como caso de frontera con AltoJahuel500, y el posible doble conteo de los data centers existentes.
- El script que arma los escenarios compara las dos tablas (480 filas: 3 cargas × 32 años × 5 escenarios) y se detiene si difieren en más de 10⁻³ MW. No difieren.

**Escenario `PROPIO`.** Dos agentes conciliaron por separado el catastro de solicitudes de conexión al CEN y del SEIA (elaborado por Raúl Ugarte, CENTRA UAI) con el catálogo propio, con las mismas cuatro reglas: existentes, un campus una vez, catálogo y 50 % de utilización.

- Ambos partieron de los 4.233,4 MW del cronograma y llegaron a 19 solicitudes nuevas (3.791 MW) más Cirion SAN2 (20 MW): 3.811 MW, 1.905,5 MW medios.
- Las trayectorias por zona y año coinciden en las 87 filas, sin diferencia.
- Ambos señalaron los mismos casos dudosos: la zona de Lo Aguirre, si Ignis son uno o dos proyectos, y si SC1 y SC2 son uno o dos. El equipo del proyecto los resolvió: AltoJahuel500, dos y dos.
- Ambos notaron que las conexiones existentes (428,4 MW, 214 MW medios) superan los ~99 MW medios que la demanda ya incluye. De ahí salió el llenado de 115,2 MW medios (DATOS_Y_SUPUESTOS.md, sección 8.5).

## 6. Resultados

Un agente validó la primera tanda de corridas (`PELP_E2`, `CEN` y `PELP_N1`, base y libre), resueltas con la versión que partía en 2026 y todavía con ubicación libre desde 2026. Las mismas comprobaciones se repitieron con código propio sobre las 9 corridas con inicio en 2025, desde sus salidas (`load_balance.csv`, `dc_ubicacion.csv`, `cost_components.csv`, `costs_itemized.csv`, `precios_nodales.csv`, `BuildTx.csv`) y sus registros.

**Consistencia interna** (inicio en 2025).

- El balance, rehecho con los términos de `load_balance.csv` (generación, flujo neto, ENS, demanda, carga neta del almacenamiento y carga de DC), cierra a 0,09 MW en las 31.248 celdas zona-hora de cada corrida: un error relativo < 10⁻⁵, el redondeo del archivo.
- La carga de DC de cada zona y hora es la de `dc_ubicacion.csv`, con diferencia ≤ 0,005 MW (redondeo).
- Los componentes de `cost_components.csv` suman el total de `total_cost.txt` con diferencia ≤ 10⁻⁴ USD, y el costo anual de `costs_itemized.csv` por el factor de VP de cada período reproduce el total con error relativo < 2·10⁻¹⁵.
- No hay ENS en ninguna de las 9 corridas, y las 9 terminaron en óptimo.

**Réplica de AMEBA** (`PELP_E2` base). Con el inicio en 2025 el modelo decide también lo que AMEBA construyó en 2024–2025. La comparación con la solución de AMEBA (capacidad FV, eólica y de almacenamiento; transmisión corredor por corredor; emisiones y CMg medio por zona) se hace con sus archivos crudos, que no están en el repositorio, y no se repitió con las corridas nuevas. Las diferencias esperables por formulación son las mismas: períodos representados con los datos de su año de inicio, 6 días, transporte y LP sin compromiso de unidades.

**Optimalidad de la ubicación libre.**

- La condición de FORMULACION.md, sección 5: la zona que recibe la carga es la de menor costo acumulado de abastecerla, y ese costo es igual a la suma de los duales del total ubicable. En la primera tanda se cumplió en los tres escenarios y en todos los períodos con crecimiento. Inicio 2025: se cumple en los 4 escenarios, en las 23 combinaciones de zona y período que reciben crecimiento desde 2030, con diferencia relativa ≤ 3·10⁻⁷.
- Por convexidad, el ahorro está entre $\sum\rho_{\text{libre}}\,(\hat x-x_{\text{libre}})$ y $\sum\rho_{\text{base}}\,(\hat x-x_{\text{libre}})$. Inicio 2025: se cumple en los 4 escenarios, en MMUSD: 175,3 ≤ 179,1 ≤ 183,1 (PELP E2), 470,2 ≤ 499,7 ≤ 529,0 (CEN), 574,4 ≤ 619,7 ≤ 665,7 (PELP N1) y 1.791,5 ≤ 2.401,9 ≤ 2.973,5 (PROPIO).

**Qué se encontró y qué se hizo** (primera tanda, inicio en 2026):

- **Artefacto del primer período.** El caso libre ponía la carga de 2026 en Parinas500 (norte). En el período 2026 el norte está desacoplado: sin HVDC y con Parinas–Cumbre en su tope. Con los CMg anuales de AMEBA, donde ese bolsón dura solo 2026–2028, la mejor zona para instalar en 2026 está en el sur. **Corregido:** la ubicación queda fija antes de 2030 (`--dc-libre-desde 2030`). Con el inicio en 2025 se mantiene: los períodos 2025 y 2027 quedan con la ubicación proyectada.
- **Script de resultados.** El factor de VP salía un 6 % alto y el costo variable por tecnología omitía combustible e impuesto. **Corregido**, con un control que compara la suma por tecnología con los componentes del objetivo. El script toma el año base del VP de `financials.csv`.
- **El sur barato dependía del tope de Ancoa–Charrúa**, en su máximo de ampliación desde 2030, igual que en AMEBA, y de una ventaja pequeña de Nueva Ancud sobre Nueva Puerto Montt. Con el inicio en 2025 se repite: Ancoa–Charrúa está en su tope en las 9 corridas desde 2030 (500 MW ampliados en 2030 y 4.500 MW en 2050), y Río Malleco–Mulchén en 2050 en todas salvo PROPIO libre. En PELP E2, CEN y PELP N1 todo el crecimiento va a Nueva Ancud, con una ventaja de 0,5–1,6 % sobre Nueva Puerto Montt en el costo acumulado. En PROPIO, el crecimiento de 2030 va al sur (Río Malleco, Pichirropulli, Nueva Puerto Montt y Nueva Ancud), y desde 2035, todo a Nueva Ancud.
- **En `PELP_N1`, la carga de DC ubicada en Nueva Ancud dependía de ampliar un enlace radial, sin criterio N−1.** Con el inicio en 2025 se repite en los casos libres de CEN, PELP N1 y PROPIO. Nueva Ancud tiene un solo enlace, Nueva Puerto Montt–Nueva Ancud (660 MW existentes), y en 2050 importa hasta 943 MW (PELP N1), 1.024 MW (CEN) y 2.354 MW (PROPIO). El enlace se amplía también sin data centers, a 3.191 MW en 2050. Declarado.
- **12 días típicos.** La corrida no terminó: la barrera se quedó sin memoria y el simplex no convergió. Se usan 6 días; su efecto sobre los insumos está medido (DATOS_Y_SUPUESTOS.md, sección 2).

## 7. Comparaciones entre casos

Un agente recalculó, con código propio, las tablas de comparación de las 9 corridas: 4 escenarios × (base, libre) más `SIN_DC`, con `--dc-libre-desde 2030`. Con el inicio en 2026 todos los controles se cumplieron, con diferencias del orden de 10⁻¹¹ millones de USD o menores. Los mismos controles sobre las 9 corridas con inicio en 2025:

| Control | Resultado |
|---|---|
| Costos totales, ahorros y costo extra frente a `SIN_DC` | Diferencia máxima 7,3·10⁻¹² millones de USD |
| Descomposición por componente | Diferencia máxima 3,6·10⁻¹² millones de USD |
| Configuración de cada corrida | Modo, `--dc-libre-desde 2030` y `--retire late` correctos en las 9; Gurobi por barrera (`Method=2`) |
| Ubicación libre en 2025 y 2027 = ubicación base, por zona | Diferencia 0 MW en los 4 escenarios |
| Total de DC por período, base = libre | Diferencia ≤ 10⁻³ MW, el redondeo de `dc_ubicacion.csv` |
| Ninguna zona decrece entre períodos | Se cumple |
| `SIN_DC` sin carga de DC | `loads.csv` idéntico byte a byte al de los escenarios; `dc_*.csv` en 0 y carga de DC nula en las 31.248 celdas zona-hora |
| Costo total = suma de componentes | Diferencia ≤ 10⁻⁴ USD |
| Factor de VP y largo de cada período | Igual a la regla de Switch: 2 años en 2025, 3 en 2027 y 5 en los demás. Los días típicos suman 8.760 h por año en cada período, y el costo anual por el factor de VP reproduce el total con error relativo < 2·10⁻¹⁵ |
| Ahorro ≥ 0 | En los 4 escenarios, como debe ser: la ubicación base es factible en el caso libre |

La tabla de ubicación del script de resultados omitía la carga fija de DC; hoy usa la carga total.

## 8. Inicio en 2025: autocomprobaciones de la traducción

El 17-nov-2026 se cambió el inicio del modelo de 2026 a 2025. Los períodos son 2025 (2025–2026), 2027 (2027–2029), 2030, 2035, 2040, 2045 y 2050, y cada uno usa los datos de AMEBA de su año de inicio. Existente es toda unidad de los datos de entrada de AMEBA en servicio el 1-ene-2025; ninguna inversión que decidió AMEBA entra como dato. Cada parte de la traducción repitió sus autocomprobaciones con los siete períodos:

| Parte | Comprobación | Resultado |
|---|---|---|
| Demanda | Energía de `loads.csv` con los pesos de los días típicos frente a la demanda servida + ENS de AMEBA, en los 7 años de datos | 0,000 %; error máximo por bloque y zona de 5·10⁻⁵ MW |
| Térmica | Capacidad existente frente a AMEBA en 2025 (12.363,3 MW) y 2027 (10.746,5 MW) | 0,0 %; disponible neta +0,04 % y +0,05 % |
| Térmica | Identidad del costo variable en las 285 centrales y los 7 años | Se cumple |
| Térmica | Ninguna térmica en el archivo de inversiones de AMEBA | Se cumple |
| FV y eólica | Existentes frente a las unidades AMEBA conectadas, en los 7 años | 0,0 % |
| FV y eólica | FP de los existentes | +0,15 % (FV) y +0,01 % (eólica) |
| FV y eólica | Energía de los candidatos que AMEBA construyó | Dentro de ±1 %, salvo eólica 2025: −6,9 % (−1,7 % en el parque total) |
| Hidro | Energía de 2025 y 2027 frente a la generación AMEBA neta | 0,0 % |
| Almacenamiento | Existente desde 2027 frente a `Capacidad_total.csv` de AMEBA | −3,0 %, el duplicado de Polpaico (60 MW) |
| Transmisión | Inversiones crudas frente a `Transmision_anual.csv`; costo por corredor frente a `Inv_Cost` | 0 MW; 3·10⁻¹⁴ millones de USD |
| Transmisión | La solución AMEBA cabe en los límites de los 7 períodos, y lo que construyó hasta 2025 cabe en el tope de 2025 | Se cumple |

- **Eólica 2025.** Lo que AMEBA construyó ese año es casi solo Pampa Fidelia (915 MW), un sitio con FP 0,484 dentro de una clase de recurso con FP 0,452. Solo afecta la comparación con lo que AMEBA eligió, no la traducción.
- **Almacenamiento existente en 2025.** Con la regla del 1 de enero, 848 MW que AMEBA cuenta en 2025 entran durante ese año y operan en Switch desde el período 2027: el período 2025 tiene 951,8 MW de almacenamiento existente, frente a 1.859,9 MW en AMEBA.
- **Carbón que cierra el 1-ene-2026.** 2.116,8 MW operan en todo el período 2025, también en 2026, cuando AMEBA ya no los tiene; las reconversiones de 2026 (500 MW) operan desde 2027. Es la consecuencia de la regla del 1 de enero con un período de dos años.
- **BESS «ley»** (2.000 MW): candidatas con inversión y O&M fijo 0 desde el período 2027. Con vida de 15 años, construidas en 2027 se retiran en 2042 y pueden reconstruirse sin costo en 2045.
- **Módulo `topes_tecnologia`** (≤ 3.000 MW FV y ≤ 1.000 MW eólicos nuevos en 2025): no pasó por los casos mínimos de la fase 4.

## 9. Lo que no está validado

- **Réplica de AMEBA con el inicio en 2025.** La comparación de capacidad, transmisión, emisiones y CMg con la solución de AMEBA (fase 6) no se repitió con las corridas nuevas.
- **Módulo `topes_tecnologia`.** Tiene la autocomprobación de la parte de FV y eólica, pero no casos mínimos con respuesta a mano como los de la fase 4.
- **`PROPIO` con el llenado de campus conectados.** La parte fija del módulo se probó en los casos mínimos de la fase 4, pero los costos y el ahorro de `PROPIO` no se recalcularon por separado.
- **Flujos y despachos horarios frente a su capacidad.** Los archivos horarios de despacho y flujo no están en el repositorio; con el inicio en 2025 se verificó el balance por zona y hora, no cada flujo ni cada despacho.
- **Si la reserva ata.** No se exportan sus duales.
- **6 frente a 12 días** en los resultados: solo se midió el efecto sobre los insumos.
- **Sensibilidades recomendadas que no se corrieron:**
  - vida útil con `--retire mid`;
  - El Salto o Lo Aguirre en la otra zona de Santiago;
  - flujo DC en la red existente.
- **Salidas de AMEBA que se siguen usando como dato** (pendientes documentados): la energía hidro por día típico, el perfil del consumo de H₂ y NH₃, y el factor 1,031 de la demanda.
- **Supuestos sin confirmación en las fuentes:**
  - el origen del factor 1,031 de la demanda;
  - la unidad del O&M fijo de AMEBA (confianza media);
  - que la demanda de la PELP 2023–2027 incluya los ~99 MW medios de DC existentes.
