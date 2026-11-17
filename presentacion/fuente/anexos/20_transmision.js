// Anexos de transmisión. Generado con un script de cálculo; cifras verificadas en verificacion_transmision_dc.md.
// Formato: FORMATO.md. Solo datos: build.js dibuja las láminas.
module.exports = [
  {
    titulo: "Anexo: corredores de transmisión (norte)",
    subtitulo: "Corredores de red de Parinacota a Nueva Pan de Azúcar: capacidad inicial, obras y tope de ampliación",
    columnas: [
      {
        ancho: 8.3,
        bloques: [
          {
            tipo: "tabla",
            header: ["Corredor", "Existente (MW)", "Obra comprometida", "Ampliación máx. 2050"],
            filas: [
              ["Nueva Pozo Almonte 220 – Parinacota 220", "450", "—", "4.500"],
              ["Nueva Pozo Almonte 220 – Lagunas 220", "662", "—", "4.500"],
              ["Lagunas 220 – Kimal 220", "789", "—", "4.500"],
              ["Kimal 500 – Kimal 220", "1.500", "—", "5.300"],
              ["Kimal 220 – Nueva Zaldívar 220", "815", "—", "4.500"],
              ["Kimal 220 – Los Changos 220", "900", "—", "0"],
              ["Kimal 500 – Los Changos 500", "1.590", "—", "4.500"],
              ["Los Changos 500 – Los Changos 220", "1.500", "—", "4.300"],
              ["Los Changos 220 – Nueva Zaldívar 220", "525", "—", "4.500"],
              ["Los Changos 500 – Parinas 500", "1.500", "—", "4.500"],
              ["Parinas 500 – Nueva Zaldívar 220", "660", "—", "4.500"],
              ["Parinas 500 – Cumbre 500", "1.500", "—", "4.500"],
              ["Cumbre 500 – Nueva Cardones 500", "2.090", "—", "4.500"],
              ["Nueva Cardones 500 – Nueva Maitencillo 500", "2.368", "—", "5.500"],
              ["Nueva Maitencillo 500 – Nueva Pan de Azúcar 500", "2.375", "—", "5.500"]
            ],
            anchos: [3.6, 1.35, 1.65, 1.7],
            letra: 11,
            derecha: [1, 2, 3]
          }
        ]
      },
      {
        ancho: 3.38,
        bloques: [
          {
            tipo: "bullets",
            letra: 12,
            items: ["Existente: líneas en servicio el 1 de enero de 2025 según los datos de entrada de la PELP", "Ampliación máxima: tope acumulado de los candidatos de la PELP hasta 2050", "Kimal 220 – Los Changos 220 no tiene candidatos y no se amplía", "Enlaces PDGE: 5 enlaces unen los polos de generación con Cumbre 500, Kimal 500, Los Changos 500 y Parinas 500; parten en 0 MW, sin tope efectivo y con costo de 1 USD/MW"]
          }
        ]
      }
    ],
    fuente: "Fuente: Ministerio de Energía (2025), datos del modelo AMEBA; elaboración propia.",
    notas: "Siglas: PELP, Planificación Energética de Largo Plazo (aquí, la 2023–2027, escenario Carbono Neutralidad); AMEBA, modelo de optimización con que el Ministerio de Energía hizo esa PELP; PDGE, polos de desarrollo de generación eléctrica; HVDC, enlace de corriente continua en alta tensión.\nPolos PDGE: ANF-B1, ANF-B2, ANF-B3, TOC-A1 y TOC-A2. No son zonas candidatas para data centers.\nLas 161 líneas de AMEBA quedan en 34 corredores: 29 de red y 5 de enlace a polos PDGE. Las líneas paralelas se suman en un corredor. La capacidad existente de los 29 corredores suma 38.519 MW: las líneas de los datos de entrada en servicio el 1 de enero de 2025. Lo que AMEBA decidió construir no es un dato: sus 2.672 MW de 2025, en 7 corredores, siguen siendo candidatos y los decide el modelo.\nLos números se redondean a MW; el nombre de cada corredor sigue el orden de las barras en la PELP."
  },
  {
    titulo: "Anexo: corredores de transmisión (centro-sur)",
    subtitulo: "Corredores de red de Nueva Pan de Azúcar a Nueva Ancud y el HVDC Kimal–Lo Aguirre",
    columnas: [
      {
        ancho: 8.3,
        bloques: [
          {
            tipo: "tabla",
            header: ["Corredor", "Existente (MW)", "Obra comprometida", "Ampliación máx. 2050"],
            filas: [
              ["Nueva Pan de Azúcar 500 – Polpaico 500", "2.500", "—", "5.500"],
              ["Kimal 500 – Alto Jahuel 500", "0", "2.000 MW (2030)", "6.000"],
              ["Quillota 500 – Polpaico 500", "1.803", "—", "4.500"],
              ["Polpaico 500 – Alto Jahuel 500", "1.880", "—", "4.500"],
              ["Candelaria 500 – Alto Jahuel 500", "680", "—", "4.500"],
              ["Rapel 500 – Alto Jahuel 500", "394", "—", "4.500"],
              ["Alto Jahuel 500 – Ancoa 500", "4.000", "—", "6.000"],
              ["Ancoa 500 – Nueva Charrúa 500", "3.000", "—", "4.500"],
              ["Concepción 500 – Nueva Charrúa 500", "260", "—", "4.500"],
              ["Nueva Charrúa 500 – Mulchén 500", "1.540", "—", "6.000"],
              ["Río Malleco 500 – Mulchén 500", "1.290", "—", "4.500"],
              ["Río Malleco 500 – Pichirropulli 500", "483", "660 MW (2030)", "6.160"],
              ["Pichirropulli 500 – Nueva Puerto Montt 500", "805", "—", "4.500"],
              ["Nueva Puerto Montt 500 – Nueva Ancud 500", "660", "—", "4.500"]
            ],
            anchos: [3.6, 1.35, 1.65, 1.7],
            letra: 11,
            derecha: [1, 2, 3]
          }
        ]
      },
      {
        ancho: 3.38,
        bloques: [
          {
            tipo: "bullets",
            letra: 12,
            items: ["HVDC Kimal–Lo Aguirre: en la red de la PELP llega a Alto Jahuel 500; 2.000 MW forzados en 2030 y tope acumulado de 6.000 MW al 2050", "Río Malleco – Pichirropulli: 660 MW forzados en 2030", "Capacidad existente de los 29 corredores: 38.519 MW"]
          }
        ]
      }
    ],
    fuente: "Fuente: Ministerio de Energía (2025), datos del modelo AMEBA; elaboración propia.",
    notas: "HVDC: enlace de corriente continua en alta tensión. En la PELP 2023–2027 el HVDC Kimal–Lo Aguirre tiene 2.000 MW y fecha enero de 2029. Una obra opera en un período si está en servicio el 1 de enero de su año de inicio; el período 2027 (2027–2029) parte antes, así que el HVDC entra en el período 2030. Antes de 2030 el corredor Kimal 500 – Alto Jahuel 500 tiene capacidad 0 y no puede ampliarse. Río Malleco – Pichirropulli tiene fecha 1 de febrero de 2030 y opera 11 de los 12 meses de ese año, así que también entra en el período 2030.\nLa ampliación máxima incluye la obra comprometida: en Kimal 500 – Alto Jahuel 500, 6.000 MW = 2.000 MW comprometidos + 4.000 MW de candidatos; en Río Malleco – Pichirropulli, 6.160 MW = 660 + 5.500.\nExistente total de los 29 corredores: 38.519 MW, en servicio el 1 de enero de 2025; lo que AMEBA construye desde 2025 no entra como dato."
  },
  {
    titulo: "Anexo: ampliación de la transmisión",
    subtitulo: "Cómo decide el modelo la capacidad de cada corredor entre 2025 y 2050",
    columnas: [
      {
        ancho: 7.2,
        bloques: [
          {
            tipo: "bullets",
            letra: 14,
            items: ["Solo se amplían los 34 corredores del modelo (29 de red y 5 enlaces PDGE); no se crean corredores entre otras zonas. El único de red sin capacidad inicial, Kimal 500 – Alto Jahuel 500, nace con el HVDC en 2030", "Ampliación continua, en MW por corredor y período, sin proyectos discretos", "Costo lineal: costo de inversión de la PELP por corredor (17.950 a 625.600 USD/MW), anualizado a 40 años y 6 % (factor 0,0665), sin O&M", "Obras comprometidas forzadas: HVDC Kimal–Lo Aguirre (2.000 MW) y Río Malleco – Pichirropulli (660 MW), en 2030", "Tope acumulado por período: suma de los candidatos de la PELP disponibles hasta ese período (entran en 2025, 2035, 2040 y 2050)", "Modelo de transporte sin pérdidas: el flujo en cada sentido no supera la capacidad; sin leyes de Kirchhoff"]
          }
        ]
      },
      {
        ancho: 4.48,
        bloques: [
          {
            tipo: "texto",
            texto: "Tope acumulado de ampliación (MW)",
            letra: 12
          },
          {
            tipo: "tabla",
            header: ["Período", "HVDC", "Típico"],
            filas: [
              ["2025", "0", "500"],
              ["2027", "0", "500"],
              ["2030", "2.000 (forzada)", "500"],
              ["2035", "3.500", "2.000"],
              ["2040", "5.000", "3.500"],
              ["2045", "5.000", "3.500"],
              ["2050", "6.000", "4.500"]
            ],
            anchos: [1.2, 1.78, 1.5],
            letra: 12,
            derecha: [1, 2]
          },
          {
            tipo: "texto",
            gris: true,
            letra: 12,
            texto: "HVDC: Kimal 500 – Alto Jahuel 500. Típico: 19 de los 28 corredores de red ampliables."
          }
        ]
      }
    ],
    fuente: "Fuente: Ministerio de Energía (2025), datos del modelo AMEBA; elaboración propia.",
    notas: "Siglas: PDGE, polos de desarrollo de generación eléctrica; HVDC, enlace de corriente continua en alta tensión; O&M, operación y mantenimiento; PELP, Planificación Energética de Largo Plazo 2023–2027.\nLa obra comprometida es un mínimo del período en que entra (incremental); el tope es acumulado, para que un mismo candidato no se construya una vez por período.\nAnualidad: 1.193 a 41.578 USD/MW-año. Los enlaces PDGE cuestan 1 USD/MW, como en la PELP.\nEl modelo cobra también la anualidad de la capacidad existente y comprometida; es un costo constante que se cancela al comparar casos.\nTransporte: en la red de la PELP 2028–2032, un modelo de transporte deja pasar 20–40 % más flujo norte–centro que un flujo DC; abastecer la Región Metropolitana sale más barato de lo que es."
  }
];
