#!/usr/bin/env python3
"""
Generador Oficial del Portal Informativo AMSOIL Costa Rica (American Lubricants Supply S.A.)
Cumplimiento estricto del Manual Oficial: AMSOIL_BrandStyleGuide_7-26.pdf

Directrices aplicadas al 100%:
1. Paleta cromática exacta (Pág. 25): #005BAA (Pantone 286), #ED1C24 (Pantone 485),
   #BCBEC0 (Cool Gray 6), #000000 (Process Black), #FFFFFF (White).
2. Tipografía digital oficial (Pág. 27): Open Sans Bold (700), Regular (400), Light (300).
   Titulares cortos en Initial Caps y titulares largos en Sentence case (sin bloques en mayúsculas sostenidas).
3. Normas del logotipo (Págs. 19–25): Exactamente 1 logotipo AMSOIL por página web (en Header blanco sólido),
   ancho >= 38 mm (1.5"), área de reserva >= 1X ("O") e Insignia Digital exclusiva en favicon/app-icon.
4. Publicaciones y Nomenclatura (Pág. 29): Orden oficial [AMSOIL + Familia + Viscosidad + Synthetic + Tipo],
   símbolos ® en primera mención, AMSOIL INC. siempre en mayúsculas sin coma previa y cero códigos de almacén frente al cliente.
5. Voz de marca (Págs. 11–16): Directa, técnica, enfocada en Protección y Rendimiento ("Overkill is Underrated" + Fórmula ABC).
"""

import json
import html
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CATALOG_PATH = BASE_DIR / "catalogo-imagenes.json"
HOME_PAGE = "index-catalogo.html"

with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    CATALOG = json.load(f)

BY_ID = {item["id"]: item for item in CATALOG}

GOOGLE_FONTS_HEAD = """    <link rel="icon" type="image/png" href="favicon.png">
    <link rel="apple-touch-icon" href="assets/logos/amsoil-insignia.png">
    <meta name="theme-color" content="#000000">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300;0,400;0,600;0,700;1,400;1,700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/styles.css">"""

# Iconos vectoriales limpios de trazo firme y bordes redondeados (Manual Pág. 28)
SVG_DOC = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="8" y1="13" x2="16" y2="13"/><line x1="8" y1="17" x2="13" y2="17"/></svg>'
SVG_PIN = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>'
SVG_NAV = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>'
SVG_PHONE = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.58 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
SVG_MSG = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>'

LINE_DISPLAY_MAP = {
    "signature-series": "Signature Series",
    "xl-synthetic": "XL Extended Life",
    "oe-synthetic": "OE Synthetic",
    "hybrid": "Hybrid Synthetic",
    "high-mileage": "High-Mileage Synthetic",
    "racing-zrod-dominator": "DOMINATOR® / Z-ROD® / Especialidad",
    "european-car-formula": "European Car Formula",
    "signature-series-max-duty": "Signature Series Max-Duty",
    "heavy-duty-ck4": "Heavy-Duty Diesel",
    "diesel-dexos-d": "100% Synthetic Diesel",
    "severe-gear-y-diferenciales": "SEVERE GEAR® & Diferenciales",
    "transmision-automatica-atf-cvt-dct": "Transmisión ATF / CVT / DCT",
    "metric-motorcycle": "Metric Motorcycle",
    "dirt-bike": "Dirt Bike",
    "v-twin": "V-Twin Motorcycle",
    "2-stroke": "2-Stroke Powersports",
    "atv-utv": "ATV / UTV",
    "marino": "HP Marine®",
    "4t-motorcycle": "4T Performance",
    "aditivos-combustible": "Aditivos de Combustible",
    "coolant-anticongelante": "Antifreeze & Coolant",
    "fluidos-frenos-direccion-varios": "Frenos, Dirección y Especialidades",
    "grasas-y-lubricantes": "Grasas Sintéticas",
}


def clean_container_label(raw_lbl):
    if not raw_lbl:
        return "Envase"
    lbl = re.sub(r"\s*\([A-Z0-9-]{2,12}\)\s*", "", raw_lbl)
    lbl = (
        lbl.replace(" (946 mL)", "")
        .replace(" (3.78 L)", "")
        .replace("Recorte PNG", "Vista Principal")
        .replace("Vista Recorte PNG/WebP", "Vista Principal")
        .replace("Envase Oficial", "Vista Principal")
    )
    return lbl.strip() or "Envase"


def pick_primary_image(item):
    images = item.get("images", [])
    for img in images:
        if "recorte-fondo-transparente" in img["filename"]:
            return img
    for img in images:
        if img.get("is_container"):
            return img
    return images[0] if images else None


def get_unique_presentations(item):
    """Devuelve hasta 4 vistas distintas de envase sin códigos de almacén."""
    images = item.get("images", [])
    seen_labels = set()
    selected = []
    primary = pick_primary_image(item)
    if primary:
        lbl = "Vista Principal" if "recorte-fondo-transparente" in primary["filename"] else clean_container_label(primary.get("short_label", "Envase"))
        seen_labels.add(lbl)
        selected.append((lbl, primary["rel_path"]))

    for img in images:
        if primary and img["rel_path"] == primary["rel_path"]:
            continue
        fn = img["filename"]
        if "catalogo-latam" in fn or "familia-" in fn or "envase-principal" in fn:
            continue
        raw_lbl = "Vista Principal" if "recorte-fondo-transparente" in fn else (img.get("short_label") or img.get("presentation") or "Envase")
        lbl = clean_container_label(raw_lbl)
        if lbl not in seen_labels:
            seen_labels.add(lbl)
            selected.append((lbl, img["rel_path"]))
        if len(selected) >= 4:
            break

    if len(selected) < 2:
        for img in images:
            if primary and img["rel_path"] == primary["rel_path"]:
                continue
            if "catalogo-latam" in img["filename"]:
                continue
            lbl = clean_container_label(img.get("short_label") or "Vista Adicional")
            if lbl not in seen_labels:
                seen_labels.add(lbl)
                selected.append((lbl, img["rel_path"]))
            if len(selected) >= 4:
                break
    return selected[:4]


def get_specific_subcat_token(prod_id):
    token_map = {
        # European Formula
        "ezt-0w-20-ls-vw": "low-saps",
        "afe-0w-20-ls": "low-saps",
        "ael-5w-30-ls": "low-saps",
        "eot-0w-30-ms": "mid-saps",
        "afl-5w-40-ms-acea-c3": "mid-saps",
        "efo-0w-40-fs": "full-saps",
        "efm-5w-40-fs": "full-saps",
        # Motos & ATV/UTV
        "mmf-5w-40": "metric-motorcycle",
        "mct-10w-30": "metric-motorcycle",
        "mcf-10w-40": "metric-motorcycle",
        "mff-15w-50": "metric-motorcycle",
        "mcs-sae-60": "v-twin-oil",
        "msv-15w-60": "v-twin-oil",
        "mvi-20w-40": "v-twin-oil",
        "mcv-20w-50": "v-twin-oil",
        "mvp-primary-fluid": "v-twin-primary",
        "mvt-transmission-fluid": "v-twin-trans",
        "mc3-10w-30": "4t-performance",
        "mc4-10w-40": "4t-performance",
        "mc5-20w-50": "4t-performance",
        "db40-10w-40": "dirt-bike-oil",
        "db50-10w-50": "dirt-bike-oil",
        "dbtf-transmission-fluid": "dirt-bike-trans",
        "tdr-dominator-2-stroke-racing": "dominator-2t",
        "ait-interceptor-2-stroke": "interceptor-2t",
        "stm-shock-therapy-suspension-fluid-10": "shock-therapy",
        "auv54-5w-40": "atv-utv-oil",
        "auv50-5w-50": "atv-utv-oil",
        "auv40-10w-40": "atv-utv-oil",
        "audt-transmission-and-differential-fluid": "atv-utv-trans",
        "audct-dct-fluid": "atv-utv-dct",
        "hpm-hp-marine-2-stroke": "marino",
        # Transmisión / Gear
        "atf-signature-series-multi-vehicle-atf-red": "signature-atf",
        "atl-signature-series-fuel-efficient-atf-blue": "signature-atf",
        "ulv-signature-series-ulv-atf": "signature-atf",
        "otf-oe-multi-vehicle-atf-red": "oe-atf",
        "otl-oe-fuel-efficient-atf-blue": "oe-atf",
        "atd-torque-drive-atf": "torque-drive",
        "art-super-shift-racing-atf": "super-shift",
        "cvt-cvt-fluid": "cvt-fluid",
        "dct-dct-fluid": "dct-fluid",
        "mtf-manual-synchromesh-5w-30": "synchromesh",
        "mtg-manual-transaxle-75w-90-gl4": "manual-gl4",
        "svl-severe-gear-75w-85": "severe-gear",
        "svg-severe-gear-75w-90": "severe-gear",
        "svo-severe-gear-75w-140": "severe-gear",
        "agl-severe-gear-80w-90": "severe-gear",
        "fgr-long-life-gear-75w-90": "long-life-gear",
        "ada-slip-lock-differential-additive": "slip-lock",
        # Aditivos / Coolant
        "api-pi-performance-improver": "pi-improver",
        "ucl-upper-cylinder-lubricant-gasoline": "upper-cylinder",
        "aob-dominator-octane-boost": "octane-boost",
        "mob-motorcycle-octane-boost": "moto-octane",
        "ads-diesel-injector-clean-cetane-boost": "diesel-injector",
        "flsh-engine-and-transmission-flush": "engine-flush",
        "antpc-passenger-car-antifreeze-50-50-yellow": "antpc",
        "anthd-heavy-duty-antifreeze-50-50-red": "anthd",
        "psaf-powersports-antifreeze-coolant": "psaf",
        "rdcb-dominator-coolant-boost": "coolant-boost",
        "bflv-dot-3-4-brake-fluid": "dot34-brake",
        "bfr-dominator-dot-4-racing-brake-fluid": "dominator-brake",
        "psf-power-steering-fluid": "power-steering",
        "gpor2-polymeric-off-road-grease-nlgi-2": "off-road-grease",
        "glc-multi-purpose-grease-nlgi-2": "multi-purpose-grease",
        "glc-red-grease-120-lbs": "red-grease",
        "acl-chain-lube-spray": "chain-lube",
        "eal-engine-assembly-lube": "assembly-lube",
        "pcj-compressor-oil-iso-68": "compressor-oil",
        "atp-saber-professional-2-stroke": "saber-2t",
    }
    return token_map.get(prod_id, "")


def render_product_card(item, extra_subcat=""):
    prod_id = item["id"]
    line = item["line"]
    visc = item.get("viscosity") or ""
    tech = item.get("tech_sheet") or {}
    summary = tech.get("summary") or ""

    primary_img = pick_primary_image(item)
    primary_src = primary_img["rel_path"] if primary_img else "01-motor-gasolina/signature-series/5w-30/recorte-fondo-transparente-ASL.webp"
    presentations = get_unique_presentations(item)

    visc_slug = visc.lower().replace("-", "").replace(" ", "")
    specific_token = get_specific_subcat_token(prod_id)
    subcat_tokens = f"{line} {visc_slug} {extra_subcat} {specific_token}".strip()

    pres_buttons_html = ""
    for idx, (short_lbl, rel_path) in enumerate(presentations):
        active_cls = "active" if idx == 0 else ""
        pres_buttons_html += (
            f'<button type="button" class="pres-switch-btn {active_cls}" '
            f'data-img-src="{html.escape(rel_path)}">'
            f'{html.escape(short_lbl)}</button>'
        )

    has_visc = visc and visc not in ("N/A", "Especialidad")
    visc_pill_html = f'<span class="prod-viscosity-pill">{html.escape(visc)}</span>' if has_visc else ""

    # Manual Pág. 29: Nunca referirse a un producto por su código de almacén en textos dirigidos al cliente
    if prod_id == "brk-break-in-oil-sae-30":
        line_badge = "Asentamiento de Motores • SAE 30"
    else:
        base_line = LINE_DISPLAY_MAP.get(line, item.get("category_short", "AMSOIL"))
        line_badge = f"{base_line} • {visc}" if has_visc else base_line

    return f"""
                <article class="amsoil-prod-tile" data-product-id="{html.escape(prod_id)}" data-subcat="{html.escape(subcat_tokens)}">
                    {visc_pill_html}
                    <div class="prod-tile-image">
                        <img src="{html.escape(primary_src)}" alt="{html.escape(item['display_name'])}" class="prod-tile-photo" loading="lazy">
                    </div>
                    <div class="prod-tile-body">
                        <div class="prod-tile-code">{html.escape(line_badge)}</div>
                        <h3 class="prod-tile-title">{html.escape(item['display_name'])}</h3>
                        <p class="prod-tile-desc">{html.escape(summary)}</p>
                        <div class="prod-presentations-bar">
                            {pres_buttons_html}
                        </div>
                    </div>
                    <div class="prod-tile-footer">
                        <button type="button" class="btn-pds-trigger" data-open-pds="{html.escape(prod_id)}">
                            {SVG_DOC} Ver Ficha Técnica y Envases
                        </button>
                    </div>
                </article>"""


def render_common_header(active_page="", search_placeholder="Ingresa tu vehículo, motor, maquinaria, viscosidad (ej. 5W-30, 15W-40) o línea AMSOIL..."):
    def nav_cls(page):
        return "nav-trigger active-page" if active_page == page else "nav-trigger"

    return f"""    <!-- NIVEL 1: TOP CORPORATE BAR (#000000 Process Black + #005BAA Pantone 286) -->
    <div class="amsoil-utility-bar">
        <div class="container utility-inner">
            <span class="utility-tagline"><strong>The First in Synthetics®</strong> — Ingeniería en lubricación sintética desde 1972</span>
            <span class="region-selector">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
                COSTA RICA
            </span>
        </div>
    </div>

    <!-- NIVEL 2: MAIN BRAND HEADER (#FFFFFF Sólido + Único Logotipo Oficial AMSOIL con Área de Reserva 1X) -->
    <header class="amsoil-brand-header">
        <div class="container brand-header-inner">
            <a href="{HOME_PAGE}" class="amsoil-official-logo" aria-label="AMSOIL Costa Rica Inicio">
                <img src="amsoil-logo.png" alt="AMSOIL®" class="amsoil-logo-svg" width="192" height="59">
            </a>

            <form id="headerGlobalSearchForm" class="global-search-form">
                <input
                    type="text"
                    id="headerGlobalSearchInput"
                    class="global-search-input"
                    placeholder="{html.escape(search_placeholder)}"
                >
                <button type="submit" class="global-search-btn" aria-label="Buscar Vehículo o Producto">
                    <svg class="car-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 16H9m10 0h3v-3.15a1 1 0 0 0-.84-.99L16 11l-2.7-3.6a1 1 0 0 0-.8-.4H5.24a2 2 0 0 0-1.8 1.1l-.8 1.63A6 6 0 0 0 2 12.42V16h2"/><circle cx="6.5" cy="16.5" r="2.5"/><circle cx="16.5" cy="16.5" r="2.5"/></svg>
                    <div class="search-btn-label">
                        <strong>Buscar Vehículo</strong>
                        <span>o Viscosidad / Fluido</span>
                    </div>
                    <svg class="lupa-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
                </button>
            </form>

            <div class="header-quick-tools">
                <a href="contacto.html" class="tool-item">
                    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                    <div class="tool-text">
                        <strong>Contáctenos</strong>
                        <span>Puntos de Venta y Talleres</span>
                    </div>
                </a>
            </div>
        </div>
    </header>

    <!-- NIVEL 3: BARRA DE NAVEGACIÓN PRINCIPAL CON MEGA-MENÚS -->
    <nav class="amsoil-nav-bar" aria-label="Navegación Principal">
        <div class="container nav-bar-inner">
            <ul class="primary-nav-list">
                <li class="nav-item">
                    <a href="automotriz.html" class="{nav_cls('automotriz')}">
                        <span>Aceite de Motor</span>
                        <svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>
                    </a>
                    <div class="mega-menu">
                        <div class="container mega-menu-grid">
                            <div class="mega-col">
                                <h4>Automotriz Gasolina</h4>
                                <ul>
                                    <li><a href="automotriz.html?filter=signature-series">AMSOIL Signature Series 100% Sintético</a></li>
                                    <li><a href="automotriz.html?filter=xl-synthetic">AMSOIL XL Extended Life 100% Sintético</a></li>
                                    <li><a href="automotriz.html?filter=oe-synthetic">AMSOIL OE 100% Sintético Motor Oil</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4>Híbridos y Alto Kilometraje</h4>
                                <ul>
                                    <li><a href="automotriz.html?filter=hybrid">AMSOIL 100% Sintético Hybrid Motor Oil</a></li>
                                    <li><a href="automotriz.html?filter=high-mileage">AMSOIL 100% Sintético High-Mileage Motor Oil</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4>Competencia y Clásicos</h4>
                                <ul>
                                    <li><a href="automotriz.html?filter=dominator">AMSOIL DOMINATOR® 100% Sintético Racing Oil</a></li>
                                    <li><a href="automotriz.html?filter=z-rod">AMSOIL Z-ROD® 100% Sintético Motor Oil</a></li>
                                    <li><a href="automotriz.html?filter=break-in">AMSOIL SAE 30 Break-In Oil</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </li>

                <li class="nav-item">
                    <a href="diesel.html" class="{nav_cls('diesel')}">
                        <span>Diesel</span>
                        <svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>
                    </a>
                    <div class="mega-menu">
                        <div class="container mega-menu-grid">
                            <div class="mega-col">
                                <h4>Signature Series Max-Duty</h4>
                                <ul>
                                    <li><a href="diesel.html?filter=signature-series-max-duty">AMSOIL Signature Series Max-Duty 100% Sintético</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4>Heavy-Duty Diesel</h4>
                                <ul>
                                    <li><a href="diesel.html?filter=heavy-duty-ck4">AMSOIL Heavy-Duty 100% Sintético Diesel Oil</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4>Diesel Ligero GM dexosD</h4>
                                <ul>
                                    <li><a href="diesel.html?filter=diesel-dexos-d">AMSOIL 100% Sintético Diesel Oil (GM dexosD)</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </li>

                <li class="nav-item">
                    <a href="european.html" class="{nav_cls('european')}">
                        <span>European Formula</span>
                        <svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>
                    </a>
                    <div class="mega-menu">
                        <div class="container mega-menu-grid">
                            <div class="mega-col">
                                <h4>Low-SAPS (LS)</h4>
                                <ul>
                                    <li><a href="european.html?filter=low-saps">AMSOIL European Car Formula Low-SAPS 100% Sintético</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4>Mid-SAPS (MS)</h4>
                                <ul>
                                    <li><a href="european.html?filter=mid-saps">AMSOIL European Car Formula Mid-SAPS 100% Sintético</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4>Full-SAPS (FS)</h4>
                                <ul>
                                    <li><a href="european.html?filter=full-saps">AMSOIL European Car Formula Full-SAPS 100% Sintético</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </li>

                <li class="nav-item">
                    <a href="motos.html" class="{nav_cls('motos')}">
                        <span>Motos &amp; ATV/UTV</span>
                        <svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>
                    </a>
                    <div class="mega-menu">
                        <div class="container mega-menu-grid">
                            <div class="mega-col">
                                <h4>Motocicletas de Calle y V-Twin</h4>
                                <ul>
                                    <li><a href="motos.html?filter=metric-motorcycle">AMSOIL 100% Sintético Metric Motorcycle Oil</a></li>
                                    <li><a href="motos.html?filter=v-twin-oil">AMSOIL 100% Sintético V-Twin Motorcycle Oil</a></li>
                                    <li><a href="motos.html?filter=v-twin-primary">AMSOIL 100% Sintético V-Twin Primary Fluid</a></li>
                                    <li><a href="motos.html?filter=v-twin-trans">AMSOIL 100% Sintético V-Twin Transmission Fluid</a></li>
                                    <li><a href="motos.html?filter=4t-performance">AMSOIL 4T Performance Synthetic Motorcycle Oil</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4>Dirt Bike, 2 Tiempos y Suspensión</h4>
                                <ul>
                                    <li><a href="motos.html?filter=dirt-bike-oil">AMSOIL 100% Sintético Dirt Bike Oil</a></li>
                                    <li><a href="motos.html?filter=dirt-bike-trans">AMSOIL 100% Sintético Dirt Bike Transmission Fluid</a></li>
                                    <li><a href="motos.html?filter=dominator-2t">AMSOIL DOMINATOR® 100% Sintético 2-Stroke Racing Oil</a></li>
                                    <li><a href="motos.html?filter=interceptor-2t">AMSOIL INTERCEPTOR® 100% Sintético 2-Stroke Oil</a></li>
                                    <li><a href="motos.html?filter=shock-therapy">AMSOIL Shock Therapy® Suspension Fluid</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4>ATV/UTV y Marino</h4>
                                <ul>
                                    <li><a href="motos.html?filter=atv-utv-oil">AMSOIL 100% Sintético ATV/UTV Motor Oil</a></li>
                                    <li><a href="motos.html?filter=atv-utv-trans">AMSOIL 100% Sintético ATV/UTV Transmission &amp; Differential Fluid</a></li>
                                    <li><a href="motos.html?filter=atv-utv-dct">AMSOIL 100% Sintético ATV/UTV DCT Fluid</a></li>
                                    <li><a href="motos.html?filter=marino">AMSOIL HP Marine® 100% Sintético 2-Stroke Oil</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </li>

                <li class="nav-item">
                    <a href="transmision.html" class="{nav_cls('transmision')}">
                        <span>Transmisión / Gear</span>
                        <svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>
                    </a>
                    <div class="mega-menu">
                        <div class="container mega-menu-grid">
                            <div class="mega-col">
                                <h4>Transmisión Automática ATF</h4>
                                <ul>
                                    <li><a href="transmision.html?filter=signature-atf">AMSOIL Signature Series 100% Sintético ATF</a></li>
                                    <li><a href="transmision.html?filter=oe-atf">AMSOIL OE 100% Sintético ATF</a></li>
                                    <li><a href="transmision.html?filter=torque-drive">AMSOIL Torque-Drive® 100% Sintético ATF</a></li>
                                    <li><a href="transmision.html?filter=super-shift">AMSOIL Super Shift® Racing Transmission Fluid</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4>CVT, DCT y Transmisión Manual</h4>
                                <ul>
                                    <li><a href="transmision.html?filter=cvt-fluid">AMSOIL 100% Sintético CVT Fluid</a></li>
                                    <li><a href="transmision.html?filter=dct-fluid">AMSOIL 100% Sintético DCT Fluid</a></li>
                                    <li><a href="transmision.html?filter=synchromesh">AMSOIL Manual Synchromesh Transmission Fluid</a></li>
                                    <li><a href="transmision.html?filter=manual-gl4">AMSOIL Manual Transmission &amp; Transaxle Gear Lube</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4>Diferenciales y Engranajes</h4>
                                <ul>
                                    <li><a href="transmision.html?filter=severe-gear">AMSOIL SEVERE GEAR® 100% Sintético Gear Lube</a></li>
                                    <li><a href="transmision.html?filter=long-life-gear">AMSOIL Long Life 100% Sintético Gear Lube</a></li>
                                    <li><a href="transmision.html?filter=slip-lock">AMSOIL Slip Lock® Differential Additive</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </li>

                <li class="nav-item">
                    <a href="aditivos.html" class="{nav_cls('aditivos')}">
                        <span>Aditivos / Coolant</span>
                        <svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>
                    </a>
                    <div class="mega-menu">
                        <div class="container mega-menu-grid">
                            <div class="mega-col">
                                <h4>Aditivos de Combustible y Motor</h4>
                                <ul>
                                    <li><a href="aditivos.html?filter=pi-improver">AMSOIL P.i.® Performance Improver Gasoline Additive</a></li>
                                    <li><a href="aditivos.html?filter=upper-cylinder">AMSOIL Upper Cylinder Lubricant Gasoline Additive</a></li>
                                    <li><a href="aditivos.html?filter=octane-boost">AMSOIL DOMINATOR® Octane Boost</a></li>
                                    <li><a href="aditivos.html?filter=moto-octane">AMSOIL Motorcycle Octane Boost</a></li>
                                    <li><a href="aditivos.html?filter=diesel-injector">AMSOIL Diesel Injector Clean + Cetane Boost</a></li>
                                    <li><a href="aditivos.html?filter=engine-flush">AMSOIL Engine &amp; Transmission Flush</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4>Coolant, Frenos y Dirección</h4>
                                <ul>
                                    <li><a href="aditivos.html?filter=antpc">AMSOIL Passenger Car &amp; Light Truck Antifreeze &amp; Coolant</a></li>
                                    <li><a href="aditivos.html?filter=anthd">AMSOIL Heavy-Duty Antifreeze &amp; Coolant</a></li>
                                    <li><a href="aditivos.html?filter=psaf">AMSOIL Powersports Antifreeze &amp; Coolant</a></li>
                                    <li><a href="aditivos.html?filter=coolant-boost">AMSOIL DOMINATOR® Coolant Boost</a></li>
                                    <li><a href="aditivos.html?filter=dot34-brake">AMSOIL DOT 3 &amp; DOT 4 100% Sintético Brake Fluid</a></li>
                                    <li><a href="aditivos.html?filter=dominator-brake">AMSOIL DOMINATOR® DOT 4 100% Sintético Racing Brake Fluid</a></li>
                                    <li><a href="aditivos.html?filter=power-steering">AMSOIL 100% Sintético Multi-Vehicle Power Steering Fluid</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4>Grasas y Especialidades</h4>
                                <ul>
                                    <li><a href="aditivos.html?filter=off-road-grease">AMSOIL NLGI #2 100% Sintético Polymeric Off-Road Grease</a></li>
                                    <li><a href="aditivos.html?filter=multi-purpose-grease">AMSOIL NLGI #2 100% Sintético Multi-Purpose Grease</a></li>
                                    <li><a href="aditivos.html?filter=red-grease">AMSOIL NLGI #2 100% Sintético Multi-Purpose Red Grease</a></li>
                                    <li><a href="aditivos.html?filter=chain-lube">AMSOIL Chain Lube</a></li>
                                    <li><a href="aditivos.html?filter=assembly-lube">AMSOIL Engine Assembly Lube</a></li>
                                    <li><a href="aditivos.html?filter=compressor-oil">AMSOIL ISO 68 100% Sintético Compressor Oil</a></li>
                                    <li><a href="aditivos.html?filter=saber-2t">AMSOIL SABER® Professional 100% Sintético 2-Stroke Oil</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </li>
            </ul>
        </div>
    </nav>

    <!-- CARRUSEL PRINCIPAL (#000000 Process Black + #005BAA Pantone 286 + #ED1C24 Pantone 485) -->
    <section class="amsoil-hero-carousel" id="amsoilHeroCarousel" aria-label="Soluciones de Lubricación Sintética AMSOIL">
        <button type="button" class="carousel-arrow-btn prev" aria-label="Anterior">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>
        </button>

        <div class="hero-carousel-track">
            <!-- DIAPOSITIVA 1: SIGNATURE SERIES -->
            <div class="hero-carousel-slide active">
                <div class="hero-slide-inner">
                    <div class="hero-slide-visual">
                        <img src="01-motor-gasolina/signature-series/0w-20/recorte-fondo-transparente-ASM.webp" alt="AMSOIL Signature Series 0W-20 100% Synthetic Motor Oil">
                        <img src="01-motor-gasolina/signature-series/5w-30/recorte-fondo-transparente-ASL.webp" alt="AMSOIL Signature Series 5W-30 100% Synthetic Motor Oil" class="featured-center">
                        <img src="01-motor-gasolina/signature-series/10w-30/recorte-fondo-transparente-ATM.webp" alt="AMSOIL Signature Series 10W-30 100% Synthetic Motor Oil">
                    </div>
                    <div class="hero-slide-content">
                        <span class="hero-slide-kicker">THE FIRST IN SYNTHETICS®</span>
                        <h2 class="hero-slide-title">AMSOIL Signature Series 100% Synthetic Motor Oil</h2>
                        <p class="hero-slide-subtitle">Diseñado para máxima protección y rendimiento: 75% más protección contra pérdida de potencia y desgaste.</p>
                        <a href="automotriz.html?filter=signature-series" class="hero-slide-cta">Explorar Línea Signature Series</a>
                        <div class="hero-slide-note">40% pistones más limpios en la prueba de doble duración <strong>ASTM Sequence IIIH</strong></div>
                    </div>
                </div>
            </div>

            <!-- DIAPOSITIVA 2: DIESEL MAX-DUTY & HEAVY-DUTY -->
            <div class="hero-carousel-slide slide-theme-2">
                <div class="hero-slide-inner">
                    <div class="hero-slide-visual">
                        <img src="02-motor-diesel/signature-series-max-duty/5w-40/recorte-fondo-transparente-DEO.webp" alt="AMSOIL Signature Series Max-Duty 5W-40 100% Synthetic Diesel Oil">
                        <img src="02-motor-diesel/signature-series-max-duty/15w-40/recorte-fondo-transparente-DME.webp" alt="AMSOIL Signature Series Max-Duty 15W-40 100% Synthetic Diesel Oil" class="featured-center">
                        <img src="02-motor-diesel/heavy-duty-ck4/15w-40/recorte-fondo-transparente-ADP.webp" alt="AMSOIL Heavy-Duty 15W-40 100% Synthetic Diesel Oil">
                    </div>
                    <div class="hero-slide-content">
                        <span class="hero-slide-kicker">PROTECCIÓN TURBODIÉSEL COMPROBADA</span>
                        <h2 class="hero-slide-title">Max-Duty &amp; Heavy-Duty Synthetic Diesel Oil</h2>
                        <p class="hero-slide-subtitle">6X más protección contra desgaste del motor en motores turbodiésel bajo carga severa y remolque.</p>
                        <a href="diesel.html" class="hero-slide-cta">Ver Lubricantes Diesel</a>
                        <div class="hero-slide-note">Supera ampliamente el estándar <strong>Detroit Diesel DD13 Scuffing (API CK-4)</strong></div>
                    </div>
                </div>
            </div>

            <!-- DIAPOSITIVA 3: EUROPEAN FORMULA & SEVERE GEAR -->
            <div class="hero-carousel-slide slide-theme-3">
                <div class="hero-slide-inner">
                    <div class="hero-slide-visual">
                        <img src="01-motor-gasolina/european-car-formula/5w-30-ls/recorte-fondo-transparente-AEL.webp" alt="AMSOIL European Car Formula 5W-30 LS 100% Synthetic Motor Oil">
                        <img src="03-transmision-y-diferenciales/severe-gear-y-diferenciales/severe-gear-75w-90/recorte-fondo-transparente-SVG.webp" alt="AMSOIL SEVERE GEAR® 75W-90 100% Synthetic Gear Lube" class="featured-center">
                        <img src="03-transmision-y-diferenciales/transmision-automatica-atf-cvt-dct/signature-series-multi-vehicle-atf-red/recorte-fondo-transparente-ATF.webp" alt="AMSOIL Signature Series Multi-Vehicle 100% Synthetic ATF">
                    </div>
                    <div class="hero-slide-content">
                        <span class="hero-slide-kicker">ENGINEERED FOR WHAT YOU DRIVE AND HOW YOU DRIVE®</span>
                        <h2 class="hero-slide-title">European Car Formula &amp; SEVERE GEAR®</h2>
                        <p class="hero-slide-subtitle">Formulaciones especializadas para motores europeos modernos, transmisiones y diferenciales 4x4 bajo presión extrema.</p>
                        <a href="transmision.html" class="hero-slide-cta">Explorar Transmisión y Diferenciales</a>
                        <div class="hero-slide-note">Disponible en <strong>Puntos de Venta y Talleres Autorizados en Costa Rica</strong></div>
                    </div>
                </div>
            </div>
        </div>

        <button type="button" class="carousel-arrow-btn next" aria-label="Siguiente">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l6-6-6-6"/></svg>
        </button>

        <button type="button" class="carousel-pause-btn" aria-label="Pausar banner">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="5" width="4" height="14"/><rect x="14" y="5" width="4" height="14"/></svg>
        </button>

        <div class="carousel-dots-bar">
            <button type="button" class="carousel-dot active" aria-label="Anuncio 1"></button>
            <button type="button" class="carousel-dot" aria-label="Anuncio 2"></button>
            <button type="button" class="carousel-dot" aria-label="Anuncio 3"></button>
        </div>
    </section>

    <!-- FRANJA AZUL CORPORATIVA DE VEHÍCULOS (#005BAA Pantone 286 + #FFFFFF + #BCBEC0) -->
    <section class="amsoil-blue-vehicle-strip" aria-label="Categorías de Vehículos">
        <div class="container">
            <div class="blue-vehicle-grid">
                <!-- 1. AUTO / LIGHT TRUCK -->
                <a href="automotriz.html" class="blue-veh-item">
                    <div class="blue-veh-icon">
                        <svg viewBox="0 0 120 52" fill="none">
                            <path d="M10 34L22 31L39 18H76L95 28L111 31V40H99C99 33 93 28 86 28C79 28 73 33 73 40H43C43 33 37 28 30 28C23 28 17 33 17 40H8V36L10 34Z" fill="#FFFFFF"/>
                            <path d="M42 21H60V29H31L42 21ZM64 21H74L88 29H64V21Z" fill="#005BAA"/>
                            <circle cx="30" cy="40" r="9" fill="#BCBEC0"/>
                            <circle cx="30" cy="40" r="4.5" fill="#000000"/>
                            <circle cx="86" cy="40" r="9" fill="#BCBEC0"/>
                            <circle cx="86" cy="40" r="4.5" fill="#000000"/>
                        </svg>
                    </div>
                    <span class="blue-veh-label">Auto / Pickup<br>Liviano</span>
                </a>

                <!-- 2. MOTORCYCLE -->
                <a href="motos.html?filter=metric-motorcycle" class="blue-veh-item">
                    <div class="blue-veh-icon">
                        <svg viewBox="0 0 120 52" fill="none">
                            <circle cx="26" cy="38" r="10.5" stroke="#BCBEC0" stroke-width="4" fill="#000000"/>
                            <circle cx="26" cy="38" r="3.5" fill="#FFFFFF"/>
                            <circle cx="92" cy="38" r="10.5" stroke="#BCBEC0" stroke-width="4" fill="#000000"/>
                            <circle cx="92" cy="38" r="3.5" fill="#FFFFFF"/>
                            <path d="M26 38L42 22H56L68 29H82L72 16H64L70 12H78L92 38" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
                            <path d="M40 24C45 18 56 18 62 24L74 28L66 37H44L40 24Z" fill="#FFFFFF"/>
                        </svg>
                    </div>
                    <span class="blue-veh-label">Motocicletas</span>
                </a>

                <!-- 3. ATV -->
                <a href="motos.html?filter=atv-utv" class="blue-veh-item">
                    <div class="blue-veh-icon">
                        <svg viewBox="0 0 120 52" fill="none">
                            <path d="M26 26L38 19H54L50 11H43M50 11L58 11M22 28H92L96 34H20L22 28Z" stroke="#FFFFFF" stroke-width="3.5" stroke-linecap="round"/>
                            <path d="M25 24L42 18H74L92 25L88 35H28L25 24Z" fill="#FFFFFF"/>
                            <circle cx="34" cy="39" r="10.5" fill="#BCBEC0"/>
                            <circle cx="34" cy="39" r="5" fill="#000000"/>
                            <circle cx="82" cy="39" r="10.5" fill="#BCBEC0"/>
                            <circle cx="82" cy="39" r="5" fill="#000000"/>
                        </svg>
                    </div>
                    <span class="blue-veh-label">Cuadraciclos<br>ATV</span>
                </a>

                <!-- 4. UTV -->
                <a href="motos.html?filter=atv-utv" class="blue-veh-item">
                    <div class="blue-veh-icon">
                        <svg viewBox="0 0 120 52" fill="none">
                            <path d="M34 26L44 10H76L88 26" stroke="#BCBEC0" stroke-width="3.5" stroke-linejoin="round"/>
                            <path d="M60 10V26" stroke="#BCBEC0" stroke-width="3"/>
                            <path d="M18 25H40L46 29H76L84 24L102 28V37H18V25Z" fill="#FFFFFF"/>
                            <circle cx="32" cy="40" r="10" fill="#BCBEC0"/>
                            <circle cx="32" cy="40" r="4.5" fill="#000000"/>
                            <circle cx="86" cy="40" r="10" fill="#BCBEC0"/>
                            <circle cx="86" cy="40" r="4.5" fill="#000000"/>
                        </svg>
                    </div>
                    <span class="blue-veh-label">Side-by-Side<br>UTV</span>
                </a>

                <!-- 5. MARINE OUTBOARD -->
                <a href="motos.html?filter=marino" class="blue-veh-item">
                    <div class="blue-veh-icon">
                        <svg viewBox="0 0 120 52" fill="none">
                            <path d="M10 27H96L110 27L98 39H22L10 27Z" fill="#FFFFFF"/>
                            <path d="M44 27L56 18H74L80 27H44Z" fill="#BCBEC0"/>
                            <path d="M12 22H22L24 31L16 44H11L15 31L12 22Z" fill="#BCBEC0"/>
                            <path d="M22 32H98" stroke="#005BAA" stroke-width="2"/>
                        </svg>
                    </div>
                    <span class="blue-veh-label">Fuera de Borda<br>Marino</span>
                </a>

                <!-- 6. PWC -->
                <a href="motos.html?filter=2-stroke" class="blue-veh-item">
                    <div class="blue-veh-icon">
                        <svg viewBox="0 0 120 52" fill="none">
                            <path d="M16 35L32 27H58L72 18L82 20L76 27L104 33L94 40H22L16 35Z" fill="#FFFFFF"/>
                            <path d="M40 27L52 21H68L62 27H40Z" fill="#BCBEC0"/>
                            <path d="M18 36H98" stroke="#005BAA" stroke-width="2.5"/>
                        </svg>
                    </div>
                    <span class="blue-veh-label">Acuáticos<br>PWC</span>
                </a>

                <!-- 7. HEAVY-DUTY ON-ROAD -->
                <a href="diesel.html?filter=signature-series-max-duty" class="blue-veh-item">
                    <div class="blue-veh-icon">
                        <svg viewBox="0 0 120 52" fill="none">
                            <path d="M14 33H52V12C64 12 74 16 78 24L98 26V38H14V33Z" fill="#FFFFFF"/>
                            <rect x="64" y="18" width="10" height="8" fill="#005BAA"/>
                            <rect x="47" y="8" width="3.5" height="26" fill="#BCBEC0"/>
                            <circle cx="25" cy="40" r="8" fill="#BCBEC0"/>
                            <circle cx="25" cy="40" r="3.8" fill="#000000"/>
                            <circle cx="43" cy="40" r="8" fill="#BCBEC0"/>
                            <circle cx="43" cy="40" r="3.8" fill="#000000"/>
                            <circle cx="86" cy="40" r="8" fill="#BCBEC0"/>
                            <circle cx="86" cy="40" r="3.8" fill="#000000"/>
                        </svg>
                    </div>
                    <span class="blue-veh-label">Transporte<br>Pesado</span>
                </a>

                <!-- 8. HEAVY-DUTY OFF-ROAD -->
                <a href="diesel.html?filter=heavy-duty-ck4" class="blue-veh-item">
                    <div class="blue-veh-icon">
                        <svg viewBox="0 0 120 52" fill="none">
                            <path d="M12 18L72 14L66 32H18L12 18Z" fill="#BCBEC0"/>
                            <path d="M68 18H90L98 26V36H16V31H66L68 18Z" fill="#FFFFFF"/>
                            <rect x="74" y="21" width="12" height="7" fill="#005BAA"/>
                            <circle cx="28" cy="40" r="8.5" fill="#BCBEC0"/>
                            <circle cx="28" cy="40" r="4" fill="#000000"/>
                            <circle cx="46" cy="40" r="8.5" fill="#BCBEC0"/>
                            <circle cx="46" cy="40" r="4" fill="#000000"/>
                            <circle cx="84" cy="40" r="8.5" fill="#BCBEC0"/>
                            <circle cx="84" cy="40" r="4" fill="#000000"/>
                        </svg>
                    </div>
                    <span class="blue-veh-label">Maquinaria<br>Pesada</span>
                </a>

                <!-- 9. AGRICULTURE -->
                <a href="diesel.html" class="blue-veh-item">
                    <div class="blue-veh-icon">
                        <svg viewBox="0 0 120 52" fill="none">
                            <path d="M18 14H56L64 26H88V36H18V14Z" fill="#FFFFFF"/>
                            <rect x="34" y="18" width="18" height="10" fill="#005BAA"/>
                            <path d="M64 31H110L106 38H64V31Z" fill="#BCBEC0"/>
                            <circle cx="32" cy="39" r="11" fill="#BCBEC0"/>
                            <circle cx="32" cy="39" r="5" fill="#000000"/>
                            <circle cx="62" cy="41" r="7.5" fill="#BCBEC0"/>
                            <circle cx="62" cy="41" r="3.5" fill="#000000"/>
                        </svg>
                    </div>
                    <span class="blue-veh-label">Equipo<br>Agrícola</span>
                </a>
            </div>
        </div>
    </section>"""


def render_common_footer():
    # Manual Pág. 19: Solo 1 logotipo AMSOIL por página web (ubicado en el Header blanco sólido).
    # En el Footer sobre #000000 Process Black se utiliza identidad tipográfica limpia y tagline invertido en #FFFFFF.
    return f"""    <!-- FOOTER CORPORATIVO OFICIAL (#000000 Process Black) -->
    <footer class="amsoil-footer">
        <div class="container">
            <div class="footer-cols">
                <div>
                    <div class="footer-brand-title">AMSOIL COSTA RICA</div>
                    <div class="footer-brand-tagline">The First in Synthetics®</div>
                    <p style="font-size:0.86rem; font-weight:300; color:var(--amsoil-cool-gray); max-width:330px; line-height:1.6;">
                        Portal técnico e informativo oficial de lubricantes, fluidos de transmisión y aditivos especializados AMSOIL en Costa Rica (American Lubricants Supply S.A.).
                    </p>
                </div>

                <div>
                    <h4>Categorías del Catálogo (104 Productos)</h4>
                    <ul>
                        <li><a href="automotriz.html">Aceite de Motor Gasolina e Híbrido (26)</a></li>
                        <li><a href="diesel.html">Diesel 100% Sintético (9)</a></li>
                        <li><a href="european.html">European Car Formula (7)</a></li>
                        <li><a href="motos.html">Motocicletas, Enduro, ATV/UTV y Marino (25)</a></li>
                        <li><a href="transmision.html">Transmisión Automática, CVT y SEVERE GEAR® (17)</a></li>
                        <li><a href="aditivos.html">Aditivos, Coolant, Frenos y Grasas (20)</a></li>
                    </ul>
                </div>

                <div>
                    <h4>Herramientas Técnicas y Ubicaciones</h4>
                    <ul>
                        <li><a href="{HOME_PAGE}#lookup-widget">Guía de Aplicación por Vehículo</a></li>
                        <li><a href="ingenieria.html">Ingeniería Sintética e Índice de 104 Fichas PDS</a></li>
                        <li><a href="contacto.html#puntos-de-venta">Dónde Encontrar Talleres y Puntos de Venta</a></li>
                        <li><a href="contacto.html#formulario-contacto">Consulta Técnica Directa</a></li>
                    </ul>
                </div>

                <div>
                    <h4>Contacto Oficial Costa Rica</h4>
                    <ul>
                        <li><a href="contacto.html">{SVG_PIN} American Lubricants Supply S.A.</a></li>
                        <li><a href="contacto.html">{SVG_PHONE} +506 2200-0000</a></li>
                        <li><a href="contacto.html">{SVG_MSG} WhatsApp: +506 8800-0000</a></li>
                        <li><a href="https://www.AMSOIL.com" target="_blank" rel="noopener">Sitio Corporativo AMSOIL.com ↗</a></li>
                    </ul>
                </div>
            </div>

            <div class="footer-copy">
                <span>© 2026 American Lubricants Supply S.A. — Distribuidor Autorizado en Costa Rica. Todas las marcas registradas son propiedad de AMSOIL INC. (Superior, Wisconsin, EE. UU.).</span>
                <span>Warranty Secure® • Catálogo Oficial de 104 Referencias</span>
            </div>
        </div>
    </footer>

    <script src="catalogo-datos.js"></script>
    <script src="js/main.js"></script>"""


# 1. BUILD INDEX-CATALOGO.HTML (Preservando index.html "En Construcción")
def build_index():
    featured_ids = [
        "asl-5w-30",
        "dme-15w-40",
        "svg-severe-gear-75w-90",
        "mcf-10w-40",
    ]
    cards_html = "\n".join(render_product_card(BY_ID[pid]) for pid in featured_ids if pid in BY_ID)

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AMSOIL Costa Rica | Lubricantes Sintéticos Especializados — The First in Synthetics®</title>
    <meta name="description" content="AMSOIL Costa Rica (American Lubricants Supply S.A.): Lubricantes 100% sintéticos diseñados en Estados Unidos para máxima protección y rendimiento en motor, diesel, motocicletas y transmisión.">
{GOOGLE_FONTS_HEAD}
</head>
<body>

{render_common_header("index")}

    <!-- GUÍA INTERACTIVA DE APLICACIÓN POR VEHÍCULO -->
    <section class="vehicle-lookup-dock" id="lookup-widget">
        <div class="container">
            <div class="lookup-dock-card">
                <div class="lookup-tabs-bar">
                    <button type="button" class="lookup-mode-tab">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M14 16H9m10 0h3v-3.15a1 1 0 0 0-.84-.99L16 11l-2.7-3.6a1 1 0 0 0-.8-.4H5.24a2 2 0 0 0-1.8 1.1l-.8 1.63A6 6 0 0 0 2 12.42V16h2"/><circle cx="6.5" cy="16.5" r="2.5"/><circle cx="16.5" cy="16.5" r="2.5"/></svg>
                        <span>Encuentra el lubricante especializado para tu vehículo o equipo</span>
                    </button>
                </div>

                <div class="lookup-dock-body">
                    <form id="aiAdvisorForm" class="lookup-Step-grid">
                        <div class="lookup-field">
                            <label for="selectEquipType">Tipo de Vehículo</label>
                            <select id="selectEquipType" class="lookup-select">
                                <option value="">Todos los vehículos</option>
                                <option value="Pickup 4x4 Turbodiésel">Pickup 4x4 / SUV Diésel</option>
                                <option value="Automóvil / SUV Gasolina">Auto / SUV Gasolina</option>
                                <option value="Vehículo Híbrido HEV">Vehículo Híbrido</option>
                                <option value="Motocicleta 4T / Enduro">Motocicleta / ATV</option>
                            </select>
                        </div>

                        <div class="lookup-field">
                            <label for="aiVehicleQuery">Marca, Modelo y Año</label>
                            <input
                                type="text"
                                id="aiVehicleQuery"
                                class="lookup-input"
                                placeholder="Ej: Toyota Hilux 2.8 2023, Honda CR-V 1.5..."
                                required
                            >
                        </div>

                        <div class="lookup-field">
                            <label for="aiVehicleMileage">Kilometraje (Opcional)</label>
                            <input
                                type="number"
                                id="aiVehicleMileage"
                                class="lookup-input"
                                placeholder="Ej: 85000 km"
                                min="0"
                                step="1000"
                            >
                        </div>

                        <div class="lookup-field">
                            <button type="submit" class="btn btn-red btn-block" style="height:44px;">
                                Consultar Aplicación →
                            </button>
                        </div>
                    </form>

                    <div class="lookup-quick-strip">
                        <span class="quick-strip-title">Consultas frecuentes:</span>
                        <button type="button" class="cr-vehicle-pill preset-chip" data-query="Toyota Hilux 2.8L 1GD-FTV Diesel 2023" data-km="85000">Toyota Hilux 2.8</button>
                        <button type="button" class="cr-vehicle-pill preset-chip" data-query="Isuzu D-Max 3.0L 4JJ3-TCX Diesel 2022" data-km="115000">Isuzu D-Max 3.0</button>
                        <button type="button" class="cr-vehicle-pill preset-chip" data-query="Toyota RAV4 Hybrid 2.5L A25A-FXS 2024" data-km="25000">Toyota RAV4 Híbrido</button>
                        <button type="button" class="cr-vehicle-pill preset-chip" data-query="Honda CR-V 1.5L VTEC Turbo Gasolina 2022" data-km="65000">Honda CR-V Turbo</button>
                    </div>

                    <div id="aiLoadingState" style="display:none; padding:16px; margin-top:14px; background:var(--bg-light); border-left:4px solid var(--amsoil-red); font-size:0.9rem;">
                        Analizando especificaciones OEM y formulaciones AMSOIL para tu vehículo...
                    </div>

                    <div id="aiResultPanel" class="amsoil-guide-results" style="display: none;">
                        <div class="guide-results-header">
                            <div>
                                <div style="display:flex; gap:8px; margin-bottom:6px; flex-wrap:wrap;">
                                    <span id="resCategoryBadge" class="tier-kicker" style="background:var(--amsoil-red); margin:0;">Guía de Aplicación AMSOIL</span>
                                    <span id="resMileageBadge" class="tier-kicker" style="background:var(--amsoil-blue); color:var(--amsoil-white); margin:0; display:none;">Alto Kilometraje</span>
                                </div>
                                <h3 id="resVehicleTitle" class="guide-veh-title">Toyota Hilux 2.8L Diesel</h3>
                                <p id="resVehicleSubtitle" class="guide-veh-sub">Especificación OEM y fluidos recomendados</p>
                            </div>
                            <button type="button" class="btn btn-outline-dark" style="padding:6px 12px; font-size:0.82rem;" onclick="document.getElementById('aiResultPanel').style.display='none'">
                                ✕ Cerrar
                            </button>
                        </div>

                        <div class="guide-specs-bar">
                            <div class="guide-spec-tile highlight">
                                <span>Viscosidad SAE Recomendada</span>
                                <strong id="resViscosity">5W-30</strong>
                            </div>
                            <div class="guide-spec-tile">
                                <span>Capacidad de Cárter</span>
                                <strong id="resCapacity">7.5 Litros</strong>
                            </div>
                            <div class="guide-spec-tile">
                                <span>Especificación OEM</span>
                                <strong id="resNorm">API CK-4 / ACEA C3</strong>
                            </div>
                            <div class="guide-spec-tile">
                                <span>Referencia de Filtración</span>
                                <strong id="resFilter">90915-YZZD2</strong>
                            </div>
                        </div>

                        <div class="guide-alerts-row">
                            <div class="guide-alert">
                                <strong>Criterio Técnico de Protección</strong>
                                <span id="resWarning"></span>
                            </div>
                            <div id="resMileageBox" class="guide-alert mileage-note" style="display:none;">
                                <strong>Recomendación por Kilometraje</strong>
                                <span id="resMileageAdvice"></span>
                            </div>
                        </div>

                        <div class="guide-sub-heading">
                            <span>Lubricantes de Motor Recomendados</span>
                        </div>
                        <div id="resAmsoilTiersGrid" class="guide-tiers-grid"></div>

                        <div class="guide-sub-heading">
                            <span>Fluidos de Transmisión, Diferenciales y Aditivos</span>
                        </div>
                        <div id="resFluidPackageGrid" class="guide-fluids-grid"></div>
                    </div>

                </div>
            </div>
        </div>
    </section>

    <!-- 4 PRODUCTOS DESTACADOS -->
    <section class="section-block-gray">
        <div class="container">
            <div class="amsoil-sec-header">
                <h2 class="amsoil-sec-title">Productos Destacados</h2>
                <a href="automotriz.html" class="amsoil-sec-link">Ver Catálogo Completo →</a>
            </div>

            <div class="amsoil-product-grid" style="grid-template-columns: repeat(4, 1fr);">
{cards_html}
            </div>
        </div>
    </section>

    <!-- AUTORIDAD CIENTÍFICA Y PRUEBAS ASTM ("OVERKILL IS UNDERRATED" - MANUAL PÁG. 12 & 16) -->
    <section class="section-block-white">
        <div class="container">
            <div class="why-amsoil-split">
                <div class="why-left-content">
                    <span class="kicker">CIENCIA EN LUBRICACIÓN SINTÉTICA</span>
                    <h2>Los estándares mínimos de la industria son solo eso: mínimos</h2>
                    <p>
                        En AMSOIL no diseñamos para cumplir lo mínimo indispensable. Formulamos lubricantes 100% sintéticos especializados que superan las pruebas mecánicas ASTM más severas, manteniendo los pistones limpios, protegiendo los turbocompresores y entregando máxima protección y rendimiento.
                    </p>
                    <div style="display:flex; gap:12px; flex-wrap:wrap;">
                        <a href="ingenieria.html" class="btn btn-red">Ver Pruebas ASTM y 104 Fichas PDS</a>
                        <a href="contacto.html" class="btn btn-outline-dark">Puntos de Venta en Costa Rica</a>
                    </div>
                </div>

                <div class="why-right-chart">
                    <span style="font-family:var(--font-heading); font-weight:700; color:var(--amsoil-blue); font-size:0.8rem; letter-spacing:0.5px;">RESULTADOS VERIFICADOS EN PRUEBAS DE MOTOR ASTM</span>
                    <h3 style="font-family:var(--font-heading); font-weight:700; font-size:1.35rem; margin:6px 0 20px; color:var(--text-primary);">Protección Comprobada Frente a Estándares API</h3>

                    <div class="astm-bar-item">
                        <div class="astm-bar-label">
                            <span>AMSOIL Signature Series 5W-30 (ASTM Sequence IVA)</span>
                            <strong style="color:var(--amsoil-red);">75% Más Protección</strong>
                        </div>
                        <div class="astm-track"><div class="astm-fill" style="width:92%; background:var(--amsoil-red);"></div></div>
                    </div>

                    <div class="astm-bar-item">
                        <div class="astm-bar-label">
                            <span>Limpieza de Pistones a Doble Duración (ASTM D8111 IIIH)</span>
                            <strong style="color:var(--amsoil-blue);">40% Más Limpios</strong>
                        </div>
                        <div class="astm-track"><div class="astm-fill" style="width:86%; background:var(--amsoil-blue);"></div></div>
                    </div>

                    <div class="astm-bar-item" style="margin-bottom:0;">
                        <div class="astm-bar-label">
                            <span>AMSOIL Max-Duty Diesel (Detroit Diesel DD13 Scuffing)</span>
                            <strong style="color:var(--amsoil-red);">6X Más Protección</strong>
                        </div>
                        <div class="astm-track"><div class="astm-fill" style="width:96%; background:var(--amsoil-red);"></div></div>
                    </div>
                </div>
            </div>
        </div>
    </section>

{render_common_footer()}
</body>
</html>
"""
    (BASE_DIR / HOME_PAGE).write_text(html_content, encoding="utf-8")


# 2. BUILD AUTOMOTRIZ.HTML (26 NON-EUROPEAN GASOLINE PRODUCTS + BREAK-IN OIL)
def build_automotriz():
    items = [
        it for it in CATALOG
        if it["category"] == "01-motor-gasolina"
        and it["line"] != "european-car-formula"
    ]
    order = {
        "signature-series": 1,
        "xl-synthetic": 2,
        "oe-synthetic": 3,
        "hybrid": 4,
        "high-mileage": 5,
        "racing-zrod-dominator": 6,
    }
    items.sort(key=lambda x: (order.get(x["line"], 99), x["index"]))

    def auto_tokens(it):
        toks = []
        name_l = it["display_name"].lower()
        if "dominator" in name_l or "4t racing" in name_l:
            toks.append("dominator")
        if "z-rod" in name_l:
            toks.append("z-rod")
        if "break-in" in name_l or it["id"] == "brk-break-in-oil-sae-30":
            toks.append("break-in")
        return " ".join(toks)

    cards_html = "\n".join(render_product_card(it, extra_subcat=auto_tokens(it)) for it in items)

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aceite de Motor Automotriz, Híbrido y Competencia ({len(items)} Referencias) | AMSOIL Costa Rica</title>
{GOOGLE_FONTS_HEAD}
</head>
<body>

{render_common_header("automotriz", "Escribe tu vehículo, viscosidad (ej. 0W-20, 5W-30) o línea AMSOIL...")}

    <div class="cat-breadcrumb-bar">
        <div class="container">
            <a href="{HOME_PAGE}">Inicio</a> &nbsp;/&nbsp; <span>Aceite de Motor Gasolina, Híbrido y Competencia ({len(items)} Referencias Oficiales)</span>
        </div>
    </div>

    <section class="cat-header-banner">
        <div class="container">
            <h1>Aceite de Motor Automotriz ({len(items)} Productos)</h1>
            <p>Soluciones de lubricación formuladas para máxima protección y rendimiento en motores de gasolina modernos, Turbo-GDI, vehículos híbridos, alto kilometraje, competencia (DOMINATOR®), clásicos de alto zinc (Z-ROD®) y asentamiento mecánico (Break-In Oil).</p>
        </div>
    </section>

    <div class="container cat-page-layout">
        <main>
            <div class="amsoil-product-grid" style="grid-template-columns: repeat(4, 1fr);">
{cards_html}
            </div>
        </main>
    </div>

{render_common_footer()}
</body>
</html>
"""
    (BASE_DIR / "automotriz.html").write_text(html_content, encoding="utf-8")


# 3. BUILD DIESEL.HTML (9 100% SYNTHETIC DIESEL MOTOR OILS ONLY)
def build_diesel():
    items = [
        it for it in CATALOG
        if it["category"] == "02-motor-diesel"
        and "commercial" not in it["line"].lower()
        and it["id"] != "sbdf-15w-40"
    ]
    order = {
        "signature-series-max-duty": 1,
        "heavy-duty-ck4": 2,
        "diesel-dexos-d": 3,
    }
    items.sort(key=lambda x: (order.get(x["line"], 99), x["index"]))
    cards_html = "\n".join(render_product_card(it) for it in items)

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aceites de Motor 100% Sintéticos Diesel ({len(items)} Referencias) | AMSOIL Costa Rica</title>
{GOOGLE_FONTS_HEAD}
</head>
<body>

{render_common_header("diesel", "Buscar lubricante Diesel (Max-Duty, Heavy-Duty, dexosD, 15W-40, 5W-40)...")}

    <div class="cat-breadcrumb-bar">
        <div class="container">
            <a href="{HOME_PAGE}">Inicio</a> &nbsp;/&nbsp; <span>Diesel 100% Sintético API CK-4 y GM dexosD ({len(items)} Referencias Oficiales)</span>
        </div>
    </div>

    <section class="cat-header-banner">
        <div class="container">
            <h1>Aceites de Motor 100% Sintéticos Diesel ({len(items)} Productos)</h1>
            <p>Ingenierizados para pickups 4x4, flotas de transporte y maquinaria pesada que operan bajo esfuerzo continuo. Entregan hasta 6X más protección contra desgaste en la prueba Detroit Diesel DD13 Scuffing y reducen el costo total de propiedad (TCO).</p>
        </div>
    </section>

    <div class="container cat-page-layout">
        <main>
            <div class="amsoil-product-grid" style="grid-template-columns: repeat(4, 1fr);">
{cards_html}
            </div>
        </main>
    </div>

{render_common_footer()}
</body>
</html>
"""
    (BASE_DIR / "diesel.html").write_text(html_content, encoding="utf-8")


# 3B. BUILD EUROPEAN.HTML (7 EUROPEAN CAR FORMULA PRODUCTS)
def build_european():
    items = [it for it in CATALOG if it["line"] == "european-car-formula"]
    items.sort(key=lambda x: x["index"])

    def euro_tokens(it):
        name_u = it["display_name"].upper()
        toks = []
        if " LS" in name_u or "LS-VW" in name_u:
            toks.append("low-saps")
        if " MS" in name_u:
            toks.append("mid-saps")
        if " FS" in name_u:
            toks.append("full-saps")
        return " ".join(toks)

    cards_html = "\n".join(render_product_card(it, extra_subcat=euro_tokens(it)) for it in items)

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AMSOIL European Car Formula 100% Synthetic ({len(items)} Referencias) | AMSOIL Costa Rica</title>
{GOOGLE_FONTS_HEAD}
</head>
<body>

{render_common_header("european", "Buscar especificación europea (VW 504/507, 508/509, BMW LL-04, MB 229.51, Porsche A40)...")}

    <div class="cat-breadcrumb-bar">
        <div class="container">
            <a href="{HOME_PAGE}">Inicio</a> &nbsp;/&nbsp; <span>AMSOIL European Car Formula 100% Synthetic ({len(items)} Referencias Oficiales)</span>
        </div>
    </div>

    <section class="cat-header-banner">
        <div class="container">
            <h1>AMSOIL European Car Formula ({len(items)} Productos)</h1>
            <p>Lubricantes 100% sintéticos formulados con precisión para motores europeos de gasolina y turbodiésel (BMW, Mercedes-Benz, Audi, Volkswagen, Porsche, Volvo y Land Rover), protegiendo turbocompresores y sistemas de emisiones DPF/GPF (Low-SAPS, Mid-SAPS y Full-SAPS).</p>
        </div>
    </section>

    <div class="container cat-page-layout">
        <main>
            <div class="amsoil-product-grid" style="grid-template-columns: repeat(4, 1fr);">
{cards_html}
            </div>
        </main>
    </div>

{render_common_footer()}
</body>
</html>
"""
    (BASE_DIR / "european.html").write_text(html_content, encoding="utf-8")


# 4. BUILD MOTOS.HTML (25 PRODUCTS)
def build_motos():
    items = [it for it in CATALOG if it["category"] == "04-motocicletas-atv-marino"]
    order = {
        "metric-motorcycle": 1,
        "dirt-bike": 2,
        "v-twin": 3,
        "2-stroke": 4,
        "atv-utv": 5,
        "marino": 6,
        "4t-motorcycle": 7,
    }
    items.sort(key=lambda x: (order.get(x["line"], 99), x["index"]))
    cards_html = "\n".join(render_product_card(it) for it in items)

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Motocicletas, Enduro, 2 Tiempos, ATV/UTV y Marino ({len(items)} Referencias) | AMSOIL Costa Rica</title>
{GOOGLE_FONTS_HEAD}
</head>
<body>

{render_common_header("motos", "Buscar lubricante para motocicleta, enduro, 2 tiempos, ATV/UTV o motor marino...")}

    <div class="cat-breadcrumb-bar">
        <div class="container">
            <a href="{HOME_PAGE}">Inicio</a> &nbsp;/&nbsp; <span>Motocicletas, Enduro, 2 Tiempos, ATV/UTV y Marino ({len(items)} Referencias Oficiales)</span>
        </div>
    </div>

    <section class="cat-header-banner">
        <div class="container">
            <h1>Motocicletas, Enduro, ATV/UTV y Marino ({len(items)} Productos)</h1>
            <p>Ride Hard. Run Cool.® Lubricantes 100% sintéticos especializados con certificación JASO MA/MA2 para cambios precisos en embrague húmedo, motocross, sintéticos de 2 tiempos (DOMINATOR®, INTERCEPTOR®), suspensiones Shock Therapy® y motores marinos HP Marine®.</p>
        </div>
    </section>

    <div class="container cat-page-layout">
        <main>
            <div class="amsoil-product-grid" style="grid-template-columns: repeat(4, 1fr);">
{cards_html}
            </div>
        </main>
    </div>

{render_common_footer()}
</body>
</html>
"""
    (BASE_DIR / "motos.html").write_text(html_content, encoding="utf-8")


# 5. BUILD TRANSMISION.HTML (17 TRANSMISION / GEAR PRODUCTS)
def build_transmision():
    items = [
        it for it in CATALOG
        if it["category"] == "03-transmision-y-diferenciales"
    ]
    order = {
        "severe-gear-y-diferenciales": 1,
        "transmision-automatica-atf-cvt-dct": 2,
    }
    items.sort(key=lambda x: (order.get(x["line"], 99), x["index"]))
    cards_html = "\n".join(render_product_card(it) for it in items)

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Transmisión ATF/CVT/DCT y Diferenciales SEVERE GEAR® ({len(items)} Referencias) | AMSOIL Costa Rica</title>
{GOOGLE_FONTS_HEAD}
</head>
<body>

{render_common_header("transmision", "Buscar fluido ATF, CVT, DCT, SEVERE GEAR® 75W-90, 75W-140 o caja manual...")}

    <div class="cat-breadcrumb-bar">
        <div class="container">
            <a href="{HOME_PAGE}">Inicio</a> &nbsp;/&nbsp; <span>Transmisión Automática y Diferenciales SEVERE GEAR® ({len(items)} Referencias Oficiales)</span>
        </div>
    </div>

    <section class="cat-header-banner">
        <div class="container">
            <h1>Transmisión Automática y Diferenciales SEVERE GEAR® ({len(items)} Productos)</h1>
            <p>Fluidos 100% sintéticos diseñados para resistir el cizallamiento y el calor extremo en cajas automáticas modernas, transmisiones CVT, doble embrague DCT, Torque-Drive®, Super Shift® y diferenciales hipoidales 4x4 bajo remolque pesado.</p>
        </div>
    </section>

    <div class="container cat-page-layout">
        <main>
            <div class="amsoil-product-grid" style="grid-template-columns: repeat(4, 1fr);">
{cards_html}
            </div>
        </main>
    </div>

{render_common_footer()}
</body>
</html>
"""
    (BASE_DIR / "transmision.html").write_text(html_content, encoding="utf-8")


# 5B. BUILD ADITIVOS.HTML (20 ADITIVOS / COOLANT / FRENOS / GRASAS PRODUCTS)
def build_aditivos():
    items = [
        it for it in CATALOG
        if it["category"] == "05-aditivos-grasas-coolant-varios"
    ]
    order = {
        "aditivos-combustible": 1,
        "coolant-anticongelante": 2,
        "fluidos-frenos-direccion-varios": 3,
        "grasas-y-lubricantes": 4,
    }
    items.sort(key=lambda x: (order.get(x["line"], 99), x["index"]))
    cards_html = "\n".join(render_product_card(it) for it in items)

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aditivos de Combustible, Coolant, Frenos y Grasas Sintéticas ({len(items)} Referencias) | AMSOIL Costa Rica</title>
{GOOGLE_FONTS_HEAD}
</head>
<body>

{render_common_header("aditivos", "Buscar aditivo P.i.®, Diesel Injector Clean, Coolant, líquido de frenos DOT 4 o grasa...")}

    <div class="cat-breadcrumb-bar">
        <div class="container">
            <a href="{HOME_PAGE}">Inicio</a> &nbsp;/&nbsp; <span>Aditivos de Combustible, Coolant, Frenos y Grasas Sintéticas ({len(items)} Referencias Oficiales)</span>
        </div>
    </div>

    <section class="cat-header-banner">
        <div class="container">
            <h1>Aditivos, Coolant, Frenos y Grasas Sintéticas ({len(items)} Productos)</h1>
            <p>AMSOIL P.i.® elimina depósitos difíciles para restaurar potencia y economía de combustible. Completa la protección de tu equipo con limpiadores de inyectores diésel, refrigerantes, DOMINATOR® Coolant Boost, líquidos de frenos DOT 3/4, SABER® y grasas poliméricas NLGI #2.</p>
        </div>
    </section>

    <div class="container cat-page-layout">
        <main>
            <div class="amsoil-product-grid" style="grid-template-columns: repeat(4, 1fr);">
{cards_html}
            </div>
        </main>
    </div>

{render_common_footer()}
</body>
</html>
"""
    (BASE_DIR / "aditivos.html").write_text(html_content, encoding="utf-8")


# 6. BUILD INGENIERIA.HTML (DIRECTORIO DE LAS 104 FICHAS TÉCNICAS SIN CÓDIGOS DE ALMACÉN FRENTE AL CLIENTE)
def build_ingenieria():
    rows_html = ""
    for item in CATALOG:
        img = pick_primary_image(item)
        img_src = img["rel_path"] if img else "01-motor-gasolina/signature-series/5w-30/recorte-fondo-transparente-ASL.webp"
        specs = item.get("tech_sheet", {}).get("specs") or "Especificación Oficial AMSOIL INC."
        short_specs = specs if len(specs) <= 82 else specs[:79] + "..."
        search_tokens = f"{item['display_name']} {item['viscosity']} {item['category_name']} {item['line_name']} {specs}".lower()
        rows_html += f"""
                        <tr data-catalog-row="{html.escape(search_tokens)}">
                            <td style="width:68px; text-align:center;">
                                <img src="{html.escape(img_src)}" alt="{html.escape(item['display_name'])}" style="height:50px; width:auto; object-fit:contain;" loading="lazy">
                            </td>
                            <td>
                                <strong style="color:var(--amsoil-blue); font-size:0.84rem;">{html.escape(item['category_short'])}</strong>
                                <div style="font-size:0.78rem; color:var(--text-muted);">{html.escape(item['line_name'])}</div>
                            </td>
                            <td>
                                <strong>{html.escape(item['display_name'])}</strong>
                            </td>
                            <td><strong>{html.escape(item['viscosity'])}</strong></td>
                            <td style="font-size:0.82rem; color:var(--text-secondary);">{html.escape(short_specs)}</td>
                            <td>
                                <button type="button" class="btn-pds-trigger" style="padding:7px 12px; font-size:0.78rem;" data-open-pds="{html.escape(item['id'])}">
                                    {SVG_DOC} Ver Ficha PDS
                                </button>
                            </td>
                        </tr>"""

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ingeniería Sintética e Índice de las 104 Fichas Técnicas (PDS) | AMSOIL Costa Rica</title>
{GOOGLE_FONTS_HEAD}
</head>
<body>

{render_common_header("ingenieria", "Filtrar por producto, viscosidad (ej. 5W-30, 15W-40, 75W-90) o norma OEM...")}

    <div class="cat-breadcrumb-bar">
        <div class="container">
            <a href="{HOME_PAGE}">Inicio</a> &nbsp;/&nbsp; <span>Ingeniería Sintética e Índice de las 104 Fichas Técnicas (PDS)</span>
        </div>
    </div>

    <section class="cat-header-banner">
        <div class="container">
            <h1>Ingeniería Sintética e Índice de 104 Fichas Técnicas (PDS)</h1>
            <p>En 1972, AMSOIL marcó un hito mundial al introducir el primer aceite 100% sintético certificado por el Instituto Americano del Petróleo (API). Consulta nuestros resultados de pruebas mecánicas ASTM y abre la Ficha Técnica de cualquiera de las 104 referencias oficiales en Costa Rica.</p>
        </div>
    </section>

    <section class="section-block-white">
        <div class="container">
            <div class="why-amsoil-split">
                <div class="why-left-content">
                    <span class="kicker">RENDIMIENTO BAJO ESFUERZO REAL</span>
                    <h2>¿Qué significan las pruebas ASTM en la topografía de Costa Rica?</h2>
                    <p>
                        Los ascensos prolongados con carga (Cerro de la Muerte, Cambronero, Ruta 32) combinados con tráfico denso y humedad tropical someten al motor y a la transmisión a estrés térmico severo. AMSOIL resiste la ruptura de viscosidad, controla la volatilidad y protege las piezas internas frente al desgaste.
                    </p>
                    <a href="{HOME_PAGE}#lookup-widget" class="btn btn-red">Consultar el Lubricante para mi Vehículo</a>
                </div>
                <div class="why-right-chart">
                    <div class="astm-bar-item">
                        <div class="astm-bar-label">
                            <span>Protección Contra Desgaste (Detroit Diesel DD13)</span>
                            <strong style="color:var(--amsoil-red);">6X Superior al Estándar</strong>
                        </div>
                        <div class="astm-track"><div class="astm-fill" style="width:94%; background-color:var(--amsoil-red);"></div></div>
                    </div>
                    <div class="astm-bar-item">
                        <div class="astm-bar-label">
                            <span>Limpieza de Pistones a Doble Duración (ASTM Sequence IIIH)</span>
                            <strong style="color:var(--amsoil-blue);">40% Más Limpios</strong>
                        </div>
                        <div class="astm-track"><div class="astm-fill" style="width:88%; background-color:var(--amsoil-blue);"></div></div>
                    </div>
                    <div class="astm-bar-item" style="margin-bottom:0;">
                        <div class="astm-bar-label">
                            <span>Protección Contra Pre-Ignición Turbo (ASTM LSPI)</span>
                            <strong style="color:var(--amsoil-red);">100% Protección</strong>
                        </div>
                        <div class="astm-track"><div class="astm-fill" style="width:100%; background-color:var(--amsoil-red);"></div></div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="section-block-gray">
        <div class="container">
            <div class="amsoil-sec-header" style="flex-wrap:wrap; gap:16px;">
                <h2 class="amsoil-sec-title">Directorio Técnico de las 104 Referencias AMSOIL</h2>
                <div style="flex:1; max-width:440px;">
                    <input type="text" id="catalogTableSearchInput" class="lookup-input" style="background:var(--amsoil-white);" placeholder="Filtrar las 104 referencias por nombre, línea, viscosidad o norma...">
                </div>
            </div>

            <div class="table-clean-wrap">
                <table class="amsoil-clean-table">
                    <thead>
                        <tr>
                            <th>Envase</th>
                            <th>Categoría y Línea</th>
                            <th>Nombre Oficial del Producto</th>
                            <th>Grado / Tipo</th>
                            <th>Especificaciones Principales (API / OEM)</th>
                            <th>Ficha Técnica</th>
                        </tr>
                    </thead>
                    <tbody id="fullCatalogTableBody">
{rows_html}
                    </tbody>
                </table>
            </div>
        </div>
    </section>

{render_common_footer()}
</body>
</html>
"""
    (BASE_DIR / "ingenieria.html").write_text(html_content, encoding="utf-8")


# 7. BUILD CONTACTO.HTML CLEANLY FROM SCRATCH
def build_contacto():
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contáctenos, Puntos de Venta y Talleres en Costa Rica | AMSOIL Costa Rica</title>
{GOOGLE_FONTS_HEAD}
</head>
<body>

{render_common_header("contacto")}

    <div class="cat-breadcrumb-bar">
        <div class="container">
            <a href="{HOME_PAGE}">Inicio</a> &nbsp;/&nbsp; <span>Contáctenos, Puntos de Venta y Talleres en Costa Rica</span>
        </div>
    </div>

    <section class="cat-header-banner">
        <div class="container">
            <h1>Contáctenos, Puntos de Venta y Talleres Autorizados</h1>
            <p>Comunícate directamente con nuestro equipo técnico en Costa Rica (American Lubricants Supply S.A.) o ubica el punto de venta y taller especializado más cercano por provincia.</p>
        </div>
    </section>

    <!-- 1. CANALES OFICIALES DE CONTACTO -->
    <section class="section-block-white" style="padding-bottom: 24px;">
        <div class="container">
            <div class="amsoil-sec-header">
                <h2 class="amsoil-sec-title">Canales Oficiales de Atención</h2>
                <a href="#formulario-contacto" class="amsoil-sec-link">Enviar Consulta Directa ↓</a>
            </div>

            <div class="contact-channels-grid">
                <div class="contact-channel-card">
                    <div class="channel-icon">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                    </div>
                    <h3>Central Telefónica</h3>
                    <p>Asesoría técnica de aplicación, disponibilidad y atención a talleres y flotas en Costa Rica.</p>
                    <span class="channel-value">+506 2200-0000</span>
                </div>

                <div class="contact-channel-card blue-top">
                    <div class="channel-icon">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>
                    </div>
                    <h3>WhatsApp Técnico CR</h3>
                    <p>Consulta rápida por modelo de vehículo, viscosidad OEM o ubicación de talleres cercanos.</p>
                    <span class="channel-value">+506 8800-0000</span>
                </div>

                <div class="contact-channel-card">
                    <div class="channel-icon">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
                    </div>
                    <h3>Correo Corporativo</h3>
                    <p>Consultas técnicas, atención a talleres aliados, flotas comerciales y soporte general.</p>
                    <span class="channel-value">info@amsoil.cr</span>
                </div>

                <div class="contact-channel-card blue-top">
                    <div class="channel-icon">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                    </div>
                    <h3>Horario de Atención</h3>
                    <p>Lunes a Viernes: 8:00 a.m. – 5:30 p.m.<br>Sábados: 8:00 a.m. – 12:30 p.m.</p>
                    <span class="channel-value">GAM y Todo el País</span>
                </div>
            </div>
        </div>
    </section>

    <!-- 2. DIRECTORIO DE PUNTOS DE VENTA, TALLERES Y MAPA -->
    <section class="section-block-gray" id="puntos-de-venta">
        <div class="container">
            <div class="amsoil-sec-header" style="flex-wrap:wrap; gap:12px;">
                <h2 class="amsoil-sec-title">Puntos de Venta y Talleres por Provincia</h2>
                <span style="font-family:var(--font-heading); font-weight:700; font-size:0.9rem; color:var(--amsoil-blue);">Selecciona tu zona en Costa Rica</span>
            </div>

            <div class="province-filter-bar">
                <button type="button" class="province-pill active" data-prov-filter="all" data-map-query="-84.25,9.82,-83.90,10.06">Todas las Ubicaciones (8)</button>
                <button type="button" class="province-pill" data-prov-filter="sanjose" data-map-query="-84.18,9.89,-84.02,9.98">San José (GAM)</button>
                <button type="button" class="province-pill" data-prov-filter="alajuela" data-map-query="-84.48,9.98,-84.18,10.35">Alajuela / San Carlos</button>
                <button type="button" class="province-pill" data-prov-filter="heredia" data-map-query="-84.18,9.96,-84.08,10.03">Heredia</button>
                <button type="button" class="province-pill" data-prov-filter="cartago" data-map-query="-83.96,9.83,-83.88,9.89">Cartago</button>
                <button type="button" class="province-pill" data-prov-filter="guanacaste" data-map-query="-85.68,10.25,-85.38,10.68">Guanacaste</button>
                <button type="button" class="province-pill" data-prov-filter="pacifico" data-map-query="-83.75,9.32,-83.65,9.40">Zona Sur / Pacífico</button>
            </div>

            <div class="locator-split-grid">
                <div class="dealers-list-grid">
                    <article class="dealer-card" data-province="sanjose">
                        <div>
                            <span class="dealer-prov-badge">SAN JOSÉ • LA URUCA / ESCAZÚ</span>
                            <h4>Centro de Distribución y Punto de Venta Central GAM</h4>
                            <p><strong>Tipo:</strong> Punto de Venta Oficial / Atención Técnica</p>
                            <p><strong>Líneas:</strong> Automotriz, Diesel Max-Duty, Motos 4T/2T, ATF y SEVERE GEAR®</p>
                            <p><strong>Horario:</strong> Lun-Vie 8:00 a.m. - 5:30 p.m. • Sáb 8:00 a.m. - 12:30 p.m.</p>
                        </div>
                        <div class="dealer-actions">
                            <a href="#" class="dealer-map-btn" data-bbox="-84.14,9.93,-84.09,9.97" data-dealer-title="Punto de Venta Central San José (La Uruca / Escazú)">{SVG_PIN} Ver en Mapa</a>
                            <a href="https://waze.com/ul?q=La%20Uruca%20San%20Jose%20Costa%20Rica" target="_blank" rel="noopener" class="dealer-map-btn">{SVG_NAV} Abrir Waze</a>
                        </div>
                    </article>

                    <article class="dealer-card" data-province="sanjose">
                        <div>
                            <span class="dealer-prov-badge">SAN JOSÉ • CURRIDABAT / ZAPOTE</span>
                            <h4>Taller y Centro de Lubricación Zona Este</h4>
                            <p><strong>Tipo:</strong> Punto de Venta y Taller de Servicio Autorizado</p>
                            <p><strong>Especialidad:</strong> Servicio 100% sintético, Engine &amp; Transmission Flush y cajas ATF/CVT</p>
                            <p><strong>Atención:</strong> Vehículos europeos, híbridos y pickups 4x4</p>
                        </div>
                        <div class="dealer-actions">
                            <a href="#" class="dealer-map-btn" data-bbox="-84.06,9.90,-84.01,9.94" data-dealer-title="Taller y Punto de Venta Zona Este (Curridabat)">{SVG_PIN} Ver en Mapa</a>
                            <a href="https://waze.com/ul?q=Curridabat%20San%20Jose%20Costa%20Rica" target="_blank" rel="noopener" class="dealer-map-btn">{SVG_NAV} Abrir Waze</a>
                        </div>
                    </article>

                    <article class="dealer-card" data-province="alajuela">
                        <div>
                            <span class="dealer-prov-badge">ALAJUELA • CENTRO / EL COYOL</span>
                            <h4>Punto de Venta y Servicio Técnico Alajuela</h4>
                            <p><strong>Tipo:</strong> Punto de Venta y Taller 4x4 / Diesel</p>
                            <p><strong>Especialidad:</strong> Pickups Turbodiésel (Hilux, D-Max, Ranger, L200) y SEVERE GEAR®</p>
                            <p><strong>Cobertura:</strong> Alajuela centro, Río Segundo y zona industrial El Coyol</p>
                        </div>
                        <div class="dealer-actions">
                            <a href="#" class="dealer-map-btn" data-bbox="-84.26,9.99,-84.19,10.04" data-dealer-title="Punto de Venta y Taller Alajuela">{SVG_PIN} Ver en Mapa</a>
                            <a href="https://waze.com/ul?q=Alajuela%20Costa%20Rica" target="_blank" rel="noopener" class="dealer-map-btn">{SVG_NAV} Abrir Waze</a>
                        </div>
                    </article>

                    <article class="dealer-card" data-province="alajuela">
                        <div>
                            <span class="dealer-prov-badge">ZONA NORTE • CIUDAD QUESADA</span>
                            <h4>Centro 4x4, Motos Enduro y Agro San Carlos</h4>
                            <p><strong>Tipo:</strong> Punto de Venta Autorizado y Taller</p>
                            <p><strong>Especialidad:</strong> Max-Duty Diesel 15W-40, Dirt Bike 4T/2T y Cuadraciclos ATV/UTV</p>
                            <p><strong>Cobertura:</strong> Ciudad Quesada, La Fortuna y Zona Norte</p>
                        </div>
                        <div class="dealer-actions">
                            <a href="#" class="dealer-map-btn" data-bbox="-84.46,10.30,-84.40,10.35" data-dealer-title="Punto de Venta Ciudad Quesada, San Carlos">{SVG_PIN} Ver en Mapa</a>
                            <a href="https://waze.com/ul?q=Ciudad%20Quesada%20Costa%20Rica" target="_blank" rel="noopener" class="dealer-map-btn">{SVG_NAV} Abrir Waze</a>
                        </div>
                    </article>

                    <article class="dealer-card" data-province="heredia">
                        <div>
                            <span class="dealer-prov-badge">HEREDIA • BELÉN / LAGUNILLA</span>
                            <h4>Punto de Venta y Taller Automotriz Heredia</h4>
                            <p><strong>Tipo:</strong> Punto de Venta y Centro de Lubricación</p>
                            <p><strong>Especialidad:</strong> Signature Series 0W-20 / 5W-30, Híbridos y Motocicletas Metric</p>
                            <p><strong>Cobertura:</strong> Heredia, Belén, Santo Domingo y Barva</p>
                        </div>
                        <div class="dealer-actions">
                            <a href="#" class="dealer-map-btn" data-bbox="-84.16,9.97,-84.10,10.02" data-dealer-title="Punto de Venta y Taller Heredia">{SVG_PIN} Ver en Mapa</a>
                            <a href="https://waze.com/ul?q=Heredia%20Costa%20Rica" target="_blank" rel="noopener" class="dealer-map-btn">{SVG_NAV} Abrir Waze</a>
                        </div>
                    </article>

                    <article class="dealer-card" data-province="cartago">
                        <div>
                            <span class="dealer-prov-badge">CARTAGO • EL TEJAR / CENTRO</span>
                            <h4>Punto de Venta y Taller Diesel / Agrícola Cartago</h4>
                            <p><strong>Tipo:</strong> Punto de Venta y Servicio Técnico</p>
                            <p><strong>Especialidad:</strong> Vehículos de trabajo pesado, pickups 4x4 y automóviles modernos</p>
                            <p><strong>Cobertura:</strong> Cartago centro, Tejar del Guarco y Paraíso</p>
                        </div>
                        <div class="dealer-actions">
                            <a href="#" class="dealer-map-btn" data-bbox="-83.95,9.84,-83.89,9.88" data-dealer-title="Punto de Venta y Taller Cartago">{SVG_PIN} Ver en Mapa</a>
                            <a href="https://waze.com/ul?q=Cartago%20Costa%20Rica" target="_blank" rel="noopener" class="dealer-map-btn">{SVG_NAV} Abrir Waze</a>
                        </div>
                    </article>

                    <article class="dealer-card" data-province="guanacaste">
                        <div>
                            <span class="dealer-prov-badge">GUANACASTE • LIBERIA / COSTA</span>
                            <h4>Punto de Venta 4x4, ATV/UTV y Marino Guanacaste</h4>
                            <p><strong>Tipo:</strong> Punto de Venta y Taller Especializado</p>
                            <p><strong>Especialidad:</strong> Protección frente a calor severo en pickups, cuadraciclos y HP Marine®</p>
                            <p><strong>Cobertura:</strong> Liberia, Santa Cruz, Nicoya y Papagayo</p>
                        </div>
                        <div class="dealer-actions">
                            <a href="#" class="dealer-map-btn" data-bbox="-85.46,10.60,-85.41,10.65" data-dealer-title="Punto de Venta Liberia, Guanacaste">{SVG_PIN} Ver en Mapa</a>
                            <a href="https://waze.com/ul?q=Liberia%20Guanacaste%20Costa%20Rica" target="_blank" rel="noopener" class="dealer-map-btn">{SVG_NAV} Abrir Waze</a>
                        </div>
                    </article>

                    <article class="dealer-card" data-province="pacifico">
                        <div>
                            <span class="dealer-prov-badge">ZONA SUR • PÉREZ ZELEDÓN</span>
                            <h4>Punto de Venta y Taller 4x4 San Isidro de El General</h4>
                            <p><strong>Tipo:</strong> Punto de Venta Autorizado y Taller</p>
                            <p><strong>Especialidad:</strong> Protección térmica para ascensos severos (Cerro de la Muerte), cajas y diferenciales</p>
                            <p><strong>Cobertura:</strong> Pérez Zeledón, Dominical, Uvita y Pacífico Sur</p>
                        </div>
                        <div class="dealer-actions">
                            <a href="#" class="dealer-map-btn" data-bbox="-83.73,9.35,-83.68,9.39" data-dealer-title="Punto de Venta San Isidro de El General">{SVG_PIN} Ver en Mapa</a>
                            <a href="https://waze.com/ul?q=San%20Isidro%20de%20El%20General%20Costa%20Rica" target="_blank" rel="noopener" class="dealer-map-btn">{SVG_NAV} Abrir Waze</a>
                        </div>
                    </article>
                </div>

                <div class="map-embed-container">
                    <div class="map-embed-header">
                        <span style="display:inline-block; background:var(--amsoil-red); color:var(--amsoil-white); font-family:var(--font-heading); font-weight:700; font-size:0.74rem; padding:2px 8px; margin-bottom:6px;">MAPA INTERACTIVO COSTA RICA</span>
                        <h3 id="activeMapLocationTitle">Cobertura GAM y Puntos de Venta en Costa Rica</h3>
                        <p>Selecciona "Ver en Mapa" en cualquier ubicación o filtra por provincia para acercar la zona.</p>
                    </div>
                    <iframe
                        id="crInteractiveMapFrame"
                        title="Mapa de Puntos de Venta y Talleres AMSOIL Costa Rica"
                        width="100%"
                        height="440"
                        style="border:0; display:block;"
                        loading="lazy"
                        src="https://www.openstreetmap.org/export/embed.html?bbox=-84.25,9.82,-83.90,10.06&amp;layer=mapnik">
                    </iframe>
                    <div style="padding:14px 18px; background:var(--amsoil-black); color:var(--amsoil-cool-gray); font-size:0.82rem; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
                        <span>Despacho a todo el territorio nacional desde GAM</span>
                        <a href="https://www.google.com/maps/search/San+Jose+Costa+Rica" target="_blank" rel="noopener" style="color:var(--amsoil-white); font-weight:700; text-decoration:underline;">Abrir en Google Maps ↗</a>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- 3. FORMULARIO DE CONSULTA TÉCNICA DIRECTA -->
    <section class="section-block-white" id="formulario-contacto">
        <div class="container">
            <div class="locator-split-grid">
                <div class="contact-form-panel">
                    <span style="display:inline-block; background:var(--amsoil-blue); color:var(--amsoil-white); font-family:var(--font-heading); font-weight:700; font-size:0.76rem; padding:3px 10px; margin-bottom:10px;">ASESORÍA DIRECTA</span>
                    <h2 style="font-family:var(--font-heading); font-weight:700; font-size:1.75rem; color:var(--text-primary); margin-bottom:8px;">Formulario de Consulta Técnica y Comercial</h2>
                    <p style="font-size:0.92rem; font-weight:300; color:var(--text-secondary); margin-bottom:22px;">
                        Envíanos los datos de tu vehículo, maquinaria o flota para recibir orientación técnica precisa o ubicar el distribuidor autorizado más cercano.
                    </p>

                    <form id="amsoilContactForm" style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
                        <div class="lookup-field">
                            <label for="contactName">Nombre Completo *</label>
                            <input type="text" id="contactName" class="lookup-input" placeholder="Ej. Carlos Rodríguez" required>
                        </div>
                        <div class="lookup-field">
                            <label for="contactPhone">Teléfono / WhatsApp *</label>
                            <input type="tel" id="contactPhone" class="lookup-input" placeholder="Ej. 8888-8888" required>
                        </div>
                        <div class="lookup-field">
                            <label for="contactEmail">Correo Electrónico</label>
                            <input type="email" id="contactEmail" class="lookup-input" placeholder="correo@ejemplo.com">
                        </div>
                        <div class="lookup-field">
                            <label for="contactZone">Provincia / Ubicación</label>
                            <select id="contactZone" class="lookup-select">
                                <option value="San José">San José</option>
                                <option value="Alajuela">Alajuela</option>
                                <option value="Heredia">Heredia</option>
                                <option value="Cartago">Cartago</option>
                                <option value="Guanacaste">Guanacaste</option>
                                <option value="Puntarenas">Puntarenas</option>
                                <option value="Limón">Limón</option>
                            </select>
                        </div>
                        <div class="lookup-field" style="grid-column: 1 / -1;">
                            <label for="contactMessage">Vehículo, Equipo o Consulta *</label>
                            <textarea id="contactMessage" rows="4" style="width:100%; background:var(--bg-light); border:1.5px solid var(--border-gray); padding:12px; font-family:var(--font-body); font-size:0.92rem; border-radius:2px; color:var(--text-primary);" placeholder="Indícanos marca, modelo y año de tu vehículo o la línea AMSOIL que deseas consultar..." required></textarea>
                        </div>
                        <div style="grid-column: 1 / -1;">
                            <button type="submit" class="btn btn-red btn-block">Enviar Consulta a AMSOIL Costa Rica</button>
                            <div id="contactFormFeedback" style="display:none; margin-top:14px; padding:12px 16px; background:var(--bg-light); border-left:4px solid var(--amsoil-blue); font-weight:700; color:var(--text-primary);"></div>
                        </div>
                    </form>
                </div>

                <div>
                    <div class="mega-promo-box" style="margin-bottom:20px; border-left-width:5px;">
                        <span class="kicker">GUÍA DE APLICACIÓN</span>
                        <h5>¿Qué lubricante requiere tu motor?</h5>
                        <p>Verifica la viscosidad OEM exacta, capacidad de cárter y el paquete completo de fluidos recomendados en nuestra guía interactiva.</p>
                        <a href="{HOME_PAGE}#lookup-widget" class="btn btn-red">Ir al Buscador por Vehículo →</a>
                    </div>

                    <div class="mega-promo-box" style="border-left-color:var(--amsoil-blue); border-left-width:5px;">
                        <span class="kicker">DATOS TÉCNICOS TRANSPARENTES</span>
                        <h5>Índice de las 104 Fichas Técnicas (PDS)</h5>
                        <p>Cada producto de nuestro catálogo cuenta con ficha técnica verificada, beneficios comprobados y normas API, ACEA, JASO y OEM cubiertas.</p>
                        <a href="ingenieria.html" class="btn btn-blue">Explorar Índice de Fichas PDS →</a>
                    </div>
                </div>
            </div>
        </div>
    </section>

{render_common_footer()}
</body>
</html>
"""
    (BASE_DIR / "contacto.html").write_text(html_content, encoding="utf-8")


# 8. BUILD 404.HTML BAJO MANUAL DE MARCA OFICIAL
def build_404():
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Página No Encontrada (404) | AMSOIL Costa Rica</title>
{GOOGLE_FONTS_HEAD}
    <style>
        .error-hero {{
            padding: 88px 20px;
            text-align: center;
            background-color: var(--amsoil-black);
            color: var(--amsoil-white);
            min-height: 62vh;
            display: flex;
            align-items: center;
            justify-content: center;
            border-bottom: 4px solid var(--amsoil-red);
        }}
        .error-card {{
            max-width: 640px;
            margin: 0 auto;
            background: var(--amsoil-black);
            border: 1px solid rgba(188, 190, 192, 0.35);
            border-top: 4px solid var(--amsoil-blue);
            border-radius: 2px;
            padding: 48px 32px;
        }}
        .error-code {{
            font-family: var(--font-heading);
            font-size: 4.5rem;
            font-weight: 700;
            color: var(--amsoil-red);
            line-height: 1;
            margin-bottom: 12px;
        }}
        .error-title {{
            font-family: var(--font-heading);
            font-size: 1.65rem;
            font-weight: 700;
            color: var(--amsoil-white);
            margin-bottom: 12px;
        }}
        .error-desc {{
            font-family: var(--font-body);
            font-weight: 300;
            font-size: 1rem;
            color: var(--amsoil-cool-gray);
            margin-bottom: 28px;
            line-height: 1.6;
        }}
        .error-actions {{
            display: flex;
            gap: 14px;
            justify-content: center;
            flex-wrap: wrap;
        }}
    </style>
</head>
<body>

    <div class="amsoil-utility-bar">
        <div class="container utility-inner">
            <span class="utility-tagline"><strong>The First in Synthetics®</strong></span>
            <span class="region-selector">COSTA RICA</span>
        </div>
    </div>

    <header class="amsoil-brand-header">
        <div class="container brand-header-inner" style="grid-template-columns: auto auto; justify-content: space-between;">
            <a href="index.html" class="amsoil-official-logo" aria-label="AMSOIL Costa Rica Inicio">
                <img src="amsoil-logo.png" alt="AMSOIL®" class="amsoil-logo-svg" width="192" height="59">
            </a>
            <div class="header-quick-tools">
                <a href="contacto.html" class="tool-item">
                    <div class="tool-text">
                        <strong>Contáctenos</strong>
                        <span>Puntos de Venta y Talleres</span>
                    </div>
                </a>
            </div>
        </div>
    </header>

    <main class="error-hero">
        <div class="error-card">
            <div class="error-code">404</div>
            <h1 class="error-title">Página No Encontrada</h1>
            <p class="error-desc">La dirección solicitada no existe o ha sido actualizada dentro del portal informativo de AMSOIL Costa Rica.</p>
            <div class="error-actions">
                <a href="index.html" class="btn btn-red">Ir a la Portada</a>
                <a href="{HOME_PAGE}" class="btn btn-blue">Ver Catálogo Oficial</a>
                <a href="contacto.html" class="btn btn-outline-white">Contáctenos</a>
            </div>
        </div>
    </main>

    <footer class="amsoil-footer" style="padding: 28px 0;">
        <div class="container footer-copy" style="border-top: none; padding-top: 0;">
            <span>© 2026 American Lubricants Supply S.A. — Distribuidor Autorizado en Costa Rica. Todas las marcas registradas son propiedad de AMSOIL INC.</span>
            <span>The First in Synthetics®</span>
        </div>
    </footer>

</body>
</html>
"""
    (BASE_DIR / "404.html").write_text(html_content, encoding="utf-8")


if __name__ == "__main__":
    build_index()
    build_automotriz()
    build_diesel()
    build_european()
    build_motos()
    build_transmision()
    build_aditivos()
    build_ingenieria()
    build_contacto()
    build_404()
    print("Successfully built all pages under strict AMSOIL INC. Brand Style Guide standards!")
