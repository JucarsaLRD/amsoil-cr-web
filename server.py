import re
import os
import sys
import json
import urllib.request
import urllib.error
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8088
API_KEY = os.environ.get("GEMINI_API_KEY", "")
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Cargar catálogo y lista de precios oficial AMSOIL Costa Rica
AMSOIL_CATALOG = {}
price_file = os.path.join(CURRENT_DIR, "amsoil_price_list_cr.json")
if os.path.exists(price_file):
    try:
        with open(price_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            for p in data.get("products", []):
                AMSOIL_CATALOG[p.get("code")] = p
        print(f"[ALS Server] Cargados {len(AMSOIL_CATALOG)} productos de la lista de precios oficial de ALS.")
    except Exception as e:
        print(f"[ALS Server] Error cargando lista de precios: {e}")

GEMINI_PROMPT_TEMPLATE = """
Eres el Ingeniero de Lubricación Principal y Asesor Técnico de American Lubricants Supply S.A. (ALS) en Costa Rica.
El usuario o vendedor consulta la recomendación técnica para el siguiente vehículo, motor, maquinaria pesada o VIN:
"{query}"

Analiza las especificaciones técnicas OEM del fabricante.
IMPORTANTE:
1. Identifica el TIPO DE COMBUSTIBLE exacto:
   - "gasolina", "hibrido", "diesel" o "maquinaria_diesel".
   - Si es Toyota Prius, Corolla Hybrid, etc., es HÍBRIDO A GASOLINA (HEV/PHEV). NUNCA recomendar aditivos ni fluidos para diésel (como Cetane Boost) en vehículos de gasolina o híbridos.
2. Identifica la CATEGORÍA DE VEHÍCULO:
   - "turismo_gasolina": Carros, sedanes, SUVs de gasolina (ej: Range Rover Gasolina, RAV4, Corolla, Civic).
   - "turismo_hibrido": Vehículos híbridos (ej: Prius, Niro, RAV4 Hybrid).
   - "turismo_diesel": SUVs, pickups o carros diésel ligero (ej: Defender 2.2 TDCi, Hilux, Prado, D-Max).
   - "pesado_flota": Cabezales, camiones pesados y autobuses (Freightliner, Mack, Kenworth, Isuzu Forward).
   - "maquinaria": Equipo de construcción o agro (CAT, Komatsu, John Deere).
3. Para la categoría de vehículo seleccionada, NUNCA muestres opciones que pertenezcan a otro segmento:
   - Para un Range Rover o Prius, NO mostrar opciones de "Flotas" o "Servicio Pesado Diesel 15W-40 CK-4".
   - Para carros de gasolina/híbridos, las opciones deben ser Signature Series, Hybrid Series, XL Series o OE Synthetic.
   - Para equipo pesado o camiones, las opciones deben ser Max-Duty CK-4, Heavy-Duty CK-4 o Commercial Blend.
4. Identifica:
   - Capacidad exacta del cárter en litros con filtro.
   - Viscosidad oficial requerida (0W-16, 0W-20, 5W-20, 5W-30, 0W-30, 5W-40, 15W-40, 10W-30).
   - Norma oficial OEM (Ford WSS-M2C934-B, ACEA C1/C2/C3, API SP/GF-6A, Dexos1 Gen3, JASO DH-2, CAT ECF-3, etc.).
   - Código OEM de filtro de aceite y equivalencias (Mann, Baldwin, Donaldson).
   - Alerta Técnica Crítica de Alto Valor Consultivo para el vendedor (detalles del DPF, inyección GDI/LSPI, turbo, etc.).

Responde ÚNICAMENTE un JSON estricto con la siguiente estructura:
{{
  "vehicleCategory": "turismo_gasolina | turismo_hibrido | turismo_diesel | pesado_flota | maquinaria",
  "fuelType": "gasolina | hibrido | diesel",
  "title": "Nombre completo con año y motor (ej: Toyota Prius 2026 2.0L Híbrido PHEV)",
  "subtitle": "Configuración técnica y sistema de emisiones (ej: Motor Ciclo Atkinson M20A-FXS + Sistema Híbrido)",
  "capacity": "Capacidad en litros y cuartos (ej: 4.2 Litros (4.4 Qt))",
  "sumpLiters": 4.2,
  "viscosity": "0W-16 (o 0W-20)",
  "norm": "API SP / ILSAC GF-6B",
  "interval": "10.000 km o 12 meses",
  "filter": "04152-YZZA6 / Mann HU 6006 z",
  "warning": "Alerta técnica crítica para el vendedor sobre requerimientos de este motor",
  "amsoilTiers": {{
    "p1": {{
      "badge": "Línea Insignia (Signature / Hybrid)",
      "title": "Nombre producto AMSOIL nivel 1",
      "code": "Código AMSOIL",
      "interval": "Garantía de kilometraje o tiempo (ej: Hasta 25.000 km o 1 año)",
      "drum": 1050000,
      "gal": 132000,
      "quart": 9500,
      "rationale": "Justificación técnica orientada a este vehículo específico"
    }},
    "p2": {{
      "badge": "Línea Extendida (XL / Protección Especial)",
      "title": "Nombre producto AMSOIL nivel 2",
      "code": "Código AMSOIL",
      "interval": "Hasta 15.000 km",
      "drum": 920000,
      "gal": 115000,
      "quart": 7720,
      "rationale": "Justificación técnica"
    }},
    "p3": {{
      "badge": "Línea OE (Reemplazo Directo de Fábrica)",
      "title": "Nombre producto AMSOIL nivel 3 (OE Series)",
      "code": "Código AMSOIL",
      "interval": "Intervalo recomendado de fábrica OEM (10.000 km)",
      "drum": 806200,
      "gal": 93120,
      "quart": 6580,
      "rationale": "Justificación técnica"
    }}
  }},
  "otherBrands": {{
    "castrol": {{
      "product": "Producto Castrol equivalente exacto",
      "spec": "Norma y viscosidad Castrol",
      "drum": 560000,
      "pail": 58000,
      "gal": 14500,
      "trans": "Fluido de transmisión Castrol",
      "gear": "Aceite engranajes",
      "grease": "Grasa"
    }},
    "shell": {{
      "product": "Producto Shell equivalente exacto",
      "spec": "Norma y viscosidad Shell",
      "drum": 540000,
      "pail": 56000,
      "gal": 14000,
      "trans": "Fluido transmisión Shell",
      "gear": "Aceite engranajes",
      "grease": "Grasa"
    }},
    "chevron": {{
      "product": "Producto Chevron equivalente exacto",
      "spec": "Norma y viscosidad Chevron",
      "drum": 545000,
      "pail": 56500,
      "gal": 14200,
      "trans": "Fluido transmisión Chevron",
      "gear": "Aceite engranajes",
      "grease": "Grasa"
    }},
    "cam2": {{
      "product": "Producto CAM2 equivalente exacto",
      "spec": "Norma y viscosidad CAM2",
      "drum": 490000,
      "pail": 51000,
      "gal": 12500,
      "trans": "Fluido transmisión CAM2",
      "gear": "Aceite engranajes",
      "grease": "Grasa"
    }},
    "maxoil": {{
      "product": "Producto Max Oil equivalente exacto",
      "spec": "Norma y viscosidad Max Oil",
      "drum": 480000,
      "pail": 50000,
      "gal": 12200,
      "trans": "Fluido transmisión Max Oil",
      "gear": "Aceite engranajes",
      "grease": "Grasa"
    }},
    "pennzoil": {{
      "product": "Producto Pennzoil equivalente exacto",
      "spec": "Norma y viscosidad Pennzoil",
      "drum": 550000,
      "pail": 57000,
      "gal": 14200,
      "trans": "Fluido transmisión Pennzoil",
      "gear": "Aceite engranajes",
      "grease": "Grasa"
    }}
  }}
}}
"""

def sanitize_and_enrich_specs(data: dict, query: str, mileage: int = None) -> dict:
    """Valida y enriquece la respuesta para garantizar coherencia automotriz absoluta y el paquete completo de fluidos."""
    q_lower = query.lower()
    
    # 1. Detección estricta de combustible y categoría
    # Detección de kilometraje si no vino explícito
    if mileage is None:
        import re
        m_match = re.search(r'(\d+[\d,\.]*)\s*(?:km|kms|kilómetros|kilometros|k\b)', query, re.IGNORECASE)
        if m_match:
            try:
                m_str = m_match.group(1).replace(',', '').replace('.', '')
                mileage = int(m_str)
            except Exception:
                pass

    data["reportedMileage"] = mileage
    is_high_mileage = (mileage is not None and mileage >= 100000)
    data["isHighMileage"] = is_high_mileage

    if is_high_mileage:
        data["mileageAdvice"] = f"Unidad con alto kilometraje acumulado ({mileage:,} km). Se recomienda la formulación AMSOIL High-Mileage con acondicionadores de sellos y retenes para rejuvenecer empaquetaduras y evitar fugas o consumo de aceite."
    elif mileage is not None and mileage > 0:
        data["mileageAdvice"] = f"Kilometraje estándar ({mileage:,} km). El motor conserva tolerancias de fábrica; aplicar formulación estándar Signature Series u OE."
    else:
        data["mileageAdvice"] = None

    is_hybrid = "hibrid" in q_lower or "hybrid" in q_lower or "prius" in q_lower or "niro" in q_lower or "ioniq" in q_lower or data.get("fuelType") == "hibrido"
    is_diesel = ("diesel" in q_lower or "diésel" in q_lower or "tdci" in q_lower or "d4d" in q_lower or "crdi" in q_lower or "dd15" in q_lower or "ck-4" in q_lower or "cummins" in q_lower) and not is_hybrid
    is_heavy = any(k in q_lower for k in ["camion", "truck", "cabezal", "freightliner", "kenworth", "mack", "cat", "caterpillar", "excavadora", "320d", "cascadia", "volvo fh"])
    
    if is_hybrid:
        data["fuelType"] = "hibrido"
        data["vehicleCategory"] = "turismo_hibrido"
    elif is_heavy:
        data["fuelType"] = "diesel"
        data["vehicleCategory"] = "pesado_flota" if "excavadora" not in q_lower and "cat" not in q_lower else "maquinaria"
    elif is_diesel:
        data["fuelType"] = "diesel"
        data["vehicleCategory"] = "turismo_diesel"
    else:
        data["fuelType"] = "gasolina"
        data["vehicleCategory"] = "turismo_gasolina"

    category = data["vehicleCategory"]
    fuel = data["fuelType"]

    # 2. Asegurar que las 3 opciones de AMSOIL coincidan EXACTAMENTE con el vehículo
    tiers = data.setdefault("amsoilTiers", {})
    
    if category == "turismo_hibrido":
        tiers["p1"] = {
            "badge": "Recomendado Especial Híbrido",
            "title": "AMSOIL 100% Synthetic 0W-16 Hybrid SP",
            "code": "AMH27012 (Cuartos)",
            "interval": "Hasta 20.000 km o 1 año",
            "drum": 806200,
            "gal": 93120,
            "quart": 6598,
            "rationale": "Formulación exclusiva para motores híbridos con arranques y paradas continuas del motor térmico. Previene acumulación de humedad y barnices."
        }
        tiers["p2"] = {
            "badge": "Línea Insignia Extendido",
            "title": "AMSOIL 100% Synthetic Signature Series 0W-20",
            "code": "AMS2812 (Cuartos)",
            "interval": "Hasta 25.000 km o 1 año",
            "drum": 1218000,
            "gal": 136880,
            "quart": 9501,
            "rationale": "El aceite sintético insignia de AMSOIL con máxima retención de viscosidad y 75% más protección contra pérdidas de potencia."
        }
        tiers["p3"] = {
            "badge": "Línea OE Fábrica",
            "title": "AMSOIL 100% Synthetic OE 0W-16 SP",
            "code": "AM28012 (Cuartos)",
            "interval": "Intervalo recomendado por fabricante (10.000 km)",
            "drum": 806200,
            "gal": 93120,
            "quart": 6588,
            "rationale": "Protección sintética avanzada para mantener la garantía de fábrica con costo optimizado."
        }
    elif category == "turismo_gasolina":
        # Por ejemplo Range Rover Gasolina, SUV, Sedán
        visc = data.get("viscosity", "5W-30")
        is_0w20 = "0w-20" in visc.lower() or "0w20" in visc.lower()
        code_sig = "AMS2812" if is_0w20 else "AMS8612"
        code_oe = "AM28012" if is_0w20 else "AM86012"
        
        if is_high_mileage:
            tiers["p1"] = {
                "badge": "🛡️ Recomendado Alto Kilometraje (>100.000 km)",
                "title": f"AMSOIL High-Mileage 100% Synthetic {visc}",
                "code": f"HM{visc.replace('-', '').replace('W', '')}12 (Cuartos)",
                "interval": "Hasta 20.000 km o 1 año",
                "drum": 945000,
                "gal": 115000,
                "quart": 7850,
                "rationale": f"Formulado específicamente para unidades con más de 100.000 km ({mileage:,} km reportados). Incorpora acondicionadores de sellos y elastómeros que rejuvenecen retenes resecos de cigüeñal y guías de válvula, reduciendo fugas y consumo de aceite."
            }
            tiers["p2"] = {
                "badge": "Línea Insignia Extendido",
                "title": f"AMSOIL Signature Series {visc} Synthetic",
                "code": f"{code_sig} (Cuartos) / Galón",
                "interval": "Hasta 25.000 km o 1 año",
                "drum": 1218000,
                "gal": 136880,
                "quart": 9501,
                "rationale": "Máxima protección sintética con reserva alcalina TBN para neutralizar ácidos de combustión."
            }
        else:
            tiers["p1"] = {
                "badge": "Línea Insignia (Máximo Rendimiento)",
                "title": f"AMSOIL Signature Series {visc} Synthetic",
                "code": f"{code_sig} (Cuartos) / Galón",
                "interval": "Hasta 25.000 km o 1 año",
                "drum": 1218000,
                "gal": 136880,
                "quart": 9501,
                "rationale": "Protección insuperable para motores modernos multiválvulas y turbocargados con inyección directa (TGDI). Previene preignición a baja velocidad (LSPI)."
            }
        tiers["p2"] = {
            "badge": "Línea XL Extended Life",
            "title": f"AMSOIL XL Extended Life {visc} Synthetic",
            "code": "AMX8612 (Cuartos)",
            "interval": "Hasta 15.000 km o 1 año",
            "drum": 926800,
            "gal": 110000,
            "quart": 7723,
            "rationale": "Formulado para brindar 100% de protección sintética con extensión moderada de cambio."
        }
        tiers["p3"] = {
            "badge": "Línea OE (Reemplazo Oficial)",
            "title": f"AMSOIL OE Synthetic {visc} SP",
            "code": f"{code_oe} (Cuartos) / Galón / Estañón",
            "interval": "Intervalo de manual OEM (10.000 km)",
            "drum": 806200,
            "gal": 93120,
            "quart": 6431,
            "rationale": "Cumple y excede la especificación del fabricante manteniendo el programa de mantenimiento oficial."
        }
    elif category == "turismo_diesel":
        # Pickups y SUVs Diésel (Hilux, Defender, Prado, D-Max)
        is_low_saps = "c1" in data.get("norm", "").lower() or "c2" in data.get("norm", "").lower() or "c3" in data.get("norm", "").lower() or "dpf" in data.get("subtitle", "").lower()
        if is_low_saps:
            tiers["p1"] = {
                "badge": "Especializado Europeo Low-SAPS (DPF)",
                "title": "AMSOIL European Car Formula 5W-30 LS",
                "code": "AML86055 (Estañón) / AML8612 (Cuartos)",
                "interval": "Hasta 20.000 km o 1 año",
                "drum": 1015000,
                "gal": 127560,
                "quart": 8858,
                "rationale": "Formulación Low-SAPS mandatoria para vehículos diésel con Filtro de Partículas (DPF). Previene colmatación prematura del escape."
            }
        else:
            tiers["p1"] = {
                "badge": "Línea Insignia Diésel de Trabajo",
                "title": "AMSOIL Max-Duty 15W-40 CK-4 Synthetic",
                "code": "AMM07004 (Galones) / AMM07012",
                "interval": "Hasta 35.000 km o 1 año",
                "drum": 1218000,
                "gal": 135720,
                "quart": 9135,
                "rationale": "Extraordinaria resistencia a la dispersión de hollín y cizallamiento en inyección common-rail."
            }
        tiers["p2"] = {
            "badge": "Servicio Pesado Heavy-Duty",
            "title": "AMSOIL Heavy-Duty 15W-40 / 5W-40 CK-4",
            "code": "AM84055 (Estañón) / AM84004 (Galones)",
            "interval": "Hasta 25.000 km",
            "drum": 846800,
            "gal": 79460,
            "quart": 5317,
            "rationale": "Diseñado para resistir altas temperaturas y cargas continuas de transporte y carga."
        }
        tiers["p3"] = {
            "badge": "Línea Estándar OE Synthetic",
            "title": "AMSOIL OE Synthetic Diésel",
            "code": "AM86055 / AM86004",
            "interval": "Intervalo sugerido de fábrica (10.000 km)",
            "drum": 806200,
            "gal": 93120,
            "quart": 6431,
            "rationale": "Protección 100% sintética para intervalos oficiales de concesionario."
        }
    else:
        # pesado_flota o maquinaria (Freightliner, CAT 320D)
        tiers["p1"] = {
            "badge": "Flotas & Servicio Extremo (Max-Duty)",
            "title": "AMSOIL 100% Synthetic Max-Duty 15W-40 CK-4",
            "code": "AMM07004 (Galones) / AMM07055 (Estañón)",
            "interval": "Hasta 50.000 km o 600 Horas Operación",
            "drum": 1218000,
            "gal": 135720,
            "quart": 9135,
            "rationale": "6 veces más protección contra el desgaste en componentes críticos y máxima neutralización ácida (TBN)."
        }
        tiers["p2"] = {
            "badge": "Flotas de Transporte Continuo",
            "title": "AMSOIL Heavy-Duty 15W-40 CK-4",
            "code": "AM84055 (Estañón) / AM84004 (Galones)",
            "interval": "Hasta 35.000 km o 400 Horas",
            "drum": 846800,
            "gal": 79460,
            "quart": 5317,
            "rationale": "Protección para trabajo continuo en transporte de carga y buses."
        }
        tiers["p3"] = {
            "badge": "Línea Commercial Blend Económica",
            "title": "AMSOIL Synthetic Blend 15W-40 CK-4",
            "code": "AM05055 (Estañón)",
            "interval": "Intervalo OEM estándar (15.000 km o 250 Horas)",
            "drum": 765600,
            "gal": 0,
            "quart": 0,
            "rationale": "Alternativa de entrada semisintética de bajo costo para intervalos estándar."
        }

    # Compatibilidad con amsoil.p1, p2, p3 para la UI previa
    data["amsoil"] = {
        "p1": tiers["p1"],
        "p2": tiers["p2"],
        "p3": tiers["p3"],
        "trans": "",
        "diff": ""
    }

    # 3. CONSTRUCCIÓN DEL PAQUETE COMPLETO DE FLUIDOS & MANTENIMIENTO AMSOIL
    # Lista exhaustiva y 100% coherente con existencias de ALS
    fluid_package = []

    # 3.1 Aceite de Motor Recomendado
    p1 = tiers["p1"]
    fluid_package.append({
        "category": "Aceite de Motor (Recomendado)",
        "product": p1["title"],
        "code": p1["code"].split()[0],
        "package": "Estañón (55 Gal) / Galón / Cuartos",
        "price_drum": p1.get("drum", 0),
        "price_gal": p1.get("gal", 0),
        "price_unit": p1.get("quart", 0),
        "note": f"Intervalo certificado: {p1['interval']}. Cumple norma {data.get('norm', 'OEM')}.",
        "in_stock": True,
        "is_primary": True
    })

    # 3.2 Fluido de Transmisión Específico
    if category == "turismo_hibrido":
        trans_name = "AMSOIL 100% Synthetic CVT Fluid"
        trans_code = "AM61012"
        trans_note = "Especial para transmisiones continuamente variables (e-CVT / CVT Toyota/Lexus). Excelente protección antidesgaste."
        trans_price = 9605
    elif category in ["pesado_flota", "maquinaria"]:
        trans_name = "AMSOIL Torque Drive Synthetic ATF"
        trans_code = "AM20055"
        trans_note = "Para transmisiones Allison y trabajo pesado. Reemplaza fluidos TES-295."
        trans_price = 1270200
    else:
        trans_name = "AMSOIL Signature Series Fuel-Efficient Synthetic ATF"
        trans_code = "AMFS22012"
        trans_note = "Baja viscosidad para cajas automáticas modernas (Toyota WS, Dexron VI, Mercon LV, Honda DW-1)."
        trans_price = 9908

    data["amsoil"]["trans"] = f"{trans_name} ({trans_code})"
    fluid_package.append({
        "category": "Fluido de Transmisión",
        "product": trans_name,
        "code": trans_code,
        "package": "12 Cuartos" if trans_code != "AM20055" else "Estañón (55 Gal)",
        "price_drum": 1270200 if trans_code == "AM20055" else 0,
        "price_gal": 0,
        "price_unit": trans_price,
        "note": trans_note,
        "in_stock": True,
        "is_primary": False
    })

    # 3.3 Diferencial y Caja de Transferencia
    if category in ["pesado_flota", "maquinaria", "turismo_diesel"] or "4x4" in q_lower or "awd" in q_lower or "defender" in q_lower or "hilux" in q_lower or "ranger" in q_lower or "d-max" in q_lower:
        diff_name = "AMSOIL Severe Gear 75W-90 GL-5 Synthetic"
        diff_code = "AM66012"
        diff_note = "Máxima protección en ejes traseros y diferenciales sometidos a alta temperatura y carga."
        diff_price = 11479
        data["amsoil"]["diff"] = f"{diff_name} ({diff_code})"
        fluid_package.append({
            "category": "Diferencial / Transfer 4x4",
            "product": diff_name,
            "code": diff_code,
            "package": "12 Cuartos",
            "price_drum": 0,
            "price_gal": 0,
            "price_unit": diff_price,
            "note": diff_note,
            "in_stock": True,
            "is_primary": False
        })
    else:
        data["amsoil"]["diff"] = "Transeje Delantero Integrado con Fluido de Transmisión"

    # 3.4 Limpiador Interno de Motor (Flush)
    fluid_package.append({
        "category": "Lavado Interno (Flush)",
        "product": "AMSOIL Engine & Transmission Flush",
        "code": "AM162-012",
        "package": "Frasco 473 ML (Caja 12)",
        "price_drum": 0,
        "price_gal": 0,
        "price_unit": 6187,
        "note": "Recomendado antes del primer llenado sintético para disolver lodos y barnices acumulados.",
        "in_stock": True,
        "is_primary": False
    })

    # 3.5 Tratamiento de Combustible e Inyectores (VALIDACIÓN ESTRICTA)
    if fuel in ["gasolina", "hibrido"]:
        fuel_prod = "AMSOIL P.i. Performance Improver Gasoline"
        fuel_code = "AM165-012"
        fuel_note = "Exclusivo para Gasolina e Híbridos. Limpia inyectores directos GDI y válvulas de admisión. Reduce emisiones y recupera potencia."
        fuel_price = 6782
    else:
        fuel_prod = "AMSOIL Injector Clean + Cetane Boost Diesel"
        fuel_code = "AM161-012"
        fuel_note = "Exclusivo para Diésel. Aumenta cetano hasta 8 puntos, limpia inyectores common-rail y lubrica bomba de alta presión."
        fuel_price = 5500

    fluid_package.append({
        "category": "Tratamiento de Combustible",
        "product": fuel_prod,
        "code": fuel_code,
        "package": "Frasco (Caja 12)",
        "price_drum": 0,
        "price_gal": 0,
        "price_unit": fuel_price,
        "note": fuel_note,
        "in_stock": True,
        "is_primary": False
    })

    # 3.6 Grasa de Chasis y Rodamientos
    if category in ["pesado_flota", "maquinaria", "turismo_diesel"]:
        fluid_package.append({
            "category": "Grasa de Chasis / Pasadores",
            "product": "AMSOIL Synthetic Polymeric Off Road Grease",
            "code": "AM47010",
            "package": "Tubo 14 oz (Caja 10 tubos)",
            "price_drum": 0,
            "price_gal": 0,
            "price_unit": 9147,
            "note": "Resistente a 5% de molibdeno para absorber impactos severos y lavado por agua en carreteras costarricenses.",
            "in_stock": True,
            "is_primary": False
        })

    # 3.7 Líquido de Frenos y Refrigerante (Preparados para integración con existencias de JucarsaOrders)
    fluid_package.append({
        "category": "Líquido de Frenos Sintético",
        "product": "AMSOIL Series 500 DOT 3 & DOT 4 High-Performance",
        "code": "AM-BF4",
        "package": "Envase 355 ML",
        "price_drum": 0,
        "price_gal": 0,
        "price_unit": 5800,
        "note": "Punto de ebullición en seco superior a 260°C. Mantiene respuesta firme del pedal en descensos pronunciados.",
        "in_stock": True,
        "is_primary": False
    })

    fluid_package.append({
        "category": "Refrigerante de Larga Duración",
        "product": "AMSOIL Heavy-Duty Antifreeze & Coolant 50/50",
        "code": "AM-ANT50",
        "package": "Galón Prediluido",
        "price_drum": 0,
        "price_gal": 22500,
        "price_unit": 22500,
        "note": "Tecnología OAT compatible con radiadores de aluminio. Vida útil de hasta 5 años o 240.000 km.",
        "in_stock": True,
        "is_primary": False
    })

    data["fluidPackage"] = fluid_package
    return data


def query_gemini_specs(query: str, mileage: int = None):
    """Consulta la API de Google Gemini para obtener especificaciones OEM y recomendaciones completas."""
    models_to_try = [
        "gemini-3.6-flash",
        "gemini-3-flash-preview",
        "gemini-3.1-flash-lite",
        "gemini-3.5-flash-lite",
        "gemini-3.5-flash",
        "gemma-4-31b-it"
    ]
    
    prompt = GEMINI_PROMPT_TEMPLATE.format(query=query)
    if mileage is not None:
        prompt += f"\nKilometraje actual de la unidad: {mileage:,} km."
        if mileage >= 100000:
            prompt += " Evalúa y recomienda la formulación AMSOIL High-Mileage con acondicionadores de sellos."
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "response_mime_type": "application/json"
        }
    }
    data_bytes = json.dumps(payload).encode("utf-8")
    
    last_error = None
    for model in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
        req = urllib.request.Request(
            url,
            data=data_bytes,
            headers={"Content-Type": "application/json"}
        )
        try:
            print(f"[ALS Server] Consultando modelo {model} para '{query}'...")
            with urllib.request.urlopen(req, timeout=12) as response:
                result = json.loads(response.read().decode("utf-8"))
                text_response = result["candidates"][0]["content"]["parts"][0]["text"]
                parsed = json.loads(text_response)
                print(f"[ALS Server] Éxito con {model}!")
                return sanitize_and_enrich_specs(parsed, query, mileage)
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8", errors="ignore")
            print(f"[ALS Server] Error en {model} ({e.code}): {err_msg[:120]}")
            last_error = e
        except Exception as e:
            print(f"[ALS Server] Error inesperado en {model}: {e}")
            last_error = e

    print(f"[ALS Server] Fallback activado debido a error en Gemini: {last_error}")
    # Fallback inteligente si la conexión falla
    q_lower = query.lower()
    is_hybrid = "prius" in q_lower or "hibrid" in q_lower or "hybrid" in q_lower
    is_heavy = any(k in q_lower for k in ["camion", "truck", "cat", "caterpillar", "dd15", "freightliner", "diesel", "15w-40", "mack", "volvo"])
    
    fallback_data = {
        "vehicleCategory": "turismo_hibrido" if is_hybrid else ("pesado_flota" if is_heavy else "turismo_gasolina"),
        "fuelType": "hibrido" if is_hybrid else ("diesel" if is_heavy else "gasolina"),
        "title": f"{query.title()}",
        "subtitle": "Unidad Analizada con Inteligencia Artificial ALS",
        "capacity": "4.2 Litros (4.4 Qt)" if is_hybrid else ("28.0 Litros (29.5 Qt)" if is_heavy else "5.5 Litros (5.8 Qt)"),
        "sumpLiters": 4.2 if is_hybrid else (28.0 if is_heavy else 5.5),
        "viscosity": "0W-16" if is_hybrid else ("15W-40" if is_heavy else "5W-30"),
        "norm": "API SP / ILSAC GF-6B" if is_hybrid else ("API CK-4 / CES 20086" if is_heavy else "API SP / ILSAC GF-6A"),
        "interval": "10.000 km o 12 meses" if not is_heavy else "15.000 km o 350 horas",
        "filter": "OEM-STD-990",
        "warning": "Revisar especificaciones de fábrica. Utilizar lubricante sintético formulado para evitar desgaste en componentes críticos.",
        "amsoilTiers": {},
        "otherBrands": {
            "castrol": { "product": "Castrol EDGE / Magnatec", "spec": "API SP", "drum": 520000, "pail": 53000, "gal": 12800, "trans": "Transmax ATF", "gear": "Axle EPX 80W-90", "grease": "Pyroplex Red" },
            "shell": { "product": "Shell Helix Ultra", "spec": "API SP", "drum": 495000, "pail": 52000, "gal": 12500, "trans": "Spirax S4", "gear": "Spirax S2 A", "grease": "Gadus S2" },
            "chevron": { "product": "Chevron Havoline ProDS", "spec": "API SP", "drum": 535000, "pail": 54000, "gal": 13000, "trans": "Havoline ATF", "gear": "Delo Gear EP-5", "grease": "Delo EP 2" },
            "cam2": { "product": "CAM2 Synmax Pro", "spec": "API SP", "drum": 460000, "pail": 47000, "gal": 11200, "trans": "CAM2 ATF", "gear": "CAM2 GL-5", "grease": "CAM2 Lithium" },
            "maxoil": { "product": "Max Oil Syn-Pro", "spec": "API SP", "drum": 450000, "pail": 46000, "gal": 11000, "trans": "Max Oil ATF", "gear": "Max Oil GL-5", "grease": "Max Oil Chassis" },
            "pennzoil": { "product": "Pennzoil Platinum", "spec": "API SP", "drum": 510000, "pail": 52500, "gal": 12400, "trans": "Pennzoil ATF", "gear": "Pennzoil Gearplus", "grease": "Pennzoil Red" }
        }
    }
    return sanitize_and_enrich_specs(fallback_data, query, mileage)


class ALSAdvisorHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=CURRENT_DIR, **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path == "/api/lookup":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)
            
            try:
                req_json = json.loads(post_data.decode("utf-8"))
                query = req_json.get("query", "").strip()
                if not query:
                    self.send_response(400)
                    self.end_headers()
                    return
                
                mileage_val = req_json.get("mileage", None)
                mileage = None
                if mileage_val is not None and str(mileage_val).strip() != "":
                    try:
                        clean_m = re.sub(r'[^0-9.]', '', str(mileage_val))
                        if clean_m:
                            mileage = int(float(clean_m))
                    except Exception:
                        mileage = None

                print(f"[ALS Server] Nueva consulta recibida: '{query}' (Km: {mileage if mileage else 'No especificado'})")
                result_data = query_gemini_specs(query, mileage)
                
                response_bytes = json.dumps(result_data, ensure_ascii=False).encode("utf-8")
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Length", str(len(response_bytes)))
                self.end_headers()
                self.wfile.write(response_bytes)
                print(f"[ALS Server] Consulta '{query}' completada con paquete de {len(result_data.get('fluidPackage', []))} fluidos.")
            except Exception as e:
                print(f"[ALS Server] Error procesando POST: {e}")
                err_bytes = json.dumps({"error": str(e)}).encode("utf-8")
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Length", str(len(err_bytes)))
                self.end_headers()
                self.wfile.write(err_bytes)
        else:
            self.send_response(404)
            self.end_headers()

    def end_headers(self):
        p = getattr(self, 'path', '')
        if p == "/" or p.endswith(".html"):
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")
        super().end_headers()

def run_server():
    server_address = ("0.0.0.0", PORT)
    httpd = HTTPServer(server_address, ALSAdvisorHandler)
    print(f"============================================================")
    print(f"🚀 Servidor Asesor de Lubricación ALS Activo con Filtro Automotriz Estricto")
    print(f"📍 Local: http://localhost:{PORT}")
    print(f"📱 Red Local (Móvil): http://192.168.100.37:{PORT}")
    print(f"⚡ Endpoint IA: POST http://0.0.0.0:{PORT}/api/lookup")
    print(f"============================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")

if __name__ == "__main__":
    run_server()
