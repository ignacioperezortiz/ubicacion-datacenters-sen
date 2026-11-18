// Presentación de avance del proyecto «Ubicación de data centers en el Sistema Eléctrico Nacional».
// Curso Economía, Resiliencia y Mercados Energéticos (UAI, 2026-S2). Versión 1 (17-nov-2026).
// Estilo: blanco y negro, plano, con filetes rectos; Calibri; logo de la Facultad de Ingeniería y Ciencias en la portada.
// Contenido:
//   - motivación y búsqueda bibliográfica: contenido.js (redactado y verificado por agentes, con fuentes);
//   - formulación, casos y resultados: estudio con Switch (tablas de resultados del estudio, VP 2026).
// Uso: construir.ps1. En los textos, lo que va entre $...$ es LaTeX y queda como ecuación nativa de PowerPoint.
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");
const { applyTheme } = require("./apply_theme.js");
const K = require("./contenido.js");

const HERE = __dirname;
const LOGO = path.join(HERE, "logo-fic-uai.png");          // 4900 x 1111 px
const OUT = process.argv[2] || path.join(HERE, "deck.pptx");
const FECHA = "17 de noviembre de 2026";
const CURSO = "Economía, Resiliencia y Mercados Energéticos";

// ---------------------------------------------------------------- tema (blanco y negro)
const THEME = {
  name: "UAI blanco y negro",
  headFontFace: "Calibri",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "111111", lt1: "FFFFFF", dk2: "595959", lt2: "F2F2F2",
    accent1: "111111", accent2: "7F7F7F", accent3: "A6A6A6", accent4: "D9D9D9",
    accent5: "404040", accent6: "BFBFBF", hlink: "111111", folHlink: "595959",
  },
};
const HEX = { rule: "111111", hair: "BFBFBF", head: "F2F2F2", grid: "E6E6E6", gray: "7F7F7F", light: "BFBFBF" };

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13,33 x 7,5 in
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "Ubicación de data centers en el Sistema Eléctrico Nacional · Presentación de avance";
pres.author = "Ignacio Pérez, Vicente Martínez, Sebastián San Martín, Raúl Ugarte";
const C = pres.SchemeColor;

const X0 = 0.6, XR = 12.73, W = XR - X0, YC = 1.75, YB = 6.7;

// espacios no separables: autor y año, número y unidad
const NB = (t) => t
  .replace(/([A-Za-zÀ-ÿ\-\.]+) (\d{4})(?![\d.,])/g, "$1 $2")
  .replace(/(\d) (kW|kWh|MWh|GWh|TWh|MW|GW|MVA|km|min|h|%|USD|MMUSD|Mt|t)(?![a-záéíóú])/g, "$1 $2");

// ---------------------------------------------------------------- ecuaciones
const EQS = {};
let EQN = 0;
const SCHEME_HEX = { tx1: THEME.colors.dk1, tx2: THEME.colors.dk2, bg1: THEME.colors.lt1, bg2: THEME.colors.lt2 };
const hexOf = (c) => SCHEME_HEX[c] || THEME.colors[c] || THEME.colors.dk1;
function eq(latex, o) {
  const id = String(++EQN);
  EQS[id] = { latex, size: o.fontSize || 16, color: hexOf(o.color) };
  return { text: `{{EQ${id}}}`, options: { ...o } };
}
function rich(text, o = {}) {
  const out = [];
  text.split(/\$([^$]+)\$/).forEach((seg, i) => {
    if (seg) out.push(i % 2 ? eq(seg, o) : { text: NB(seg), options: { ...o } });
  });
  return out;
}

// ---------------------------------------------------------------- layouts
const FOOTER = [
  { line: { x: X0, y: 6.98, w: W, h: 0, line: { color: HEX.light, width: 0.75 } } },
  { text: { text: `Presentación de avance · ${CURSO} · ${FECHA}`, options: { x: X0, y: 7.04, w: 10, h: 0.28,
      fontSize: 10, color: C.text2, margin: 0, valign: "middle" } } },
];
pres.defineSlideMaster({
  title: "PORTADA",
  background: { color: "FFFFFF" },
  objects: FOOTER,
});
pres.defineSlideMaster({
  title: "CONTENIDO",
  background: { color: "FFFFFF" },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: X0, y: 0.42, w: W, h: 0.62,
        fontSize: 30, bold: true, color: C.text1, valign: "middle", align: "left", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "sub", type: "body", x: X0, y: 1.05, w: W, h: 0.4,
        fontSize: 16, color: C.text2, valign: "middle", align: "left", margin: 0 }, text: "" } },
    ...FOOTER,
  ],
  slideNumber: { x: XR - 0.6, y: 7.04, w: 0.6, h: 0.28, fontSize: 10, color: C.text2, align: "right" },
});

// ---------------------------------------------------------------- utilidades
const tb = (s, text, o) => s.addText(text, Object.assign({ margin: 0, isTextBox: true, color: C.text1, valign: "top" }, o));
function bullets(items, { size = 16, after = 8, color, indent = 16 } = {}) {
  return items.flatMap((it, i) => {
    const sub = typeof it === "object" && it.sub;
    const txt = typeof it === "object" ? it.text : it;
    const runs = rich(txt, Object.assign({ fontSize: sub ? size - 2 : size }, color ? { color } : {}));
    runs[0].options.bullet = sub ? { indent, characterCode: "2013" } : { indent };
    runs[0].options.indentLevel = sub ? 1 : 0;
    runs[0].options.paraSpaceAfter = after;
    if (i !== items.length - 1) runs[runs.length - 1].options.breakLine = true;
    return runs;
  });
}
const label = (t, o = {}) => ({ text: NB(t), options: Object.assign({ bold: true, fontSize: 16, breakLine: true, paraSpaceAfter: 6 }, o) });
const hrule = (s, x, y, w, color = HEX.light) => s.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color, width: 0.75 } });
const vrule = (s, x, y, h) => s.addShape(pres.shapes.LINE, { x, y, w: 0, h, line: { color: HEX.light, width: 0.75 } });
const box = (s, x, y, w, h, o = {}) => s.addShape(pres.shapes.RECTANGLE, Object.assign({ x, y, w, h,
  fill: { color: o.fill || "FFFFFF" }, line: { color: o.line || HEX.rule, width: o.width || 1 } }, o.extra || {}));

// tabla académica: filetes horizontales, sin verticales; celdas con $...$ admiten ecuaciones
function acadTable(s, header, rows, o) {
  const n = rows.length;
  const none = { type: "none" };
  const top = { type: "solid", pt: 1.25, color: HEX.rule };
  const mid = { type: "solid", pt: 0.75, color: HEX.rule };
  const hair = { type: "solid", pt: 0.5, color: HEX.hair };
  const fs = o.fontSize || 14;
  const cell = (c, extra) => {
    const base = { fontSize: fs, color: C.text1, valign: "middle", margin: o.margin || [4, 6, 4, 6] };
    const isObj = c && typeof c === "object";
    if (isObj && c.runs) return { text: c.runs, options: Object.assign(base, extra) };
    const str = isObj ? c.text : String(c);
    const copts = (isObj && c.options) || {};
    const opts = Object.assign(base, extra, copts);
    const text = str.includes("$") ? rich(str, { fontSize: fs, color: opts.color, bold: !!opts.bold }) : NB(str);
    return { text, options: opts };
  };
  const data = [];
  if (header) data.push(header.map((h) => cell(h, { bold: true, fill: { color: HEX.head }, border: [top, none, mid, none] })));
  rows.forEach((r, i) => data.push(r.map((c) => cell(c, {
    border: [!header && i === 0 ? top : none, none, i === n - 1 ? top : hair, none] }))));
  s.addTable(data, { x: o.x, y: o.y, w: o.w, colW: o.colW, autoPage: false });
}

let SECCION = null;
function content(sec, title, sub) {
  if (sec !== SECCION) { pres.addSection({ title: sec }); SECCION = sec; }
  const s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: sec });
  s.addText(NB(title), { placeholder: "title" });
  if (sub) s.addText(NB(sub), { placeholder: "sub" });
  return s;
}
const fuente = (s, t, y = 6.5) => tb(s, NB(t), { x: X0, y, w: W, h: 0.35, fontSize: 11, color: C.text2, valign: "bottom" });
const R = { align: "right" };

// ---------------------------------------------------------------- cifras de casos y resultados (extraer_cifras.py -> cifras.json)
const CF = JSON.parse(fs.readFileSync(path.join(HERE, "cifras.json"), "utf-8"));
const fnum = (x, d = 0) => {
  const p = Math.abs(x).toFixed(d).split(".");
  p[0] = p[0].replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  return (x < 0 ? "−" : "") + p.join(",");
};
const rango = (arr, d = 0, sep = "–") => {
  const a = Math.min(...arr), b = Math.max(...arr);
  return fnum(a, d) === fnum(b, d) ? fnum(a, d) : `${fnum(a, d)}${sep}${fnum(b, d)}`;
};
const PER = CF.periodos, ULT = PER[PER.length - 1];
const FIN = CF.periodos_rango[CF.periodos_rango.length - 1].split("–")[1];
const VP = `VP ${CF.anio_base}`;
const SUR = CF.macrozonas_elegidas.every((m) => m === "Sur" || m === "Centro-Sur");
// Qué cambia en la expansión: tecnologías con el mismo signo en los 4 escenarios
const mas = [], menos = [];
const MINUS = { "Eólica": "eólica", "Solar FV": "solar FV", "Baterías": "baterías", "Bombeo": "bombeo", "Transmisión": "transmisión" };
Object.entries(CF.cambio_capacidad).forEach(([t, v]) => {
  if (v.every((x) => x > 0)) mas.push(MINUS[t] || t);
  else if (v.every((x) => x < 0)) menos.push(MINUS[t] || t);
});
const lista = (a) => a.length <= 1 ? a.join("") : `${a.slice(0, -1).join(", ")} y ${a[a.length - 1]}`;
const QUE_CAMBIA = [mas.length ? `más ${lista(mas)}` : "", menos.length ? `menos ${lista(menos)}` : ""].filter(Boolean).join(" y ");

// Dónde queda la ubicación óptima: macrozonas comunes a los 4 escenarios y las que agrega cada uno
const MZ = (m) => ({ "Norte Grande": "norte grande", "Norte Chico": "norte chico", "Centro": "centro", "Centro-Sur": "centro-sur", "Sur": "sur" }[m] || m);
const MZ_ESC = CF.macrozonas_por_escenario;
const MZ_TODOS = CF.macrozonas_elegidas.filter((m) => CF.escenarios.every((e) => MZ_ESC[e].includes(m)));
const MZ_ALGUNOS = CF.macrozonas_elegidas.filter((m) => !MZ_TODOS.includes(m))
  .map((m) => ({ m, esc: CF.escenarios.filter((e) => MZ_ESC[e].includes(m)) }));
const DONDE = (MZ_TODOS.length ? `La ubicación óptima está en el ${lista(MZ_TODOS.map(MZ))} en los cuatro escenarios` : "La ubicación óptima cambia según el escenario")
  + MZ_ALGUNOS.map(({ m, esc }) => `; en ${lista(esc)}, también en el ${MZ(m)}`).join("");
const PRECIO_MZ = CF.macrozonas_elegidas.slice().sort((a, b) => CF.precio_2040_por_macrozona[a][0] - CF.precio_2040_por_macrozona[b][0])
  .map((m) => `${rango(CF.precio_2040_por_macrozona[m], 1)} USD/MWh en el ${MZ(m)}`);


// ================================================================ 1. Portada
{
  pres.addSection({ title: "Portada" }); SECCION = "Portada";
  const s = pres.addSlide({ masterName: "PORTADA", sectionTitle: "Portada" });
  s.addImage({ path: LOGO, x: X0, y: 0.5, w: 4.41, h: 1.0, altText: "Universidad Adolfo Ibáñez, Facultad de Ingeniería y Ciencias" });
  tb(s, "PRESENTACIÓN DE AVANCE", { x: X0, y: 2.05, w: W, h: 0.35, fontSize: 14, bold: true, color: C.text2, charSpacing: 2 });
  tb(s, [{ text: "Ubicación de data centers en el", options: { breakLine: true } }, { text: "Sistema Eléctrico Nacional" }],
    { x: X0, y: 2.4, w: W, h: 1.4, fontSize: 40, bold: true, valign: "top", lineSpacingMultiple: 0.95 });
  tb(s, "Planificación de generación y transmisión con la ubicación de la demanda como variable de decisión",
    { x: X0, y: 3.88, w: W, h: 0.45, fontSize: 20, color: C.text2 });
  hrule(s, X0, 4.6, W, HEX.rule);
  const col = (x, titulo, lineas, w) => tb(s, [
    { text: titulo, options: { fontSize: 12, bold: true, color: C.text2, charSpacing: 1, breakLine: true, paraSpaceAfter: 6 } },
    ...lineas.map((l, i) => ({ text: l, options: { fontSize: 18, breakLine: i < lineas.length - 1, paraSpaceAfter: 2 } })),
  ], { x, y: 4.82, w, h: 1.75, valign: "top" });
  col(X0, "INTEGRANTES", ["Ignacio Pérez", "Vicente Martínez", "Sebastián San Martín", "Raúl Ugarte"], 4.6);
  vrule(s, X0 + 5.0, 4.85, 1.7);
  col(X0 + 5.35, "PROFESOR", ["Rodrigo Moreno"], 3.0);
  col(X0 + 5.35 + 3.2, "AYUDANTE", ["Yerko Orellana"], 3.0);
  tb(s, [{ text: CURSO, options: { fontSize: 16, breakLine: true } }, { text: "Universidad Adolfo Ibáñez · 2026", options: { fontSize: 16, color: C.text2 } }],
    { x: X0 + 5.35, y: 5.8, w: 6.5, h: 0.75, valign: "top" });
}

// ---------------------------------------------------------------- gráficos nativos en grises (cuerpo y anexos)
const GRISES = [HEX.rule, "595959", "A6A6A6", "D9D9D9"];
function grafico(s, g, x, y, w, h) {
  let yy = y, hh = h;
  if (g.titulo) {
    tb(s, NB(g.titulo), { x: x + 0.05, y, w: w - 0.05, h: 0.5, fontSize: 13, bold: true });
    yy += 0.52; hh -= 0.52;
  }
  const forma = g.forma || "columnas";
  const tipo = forma === "lineas" ? pres.charts.LINE : pres.charts.BAR;
  const series = g.series.map((d) => ({ name: d.nombre, labels: g.etiquetas, values: d.valores }));
  const fmt = g.formato || "#,##0";
  const apil = forma.endsWith("apiladas");
  const o = {
    x, y: yy, w, h: hh,
    chartColors: (g.colores || GRISES).slice(0, series.length),
    catAxisLabelFontSize: 11, valAxisLabelFontSize: 10, catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt",
    catAxisLabelColor: THEME.colors.dk1, valAxisLabelColor: THEME.colors.dk2, valAxisLineShow: false, valAxisLabelFormatCode: fmt,
    valGridLine: { color: HEX.grid, size: 0.5 }, catGridLine: { style: "none" },
    showLegend: series.length > 1, legendPos: "b", legendFontSize: 10, legendFontFace: "+mn-lt", legendColor: THEME.colors.dk1,
    showValAxisTitle: !!g.eje, valAxisTitle: g.eje || "", valAxisTitleFontSize: 10, valAxisTitleColor: THEME.colors.dk2, valAxisTitleFontFace: "+mn-lt",
  };
  if (tipo === pres.charts.BAR) {
    o.barDir = forma.startsWith("barras") ? "bar" : "col";
    if (apil) o.barGrouping = "stacked";
    o.barGapWidthPct = 50;
    if (o.barDir === "bar") o.catAxisOrientation = "maxMin";
    if (g.series.some((d) => d.valores.some((v) => v < 0))) o.catAxisLabelPos = "low";
  } else {
    o.lineSize = 2; o.lineDataSymbol = "circle"; o.lineDataSymbolSize = 6;
  }
  if (g.etiquetas_datos) {
    Object.assign(o, { showValue: true, dataLabelFontSize: 9, dataLabelFontFace: "+mn-lt", dataLabelFormatCode: fmt,
      dataLabelPosition: apil ? "ctr" : (tipo === pres.charts.LINE ? "t" : "outEnd"),
      dataLabelColor: apil ? "FFFFFF" : THEME.colors.dk1 });
  }
  s.addChart(tipo, series, o);
}
const fuenteLinea = (s, t, x, y, w) => tb(s, NB(t), { x, y, w, h: 0.4, fontSize: 9, color: C.text2 });

// celda de tabla con ecuación arriba y nomenclatura en gris abajo
function eqNom(latex, nom, fs = 15, fn = 12) {
  const a = rich(`$${latex}$`, { fontSize: fs });
  a[a.length - 1].options.breakLine = true;
  a[a.length - 1].options.paraSpaceAfter = 2;
  return { runs: [...a, ...rich(nom, { fontSize: fn, color: C.text2 })] };
}

// ================================================================ 2–3. Motivación (contenido.js)
K.motivacion.forEach((m) => {
  const s = content("Motivación", m.titulo, m.subtitulo);
  if (m.graficos) {
    // mensajes arriba y tres gráficos abajo
    tb(s, bullets(m.bullets, { size: 17, after: 8 }), { x: X0, y: YC, w: W, h: 1.45 });
    const n = m.graficos.length, gap = 0.35, cw = (W - (n - 1) * gap) / n;
    m.graficos.forEach((g, i) => {
      const x = X0 + i * (cw + gap);
      grafico(s, g, x, 3.3, cw, 3.05);
      if (g.fuente) fuenteLinea(s, g.fuente, x + 0.05, 6.38, cw - 0.05);
    });
  } else if (m.grafico) {
    tb(s, bullets(m.bullets, { size: 17, after: 14 }), { x: X0, y: YC + 0.05, w: 6.3, h: 4.75, valign: "middle" });
    grafico(s, m.grafico, 7.25, YC, XR - 7.25, 4.45);
    if (m.grafico.fuente) fuenteLinea(s, m.grafico.fuente, 7.3, YC + 4.5, XR - 7.3);
  } else {
    tb(s, bullets(m.bullets, { size: 17, after: 11 }), { x: X0, y: YC, w: W, h: YB - YC - 0.3 });
  }
  if (m.notas) s.addNotes(m.notas);
});

// ================================================================ 4. Pregunta y propuesta
{
  const s = content("Motivación", "Pregunta y propuesta", "La ubicación de los data centers como variable de la planificación de largo plazo");
  tb(s, [
    label("Pregunta"),
    { text: NB("¿Cuánto le cuesta al sistema ubicar los data centers donde dicen las proyecciones, frente a ubicarlos donde le conviene al sistema?"),
      options: { fontSize: 17, breakLine: true, paraSpaceAfter: 14 } },
    label("Propuesta"),
    ...bullets([
      "Modelo de expansión de generación y transmisión de mínimo costo para el SEN: Switch (Johnston et al., 2019)",
      "La cantidad y la fecha de los data centers son dato; su zona es una variable de decisión",
      "Se comparan tres casos con todo lo demás igual",
    ], { size: 16, after: 6 }),
  ], { x: X0, y: YC, w: 5.7, h: 4.6 });
  const xs = 6.85, bw = XR - xs, bh = 0.95, gap = 0.42;
  const casos = [
    ["Sin data centers", "Referencia: Carbono Neutralidad sin data centers proyectados", "$C^{\\mathrm{sin}}$"],
    ["Base", "Los data centers en las zonas que indican las proyecciones", "$C^{\\mathrm{base}}$"],
    ["Libre", "El modelo elige la zona de los data centers (desde 2030)", "$C^{\\mathrm{libre}}$"],
  ];
  casos.forEach(([t, d, c], i) => {
    const y = YC + 0.05 + i * (bh + gap);
    box(s, xs, y, bw, bh);
    tb(s, [{ text: t, options: { bold: true, fontSize: 16, breakLine: true } }, { text: NB(d), options: { fontSize: 13, color: C.text2 } }],
      { x: xs + 0.2, y: y + 0.12, w: bw - 1.45, h: bh - 0.2, valign: "middle" });
    tb(s, rich(c, { fontSize: 18 }), { x: xs + bw - 1.2, y: y + 0.12, w: 1.0, h: bh - 0.24, valign: "middle", align: "right" });
  });
  const ym = YC + 0.05 + 3 * (bh + gap) - 0.1;
  tb(s, [
    ...rich("Costo extra de los data centers: $C^{\\mathrm{base}}-C^{\\mathrm{sin}}$", { fontSize: 15, breakLine: true, paraSpaceAfter: 4 }),
    ...rich("Ahorro de ubicarlos bien: $C^{\\mathrm{base}}-C^{\\mathrm{libre}}\\ge 0$", { fontSize: 15 }),
  ], { x: xs, y: ym, w: bw, h: 0.75 });
  s.addNotes("C es el costo total del sistema en valor presente " + CF.anio_base + " (inversión en generación, almacenamiento y transmisión, más operación, impuesto al CO2 y energía no suministrada).\n" +
    "El ahorro es no negativo por construcción: el caso base es una solución factible del caso libre.");
}

// ================================================================ 5. Búsqueda bibliográfica (contenido.js)
K.literatura.forEach((lam) => {
  const s = content("Búsqueda bibliográfica", lam.titulo, lam.subtitulo);
  const n = lam.estudios.length;
  const gap = 0.45, cw = (W - (n - 1) * gap) / n;
  lam.estudios.forEach((e, i) => {
    const x = X0 + i * (cw + gap);
    if (i > 0) vrule(s, x - gap / 2, YC + 0.05, 4.1);
    if (e.pendiente) {
      tb(s, [
        { text: NB(e.cita), options: { bold: true, fontSize: 16, color: C.text2, breakLine: true, paraSpaceAfter: 10 } },
        { text: NB(e.pendiente), options: { italic: true, fontSize: 15, color: C.text2 } },
      ], { x, y: YC, w: cw, h: 4.2 });
      return;
    }
    tb(s, [
      { text: NB(e.cita), options: { bold: true, fontSize: 16, breakLine: true, paraSpaceAfter: 2 } },
      { text: NB(e.titulo), options: { italic: true, fontSize: 13, color: C.text2, breakLine: true, paraSpaceAfter: 10 } },
      ...bullets(e.bullets, { size: 15, after: 8 }),
    ], { x, y: YC, w: cw, h: 4.2 });
  });
  if (lam.cierre) {
    hrule(s, X0, 6.1, W);
    tb(s, rich(lam.cierre, { fontSize: 15 }), { x: X0, y: 6.2, w: W, h: 0.5 });
  }
  if (lam.notas) s.addNotes(lam.notas);
});

// ================================================================ 6. Formulación: función objetivo
{
  const s = content("Formulación", "Formulación: función objetivo",
    "Expansión de generación y transmisión de mínimo costo, en valor presente, con días típicos por período");
  tb(s, rich(String.raw`$\min\; C=\sum_{y\in Y}B_y\Big[\sum_{g\in G}I_g\,X_{g,y}+\sum_{k\in K}I^{T}_k\,F_{k,y}$`, { fontSize: 20 }),
    { x: X0 + 0.3, y: YC, w: W - 0.3, h: 0.6, valign: "middle" });
  tb(s, rich(String.raw`$+\sum_{t\in T_y}\Delta T_t\Big(\sum_{g\in G}\big(MC_g+\tau^{\mathrm{CO}_2}_y\,\varepsilon_g\big)\,p_{g,t}+VOLL\sum_{z\in Z}ls_{z,t}\Big)\Big]$`, { fontSize: 20 }),
    { x: X0 + 2.55, y: YC + 0.62, w: W - 2.55, h: 0.6, valign: "middle" });
  acadTable(s, ["Término", "Significado"], [
    ["$B_y$", `Factor que lleva a valor presente ${CF.anio_base} los costos anuales del período $y$ (tasa de 6 %)`],
    ["$I_g\\,X_{g,y}$", "Anualidad de inversión más O&M fijo de la capacidad instalada de generación y almacenamiento"],
    ["$I^{T}_k\\,F_{k,y}$", "Anualidad de la capacidad de transmisión del corredor $k$ (existente más ampliaciones)"],
    ["$\\Delta T_t$", "Horas del año que representa la hora $t$ del día típico (6 días típicos × 24 h)"],
    ["$MC_g,\\ \\tau^{\\mathrm{CO}_2}_y\\,\\varepsilon_g$", "Costo variable (combustible y O&M) e impuesto al CO₂ por MWh"],
    ["$VOLL\\,ls_{z,t}$", "Energía no suministrada, valorizada a 650 USD/MWh"],
  ], { x: X0, y: YC + 1.5, w: W, colW: [2.9, W - 2.9], fontSize: 14 });
  s.addNotes("Es el modelo de expansión de capacidad de la Clase 8 (con VOLL) extendido a varios períodos, con transmisión co-optimizada como en la Clase 13 e impuesto al CO2. Con un solo período de un año se reduce exactamente al modelo de la Clase 8: se verificó reproduciendo en Switch el ejemplo del curso (nuclear 7.086, carbón 1.918 y gas 2.165 MW).");
}

// ================================================================ 7. Formulación: restricciones (con nomenclatura)
{
  const s = content("Formulación", "Formulación: restricciones",
    "Por zona y hora; sin compromiso de unidades ni inercia, y transmisión como transporte entre zonas");
  const eqNom7 = (l, n) => eqNom(l, n, 14, 11);
  acadTable(s, null, [
    ["Balance por zona", eqNom7("\\sum_{g\\in G_z}p_{g,t}+\\sum_{m}f_{m\\to z,t}-\\sum_{n}f_{z\\to n,t}+ls_{z,t}=D_{z,t}+c_{z,t}+D^{\\mathrm{DC}}_{z,t}\\quad(\\rho_{z,t})",
      "$p$ generación · $f$ flujo entre zonas · $ls$ energía no suministrada · $D$ demanda · $c$ carga de almacenamiento · $D^{\\mathrm{DC}}$ data centers · $\\rho$ precio de la zona (dual)")],
    ["Generación", eqNom7("0\\le p_{g,t}\\le \\alpha_g\\,\\kappa_{g,t}\\,X_{g,y(t)},\\qquad X_{g,y}\\le \\bar X_g",
      "$X$ capacidad instalada (decisión) · $\\alpha$ disponibilidad · $\\kappa$ perfil horario del recurso (solar, eólica) · $\\bar X$ potencial máximo del proyecto")],
    ["Almacenamiento", eqNom7("e_{s,t}=e_{s,t-1}+\\eta_s\\,c_{s,t}-p_{s,t},\\qquad e_{s,t}\\le h_s\\,X_{s,y(t)}",
      "$e$ energía almacenada · $c$ carga · $p$ descarga · $\\eta$ eficiencia de ida y vuelta · $h$ horas de almacenamiento")],
    ["Hidroelectricidad", eqNom7("\\sum_{t\\in d}p_{h,t}\\le 24\\,A_{h,d},\\qquad p_{h,t}\\ge \\underline{P}_{h,d}",
      "$A$ potencia media disponible en el día típico $d$ (energía mensual de la PELP) · $\\underline{P}$ potencia mínima")],
    ["Transmisión", eqNom7("0\\le f_{m\\to n,t}\\le F_{k,y(t)},\\qquad F_{k,y}=F^0_k+\\sum_{v\\le y}T_{k,v},\\qquad \\sum_{v\\le y}T_{k,v}\\le \\bar T_{k,y}",
      "$F$ capacidad del corredor $k=(m,n)$ · $F^0$ existente · $T$ ampliación (decisión) · $\\bar T$ tope de la PELP; solo se amplían corredores existentes")],
    ["Reserva", eqNom7("\\sum_{g\\in G^R}\\big(\\bar p_{g,t}-p_{g,t}\\big)\\ge R^{+},\\qquad \\sum_{g\\in G^R}p_{g,t}\\ge R^{-}",
      "$G^R$ proyectos que dan reserva · $\\bar p=\\alpha\\,\\kappa\\,X$ potencia disponible · $R^{+},R^{-}$ reserva de subida (551 MW) y de bajada (407 MW)")],
  ], { x: X0, y: YC - 0.1, w: W, colW: [2.2, W - 2.2], fontSize: 14, margin: [4, 6, 4, 6] });
  tb(s, rich("Índices: $g$ proyecto, $s$ almacenamiento, $h$ hidro, $z$ zona, $k$ corredor, $t$ hora, $d$ día típico, $y$ período.",
    { fontSize: 12, color: C.text2 }), { x: X0, y: 6.52, w: W, h: 0.3 });
  s.addNotes("Hidro: presupuesto de energía por día típico (energía mensual que despachó la PELP); el vertimiento no tiene costo. Transmisión: modelo zonal de la Clase 5; las ampliaciones son continuas y tienen el tope y la fecha de los candidatos de la PELP; las obras comprometidas (HVDC Kimal–Alto Jahuel y Río Malleco–Pichirropulli, ambas en 2030) entran obligatoriamente. Reserva sistémica: primaria más secundaria de la PELP.");
}

// ================================================================ 8. Formulación: data centers (con nomenclatura)
{
  const s = content("Formulación", "Formulación: ubicación de data centers",
    "Módulo propio en Switch: la demanda total de data centers es dato y su zona es decisión");
  acadTable(s, null, [
    ["Demanda en el balance", eqNom("D^{\\mathrm{DC}}_{z,t}=\\bar D^{\\mathrm{DC}}_{z,y(t)}+x^{\\mathrm{DC}}_{z,y(t)}",
      "Carga plana de la zona $z$: una parte fija $\\bar D^{\\mathrm{DC}}$, que no se reubica, más una parte ubicable $x^{\\mathrm{DC}}$, en MW medios")],
    ["Total por período", eqNom("\\sum_{z\\in Z^{\\mathrm{DC}}}x^{\\mathrm{DC}}_{z,y}=D^{\\mathrm{DC}}_y\\qquad(\\lambda^{\\mathrm{DC}}_y)",
      "Caso libre. $D^{\\mathrm{DC}}_y$ MW ubicables del escenario en el período $y$ (dato) · $Z^{\\mathrm{DC}}$ las 26 barras candidatas · $\\lambda^{\\mathrm{DC}}_y$ costo de 1 MW más")],
    ["Sin traslado", eqNom("x^{\\mathrm{DC}}_{z,y}\\ge x^{\\mathrm{DC}}_{z,y-1}",
      "Lo instalado en la zona $z$ sigue ahí en los períodos siguientes")],
    ["Ubicación proyectada", eqNom("x^{\\mathrm{DC}}_{z,y}=\\hat x^{\\mathrm{DC}}_{z,y}",
      "$\\hat x^{\\mathrm{DC}}$ ubicación según la proyección. Caso base: en todos los períodos; caso libre: solo antes de 2030")],
  ], { x: X0, y: YC - 0.05, w: W, colW: [2.6, W - 2.6], fontSize: 16, margin: [7, 6, 7, 6] });
  tb(s, [
    label("Interpretación", { fontSize: 16 }),
    ...bullets([
      "Caso libre: cada MW nuevo va a la zona donde abastecer 1 MW plano cuesta menos, desde que se instala hasta 2054, con $\\rho_{z,t}$ como precio: $\\sum_t \\Delta T_t\\,\\rho_{z,t}$",
      "El caso base es una solución factible del caso libre, así que $C^{\\mathrm{libre}}\\le C^{\\mathrm{base}}$",
    ], { size: 15, after: 6 }),
  ], { x: X0, y: 4.95, w: W, h: 1.7 });
  s.addNotes("Z^DC son las 26 barras eléctricas (sin los polos de generación). No hay costo de conexión ni de terreno, ni tope por zona: el ahorro es solo del sistema eléctrico. Lo que se conecta antes de 2030 son proyectos ya comprometidos y queda fijo también en el caso libre. La condición de optimalidad (KKT) iguala, entre las zonas elegidas, el costo acumulado de abastecer un MW plano en los períodos en que la carga está instalada.");
}

// ================================================================ 9. Casos de estudio: sistema modelado (con diagrama unilineal)
{
  const s = content("Casos de estudio", "Casos de estudio: sistema modelado",
    "Switch 2.0.9 sobre la red de la PELP 2023–2027, escenario Carbono Neutralidad");
  const wl = 6.55;
  const r = CF.periodos_rango;
  tb(s, [
    label("Sistema", { fontSize: 16 }),
    ...bullets([
      "26 barras y 5 polos de generación (31 zonas), unidos por 34 corredores; transporte entre zonas, sin pérdidas",
      `El modelo decide todas las inversiones desde ${PER[0]}; las que resolvió la PELP no se toman como dato`,
      "Candidatos de la PELP por zona: solar, eólica, CSP, hidro de pasada, geotermia, biomasa, gas, diésel, baterías, bombeo, aire comprimido y Carnot",
      "Transmisión: solo se amplían los corredores existentes, hasta los topes de la PELP; las obras comprometidas entran en 2030",
      "Demanda Carbono Neutralidad: 110 TWh en 2030 y 272 TWh en 2050, con hidrógeno (Ministerio de Energía, 2025)",
    ], { size: 13, after: 4 }),
    { text: " ", options: { fontSize: 5, breakLine: true } },
    label("Tiempo y cómputo", { fontSize: 16 }),
    ...bullets([
      `${PER.length} períodos de ${PER[0]} a ${FIN} (${r[0]}, ${r[1]} y luego cada 5 años)`,
      "6 días típicos × 24 h por año (con 12 no cabe en memoria)",
      `Programa lineal de ${fnum(CF.filas / 1e6, 2)} millones de restricciones; Gurobi (barrera), ${rango(CF.minutos_corrida)} min por corrida`,
    ], { size: 13, after: 4 }),
  ], { x: X0, y: YC, w: wl, h: 4.85 });
  const DIAG = path.join(HERE, "graficos", "diagrama_red.png");
  if (fs.existsSync(DIAG)) {
    s.addImage({ path: DIAG, x: XR - 5.5, y: 1.6, w: 5.5, h: 5.0, altText: "Diagrama unilineal de la red modelada: 26 barras, 5 polos de generación y 34 corredores" });
  }
  s.addNotes("Detalle de candidatos, costos, corredores y obras comprometidas en los anexos. Obras comprometidas: HVDC Kimal–Lo Aguirre (2.000 MW en los datos de la PELP 2023–2027; el CEN informa 3.000 MW) y Río Malleco–Pichirropulli (660 MW), ambas en 2030. Los topes anuales de inversión FV y eólica de la PELP se suman por período y no restringen. La traducción de los datos de la PELP (modelo AMEBA del Ministerio de Energía) a Switch se validó contra las entradas de AMEBA. Con 12 días típicos por año el problema no cabe en memoria (63 GB) con barrera; por eso 6 días típicos (meses impares, cada uno con el peso del mes siguiente).");
}

// ================================================================ 10. Casos de estudio: escenarios de data centers
{
  const s = content("Casos de estudio", "Casos de estudio: escenarios de data centers",
    "Cuatro proyecciones de demanda de data centers; todo lo demás es la PELP, escenario Carbono Neutralidad");
  const cw = (W - 0.45) / 2;
  grafico(s, { forma: "lineas", titulo: "Demanda de data centers agregada al modelo (MW medios)", etiquetas: PER.map(String),
    series: CF.escenarios.map((e) => ({ nombre: e, valores: CF.dc_total_por_periodo[e] })) }, X0, YC, cw, 2.85);
  grafico(s, { forma: "barras_apiladas", titulo: `Ubicación proyectada en ${ULT} (MW medios)`, etiquetas: CF.escenarios,
    series: ["Metropolitana", "Valparaíso", "Antofagasta"].filter((r) => CF.ubicacion_proyectada_region[r])
      .map((r) => ({ nombre: r === "Metropolitana" ? "Región Metropolitana" : r, valores: CF.ubicacion_proyectada_region[r] })) },
    X0 + cw + 0.45, YC, cw, 2.85);
  tb(s, bullets([
    "Datos de la PELP 2023–2027 (Carbono Neutralidad), iguales en todos los casos: red y topes de ampliación, demanda, proyectos existentes y candidatos, costos de inversión y de O&M, combustibles, perfiles renovables, hidrología, impuesto al CO₂, reserva, VOLL y tasa de descuento",
    "Solo cambia la demanda de data centers: los que ya operan (~100 MW medios) están en la demanda de la PELP y se agrega lo proyectado, con 50 % de utilización",
    "Después de cada proyección la demanda sigue creciendo 3 % anual: CEN desde 2031 y escenario propio desde 2033; la PELP trae su propio crecimiento",
    "Escenario propio: solicitudes de conexión vigentes al Coordinador, cada campus una vez, más el llenado de los campus ya conectados",
  ], { size: 13, after: 3 }), { x: X0, y: 4.68, w: W, h: 1.75 });
  fuenteLinea(s, "Promedio de cada período. Fuentes: Ministerio de Energía (2025; 2026a), CEN (2026a) y CEN (s. f.).", X0, 6.45, W);
  s.addNotes("Ubicación proyectada en el modelo: El Salto 220 (RM) → zona Polpaico 500; Torquemada 110 (Valparaíso) → Quillota 500; Kimal 220 (Antofagasta) → Kimal 220. Escenario propio: además Alto Jahuel 500 (RM).\n" +
    "Crecimiento después del horizonte: CEN, la capacidad crece 3 % anual desde 2031 (la proyección del CEN termina en 2030 con 1.381 MW); propio, la demanda total de data centers crece 3 % anual desde 2033 y el aumento es ubicable. La PELP 2028–2032 ya crece después de 2030 (E2 ~1,4 % anual; N1 ~0,4 % anual desde 2035).\n" +
    `Hasta ${PER.filter((p) => p < 2030).join(" y ")} la ubicación es la proyectada también en el caso libre.`);
}

// ================================================================ 11. Resultados: costo extra y ahorro
{
  const s = content("Resultados", "Resultados: costo extra y ahorro",
    `Valor presente ${CF.anio_base}, millones de USD. El sistema sin data centers proyectados cuesta ${fnum(CF.costo_sin_dc)}`);
  const cats = CF.escenarios;
  s.addChart(pres.charts.BAR, [
    { name: "Costo extra con la ubicación óptima (libre)", labels: cats, values: CF.extra_libre },
    { name: "Ahorro de ubicar bien (base − libre)", labels: cats, values: CF.ahorro },
  ], {
    x: X0 - 0.1, y: YC, w: 7.3, h: 4.75, barDir: "bar", barGrouping: "stacked", chartColors: [HEX.rule, "808080"], valAxisLabelFormatCode: "#,##0",
    showValue: true, dataLabelPosition: "ctr", dataLabelFontSize: 12, dataLabelColor: "FFFFFF", dataLabelFontFace: "+mn-lt", dataLabelFormatCode: '[>=500]#,##0;""',  // oculta etiquetas de barras cortas (las cifras están en la tabla)
    catAxisLabelFontSize: 13, valAxisLabelFontSize: 11, catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt",
    catAxisLabelColor: THEME.colors.dk1, valAxisLabelColor: THEME.colors.dk2, catAxisOrientation: "maxMin", valAxisLineShow: false,
    valGridLine: { color: HEX.grid, size: 0.5 }, catGridLine: { style: "none" },
    showLegend: true, legendPos: "b", legendFontSize: 12, legendFontFace: "+mn-lt", legendColor: THEME.colors.dk1,
    showValAxisTitle: true, valAxisTitle: "Costo extra frente al sistema sin data centers (MMUSD)", valAxisTitleFontSize: 11, valAxisTitleColor: THEME.colors.dk2, valAxisTitleFontFace: "+mn-lt",
  });
  acadTable(s, ["Escenario", { text: "Extra base", options: R }, { text: "Ahorro", options: R }, { text: "% del extra", options: R }],
    cats.map((e, i) => [e, { text: fnum(CF.extra_base[i]), options: R }, { text: fnum(CF.ahorro[i]), options: R }, { text: `${fnum(CF.ahorro_pct_extra[i])} %`, options: R }]),
    { x: 7.75, y: YC + 0.05, w: XR - 7.75, colW: [1.45, 1.25, 1.05, XR - 7.75 - 3.75], fontSize: 14 });
  tb(s, bullets([
    `Ubicar bien evita entre el ${fnum(Math.min(...CF.ahorro_pct_extra))} % y el ${fnum(Math.max(...CF.ahorro_pct_extra))} % del costo extra`,
    `Por MWh reubicado, el ahorro va de ${rango(CF.ahorro_usd_mwh_reubicable, 1, " a ")} USD/MWh entre escenarios`,
  ], { size: 14, after: 6 }), { x: 7.75, y: 4.15, w: XR - 7.75, h: 1.5 });
  s.addNotes(`Costo extra base = C_base − C_sin; ahorro = C_base − C_libre. Reubicable en ${ULT}: ${CF.escenarios.map((e, i) => `${e} ${fnum(CF.reubicable_2050_pct[i])} %`).join(", ")} (lo conectado antes de 2030 queda fijo).\n` +
    `Costo extra por MWh de data centers: ${rango(CF.extra_usd_mwh_base, 0, " a ")} USD/MWh con la ubicación proyectada y ${rango(CF.extra_usd_mwh_libre, 0, " a ")} USD/MWh con la óptima.`);
}

// ================================================================ 12. Resultados: mapa de ubicación por región
{
  const s = content("Resultados", "Resultados: ubicación de los data centers",
    `Capacidad instalada de data centers en ${ULT} por región, con la ubicación proyectada y con la óptima`);
  const MAPA = path.join(HERE, "graficos", "mapa_dc_2050.png");
  if (fs.existsSync(MAPA)) {
    s.addImage({ path: MAPA, x: X0, y: YC, w: W, h: W * 4.6 / 12.1, altText: `Mapas de Chile por región con la capacidad de data centers en ${ULT}, por escenario, con la ubicación proyectada y la óptima` });
  }
  fuenteLinea(s, "Capacidad instalada = MW medios / 0,5. Círculos de área proporcional, separados si se tocan. La ubicación óptima mantiene lo conectado antes de 2030. Elaboración propia.", X0, 6.42, W);
  s.addNotes(SUR ? "En los cuatro escenarios, lo que el modelo puede reubicar va al sur. Lo que queda en la RM, Valparaíso y Antofagasta en la ubicación óptima es lo conectado antes de 2030."
    : `${DONDE}. Lo que queda en la RM, Valparaíso y Antofagasta en la ubicación óptima es lo conectado antes de 2030.`);
}

// ================================================================ 13. Resultados: ubicación por zona (tabla)
{
  const s = content("Resultados", "Resultados: ubicación por zona",
    `MW medios de data centers en ${ULT} por zona, con la ubicación proyectada y con la óptima`);
  const filas = CF.ubicacion_por_zona.map((f) => [f.zona, ...f.celdas.map((c) => ({ text: c, options: R }))]);
  const fsz = filas.length > 10 ? 12 : 13;
  acadTable(s, ["Zona (de norte a sur)", ...CF.escenarios.map((e) => ({ text: e, options: R }))], filas,
    { x: X0, y: YC + 0.05, w: 7.9, colW: [3.1, 1.2, 1.2, 1.2, 1.2], fontSize: fsz, margin: [3, 6, 3, 6] });
  const altoTabla = (filas.length + 1) * (fsz <= 12 ? 0.29 : 0.31);
  tb(s, "MW medios: proyectada → óptima.", { x: X0, y: YC + 0.12 + altoTabla, w: 7.6, h: 0.3, fontSize: 12, color: C.text2 });
  const pe = CF.precio_2040_elegidas, pp = CF.precio_2040_proyectadas;
  // Si la ubicación óptima es el sur, solo cuentan los corredores que traen energía del sur al centro.
  const CORR_TOPE = SUR ? CF.corredores_sur_en_tope_todos : CF.corredores_en_tope_todos;
  tb(s, [
    label(SUR ? "Por qué el sur" : "Por qué esas zonas", { fontSize: 16 }),
    ...bullets([
      `En 2040, sin data centers, 1 MW plano cuesta ${lista([...PRECIO_MZ, `${rango(pp, 1)} USD/MWh en las zonas proyectadas`])}`,
      ...(CORR_TOPE.length ? [`${CORR_TOPE.length > 1 ? "Los corredores" : "El corredor"} ${lista(CORR_TOPE)} ${CORR_TOPE.length > 1 ? "llegan" : "llega"} a su tope de ampliación en los ${CF.n_corridas} casos`] : []),
      SUR ? "Todo lo reubicable va al sur en los 4 escenarios" : DONDE,
    ], { size: 14, after: 7 }),
  ], { x: 8.75, y: YC, w: XR - 8.75, h: 4.7 });
  s.addNotes("Lo que se ve en Santiago, Valparaíso y Antofagasta en el caso libre es lo conectado antes de 2030 (fijo) y, en el escenario propio, el llenado de los campus ya conectados.");
}

// ================================================================ 14. Resultados: expansión del sistema (gráficos)
{
  const s = content("Resultados", "Resultados: expansión del sistema",
    `Diferencia entre la ubicación óptima y la proyectada: capacidad construida al ${ULT} y costos`);
  const cw = (W - 0.45) / 2;
  grafico(s, { forma: "barras", titulo: `Cambio de capacidad al ${ULT}, óptima − proyectada (MW)`,
    etiquetas: Object.keys(CF.cambio_capacidad),
    series: CF.escenarios.map((e, i) => ({ nombre: e, valores: Object.values(CF.cambio_capacidad).map((v) => v[i]) })) }, X0, YC, cw, 3.5);
  const comp = Object.entries(CF.ahorro_componentes).filter(([, v]) => v.some((x) => Math.abs(x) >= 1));
  grafico(s, { forma: "columnas_apiladas", titulo: `Ahorro por tipo de costo (millones de USD, ${VP})`,
    etiquetas: CF.escenarios.map((e, i) => `${e} (${fnum(CF.ahorro[i])})`),
    series: comp.map(([n, v]) => ({ nombre: n, valores: v })) }, X0 + cw + 0.45, YC, cw, 3.5);
  const em = CF.emisiones_menos_libre_Mt;
  tb(s, bullets([
    ...(QUE_CAMBIA ? [`En los cuatro escenarios, con la ubicación óptima se construye ${QUE_CAMBIA}`] : []),
    `Cada MW medio de data center pide ${rango(CF.mw_nuevos_por_mw_dc_libre, 1)} MW de capacidad nueva, en vez de ${rango(CF.mw_nuevos_por_mw_dc_base, 1)}`,
    em.every((x) => x > 0) ? `Las emisiones acumuladas ${PER[0]}–${FIN} bajan entre ${rango(em, 1, " y ")} Mt CO₂` : `Cambio de emisiones acumuladas (proyectada − óptima): ${em.map((x) => fnum(x, 1)).join("; ")} Mt CO₂`,
  ], { size: 15, after: 6 }), { x: X0, y: 5.4, w: W, h: 1.25 });
  s.addNotes("Transmisión: capacidad total de los corredores ampliados al último período. Entre paréntesis, el ahorro total de cada escenario. Capacidad nueva por MW medio de data center: (capacidad nueva del caso − la del caso sin data centers) / MW medios de data centers del último período."
    + (CF.otros_cambios_capacidad.length ? " Otros cambios de 500 MW o más: " + CF.otros_cambios_capacidad.map((o) => `${o.escenario}, ${o.grupo.toLowerCase()} ${o.dif_MW > 0 ? "+" : ""}${fnum(o.dif_MW)} MW`).join("; ") + "." : ""));
}

// ================================================================ 15. Conclusiones
{
  const s = content("Conclusiones", "Conclusiones", "Resultados preliminares de la primera implementación");
  const iProp = CF.escenarios.indexOf("Propio");
  const ah = CF.ahorro_usd_mwh_reubicable;
  tb(s, bullets([
    `Ubicar los data centers donde le conviene al sistema evita entre el ${fnum(Math.min(...CF.ahorro_pct_extra))} % y el ${fnum(Math.max(...CF.ahorro_pct_extra))} % del costo extra que agregan (${rango(CF.ahorro, 0, " a ")} millones de USD en valor presente)`,
    "Es comparable con lo que se estima para Japón: 16–20 % (Onodera et al., 2026)",
    Math.max(...ah) - Math.min(...ah) < 2 ? `El ahorro por MWh reubicado es estable entre escenarios (${rango(ah, 1)} USD/MWh): el tamaño de la proyección define el monto`
      : `El ahorro por MWh reubicado va de ${rango(ah, 1, " a ")} USD/MWh entre escenarios`,
    SUR ? "La ubicación óptima está en el sur, donde la energía es más barata y los corredores hacia el centro están al tope"
      : `${DONDE}. Las proyecciones, en cambio, concentran los data centers en la RM`,
    ...(QUE_CAMBIA ? [`Cambia la expansión eficiente: ${QUE_CAMBIA}`] : []),
    `Con las solicitudes vigentes y 3 % anual desde 2033, el escenario propio llega a ${fnum(CF.dc_ultimo_periodo[iProp])} MW medios en ${ULT}–${FIN}`,
  ], { size: 17, after: 10 }), { x: X0, y: YC, w: W, h: 4.8 });
}

// ================================================================ 16. Trabajo futuro
{
  const s = content("Trabajo futuro", "Trabajo futuro", "Extensiones del modelo y de los datos");
  const cw = (W - 0.5) / 2;
  tb(s, [label("Modelo"), ...bullets([
    "Flujo DC (leyes de Kirchhoff) en los lazos de la red",
    "Zonas donde realmente se pueden instalar data centers, según la red de fibra óptica de Chile",
    "Escenarios Recuperación Lenta y Transición Acelerada de la PELP, además de Carbono Neutralidad",
  ], { size: 16, after: 9 })], { x: X0, y: YC, w: cw, h: 4.6 });
  vrule(s, X0 + cw + 0.25, YC + 0.05, 3.6);
  tb(s, [label("Datos y análisis"), ...bullets([
    "Contrastar el escenario propio con los desarrolladores y el Coordinador",
    "Sensibilidad a la utilización de los data centers y a la fecha desde la que se decide la ubicación",
    "Red de mayor resolución (234 nodos de la PELP 2028–2032) en las zonas candidatas",
    "Impacto en tarifas y señales de mercado para una ubicación eficiente (Newbery, 2026)",
  ], { size: 16, after: 9 })], { x: X0 + cw + 0.5, y: YC, w: cw, h: 4.6 });
}

// ================================================================ 17. Referencias
{
  const s = content("Referencias", "Referencias", "");
  const n = Math.ceil(K.referencias.length / 2), cw = (W - 0.5) / 2;
  [K.referencias.slice(0, n), K.referencias.slice(n)].forEach((col, j) => {
    tb(s, col.map((r, i) => ({ text: NB(r), options: { fontSize: 11, breakLine: i < col.length - 1, paraSpaceAfter: 7 } })),
      { x: X0 + j * (cw + 0.5), y: 1.25, w: cw, h: 5.45, valign: "top" });
  });
}

// ================================================================ Anexos (fuente\anexos\NN_tema.js, formato en anexos\FORMATO.md)
function altoTexto(txt, fs, w) {
  const porLinea = Math.max(10, Math.floor(w * 168 / fs));
  return Math.ceil(String(txt).length / porLinea) * fs * 1.25 / 72;
}
function bloque(s, b, x, y, w) {
  if (b.tipo === "tabla") {
    const fsz = b.letra || 12;
    const der = new Set(b.derecha || []);
    const cel = (c, j, extra) => ({ text: String(c), options: Object.assign({}, der.has(j) ? R : {}, extra || {}) });
    const header = b.header ? b.header.map((h, j) => cel(h, j)) : null;
    const nf = b.filas.length;
    const filas = b.filas.map((r, i) => r.map((c, j) => cel(c, j, b.total && i === nf - 1 ? { bold: true } : null)));
    acadTable(s, header, filas, { x, y, w, colW: b.anchos, fontSize: fsz, margin: [3, 6, 3, 6] });
    const rowH = fsz <= 11 ? 0.28 : fsz <= 12 ? 0.3 : fsz <= 13 ? 0.32 : 0.34;
    return y + rowH * (nf + (header ? 1 : 0));
  }
  if (b.tipo === "bullets") {
    const fsz = b.letra || 14;
    const h = b.alto || b.items.reduce((a, it) => a + altoTexto(typeof it === "object" ? it.text : it, fsz, w - 0.3) + 0.08, 0);
    tb(s, bullets(b.items, { size: fsz, after: 5 }), { x, y, w, h });
    return y + h;
  }
  if (b.tipo === "grafico") {
    const h = b.alto || 3.2;
    grafico(s, b, x, y, w, h);
    return y + h;
  }
  if (b.tipo === "texto") {
    const fsz = b.letra || 12;
    const h = b.alto || altoTexto(b.texto, fsz, w) + 0.05;
    tb(s, rich(b.texto, { fontSize: fsz, color: b.gris ? C.text2 : C.text1, bold: !!b.negrita }), { x, y, w, h });
    return y + h;
  }
  return y;
}
{
  const DIR = path.join(HERE, "anexos");
  const mods = fs.existsSync(DIR) ? fs.readdirSync(DIR).filter((f) => /^\d+_.+\.js$/.test(f)).sort() : [];
  const ANEXOS = mods.flatMap((f) => require(path.join(DIR, f)));
  if (ANEXOS.length) {
    const s = content("Anexos", "Anexos", "Respaldo de los datos y del modelo");
    const items = ANEXOS.map((a) => a.titulo.replace(/^Anexo:\s*/, "")).map((t) => t.charAt(0).toUpperCase() + t.slice(1));
    const half = Math.ceil(items.length / 2), cw = (W - 0.5) / 2;
    [items.slice(0, half), items.slice(half)].forEach((col, j) => {
      if (col.length) tb(s, bullets(col, { size: 16, after: 8 }), { x: X0 + j * (cw + 0.5), y: YC, w: cw, h: 4.8 });
    });
    ANEXOS.forEach((a) => {
      const sl = content("Anexos", a.titulo, a.subtitulo);
      const cols = a.columnas || [{ ancho: W, bloques: a.bloques || [] }];
      let x = X0;
      cols.forEach((col) => {
        const w = col.ancho || W;
        let y = YC;
        (col.bloques || []).forEach((b) => { y = bloque(sl, b, x, y, w) + 0.15; });
        x += w + 0.45;
      });
      if (a.fuente) fuenteLinea(sl, a.fuente, X0, 6.5, W);
      if (a.notas) sl.addNotes(a.notas);
    });
  }
}

// ---------------------------------------------------------------- escribir
(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  fs.writeFileSync(OUT + ".eqs.json", JSON.stringify(EQS, null, 1));
  console.log(`escrito ${OUT} con ${EQN} ecuaciones`);
})();
