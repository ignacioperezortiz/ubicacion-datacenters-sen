# Presentación de avance

Presentación de avance del estudio «Ubicación de data centers en el SEN» (curso Economía, Resiliencia y Mercados Energéticos, UAI, 2026-S2). Se genera con código desde los resultados del repositorio: para cambiar algo, se edita la fuente y se regenera. No se edita el PPTX a mano.

- `Presentacion de avance - Ubicacion de data centers en el SEN.pptx`: la presentación (editable, ecuaciones nativas de PowerPoint).
- `Presentacion de avance - Ubicacion de data centers en el SEN.pdf`: la misma, en PDF.

## Requisitos

- **Windows con Microsoft PowerPoint** (Office 2016 o posterior). Hace falta para dos cosas: el archivo `MML2OMML.XSL` de Office, que convierte las ecuaciones a formato nativo, y la exportación a PDF (PowerPoint por COM). Si `MML2OMML.XSL` no está en la ruta habitual, defina la variable de entorno `MML2OMML_XSL` con su ruta.
- **Node.js** 20 o posterior, con npm. `construir.ps1` instala solo los módulos (`npm ci` en `fuente\`) la primera vez.
- **Python 3.11** con `pip install -r presentacion\requirements.txt` (pandas, matplotlib, lxml, python-pptx y, solo con el catastro privado, openpyxl). `latex2mathml` va incluido en `fuente\eq\pylib\`.
- **Internet la primera vez**: `mapa_dc_2050_fig.py` descarga los límites regionales de GADM (ver «Datos de terceros»).

## Regenerar

Desde la raíz del repositorio, en PowerShell:

```powershell
pip install -r presentacion\requirements.txt
.\presentacion\regenerar.ps1               # todo: cifras, gráficos, anexos, PPTX y PDF
.\presentacion\regenerar.ps1 -SinAnexos    # sin recalcular los anexos 10/20/30
.\presentacion\regenerar.ps1 -Salida C:\temp\prueba.pptx   # escribe en otra parte
.\presentacion\regenerar.ps1 -SinPdf       # sin exportar el PDF (no abre PowerPoint)
.\presentacion\fuente\construir.ps1        # solo arma el PPTX y el PDF (tras editar textos o layout); acepta -Salida y -SinPdf
```

Antes de regenerar, cierre la presentación en PowerPoint: el PPTX y el PDF se sobrescriben y, si están abiertos, la escritura falla. `export_pdf.ps1` cierra PowerPoint al terminar solo si no quedó otra presentación abierta.

`regenerar.ps1` corre, en orden:

| Paso | Script | Lee | Escribe |
|---|---|---|---|
| 1 | `fuente\extraer_cifras.py` | `resultados\tablas\*.csv`, `casos\SIN_DC\inputs\` | `fuente\cifras.json` |
| 2 | `fuente\graficos\mapa_dc_2050_fig.py` | `resultados\tablas\ubicacion_dc.csv`, `zonas.csv`, GADM | `fuente\graficos\mapa_dc_2050.png/.svg`, `mapa_dc_2050_datos.csv` |
| 3 | `fuente\graficos\diagrama_red.py` | `resultados\tablas\zonas.csv`, `casos\SIN_DC\inputs\transmission_lines.csv` | `fuente\graficos\diagrama_red.png/.svg` |
| 4 | `fuente\anexos\anexo_generacion.py` | `casos\SIN_DC\inputs\`, `resultados\tablas\zonas.csv` | `fuente\anexos\10_generacion.js` |
| 5 | `fuente\anexos\anexos_tx_dc.py` | `casos\<CASO>\inputs\`, `fuente\datos\` | `fuente\anexos\20_transmision.js`, `30_data_centers.js`, `verificacion_transmision_dc.md` |
| 6 | `fuente\construir.ps1` | todo lo anterior | PPTX y PDF |

Todas las rutas son relativas al repositorio: los scripts encuentran `casos\` y `resultados\` subiendo desde su propia carpeta.

Los dos scripts de anexos comprueban cada cifra contra los datos y se detienen con `FALLA: ...` o `AssertionError` si algo no cuadra. Están escritos para los casos con inicio en 2025 (períodos 2025, 2027, 2030, ..., 2050). Con otros casos fallan a propósito: hay que revisar el anexo y actualizar sus comprobaciones, o regenerar con `-SinAnexos`.

`40_modelo.js` y `FORMATO.md` se escriben a mano; ningún script los toca.

## Estructura

```
presentacion\
  regenerar.ps1            regenera todo (pasos 1 a 6)
  requirements.txt         paquetes de Python
  VERIFICACION_EMPAQUETADO.md   prueba de regeneración de este paquete
  VERIFICACION_V2.md       verificación independiente de las cifras del deck (inicio 2025)
  AUDITORIA_REPRODUCIBILIDAD.md auditoría previa a la publicación: privacidad, regeneración y documentación
  fuente\
    build.js               arma el PPTX con pptxgenjs: tema, layouts y un bloque por lámina
    contenido.js           textos de motivación, búsqueda bibliográfica y referencias
    cifras.json            cifras de casos y resultados (lo escribe extraer_cifras.py)
    extraer_cifras.py      tablas del repositorio -> cifras.json
    construir.ps1          build.js -> eq\ecuaciones.py -> export_pdf.ps1
    apply_theme.js         escribe los colores del tema en el PPTX (lo llama build.js)
    export_pdf.ps1         PPTX -> PDF con PowerPoint
    render.ps1             PPTX -> una PNG por lámina, para revisar (uso: render.ps1 deck.pptx carpeta)
    package.json, package-lock.json   pptxgenjs 4.0.1 y jszip 3.10.2, versiones exactas
    logo-fic-uai.png       logo de la portada
    eq\ecuaciones.py       reemplaza los marcadores {{EQn}} por ecuaciones nativas (OMML)
    eq\omml.py             LaTeX -> MathML -> OMML con MML2OMML.XSL de Office
    eq\pylib\latex2mathml\ latex2mathml 3.81.1 (MIT), incluido
    graficos\              mapa y diagrama de red (scripts y PNG/SVG); geo\ se descarga y no se versiona
    anexos\                láminas de anexo como datos (NN_tema.js), sus scripts y verificaciones
    datos\                 copias pequeñas de datos que no están en casos\ (ver «Datos de anexos»)
    graficos_motivacion_A\, graficos_motivacion_B\   cifras de los gráficos de motivación, con su página de origen (datos.md)
    motivacion.md, motivacion_grafico.csv            borrador y datos de la motivación
    literatura\            notas de la búsqueda bibliográfica
    verificacion\          informes de verificación de cifras y referencias
```

## Cómo editar

Después de cada cambio, corra `.\presentacion\fuente\construir.ps1` desde la raíz del repositorio (o `.\presentacion\regenerar.ps1` si cambiaron los resultados) y revise el PDF. Para ver cada lámina como imagen: `.\presentacion\fuente\render.ps1 <archivo.pptx> <carpeta>` (una PNG por lámina; borra las PNG que ya estén en esa carpeta).

- **Textos y referencias de motivación y bibliografía** → `fuente\contenido.js`. Ahí están los bullets, las notas del orador, los datos de los gráficos de motivación y la lista `referencias`. Toda cifra nueva lleva su fuente en el texto y en `referencias`.
- **Cifras de casos y resultados** → salen de `fuente\cifras.json`, que escribe `extraer_cifras.py` desde `resultados\tablas\`. Nunca se escriben a mano, ni en `cifras.json` ni en `build.js`. Si falta una cifra, se agrega su cálculo en `extraer_cifras.py`, se corre `python -B presentacion\fuente\extraer_cifras.py` y se usa como `CF.<nombre>` en `build.js`.
- **Layout, colores y tema** → constantes al inicio de `fuente\build.js`:
  - `THEME.colors`: los 12 colores del tema (`dk1` texto, `dk2` texto secundario, `accent1`–`accent6`, etc.), en seis dígitos hexadecimales sin `#`. `apply_theme.js` los escribe en el PPTX y se detiene con un error si alguno no tiene ese formato. Los textos usan colores del tema (`C.text1`, `C.text2`, …; `C` es `pres.SchemeColor`), así que cambian solos al cambiar `THEME.colors`.
  - `HEX`: filetes, encabezados de tabla, grillas y grises fijos. `GRISES`: las series de los gráficos de `grafico()`, que usan también los anexos.
  - Colores escritos directamente en el código (búsquelos con la expresión regular `"[0-9A-Fa-f]{6}"`): el fondo `FFFFFF` de los maestros, `808080` y las etiquetas `FFFFFF` del gráfico de la lámina 11, y las etiquetas `FFFFFF` de los gráficos apilados en `grafico()`.
  - Los maestros (`PORTADA`, `CONTENIDO`) y el pie están en la sección «layouts». La regla de estilo es blanco y negro (ver «Reglas de estilo»).
- **Tablas y gráficos de cada lámina** → bloques numerados de `fuente\build.js`, que empiezan con una línea `// ======… N. Título` (búsquelos como `==== 11. Resultados`). Las tablas usan `acadTable(s, encabezado, filas, opciones)`: cada fila es un arreglo de celdas, que son texto o `{ text, options }` (`options: R` alinea a la derecha) y admiten `$...$`. Los gráficos nativos usan `grafico()` o `s.addChart()`. Para agregar una fila:
  - Láminas 6–8 (formulación): las filas están escritas en el bloque; se agrega un arreglo más a la lista de filas de `acadTable`.
  - Láminas 11 y 13 (resultados): las filas se arman desde `cifras.json` (`CF.escenarios`, `CF.ubicacion_por_zona`, …). Una fila nueva es una cifra nueva: se agrega en `extraer_cifras.py` (ver «Cifras de casos y resultados») y luego en el `map` que arma las filas del bloque.
  - Anexos: en el bloque `tabla` del `.js` (`filas`), o en su script si es `10_`, `20_` o `30_`.
  - Cada fila ocupa unos 0,29–0,31 in (letra de 11–12 pt) y el área útil termina en y = 6,55 in; revise con `render.ps1` que la tabla no se salga de la lámina.
- **Ecuaciones** → en cualquier texto de `build.js` o `contenido.js`, lo que va entre `$...$` es LaTeX y queda como ecuación nativa y editable.
- **Anexos** → `fuente\anexos\NN_tema.js` según `fuente\anexos\FORMATO.md` (esquema de datos, área útil y alto por fila). `build.js` incluye todos los `NN_*.js` de la carpeta en orden de nombre, así que un anexo nuevo es un archivo nuevo (por ejemplo, `50_tema.js`). `10_`, `20_` y `30_` se regeneran con sus scripts: los cambios de contenido van en el script (`anexo_generacion.py`, `anexos_tx_dc.py`), no en el `.js`; después se corre ese script (`python -B presentacion\fuente\anexos\<script>.py`) y `construir.ps1`. `40_modelo.js` se edita a mano.

### Imágenes y gráficos nativos

- **Imágenes** (3): el logo, `graficos\diagrama_red.png` (lámina 9) y `graficos\mapa_dc_2050.png` (lámina 12). Para cambiarlas, se edita su script de Python y se regenera.
- **Gráficos nativos de PowerPoint** (9 en la versión actual, editables en PowerPoint): los de motivación (datos en `contenido.js`), el de costo extra y ahorro (lámina 11), los de expansión del sistema (lámina 14) y los de los anexos. Se definen en `build.js` y en los `.js` de anexos.
- **Tablas**: todas son tablas nativas.

## Reglas de estilo

- Blanco y negro: texto negro, grises para jerarquía, filetes rectos. Sin rellenos de color.
- Académico: tablas con filetes horizontales y sin verticales, ecuaciones nativas, siglas explicadas, citas autor-año.
- Pocas cifras en la motivación: una idea por lámina y las cifras justas para sostenerla.
- Toda cifra externa cita su fuente en la lámina (pie del gráfico o paréntesis autor-año) y aparece en `referencias`.
- Las cifras del estudio salen de `cifras.json` o de los scripts de anexos, que las comprueban contra los datos.

## Fuentes de la motivación

Las cifras de motivación vienen de documentos públicos. Los PDF no se incluyen en el repositorio (derechos de autor); las cifras extraídas y su página están en `fuente\graficos_motivacion_A\datos.md`, `fuente\graficos_motivacion_B\datos.md` y `fuente\motivacion.md`, y su verificación en `fuente\verificacion\motivacion_verificador.md`.

- Comisión Nacional de Energía. (2026). Reporte mensual ERNC: septiembre 2026 (Vol. 121).
- Coordinador Eléctrico Nacional. (s. f.). Plataforma de Acceso Abierto: solicitudes de conexión [Base de datos]. Consultada el 13 de noviembre de 2026.
- Coordinador Eléctrico Nacional. (2026a). Proyección de demanda de largo plazo SEN 2026–2046.
- Coordinador Eléctrico Nacional. (2026b). Reporte anual de desempeño del Sistema Eléctrico Nacional, año 2025.
- International Energy Agency. (2025). Energy and AI.
- Ministerio de Energía. (2025). Planificación Energética de Largo Plazo 2023–2027: Informe definitivo.
- Ministerio de Energía. (2026a). Planificación Energética de Largo Plazo 2028–2032: Informe preliminar.
- Ministerio de Energía. (2026b). Reporte de proyectos: junio 2026.
- Shehabi, A., et al. (2024). 2024 United States data center energy usage report (LBNL-2001637). Lawrence Berkeley National Laboratory.

La lista completa de referencias de la presentación, con la literatura (Newbery, Onodera et al., Shao et al., Johnston et al.), está en `referencias` de `fuente\contenido.js`.

## Datos de anexos

`fuente\datos\` guarda copias pequeñas de lo que usa `anexos_tx_dc.py` y no está en `casos\`:

- `campus_escenario_propio.csv`: las 35 solicitudes vigentes con fecha que usa el escenario propio, con la clase que les dan las reglas del anexo (`existente`, `repetida`, `sin_mw`, `incluida`). Origen: catastro de solicitudes de conexión del CEN cruzado con el SEIA, elaborado por Raúl Ugarte. El catastro completo (`Catastro_DataCenters_CEN_SEIA.xlsx`) es privado y no se versiona. Si se tiene, se deja en `fuente\datos\` o se indica con la variable `CATASTRO_DC_XLSX`; el script lo lee y reescribe este CSV con la misma lógica. Sin él, el script lee el CSV y comprueba que las clases coinciden. Las dos vías dan los mismos `20_transmision.js` y `30_data_centers.js`, byte a byte.
- `inversion_ameba_hasta_2025.csv`: los 2.672 MW de transmisión que AMEBA construyó hasta 2025 en 7 corredores, que ya no entran como existentes; el anexo de transmisión lo menciona en sus notas. Los datos de la PELP (por ejemplo, la lista de líneas de AMEBA) no se publican en este repositorio; con ellos, `anexos_tx_dc.py` corre además una verificación de trazabilidad que aquí se omite.
- `resumen_escenarios_dc.csv`: resumen del script de escenarios de data centers; el anexo comprueba contra él la demanda agregada al modelo.

## Datos de terceros

- **Límites regionales (GADM 4.1)**: el mapa usa `gadm41_CHL_1.json.zip` de https://geodata.ucdavis.edu/gadm/gadm4.1/json/. La licencia de GADM no permite redistribuir los datos, así que `fuente\graficos\geo\` va en `.gitignore` y `mapa_dc_2050_fig.py` lo descarga si falta. La PNG y la SVG del mapa sí se versionan.
- **latex2mathml 3.81.1** (licencia MIT), incluido en `fuente\eq\pylib\`.
- **pptxgenjs 4.0.1** (MIT), se instala con npm.
