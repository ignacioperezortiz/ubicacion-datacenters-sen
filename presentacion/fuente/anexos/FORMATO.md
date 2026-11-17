# Formato de las láminas de anexo

Cada tema es un módulo CommonJS en esta carpeta, `NN_tema.js`, que exporta una lista de láminas. `build.js` las dibuja con el mismo estilo del deck: blanco y negro, Calibri, tablas académicas con filetes horizontales y gráficos nativos en grises. Tú no escribes código de pptxgenjs: solo datos con este esquema.

```js
module.exports = [
  {
    titulo: "Anexo: parque generador candidato",        // directo, ≤ 45 caracteres, sin mensajes
    subtitulo: "Tecnologías en que el modelo puede invertir, por zona",   // bajada, ≤ 110 caracteres
    columnas: [                                          // 1 o 2 columnas
      { ancho: 7.2, bloques: [ /* bloques, de arriba hacia abajo */ ] },
      { ancho: 4.48, bloques: [ /* ... */ ] },
    ],
    fuente: "Fuente: Ministerio de Energía (2025), escenario Carbono Neutralidad.",  // opcional, una línea
    notas: "Notas del orador: detalle, siglas, advertencias.",                      // opcional
  },
];
```

**Área útil:** 12,13 in de ancho por 4,8 in de alto (de y = 1,75 a 6,55 in). Con dos columnas, la separación es de 0,45 in y la suma de los anchos debe ser 11,68 in. Con una columna, el ancho es 12,13 in. Los bloques se apilan con 0,15 in entre ellos y **no pueden pasarse del alto útil**: haz la cuenta.

## Bloques

- **Tabla:** `{ tipo: "tabla", header: ["Zona", "FV", ...], filas: [["Kimal 220", "1.200", ...], ...], anchos: [2.2, 1.0, ...], letra: 12, derecha: [1, 2], total: false }`
  - `anchos` suma el ancho de la columna. `derecha`: índices de las columnas alineadas a la derecha (números). `total: true` pone en negrita la última fila.
  - Cada celda cabe en **una línea**: unos 14 caracteres por pulgada a 12 pt y 16 a 11 pt.
  - Alto por fila (encabezado incluido): 0,31 in a 12 pt, 0,29 in a 11 pt, 0,34 in a 14 pt. Con 4,8 in caben unas 15 filas a 12 pt. Si no caben, parte en dos láminas o agrega.
  - Las celdas admiten LaTeX entre `$...$` para símbolos.
- **Viñetas:** `{ tipo: "bullets", items: ["...", { text: "...", sub: true }], letra: 14 }` (12 a 16 pt). Alto ≈ líneas × letra × 1,25 / 72 + 0,08 por ítem. Unos 12 caracteres por pulgada a 14 pt.
- **Gráfico nativo:** `{ tipo: "grafico", forma: "columnas" | "barras" | "lineas" | "columnas_apiladas" | "barras_apiladas", titulo: "...", etiquetas: ["2026", ...], series: [{ nombre: "...", valores: [1, 2, ...] }], eje: "USD/kW", alto: 3.5, formato: "#,##0", etiquetas_datos: false }`. Máximo 4 series (van en grises). Alto entre 2,5 y 4,8 in, título incluido.
- **Texto:** `{ tipo: "texto", texto: "...", letra: 12, gris: true }`, para una nota corta o un rótulo.

## Reglas de redacción

- **Idioma y estilo:** español, estilo académico directo, sin metacomentarios. Títulos sin mensajes ocultos («Anexo: corredores de transmisión»). El subtítulo es una bajada, no una conclusión.
- **Números:** coma decimal y punto de miles (1.234,5); unidades con espacio (MW, USD/kW, %). En las tablas, los números van como texto ya formateado.
- **Densidad:** poca. Son láminas de respaldo para responder preguntas, pero se leen en pantalla. Mejor dos láminas legibles que una repleta.
- **Autocontenidas:**
  - No se nombran archivos locales, carpetas, scripts, repositorios ni GitHub (nada de «gen_info.csv»).
  - Las fuentes se citan como institución o documento:
    - Ministerio de Energía (2025) = PELP 2023–2027, Informe definitivo, datos del modelo AMEBA, escenario Carbono Neutralidad;
    - Ministerio de Energía (2026a) = PELP 2028–2032, Informe preliminar;
    - CEN (2026a) = Proyección de demanda 2026–2046;
    - CEN (s. f.) = Plataforma de Acceso Abierto, solicitudes de conexión;
    - «elaboración propia».
- **Siglas:** se explican una vez, en `notas` o en un bloque de texto.
- **Datos:** toda cifra sale de los datos o documentos indicados en el encargo y se comprueba con un script. Nada inventado ni estimado a ojo.
