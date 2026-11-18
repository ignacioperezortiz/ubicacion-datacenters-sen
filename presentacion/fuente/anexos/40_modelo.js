// Anexos del modelo: decisiones, adaptaciones de los datos de la PELP y validación.
// Cada afirmación y cada cifra sale de FORMULACION.md, DATOS_Y_SUPUESTOS.md o VALIDACION.md del estudio;
// el mapa afirmación → sección está en verificacion_modelo.md.
module.exports = [
  // ------------------------------------------------------------ 1. Decisiones del modelo
  {
    titulo: "Anexo: decisiones del modelo",
    subtitulo: "Qué elige la optimización y qué entra como dato en los casos sin data centers, base y libre",
    columnas: [
      {
        ancho: 12.13,
        bloques: [
          {
            tipo: "tabla",
            header: ["Qué", "Lo decide el modelo", "Dato"],
            filas: [
              ["Inversión en generación y almacenamiento", "Cuánto construir de cada candidato, dónde y cuándo", "Candidatos de la PELP con costo, tope y primer período"],
              ["Ampliación de transmisión", "MW por corredor y período, en forma continua", "34 corredores; costo, topes acumulados, obras comprometidas"],
              ["Despacho horario", "Generación y flujos entre zonas, hora a hora", "Disponibilidad de cada central; 6 días típicos de 24 h"],
              ["Carga y descarga de almacenamiento", "Carga, descarga y energía almacenada; ciclo diario", "Eficiencia y duración fija de cada proyecto"],
              ["Energía no suministrada", "ENS por zona y hora, también de data centers", "VOLL de 650 USD/MWh, el de AMEBA"],
              ["Ubicación de data centers", "Caso libre: zona del crecimiento desde 2030 (26 barras)", "Caso base: zona proyectada; siempre: MW medios por período"],
              ["Demanda", "—", "Carbono Neutralidad × 1,031, con H₂ y NH₃; inelástica"],
              ["Costos y combustibles", "—", "Inversión, O&M y combustibles de AMEBA; tasa de 6 %"],
              ["Perfiles renovables e hidrología", "Recorte renovable; reparto horario de la hidro en el día", "Perfiles de cambio climático; hidro mensual de AMEBA"],
              ["Impuesto al CO₂", "—", "Promedio por período: 0; 3,33; 10; 23,48; 35; 35; 35 USD/t"],
              ["Reserva", "Holgura de los proyectos elegibles, hora a hora", "Subida 551 MW y bajada 407 MW; 113 proyectos elegibles"],
            ],
            anchos: [3.15, 4.4, 4.58],
            letra: 12,
          },
          {
            tipo: "texto",
            texto: "—: no lo decide el modelo. Base y libre usan la misma red, los mismos días y el mismo horizonte; el caso sin data centers no agrega carga de data centers.",
            letra: 12,
            gris: true,
          },
        ],
      },
    ],
    fuente: "Fuente: elaboración propia con datos de Ministerio de Energía (2025, 2026a), CEN (2026a) y CEN (s. f.).",
    notas:
      "Siglas: PELP, Planificación Energética de Largo Plazo; AMEBA, modelo de optimización con que el Ministerio de Energía hizo la PELP 2023–2027; ENS, energía no suministrada; VOLL, valor de la carga perdida; O&M, operación y mantenimiento; H₂ y NH₃, hidrógeno y amoníaco; HVDC, enlace de corriente continua en alta tensión.\n" +
      "Inversión: el modelo parte en 2025, como AMEBA, y decide todas las inversiones desde ese año; no se usan las decisiones de inversión de AMEBA. Existente es lo que está en servicio el 1 de enero de 2025 según los datos de entrada de la PELP; lo comprometido en esos datos entra en el primer período en que está en servicio. Períodos: 2025 (2025–2026), 2027 (2027–2029), 2030, 2035, 2040, 2045 y 2050 (2050–2054); valor presente a 2025. El modelo es lineal y sin compromiso de unidades: no hay mínimos técnicos, rampas ni costos de partida.\n" +
      "Transmisión: cada corredor puede ampliarse hasta la suma de sus candidatos disponibles hasta ese período. Obras comprometidas: HVDC Kimal–Alto Jahuel (2.000 MW) y Río Malleco–Pichirropulli (660 MW), ambas en 2030.\n" +
      "Data centers: las zonas candidatas son las 26 barras eléctricas, no los 5 polos de generación; no hay tope por zona ni costo de conexión o de terreno. Antes de 2030 la ubicación es la proyectada también en el caso libre: lo que entra en 2025–2029 ya tiene sitio y solicitud de conexión, y los períodos 2025 y 2027 no tienen el HVDC. Después del horizonte de cada proyección, CEN y el escenario propio crecen 3 % anual, desde 2031 y 2033, respectivamente. Se supone que la demanda de la PELP ya incluye los data centers que operan hoy (unos 99 MW medios); por eso se agrega solo lo que supera ese nivel.",
  },

  // ------------------------------------------------------------ 2. Adaptaciones de los datos de la PELP
  {
    titulo: "Anexo: adaptaciones de los datos de la PELP",
    subtitulo: "Cambios respecto de los datos del modelo AMEBA y su motivo",
    columnas: [
      {
        ancho: 5.84,
        bloques: [
          { tipo: "texto", texto: "Tiempo, demanda y costos", letra: 14 },
          {
            tipo: "bullets",
            letra: 14,
            items: [
              "6 días típicos por período (meses impares) en vez de 12: con 12, la barrera de Gurobi se quedó sin memoria en 63 GB",
              "Impuesto al CO₂ promedio de cada período (0 a 35 USD/t), no el del año de inicio: cambia los precios relativos entre zonas",
              "Demanda × 1,031: AMEBA abastece 1,031 veces la serie en todas las barras; se interpreta como margen de pérdidas (hipótesis)",
              "Generación neta de servicios auxiliares (entre 2,0 y 2,6 % de la bruta), porque el balance de AMEBA solo cierra en neto",
              "Parte en 2025, como AMEBA, y decide todas las inversiones: lo que AMEBA construyó (3.000 MW FV, 1.000 MW eólicos, 92,1 MW de baterías, 2.672 MW de transmisión) no es dato",
            ],
          },
        ],
      },
      {
        ancho: 5.84,
        bloques: [
          { tipo: "texto", texto: "Tecnologías y red", letra: 14 },
          {
            tipo: "bullets",
            letra: 14,
            items: [
              "Hidro existente: energía fija por día típico, la que AMEBA despachó ese mes, porque los días típicos no se conectan entre sí",
              "CSP como generador variable con perfil fijo: como almacenamiento, Switch la cargaría desde la red y no desde su campo solar",
              "Baterías con su energía entregable (nominal × eficiencia de descarga), porque Switch aplica la eficiencia a la carga: 4 h → 3,84 h",
              "Reserva simplificada (551/407 MW de subida/bajada) sin tope por unidad: la nativa de Switch exige compromiso de unidades",
              "Transporte sin pérdidas en 34 corredores, sin flujo DC: 17 de 38 tramos de AMEBA tienen una reactancia que parece valor por omisión",
            ],
          },
        ],
      },
    ],
    fuente: "Fuente: elaboración propia con datos de Ministerio de Energía (2025).",
    notas:
      "Siglas: PELP, Planificación Energética de Largo Plazo; AMEBA, modelo de optimización con que el Ministerio de Energía hizo la PELP 2023–2027; FV, fotovoltaica; CSP, concentración solar de potencia; FP, factor de planta; flujo DC, flujo de corriente continua (leyes de Kirchhoff); HVDC, enlace de corriente continua en alta tensión.\n" +
      "Días típicos: enero, marzo, mayo, julio, septiembre y noviembre; cada uno representa también al mes siguiente. Son 144 horas por año, la resolución de la PELP 2028–2032. Con 12 días, además, el simplex dual seguía sin converger a los 110 minutos. Efecto sobre los insumos: demanda −0,04 a −0,09 %; energía hidro +4,9 % en 2035, +4,6 % en 2045, +6,6 % en 2050 y −1,8 % en 2030; FP eólico −5,3 % en 2035.\n" +
      "Impuesto al CO₂: AMEBA cobra 0 hasta 2027, 5 USD/t desde 2028 y 35 USD/t desde 2040. Con el valor del año de inicio, el período 2027 tendría 0 y el 2035 tendría 15,8 USD/t, aunque dentro de ese período llega a 31,1. Promedios: 0; 3,33; 10; 23,48; 35; 35 y 35 USD/t.\n" +
      "Demanda: el factor 1,031 no figura en ningún archivo de entrada de AMEBA; se encontró rehaciendo el balance de cada barra. Como AMEBA resuelve la red con pérdidas nulas, con él Switch abastece la misma energía que AMEBA. El consumo de H₂ y NH₃ entra como carga fija en la barra eléctrica que alimenta esas barras auxiliares, con el flujo horario de AMEBA.\n" +
      "Baterías: los 2.000 MW de baterías «ley», con inversión y O&M fijo nulos en los datos de la PELP, son candidatas a costo 0 desde el período 2027; no son predeterminadas. CSP: AMEBA no construye CSP en este escenario; la única existente es Cerro Dominador (110 MW). Reserva: primaria 331/85 MW y secundaria 220/322 MW (subir/bajar), sumadas; dan reserva 113 proyectos.\n" +
      "Otros cambios: los candidatos FV y eólicos se parten en clases de recurso por FP (sin ellas, la energía eólica de lo que construyó AMEBA quedaba hasta 7,5 % bajo AMEBA en 2030; con ellas, dentro de ±1 %, salvo la eólica de 2025, −6,9 %); una obra opera en un período si está en servicio el 1 de enero de su año de inicio, así que el HVDC Kimal–Alto Jahuel (2.000 MW, enero de 2029 en AMEBA) entra en el período 2030, igual que Río Malleco–Pichirropulli (660 MW, 1 de febrero de 2030); los topes anuales de inversión de AMEBA en FV y eólica se suman por período y no restringen; las líneas paralelas se suman en un corredor.\n" +
      "Siguen saliendo de resultados de AMEBA, como pendientes: la energía hidro por día típico, el perfil del consumo de H₂ y NH₃ y el factor 1,031 de la demanda.",
  },

  // ------------------------------------------------------------ 3. Validación
  {
    titulo: "Anexo: validación",
    subtitulo: "Comprobación de la traducción de AMEBA, de la formulación frente al curso y tamaño del problema",
    columnas: [
      {
        ancho: 6.4,
        bloques: [
          {
            tipo: "tabla",
            header: ["Entrada de Switch", "Comparada con AMEBA", "Dif. máx."],
            filas: [
              ["Demanda", "La que abasteció AMEBA, por año y zona", "0,000 %"],
              ["Capacidad existente", "498 celdas (año, clase, zona)", "0,0 %"],
              ["Costos de candidatos", "343 candidatos y 1.880 pares proyecto-período", "0,000 %"],
              ["Costo variable", "276 térmicas × 6 años", "0,0006 USD/MWh"],
              ["Perfiles", "FV, eólica e hidro candidata", "0,000 %"],
              ["Transmisión", "34 corredores, obras comprometidas y topes", "0,0 %"],
              ["Hidro", "Energía neta por zona y mes", "0,00 %"],
              ["Almacenamiento", "Potencia, energía entregable y eficiencia", "0,0 %"],
            ],
            anchos: [1.7, 3.45, 1.25],
            letra: 12,
            derecha: [2],
          },
          {
            tipo: "bullets",
            letra: 13,
            items: [
              "Versión con inicio en 2026: cada entrada se recalculó en forma independiente desde los datos crudos de AMEBA",
              "Réplica de AMEBA (versión 2026): misma capacidad térmica, hidro y existente; FV −15 % y eólica +4 % en 2030",
              "Módulos propios (data centers, reserva y límites de transmisión): 25 casos mínimos resueltos a mano, 63 de 63 comprobaciones",
            ],
          },
        ],
      },
      {
        ancho: 5.28,
        bloques: [
          { tipo: "texto", texto: "Ejemplo de la Clase 8 resuelto en Switch", letra: 14 },
          {
            tipo: "tabla",
            header: ["MW", "Nuclear", "Carbón", "Gas", "Petróleo"],
            filas: [
              ["Lámina del curso", "7.086", "1.918", "2.165", "0"],
              ["Switch", "7.086", "1.918", "2.165", "0"],
            ],
            anchos: [1.68, 0.9, 0.9, 0.9, 0.9],
            letra: 12,
            derecha: [1, 2, 3, 4],
          },
          {
            tipo: "texto",
            texto: "Igual en las 4 variantes probadas. Precios por bloque: 109,20; 27,52 y 12,56 USD/MWh, que cumplen la condición de inversión de la Clase 8.",
            letra: 12,
            gris: true,
          },
          { tipo: "texto", texto: "Cómputo", letra: 14 },
          {
            tipo: "bullets",
            letra: 13,
            items: [
              "Programa lineal de 1,54 millones de restricciones, 1,35 millones de variables y 8,07 millones de coeficientes",
              "Gurobi, barrera y crossover: 10 a 18 min por corrida, una a la vez",
              "Con 12 días típicos (2,68 millones de restricciones), la barrera se quedó sin memoria en 63 GB",
            ],
          },
        ],
      },
    ],
    fuente: "Fuente: elaboración propia con datos de Ministerio de Energía (2025) y la Clase 8 del curso.",
    notas:
      "La tabla de la izquierda resume la validación de la traducción de AMEBA hecha con la versión anterior de los casos (inicio en 2026); el método de traducción no cambió.\nSiglas: AMEBA, modelo de optimización con que el Ministerio de Energía hizo la PELP 2023–2027 (Planificación Energética de Largo Plazo); FV, fotovoltaica; ENS, energía no suministrada; O&M, operación y mantenimiento.\n" +
      "Cada fase se revisó en forma independiente, recalculando con código propio desde las fuentes. La tabla compara las entradas del escenario E2 con los datos crudos de AMEBA; el costo variable es precio × tasa de calor + O&M variable. Los costos de candidatos incluyen inversión, O&M fijo, años permitidos, límites y vida.\n" +
      "Réplica de AMEBA (E2, caso base): la transmisión es −2 % en 2030 y +8 % en 2050; las emisiones de 2030–2050 son 8–34 % mayores y el costo marginal medio 2–8 USD/MWh más alto, con el mismo orden entre zonas. Se explica por la formulación: 6 días típicos, transporte y programa lineal sin compromiso de unidades. Esta réplica se hizo con la versión anterior del modelo, que partía en 2026 y tomaba como dato lo que AMEBA construyó hasta 2025; las entradas de la versión con inicio en 2025 se verificaron de nuevo en forma independiente, sin errores.\n" +
      "Clase 8: cuatro variantes en Switch (sin descuento; con descuento al 7 %; inversión como O&M fijo; con ENS a 1.000 USD/MWh). Además, 12 de 12 ecuaciones de la formulación coinciden con las láminas de las Clases 4, 5, 8, 12 y 13.\n" +
      "No validado todavía: los costos y el ahorro de las corridas del escenario propio con el llenado de campus conectados no se recalcularon por separado; la condición de optimalidad de la ubicación no se ha verificado en las corridas con inicio en 2025, solo en una tanda anterior; no se sabe si la reserva ata; de 6 frente a 12 días solo se midió el efecto sobre los insumos.",
  },
];
