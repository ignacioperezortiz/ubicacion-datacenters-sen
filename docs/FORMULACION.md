# Formulación del modelo

El modelo es Switch 2.0.9: un programa lineal (LP) de expansión de generación, almacenamiento y transmisión en varios períodos, con cinco módulos propios en `modulos/`. Aquí se escribe en la notación del curso «Economía, Resiliencia y Mercados Energéticos». Hay dos cambios para evitar choques de símbolos:

- el período de inversión se indexa con $y$, porque en el curso $p$ es potencia producida;
- todo lo de data centers lleva el superíndice $\mathrm{DC}$, porque en el curso $x$ es la inversión en generación.

Siglas: VP, valor presente; ENS, energía no suministrada; VOLL, valor de la carga perdida; CRF, factor de recuperación de capital; O&M, operación y mantenimiento; PDGE, polos de desarrollo de generación eléctrica; HVDC, enlace de corriente continua en alta tensión; BESS, sistema de almacenamiento en baterías; FV, fotovoltaica; AMEBA, modelo con que se hizo la PELP 2023–2027; PELP, Planificación Energética de Largo Plazo.

Los valores de cada parámetro y su origen están en [DATOS_Y_SUPUESTOS.md](DATOS_Y_SUPUESTOS.md). Cómo se validó, en [VALIDACION.md](VALIDACION.md).

---

## 1. Conjuntos, variables y parámetros

| Símbolo | Significado | Componente de Switch o archivo |
|---|---|---|
| $y\in Y$ | período de inversión: 2025 (2025–2026), 2027 (2027–2029), 2030, 2035, 2040, 2045 y 2050 (2050–2054); $s_y$ es su año de inicio y $L_y$ su largo en años | `PERIODS`, `periods.csv` |
| $\mathcal Q\subseteq\Theta\times Y$ | pares (tecnología, período) con tope de inversión; $G_\theta$ son los proyectos de la tecnología $\theta$ | `topes_tecnologia.csv`, `GENS_BY_TECHNOLOGY` |
| $d\in\mathcal D_y$ | día típico del período (6 por período) | `TIMESERIES` |
| $t\in T_d$; $T_y$ | hora del día típico (24); horas del período $y$. $y(t)$ es el período de $t$ y $t^-$ la hora anterior, circular dentro del día | `TIMEPOINTS`, `tp_previous` |
| $\Delta T_t$ | horas del año que representa la hora $t$ | `tp_weight_in_year` |
| $z\in Z$ | zona: 26 barras eléctricas y 5 polos PDGE | `LOAD_ZONES` |
| $g\in G$; $G_z$ | proyecto de generación o almacenamiento, existente o candidato; los de la zona $z$ | `GENERATION_PROJECTS` |
| $S\subseteq G$; $H\subseteq G$ | almacenamiento; hidro con energía fija por día | `STORAGE_GENS`, `HYDRO_GENS` |
| $G^R\subseteq G$ | proyectos que dan reserva | `reserva_elegibles.csv` |
| $k=(m,n)\in K$ | corredor de transmisión entre las zonas $m$ y $n$ (tramos paralelos sumados) | `TRANSMISSION_LINES` |
| $Z^{\mathrm{DC}}\subseteq Z$ | zonas candidatas para data centers: las 26 barras eléctricas | `dc_candidatas.csv` |

**Variables** (todas $\ge 0$):

| Símbolo | Significado | Switch |
|---|---|---|
| $x_{g,v}$ | MW construidos del proyecto $g$ en la cosecha $v$ | `BuildGen` |
| $X_{g,y}$ | capacidad en servicio en el período $y$ (expresión) | `GenCapacity` |
| $p_{g,t}$ | despacho; en almacenamiento, descarga | `DispatchGen` |
| $c_{s,t}$; $e_{s,t}$ | carga y energía almacenada | `ChargeStorage`, `StateOfCharge` |
| $sp_{h,t}$ | vertimiento hidro | `SpillHydro` |
| $ls_{z,t}$ | ENS | `UnservedLoad` |
| $f_{m\to n,t}$ | flujo dirigido de $m$ a $n$ | `DispatchTx` |
| $T_{k,y}$; $F_{k,y}$ | ampliación del corredor en el período $y$; capacidad total (expresión) | `BuildTx`, `TxCapacityNameplate` |
| $x^{\mathrm{DC}}_{z,y}$ | carga ubicable de data centers en la zona $z$, en MW medios | `DCUbicado` (módulo `data_centers`) |

**Parámetros:**

| Símbolo | Significado | Archivo |
|---|---|---|
| $r$; $i$; $y_0$ | tasa de descuento y de interés (6 %); año base del VP (2025) | `financials.csv` |
| $B_y$ | factor que lleva un costo anual constante del período $y$ a VP | calculado por Switch |
| $c^{ov}_{g,v}$; $FOM_{g,v}$ | costo de inversión (USD/MW) y O&M fijo (USD/MW-año) | `gen_build_costs.csv` |
| $\ell_g$ | vida útil | `gen_info.csv` |
| $VOM_g$; $HR_g$; $c^{f}_{g,y}$ | O&M variable (USD/MWh), tasa de calor y precio del combustible | `gen_info.csv`, `fuel_cost.csv` |
| $\phi_f$; $\tau^{\mathrm{CO_2}}_y$ | intensidad de CO₂ del combustible; impuesto (USD/t) | `fuels.csv`, `carbon_policies.csv` |
| $\alpha_g$ | disponibilidad: $1-$ tasa de falla forzada equivalente | `gen_info.csv` |
| $\kappa_{g,t}$ | perfil de recurso de FV, eólica, CSP e hidro candidata; 1 en el resto | `variable_capacity_factors.csv` |
| $\bar X_g$ | potencial máximo del proyecto | `gen_info.csv` |
| $D_{z,t}$ | demanda, que ya incluye los data centers existentes | `loads.csv` |
| $VOLL$ | costo de la ENS (650 USD/MWh) | `lost_load_cost.csv` |
| $F^0_k$; $c^{T}_k$ | capacidad existente (MW) y costo de inversión del corredor (USD/MW) | `transmission_lines.csv` |
| $\underline T_{k,y}$; $\bar T_{k,y}$ | obra comprometida que entra en $y$; ampliación acumulada máxima hasta $y$ | `trans_build_limits.csv` |
| $\bar N_{\theta,y}$ | MW nuevos máximos de la tecnología $\theta$ en el período $y$, sumando todas las zonas | `topes_tecnologia.csv` |
| $\eta_s$; $h_s$ | eficiencia de ida y vuelta; razón energía/potencia | `gen_info.csv` |
| $A_{h,d}$; $\underline P_{h,d}$ | potencia media y mínima de la hidro en el día $d$ | `hydro_timeseries.csv` |
| $R^{+}_y$; $R^{-}_y$ | reserva de subida y de bajada | `reserva_requerimiento.csv` |
| $\bar D^{\mathrm{DC}}_{z,y}$ | carga fija de data centers (no reubicable) | `dc_fijo.csv` |
| $D^{\mathrm{DC}}_y$ | total ubicable del período | `dc_libre.csv` |
| $\hat x^{\mathrm{DC}}_{z,y}$ | ubicación proyectada de la carga ubicable | `dc_base.csv` |
| $\bar X^{\mathrm{DC}}_z$; $c^{\mathrm{DC}}_z$ | tope y costo anual por MW de ubicar en la zona (en este estudio, sin tope y 0) | `dc_candidatas.csv` |

---

## 2. Tiempo y descuento

Cada período tiene 6 días típicos de 24 horas consecutivas. El peso de cada hora es

$$
\Delta T_t=\tau_t\,\frac{\sigma_{d(t)}}{L_{y(t)}}\quad[\text{h/año}],\qquad \sum_{t\in T_y}\Delta T_t=8.760,
$$

con $\tau_t=1$ h y $\sigma_d$ = `ts_scale_to_period`, el número de veces que el día se repite en el período. Cada día típico es el de un mes impar y representa también al mes siguiente: $\sigma_d$ = (días del mes + días del mes siguiente) × $L_y$. Por ejemplo, el día de enero de 2030 vale $(31+28)\times 5=295$ y cada una de sus horas pesa 59 h/año. Febrero tiene siempre 28 días, como en AMEBA.

- Los días típicos no se conectan entre sí. Almacenamiento e hidro cierran su ciclo dentro de cada día.
- Demanda y perfiles son los mismos en todos los años de un período.
- $L_y$ es 2 en el período 2025, 3 en el 2027 y 5 en los demás.
- Cada período usa los datos de AMEBA de su año de inicio.

El factor de VP de un costo anual constante del período es

$$
B_y=\frac{1-(1+r)^{-L_y}}{r}\,(1+r)^{-(s_y-y_0)},
$$

que da 1,8334; 2,3790; 3,1477; 2,3522; 1,7577; 1,3134 y 0,9815 para 2025, 2027, …, 2050.

**Frente al curso.** $\Delta T_t$ cumple el papel de $\Delta T_j$ de la Clase 8, pero los bloques son horas cronológicas y no tramos de la curva de duración. Así se conservan la secuencia del día (almacenamiento, solar) y la coincidencia horaria entre zonas.

---

## 3. Función objetivo

$$
\min\ C=\sum_{y\in Y}B_y\Bigg[\sum_{g\in G}\sum_{v\in\mathcal V_{g,y}}\big(I_{g,v}+FOM_{g,v}\big)x_{g,v}+\sum_{k\in K}I^{T}_k\,F_{k,y}+\sum_{z\in Z^{\mathrm{DC}}}c^{\mathrm{DC}}_z\,x^{\mathrm{DC}}_{z,y}+\sum_{t\in T_y}\Delta T_t\Big(\sum_{g\in G}\big(MC_{g,y}+\tau^{\mathrm{CO_2}}_y\,\varepsilon_g\big)p_{g,t}+VOLL\sum_{z\in Z}ls_{z,t}\Big)\Bigg]
$$

- **Inversión.** $I_{g,v}=c^{ov}_{g,v}\,CRF(i,\ell_g)$ en USD/MW-año, con $CRF(i,n)=\dfrac{i}{1-(1+i)^{-n}}$. Los existentes tienen $c^{ov}=0$ y solo pagan O&M fijo. El costo de conexión es 0. En almacenamiento todo el costo va por MW (el costo por MWh es 0).
- **Costo variable.** $MC_{g,y}=VOM_g+HR_g\,c^{f}_{g,y}$, en USD/MWh neto.
- **Emisiones.** $\varepsilon_g=HR_g\,\phi_{f(g)}$, en tCO₂/MWh. El costo es emisiones anuales × impuesto del período (módulo `carbon_policies`). El impuesto de cada período es el promedio de sus años: 0; 3,33; 10; 23,48; 35; 35 y 35 USD/t para 2025, 2027, …, 2050.
- **Transmisión.** $I^{T}_k=c^{T}_k\,CRF(i,40)$, sin O&M, y $F_{k,y}=F^0_k+\sum_{v\le y}T_{k,v}$. Es la estructura $VATT=AVI+COMA$ de la Clase 13, con $COMA=0$.
- **Cosechas vivas.** $\mathcal V_{g,y}$ son las cosechas de $g$ en servicio en $y$ (sección 4.2).

En Switch, los términos por período son `TotalGenFixedCosts`, `TxFixedCosts`, `EmissionsCosts` y `DCCostoAnual`; los términos por hora, `FuelCostsPerTP`, `GenVariableOMCostsInTP` y `UnservedLoadPenalty`.

**Horizonte.** No hay valor terminal: cada cosecha paga su anualidad solo en los períodos del horizonte en que está viva. Como $i=r$, esto equivale a acreditar como valor residual el VP de las anualidades que quedan después de 2054.

**Constantes.** Switch cobra la anualidad de toda la capacidad de transmisión, también la existente y la comprometida, que no son decisiones: unos 176 MUSD/año en 2025–2029 y 266 MUSD/año desde 2030, cuando entran el HVDC Kimal–Alto Jahuel y Río Malleco–Pichirropulli. Lo mismo pasa con el O&M fijo del almacenamiento y la CSP existentes. Son iguales en todos los casos y se cancelan en las diferencias de costo.

**Frente al curso.** Con un solo período de un año, $B_y$ es una constante; dividiendo por 8.760 h, $I_{g,v}/8.760$ es el costo horario de inversión $I_i$ de la Clase 8 y $\Delta T_t/8.760$ la fracción de tiempo $\Delta T_j$. El objetivo es entonces el del modelo de expansión con demanda inelástica y VOLL (VOLLP, Clase 8), al que se suman la transmisión co-optimizada (Clase 13) y el impuesto al CO₂.

---

## 4. Restricciones

### 4.1 Balance por zona y hora

$$
\sum_{g\in G_z}p_{g,t}+\sum_{m}f_{m\to z,t}-\sum_{n}f_{z\to n,t}+ls_{z,t}=D_{z,t}+\sum_{s\in S\cap G_z}c_{s,t}+\bar D^{\mathrm{DC}}_{z,y(t)}+x^{\mathrm{DC}}_{z,y(t)}\qquad(\rho_{z,t})\quad\forall z,t
$$

Es el balance nodal de las Clases 4 y 5 con demanda inelástica. La carga de data centers entra como un retiro más (`DCCarga` en `Zone_Power_Withdrawals`): es plana, el mismo valor en todas las horas del período.

### 4.2 Generación

$$
\begin{aligned}
& X_{g,y}=\sum_{v\in\mathcal V_{g,y}}x_{g,v},\qquad x_{g,v}=\bar x_{g,v}\ \text{si la cosecha es existente} && \forall g,y\\
& X_{g,y}\le\bar X_g && \forall g,y\\
& 0\le p_{g,t}\le\bar p_{g,t}:=\alpha_g\,\kappa_{g,t}\,X_{g,y(t)} && \forall g,t
\end{aligned}
$$

- **Existentes.** Son las unidades de los datos de entrada de AMEBA en servicio el 1 de enero de 2025. Una unidad opera en un período si está en servicio el 1 de enero de su año de inicio; lo comprometido con fecha entra en el primer período que cumple esa regla. Ninguna inversión que decidió AMEBA entra como dato: el modelo decide todas las inversiones desde 2025.
- **Cosechas admisibles.** Son las filas de `gen_build_costs.csv`; así se fija desde qué período puede entrar cada candidato. Un candidato puede construirse desde el primer período cuyo año de inicio es mayor o igual que su fecha de entrada en AMEBA. Por ejemplo, las tres BESS «ley» (2.000 MW) son candidatas con inversión y O&M fijo 0 desde el período 2027.
- **Cosechas vivas.** Una cosecha entra en $s_v$, que es el inicio del período si $v$ es un período y el año $v$ si no lo es. Con la regla `--retire late`, por omisión, opera en $y$ si $s_v\le s_y<s_v+\ell_g$.
- **Sin compromiso de unidades.** No hay mínimos técnicos, rampas ni costos de partida (`no_commit`). El despacho mínimo es 0.
- Es la restricción $p_{ij}\le x_i$ de la Clase 8, con disponibilidad $\alpha_g$ y perfil $\kappa_{g,t}$.

### 4.3 Almacenamiento

$$
\begin{aligned}
& e_{s,t}=e_{s,t^-}+\eta_s\,c_{s,t}-p_{s,t} && \forall s,t\\
& e_{s,t}\le E_{s,y(t)},\qquad c_{s,t}\le\bar p_{s,t},\qquad p_{s,t}\le\bar p_{s,t} && \forall s,t\\
& E_{s,y}=\sum_{v\in\mathcal V_{s,y}}h_s\,x_{s,v}\ \ \text{(candidatos)};\qquad \text{energía dada (existentes)}
\end{aligned}
$$

La eficiencia de ida y vuelta se aplica a la carga. La Clase 7 la aplica a la descarga ($pH/\eta$): la energía de ida y vuelta es la misma, pero el estado de carga queda escalado. Por eso la energía de cada batería se tradujo como energía entregable (ver DATOS_Y_SUPUESTOS.md). El ciclo se cierra cada día típico.

### 4.4 Hidro

$$
p_{h,t}\ge\underline P_{h,d(t)},\qquad \sum_{t\in T_d}\big(p_{h,t}+sp_{h,t}\big)=24\,A_{h,d},\qquad p_{h,t}\le\alpha_h X_{h,y(t)}\qquad\forall h\in H,\ d,\ t
$$

Es un presupuesto de energía por día típico (`hydro_simple`). El vertimiento no tiene costo, así que $A_{h,d}$ es un tope de energía. No hay volúmenes ni afluentes ni acople entre días: la regulación entre meses de la Clase 7 viene dada desde afuera, con la energía mensual que despachó AMEBA. Es una salida de AMEBA usada como dato, declarada como pendiente en DATOS_Y_SUPUESTOS.md. La hidro candidata se modela como generación variable con su perfil $\kappa_{g,t}$.

### 4.5 Transmisión como transporte

$$
0\le f_{m\to n,t}\le F_{k,y(t)},\qquad 0\le f_{n\to m,t}\le F_{k,y(t)}\qquad\forall k=(m,n),\ t
$$

Es el modelo zonal de la Clase 5 con $ATC_k=F_{k,y}$, sin pérdidas (eficiencia 1) y sin leyes de Kirchhoff: no hay ángulos ni reactancias. La ampliación $T_{k,y}$ es continua y de costo lineal.

**Límites de construcción** (módulo `limites_transmision`). Switch, sin este módulo, deja ampliar cualquier corredor sin tope y en cualquier período. El módulo impone, para cada fila $(k,y)\in\mathcal L$ de `trans_build_limits.csv`:

$$
T_{k,y}\ge\underline T_{k,y},\qquad \sum_{v\le y}T_{k,v}\le\bar T_{k,y}\qquad\forall(k,y)\in\mathcal L;\qquad T_{k,y}=0\quad\forall(k,y)\notin\mathcal L.
$$

- El mínimo es **incremental**: la obra comprometida que entra en $y$ se construye en $y$. Con un mínimo acumulado, una ampliación candidata anterior podría contarse como parte de la obra comprometida.
- El máximo es **acumulado**: el tope de un candidato vale para todo el horizonte. Con un tope por período se podría construir el mismo candidato en cada período.
- Hay dos obras comprometidas, ambas en 2030: el HVDC Kimal–Alto Jahuel (Kimal–Lo Aguirre), con $\underline T=\bar T=2.000$ MW, y Río Malleco–Pichirropulli, con $\underline T=660$ MW.

### 4.6 Reserva sistémica

Módulo `reserva_simple`. En cada hora, la holgura de los proyectos elegibles cubre el requerimiento:

$$
\begin{aligned}
&\sum_{g\in G^R}\big(\bar p_{g,t}-p_{g,t}\big)+\sum_{s\in S\cap G^R}c_{s,t}\ \ge\ R^{+}_{y(t)} && (\rho R^{+}_t)\quad\forall t\\
&\sum_{g\in G^R}p_{g,t}+\sum_{s\in S\cap G^R}\big(\bar p_{s,t}-c_{s,t}\big)\ \ge\ R^{-}_{y(t)} && (\rho R^{-}_t)\quad\forall t
\end{aligned}
$$

Un almacenamiento aporta a subir dejando de cargar y a bajar cargando más. No hay variables nuevas.

**Frente al curso.** La Clase 8 (planificación con reservas) y la Clase 12 usan $p_{g,t}+r_{g,t}\le\bar p_{g,t}$ y $\sum_g r_{g,t}\ge R_t$. Sin tope de reserva por unidad ni costo de oferta de reserva, eliminar $r$ de ese sistema da exactamente la primera restricción: existe $r\ge 0$ que cumple ambas si y solo si $\sum_g(\bar p_{g,t}-p_{g,t})\ge R_t$. Diferencias:

- se agrega la reserva de bajada, que el curso no tiene y AMEBA sí;
- no hay tope por unidad ($R^{max}_g$ de la Clase 12);
- la hidro se cuenta desde 0 hacia abajo aunque tenga caudal mínimo, y el almacenamiento sin mirar su estado de carga;
- la reserva no usa la red: es un área única, como en AMEBA.

La reserva nativa de Switch no sirve aquí: exige el módulo de compromiso de unidades y tampoco tiene tope por unidad.

### 4.7 Energía no suministrada

$ls_{z,t}\ge 0$ entra como inyección en el balance de cada zona, con costo $VOLL$ por MWh (`unserved_load`). Es el $ls_j$ de la Clase 8 y cubre también la carga de data centers.

### 4.8 Topes de inversión por tecnología

Módulo `topes_tecnologia`. AMEBA limita cada año los MW nuevos de FV y eólica en todo el sistema. En Switch, $\bar X_g$ es un tope por proyecto sobre la capacidad en servicio, así que el módulo agrega, para cada fila $(\theta,y)\in\mathcal Q$ de `topes_tecnologia.csv`:

$$
\sum_{g\in G_\theta}x_{g,y}\le\bar N_{\theta,y}\qquad\forall(\theta,y)\in\mathcal Q .
$$

- Solo suma las cosechas nuevas del propio período; lo existente no cuenta.
- Con los datos de entrada de AMEBA, el tope de un período es la suma de los topes anuales de sus años: $\bar N_{\text{FV},2025}=3.000+50.000$ MW y $\bar N_{\text{Eolica},2025}=1.000+50.000$ MW, y desde 2027 es mayor. No restringe, así que en los casos de este estudio el módulo no se carga.
- Un período que no aparece en el archivo no tiene tope. Sin el archivo, el módulo no agrega restricciones.

---

## 5. Data centers

Módulo `data_centers`. La carga de data centers de cada zona tiene dos partes:

- **fija**, $\bar D^{\mathrm{DC}}_{z,y}$: no se mueve en ningún caso;
- **ubicable**, $x^{\mathrm{DC}}_{z,y}$: su total por período $D^{\mathrm{DC}}_y$ es un dato; su reparto entre zonas es un dato en el caso base y una decisión en el caso libre.

$D^{\mathrm{DC}}_y$ sale de cada escenario (DATOS_Y_SUPUESTOS.md): las trayectorias de la PELP 2028–2032 (E2 y N1) sin cambios; la del CEN, que crece 5 % anual desde 2031; y la propia, cuya demanda total de data centers crece 8 % anual desde 2033, con todo ese crecimiento ubicable.

$$
\begin{aligned}
&\sum_{z\in Z^{\mathrm{DC}}}x^{\mathrm{DC}}_{z,y}=D^{\mathrm{DC}}_y && (\lambda^{\mathrm{DC}}_y)\quad\text{solo en el caso libre}\\
&x^{\mathrm{DC}}_{z,y}\ge x^{\mathrm{DC}}_{z,y-1} && (\mu_{z,y})\quad\text{un data center no se traslada}\\
&x^{\mathrm{DC}}_{z,y}\le\bar X^{\mathrm{DC}}_z && \text{solo si la zona tiene tope}\\
&x^{\mathrm{DC}}_{z,y}=\hat x^{\mathrm{DC}}_{z,y} && \text{caso base: todo }y;\ \text{caso libre: }y<y^{\mathrm{libre}}
\end{aligned}
$$

**Caso base** (`--dc-modo base`): los data centers quedan donde dicen las proyecciones. La suma por período se omite porque es redundante, y así se evita que una diferencia de redondeo entre `dc_base.csv` y `dc_libre.csv` vuelva infactible el problema. En su lugar, una comprobación al construir el modelo detiene la corrida si $\big|\sum_z\hat x^{\mathrm{DC}}_{z,y}-D^{\mathrm{DC}}_y\big|>10^{-3}$ MW o si $\hat x^{\mathrm{DC}}$ decrece entre períodos. Si falta `dc_base.csv`, la suma da 0 y la comprobación también lo detiene.

**Caso libre** (`--dc-modo libre`): el modelo elige la zona de la carga ubicable, con el mismo total por período.

**Ubicación fija antes de 2030** (`--dc-libre-desde 2030`). En el caso libre, los períodos anteriores a $y^{\mathrm{libre}}=2030$ (2025 y 2027) quedan con la ubicación base. Con la regla de no traslado, lo ubicado en 2027 sigue en su zona después; el modelo solo decide dónde va el crecimiento desde 2030. Por eso la carga **reubicable** de un período $y\ge 2030$ es $D^{\mathrm{DC}}_y-D^{\mathrm{DC}}_{2027}$, lo agregado después del último período anterior a $y^{\mathrm{libre}}$. Es lo que se usa en todas las corridas. Las razones:

- lo que entra en 2025–2029 ya tiene sitio y solicitud de conexión;
- los períodos 2025 y 2027 se representan con los datos de su año de inicio, sin el HVDC Kimal–Alto Jahuel, que entra en 2030. En la primera versión del modelo, que partía en 2026, la ubicación libre desde el primer período aprovechaba un norte desacoplado y barato que en la realidad dura hasta 2028 (VALIDACION.md, fase 6).

**Costo.** $B_y\sum_z c^{\mathrm{DC}}_z x^{\mathrm{DC}}_{z,y}$ entra en el objetivo (`DCCostoAnual`). En este estudio $c^{\mathrm{DC}}_z=0$ y no hay topes $\bar X^{\mathrm{DC}}_z$: el resultado es la ubicación óptima para el sistema eléctrico, sin costos de terreno ni de conexión.

**Lectura de optimalidad.** Sea $\pi_{z,y}$ el costo, en VP, de abastecer 1 MW plano en la zona $z$ durante el período $y$:

$$
\pi_{z,y}=B_y\Big(c^{\mathrm{DC}}_z+\sum_{t\in T_y}\Delta T_t\,\rho_{z,t}\Big),
$$

con $\rho_{z,t}$ en USD/MWh del año (sección 6). Sumando las condiciones de Karush-Kuhn-Tucker de $x^{\mathrm{DC}}_{z,q}$ desde $q=y$ hasta el último período, los multiplicadores de no traslado se cancelan en cadena y queda

$$
\sum_{q\ge y}\pi_{z,q}=\sum_{q\ge y}\lambda^{\mathrm{DC}}_q+\mu_{z,y}+\sum_{q\ge y}\nu_{z,q}\ \ge\ \sum_{q\ge y}\lambda^{\mathrm{DC}}_q ,
$$

donde $\nu_{z,q}\ge 0$ es el multiplicador de $x^{\mathrm{DC}}_{z,q}\ge 0$. Si la zona $z$ recibe crecimiento en $y$ ($x^{\mathrm{DC}}_{z,y}>x^{\mathrm{DC}}_{z,y-1}$), entonces $\mu_{z,y}=0$ y $\nu_{z,q}=0$ para $q\ge y$, y

$$
\sum_{q\ge y}\pi_{z,q}=\sum_{q\ge y}\lambda^{\mathrm{DC}}_q=\min_{z'\in Z^{\mathrm{DC}}}\ \sum_{q\ge y}\pi_{z',q}.
$$

Un data center que se instala en $y$ va a la zona donde abastecerlo cuesta menos **desde $y$ hasta el final del horizonte**, no solo en el período en que entra. Con un solo período queda la forma de las condiciones de optimalidad de la Clase 8: $x^{\mathrm{DC}}_z>0\Rightarrow\pi_z=\lambda^{\mathrm{DC}}$ y $x^{\mathrm{DC}}_z=0\Rightarrow\pi_z\ge\lambda^{\mathrm{DC}}$. Los precios $\rho$ son endógenos: al mover cientos de MW cambian la generación y la red que se construyen. Por eso la ubicación es una variable del modelo y no una lectura de precios.

---

## 6. Precios

Módulo `precios`; requiere correr con `--suffixes dual`. El objetivo está en VP, así que el dual del balance de la zona $z$ en la hora $t$ está en USD de VP por MW. Para llevarlo a USD/MWh del año en que ocurre:

$$
\rho_{z,t}=\frac{\text{dual}\big(\text{balance}_{z,t}\big)}{B_{y(t)}\,\Delta T_t}\quad[\text{USD/MWh}],\qquad \bar\rho_{z,y}=\frac{\sum_{t\in T_y}\Delta T_t\,\rho_{z,t}}{\sum_{t\in T_y}\Delta T_t}.
$$

$\bar\rho_{z,y}$ es lo que paga una carga plana de 1 MW por MWh en la zona $z$: el precio que importa para un data center. Archivos de salida:

- `precios_nodales.csv`: $\rho_{z,t}$;
- `precios_zonales_anuales.csv`: $\bar\rho_{z,y}$;
- `dual_dc_total.csv`: $\lambda^{\mathrm{DC}}_y$ en USD de VP por MW, en el caso libre.

---

## 7. Métrica

$$
\Delta C=C^{*}_{\text{base}}-C^{*}_{\text{libre}}\ \ge 0 .
$$

La ubicación base cumple todas las restricciones del caso libre (total por período, no traslado y ubicación fija antes de 2030), así que es factible en él y el libre no puede costar más. Los dos casos usan la misma red, los mismos días y el mismo horizonte.

Con el caso sin data centers nuevos (`SIN_DC`), el costo extra de los data centers es $E=C^{*}-C^{*}_{\text{SIN\_DC}}$, en el caso base o en el libre. El ahorro se expresa sobre el costo total ($\Delta C/C^{*}_{\text{base}}$) y sobre el costo extra ($\Delta C/E_{\text{base}}$).

$C^{*}$ es `total_cost.txt`. El archivo `costs_itemized.csv` de Switch da el costo de un solo año de cada período llevado a VP, no el del período completo.

---

## 8. Correspondencia con el curso

| En el curso | Clase | En este modelo | Diferencia |
|---|---|---|---|
| Inversión $x_i$ con costo horario $I_i$ | 8 | $x_{g,v}$ con anualidad $I_{g,v}$ (USD/MW-año $=8.760\,I_i$) | Cosechas, vida útil, varios períodos con descuento |
| $p_{ij}\le x_i$ | 8 | $p_{g,t}\le\alpha_g\kappa_{g,t}X_{g,y}$ | Disponibilidad y perfil de recurso |
| Bloques $\Delta T_j$ de la curva de duración | 8 | Horas cronológicas $\Delta T_t$ de 6 días típicos | Conserva la secuencia del día y la coincidencia entre zonas |
| Costo marginal $MC_i$ | 3, 8 | $VOM+HR\cdot c^{f}$, más el impuesto al CO₂ | Varía por central, zona y período |
| Demanda inelástica con VOLL | 3, 8 | Igual, VOLL de 650 USD/MWh | Un VOLL único |
| Balance nodal y precio $\rho_n$ | 4, 5 | $\rho_{z,t}$, escalado como en la sección 6 | — |
| Transporte con ATC | 5 | Flujos dirigidos con $ATC=F_{k,y}$ | Sin pérdidas |
| Flujo DC con PTDF o susceptancias | 4 | No está | Ver DATOS_Y_SUPUESTOS.md, limitaciones |
| $C_T=c_T\,T$; $\pi_T=c_T$ en el óptimo | 13 | $I^T_k\,T_{k,y}$ con topes por período | Ampliación continua; obras comprometidas con fecha |
| $VATT=AVI+COMA$ | 13 | $c^T_k\,CRF(6\,\%,40)$ | $COMA=0$, como en AMEBA |
| $p+r\le x$, $\sum r\ge R$ | 8, 12 | Holgura de los elegibles $\ge R$ (sección 4.6) | Agrega bajada; sin tope por unidad; sin red para la reserva |
| Embalse y valor del agua | 7 | Energía fija por día típico | Sin acople entre meses |
| Bombeo con eficiencia | 7 | Almacenamiento con $\eta$ en la carga | Ciclo diario |
| Predespacho | 6 | No está | LP sin variables binarias |
| Un año, sin descuento | 8 | 7 períodos con $B_y$ | — |

---

## 9. Verificación: Switch reproduce el ejemplo de la Clase 8

Para comprobar que Switch es el modelo del curso, se resolvió en Switch el ejemplo de expansión de la Clase 8 y se comparó con la solución de las láminas.

**Datos del ejemplo.**

| Tecnología | $MC$ (USD/MWh) | $I$ (USD/MWh) |
|---|---|---|
| Carbón | 25 | 16 |
| Gas natural | 80 | 5 |
| Nuclear | 6,5 | 32 |
| Petróleo | 160 | 2 |

La curva de duración de las láminas está en tres tramos horizontales. Switch necesita bloques verticales con la carga total y su duración:

| Bloque | Horas | Demanda (MW) |
|---|---|---|
| 1 | 1.500 | 11.169 |
| 2 | 5.500 | 9.004 |
| 3 | 1.760 | 7.086 |

**Caso en Switch.** Una zona y un período de un año. Tres días típicos de una hora, con $\sigma$ = 1.500, 5.500 y 1.760: así $\Delta T_t$ son las horas de cada bloque. Cuatro proyectos candidatos sin combustible, con $MC$ como O&M variable. Como la inversión del curso está en USD por MWh, la anualidad es $8.760\,I_i$ USD/MW-año, y el objetivo de Switch queda $B\times 8.760\times$ el del curso: una escala positiva que no cambia la solución. Se probaron cuatro variantes:

| Variante | Tasas | Vida | Cómo entra la inversión |
|---|---|---|---|
| A | $i=r=0$ | 1 año | costo de inversión $=8.760\,I_i$ |
| B | $i=r=7\,\%$ | 30 años | costo de inversión $=8.760\,I_i/CRF(7\,\%,30)$ |
| C | $i=r=0$ | 1 año | O&M fijo $=8.760\,I_i$, inversión 0 |
| D | como A, con ENS a 1.000 USD/MWh | 1 año | como A |

**Resultado** (HiGHS):

| | Nuclear | Carbón | Gas | Petróleo | Costo total Switch (USD) |
|---|---|---|---|---|---|
| Lámina | 7.086 | 1.918 | 2.165 | 0 | — |
| A | 7.086 | 1.918 | 2.165 | 0 | 3.348.928.240 |
| B | 7.086 | 1.918 | 2.165 | 0 | 3.129.839.477 = A / 1,07 |
| C | 7.086 | 1.918 | 2.165 | 0 | 3.348.928.240 |
| D | 7.086 | 1.918 | 2.165 | 0 | 3.348.928.240, sin ENS |

- En A, 3.348.928.240 / 8.760 = 382.297,74 USD/h, que es el objetivo del curso evaluado en la solución de la lámina.
- El despacho llena la curva como en la lámina: nuclear en los tres bloques, carbón en los bloques 1 y 2, gas solo en el 1.
- **Precios.** Con la fórmula de la sección 6, los precios de los bloques son 109,20; 27,52 y 12,56 USD/MWh, iguales en A, B y C (la B tiene descuento). Cumplen la condición de inversión de la Clase 8, $I_i=\sum_j\Delta T_j\,(\rho_j-MC_i)^+$: nuclear 32,0, carbón 16,0 y gas 5,0. Para el petróleo, $0\le 2$, así que no se construye.
- La variante D muestra que con tres tramos ni el petróleo ni la ENS entran: el bloque más corto dura 1.500 h, más que sus quiebres (328 h y unas 21 h). Por eso el ejemplo con VOLL de la Clase 8, que usa la curva continua, no se puede reproducir con estos tres bloques.

---

## 10. Módulos y ejecución

`casos/<escenario>/inputs/modules.txt`:

```
# Núcleo de Switch
switch_model
switch_model.timescales
switch_model.financials
switch_model.balancing.load_zones
switch_model.energy_sources.properties
switch_model.generators.core.build
switch_model.generators.core.dispatch
switch_model.reporting
# Operación simplificada (sin compromiso de unidades)
switch_model.generators.core.no_commit
switch_model.energy_sources.fuel_costs.simple
switch_model.generators.extensions.storage
switch_model.generators.extensions.hydro_simple
switch_model.transmission.transport.build
switch_model.transmission.transport.dispatch
switch_model.balancing.unserved_load
switch_model.policies.carbon_policies
# Módulos propios del proyecto
modulos.limites_transmision
modulos.reserva_simple
modulos.data_centers
modulos.precios
```

| Módulo propio | Qué agrega | Sección |
|---|---|---|
| `limites_transmision` | obras comprometidas con fecha y topes acumulados por corredor y período | 4.5 |
| `topes_tecnologia` | MW nuevos máximos por tecnología y período, sumando todas las zonas; disponible, no se carga en estos casos | 4.8 |
| `reserva_simple` | reserva sistémica de subida y bajada sin compromiso de unidades | 4.6 |
| `data_centers` | carga de data centers fija y ubicable; casos base y libre | 5 |
| `precios` | precios por zona y hora, precio de carga plana y dual del total ubicable | 6 |

No se usan: compromiso de unidades (`commit.*`), reservas nativas (`operating_reserves.*`), `hydro_system`, `planning_reserves`, `local_td` ni variables binarias de construcción.

`scripts/correr_casos.py` resuelve cada caso con la misma línea de comandos en base y en libre:

```
switch solve --inputs-dir inputs --outputs-dir outputs_base  --solver gurobi_direct \
    --dc-modo base  --dc-libre-desde 2030 --suffixes dual --solver-options-string "Method=2 Threads=6"
switch solve --inputs-dir inputs --outputs-dir outputs_libre --solver gurobi_direct \
    --dc-modo libre --dc-libre-desde 2030 --suffixes dual --solver-options-string "Method=2 Threads=6"
```

- `--dc-libre-desde` no tiene efecto en el caso base.
- La regla de vida útil es `--retire late`, la de Switch por omisión; queda registrada en `model_config.json` de cada salida.
- Cada caso es un LP de unos 1,54 millones de restricciones, 1,35 millones de variables y 8,07 millones de coeficientes. Con Gurobi (barrera y crossover, 8 a 14 hilos), cada corrida tarda entre 10 y 18 minutos. HiGHS (`--solver appsi_highs`) es la alternativa libre, bastante más lenta.
