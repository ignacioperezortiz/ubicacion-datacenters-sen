# Verificación de las dos láminas de motivación (verificador independiente)

Fecha: 17-nov-2026. Texto extraído de los PDF de `fuentes_motivacion\` con PyMuPDF (`fitz`) bajo `python -P`; el .docx de Georgia Power se leyó con zipfile (word/document.xml, notas al pie y las imágenes de las tablas 1 y 2). El catastro `Catastro_DataCenters_CEN_SEIA.xlsx` se leyó con openpyxl en solo lectura. Scripts en el scratchpad; nada se ejecutó desde la carpeta de las fuentes.

Páginas: «impresa / archivo». IEA, CEN (ambos), CNE y PELP: impresa = archivo. Shehabi (LBNL): impresa = archivo − 1. Dominion: número de lámina = archivo. Reporte de Proyectos del Ministerio: láminas sin número impreso. El .docx de Georgia Power no tiene paginación fija; se cita la sección.

## Resultado

| id | veredicto | evidencia textual (≤ 25 palabras) | pág. impresa / archivo | corrección propuesta |
|---|---|---|---|---|
| M1 | CORRECTA | «Data centres accounted for around 1.5% of the world's electricity consumption in 2024, or 415 terawatt-hours (TWh)»; «set to more than double to around 945 TWh by 2030» | 14 / 14 (también 49 / 49 y 63 / 63) | Ninguna. Opcional: los 945 TWh son del escenario base (*Base Case*). |
| M2 | CORRECTA | «Global investment in data centres has nearly doubled since 2022 and amounted to half a trillion dollars in 2024» | 13 / 13 (y 222 / 222: «over USD 500 billion in 2024») | Ninguna. |
| M3 | CORRECTA | «reaching 176 TWh by 2023, representing 4.4% of total U.S. electricity consumption»; «roughly 325 and 580 TWh in 2028»; «6.7% to 12.0%» | 6–7 / 7–8 (resumen); 51 / 52 | Ninguna. |
| M4 | IMPRECISA (etiqueta) | Título de la lámina: «Data center contracted capacity (updated)». Julio 2026: «~53.8 GW» = «SELOA: 32.4 GW» + «CLOA: 9.4 GW» + «ESA: 12.0 GW» | lámina 5 / 5 (deck del 31-jul-2026) | Las cifras están bien, pero Dominion llama a los 53,8 GW «capacidad contratada», no cartera. Todo está ya bajo algún contrato, en tres etapas. Proponer: «~53,8 GW de capacidad de data centers contratada (julio 2026): 32,4 GW con carta de ingeniería (SELOA), 9,4 GW con carta de construcción (CLOA) y 12,0 GW con contrato de servicio eléctrico (ESA)». |
| M5 | CORRECTA | «As of March 31, 2026 … 76,200 MW. Of this, 73,100 MW represents large load economic development projects»; «reaching a total of 12,400 MW across 31 customers» | docx: *Introduction* y tabla 2 (imagen) | Ninguna. Son grandes cargas («above the Company's organic load growth thresholds for commercial and industrial load», nota 1), no solo data centers. La tabla 1 (imagen) desglosa los 12,4 GW comprometidos: 26 data centers por 11.750 MW y 5 industriales por 607 MW. La cartera de 73,1 GW no se desglosa por tipo. Opcional: «Georgia Power» (no el estado) y «hasta mediados de los 2030». |
| M6 | CORRECTA | «Al año 2025 se estima una capacidad instalada de aproximadamente 398 MW»; «alcanzaría aproximadamente 1381 MW»; RM «1225 MW», Valparaíso «155 MW»; «cerca de 89%» | 32 / 32 (fig. 5-13: 398, 552, 642, 963, 1281, 1381) | Ninguna. Nota: el propio CEN es inconsistente en el texto. Dice 364 MW en la RM («cerca de 98%») y un incremento «cercano a 1011 MW», ambos coherentes con ~370 MW en operación, no con 398. Esto no afecta a la lámina. |
| M7 | CORRECTA (se reconstruye exacta) | Catastro, hoja «Notas y metodología»: «Una solicitud es 'vigente' si su estado no es Rechazada ni Desistida»; «Cronograma MW»: «puede incluir solicitudes alternativas para un mismo campus y solicitudes ya conectadas» | hojas «Solicitudes CEN», «Cronograma MW», «Catastro DC» | Cifras exactas: 37 vigentes, 4.250,0 MW; RM 3.450 MW (81,2 %) y Valparaíso 800 MW (18,8 %); la conexión estimada más lejana es el 15-10-2032. La serie es un acumulado desde 2022: 428,4 / 440,4 / 452,4 / 1.330,4 / 1.818,4 / 3.318,4 MW. Conviene aclarar en la lámina que incluye ~0,82 GW ya autorizados o declarados en construcción, parte de ellos en operación. Ver detalle abajo. |
| M8 | CORRECTA | Tabla 4: «POLPAICO 500 -> NUEVA PAN DE AZÚCAR 500 · 319 · 1.305»; «cantidad de eventos de congestión que tuvieron las líneas, como cantidad de horas desacopladas del sistema» | 17 / 17 | Ninguna: 1.305 / 8.760 = 14,9 % ≈ 15 %. Opcional: «319 eventos de congestión». Es el tercer tramo con más horas (El Peñón–La Ruca 110 kV tiene 2.771 h y Lastarria–Ciruelos 220 kV 1.797 h) y el único de 500 kV en la tabla. |
| M9 | CORRECTA | «Debido a la congestión en líneas de transmisión y al excedente generalizado de oferta … se registraron reducciones de energía eólica y solar» (total: «6.084 GWh») | 6 / 6 (también 16 / 16, fig. 13) | Sí dice «congestión y excedente de oferta». Razón con el mismo reporte (9 / 9: solar 20.490,1 GWh; eólica 12.192,9 GWh): 6.084 / 32.683 = 18,6 % ≈ 19 % de la generación solar y eólica inyectada. Si se mide sobre lo disponible (generado + reducido), es 15,7 %. Conviene decir «≈19 % de lo generado». |
| M10 | CORRECTA (matiz) | «provocó que los costos marginales diurnos en la zona norte se proyectaran cercanos a cero durante los meses de primera [sic] y verano»; HVDC «prevista para el año 2029» | 6 / 6; 3.000 MW: 55 / 55 («aportará 3.000 MW de capacidad adicional de transmisión entre el norte y el centro») | Ninguna obligatoria. Matiz: la afirmación sale de las conclusiones, que dicen «se proyectaran». El reporte no muestra costos marginales horarios diurnos observados de 2025, solo promedios mensuales por barra (fig. 7, Crucero 220 kV, 11 / 11), y ninguno es cercano a cero. Sugerencia: «según el CEN, …». |
| M11 | CORRECTA | Cuadro resumen, Operación [MW]: «Solar - PV · 12.680»; nota «(1) Considera sólo proyectos entregados a explotación comercial»; datos «a agosto de 2026» | 2 / 2 | Ninguna. Se trata de capacidad neta; además hay 9 MW en pruebas y 3.819 MW en construcción. |
| M12 | CORRECTA | «para tal año [2035, escenario E], existen en el sistema 10,750 [MW] en plantas solares fotovoltaicas y 6,787 [MW] en plantas eólicas» | 97 / 97; escenarios: tabla 13, 57 / 57 | Ninguna. E es el escenario con más solar FV, empatado con B, así que la comparación es justa y conservadora. Ver detalle abajo. |
| M13 | CORRECTA (fuente con descuadres internos) | «Sistemas de Almacenamiento en ejecución – junio 2026 … 10.234 MW»; «La meta de 6.000 MW … al 2030 registra un avance del 35%, con 2.291 MW ya operativos» | lámina 6 / 6 (sin número impreso) | Ninguna para las cifras de la lámina. «En ejecución» abarca lo declarado en construcción ante la CNE, en construcción, en pruebas y en operación. No desglosar: los segmentos del gráfico (2.291 + 2.760 + 4.705 + 505) suman 10.261 MW, el texto da 2.524 MW en pruebas y 4.937 MW en construcción, y 2.291 / 6.000 da 38 %, no 35 %. |
| M14 | CORRECTA | «303 solicitudes de conexión aprobadas (35.044 MW)… 216 solicitudes equivalentes a 27.459 MW… mayoritariamente en el norte del país»; «representa un 78% de la potencia total» | 6 / 6; 42 / 42 | Ninguna. El resumen ejecutivo destaca el 71 % (por número de solicitudes, 216 / 303). El 78 % es por potencia y también está en el texto (42 / 42). |

## Detalle M4 (Dominion, lámina 5)

- **53,8 GW**: el rótulo es «~53.8 GW» sobre la columna «July 2026». El título de la lámina es «Data center contracted capacity (updated)». La cifra es la suma de tres etapas contractuales:
  - SELOA (*Substation Engineering Letter of Authorization*): 32,4 GW. Plan de ingeniería detallado, con los costos reembolsados a Dominion.
  - CLOA (*Construction Letter of Authorization*): 9,4 GW. Autoriza la construcción, y el cliente reembolsa lo gastado si se retira.
  - ESA (*Electric Service Agreement*): 12,0 GW.
- **12,0 GW**: es la etapa ESA. La lámina la describe así: «Defines how the customer will take service and structure to recover costs», «Includes revenue requirement whether customer takes service or not». Llamarla «contrato de servicio firmado» es correcto.
- Contexto de la misma lámina: +5,3 GW (11 %) frente a diciembre de 2025 (~48,5 GW). En marzo de 2026 eran ~51,0 GW, y en julio de 2023, ~16,5 GW.

## Detalle M7 (catastro del equipo, descargado del CEN el 13-11-2026)

- **Filtros**:
  - Hoja «Solicitudes CEN»: 73 solicitudes identificadas como data center.
  - Se excluyen las que tienen «Categoría estado» = Rechazada (24) o Desistida (12). Quedan 37, que coinciden con la columna «Vigente» = Sí.
  - Las 37 se reparten así: en tramitación 14, detenidas 3, autorizadas por declarar en construcción 5, obra menor 7 y declaradas en construcción 8.
- **MW**: 4.250,0 MW en total. Siete vigentes no informan MW.
  - Por región: RM 3.450 MW (81,2 %) y Valparaíso 800 MW (18,8 %).
  - Por estado: en tramitación o detenidas, 3.433 MW. Autorizadas, obra menor o declaradas en construcción, 817 MW.
- **Fechas**: 35 vigentes tienen fecha (4.233,4 MW) y 2 no la tienen (alimentadores MT de ODATA, 8,3 + 8,3 MW). La fecha más lejana es el 15-10-2032 (Ampliación Mega Data Center Lampa Etapa 2, 300 MW).
- **Serie acumulada por año de la «fecha estimada de conexión»**:

  | | 2022 | 2023 | 2024 | 2025 | 2026 | 2027 | 2028 | 2029 | 2030 | 2031 | 2032 |
  |---|---|---|---|---|---|---|---|---|---|---|---|
  | MW acumulados | 30 | 290 | 420 | 428,4 | 440,4 | 452,4 | 1.330,4 | 1.818,4 | 3.318,4 | 3.933,4 | 4.233,4 |

  Coincide con la suma acumulada de la hoja «Cronograma MW». Ojo: el valor de 2025 (428 MW) ya incluye lo conectado en 2022–2024, por lo que equivale a la base existente (comparable con los 398 MW del CEN).
- **Solicitudes que se cuentan dos veces**: las 37 solicitudes corresponden a 20 campus.
  - Duplicadas en número, pero no en MW:
    - Ascenty SCL4: 2719 con 150 MW y 2718 detenida, sin MW.
    - Ascenty Quilicura: cinco alimentadores, y solo uno informa MW (8,4).
    - Scala Lampa: «Ampliación» 2711 (sin MW) y «Etapa 2» 2879 (300 MW).
  - Posible doble conteo en MW:
    - ACS DC Santiago I, alimentadores N.º 1 y N.º 2 (14 + 14 MW, misma S/E Chacabuco): si son redundantes, sobran 14 MW.
    - Lader, Lo Aguirre (500 MW en 500 kV) y Lo Aguirre A (25 MW en 44 kV): mismo titular y misma fecha.
    - ODATA, alimentadores de 12 kV (16,6 MW, sin fecha): posible suministro provisorio del campus ST02.
    - En total, como mucho ~55 MW (~1 %).
  - No parecen alternativas, pero conviene tenerlas a la vista:
    - FR Data, Valparaíso 1 y 2: 200 + 100 MW en la misma S/E, con paños distintos.
    - Ignis, Noviciado I (500 MW, Lo Aguirre) y Pacífico 33-S (500 MW, La Pólvora): sitios distintos. Si fueran alternativas, serían 500 MW.
  - SC2 de Polpaico tiene una solicitud rechazada y una vigente, y la vigente se cuenta una sola vez.

## Detalle M12 (PELP 2018–2022)

- **Los escenarios** (tabla 13, 57 / 57): E combina demanda alta, costos de inversión renovable bajos, combustibles fósiles caros, externalidades altas y cambio tecnológico alto en baterías. Es el escenario más favorable a la solar.
- **Solar FV al 2035 en los otros escenarios**: el texto no lo dice. Lo medí sobre los gráficos vectoriales de capacidad instalada (figs. 28, 30, 32, 34 y 36; págs. 74, 76, 78, 80 y 82). Para validar el método, el escenario E da 10.749 MW, igual a los 10.750 del texto.

  | Escenario | Solar FV al 2035 (estimado del gráfico) |
  |---|---|
  | E | ≈10,7 GW |
  | B | ≈10,7 GW |
  | C | ≈5,9 GW |
  | A | ≈5,5 GW |
  | D | ≈4,0 GW |

- **FV nueva incorporada al 2046** (tablas 15–19): E 13.463 MW, B 13.397 MW, C 8.848 MW, A 7.861 MW y D 5.215 MW.
- **Conclusión**: la comparación usa el escenario más optimista para la solar (empatado con B), así que es justa y conservadora. Los 12,7 GW de agosto de 2026 superan lo que el escenario más solar preveía para 2035.
- **Dato extra** (gráficos): para 2025 todos los escenarios rondaban los 2,6–2,9 GW de solar FV.

## Resumen

- INCORRECTAS: ninguna.
- IMPRECISAS: M4. Las cifras están bien, pero los 53,8 GW son «data center contracted capacity», es decir, SELOA + CLOA + ESA ya contratados, y no una «cartera de contratación».
- Matices recomendados:
  - M7: aclarar que la serie es un acumulado desde 2022 y que incluye ~0,82 GW ya autorizados o declarados en construcción.
  - M9: el 19 % es sobre lo generado; sobre lo disponible es 16 %.
  - M10: la frase del CEN dice «se proyectaran»; atribuirla al CEN.
  - M13: no desglosar los 10.234 MW, porque la fuente no cuadra internamente.
