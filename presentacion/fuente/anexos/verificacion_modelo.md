# Verificación de `40_modelo.js`

Cada afirmación de las tres láminas de anexo se mapea a su sección en los documentos del estudio (`ubicacion-datacenters-sen\docs\`):

- **F** = `FORMULACION.md`;
- **D** = `DATOS_Y_SUPUESTOS.md`;
- **V** = `VALIDACION.md`.

**Comprobación automática** (script temporal de la sesión del 17-nov, no guardado en esta carpeta; `node -e "console.log(require('./40_modelo.js').length)"` da 3):

- extrae las 85 cifras distintas del módulo (títulos, tablas, viñetas, textos y notas) y busca cada una, literal, en los tres documentos: todas aparecen;
- revisa largos de título y subtítulo, suma de anchos, caracteres por pulgada de cada celda y alto estimado de cada columna: 0 problemas.

La búsqueda literal no prueba que la cifra esté en el contexto correcto. Eso se revisó a mano en las tablas de abajo.

---

## Lámina 1. Anexo: decisiones del modelo

| Fila / afirmación | Lo que dice la lámina | Fuente |
|---|---|---|
| Inversión: decisión | Cuánto construir de cada candidato, dónde y cuándo | F §1 ($x_{g,v}$ por proyecto y cosecha; proyectos por zona $G_z$); F §4.2 (cosechas admisibles) |
| Inversión: dato | Candidatos de la PELP con costo, tope y primer período | F §1 ($c^{ov}$, $FOM$, $\bar X_g$); F §4.2 («así se fija desde qué período puede entrar cada candidato»); D §4 |
| Transmisión: decisión | MW por corredor y período, en forma continua | F §4.5 («La ampliación $T_{k,y}$ es continua y de costo lineal») |
| Transmisión: dato | 34 corredores; costo, topes acumulados, obras comprometidas | D §6 («161 líneas de AMEBA quedan en 34 corredores»; topes acumulados; obras comprometidas); F §4.5 ($T_{k,y}=0$ fuera de $\mathcal L$) |
| Despacho: decisión | Generación y flujos entre zonas, hora a hora | F §1 ($p_{g,t}$, $f_{m\to n,t}$) |
| Despacho: dato | Disponibilidad de cada central; 6 días típicos de 24 h | F §1 ($\alpha_g$); F §2 («6 días típicos de 24 horas consecutivas»); D §2 |
| Almacenamiento: decisión | Carga, descarga y energía almacenada; ciclo diario | F §1 ($c_{s,t}$, $e_{s,t}$); F §4.3 («El ciclo se cierra cada día típico») |
| Almacenamiento: dato | Eficiencia y duración fija de cada proyecto | F §1 ($\eta_s$, $h_s$); D §5.2 («Duración fija») |
| ENS: decisión | ENS por zona y hora, también de data centers | F §4.7 («cubre también la carga de data centers») |
| ENS: dato | VOLL de 650 USD/MWh, el de AMEBA | D §7 («650 USD/MWh, el VOLL de AMEBA») |
| Data centers: decisión | Caso libre: zona del crecimiento desde 2030 (26 barras) | F §5 («el modelo solo decide dónde va el crecimiento desde 2030»); F §1 ($Z^{\mathrm{DC}}$: las 26 barras eléctricas) |
| Data centers: dato | Caso base: zona proyectada; siempre: MW medios por período | F §5 (caso base $x=\hat x$; «su total por período $D^{\mathrm{DC}}_y$ es un dato»); D §8.2 |
| Demanda | Carbono Neutralidad × 1,031, con H₂ y NH₃; inelástica | D §3 (fórmula de $D_{z,t}$); D §1 (variante `rumbo_CN`); F §8 («Demanda inelástica con VOLL») |
| Costos y combustibles | Inversión, O&M y combustibles de AMEBA; tasa de 6 % | D §1 (variantes `Medio` y `PComb_Ref`; unidades); D §4.1; D §7 («Tasa de descuento e interés de 6 %») |
| Perfiles: decisión | Recorte renovable; reparto horario de la hidro en el día | F §4.2 ($0\le p_{g,t}\le\alpha_g\kappa_{g,t}X_{g,y}$: puede despachar bajo el perfil); D §4.3 («Switch solo puede recortar»); D §5.1 («la hidro puede mover su energía dentro del día, pero no entre meses») |
| Perfiles: dato | Perfiles de cambio climático; hidro mensual de AMEBA | D §1 (`climate_change_projections`, MIROC-ESM-CHEM); D §5.1 (energía que AMEBA despachó ese mes) |
| Impuesto al CO₂ | Promedio por período: 2,5; 10; 23,48; 35; 35 y 35 USD/t | D §7 |
| Reserva: decisión | Holgura de los proyectos elegibles, hora a hora | F §4.6 (holgura de los elegibles ≥ requerimiento; «No hay variables nuevas») |
| Reserva: dato | Subida 551 MW y bajada 407 MW; 104 proyectos elegibles | D §7 |
| Texto | Base y libre: misma red, días y horizonte | F §7 («Los dos casos usan la misma red, los mismos días y el mismo horizonte») |
| Texto | Sin data centers no agrega carga de data centers | D §8.6; V §7 (demanda idéntica byte a byte) |
| Fuente | Ministerio de Energía (2025, 2026a), CEN (2026a), CEN (s. f.) | D §1 (fuentes) |

**Notas del orador:**

| Afirmación | Fuente |
|---|---|
| Lo construido por AMEBA hasta 2025 entra como existente, sin costo, y se descuenta del potencial | D §4 |
| Lineal, sin compromiso de unidades: sin mínimos técnicos, rampas ni partidas | F §4.2 |
| Topes = suma de candidatos disponibles hasta el período | D §6 |
| HVDC Kimal–Alto Jahuel 2.000 MW y Río Malleco–Pichirropulli 660 MW, en 2030 | D §6; F §4.5 |
| Zonas candidatas: 26 barras, no los 5 polos; sin tope ni costo de conexión o terreno | D §8.2; F §5 |
| Antes de 2030: sitio y solicitud de conexión; período 2026 sin HVDC | F §5 |
| Se supone que la demanda incluye ~99 MW medios existentes; se agrega lo que supera ese nivel | D §8.1 |

---

## Lámina 2. Anexo: adaptaciones de los datos de la PELP

| Viñeta | Fuente |
|---|---|
| 6 días típicos (meses impares) en vez de 12; con 12, la barrera de Gurobi sin memoria en 63 GB | D §2 («Por qué 6 y no 12 días»); V §6 |
| Impuesto al CO₂ promedio del período (2,5 a 35 USD/t), no el del año de inicio, porque cambia los precios relativos entre zonas | D §7 («Como el impuesto cambia los precios relativos entre zonas…»); V §4 |
| Demanda × 1,031: AMEBA abastece 1,031 × la serie en todas las barras; margen de pérdidas (hipótesis) | D §3 («Factor 1,031»); V §8 (origen sin confirmar) |
| Generación neta de servicios auxiliares (entre 2,0 y 2,6 % de la bruta), porque el balance de AMEBA solo cierra en neto | D §4 («Regla común») |
| Lo construido por AMEBA hasta 2025 (3.000 MW FV, 1.000 MW eólicos, 92,1 MW de baterías, 2.672 MW de transmisión) entra como existente; el modelo parte en 2026 | D §4 («Inversiones de AMEBA hasta 2025: existentes»); V §3, hallazgo 1 |
| Hidro existente: energía fija por día típico, la que AMEBA despachó ese mes; los días típicos no se conectan | D §5.1; F §2 («Los días típicos no se conectan entre sí»); F §4.4 |
| CSP como generador variable con perfil fijo; como almacenamiento, Switch la cargaría desde la red | D §4.3 |
| Baterías con energía entregable (nominal × eficiencia de descarga); Switch aplica la eficiencia a la carga; 4 h → 3,84 h | D §5.2; F §4.3 |
| Reserva simplificada (551/407 MW) sin tope por unidad; la nativa de Switch exige compromiso de unidades | D §7; F §4.6 («La reserva nativa de Switch no sirve aquí…»); V §2 |
| Transporte sin pérdidas en 34 corredores, sin flujo DC; 17 de 38 tramos con reactancia que parece valor por omisión | D §6; F §4.5; V §2 (omisión 3 y «El flujo DC no se programó, por el problema de las reactancias») |

**Notas del orador:**

| Afirmación | Fuente |
|---|---|
| Meses conservados; cada uno representa al siguiente; 144 h/año, como la PELP 2028–2032 | D §2 |
| Simplex dual sin converger a los 110 minutos | D §2 |
| Efecto de 6 días: demanda −0,04 a −0,09 %; hidro +4,9 / +4,6 / +6,6 / −1,8 %; FP eólico −5,3 % en 2035 | D §2 |
| CO₂ en AMEBA: 0 hasta 2027, 5 desde 2028, 35 desde 2040; 15,8 vs 31,1 en 2035 | D §7 |
| 1,031 no figura en entradas; se halló rehaciendo el balance; AMEBA con pérdidas nulas | D §3 |
| H₂ y NH₃ como carga fija en la barra eléctrica, con el flujo horario de AMEBA | D §3 |
| 2.000 MW de baterías «ley» como comprometidos | D §4 |
| Sin CSP nueva en AMEBA; Cerro Dominador 110 MW | D §4.3 |
| Primaria 331/85 MW y secundaria 220/322 MW, sumadas; 104 proyectos | D §7 |
| Clases de recurso: −7,5 % sin ellas, ±1 % con ellas | D §4.2; V §3 |
| HVDC (2.000 MW, enero de 2029 en AMEBA) entra en el período 2030 | D §6 |
| Líneas paralelas sumadas en un corredor | D §6 |

---

## Lámina 3. Anexo: validación

| Afirmación | Fuente |
|---|---|
| Tabla de la traducción: demanda 0,000 %; capacidad existente 498 celdas 0,0 %; 343 candidatos y 1.880 pares 0,000 %; costo variable 276 térmicas × 6 años 0,0006 USD/MWh; perfiles 0,000 %; transmisión 34 corredores 0,0 %; hidro por zona y mes 0,00 %; almacenamiento 0,0 % | V §3, tabla |
| Un agente independiente recalculó cada entrada desde los datos crudos de AMEBA, con código propio | V §3 («Validación independiente»); V introducción |
| Réplica de AMEBA: misma capacidad térmica, hidro y existente; FV −15 %, eólica +4 % en 2030; ±3 % en 2050 | V §6 («Réplica de AMEBA») |
| Módulos propios: 25 casos mínimos, 63 de 63 comprobaciones | V §4 |
| Clase 8: nuclear 7.086, carbón 1.918, gas 2.165, petróleo 0 MW en la lámina y en Switch | F §9 («Resultado»); V §2 |
| Igual en las 4 variantes | F §9 (variantes A–D) |
| Precios por bloque 109,20; 27,52 y 12,56 USD/MWh; cumplen la condición de inversión de la Clase 8 | F §9; V §2 |
| LP de 1,35 millones de restricciones, 1,18 millones de variables y 6,9 millones de coeficientes | F §10 |
| Gurobi, barrera y crossover, 5 o 6 hilos: 8 a 16 min por corrida | F §10 |
| 12 días: 2,68 millones de restricciones; barrera sin memoria en 63 GB | D §2 |

**Notas del orador:**

| Afirmación | Fuente |
|---|---|
| Cada fase revisada por al menos un agente independiente, con código propio | V introducción |
| La tabla es del caso E2; costo variable = precio × tasa de calor + O&M variable; contenido de «costos de candidatos» | V §3; D §1 |
| Réplica: transmisión −2 % (2030) y +8 % (2050); emisiones +8–34 %; CMg +2–8 USD/MWh; causas | V §6 |
| Cuatro variantes de la Clase 8 (ENS a 1.000 USD/MWh) | F §9 |
| 12 de 12 ecuaciones contra las Clases 4, 5, 8, 12 y 13 | V §2 |
| Lo no validado: escenario propio con llenado; optimalidad solo en la primera tanda; si la reserva ata; 6 vs 12 días solo en insumos | V §8; V §6 |
