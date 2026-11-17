// Anexo de generación candidata. Generado por un script de elaboración propia; no editar a mano.
module.exports = [
  {
    "titulo": "Anexo: tecnologías candidatas",
    "subtitulo": "Tecnologías en que el modelo puede invertir entre 2025 y 2050: alcance, potencial y costo de inversión",
    "columnas": [
      {
        "ancho": 12.13,
        "bloques": [
          {
            "tipo": "tabla",
            "header": [
              "Tecnología",
              "Zonas",
              "Potencial máx. (MW)",
              "Desde",
              "Costo 2030 (USD/kW)",
              "Costo 2050 (USD/kW)"
            ],
            "filas": [
              [
                "Solar FV",
                "27",
                "661.787",
                "2025",
                "628–794",
                "454–573"
              ],
              [
                "Eólica",
                "20",
                "53.877",
                "2025",
                "1.020–1.408",
                "852–1.192"
              ],
              [
                "CSP (6, 9 y 13 h)",
                "13",
                "51.875",
                "2030 (13 h)",
                "4.800",
                "2.934–3.906"
              ],
              [
                "Hidro de pasada",
                "8",
                "6.313",
                "2035",
                "—",
                "3.250"
              ],
              [
                "Geotermia",
                "8",
                "1.682",
                "2030",
                "5.689",
                "4.960"
              ],
              [
                "Biomasa",
                "5",
                "201",
                "2027",
                "2.948",
                "2.761"
              ],
              [
                "Gas natural, ciclo combinado",
                "10",
                "sin límite práctico",
                "2030",
                "1.053",
                "1.053"
              ],
              [
                "Gas natural, ciclo abierto",
                "10",
                "sin límite práctico",
                "2030",
                "791",
                "791"
              ],
              [
                "Gas natural con captura de CO₂",
                "3",
                "sin límite práctico",
                "2030",
                "2.370",
                "1.769"
              ],
              [
                "Diésel, ciclo abierto",
                "4",
                "sin límite práctico",
                "2030",
                "470",
                "470"
              ],
              [
                "Baterías (1, 2, 4, 6 y 8 h)",
                "26",
                "85.000",
                "2025",
                "413–1.524",
                "314–1.144"
              ],
              [
                "Baterías «ley» (4 h)",
                "3",
                "2.000",
                "2027",
                "0",
                "0"
              ],
              [
                "Bombeo hidráulico",
                "13",
                "42.278",
                "2030",
                "1.605",
                "1.605"
              ],
              [
                "Aire comprimido (CAES, 4 h)",
                "26",
                "52.000",
                "2025",
                "1.014",
                "899"
              ],
              [
                "Carnot (4 y 12 h)",
                "2",
                "1.242",
                "2025",
                "796–1.433",
                "796–1.433"
              ]
            ],
            "anchos": [
              3.33,
              0.9,
              2.2,
              1.5,
              2.1,
              2.1
            ],
            "letra": 11,
            "derecha": [
              1,
              2,
              3,
              4,
              5
            ],
            "total": false
          }
        ]
      }
    ],
    "fuente": "Fuente: Ministerio de Energía (2025), datos del modelo AMEBA, escenario Carbono Neutralidad; elaboración propia.",
    "notas": "Siglas: FV, fotovoltaica; CSP, concentración solar de potencia, con almacenamiento térmico de 6, 9 o 13 h; CAES, almacenamiento por aire comprimido; Carnot, batería térmica que devuelve electricidad con una turbina, en carboneras reconvertidas; CO₂, dióxido de carbono; PDGE, polos de desarrollo de generación eléctrica; AMEBA, modelo de optimización con que el Ministerio de Energía hizo la PELP 2023–2027 (PELP, Planificación Energética de Largo Plazo). Candidatos son los proyectos que el modelo puede construir entre 2025 y 2050. Solo lo existente y lo comprometido en los datos de entrada de la PELP entran como capacidad predeterminada. Ninguna inversión que decidió AMEBA entra como dato: el modelo decide todas las inversiones desde 2025, y el potencial es el tope completo de cada candidato. No son candidatas las conversiones ya programadas: la co-combustión con amoníaco de Guacolda y tres reconversiones de 2026 (dos a biomasa y una a gas). Baterías «ley» (Kimal 500, 1.000 MW; Cumbre 500, 500 MW; Nueva Cardones 500, 500 MW): 2.000 MW de 4 h que en los datos de la PELP tienen inversión y O&M fijo nulos; son candidatas desde el período 2027, el primero que parte en 2026 o después (O&M, operación y mantenimiento). Los topes anuales de inversión de AMEBA en FV y eólica (3.000 y 1.000 MW en 2025; 50.000 MW por año desde 2026) se suman en los años de cada período y no restringen. Potencial: suma de los topes de los proyectos de cada zona (clases de recurso y de costo). En CSP, baterías y Carnot cada duración tiene su propio tope en la zona; se informa el mayor, sin sumar duraciones (en CSP y Carnot el tope es el mismo para todas). Gas natural y diésel: 10.000 MW por sitio, sin límite práctico. CSP: la de 13 h desde 2030 y las de 6 y 9 h desde 2035. Hidro de pasada desde 2035, a 3.250 USD/kW. Costo de inversión overnight, en USD/kW, variante «Medio» de AMEBA; el rango de baterías y Carnot es entre duraciones, el de FV y eólica entre zonas y clases de costo, y el de CSP 2050 entre duraciones y zonas."
  },
  {
    "titulo": "Anexo: candidatos por zona (norte)",
    "subtitulo": "Potencial máximo candidato por zona (MW), de Parinacota a Nueva Pan de Azúcar, y polos PDGE",
    "columnas": [
      {
        "ancho": 12.13,
        "bloques": [
          {
            "tipo": "tabla",
            "header": [
              "Zona",
              "FV",
              "Eólica",
              "CSP",
              "Hidro pasada",
              "Geotermia",
              "Biomasa",
              "Gas natural",
              "Diésel",
              "Baterías",
              "Bombeo",
              "CAES",
              "Carnot"
            ],
            "filas": [
              [
                "Parinacota 220",
                "38.866",
                "—",
                "3.712",
                "—",
                "346",
                "—",
                "—",
                "—",
                "5.000",
                "16.889",
                "2.000",
                "—"
              ],
              [
                "Nueva Pozo Almonte 220",
                "40.317",
                "—",
                "7.653",
                "—",
                "126",
                "—",
                "—",
                "✓",
                "5.000",
                "5.167",
                "2.000",
                "—"
              ],
              [
                "Lagunas 220",
                "36.307",
                "—",
                "12.608",
                "—",
                "—",
                "—",
                "—",
                "—",
                "5.000",
                "7.944",
                "2.000",
                "—"
              ],
              [
                "Kimal 220",
                "57.791",
                "1.102",
                "—",
                "—",
                "—",
                "—",
                "✓",
                "✓",
                "5.000",
                "—",
                "2.000",
                "—"
              ],
              [
                "Kimal 500",
                "11.551",
                "—",
                "4.150",
                "—",
                "139",
                "—",
                "✓",
                "—",
                "5.000",
                "833",
                "2.000",
                "853"
              ],
              [
                "Los Changos 500",
                "7.367",
                "—",
                "7.093",
                "—",
                "—",
                "—",
                "✓ + CCS",
                "—",
                "5.000",
                "1.722",
                "2.000",
                "389"
              ],
              [
                "Los Changos 220",
                "10.000",
                "156",
                "—",
                "—",
                "—",
                "—",
                "—",
                "—",
                "5.000",
                "—",
                "2.000",
                "—"
              ],
              [
                "Nueva Zaldívar 220",
                "23.394",
                "334",
                "8.526",
                "—",
                "387",
                "—",
                "✓",
                "—",
                "5.000",
                "—",
                "2.000",
                "—"
              ],
              [
                "Parinas 500",
                "43.244",
                "9.994",
                "—",
                "—",
                "—",
                "—",
                "✓",
                "—",
                "5.000",
                "1.389",
                "2.000",
                "—"
              ],
              [
                "Cumbre 500",
                "51.306",
                "132",
                "1.386",
                "—",
                "—",
                "—",
                "✓",
                "—",
                "5.000",
                "1.667",
                "2.000",
                "—"
              ],
              [
                "Nueva Cardones 500",
                "14.038",
                "—",
                "726",
                "—",
                "—",
                "—",
                "✓ + CCS",
                "—",
                "5.000",
                "—",
                "2.000",
                "—"
              ],
              [
                "Nueva Maitencillo 500",
                "27.153",
                "388",
                "240",
                "—",
                "—",
                "—",
                "—",
                "—",
                "2.000",
                "556",
                "2.000",
                "—"
              ],
              [
                "Nueva Pan de Azúcar 500",
                "26.151",
                "695",
                "40",
                "—",
                "—",
                "—",
                "—",
                "✓",
                "2.000",
                "1.944",
                "2.000",
                "—"
              ],
              [
                "Polos PDGE (5)",
                "11.558",
                "2.291",
                "5.742",
                "—",
                "—",
                "—",
                "—",
                "—",
                "—",
                "—",
                "—",
                "—"
              ]
            ],
            "anchos": [
              1.93,
              0.85,
              0.85,
              0.85,
              0.85,
              0.85,
              0.85,
              0.85,
              0.85,
              0.85,
              0.85,
              0.85,
              0.85
            ],
            "letra": 11,
            "derecha": [
              1,
              2,
              3,
              4,
              5,
              6,
              7,
              8,
              9,
              10,
              11,
              12
            ],
            "total": false
          }
        ]
      }
    ],
    "fuente": "Fuente: Ministerio de Energía (2025), datos del modelo AMEBA, escenario Carbono Neutralidad; elaboración propia.",
    "notas": "Cifras: potencial máximo en MW por zona; «✓», disponible sin límite práctico (10.000 MW por sitio); «—», sin candidato. Gas natural: ciclo combinado y ciclo abierto; «+ CCS» indica que además hay ciclo combinado con captura de CO₂ (CCS, captura y almacenamiento de carbono). Baterías: mayor tope entre duraciones (1, 2 y 4 h; las de 6 y 8 h tienen topes de 100 a 700 MW); no incluye las baterías «ley» (Kimal 500, 1.000 MW; Cumbre 500, 500 MW; Nueva Cardones 500, 500 MW). CSP y Carnot: tope común a todas sus duraciones. Los cinco polos PDGE (polos de desarrollo de generación eléctrica) se agrupan en una fila; por polo: Polo Tocopilla A1: FV 816 MW; Polo Tocopilla A2: FV 2.460 MW, CSP 1.413 MW; Polo Antofagasta B1: FV 4.174 MW, CSP 2.047 MW; Polo Antofagasta B2: Eólica 2.291 MW; Polo Antofagasta B3: FV 4.108 MW, CSP 2.282 MW."
  },
  {
    "titulo": "Anexo: candidatos por zona (centro y sur)",
    "subtitulo": "Potencial máximo candidato por zona (MW), de Quillota a Nueva Ancud",
    "columnas": [
      {
        "ancho": 12.13,
        "bloques": [
          {
            "tipo": "tabla",
            "header": [
              "Zona",
              "FV",
              "Eólica",
              "CSP",
              "Hidro pasada",
              "Geotermia",
              "Biomasa",
              "Gas natural",
              "Diésel",
              "Baterías",
              "Bombeo",
              "CAES",
              "Carnot"
            ],
            "filas": [
              [
                "Quillota 500",
                "11.274",
                "198",
                "—",
                "—",
                "—",
                "—",
                "—",
                "—",
                "2.000",
                "278",
                "2.000",
                "—"
              ],
              [
                "Polpaico 500",
                "11.189",
                "25",
                "—",
                "30",
                "—",
                "—",
                "—",
                "—",
                "2.000",
                "—",
                "2.000",
                "—"
              ],
              [
                "Alto Jahuel 500",
                "11.292",
                "6",
                "—",
                "—",
                "—",
                "—",
                "—",
                "—",
                "2.000",
                "—",
                "2.000",
                "—"
              ],
              [
                "Candelaria 500",
                "11.381",
                "—",
                "—",
                "129",
                "198",
                "—",
                "—",
                "—",
                "2.000",
                "—",
                "2.000",
                "—"
              ],
              [
                "Rapel 500",
                "41.577",
                "45",
                "—",
                "43",
                "—",
                "—",
                "—",
                "—",
                "2.000",
                "—",
                "2.000",
                "—"
              ],
              [
                "Ancoa 500",
                "57.392",
                "978",
                "—",
                "—",
                "—",
                "—",
                "—",
                "—",
                "2.000",
                "278",
                "2.000",
                "—"
              ],
              [
                "Concepción 500",
                "20.732",
                "5.156",
                "—",
                "—",
                "—",
                "63",
                "✓ + CCS",
                "—",
                "2.000",
                "278",
                "2.000",
                "—"
              ],
              [
                "Nueva Charrúa 500",
                "41.286",
                "3.940",
                "—",
                "1.973",
                "315",
                "46",
                "✓",
                "—",
                "2.000",
                "—",
                "2.000",
                "—"
              ],
              [
                "Mulchén 500",
                "28.018",
                "5.545",
                "—",
                "1.509",
                "72",
                "20",
                "✓",
                "—",
                "2.000",
                "—",
                "2.000",
                "—"
              ],
              [
                "Río Malleco 500",
                "28.603",
                "5.734",
                "—",
                "714",
                "99",
                "62",
                "—",
                "—",
                "2.000",
                "—",
                "2.000",
                "—"
              ],
              [
                "Pichirropulli 500",
                "—",
                "3.341",
                "—",
                "1.669",
                "—",
                "10",
                "—",
                "—",
                "2.000",
                "—",
                "2.000",
                "—"
              ],
              [
                "Nueva Puerto Montt 500",
                "—",
                "2.604",
                "—",
                "—",
                "—",
                "—",
                "—",
                "—",
                "2.000",
                "3.333",
                "2.000",
                "—"
              ],
              [
                "Nueva Ancud 500",
                "—",
                "11.212",
                "—",
                "246",
                "—",
                "—",
                "—",
                "✓",
                "2.000",
                "—",
                "2.000",
                "—"
              ]
            ],
            "anchos": [
              1.93,
              0.85,
              0.85,
              0.85,
              0.85,
              0.85,
              0.85,
              0.85,
              0.85,
              0.85,
              0.85,
              0.85,
              0.85
            ],
            "letra": 11,
            "derecha": [
              1,
              2,
              3,
              4,
              5,
              6,
              7,
              8,
              9,
              10,
              11,
              12
            ],
            "total": false
          }
        ]
      }
    ],
    "fuente": "Fuente: Ministerio de Energía (2025), datos del modelo AMEBA, escenario Carbono Neutralidad; elaboración propia.",
    "notas": "Cifras: potencial máximo en MW por zona; «✓», disponible sin límite práctico (10.000 MW por sitio); «—», sin candidato. Gas natural: ciclo combinado y ciclo abierto; «+ CCS» indica que además hay ciclo combinado con captura de CO₂ (CCS, captura y almacenamiento de carbono). Baterías: mayor tope entre duraciones (1, 2 y 4 h; las de 6 y 8 h tienen topes de 100 a 700 MW); no incluye las baterías «ley» (Kimal 500, 1.000 MW; Cumbre 500, 500 MW; Nueva Cardones 500, 500 MW). CSP y Carnot: tope común a todas sus duraciones. Los cinco polos PDGE (polos de desarrollo de generación eléctrica) se agrupan en una fila; por polo: Polo Tocopilla A1: FV 816 MW; Polo Tocopilla A2: FV 2.460 MW, CSP 1.413 MW; Polo Antofagasta B1: FV 4.174 MW, CSP 2.047 MW; Polo Antofagasta B2: Eólica 2.291 MW; Polo Antofagasta B3: FV 4.108 MW, CSP 2.282 MW."
  }
];
