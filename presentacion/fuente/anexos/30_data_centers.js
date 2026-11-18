// Anexos de data centers. Generado con un script de cálculo; cifras verificadas en verificacion_transmision_dc.md.
// Formato: FORMATO.md. Solo datos: build.js dibuja las láminas.
module.exports = [
  {
    titulo: "Anexo: escenarios de data centers",
    subtitulo: "Origen, ubicación base y carga media que cada escenario agrega al modelo",
    columnas: [
      {
        ancho: 12.13,
        bloques: [
          {
            tipo: "tabla",
            letra: 12,
            anchos: [1.1, 3.3, 1.85, 5.88],
            header: ["Escenario", "Origen", "Paso a MW medios", "Nodo o subestación → zona del modelo"],
            filas: [
              ["PELP E2", "PELP 2028–2032, escenario E2", "Carga de la PELP", "El Salto 220 kV → Polpaico 500 (85 %); Torquemada 110 kV → Quillota 500 (15 %)"],
              ["CEN", "Proyección de demanda 2026–2046 del CEN", "50 % de la capacidad", "RM → Polpaico 500 (1.225 MW); Valparaíso → Quillota 500 (155 MW), al 2030"],
              ["PELP N1", "PELP 2028–2032, escenario N1", "Carga de la PELP", "Como E2, más Kimal 220 kV → Kimal 220 (750 MW medios desde 2035)"],
              ["Propio", "Solicitudes de conexión vigentes al CEN", "50 % de lo solicitado", "Subestaciones de conexión → Polpaico 500, Alto Jahuel 500 y Quillota 500"]
            ]
          },
          {
            tipo: "tabla",
            letra: 12,
            anchos: [2.33, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4],
            derecha: [1, 2, 3, 4, 5, 6, 7],
            header: ["MW medios agregados", "2025", "2027", "2030", "2035", "2040", "2045", "2050"],
            filas: [
              ["PELP E2", "0,0", "99,0", "224,8", "272,8", "292,4", "311,9", "331,5"],
              ["CEN", "138,3", "381,7", "633,7", "750,4", "885,6", "1.042,5", "1.224,3"],
              ["PELP N1", "37,5", "324,0", "749,8", "1.022,8", "1.042,4", "1.061,9", "1.081,5"],
              ["Propio", "19,5", "460,5", "1.937,7", "2.360,5", "2.752,2", "3.206,3", "3.732,8"],
              ["Propio, de ella fija", "11,5", "69,1", "115,2", "115,2", "115,2", "115,2", "115,2"]
            ]
          },
          {
            tipo: "texto",
            letra: 12,
            gris: true,
            texto: "Carga por encima de los ~99 MW medios de data centers que ya están en la demanda. Cada período usa el promedio de la trayectoria anual en sus años (2025 = 2025–2026; 2050 = 2050–2054). Después de su horizonte, CEN crece 3 % anual desde 2031 y Propio 3 % anual desde 2033; E2 y N1 traen su propio crecimiento."
          }
        ]
      }
    ],
    fuente: "Fuente: Ministerio de Energía (2026a), CEN (2026a), CEN (s. f.); elaboración propia.",
    notas: "Siglas: PELP, Planificación Energética de Largo Plazo; CEN, Coordinador Eléctrico Nacional; RM, Región Metropolitana; S/E, subestación; MW medios, potencia media anual (carga plana).\nPELP E2 y N1: la PELP 2028–2032 trae los data centers como cargas planas en nodos de su red de 234 nodos. RM + Valparaíso: 99 MW medios en 2025 y 2026, 297 en 2030, 364 en 2035 y 450 en 2057, siempre 85 % / 15 %. N1 agrega Antofagasta (S/E Kimal 220 kV): 75 MW medios más por año desde 2026 hasta 750 en 2035. El Salto queda casi en empate entre Polpaico 500 y Alto Jahuel 500; se asigna a Polpaico 500 por su línea de 220 kV y la distancia.\nCEN: capacidad identificada de 398 MW en 2025, 552 en 2026, 642 en 2027, 963 en 2028, 1.281 en 2029 y 1.381 en 2030, con 50 % de utilización; reparto RM 1.225 MW y Valparaíso 155 MW. La proyección llega a 2030; desde 2031 la capacidad crece 3 % anual, hasta 2.807 MW en 2054.\nPropio: 3.811 MW solicitados = 1.905,5 MW medios en 2032, más 115,2 MW medios fijos por el llenado de campus ya conectados (11,5 en promedio en 2025–2026 y 69,1 en 2027–2029). Desde 2033 la demanda total de data centers (99 + 115,2 + 1.905,5 = 2.119,7 MW medios en 2032) crece 3 % anual; el aumento es carga nueva y ubicable, con ubicación base en proporción a lo solicitado.\nSe descuentan los ~99 MW medios existentes: 84,15 en Polpaico 500 y 14,85 en Quillota 500. En el caso libre, el modelo puede mover desde 2030 todo lo que no es fijo; antes de 2030 la ubicación es la base."
  },
  {
    titulo: "Anexo: escenario propio, campus (1/2)",
    subtitulo: "Campus con solicitud de conexión vigente desde 2026, uno por fila: zona Polpaico 500",
    columnas: [
      {
        ancho: 12.13,
        bloques: [
          {
            tipo: "tabla",
            letra: 12,
            anchos: [3.15, 2.85, 1.35, 0.9, 2.2, 1.68],
            derecha: [3],
            total: true,
            header: ["Campus (titular)", "Subestación", "Zona del modelo", "MW solic.", "Estado (CEN)", "Fecha estimada"],
            filas: [
              ["SAN2 (Cirion)", "Distribución (Quilicura)", "Polpaico 500", "20", "Sin solicitud al CEN", "2026"],
              ["Quilicura, dos alimentadores (Scala)", "Chacabuco y Quilicura 23 kV", "Polpaico 500", "24", "En construcción y autorizada", "mar-2026 y may-2027"],
              ["DC Santiago I y II (ACS)", "Chacabuco 23 kV y Punta Verde 110 kV", "Polpaico 500", "54", "En tramitación y detenida", "jul-2028 y jul-2029"],
              ["SCL4 (Ascenty)", "Punta Verde 110 kV", "Polpaico 500", "150", "En tramitación", "dic-2028"],
              ["Campus Norte, etapa II (Eléc. Chicureo)", "Chicureo 220 kV", "Polpaico 500", "200", "En tramitación", "dic-2028"],
              ["SC1 (SAE Ladera Sur)", "Manuel Rodríguez 220 kV", "Polpaico 500", "300", "Detenida", "mar-2029"],
              ["DC Hermes (Mytilineos)", "Nueva Lampa 220 kV", "Polpaico 500", "100", "En tramitación", "dic-2029"],
              ["SC2 (RTB Energy)", "Polpaico 500 kV", "Polpaico 500", "500", "En tramitación", "jul-2030"],
              ["Mega Data Center Lampa, etapa 2 (Scala)", "Santa Teresa 220 kV", "Polpaico 500", "300", "Autorizada", "oct-2032"],
              ["Total Polpaico 500", "", "", "1.648", "", ""]
            ]
          },
          {
            tipo: "bullets",
            letra: 12,
            items: ["Fuera: 12 solicitudes con conexión hasta 2025 (428,4 MW, ya en la demanda), 2 que repiten otra del mismo campus (14 MW) y 2 que no informan MW", "Cirion SAN2 se conecta en distribución y no figura en el CEN; los anuncios sin año de conexión no se consideran"]
          }
        ]
      }
    ],
    fuente: "Fuente: Ministerio de Energía (2026a), CEN (2026a), CEN (s. f.); elaboración propia.",
    notas: "Siglas: CEN, Coordinador Eléctrico Nacional; S/E, subestación; MW solic., MW solicitados en la solicitud de conexión.\nBase: catastro de solicitudes de conexión de data centers a la plataforma de Acceso Abierto del CEN, al 13-nov-2026, con las vigentes (no rechazadas ni desistidas) con fecha estimada de conexión: 35 solicitudes, 4.233,4 MW.\nUn campus aparece una vez. Quilicura (Scala) son dos alimentadores en S/E distintas (12 + 12 MW, 2026 y 2027); DC Santiago I y II (ACS) son dos edificios (14 + 40 MW). Las repetidas son el segundo alimentador de 14 MW de DC Santiago I (misma S/E y fecha) y una solicitud detenida de SCL4 sin MW.\nZona: la barra de 500/220 kV que abastece la subestación de conexión. SC1 y SC2 tienen distinto titular, subestación y potencia, y se cuentan como dos campus.\nLas 2 solicitudes vigentes sin fecha (alimentadores de ODATA, 16,6 MW) son obras de 2022 de un campus existente.\nEs una cota superior: toma toda la cartera vigente, sin probabilidad de realización."
  },
  {
    titulo: "Anexo: escenario propio, campus (2/2)",
    subtitulo: "Campus con solicitud de conexión vigente desde 2026: zonas Alto Jahuel 500 y Quillota 500",
    columnas: [
      {
        ancho: 12.13,
        bloques: [
          {
            tipo: "tabla",
            letra: 12,
            anchos: [3.15, 2.85, 1.35, 0.9, 2.2, 1.68],
            derecha: [3],
            total: true,
            header: ["Campus (titular)", "Subestación", "Zona del modelo", "MW solic.", "Estado (CEN)", "Fecha estimada"],
            filas: [
              ["Proyecto Rivera (Inmobiliaria STPA)", "Bajos de Mena 110 kV", "Alto Jahuel 500", "200", "En tramitación", "sep-2028"],
              ["San Bernardo, ampliación (ODATA)", "Odata San Bernardo 110 kV", "Alto Jahuel 500", "48", "Autorizada", "mar-2029"],
              ["Noviciado I (Ignis)", "Lo Aguirre 500 kV", "Alto Jahuel 500", "500", "En tramitación", "nov-2030"],
              ["Lo Aguirre y Lo Aguirre A (Lader Energy)", "Lo Aguirre 500 kV y Lo Prado 44 kV", "Alto Jahuel 500", "525", "En tramitación", "ene-2031"],
              ["Moreras (Orion Power)", "Alto Jahuel 110 kV", "Alto Jahuel 500", "90", "En tramitación", "may-2031"],
              ["DC Valparaíso 1 y 2 (FR Data)", "La Pólvora 220 kV", "Quillota 500", "300", "En tramitación", "abr-2028"],
              ["Pacífico 33-S (Ignis)", "La Pólvora 220 kV", "Quillota 500", "500", "En tramitación", "nov-2030"],
              ["Total de los 16 campus", "", "", "3.811", "", ""]
            ]
          },
          {
            tipo: "bullets",
            letra: 12,
            items: ["MW medios = 50 % de los MW solicitados, como carga plana desde el año estimado de conexión: 3.811 MW solicitados dan 1.905,5 MW medios en 2032 (824 en Polpaico 500, 681,5 en Alto Jahuel 500 y 400 en Quillota 500); desde 2033 el total de data centers crece 3 % anual", "Llenado de los campus ya conectados: 428,4 MW × 50 % − 99 = 115,2 MW medios fijos (93,7 en Polpaico 500 y 21,5 en Alto Jahuel 500), con rampa de 20 % por año hasta 2030"]
          }
        ]
      }
    ],
    fuente: "Fuente: Ministerio de Energía (2026a), CEN (2026a), CEN (s. f.); elaboración propia.",
    notas: "Lo Aguirre secciona la línea Polpaico–Alto Jahuel y queda casi en empate eléctrico entre ambas zonas; va a Alto Jahuel 500 porque la red de la PELP 2023–2027 lleva ahí el terminal del HVDC Kimal–Lo Aguirre (HVDC: enlace de corriente continua en alta tensión).\nNoviciado I y Pacífico 33-S (Ignis) son dos campus: otro nombre, otra comuna y otra región. Lo Aguirre y Lo Aguirre A (Lader Energy) son 500 + 25 MW en S/E distintas; DC Valparaíso 1 y 2 (FR Data) son 200 + 100 MW en paños distintos.\nUna fecha dentro de un año cuenta el año completo; cada período del modelo usa el promedio de sus años (8,0 MW medios en 2025–2026, 391,3 en 2027–2029 y 1.822,5 en 2030–2034, este último ya con el crecimiento de 2033–2034).\nCrecimiento: desde 2033, la demanda total de data centers, 2.119,7 MW medios en 2032 (99 ya en la demanda, 115,2 de llenado y 1.905,5 solicitados), crece 3 % anual. El aumento se agrega como carga ubicable y su ubicación base sigue el reparto de lo solicitado; en 2050–2054 el escenario agrega 3.732,8 MW medios.\nLlenado: las conexiones existentes suman 428,4 MW; al 50 % consumirían 214,2 MW medios, frente a los ~99 que consumen hoy. La diferencia entra fija, en proporción a los MW conectados por zona.\nEn 2030 la cartera suma 2.896 MW solicitados, frente a 1.381 MW que identifica el CEN."
  }
];
