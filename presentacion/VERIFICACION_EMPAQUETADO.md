# Verificación del empaquetado (17-nov-2026)

Prueba de que la presentación se regenera desde el repositorio, sin rutas de la máquina de origen.

## Cómo se probó

1. Copia aislada: `presentacion\` copiado a una carpeta temporal, sin `node_modules\` ni `graficos\geo\`, con `casos\` y `resultados\` enlazados (junction) a los del repositorio. Así se prueba que los scripts encuentran los datos por ruta relativa desde cualquier ubicación.
2. `regenerar.ps1 -SinAnexos -Salida <temporal>\prueba.pptx`, con los resultados del repositorio a esa fecha (casos anteriores al inicio 2025, períodos 2026–2050).
3. Los anexos, aparte, con los inputs de inicio 2025 del modelo (períodos 2025–2050), que es para lo que están escritos.
4. Búsqueda de rutas absolutas (`C:\Users\...`) en todo `presentacion\` salvo `node_modules\`.

## Resultado

| Comprobación | Resultado |
|---|---|
| `npm ci` desde `package-lock.json` (pptxgenjs 4.0.1, jszip 3.10.2) | ok, 19 paquetes |
| Paso 1, `extraer_cifras.py` → `cifras.json` | ok |
| Paso 2, mapa: descarga de GADM (`geo\` ausente) y figura | ok |
| Paso 3, diagrama de red | ok |
| Paso 6, `build.js` | ok, 30 láminas |
| Ecuaciones nativas (`MML2OMML.XSL` encontrado solo) | 73 de 73 reemplazadas, 0 marcadores `{{EQn}}` restantes |
| PDF con PowerPoint | ok, 30 páginas |
| Contenido del PPTX | 9 gráficos nativos, 3 imágenes (logo, diagrama, mapa) |
| `Presentacion de avance ... .pptx/.pdf` de `presentacion\` | intactos (iguales byte a byte a los originales) |
| Rutas absolutas a `C:\Users\...` | ninguna |

Las cifras de la prueba son las de los resultados que había en el repositorio, no necesariamente las del deck incluido.

### Anexos

- `anexo_generacion.py` con los inputs de inicio 2025: `10_generacion.js` idéntico byte a byte al original.
- `anexos_tx_dc.py` con los inputs de inicio 2025:
  - con el catastro privado (`CATASTRO_DC_XLSX`): todas las comprobaciones pasan, escribe `datos\campus_escenario_propio.csv` (35 filas) y `20_transmision.js` y `30_data_centers.js` salen idénticos byte a byte a los originales;
  - sin el catastro, leyendo el CSV: las mismas comprobaciones de las reglas 1 y 2 pasan y los dos `.js` salen otra vez idénticos byte a byte.
- Con los casos del repositorio a la fecha de la prueba (períodos 2026–2050), los dos scripts se detienen en sus comprobaciones (`AssertionError: [2026, 2030, ...]` y `{'BESS_4h_ley'}`), como deben: los anexos describen los casos con inicio en 2025. Cuando el repositorio tenga esos casos, `regenerar.ps1` sin `-SinAnexos` debiera correr completo; no se probó porque aún no estaban.

## Qué no se probó

- Una máquina sin Office (debe fallar con el mensaje de `MML2OMML.XSL`).
- `regenerar.ps1` completo, con anexos, sobre los casos de inicio 2025 dentro del repositorio.
