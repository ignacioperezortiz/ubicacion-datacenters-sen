// Contenido de motivación, búsqueda bibliográfica y referencias de la presentación de avance.
// Cada cifra viene de un documento público de la lista «referencias» (los PDF no van en el repositorio) y fue verificada por al menos dos agentes
// (fuente\motivacion.md, fuente\graficos_motivacion_A|B\, fuente\literatura_*\, fuente\verificacion\).
module.exports = {
  motivacion: [
    {
      titulo: "Motivación: data centers",
      subtitulo: "Demanda eléctrica de los data centers en el mundo, en EE. UU. y en Chile",
      bullets: [
        "La demanda eléctrica de los data centers crece rápido: en el mundo, más que se duplicaría entre 2024 y 2030 (IEA, 2025)",
        "En EE. UU. ya es el 4,4 % del consumo eléctrico y podría llegar al 12 % en 2028 (Shehabi et al., 2024)",
        "En Chile, las solicitudes de conexión más que duplican lo que proyecta el Coordinador al 2030, y el 81 % apunta a la RM (CEN, 2026a; CEN, s. f.)",
      ],
      graficos: [
        {
          forma: "columnas", titulo: "Mundo: consumo de los data centers (TWh)", etiquetas_datos: true,
          etiquetas: ["2020", "2023", "2024", "2030*", "2035*"],
          series: [{ nombre: "TWh", valores: [269, 361, 416, 946, 1193] }],
          fuente: "Fuente: IEA (2025), tabla A.1. *Proyección, escenario base.",
        },
        {
          forma: "columnas", titulo: "EE. UU.: consumo de los data centers (TWh)", etiquetas_datos: true,
          etiquetas: ["2014", "2018", "2023", "2028 bajo*", "2028 alto*"],
          series: [{ nombre: "TWh", valores: [60, 76, 176, 325, 580] }],
          fuente: "Fuente: Shehabi et al. (2024). 2014: ~60 TWh. *Rango proyectado.",
        },
        {
          forma: "columnas", titulo: "Chile: data centers proyectados y solicitados (MW)", etiquetas_datos: false,
          etiquetas: ["2025", "2026", "2027", "2028", "2029", "2030"],
          series: [
            { nombre: "Solicitudes vigentes (acumuladas)", valores: [428, 440, 452, 1330, 1818, 3318] },
            { nombre: "Proyección del CEN", valores: [398, 552, 642, 963, 1281, 1381] },
          ],
          fuente: "Fuente: CEN (2026a), fig. 5-13; CEN (s. f.), por año de conexión declarado.",
        },
      ],
      notas:
        "IEA (2025), tabla A.1: 269 TWh (2020), 361 (2023), 416 (2024); escenario base 946 (2030) y 1.193 (2035). En 2035 el rango entre escenarios va de ~700 a ~1.720 TWh.\n" +
        "Shehabi et al. (2024): ~60 TWh estables en 2014–2016, 76 TWh en 2018 (1,9 %), 176 TWh en 2023 (4,4 %) y 325 a 580 TWh en 2028 (6,7 % a 12 %).\n" +
        "Chile: el CEN estima 398 MW instalados en 2025 y 1.381 MW al 2030 (89 % en la RM). Las 37 solicitudes vigentes suman ~4,25 GW hasta 2032 (81 % RM, 19 % Valparaíso); al 2030 acumulan 3.318 MW, 2,4 veces lo proyectado. La serie acumula desde 2022: el valor de 2025 (428 MW) es la base ya conectada. Las 37 solicitudes corresponden a 20 campus; el doble conteo posible en MW es de a lo más ~55 MW.\n" +
        "Contexto adicional: en Virginia, Dominion suma 53,8 GW de data centers en etapas de contrato y 12,0 GW con contrato de servicio (julio de 2026).",
    },
    {
      titulo: "Motivación: sistema eléctrico chileno",
      subtitulo: "Congestión de la transmisión norte–centro, vertimiento renovable y ubicación de la nueva demanda",
      bullets: [
        "El corredor norte–centro se congestiona: el tramo Polpaico–Nueva Pan de Azúcar 500 kV estuvo desacoplado 1.305 h en 2025 (CEN, 2026b)",
        "Por congestión y exceso de oferta se recortaron 6.084 GWh eólicos y solares en 2025: energía que se pudo generar y no se usó (CEN, 2026b)",
        "La inversión llega en oleadas, primero solar y ahora almacenamiento, y el CEN proyecta costos marginales diurnos cercanos a cero en el norte (CNE, 2026; Ministerio de Energía, 2026b; CEN, 2026b)",
        "Se esperaría que la nueva demanda vaya donde sobra energía, pero el 89 % de los data centers proyectados al 2030 está en la RM (CEN, 2026a)",
      ],
      grafico: {
        forma: "columnas_apiladas", titulo: "Reducciones de generación eólica y solar en 2025 (GWh)",
        etiquetas: ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"],
        series: [
          { nombre: "Solar", valores: [505, 300, 430, 271, 132, 218, 170, 328, 426, 520, 554, 599] },
          { nombre: "Eólica", valores: [148, 102, 125, 66, 57, 69, 50, 166, 173, 211, 251, 215] },
        ],
        colores: ["111111", "BFBFBF"],
        fuente: "Fuente: CEN (2026b), figura 13. Total anual: 6.084 GWh, el 19 % de la generación eólica y solar.",
      },
      notas:
        "Con la congestión y el vertimiento, estas oleadas de inversión pueden leerse como sobreinversión respecto de la transmisión disponible.\n" +
        "Desacople: horas en que la línea opera en su límite y el sistema queda partido en zonas con costos marginales distintos (CEN, 2026b, tabla 4). El HVDC Kimal–Lo Aguirre (3.000 MW según el CEN; el modelo usa los 2.000 MW de la PELP 2023–2027), que alivia el corredor, entraría en 2029.\n" +
        "Vertimiento: se usa una sola serie, la del Coordinador. El 19 % es sobre lo generado; sobre lo disponible es 16 %.\n" +
        "Oleadas: la solar FV en operación llegó a 12,7 GW en agosto de 2026 (CNE, 2026); el almacenamiento en ejecución suma 10,2 GW frente a una meta de 6 GW al 2030 (Ministerio de Energía, 2026b); el 78 % de la potencia aprobada para conexión en 2025 incluye almacenamiento (CEN, 2026b).",
    },
  ],
  literatura: [
    {
      titulo: "Búsqueda bibliográfica",
      subtitulo: "Estudios sobre la ubicación de data centers en la planificación del sistema eléctrico",
      estudios: [
        {
          cita: "Onodera et al. (2026)",
          titulo: "Cell Reports Sustainability · Japón",
          bullets: [
            "Expansión de costo mínimo de generación, almacenamiento y transmisión al 2050, con 1.741 nodos",
            "Data centers en su ubicación actual frente a la que elige el modelo, con y sin restricciones de sitio",
            "Elegir la ubicación reduce entre 16 % y 20 % el costo extra de los data centers (12–14 % con restricciones)",
          ],
        },
        {
          cita: "Shao, Yu y Wong (2025)",
          titulo: "Int. J. Electr. Power Energy Syst. · PJM, EE. UU.",
          bullets: [
            "Planificación estocástica a 15 años en 21 zonas",
            "La ubicación de los data centers se decide junto con la generación, el almacenamiento y la transmisión",
            "Frente a ubicarlos sin coordinarse con la red, la inversión del sistema eléctrico baja 11,7 % y la operación 8,3 % (un año)",
          ],
        },
        { cita: "Tercer estudio", pendiente: "Falta decidir cuál." },
      ],
      cierre: "Para Chile no encontramos estudios que comparen el costo de la ubicación proyectada de los data centers con la que conviene al sistema",
      notas:
        "Onodera et al.: estrategias BAU (ubicación actual), ILA (el modelo elige entre sitios industriales que cumplen umbrales de riesgo, latencia, agua y transporte) y FLEX (el modelo elige libremente), comparadas con un caso sin data centers. FLEX reduce el costo adicional en 16,3 %, 19,7 % y 17,9 % según el crecimiento (bajo, medio, alto); ILA en 11,7 %, 14,1 % y 11,6 % (p. 5). Es la misma comparación y la misma métrica que usamos.\n" +
        "Shao et al.: programa estocástico de dos etapas con descomposición de Benders; la comparación conjunta vs. no conjunta es una instancia de un año (Tabla 7, p. 9). Sus porcentajes son sobre la inversión y la operación totales, no sobre el costo extra de los data centers.",
    },
  ],
  referencias: [
    "Comisión Nacional de Energía. (2026). Reporte mensual ERNC: septiembre 2026 (Vol. 121).",
    "Coordinador Eléctrico Nacional. (s. f.). Plataforma de Acceso Abierto: solicitudes de conexión [Base de datos]. Consultada el 13 de noviembre de 2026.",
    "Coordinador Eléctrico Nacional. (2026a). Proyección de demanda de largo plazo SEN 2026–2046.",
    "Coordinador Eléctrico Nacional. (2026b). Reporte anual de desempeño del Sistema Eléctrico Nacional, año 2025.",
    "International Energy Agency. (2025). Energy and AI.",
    "Johnston, J., Henriquez-Auba, R., Maluenda, B., & Fripp, M. (2019). Switch 2.0: A modern platform for planning high-renewable power systems. SoftwareX, 10, 100251.",
    "Ministerio de Energía. (2025). Planificación Energética de Largo Plazo 2023–2027: Informe definitivo.",
    "Ministerio de Energía. (2026a). Planificación Energética de Largo Plazo 2028–2032: Informe preliminar.",
    "Ministerio de Energía. (2026b). Reporte de proyectos: junio 2026.",
    "Newbery, D. (2026). Locating data centres efficiently in Britain – reformed transmission charging, energy subsidies or zonal pricing? (EPRG Working Paper 2623). University of Cambridge.",
    "Onodera, H., Shiraki, H., & Matsuhashi, K. (2026). Strategic data center siting can mitigate trade-offs between decarbonization and digitalization in Japan. Cell Reports Sustainability, 3(9), 100823.",
    "Shao, Z., Yu, N., & Wong, D. (2025). Stochastic long-term joint decarbonization planning for power systems and data centers: A case study in PJM. International Journal of Electrical Power & Energy Systems, 173, 111377.",
    "Shehabi, A., et al. (2024). 2024 United States data center energy usage report (LBNL-2001637). Lawrence Berkeley National Laboratory.",
  ],
};
