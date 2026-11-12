import json
import os
import re

OUT_DIR = "/Users/Osito/.gemini/antigravity/scratch/amsoil-imagenes"
with open(os.path.join(OUT_DIR, "catalogo-imagenes.json"), "r", encoding="utf-8") as f:
    raw_catalog = json.load(f)

# Exact ALS SKU -> Presentation mapping from the PDF (without prices)
ALS_SKU_INFO = {
    "AM28012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC OE 0W20 SP CUARTOS"),
    "AM29012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC OE 5W20 SP CUARTOS"),
    "AM86012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC OE 5W30 SP CUARTOS"),
    "AM86004": ("4 Galones", "AMSOIL 100% SYNTHETIC OE 5W30 SP GALON"),
    "AM86055": ("Estañón 55 Gal", "AMSOIL 100% SYNTHETIC OE 5W30 SP ESTAÑON"),
    "AM87012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC OE 5W40 SP CUARTOS"),
    "AM06012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC OE 10W30 SP CUARTOS"),
    "AM06004": ("4 Galones", "AMSOIL 100% SYNTHETIC OE 10W30 SP GALON"),
    "AM06055": ("Estañón 55 Gal", "AMSOIL 100% SYNTHETIC OE 10W30 SP ESTAÑON"),
    "AM24012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC OE 10W40 SP+ CUARTOS"),
    "AM02012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC OE 20W50 SP+ CUARTOS"),
    "AM02055": ("Estañón 55 Gal", "AMSOIL 100% SYNTHETIC OE 20W50 SP+ ESTAÑON"),
    "AMX0612": ("12 Cuartos", "AMSOIL 100% SYNTHETIC 10W30 XL"),
    "AMX8612": ("12 Cuartos", "AMSOIL 100% SYNTHETIC 5W30 XL"),
    "AML8612": ("12 Cuartos", "AMSOIL 100% SYNTHETIC EUROPEAN CAR FORMULA LS 5W30"),
    "AML86004": ("4 Galones", "AMSOIL 100% SYNTHET EUROPEAN 5W30 LS GAL"),
    "AML86055": ("Estañón 55 Gal", "AMSOIL 100% SYNTHET EUROPEAN FOR 5W30 LS"),
    "AMF8712": ("12 Cuartos", "AMSOIL 100% SYNTHETIC EUROPEAN CAR FORMULA FS 5W40"),
    "AME8712": ("12 Cuartos", "AMSOIL 100% SYNTHETIC EUROPEAN CAR FORMULA MS 5W40 ACEA C3"),
    "AME2812": ("12 Cuartos", "AMSOIL 100% SYNTHET EUROPEAN 0W20"),
    "AME8812": ("12 Cuartos", "AMSOIL 100% SYNTHET EUROPEAN 0W40 FS"),
    "AME8912": ("12 Cuartos", "AMSOIL 100% SYNTHET EUROPEAN 0W30 MS"),
    "AMH27012": ("12 Cuartos", "AMSOIL 100% SYNTHET SP 0W16 HYBRID MO QT"),
    "AMH28012": ("12 Cuartos", "AMSOIL 100% SYNTHET SP 0W20 HYBRID MO QT"),
    "AMS2812": ("12 Cuartos", "AMSOIL 100% SYNTHETIC SIGNATURE 0W20"),
    "AMS4012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC SIGNATURE 0W40"),
    "AMS4112": ("12 Cuartos", "AMSOIL 100% SYNTHETIC SIGNATURE 5W20"),
    "AMS8612": ("12 Cuartos", "AMSOIL 100% SYNTHETIC SIGNATURE 5W30"),
    "AMS8604": ("4 Galones", "AMSOIL 100% SYNTHETIC SIGNATURE 5W30 GAL"),
    "AMS86055": ("Estañón 55 Gal", "AMSOIL 100% SYNTH SIGNATURE 5W30 55 GAL"),
    "AMM88012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC SIGNATURE 5W50"),
    "AMS0612": ("12 Cuartos", "AMSOIL 100% SYNTHETIC SIGNATURE 10W30"),
    "AMZ06012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC 10W30 ZROD"),
    "AMZ24012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC 10W40 ZROD"),
    "AMZ02012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC 20W50 ZROD"),
    "AMBS012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC BRIGS & STRATTON 4T RACING OIL"),
    "AMR8412": ("12 Cuartos", "AMSOIL 100% SYNTHET DOMINATOR RAC 10W40"),
    "AMR8512": ("12 Cuartos", "AMSOIL 100% SYNTHETIC DOMINATOR RACING OIL 15W50"),
    "AM92012": ("12 Cuartos", "AMSOIL 100% SYN HIGH MILEAGE 10W30"),
    "AM93012": ("12 Cuartos", "AMSOIL 100% SYN HIGH MILEAGE 5W30"),
    "AM30012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC HD 5W40 CK-4 CUARTOS"),
    "AM30004": ("4 Galones", "AMSOIL 100% SYNTHETIC HD 5W40 CK-4 GALONES"),
    "AM30055": ("Estañón 55 Gal", "AMSOIL 100% SYNTHETIC HD 5W40 CK-4 ESTAÑÓN"),
    "AM26012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC HD 10W30 CK-4 CUARTOS"),
    "AM26004": ("4 Galones", "AMSOIL 100% SYNTHETIC HD 10W30 CK-4 GALONES"),
    "AM26002": ("2 x 2.5 Galones", "AMSOIL 100% SYNTHETIC HD 10W30 CK-4 5 GALONES"),
    "AM26055": ("Estañón 55 Gal", "AMSOIL 100% SYNTHETIC HD 10W30 CK-4 ESTAÑÓN"),
    "AM84012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC HD 15W40 CK4 CUARTOS"),
    "AM84004": ("4 Galones", "AMSOIL 100% SYNTHETIC HD 15W40 CK-4 GALONES"),
    "AM84002": ("2 x 2.5 Galones", "AMSOIL 100% SYNTHETIC HD 15W40 CK-4 GARRAFA"),
    "AM84055": ("Estañón 55 Gal", "AMSOIL 100% SYNTHETIC HD 15W40 CK-4 ESTAÑÓN"),
    "AM05055": ("Estañón 55 Gal", "AMSOIL SYNTHETIC BLEND 15W40 DIESEL CK-4"),
    "AM27012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC DIESEL DEXOS D 0W20 CUARTOS"),
    "AM85012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC DIESEL DEXOS D 5W30 CUARTOS"),
    "AMM86012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC MAX-DUTY 5W30 CK-4 CUARTOS"),
    "AMM86004": ("4 Galones", "AMSOIL 100% SYNTHETIC MAXDUTY 5W30 CK-4 GALONES"),
    "AMM86055": ("Estañón 55 Gal", "AMSOIL 100% SYNTHETIC MAXDUTY 5W30 CK-4 ESTAÑÓN"),
    "AMM30012": ("12 Cuartos", "AMSOIL 100% SYNTHET MAXDUTY 5W40 DIESEL CUARTOS"),
    "AMM30002": ("2 x 2.5 Galones", "AMSOIL 100% SYNTHET MAXDUTY 5W40 DIESEL 5 GALONES"),
    "AMM06012": ("12 Cuartos", "AMSOIL 100% SYNTHET MAXDUTY 10W30 QT"),
    "AMM06004": ("4 Galones", "AMSOIL 100% SYNTHET MAXDUTY 10W30 GAL"),
    "AMM07012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC MAX-DUTY 15W40 CK-4 CUARTOS"),
    "AMM07004": ("4 Galones", "AMSOIL 100% SYNTHETIC MAX-DUTY 15W40 CK-4 GALONES"),
    "AM62012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC SEVERE GEAR 75W85 GEAR LUBE GL-5 CUARTOS"),
    "AM63012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC 75W90 LONG LIFE GEAR LUBE GL-5 CUARTOS"),
    "AM65012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC 75W90 MANUAL TRANSMISSION & TRANSAXLE GEAR LUBE GL-4 CUARTOS"),
    "AM66012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC SEVERE GEAR 75W90 GEAR LUBE GL-5 CUARTOS"),
    "AM64012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC SEVERE GEAR 75W140 GEAR LUBE GL-5 CUARTOS"),
    "AM58012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC SEVERE GEAR 80W90 GEAR LUBE GL-5 CUARTOS"),
    "AM11012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC MANUAL SYNCHRO TRANSMISION FL CUARTOS"),
    "AM160-012": ("12 Tubos (4 oz)", "AMSOIL SLIP LOCK ADDITIVE (BLOQUEO)"),
    "AM20004": ("4 Galones", "AMSOIL 100% SYNTHETIC TORQUE DRIVE ATF GALONES"),
    "AM20002": ("2 x 2.5 Galones", "AMSOIL 100% SYNTHETIC TORQUE DRIVE ATF 5 GALONES"),
    "AM20055": ("Estañón 55 Gal", "AMSOIL 100% SYNTHETIC TORQUE DRIVE ATF ESTAÑÓN"),
    "AM22012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC MV OE ATF RED CUARTOS"),
    "AM22004": ("4 Galones", "AMSOIL 100% SYNTHETIC MV OE ATF RED 4 GL"),
    "AM22002": ("2 x 2.5 Galones", "AMSOIL 100% SYNTHETIC MV OE ATF RED 5 GALONES"),
    "AMS22012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC SIGNATURE MV ATF RED CUARTOS"),
    "AMF22012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC MV OE ATF FUEL EFFICIENT BLUE CUARTOS"),
    "AMF22004": ("4 Galones", "AMSOIL 100% SYNTHETIC MV OE ATF FUEL EFFICIENT BLUE 4 GAL"),
    "AMFS22012": ("12 Cuartos", "AMSOIL 100% SYNTH SIGNATURE SERIES ATF FUEL EFFICIENT BLUE CUARTOS"),
    "AM61012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC CVT FLUID CUARTOS"),
    "AMDCT012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC MULTI-VEHICLE DCT CUARTOS"),
    "AM91012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC ULV-ATF"),
    "AM08012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC SUPER SHIFT CUARTOS"),
    "AM79012": ("12 x 354 mL", "AMSOIL 100% SYNTHETIC DOT 3 & 4 BRAKE FLUID"),
    "AMD79012": ("12 x 354 mL", "AMSOIL 100% SYNT DOMINATOR BRAKE F DOT4"),
    "AM80012": ("12 x 473 mL", "AMSOIL 100% SYNTHETIC POWER STEERING FLD"),
    "AM90012": ("12 x 118 mL", "AMSOIL 100% SYNTH ASSEMBLY LUBE"),
    "AM39012": ("12 Cuartos", "AMSOIL SYNTHETIC BREAK-IN OIL SAE 30"),
    "AM19055": ("Estañón 55 Gal", "AMSOIL SYNTHETIC COMPRESSOR OIL ISO 68"),
    "AM89012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC SABER 2 STROKE"),
    "AM162-012": ("12 x 473 mL", "AMSOIL ENGINE & TRANSMISSION FLUSH"),
    "AM161-012": ("12 x 473 mL", "AMSOIL INJECTOR CLEAN+CETANE BOOST DIESL"),
    "AM164-012": ("12 x 177 mL", "AMSOIL UPPER CYLINDER GASOLINE ADDITIVE"),
    "AM167-006": ("6 x 354 mL", "AMSOIL DOMINATOR OCTANE BOOST"),
    "AM165-012": ("12 x 354 mL (12 oz)", "AMSOIL 100% SYNTHETIC PERFORMANCE IMPROVER"),
    "AM47010": ("Caja de 10 Tubos", "AMSOIL SYNTHETIC POLY OFF ROAD GREASE TUBOS"),
    "AMCL006": ("Caja de 6 Latas", "AMSOIL CHAIN LUBE"),
    "AM52010": ("Caja de 10 Tubos", "AMSOIL SYNTHETIC MULTI PURPOSE #2 GREASE"),
    "AM52120": ("Cuñete 120 lbs", "AMSOIL 100% SYNTHETIC RED GREASE 120 LBS"),
    "AM83004": ("4 Galones", "AMSOIL ANTI/COOLANT PASSENGER CAR 50/50 YELLOW"),
    "AM88004": ("4 Galones", "AMSOIL ANTIFREEZE COOLANT HD 50/50 RED"),
    "AMPS82012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC POWERSPORTS COOLANT"),
    "AM166-006": ("6 x 473 mL", "AMSOIL DOMINATOR COOLANT BOOST"),
    "AM31012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC 4T MC 10W30 SN/MA2 CUARTOS"),
    "AM23012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC 4T MC 10W40 SN/MA2 CUARTOS"),
    "AM23055": ("Estañón 55 Gal", "AMSOIL 100% SYNTHETIC 4T MC 10W40 ESTAÑÓN"),
    "AM21012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC 4T MC 20W50 SN/MA2 CUARTOS"),
    "AM41012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC SHOCK THERAPY #10"),
    "AM25012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC V-TWIN SAE 60 CUARTO"),
    "AM35012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC V-TWIN 15W60 CUARTO"),
    "AM36012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC V-TWIN 20W40 CUARTO"),
    "AM32012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC V-TWIN 20W50 CUARTO"),
    "AM33012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC V-TWIN PRIMARY FLUID CUARTO"),
    "AM34012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC V-TWIN TRANS FLUID CUARTO"),
    "AMD13012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC DOMINATOR SYNTH 2-STROKE OIL"),
    "AMI0012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC INTERCEPTOR 2-STROKER CUARTOS"),
    "AMAU8712": ("12 Cuartos", "AMSOIL 100% SYNTHETIC 5W40 ATV/UTV"),
    "AMAU012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC 5W50 ATV/UTV"),
    "AMAU24012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC 10W40 ATV/UTV"),
    "AMAU2512": ("12 Cuartos", "AMSOIL 100% SYNTHETIC ATV/UTV DCT"),
    "AMAU6212": ("12 Cuartos", "AMSOIL 100% SYNTHETIC ATV/UTV TRANSMISSION & DIFFERENTIAL FLUID"),
    "AMD2412": ("12 Cuartos", "AMSOIL 100% SYNTHETIC DIRT BIKE 10W40"),
    "AMD2512": ("12 Cuartos", "AMSOIL 100% SYNTHETIC DIRT BIKE 10W50"),
    "AMD2612": ("12 Cuartos", "AMSOIL 100% SYNTHETIC DIRT BIKE TRANS FL 80"),
    "AM42012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC MC METRIC 5W40 QT"),
    "AM40012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC METRIC MC 10W30 QT"),
    "AM37012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC METRIC MC 10W40 QT"),
    "AM38012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC METRIC MC 15W50 QT"),
    "AM13012": ("12 Cuartos", "AMSOIL 100% SYNTHETIC HP MARINE SYNT 2-STROKE OIL"),
    "AM163-012": ("12 x 118 mL", "AMSOIL MOTORCYC OCTANE BOOST 12 X 118ML"),
}

CATEGORY_META = {
    "01-motor-gasolina": {
        "name": "Aceites de Motor Gasolina",
        "short": "Motor Gasolina",
        "icon": "🚗"
    },
    "02-motor-diesel": {
        "name": "Aceites de Motor Diésel",
        "short": "Motor Diésel",
        "icon": "🚛"
    },
    "03-transmision-y-diferenciales": {
        "name": "Transmisiones y Diferenciales",
        "short": "Transmisión y Diferencial",
        "icon": "⚙️"
    },
    "04-motocicletas-atv-marino": {
        "name": "Motocicletas, ATV/UTV y Marino",
        "short": "Motos, ATV y Marino",
        "icon": "🏍️"
    },
    "05-aditivos-grasas-coolant-varios": {
        "name": "Aditivos, Grasas, Coolant y Fluidos",
        "short": "Aditivos, Grasas y Fluidos",
        "icon": "🧪"
    }
}

LINE_TECH_INFO = {
    "oe-synthetic": {
        "line_name": "Serie OE 100% Sintético (Gasolina)",
        "summary": "Lubricante 100% sintético formulado específicamente para cumplir y superar los intervalos de cambio recomendados por los fabricantes de equipo original (OEM). Ideal para motores modernos con inyección directa (GDI) y turbocargadores.",
        "benefits": [
            "Protección superior contra el desgaste (hasta 47% más protección que el estándar GM dexos1).",
            "100% de protección contra la pre-ignición a baja velocidad (LSPI) en motores turbo GDI.",
            "Excelente control de lodos y depósitos en altas temperaturas.",
            "Óptima fluidez en arranque en frío y ahorro de combustible."
        ],
        "specs": "API SP (Resource Conserving), ILSAC GF-6A / GF-6B, GM dexos1 Gen 3, Ford, Chrysler MS-6395",
        "service_life": "Intervalos recomendados por el fabricante del vehículo (OEM) o el monitor de vida útil del aceite."
    },
    "xl-synthetic": {
        "line_name": "Serie XL Extended-Life 100% Sintético",
        "summary": "Aceite 100% sintético potenciado con paquete extra de aditivos detergentes y neutralizadores de ácidos para quienes buscan extender sus cambios de aceite con total seguridad.",
        "benefits": [
            "Formulado para intervalos extendidos de hasta 12,000 millas (19,300 km) o 1 año.",
            "Reserva adicional de TBN para neutralizar ácidos de la combustión.",
            "Reduce el consumo de aceite por volatilidad y mantiene limpios los anillos del pistón.",
            "Protección comprobada contra LSPI y desgaste de árbol de levas."
        ],
        "specs": "API SP (Resource Conserving), ILSAC GF-6A, GM dexos1 Gen 3, ACEA A1/B1, Chrysler MS-6395, Ford",
        "service_life": "Hasta 12,000 millas (19,300 km) o 1 año, lo que ocurra primero."
    },
    "european-car-formula": {
        "line_name": "Serie Europea (European Car Formula)",
        "summary": "Ingeniería 100% sintética diseñada específicamente para las estrictas especificaciones de vehículos europeos de gasolina y diésel ligero (Volkswagen, Audi, BMW, Mercedes-Benz, Porsche, Volvo, Peugeot).",
        "benefits": [
            "Formulaciones de bajo, medio y completo contenido de cenizas sulfatadas (Low/Mid/Full SAPS) para proteger sistemas de emisiones (DPF/GPF y catalizadores).",
            "Estabilidad térmica excepcional para turbocargadores europeos de alta presión.",
            "Cumple rigurosas normas ACEA y aprobaciones de fabricantes europeos."
        ],
        "specs": "ACEA C3 / C2 / C5 / A3/B4, VW 504.00/507.00 / 508.00/509.00 / 502.00/505.00, MB 229.51 / 229.5, BMW LL-04 / LL-01, Porsche C30 / A40",
        "service_life": "Intervalos recomendados por el fabricante europeo del vehículo."
    },
    "hybrid": {
        "line_name": "Serie Híbrida 100% Sintética",
        "summary": "Desarrollado específicamente para los desafíos únicos de los motores híbridos eléctricos (HEV y PHEV), donde el ciclo constante de encendido y apagado genera condensación de agua, dilución por combustible y arranques frecuentes en frío.",
        "benefits": [
            "Inhibidores avanzados contra la corrosión y herrumbre causada por humedad y bajas temperaturas de operación.",
            "Dispersantes reforzados para manejar el agua y contaminantes propios del ciclo Stop-Start.",
            "Baja viscosidad ultra fluida para lubricación instantánea al activarse el motor de combustión."
        ],
        "specs": "API SP (Resource Conserving), ILSAC GF-6A / GF-6B (0W-16), Toyota / Honda / Hyundai / Kia Hybrid",
        "service_life": "Hasta 15,000 millas (24,100 km) o 1 año."
    },
    "signature-series": {
        "line_name": "Serie Signature 100% Sintético (Gasolina)",
        "summary": "El aceite insignia de máximo rendimiento de AMSOIL. Desarrollado para entusiastas y conductores que exigen la máxima protección existente en la industria automotriz.",
        "benefits": [
            "75% más protección del motor contra pérdida de potencia y desgaste que lo exigido por la norma de la industria.",
            "Protege los turbocargadores un 72% mejor que los requisitos de la prueba GM.",
            "28% más poder neutralizador de ácidos que Mobil 1 y limpieza superior de pistones.",
            "Resistencia extrema a la degradación térmica y oxidación."
        ],
        "specs": "API SP (Resource Conserving), ILSAC GF-6A, GM dexos1 Gen 3, Ford WSS-M2C961-A1, Chrysler MS-6395",
        "service_life": "Hasta 25,000 millas (40,200 km), 700 horas de operación o 1 año."
    },
    "racing-zrod-dominator": {
        "line_name": "Serie Racing, Z-ROD y Motores de Alto Desempeño",
        "summary": "Lubricantes 100% sintéticos de alta película lubricante y alto contenido de Zinc/Fósforo (ZDDP) para motores de competencia (DOMINATOR), autos clásicos/modificados con árboles de levas planos (Z-ROD) y motores 4T de competencia (Briggs & Stratton).",
        "benefits": [
            "Alto nivel de ZDDP (Zinc y Fósforo) para máxima protección en levas planas (flat-tappet), balancines y cojinetes sometidos a cargas extremas.",
            "Z-ROD incluye inhibidores especiales contra el óxido para proteger motores durante almacenamientos prolongados.",
            "DOMINATOR soporta altas RPM, temperaturas extremas y dilución por combustible en pista."
        ],
        "specs": "Formulaciones de alto Zinc (ZDDP) para competencia, Hot-Rods, Muscle Cars y motores modificados.",
        "service_life": "Según régimen de competencia o hasta 5,000 millas / 1 año en vehículos clásicos (Z-ROD)."
    },
    "high-mileage": {
        "line_name": "Serie Alto Millaje (High-Mileage) 100% Sintético",
        "summary": "Diseñado específicamente para motores con más de 75,000 millas (120,000 km). Revitaliza sellos, reduce el consumo de aceite y limpia depósitos acumulados.",
        "benefits": [
            "Acondicionadores de sellos que restauran la elasticidad de retenedores y empaques para detener y prevenir fugas.",
            "Película lubricante reforzada y baja volatilidad para disminuir la quema de aceite.",
            "Detergencia activa que disuelve barnices y lodos acumulados con los años."
        ],
        "specs": "API SP (Resource Conserving), ILSAC GF-6A, GM dexos1 Gen 3, Chrysler MS-6395, Ford",
        "service_life": "Hasta 12,000 millas (19,300 km) o 1 año."
    },
    "heavy-duty-ck4": {
        "line_name": "Serie Heavy-Duty Diésel CK-4 100% Sintético",
        "summary": "Protección 100% sintética para motores diésel de servicio pesado de carretera y fuera de carretera. Proporciona hasta 4 veces más protección contra el desgaste que lo requerido por la norma Detroit Diesel DD13.",
        "benefits": [
            "4X más protección contra el desgaste que el estándar Detroit Diesel DD13 Scuffing Test.",
            "Bajo consumo de aceite (hasta 66% menos volatilidad que lo exigido por API CK-4).",
            "Totalmente compatible con sistemas de postratamiento de gases (DPF, EGR, SCR).",
            "Excelente control del hollín y estabilidad al cizallamiento."
        ],
        "specs": "API CK-4 / SN, ACEA E9, Cummins CES 20086, Detroit Diesel DFS 93K222, Mack EOS-4.5, Volvo VDS-4.5, Caterpillar ECF-3, Renault RLD-3",
        "service_life": "Intervalos extendidos según guía de servicio pesado AMSOIL o recomendaciones OEM."
    },
    "commercial-synthetic-blend": {
        "line_name": "Serie Commercial Synthetic-Blend Diésel CK-4",
        "summary": "Mezcla sintética de grado comercial con más de 50% de contenido sintético, diseñada para flotas diésel y maquinaria pesada que buscan superar el rendimiento de los aceites minerales convencionales optimizando costos operativos.",
        "benefits": [
            "Contiene más de 50% de aceites base sintéticos (muy superior a mezclas convencionales del mercado).",
            "Supera en más de 2X la protección contra desgaste del ensayo Detroit Diesel DD13.",
            "Protege filtros de partículas diésel (DPF) y reduce el consumo de aceite en flotas."
        ],
        "specs": "API CK-4 / SN, Cummins CES 20086, Detroit Diesel DFS 93K222, Volvo VDS-4.5, Mack EOS-4.5, Caterpillar ECF-3",
        "service_life": "Intervalos recomendados por el fabricante del motor (OEM)."
    },
    "diesel-dexos-d": {
        "line_name": "Serie Diésel Ligero 100% Sintético (GM dexosD)",
        "summary": "Aceite 100% sintético de baja viscosidad desarrollado para motores turbodiésel modernos de camionetas y SUVs ligeras (como motores GM Duramax 3.0L LM2 / LZ0 y 2.8L) que exigen la especificación GM dexosD.",
        "benefits": [
            "Cumple los exigentes requisitos de la especificación GM dexosD para diésel ligero.",
            "Fórmula de bajas cenizas (Mid/Low SAPS) que prolonga la vida útil del filtro DPF y catalizadores SCR.",
            "Flujo inmediato en frío y resistencia superior a la oxidación en turbos de geometría variable."
        ],
        "specs": "GM dexosD, ACEA C2 / C3",
        "service_life": "Intervalos indicados por el sistema de monitoreo de vida del aceite o manual OEM."
    },
    "signature-series-max-duty": {
        "line_name": "Serie Signature Max-Duty Diésel 100% Sintético",
        "summary": "La máxima tecnología de AMSOIL en lubricación diésel de servicio pesado. Ofrece 6 veces más protección contra el desgaste del motor que el estándar Detroit Diesel DD13.",
        "benefits": [
            "6X más protección contra el desgaste que el estándar Detroit Diesel DD13 Scuffing Test.",
            "Hasta 76% menos consumo de aceite que lo permitido por la norma API CK-4.",
            "60% mejor limpieza de turbocargadores y control superior de espesamiento por hollín.",
            "Permite intervalos de drenaje extendidos hasta 3X los recomendados por el OEM con análisis de aceite."
        ],
        "specs": "API CK-4 / CJ-4 / CI-4+ / SN, ACEA E9/E7, Cummins CES 20086, Detroit Diesel DFS 93K222, Mack EOS-4.5, Volvo VDS-4.5, Caterpillar ECF-3, MB 228.31, MTU Type 2.1",
        "service_life": "Hasta 3X el intervalo OEM (hasta 60,000 millas / 600 horas) en motores diésel de servicio pesado."
    },
    "severe-gear-y-diferenciales": {
        "line_name": "Lubricantes Sintéticos para Diferenciales y Transmisiones Manuales",
        "summary": "Aceites 100% sintéticos de extrema presión (GL-5 y GL-4) diseñados para diferenciales hipoidales, ejes de arrastre pesado, vehículos 4x4, todoterreno y cajas de transmisión manual o sincronizadas.",
        "benefits": [
            "SEVERE GEAR mantiene su viscosidad sin cizallarse (20% más protección en película fría y caliente que la competencia).",
            "Previene la ruptura térmica y el desgaste por picadura (pitting) en coronas y piñones bajo remolque extremo.",
            "Compatible con la mayoría de diferenciales de deslizamiento limitado (Limited-Slip).",
            "Disponible en práctico envase flexible Easy-Pack para cambios rápidos y limpios en lugares de difícil acceso."
        ],
        "specs": "API GL-5 / MT-1 (Severe Gear & Long Life), API GL-4 (Manual Transaxle 75W-90), Synchromesh (GM / Honda / Chrysler)",
        "service_life": "Hasta 100,000 millas en servicio normal o 50,000 millas en servicio severo/remolque."
    },
    "transmision-automatica-atf-cvt-dct": {
        "line_name": "Fluidos 100% Sintéticos para Transmisión Automática (ATF, CVT, DCT)",
        "summary": "Gama completa de fluidos 100% sintéticos para cajas automáticas modernas de múltiples velocidades (6, 8, 9 y 10 cambios), transmisiones continuamente variables (CVT), doble embrague (DCT) y transmisiones de servicio pesado (Torque-Drive).",
        "benefits": [
            "Excepcional resistencia al calor extremo y a la formación de barniz en cuerpos de válvulas y solenoides.",
            "Cambios suaves y precisos sin vibración (shudder) del convertidor de par.",
            "Versiones Multi-Vehicle (Red), Fuel-Efficient de baja viscosidad (Blue), Ultra-Low Viscosity (ULV) y Heavy-Duty (Allison TES-295 / C-4)."
        ],
        "specs": "GM DEXRON III / VI / ULV, Ford MERCON V / LV / ULV, Toyota WS, Honda DW-1 / HCF-2, Nissan Matic / NS-2 / NS-3, Allison C-4 / TES-295, ZF, DSG/DCT",
        "service_life": "Hasta 100,000 millas en servicio normal o 50,000 millas en servicio severo (Signature Series ATF)."
    },
    "fluidos-frenos-direccion-varios": {
        "line_name": "Fluidos de Frenos, Dirección Hidráulica, Compresores y Especialidades",
        "summary": "Fluidos sintéticos de alto punto de ebullición para sistemas de frenos (DOT 3/4 y Racing DOT 4), dirección hidráulica multi-vehículo, aceite de asentamiento de motores (Break-In), compresores (ISO 68), ensamblaje de motores y limpieza interna (Flush).",
        "benefits": [
            "Líquidos de frenos con altísimo punto de ebullición en seco y húmedo para evitar el pedal esponjoso (brake fade).",
            "SABER Professional 2-Stroke elimina el humo y estabiliza el combustible a cualquier proporción (hasta 100:1).",
            "Engine & Transmission Flush disuelve lodos de forma segura en 15 minutos antes del cambio de aceite."
        ],
        "specs": "FMVSS 116 DOT 3 / DOT 4, ISO VG 68 (Compresores), JASO FD / ISO-L-EGD (SABER 2T)",
        "service_life": "Según aplicación y programa de mantenimiento preventivo."
    },
    "aditivos-combustible": {
        "line_name": "Aditivos Sintéticos de Combustible (Diésel y Gasolina)",
        "summary": "Tratamientos concentrados de grado profesional para limpiar inyectores, cámaras de combustión y válvulas, lubricar la parte superior del cilindro y elevar el índice de octano o cetano.",
        "benefits": [
            "P.i. Performance Improver restaura hasta el 14% de la potencia y limpia inyectores GDI y de puerto en un solo tanque.",
            "Diesel Injector Clean + Cetane Boost limpia inyectores diésel, lubrica bombas de alta presión y eleva el cetano hasta en 8 puntos.",
            "Upper Cylinder Lubricant reduce en 18% el desgaste de anillos y cilindros en cada tanqueada.",
            "DOMINATOR Octane Boost eleva el octanaje hasta en 4 números para eliminar el cascabeleo (knock)."
        ],
        "specs": "Seguros para convertidores catalíticos, sensores de oxígeno, turbos y filtros de partículas diésel (DPF).",
        "service_life": "Uso continuo en cada tanqueada o tratamiento periódico cada 4,000 millas."
    },
    "grasas-y-lubricantes": {
        "line_name": "Grasas 100% Sintéticas de Complejo de Litio y Lubricantes de Cadena",
        "summary": "Grasas sintéticas de alta adherencia y resistencia al lavado por agua para equipo pesado, minería, construcción, agricultura (Polymeric Off-Road NLGI #2), rodamientos automotrices e industriales (Multi-Purpose NLGI #2) y cadenas.",
        "benefits": [
            "Excelente resistencia al impacto (carga Timken OK y soldadura de 4 bolas) en pines, bocinas y quintas ruedas.",
            "Polímeros sintéticos que se adhieren al metal y rechazan el agua, barro y contaminantes.",
            "Chain Lube penetra en eslabones y O-rings sin salpicar (no fling-off) ni atraer polvo."
        ],
        "specs": "NLGI #2, Complejo de Litio Sintético, Extrema Presión (EP).",
        "service_life": "Intervalos de engrase extendidos en equipo pesado y automotriz."
    },
    "coolant-anticongelante": {
        "line_name": "Anticongelantes / Coolants de Larga Duración y Mejoradores Térmicos",
        "summary": "Refrigerantes pre-diluidos 50/50 de ácidos orgánicos híbridos (HOAT) libres de fosfatos, boratos y aminas para vehículos livianos, equipo pesado diésel y motocicletas/ATV, además del aditivo reductor de temperatura DOMINATOR Coolant Boost.",
        "benefits": [
            "Protección superior contra la cavitación de camisas húmedas, corrosión galvánica y formación de incrustaciones.",
            "Compatible con todos los colores y tipos de anticongelantes etilenglicol y propilenglicol.",
            "DOMINATOR Coolant Boost reduce la temperatura del motor hasta en 25 °F (14 °C) y acelera el calentamiento."
        ],
        "specs": "ASTM D3306, D4985, D6210, Cummins, Caterpillar EC-1, Detroit Diesel, Mack, Paccar, OEM Automotriz",
        "service_life": "Hasta 150,000 millas (5 años) en autos livianos y hasta 1,000,000 de millas (8 años) en servicio pesado."
    },
    "4t-motorcycle": {
        "line_name": "Serie 4T Performance para Motocicletas y Suspensión",
        "summary": "Aceite 100% sintético diseñado para motocicletas de 4 tiempos enfriadas por aire o líquido con motor, caja de cambios y embrague húmedo integrados, junto con el fluido sintético de suspensión Shock Therapy.",
        "benefits": [
            "Fricción optimizada sin modificadores resbaladizos para un acople firme del embrague húmedo (JASO MA2).",
            "Alta estabilidad al cizallamiento en los engranajes de la transmisión.",
            "Shock Therapy controla la fricción y evita la aireación/espuma en horquillas y amortiguadores."
        ],
        "specs": "API SN / SM, JASO MA / MA2",
        "service_life": "Hasta 2X el intervalo recomendado por el fabricante de la motocicleta."
    },
    "v-twin": {
        "line_name": "Serie V-Twin 100% Sintética (Harley-Davidson y Custom)",
        "summary": "Lubricantes 100% sintéticos formulados específicamente para soportar el calor extremo de los motores V-Twin enfriados por aire (Harley-Davidson, Indian, etc.), así como fluidos dedicados para caja primaria (Primary) y transmisión.",
        "benefits": [
            "Resiste la degradación por calor extremo en el cilindro trasero de motores V-Twin.",
            "Puede utilizarse en los 3 compartimentos (Motor, Transmisión y Primaria) o combinarse con los fluidos específicos V-Twin Primary y V-Twin Transmission.",
            "Elimina el patinamiento del embrague y facilita encontrar el neutro con cambios más silenciosos."
        ],
        "specs": "API SG / SL / CF / CG-4, JASO MA / MA2 (Seguro para embragues húmedos)",
        "service_life": "Hasta 2X el intervalo recomendado por el fabricante o 1 año."
    },
    "2-stroke": {
        "line_name": "Serie 2-Tiempos 100% Sintética (INTERCEPTOR y DOMINATOR)",
        "summary": "Aceites 100% sintéticos de combustión limpia para motores de 2 tiempos de alto desempeño, motocross, enduro, karts, motos de agua y nieve, tanto en sistemas de inyección como en pre-mezcla.",
        "benefits": [
            "INTERCEPTOR evita que las válvulas de escape (power valves / RAVE) se peguen por carbón.",
            "DOMINATOR 2T entrega una película lubricante reforzada para motores de carreras modificados y altas RPM.",
            "Combustión limpia con mínima emisión de humo."
        ],
        "specs": "API TC, JASO FD, ISO-L-EGD",
        "service_life": "Inyección directa/variable o pre-mezcla (típicamente 50:1)."
    },
    "atv-utv": {
        "line_name": "Serie ATV/UTV 100% Sintética (Motor, DCT y Transmisión/Diferencial)",
        "summary": "Desarrollada y probada en terrenos severos para cuadriciclos (ATV) y vehículos utilitarios Side-by-Side (UTV) como Polaris, Can-Am, Honda, Yamaha, Kawasaki y CFMoto.",
        "benefits": [
            "Protección comprobada bajo cargas de arrastre, barro profundo y bajas velocidades con alta temperatura.",
            "Fórmula segura para embragues húmedos (JASO MA2).",
            "Fluidos específicos para diferenciales, cajas de demanda y transmisiones de doble embrague (DCT) de ATV/UTV."
        ],
        "specs": "API SG / SJ / SL / CF, JASO MA / MA2",
        "service_life": "Intervalos extendidos en servicio todoterreno severo."
    },
    "dirt-bike": {
        "line_name": "Serie Dirt Bike 100% Sintética (Motocross y Enduro)",
        "summary": "Formulado para brindar sensación consistente en la maneta del embrague y máxima protección contra el desgaste de pistones y engranajes en motos de motocross y enduro de 4 y 2 tiempos.",
        "benefits": [
            "Acción consistente del embrague en arrancadas (holeshot) y secciones técnicas.",
            "Sufre mínimo cizallamiento en la caja de cambios bajo impactos repetitivos.",
            "Para Honda, Yamaha, KTM, Husqvarna, GasGas, Kawasaki y Suzuki."
        ],
        "specs": "JASO MA, API SG / SJ / SH / SL",
        "service_life": "Según horas de competencia o entrenamiento."
    },
    "metric-motorcycle": {
        "line_name": "Serie Metric Motorcycle 100% Sintética (Deportivas, Naked y Adventure)",
        "summary": "Diseñado para motocicletas métricas de altas RPM (Honda, Yamaha, Kawasaki, Suzuki, BMW, Triumph, Ducati, KTM) que exigen máxima protección contra el desgaste de caja y motor.",
        "benefits": [
            "Mantiene su viscosidad protectora a altas revoluciones y temperaturas.",
            "Cambios de marcha suaves y máxima vida útil de los discos del embrague (JASO MA2).",
            "Protección superior contra la herrumbre durante periodos de inactividad."
        ],
        "specs": "API SM / SG / SL / CF, JASO MA / MA2",
        "service_life": "Hasta 2X el intervalo recomendado por el fabricante o 1 año."
    },
    "marino": {
        "line_name": "Serie Marina 100% Sintética (HP Marine 2-Stroke)",
        "summary": "Aceite marino 100% sintético diseñado para motores fuera de borda de 2 tiempos, incluyendo motores modernos de inyección directa (DFI como Evinrude E-TEC, Mercury Optimax y Yamaha HPDI) y pre-mezcla.",
        "benefits": [
            "Tecnología de aditivos MAXDOSE que previene depósitos en anillos (ring jacking) y bujías.",
            "Baja toxicidad acuática y mínima emisión de humo.",
            "Excelente fluidez para sistemas de inyección de aceite y pre-mezcla 50:1."
        ],
        "specs": "NMMA TC-W3, API TC",
        "service_life": "Inyección directa (DFI), inyección electrónica (EFI) o pre-mezcla 50:1."
    }
}

# Order priority for presentation selector buttons
def presentation_sort_key(img):
    fn = img["filename"]
    order = [
        "cuarto-1qt-",
        "easy-pack-1qt-",
        "botella-4oz-",
        "tubo-4oz-",
        "botella-8oz-",
        "botella-12oz-",
        "botella-16oz-",
        "botella-cn-",
        "lata-spray-",
        "cartucho-tubo-",
        "medio-galon-",
        "galon-1gal-",
        "garrafa-2.5gal-",
        "cubeta-5gal-",
        "cubeta-35lb-",
        "barril-16gal-",
        "estanon-30gal-",
        "estanon-55gal-",
        "cunete-120lb-",
        "tote-275gal-",
        "envase-principal-",
        "catalogo-latam-",
        "vista-general-",
        "recorte-fondo-transparente-",
    ]
    for i, prefix in enumerate(order):
        if fn.startswith(prefix):
            return (i, fn)
    return (99, fn)

def short_pres_badge(img):
    fn = img["filename"]
    if fn.startswith("cuarto-1qt-"):
        return "1 Cuarto (946 mL)"
    if fn.startswith("easy-pack-1qt-"):
        return "Easy-Pack 1 Qt"
    if fn.startswith("galon-1gal-"):
        return "1 Galón (3.78 L)"
    if fn.startswith("garrafa-2.5gal-"):
        return "Garrafa 2.5 Gal"
    if fn.startswith("cubeta-5gal-"):
        return "Cubeta 5 Gal"
    if fn.startswith("barril-16gal-"):
        return "Barril 16 Gal"
    if fn.startswith("estanon-30gal-"):
        return "Estañón 30 Gal"
    if fn.startswith("estanon-55gal-"):
        return "Estañón 55 Gal"
    if fn.startswith("tote-275gal-"):
        return "Tote 275 Gal"
    if fn.startswith("cartucho-tubo-"):
        return "Cartucho 14 oz"
    if fn.startswith("cubeta-35lb-"):
        return "Cubeta 35 lbs"
    if fn.startswith("cunete-120lb-"):
        return "Cuñete 120 lbs"
    if fn.startswith("botella-8oz-"):
        return "Botella 8 oz"
    if fn.startswith("botella-12oz-"):
        return "Botella 12 oz"
    if fn.startswith("botella-16oz-"):
        return "Botella 16 oz"
    if fn.startswith("medio-galon-"):
        return "Medio Galón (64 oz)"
    if fn.startswith("botella-4oz-"):
        return "Botella 4 oz"
    if fn.startswith("tubo-4oz-"):
        return "Tubo 4 oz"
    if fn.startswith("botella-cn-"):
        return "Envase Individual"
    if fn.startswith("lata-spray"):
        return "Spray Aerosol"
    if fn.startswith("vista-general-"):
        return "Familia / Presentaciones"
    if fn.startswith("recorte-fondo-transparente-"):
        return "Vista Recorte PNG/WebP"
    if fn.startswith("envase-principal-"):
        return "Envase Estándar"
    if fn.startswith("catalogo-latam-"):
        return f"Vista Catálogo ({img['sku']})"
    return img["sku"]

def extract_viscosity_tag(item_slug, display_name):
    m = re.search(r"\b(\d+W-\d+|SAE\s*\d+|ISO\s*\d+|DOT\s*3\s*&\s*4|DOT\s*4|NLGI\s*#\d+|50/50)\b", display_name, re.I)
    if m:
        return m.group(1).upper()
    if "2-stroke" in item_slug or "2-Stroke" in display_name:
        return "2-Tiempos"
    if "atf" in item_slug or "ATF" in display_name:
        return "ATF"
    if "cvt" in item_slug:
        return "CVT"
    if "dct" in item_slug:
        return "DCT"
    return "Especialidad"

enriched = []
for p in raw_catalog:
    cat_meta = CATEGORY_META.get(p["category"], {"name": p["category"], "short": p["category"], "icon": "🛢️"})
    line_meta = LINE_TECH_INFO.get(p["line"], {
        "line_name": p["line"],
        "summary": "Lubricante 100% sintético de alto rendimiento AMSOIL.",
        "benefits": ["Protección sintética avanzada contra desgaste y temperatura."],
        "specs": "Estándares OEM e industriales.",
        "service_life": "Según recomendación técnica."
    })

    # Sort images cleanly so primary container (Quart/Gallon/Bottle) comes first
    sorted_imgs = sorted(p["images"], key=presentation_sort_key)
    for img in sorted_imgs:
        img["short_label"] = short_pres_badge(img)
        img["is_container"] = not (
            img["filename"].startswith("recorte-fondo-transparente-") or
            img["filename"].startswith("vista-general-") or
            img["filename"].startswith("catalogo-latam-")
        )

    # Map ALS codes to their presentation names
    als_details = []
    for code in p["als_codes"]:
        pres_name, desc_pdf = ALS_SKU_INFO.get(code, ("Presentación Estándar", p["display_name"]))
        als_details.append({
            "code": code,
            "presentation": pres_name,
            "description_pdf": desc_pdf
        })

    visc_tag = extract_viscosity_tag(p["item_slug"], p["display_name"])

    enriched.append({
        "index": p["index"],
        "id": f"{p['amsoil_code'].lower()}-{p['item_slug']}",
        "category": p["category"],
        "category_name": cat_meta["name"],
        "category_short": cat_meta["short"],
        "category_icon": cat_meta["icon"],
        "line": p["line"],
        "line_name": line_meta["line_name"],
        "item_slug": p["item_slug"],
        "display_name": p["display_name"],
        "viscosity": visc_tag,
        "amsoil_code": p["amsoil_code"],
        "als_codes": p["als_codes"],
        "als_presentations": als_details,
        "folder": p["folder"],
        "tech_sheet": {
            "summary": line_meta["summary"],
            "benefits": line_meta["benefits"],
            "specs": line_meta["specs"],
            "service_life": line_meta["service_life"],
        },
        "available_packages_official": p.get("available_packages_official", []),
        "images": sorted_imgs
    })

with open(os.path.join(OUT_DIR, "catalogo-imagenes.json"), "w", encoding="utf-8") as f:
    json.dump(enriched, f, ensure_ascii=False, indent=2)

with open(os.path.join(OUT_DIR, "catalogo-datos.js"), "w", encoding="utf-8") as f:
    f.write("window.AMSOIL_CATALOG = ")
    json.dump(enriched, f, ensure_ascii=False, indent=2)
    f.write(";\n")

print(f"Enriched {len(enriched)} products and generated catalogo-datos.js!")
