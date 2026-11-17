# Verificación de la lámina de búsqueda bibliográfica (verificador independiente)

Fecha: 17-nov-2026. Texto extraído de los PDF de `literatura_B\pdf\` con PyMuPDF (`fitz`) bajo `python -I` (pypdf y pdfplumber no están instalados en este equipo); scripts en el scratchpad, nada ejecutado desde la carpeta de los PDF. Metadatos contrastados con Crossref (`api.crossref.org/works/<DOI>`).

Páginas: «impresa / archivo». En Onodera la página impresa = archivo − 1 (la hoja 1 del archivo es el resumen gráfico). En Shao (arXiv) impresa = archivo. En Newbery impresa = archivo − 2 (portada y hoja de resumen sin número).

## Resultado

| id | veredicto | evidencia textual (≤ 25 palabras) | pág. impresa / archivo | corrección propuesta |
|---|---|---|---|---|
| O1 | CORRECTA | «simultaneously optimizes capacity expansion and operation planning for electricity generation, storage, transmission…»; «the model covers 1,741 municipal-level nodes» | 7 / 8; 8 / 9 | Ninguna. Matiz opcional: el modelo (ReGRID) también optimiza hidrógeno y remoción de carbono (DACCS); el horizonte es 2050 («designed for 2050», 3 / 4). |
| O2 | CORRECTA (matiz) | «BAU… maintains the current urban concentration»; «FLEX… with no explicit siting constraints»; «counterfactual case (NoDC) that excludes data center electricity demand» | 2 / 3 | Opcional, más preciso: en BAU «new capacity follows the current spatial distribution» y los existentes se quedan (fig. 4, 6 / 7); el modelo elige solo la ubicación de la capacidad nueva. |
| O3 | CORRECTA | «The FLEX strategy significantly reduces this additional cost by 16.3%, 19.7%, and 17.9% … ILA strategy reduces additional system costs by 11.7%, 14.1%, and 11.6%» | 5 / 6 | Ninguna. Base confirmada: «this additional cost» es el aumento del costo del sistema por los data centers en BAU frente a NoDC en 2050 (BAU suma 2,5–12,2 % al costo total), no el costo total. 11,6 % → «12 %» es redondeo válido. |
| O4 | CORRECTA | PDF: «Cell Reports Sustainability 3, 100823, September 25, 2026 … https://doi.org/10.1016/j.crsus.2026.100823». Crossref: vol. 3, issue 9, art. 100823, 2026-09 | 1 / 2 (y hoja 1) | Ninguna (título y autores idénticos a Crossref). |
| S1 | CORRECTA | «co-optimizes … over a 15-year horizon»; «two-stage stochastic program»; «21 buses and 42 transmission corridors»; «decisions on generation, storage, transmission, and data center siting» | 1 / 1; 8 / 8; 13 / 13 | Ninguna. Cada «bus» es una zona de transmisión de PJM («each modeled as a node»); la expansión de transmisión es la ec. (4c) y la fig. 9. |
| S2 | CORRECTA | Tabla 7: «Power System Investment … −11.72%»; «Operational Cost … −8.25%»; «evaluation is conducted using a one-year static planning instance» | 10 / 10 | Ninguna. El texto redondea a 8,3 %; la inversión total (incl. data centers) baja 12,6 %. No conjunta = data centers ubicados por precio e intensidad de carbono local y red planificada aparte (9 / 9). El resumen publicado en IJEPES (vía OpenAlex) trae las mismas cifras que el preprint (12,6 % / 8,25 %); la tabla 7 solo pudo verse en el preprint. |
| S3 | CORRECTA | Crossref: «Stochastic long-term joint decarbonization planning for power systems and data centers: A case study in PJM», Int. J. Electr. Power Energy Syst., vol. 173, art. 111377, 2025-12 | — | Ninguna (autores Shao Zhentong, Yu Nanpeng, Wong Daniel). |
| N1 | CORRECTA | «This paper compares and evaluates these three options for Britain»; resumen: «transmission pricing reform, zonal pricing and energy price discounts in export-constrained zones» | 2 / 4; 1 / 3 | Ninguna. |
| N2 | CORRECTA | «2.2 GW of data centre demand would avoid … one of the SEGL subsea links»; «£15/MWh … save 2000 x £131,370/MWyr or £263 million/yr» | 5 / 7 (HVDC: «subsea HVDC links», 4 / 6) | Ninguna. Matiz opcional: cifras para SEGL2 «built to budget», precios 2023 y demanda firme 24/7; si se construyeran líneas en tierra, el costo evitado bajaría a ~£4,68/MWh (7 / 9). |
| N3 | IMPRECISA (redacción) | «L-TNUoS charges should be negative, but instead they are collared at zero»; «for Northern Scotland … the charge would be -£34.67/kWyr» | 5 / 7 | «Topado» sugiere un techo; es un piso. Proponer: «El cargo de transmisión a la demanda tiene piso en cero: en el norte de Escocia debería ser negativo (−£34,67/kW-año), así que no premia esa ubicación». |
| N4 | CORRECTA | Portada: «EPRG Working Paper EPRG 2623 / Cambridge Working Paper in Economics CWPE2681»; «Energy Policy Research Group, University of Cambridge, 12 October 2026» | — / 1; 1 / 3 | Ninguna. Opcional: «(CWPE 2681), octubre 2026». Ojo: el archivo local se llama `wp2326` (dígitos cruzados); el número correcto es 2623 (la URL de JBS `uploads/2026/11/eprg-wp2623.pdf` responde con un PDF de 589.334 bytes, igual al local). |
| R1 | CORRECTA | Crossref: Johnston, Josiah; Henriquez-Auba, Rodrigo; Maluenda, Benjamín; Fripp, Matthias. SoftwareX, vol. 10, art. 100251, 2019-07 | — | Ninguna. |
| R2 | CORRECTA | Crossref: Fripp, Matthias. Environmental Science & Technology, vol. 46, issue 11, pp. 6371–6378; en línea 2012-05-08, impreso 2012-06-05 | — | Ninguna. |

## Resumen

- INCORRECTAS: ninguna.
- IMPRECISAS: N3 (solo redacción: «topado en cero» → «con piso en cero»).
- Matices opcionales: O2 (BAU = la capacidad nueva sigue la distribución actual; el modelo ubica solo la nueva) y N2 (cifras de SEGL2 a presupuesto, precios 2023).
