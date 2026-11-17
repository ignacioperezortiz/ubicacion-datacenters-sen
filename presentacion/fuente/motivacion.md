# Motivación: contenido de las 2 diapositivas

Cifras revisadas el 17-nov-2026 en la fuente primaria. Las citas breves remiten a la lista de referencias del final.

---

## Diapositiva 1

**Título:** Motivación: data centers

**Subtítulo:** Consumo eléctrico, inversión y solicitudes de conexión de los data centers en el mundo, en EE. UU. y en Chile

- El consumo eléctrico de los data centers en el mundo fue de 415 TWh en 2024 (1,5 % del total) y llegaría a ~945 TWh en 2030 (IEA, 2025).
- La inversión mundial en data centers casi se duplicó desde 2022 y alcanzó ~USD 500 mil millones en 2024 (IEA, 2025).
- En EE. UU., los data centers consumieron 176 TWh en 2023 (4,4 % del país); para 2028 se proyectan 325–580 TWh (6,7–12 %) (Shehabi et al., 2024).
- En EE. UU., las carteras de conexión superan 4 a 6 veces lo contratado: en Virginia, 53,8 GW de data centers frente a 12,0 GW con contrato de servicio firmado; en Georgia, 73,1 GW de grandes cargas frente a 12,4 GW comprometidos (Dominion Energy, 2026; Georgia Power, 2026).
- En Chile, el CEN estima 398 MW instalados en 2025 y proyecta 1.381 MW al 2030: 1.225 MW en la RM (89 %) y 155 MW en Valparaíso (CEN, 2026a).
- Ante el CEN hay 37 solicitudes de conexión de data centers vigentes, por ≈4,25 GW con conexión estimada hasta 2032: el triple de lo proyectado al 2030, con 81 % en la RM y 19 % en Valparaíso (CEN, s. f.).

**Siglas (pie de lámina):** IEA, Agencia Internacional de Energía; CEN, Coordinador Eléctrico Nacional; RM, Región Metropolitana.

---

## Diapositiva 2

**Título:** Motivación: sistema eléctrico chileno

**Subtítulo:** Congestión de la transmisión norte–centro, vertimiento renovable, oleadas de inversión y ubicación de la nueva demanda en el SEN

- En 2025, el tramo Polpaico–Nueva Pan de Azúcar 500 kV, del corredor norte–centro, estuvo desacoplado 1.305 horas, ~15 % del año (CEN, 2026b).
- En 2025 se redujeron 6.084 GWh de generación eólica y solar por congestión y excedente de oferta, ≈19 % de lo que esas fuentes generaron (CEN, 2026b).
- La solar FV en operación llegó a 12,7 GW en agosto de 2026, por sobre los 10,75 GW que el escenario E de la PELP 2018–2022 preveía para 2035 (CNE, 2026; Ministerio de Energía, 2018).
- El almacenamiento en ejecución suma 10,2 GW (junio de 2026), frente a una meta de 6 GW al 2030; en 2025, el 78 % de la potencia aprobada para conexión correspondió a proyectos con almacenamiento, mayoritariamente en el norte (Ministerio de Energía, 2026; CEN, 2026b).
- En 2025, los costos marginales diurnos del norte fueron cercanos a cero en primavera y verano; la HVDC Kimal–Lo Aguirre (3.000 MW), que aliviaría el corredor norte–centro, entraría en 2029 (CEN, 2026b).
- La nueva demanda de data centers se ubica en el extremo receptor del corredor: el 89 % de la capacidad proyectada al 2030 está en la RM (CEN, 2026a).

**Serie de vertimiento usada:** reducciones de generación ERV (eólica y solar) del CEN, estimadas desde su registro de instrucciones de reducción (CEN, 2026b, sección II.10). Solo se usa el año 2025, sin compararlo con otros años ni con otras series (ACERA, Ember, CNE).

**Siglas (pie de lámina):** SEN, Sistema Eléctrico Nacional; FV, fotovoltaica; PELP, Planificación Energética de Largo Plazo; CNE, Comisión Nacional de Energía; HVDC, corriente continua en alta tensión; ERV, energía renovable variable.

---

## Gráfico propuesto (diapositiva 1)

- **Título:** Solicitudes de conexión vigentes de data centers al CEN, por año estimado de conexión (MW)
- **Tipo:** barras, una serie: columna `mw_solicitados` de `motivacion_grafico.csv`, años 2022–2032. Eje vertical en MW.
- **Pie del gráfico:** «Fuente: elaboración propia con datos de la Plataforma de Acceso Abierto del CEN (consulta del 13-nov-2026). Fechas declaradas por los solicitantes; puede haber solicitudes alternativas para un mismo campus.»
- **Lectura para quien presente:** 3,5 GW tienen conexión estimada entre 2028 y 2031. Las solicitudes de 2022–2025 (428 MW) ya están autorizadas o declaradas en construcción, del orden de los 398 MW que el CEN estima instalados en 2025.
- **Variante, si el formato admite dos series:** `mw_solicitados_acumulados` (línea) frente a `cen_capacidad_instalada_proyectada_mw` (barras, 2025–2030; CEN, 2026a, figura 5-13). Al 2030, lo solicitado acumula 3.318 MW, 2,4 veces los 1.381 MW proyectados.
- **Excluido:** dos solicitudes vigentes sin fecha estimada (16,6 MW). No se incluyó la trayectoria de la PELP 2028–2032 (594 MW instalados al 2030) porque no se pudo verificar en el PDF; ver la tabla.

Columnas del CSV: año estimado de conexión; número de solicitudes vigentes; MW solicitados en el año, desglosados en autorizados o en construcción, en tramitación y detenidos; MW acumulados; capacidad instalada proyectada por el CEN.

---

## Tabla de verificación

| Cifra | Fuente primaria | URL | Página o sección | Verificada |
|---|---|---|---|---|
| 415 TWh en 2024, 1,5 % del consumo mundial | IEA, *Energy and AI* (2025) | https://www.iea.org/reports/energy-and-ai/executive-summary | Resumen ejecutivo, «Data centres account for a small share…» | Sí |
| ~945 TWh en 2030 | IEA (2025) | ídem | Resumen ejecutivo, «Electricity demand for data centres more than doubles by 2030» | Sí |
| Inversión casi duplicada desde 2022, ~USD 500 mil millones en 2024 | IEA (2025) | ídem | Resumen ejecutivo, «Data centres account for a small share…» | Sí |
| EE. UU.: 176 TWh en 2023, 4,4 % del consumo | Shehabi et al. (2024), LBNL-2001637 | https://eta-publications.lbl.gov/sites/default/files/2024-12/us_data_center_energy_usage_report_lbnl-2001637.pdf | Resumen ejecutivo, p. 7 impresa (p. 8 del PDF); también p. 52 del PDF | Sí |
| EE. UU.: 325–580 TWh en 2028, 6,7–12,0 % | Shehabi et al. (2024) | ídem | Resumen ejecutivo, p. 7 impresa, figura ES-1 | Sí |
| Virginia: ~53,8 GW de data centers en contratación y 12,0 GW con contrato de servicio (ESA), julio de 2026 | Dominion Energy, presentación de resultados Q2-2026 | https://s2.q4cdn.com/510812146/files/doc_financials/2026/q2/2026-07-31-DE-IR-2Q-2026-earnings-call-slides-vTCII.pdf | Lámina 5, «Data center contracted capacity» | Sí |
| Georgia: 73.100 MW de grandes cargas en cartera y 12.400 MW comprometidos (31 clientes), al 31-mar-2026 | Georgia Power, *Q1 2026 Large Load Economic Development Report*, expediente 56002 | https://services.psc.ga.gov/api/v1/External/Public/Get/Document/DownloadFile/226607/107927 | Secciones «Changes in the Economic Development Pipeline» y «Changes in Commitments from Large Load Customers» | Sí |
| «4 a 6 veces» (53,8/12,0 = 4,5; 73,1/12,4 = 5,9) | Cálculo propio con las dos filas anteriores | — | — | Sí |
| Chile: 398 MW instalados en 2025 | CEN, *Proyección de Demanda de Largo Plazo SEN 2026–2046* (oct-2026) | https://www.coordinador.cl/wp-content/uploads/2026/10/20261007-INF-proy-demanda-26-46-v01.pdf | Sección 5.7.2, p. 32 | Sí |
| Chile: 1.381 MW al 2030; serie 398, 552, 642, 963, 1.281, 1.381 MW (2025–2030) | CEN (2026a) | ídem | Sección 5.7.2, figura 5-13, p. 32 | Sí |
| RM 1.225 MW y Valparaíso 155 MW al 2030; 89 % en la RM | CEN (2026a) | ídem | Sección 5.7.2, p. 32 | Sí |
| 37 solicitudes vigentes de data centers, ≈4,25 GW (RM 3,45 GW, 81 %; Valparaíso 0,80 GW, 19 %); serie anual del gráfico | CEN, Plataforma de Acceso Abierto, listado público de solicitudes | https://accesoabierto.coordinador.cl | Listado de solicitudes, consulta del 13-nov-2026; filtro de solicitudes de consumo de data centers, sin rechazadas ni desistidas | **NO VERIFICADA** en línea |
| «El triple de lo proyectado al 2030» (4.250/1.381 = 3,1) | Cálculo propio con las dos filas anteriores | — | — | **NO VERIFICADA** (depende de la fila anterior) |
| Polpaico 500 → Nueva Pan de Azúcar 500: 1.305 horas desacopladas (319 eventos) en 2025 | CEN, *Reporte Anual de Desempeño del SEN, año 2025* (abr-2026) | https://www.coordinador.cl/wp-content/uploads/2026/04/CEN-Reporte-Art-72-15-ano-2025-21-04-2026.pdf | Sección II.11, tabla 4, p. 17 | Sí |
| «~15 % del año» (1.305/8.760) | Cálculo propio | — | — | Sí |
| 6.084 GWh de reducciones eólicas y solares en 2025 | CEN (2026b) | ídem | Sección I.3, p. 6; sección II.10, figura 13, p. 16 | Sí |
| «≈19 % de lo que esas fuentes generaron»: 6.084 / (20.490,1 solar + 12.192,9 eólica) = 18,6 % | Cálculo propio con CEN (2026b) | ídem | Generación por fuente: sección II.4, p. 9 | Sí |
| 12.680 MW solares FV en operación comercial a agosto de 2026 | CNE, *Reporte Mensual ERNC*, septiembre de 2026 (vol. 121) | https://www.cne.cl/wp-content/uploads/2026/09/RMensual_ERNC_v202609.pdf | Cuadro resumen «Estado de proyectos ERNC», p. 2 | Sí |
| PELP 2018–2022, escenario E: 10.750 MW FV en 2035 | Ministerio de Energía, PELP 2018–2022, informe final corregido (19-feb-2018) | https://energia.gob.cl/sites/default/files/documentos/informe_final_corregido_pelp_2018-2022.pdf | Sección 5.2.4, p. 97 | Sí |
| Almacenamiento en ejecución: 10.234 MW a junio de 2026 (2.291 MW en operación); meta de 6.000 MW al 2030 | Ministerio de Energía, *Reporte de Proyectos*, junio de 2026 | https://energia.gob.cl/sites/default/files/documentos/reporte_de_proyectos_-_junio_2026.pdf | «Estado de avance sistemas de almacenamiento de energía», p. 6 | Sí |
| 2025: 303 solicitudes aprobadas por 35.044 MW; 216 con almacenamiento por 27.459 MW (78 % de la potencia), mayoritariamente en el norte | CEN (2026b) | URL del reporte anual del CEN | Sección I.3, p. 6; sección VIII.1, p. 42; figura 53, p. 44 | Sí |
| Costos marginales diurnos del norte cercanos a cero en primavera y verano de 2025 | CEN (2026b) | ídem | Sección I.4 (Conclusiones), p. 6 | Sí |
| HVDC Kimal–Lo Aguirre: 3.000 MW, entrada prevista en 2029, alivio del corredor norte–centro | CEN (2026b) | ídem | Sección I.4, p. 6; sección X.2, p. 55 | Sí |
| PELP 2028–2032: 198 MW (2024) y 594 MW (2030) instalados (no se usa en las láminas) | Ministerio de Energía, informe preliminar PELP 2028–2032 (24-jul-2026) | https://www.energia.gob.cl/sites/default/files/documentos/20260724_informe_preliminar_pelp_2028-2032.pdf | Sección 5.1.5 según lectura anterior; no releída | **NO VERIFICADA** |

**Resumen:** de las 23 cifras de los bullets (filas 1 a 23), 21 quedan verificadas en la fuente primaria. Las dos no verificadas son la de solicitudes al CEN y el «triple» que se calcula con ella.

### Notas de la verificación

- **Solicitudes al CEN:** la Plataforma de Acceso Abierto es una aplicación web y su listado no se puede leer con WebFetch. Las cifras vienen del listado público descargado el 13-nov-2026: 37 solicitudes vigentes, que incluyen las detenidas, en tramitación, autorizadas y declaradas en construcción. Los MW son la potencia o demanda solicitada, no la capacidad instalada. La suma puede contar dos veces un campus con solicitudes alternativas, y las fechas las declara el solicitante. No se encontró una fuente oficial que publique el total. Antes de presentar, conviene repetir la consulta en la plataforma.
- **PELP 2028–2032:** el PDF supera el límite de WebFetch (10 MB). El comunicado del Ministerio del 24-jul-2026 no da cifras de data centers. Las cifras 198 y 594 MW solo se encontraron en prensa (pv magazine, 28-jul-2026). Por eso no van en las láminas ni en el gráfico.
- **Vertimiento 2025:** el CEN define los 6.084 GWh como reducción de energía eólica y solar (ERV). La misma cifra aparece en el balance de ACERA, pero aquí se cita solo al CEN.
- **Capacidad de data centers en la RM en 2025:** el CEN escribe «364 MW … cerca de 98 %», pero 364/398 = 91 %. Por esa inconsistencia, esa cifra no se usa.
- **Almacenamiento:** en el reporte del Ministerio, el gráfico da 2.760 MW en pruebas y 4.705 MW en construcción, mientras el texto dice 2.524 y 4.937 MW. Por eso solo se usan el total en ejecución (10.234 MW), que muestra el gráfico, y los 2.291 MW en operación, que coinciden en el gráfico y el texto.
- **Georgia:** la cartera es de grandes cargas en general, no solo de data centers. El bullet lo dice así.
- **LBNL:** la copia del PDF en el sitio del laboratorio lleva la marca «EMBARGOED REPORT»; es el informe publicado en diciembre de 2024. En la referencia se usa el DOI.

---

## Referencias (APA 7)

Comisión Nacional de Energía [CNE]. (2026). *Reporte mensual ERNC: septiembre 2026* (Vol. 121). https://www.cne.cl/wp-content/uploads/2026/09/RMensual_ERNC_v202609.pdf

Coordinador Eléctrico Nacional [CEN]. (s. f.). *Plataforma de Acceso Abierto: solicitudes de conexión* [Base de datos]. Recuperado el 13 de noviembre de 2026 de https://accesoabierto.coordinador.cl

Coordinador Eléctrico Nacional [CEN]. (2026a). *Proyección de demanda de largo plazo SEN 2026–2046* (Informe 2610-C13-INF-DPR-01-V1). https://www.coordinador.cl/wp-content/uploads/2026/10/20261007-INF-proy-demanda-26-46-v01.pdf

Coordinador Eléctrico Nacional [CEN]. (2026b). *Reporte anual de desempeño del Sistema Eléctrico Nacional, año 2025 (Art. 72°-15, DFL 4/20.018)*. https://www.coordinador.cl/wp-content/uploads/2026/04/CEN-Reporte-Art-72-15-ano-2025-21-04-2026.pdf

Dominion Energy. (2026, 31 de julio). *Q2 2026 earnings call* [Diapositivas]. https://s2.q4cdn.com/510812146/files/doc_financials/2026/q2/2026-07-31-DE-IR-2Q-2026-earnings-call-slides-vTCII.pdf

Georgia Power. (2026, 15 de mayo). *Q1 2026 large load economic development report* (Expediente N.° 56002). Georgia Public Service Commission. https://services.psc.ga.gov/api/v1/External/Public/Get/Document/DownloadFile/226607/107927

International Energy Agency [IEA]. (2025). *Energy and AI*. https://www.iea.org/reports/energy-and-ai

Ministerio de Energía. (2018). *Planificación energética de largo plazo, período 2018–2022: Informe final corregido*. https://energia.gob.cl/sites/default/files/documentos/informe_final_corregido_pelp_2018-2022.pdf

Ministerio de Energía. (2026). *Reporte de proyectos: junio 2026*. https://energia.gob.cl/sites/default/files/documentos/reporte_de_proyectos_-_junio_2026.pdf

Shehabi, A., Smith, S. J., Hubbard, A., Newkirk, A., Lei, N., Siddik, M. A. B., Holecek, B., Koomey, J., Masanet, E., & Sartor, D. (2024). *2024 United States data center energy usage report* (LBNL-2001637). Lawrence Berkeley National Laboratory. https://doi.org/10.71468/P1WC7Q
