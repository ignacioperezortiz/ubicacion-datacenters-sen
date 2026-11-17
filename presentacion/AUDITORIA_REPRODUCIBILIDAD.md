# Auditoría de reproducibilidad antes de publicar

17-nov-2026. Auditoría independiente del repositorio antes de subirlo a GitHub, sobre el árbol de trabajo con los cambios sin commit (380 modificados, 4 borrados, 84 archivos nuevos). Universo revisado: lo que entraría al commit, es decir `git ls-files -c -o --exclude-standard` (528 archivos existentes).

## Resultado

| Comprobación | Resultado |
|---|---|
| 1. Privacidad, licencias y tamaño | Sin problemas bloqueantes |
| 2. Tablas regenerables sin resolver | Sí: las 27 tablas regeneradas son idénticas byte a byte |
| 3. Presentación regenerable | Sí, después de corregir `construir.ps1` (ver «Cambios hechos») |
| 4. Documentación coherente con el código | Sí, salvo detalles de `presentacion\README.md`, ya corregidos |
| 5. Instrucciones de edición | Tenían vacíos; completadas en `presentacion\README.md` |

## 1. Privacidad, licencias y tamaño

- **Rutas locales** (`C:\Users`, nombre del equipo, `OneDrive`, `AppData`): ninguna en los archivos de texto, en las partes XML del PPTX, en los metadatos del PDF, en las SVG ni en las PNG. Las únicas rutas absolutas son ejemplos (`C:\temp\prueba.pptx`, `C:\tmp\x.pptx`) y `C:\Windows` como respaldo de `%WINDIR%` en `mapa_dc_2050_fig.py`.
- **Correos y credenciales**: ningún `@gmail`, `@uai`, `@edu`, clave, token ni `gurobi.lic`. Los registros de Gurobi (`casos\*\log_*.txt`, `casos\corrida_2025.txt`) no tienen líneas de licencia. El único correo es el del autor de latex2mathml en su `METADATA`, que es público.
- **Nombres**: los cuatro integrantes figuran como autores en `build.js` y en los metadatos del PPTX y del PDF, y Raúl Ugarte en el `README.md`. Es autoría, no un dato privado.
- **Datos de terceros**: no hay PDF con derechos de autor (el único PDF es la presentación), ni datos GADM (`graficos\geo\` está en `.gitignore`), ni el catastro privado (`datos\*.xlsx` en `.gitignore`), ni datos crudos de PELP/AMEBA. Lo que hay son entradas traducidas a Switch en `casos\` y tablas pequeñas derivadas.
- **Tamaño**: el archivo más grande pesa 8,8 MB (`variable_capacity_factors.csv`, uno por caso). Ninguno pasa de 50 MB.

## 2. Tablas y figuras sin volver a resolver

Copia de los archivos versionables en una carpeta temporal; desde su raíz, con Python 3.11.9, pandas 3.0.3 y matplotlib 3.11.1:

```
python -I scripts/resultados.py        # 2 s
python -I scripts/tiempos_computo.py   # 1 s
python -I scripts/analisis.py          # 6 s
python -I scripts/graficos.py          # 6 s
```

- Las 27 tablas de `resultados\tablas\*.csv` salen **idénticas byte a byte**, así que cumplen la tolerancia relativa de 1e-9.
- Las 11 PNG de `resultados\figuras\` también salen idénticas. Las 11 SVG cambian solo en la fecha (`dc:date`) y en los identificadores aleatorios de `clip-path`.

## 3. Presentación

En la copia, sin `node_modules\` ni `graficos\geo\`, como queda un clon recién hecho: `.\presentacion\regenerar.ps1 -Salida <temp>\deck.pptx`, con Node 20.20.2, npm 10.8.2, lxml 6.1.3, python-pptx 1.0.2 y PowerPoint por COM.

- **Primer intento: falló en el paso 6.** `npm ci` escribe `npm notice` en stderr. Con `$ErrorActionPreference = 'Stop'` y la salida redirigida, Windows PowerShell 5.1 lo convierte en error y detiene el script, aunque npm terminó bien. Es el caso de un agente (Claude) que corre el script y captura su salida. Se corrigió `construir.ps1` (ver «Cambios hechos»).
- **Segundo intento, desde cero: completo, en 12 s.** Descargó GADM, instaló los módulos con `npm ci`, insertó 73 ecuaciones y exportó el PDF. PowerPoint no estaba abierto y el script lo cerró al terminar.
- **`cifras.json`**: idéntico byte a byte al del repositorio.
- **Anexos regenerados** (`10_generacion.js`, `20_transmision.js`, `30_data_centers.js`, `verificacion_transmision_dc.md`), `mapa_dc_2050.png`, `mapa_dc_2050_datos.csv` y `diagrama_red.png`: idénticos. Las SVG cambian solo en la fecha y los identificadores.
- **Deck**: 30 láminas. Con python-pptx, los textos, las 174 filas de tabla, los datos de las 23 series de gráficos, las notas (25 láminas las tienen) y la posición y el tamaño de cada forma son **idénticos** a los del PPTX del repositorio. Los bytes difieren solo en las fechas de `docProps/core.xml`, los GUID de las secciones en `presentation.xml` y las fechas internas de los 9 Excel incrustados. El PDF tiene 30 páginas, igual que el del repositorio.
- **Pasos no documentados**: ninguno, salvo los que se agregaron al README (cerrar el deck en PowerPoint antes de regenerar; `-SinPdf`).

## 4. Documentación y código

- **`README.md`**:
  - Las opciones de `correr_casos.py` existen en su argparse: `escenarios`, `--modos`, `--paralelo` (3 por omisión), `--hilos` (6 por omisión), `--casos`, `--dc-libre-desde` (2030) y `--solver`.
  - Los cuatro scripts de resultados corren sin argumentos, como dice el README.
  - Horizonte: `periods.csv` tiene 7 períodos, de 2025 (2025–2026) a 2050 (2050–2054), iguales en los 5 casos. `financials.csv` tiene año base 2025 y tasa de 6 %.
  - La tabla de resultados principales coincide con `costos.csv`: sin data centers 42.618,8; y en cada escenario, el costo extra base y libre, el ahorro, el porcentaje del extra y los USD/MWh. También coinciden el rango del 17 % al 28 % y los 11,9–14,9 USD/MWh reubicado de `docs\ANALISIS.md`.
  - Tamaño del problema (1.542.353 × 1.346.239, con 8.072.244 coeficientes; 890.197 × 995.883 tras el presolve) y 115 min en serie: coinciden con `tiempos_computo.csv` y con la salida de `tiempos_computo.py`.
- **Enlaces de `README.md`**: los 8 relativos existen y los 2 externos (Switch en GitHub y la licencia académica de Gurobi) responden 200.
- **`presentacion\README.md`**:
  - Los parámetros documentados existen (`-Salida`, `-SinAnexos`), igual que las variables `MML2OMML_XSL` (en `omml.py`) y `CATASTRO_DC_XLSX` (en `anexos_tx_dc.py`) y los nombres de `build.js` (`THEME`, `HEX`, `GRISES`, `acadTable`, `grafico`, `PORTADA`, `CONTENIDO`).
  - Errores corregidos: los bloques no empiezan con `// ===== 1. Portada` (la línea real es `// ====…==== 1. Portada`); «agregar al arreglo `rows`» no sirve para las tablas de resultados, que se arman desde `cifras.json`; faltaban `-SinPdf` y `VERIFICACION_V2.md`.

## 5. Instrucciones de edición

Antes de la corrección, con solo `presentacion\README.md`, un agente:

- **Podía editar o agregar un anexo**, porque `FORMATO.md` está bien.
- **Encontraba los colores**, pero no sabía que hay colores escritos directamente en el código (`808080` en la lámina 11, `FFFFFF` en fondos y etiquetas), que `C.text1` y los demás son colores del tema ni que `apply_theme.js` exige seis dígitos hexadecimales sin `#`.
- **Agregaba mal una fila** a las tablas de las láminas 11 y 13: buscaría un arreglo `rows` que no existe y escribiría una cifra a mano, contra la regla del README.

Ahora el README cubre los tres casos: dónde están los colores y su formato; cómo agregar una fila según el tipo de tabla (escrita en el bloque, armada desde `cifras.json` o en un anexo), con el alto por fila y el límite inferior; y cómo agregar o regenerar un anexo. También dice cómo revisar el resultado con `render.ps1` y desde dónde se corre cada comando.

## Cambios hechos

1. `presentacion\fuente\construir.ps1`: `npm ci` se corre con `$ErrorActionPreference = 'Continue'` y `2>&1`, y solo su código de salida decide si falló. Con eso, los avisos de npm en stderr ya no detienen la construcción cuando la salida está redirigida. Se probó desde cero en la copia temporal.
2. `presentacion\README.md`:
   - «Regenerar»: se agregaron `-SinPdf` (en `regenerar.ps1` y `construir.ps1`) y el aviso de cerrar el deck en PowerPoint antes de regenerar.
   - «Estructura»: se agregaron `VERIFICACION_V2.md` y este archivo.
   - «Cómo editar»: comandos desde la raíz y `render.ps1` para revisar; el comando para regenerar `cifras.json`; el detalle de colores (`THEME.colors`, `C` = colores del tema, formato hexadecimal, colores escritos en el código); el marcador real de los bloques; la firma de `acadTable` y cómo agregar una fila según el tipo de tabla; y cómo agregar o regenerar un anexo.
3. Este archivo, `presentacion\AUDITORIA_REPRODUCIBILIDAD.md`.

No se hizo commit ni push.

## Notas menores (sin corregir)

- **Mismo riesgo que con npm en los pasos de Python**: `Paso` en `regenerar.ps1` y las llamadas a `node` y `python` en `construir.ps1` tienen el mismo problema. Si Python o Node escriben un aviso en stderr (por ejemplo, un `FutureWarning` con otra versión de pandas) y la salida está redirigida, el script se detiene aunque el paso haya terminado bien. Hoy no escriben nada en stderr. Se arregla con el mismo patrón de `construir.ps1`.
- **`construir.ps1` cambia de carpeta**: hace `Set-Location $PSScriptRoot`, y al llamarlo con `&` la sesión queda en `presentacion\fuente\`.
- **Salidas que no son deterministas**: las SVG (fecha y `clip-path`) y el PPTX (fechas, GUID de secciones, Excel incrustados) cambian en cada regeneración aunque el contenido sea el mismo, lo que ensucia los diffs de git. Para las SVG bastaría `plt.rcParams['svg.hashsalt']` fijo y `metadata={'Date': None}`.
- **Licencia de latex2mathml**: la copia incluida en `eq\pylib\` declara MIT en `METADATA`, pero no trae el texto de la licencia. La MIT pide incluir el aviso: conviene agregar un `LICENSE` en `latex2mathml-3.81.1.dist-info\`.
- **Versión de pandas**: `requirements.txt` fija pandas 3.1.1 y la verificación usó 3.0.3. Las tablas salieron idénticas igual.
- **Borrados**: hay 4 archivos versionados que se borraron (`casos\corrida_1_casos_base.txt` a `corrida_4_propio.txt`). El commit debe incluir esos borrados (`git add -A`).
- **Internet en la primera regeneración**: hace falta para GADM y para `npm ci`. Está documentado.
