#!/usr/bin/env python3
import json
import html
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CATALOG_PATH = BASE_DIR / "catalogo-imagenes.json"

with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    CATALOG = json.load(f)

BY_ID = {item["id"]: item for item in CATALOG}


def pick_primary_image(item):
    images = item.get("images", [])
    # Prefer transparent studio cutout first for crisp look, or 1qt/1gal container
    for img in images:
        if "recorte-fondo-transparente" in img["filename"]:
            return img
    for img in images:
        if img.get("is_container"):
            return img
    return images[0] if images else None


def get_unique_presentations(item):
    """Return up to 6 distinct container/cutout images for the interactive switcher."""
    images = item.get("images", [])
    seen_labels = set()
    selected = []
    # Put primary image first
    primary = pick_primary_image(item)
    if primary:
        lbl = "Envase Oficial" if "recorte-fondo-transparente" in primary["filename"] else primary.get("short_label", "Envase")
        seen_labels.add(lbl)
        selected.append((lbl, primary["rel_path"], primary.get("sku", item["amsoil_code"])))

    for img in images:
        if primary and img["rel_path"] == primary["rel_path"]:
            continue
        fn = img["filename"]
        if "catalogo-latam" in fn or "familia-" in fn or "envase-principal" in fn:
            continue
        lbl = img.get("short_label") or img.get("presentation") or img.get("sku")
        if "recorte-fondo-transparente" in fn:
            lbl = "Recorte PNG"
        if lbl not in seen_labels:
            seen_labels.add(lbl)
            selected.append((lbl, img["rel_path"], img.get("sku", item["amsoil_code"])))
        if len(selected) >= 6:
            break

    # If still only 1 image and there are other images, add them
    if len(selected) < 2:
        for img in images:
            if primary and img["rel_path"] == primary["rel_path"]:
                continue
            lbl = img.get("short_label") or img.get("sku") or "Vista 2"
            if lbl not in seen_labels:
                seen_labels.add(lbl)
                selected.append((lbl, img["rel_path"], img.get("sku", item["amsoil_code"])))
            if len(selected) >= 4:
                break
    return selected[:4]


def badge_class_for_line(line):
    return ""


def get_specific_subcat_token(prod_id):
    token_map = {
        # European Formula
        "ezt-0w-20-ls-vw": "low-saps",
        "afe-0w-20-ls": "low-saps",
        "ael-5w-30-ls": "low-saps",
        "eot-0w-30-ms": "mid-saps",
        "afl-5w-40-ms": "mid-saps",
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
    amsoil_code = item.get("amsoil_code") or ""
    tech = item.get("tech_sheet") or {}
    summary = tech.get("summary") or ""

    primary_img = pick_primary_image(item)
    primary_src = primary_img["rel_path"] if primary_img else "amsoil-logo.png"
    presentations = get_unique_presentations(item)

    visc_slug = visc.lower().replace("-", "").replace(" ", "")
    specific_token = get_specific_subcat_token(prod_id)
    subcat_tokens = f"{line} {visc_slug} {extra_subcat} {specific_token}".strip()

    pres_buttons_html = ""
    for idx, (lbl, rel_path, sku) in enumerate(presentations):
        active_cls = "active" if idx == 0 else ""
        short_lbl = lbl.replace(" (946 mL)", "").replace(" (3.78 L)", "").replace("Recorte PNG", "Vista Principal").replace("Envase Oficial", "Vista Principal")
        pres_buttons_html += (
            f'<button type="button" class="pres-switch-btn {active_cls}" '
            f'data-img-src="{html.escape(rel_path)}" data-sku="{html.escape(sku)}">'
            f'{html.escape(short_lbl)}</button>'
        )

    visc_pill_html = f'<span class="prod-viscosity-pill">{html.escape(visc)}</span>' if visc and visc != "N/A" else ""
    meta_str = f"Código {amsoil_code}" + (f" • SAE {visc}" if visc and visc != "N/A" else "")

    return f"""
                <article class="amsoil-prod-tile" data-product-id="{html.escape(prod_id)}" data-subcat="{html.escape(subcat_tokens)}">
                    {visc_pill_html}
                    <div class="prod-tile-image">
                        <img src="{html.escape(primary_src)}" alt="{html.escape(item['display_name'])}" class="prod-tile-photo" loading="lazy">
                    </div>
                    <div class="prod-tile-body">
                        <div class="prod-tile-code">{html.escape(meta_str)}</div>
                        <h3 class="prod-tile-title">{html.escape(item['display_name'])}</h3>
                        <p class="prod-tile-desc">{html.escape(summary)}</p>
                        <div class="prod-presentations-bar">
                            {pres_buttons_html}
                        </div>
                    </div>
                    <div class="prod-tile-footer">
                        <button type="button" class="btn-pds-trigger" data-open-pds="{html.escape(prod_id)}">
                            Ver Ficha Técnica y Envases →
                        </button>
                    </div>
                </article>"""


def render_common_header(active_page="", search_placeholder="Ingresa tu vehículo, motor, maquinaria, viscosidad (ej. 5W-30, 15W-40) o tipo de aceite..."):
    def nav_cls(page):
        return "nav-trigger active-page" if active_page == page else "nav-trigger"

    lookup_href = "#lookup-widget" if active_page == "index" else "index.html#lookup-widget"

    return f"""    <!-- NIVEL 1: TOP UTILITY BAR (#0F1416 Bunker + #2C73B7 Blue) -->
    <div class="amsoil-utility-bar">
        <div class="container utility-inner">
            <span class="region-selector">🇨🇷 COSTA RICA</span>
        </div>
    </div>

    <!-- NIVEL 2: MAIN BRAND HEADER BLANCO (#FFFFFF + Logo Oficial AMSOIL + Buscador Unificado) -->
    <header class="amsoil-brand-header">
        <div class="container brand-header-inner">
            <a href="index.html" class="amsoil-official-logo" aria-label="AMSOIL Costa Rica Inicio">
                <img src="amsoil-logo.png" alt="AMSOIL Oficial Costa Rica" class="amsoil-logo-svg">
            </a>

            <form id="headerGlobalSearchForm" class="global-search-form">
                <input 
                    type="text" 
                    id="headerGlobalSearchInput" 
                    class="global-search-input" 
                    placeholder="{html.escape(search_placeholder)}"
                >
                <button type="submit" class="global-search-btn" aria-label="Buscar Vehículo o Producto">
                    <svg class="car-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 16H9m10 0h3v-3.15a1 1 0 00-.84-.99L16 11l-2.7-3.6a1 1 0 00-.8-.4H5.24a2 2 0 00-1.8 1.1l-.8 1.63A6 6 0 002 12.42V16h2"/><circle cx="6.5" cy="16.5" r="2.5"/><circle cx="16.5" cy="16.5" r="2.5"/></svg>
                    <div class="search-btn-label">
                        <strong>Buscar Vehículo</strong>
                        <span>o Viscosidad / Aceite</span>
                    </div>
                    <svg class="lupa-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
                </button>
            </form>

            <div class="header-quick-tools">
                <a href="contacto.html" class="tool-item">
                    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
                    <div class="tool-text">
                        <strong>Contáctenos</strong>
                        <span>Puntos de Venta y Mapa</span>
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
                        <svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M6 9l6 6 6-6"/></svg>
                    </a>
                    <div class="mega-menu">
                        <div class="container mega-menu-grid">
                            <div class="mega-col">
                                <h4>Automotriz Gasolina</h4>
                                <ul>
                                    <li><a href="automotriz.html?filter=signature-series">Signature Series 100% Sintético</a></li>
                                    <li><a href="automotriz.html?filter=xl-synthetic">XL Extended Life 100% Sintético</a></li>
                                    <li><a href="automotriz.html?filter=oe-synthetic">OE 100% Sintético Motor Oil</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4>Híbridos & Alto Kilometraje</h4>
                                <ul>
                                    <li><a href="automotriz.html?filter=hybrid">AMSOIL Hybrid 100% Sintético</a></li>
                                    <li><a href="automotriz.html?filter=high-mileage">AMSOIL High-Mileage 100% Sintético</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4>Competencia & Clásicos Alto Zinc</h4>
                                <ul>
                                    <li><a href="automotriz.html?filter=dominator">DOMINATOR® Racing 100% Sintético</a></li>
                                    <li><a href="automotriz.html?filter=z-rod">Z-ROD® Alto Zinc 100% Sintético</a></li>
                                    <li><a href="automotriz.html?filter=break-in">Break-In Oil</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </li>

                <li class="nav-item">
                    <a href="diesel.html" class="{nav_cls('diesel')}">
                        <span>Diesel</span>
                        <svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M6 9l6 6 6-6"/></svg>
                    </a>
                    <div class="mega-menu">
                        <div class="container mega-menu-grid">
                            <div class="mega-col">
                                <h4>Signature Series Max-Duty</h4>
                                <ul>
                                    <li><a href="diesel.html?filter=signature-series-max-duty">Signature Series Max-Duty 100% Sintético</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4>Heavy-Duty</h4>
                                <ul>
                                    <li><a href="diesel.html?filter=heavy-duty-ck4">Heavy-Duty 100% Sintético</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4>100% Synthetic Diesel GM dexosD</h4>
                                <ul>
                                    <li><a href="diesel.html?filter=diesel-dexos-d">100% Sintético Diesel GM dexosD</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </li>

                <li class="nav-item">
                    <a href="european.html" class="{nav_cls('european')}">
                        <span>European Formula</span>
                        <svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M6 9l6 6 6-6"/></svg>
                    </a>
                    <div class="mega-menu">
                        <div class="container mega-menu-grid">
                            <div class="mega-col">
                                <h4>Low-SAPS (LS)</h4>
                                <ul>
                                    <li><a href="european.html?filter=low-saps">European Car Formula Low-SAPS (LS) 100% Sintético</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4>Mid-SAPS (MS)</h4>
                                <ul>
                                    <li><a href="european.html?filter=mid-saps">European Car Formula Mid-SAPS (MS) 100% Sintético</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4>Full-SAPS (FS)</h4>
                                <ul>
                                    <li><a href="european.html?filter=full-saps">European Car Formula Full-SAPS (FS) 100% Sintético</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </li>

                <li class="nav-item">
                    <a href="motos.html" class="{nav_cls('motos')}">
                        <span>Motos & ATV/UTV</span>
                        <svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M6 9l6 6 6-6"/></svg>
                    </a>
                    <div class="mega-menu">
                        <div class="container mega-menu-grid">
                            <div class="mega-col">
                                <h4>Motocicletas de Calle & V-Twin</h4>
                                <ul>
                                    <li><a href="motos.html?filter=metric-motorcycle">Metric Motorcycle Oil 100% Sintético</a></li>
                                    <li><a href="motos.html?filter=v-twin-oil">V-Twin Motorcycle Oil 100% Sintético</a></li>
                                    <li><a href="motos.html?filter=v-twin-primary">V-Twin Primary Fluid 100% Sintético</a></li>
                                    <li><a href="motos.html?filter=v-twin-trans">V-Twin Transmission Fluid 100% Sintético</a></li>
                                    <li><a href="motos.html?filter=4t-performance">4T Performance Motorcycle Oil 100% Sintético</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4>Dirt Bike, 2 Tiempos & Suspensión</h4>
                                <ul>
                                    <li><a href="motos.html?filter=dirt-bike-oil">Dirt Bike Oil 100% Sintético</a></li>
                                    <li><a href="motos.html?filter=dirt-bike-trans">Dirt Bike Transmission Fluid 100% Sintético</a></li>
                                    <li><a href="motos.html?filter=dominator-2t">DOMINATOR® 2-Stroke Racing Oil 100% Sintético</a></li>
                                    <li><a href="motos.html?filter=interceptor-2t">INTERCEPTOR® 2-Stroke Oil 100% Sintético</a></li>
                                    <li><a href="motos.html?filter=shock-therapy">Shock Therapy® Suspension Fluid</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4>ATV/UTV & Marino</h4>
                                <ul>
                                    <li><a href="motos.html?filter=atv-utv-oil">ATV/UTV Motor Oil 100% Sintético</a></li>
                                    <li><a href="motos.html?filter=atv-utv-trans">ATV/UTV Transmission & Differential Fluid 100% Sintético</a></li>
                                    <li><a href="motos.html?filter=atv-utv-dct">ATV/UTV Dual-Clutch (DCT) Fluid 100% Sintético</a></li>
                                    <li><a href="motos.html?filter=marino">HP Marine™ 2-Stroke Oil 100% Sintético</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </li>

                <li class="nav-item">
                    <a href="transmision.html" class="{nav_cls('transmision')}">
                        <span>Transmisión / Gear</span>
                        <svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M6 9l6 6 6-6"/></svg>
                    </a>
                    <div class="mega-menu">
                        <div class="container mega-menu-grid">
                            <div class="mega-col">
                                <h4>Transmisión Automática ATF</h4>
                                <ul>
                                    <li><a href="transmision.html?filter=signature-atf">Signature Series ATF 100% Sintético</a></li>
                                    <li><a href="transmision.html?filter=oe-atf">OE ATF 100% Sintético</a></li>
                                    <li><a href="transmision.html?filter=torque-drive">Torque-Drive® Heavy-Duty ATF 100% Sintético</a></li>
                                    <li><a href="transmision.html?filter=super-shift">Super Shift® Racing Transmission Fluid</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4>CVT, DCT & Transmisión Manual</h4>
                                <ul>
                                    <li><a href="transmision.html?filter=cvt-fluid">100% Sintético CVT Fluid</a></li>
                                    <li><a href="transmision.html?filter=dct-fluid">100% Sintético DCT Fluid</a></li>
                                    <li><a href="transmision.html?filter=synchromesh">Manual Synchromesh Transmission Fluid (MTF)</a></li>
                                    <li><a href="transmision.html?filter=manual-gl4">Manual Transmission & Transaxle Gear Lube (GL-4)</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4>Diferenciales & Gear Lube</h4>
                                <ul>
                                    <li><a href="transmision.html?filter=severe-gear">SEVERE GEAR® EP Gear Lube 100% Sintético</a></li>
                                    <li><a href="transmision.html?filter=long-life-gear">Long Life Gear Lube 100% Sintético</a></li>
                                    <li><a href="transmision.html?filter=slip-lock">Slip Lock® Differential Additive</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </li>

                <li class="nav-item">
                    <a href="aditivos.html" class="{nav_cls('aditivos')}">
                        <span>Aditivos / Coolant</span>
                        <svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M6 9l6 6 6-6"/></svg>
                    </a>
                    <div class="mega-menu">
                        <div class="container mega-menu-grid">
                            <div class="mega-col">
                                <h4>Aditivos de Combustible & Motor</h4>
                                <ul>
                                    <li><a href="aditivos.html?filter=pi-improver">P.i.® Performance Improver Gasoline Additive</a></li>
                                    <li><a href="aditivos.html?filter=upper-cylinder">Upper Cylinder Lubricant Gasoline Additive</a></li>
                                    <li><a href="aditivos.html?filter=octane-boost">DOMINATOR® Octane Boost</a></li>
                                    <li><a href="aditivos.html?filter=moto-octane">Motorcycle Octane Boost</a></li>
                                    <li><a href="aditivos.html?filter=diesel-injector">Diesel Injector Clean + Cetane Boost</a></li>
                                    <li><a href="aditivos.html?filter=engine-flush">Engine & Transmission Flush</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4>Coolant, Frenos & Dirección</h4>
                                <ul>
                                    <li><a href="aditivos.html?filter=antpc">Passenger Car & Light Truck Antifreeze & Coolant</a></li>
                                    <li><a href="aditivos.html?filter=anthd">Heavy-Duty Antifreeze & Coolant</a></li>
                                    <li><a href="aditivos.html?filter=psaf">Powersports Antifreeze & Coolant</a></li>
                                    <li><a href="aditivos.html?filter=coolant-boost">DOMINATOR® Coolant Boost</a></li>
                                    <li><a href="aditivos.html?filter=dot34-brake">DOT 3 & DOT 4 Brake Fluid 100% Sintético</a></li>
                                    <li><a href="aditivos.html?filter=dominator-brake">DOMINATOR® DOT 4 Racing Brake Fluid 100% Sintético</a></li>
                                    <li><a href="aditivos.html?filter=power-steering">Multi-Vehicle Power Steering Fluid 100% Sintético</a></li>
                                </ul>
                            </div>
                            <div class="mega-col">
                                <h4>Grasas, Lubricantes & Especialidades</h4>
                                <ul>
                                    <li><a href="aditivos.html?filter=off-road-grease">NLGI #2 Polymeric Off-Road Grease 100% Sintético</a></li>
                                    <li><a href="aditivos.html?filter=multi-purpose-grease">Multi-Purpose Grease NLGI #2 100% Sintético</a></li>
                                    <li><a href="aditivos.html?filter=red-grease">100% Sintético Red Grease</a></li>
                                    <li><a href="aditivos.html?filter=chain-lube">Chain Lube Spray</a></li>
                                    <li><a href="aditivos.html?filter=assembly-lube">Engine Assembly Lube</a></li>
                                    <li><a href="aditivos.html?filter=compressor-oil">ISO 68 Compressor Oil 100% Sintético</a></li>
                                    <li><a href="aditivos.html?filter=saber-2t">SABER® Professional 2-Stroke Oil 100% Sintético</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </li>
            </ul>
        </div>
    </nav>

    <!-- BANNER TRANSITORIO DE ANUNCIOS E INFORMACIÓN DE PRODUCTOS (CARRUSEL INTERACTIVO) -->
    <section class="amsoil-hero-carousel" id="amsoilHeroCarousel" aria-label="Anuncios y Productos Destacados">
        <button type="button" class="carousel-arrow-btn prev" aria-label="Anterior">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M15 18l-6-6 6-6"/></svg>
        </button>

        <div class="hero-carousel-track">
            <!-- DIAPOSITIVA 1: SIGNATURE SERIES -->
            <div class="hero-carousel-slide active">
                <div class="hero-slide-inner">
                    <div class="hero-slide-visual">
                        <img src="01-motor-gasolina/signature-series/0w-20/recorte-fondo-transparente-ASM.webp" alt="AMSOIL Signature Series 0W-20">
                        <img src="01-motor-gasolina/signature-series/5w-30/recorte-fondo-transparente-ASL.webp" alt="AMSOIL Signature Series 5W-30" class="featured-center">
                        <img src="01-motor-gasolina/signature-series/10w-30/recorte-fondo-transparente-ATM.webp" alt="AMSOIL Signature Series 10W-30">
                    </div>
                    <div class="hero-slide-content">
                        <span class="hero-slide-kicker">THE FIRST IN SYNTHETICS®</span>
                        <h2 class="hero-slide-title">Signature Series 100% Sintético</h2>
                        <p class="hero-slide-subtitle">75% más protección contra pérdida de potencia y desgaste</p>
                        <a href="automotriz.html?filter=signature-series" class="hero-slide-cta">VER LÍNEA SIGNATURE</a>
                        <div class="hero-slide-note">Protección garantizada hasta <strong>25,000 millas / 1 año</strong></div>
                    </div>
                </div>
            </div>

            <!-- DIAPOSITIVA 2: DIESEL MAX-DUTY & HEAVY-DUTY -->
            <div class="hero-carousel-slide slide-theme-2">
                <div class="hero-slide-inner">
                    <div class="hero-slide-visual">
                        <img src="02-motor-diesel/signature-series-max-duty/5w-40/recorte-fondo-transparente-DEO.webp" alt="AMSOIL Max-Duty 5W-40 Diesel">
                        <img src="02-motor-diesel/signature-series-max-duty/15w-40/recorte-fondo-transparente-DME.webp" alt="AMSOIL Max-Duty 15W-40 Diesel" class="featured-center">
                        <img src="02-motor-diesel/heavy-duty-ck4/15w-40/recorte-fondo-transparente-ADP.webp" alt="AMSOIL Heavy-Duty 15W-40 Diesel">
                    </div>
                    <div class="hero-slide-content">
                        <span class="hero-slide-kicker">POTENCIA Y PROTECCIÓN TURBODIÉSEL</span>
                        <h2 class="hero-slide-title">Max-Duty & Heavy-Duty Diesel</h2>
                        <p class="hero-slide-subtitle">6X más protección contra desgaste en motores pesados</p>
                        <a href="diesel.html" class="hero-slide-cta">EXPLORAR DIESEL</a>
                        <div class="hero-slide-note">Certificación oficial <strong>API CK-4 & GM dexosD</strong></div>
                    </div>
                </div>
            </div>

            <!-- DIAPOSITIVA 3: EUROPEAN FORMULA & EASY-PACK -->
            <div class="hero-carousel-slide slide-theme-3">
                <div class="hero-slide-inner">
                    <div class="hero-slide-visual">
                        <img src="01-motor-gasolina/european-car-formula/5w-30-ls/recorte-fondo-transparente-AEL.webp" alt="AMSOIL European Car Formula 5W-30">
                        <img src="03-transmision-y-diferenciales/severe-gear-y-diferenciales/severe-gear-75w-90/recorte-fondo-transparente-SVG.webp" alt="AMSOIL SEVERE GEAR 75W-90 Easy-Pack" class="featured-center">
                        <img src="03-transmision-y-diferenciales/transmision-automatica-atf-cvt-dct/signature-series-multi-vehicle-atf-red/recorte-fondo-transparente-ATF.webp" alt="AMSOIL Signature Series ATF">
                    </div>
                    <div class="hero-slide-content">
                        <span class="hero-slide-kicker">INNOVACIÓN EN CADA CAMBIO</span>
                        <h2 class="hero-slide-title">European Formula & Easy-Pack®</h2>
                        <p class="hero-slide-subtitle">Homologaciones OEM europeas y diferenciales 4x4 sin derrames</p>
                        <a href="european.html" class="hero-slide-cta">VER CATÁLOGO</a>
                        <div class="hero-slide-note">Disponible en <strong>Talleres y Puntos de Venta en CR</strong></div>
                    </div>
                </div>
            </div>
        </div>

        <button type="button" class="carousel-arrow-btn next" aria-label="Siguiente">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M9 18l6-6-6-6"/></svg>
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

    <!-- FRANJA AZUL DE VEHÍCULOS (9 SILUETAS OFICIALES, SIN MOTO DE NIEVE Y SIN "SHOP BY VEHICLE") -->
    <section class="amsoil-blue-vehicle-strip" aria-label="Categorías de Vehículos">
        <div class="container">
            <div class="blue-vehicle-grid">
                <!-- 1. AUTO / LIGHT TRUCK -->
                <a href="automotriz.html" class="blue-veh-item">
                    <div class="blue-veh-icon">
                        <svg viewBox="0 0 120 52" fill="none">
                            <path d="M10 34L22 31L39 18H76L95 28L111 31V40H99C99 33 93 28 86 28C79 28 73 33 73 40H43C43 33 37 28 30 28C23 28 17 33 17 40H8V36L10 34Z" fill="#D8E6F3"/>
                            <path d="M42 21H60V29H31L42 21ZM64 21H74L88 29H64V21Z" fill="#00386B"/>
                            <circle cx="30" cy="40" r="9" fill="#8FB0CC"/>
                            <circle cx="30" cy="40" r="4.5" fill="#00386B"/>
                            <circle cx="86" cy="40" r="9" fill="#8FB0CC"/>
                            <circle cx="86" cy="40" r="4.5" fill="#00386B"/>
                        </svg>
                    </div>
                    <span class="blue-veh-label">AUTO/LIGHT<br>TRUCK</span>
                </a>

                <!-- 2. MOTORCYCLE -->
                <a href="motos.html?filter=metric-motorcycle" class="blue-veh-item">
                    <div class="blue-veh-icon">
                        <svg viewBox="0 0 120 52" fill="none">
                            <circle cx="26" cy="38" r="10.5" stroke="#8FB0CC" stroke-width="4" fill="#00386B"/>
                            <circle cx="26" cy="38" r="3.5" fill="#D8E6F3"/>
                            <circle cx="92" cy="38" r="10.5" stroke="#8FB0CC" stroke-width="4" fill="#00386B"/>
                            <circle cx="92" cy="38" r="3.5" fill="#D8E6F3"/>
                            <path d="M26 38L42 22H56L68 29H82L72 16H64L70 12H78L92 38" stroke="#D8E6F3" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
                            <path d="M40 24C45 18 56 18 62 24L74 28L66 37H44L40 24Z" fill="#D8E6F3"/>
                        </svg>
                    </div>
                    <span class="blue-veh-label">MOTORCYCLE</span>
                </a>

                <!-- 3. ATV -->
                <a href="motos.html?filter=atv-utv" class="blue-veh-item">
                    <div class="blue-veh-icon">
                        <svg viewBox="0 0 120 52" fill="none">
                            <path d="M26 26L38 19H54L50 11H43M50 11L58 11M22 28H92L96 34H20L22 28Z" stroke="#D8E6F3" stroke-width="3.5" stroke-linecap="round"/>
                            <path d="M25 24L42 18H74L92 25L88 35H28L25 24Z" fill="#D8E6F3"/>
                            <circle cx="34" cy="39" r="10.5" fill="#8FB0CC"/>
                            <circle cx="34" cy="39" r="5" fill="#00386B"/>
                            <circle cx="82" cy="39" r="10.5" fill="#8FB0CC"/>
                            <circle cx="82" cy="39" r="5" fill="#00386B"/>
                        </svg>
                    </div>
                    <span class="blue-veh-label">ATV</span>
                </a>

                <!-- 4. UTV -->
                <a href="motos.html?filter=atv-utv" class="blue-veh-item">
                    <div class="blue-veh-icon">
                        <svg viewBox="0 0 120 52" fill="none">
                            <path d="M34 26L44 10H76L88 26" stroke="#8FB0CC" stroke-width="3.5" stroke-linejoin="round"/>
                            <path d="M60 10V26" stroke="#8FB0CC" stroke-width="3"/>
                            <path d="M18 25H40L46 29H76L84 24L102 28V37H18V25Z" fill="#D8E6F3"/>
                            <circle cx="32" cy="40" r="10" fill="#8FB0CC"/>
                            <circle cx="32" cy="40" r="4.5" fill="#00386B"/>
                            <circle cx="86" cy="40" r="10" fill="#8FB0CC"/>
                            <circle cx="86" cy="40" r="4.5" fill="#00386B"/>
                        </svg>
                    </div>
                    <span class="blue-veh-label">UTV</span>
                </a>

                <!-- 5. MARINE OUTBOARD -->
                <a href="motos.html?filter=marino" class="blue-veh-item">
                    <div class="blue-veh-icon">
                        <svg viewBox="0 0 120 52" fill="none">
                            <path d="M10 27H96L110 27L98 39H22L10 27Z" fill="#D8E6F3"/>
                            <path d="M44 27L56 18H74L80 27H44Z" fill="#8FB0CC"/>
                            <path d="M12 22H22L24 31L16 44H11L15 31L12 22Z" fill="#8FB0CC"/>
                            <path d="M22 32H98" stroke="#00386B" stroke-width="2"/>
                        </svg>
                    </div>
                    <span class="blue-veh-label">MARINE<br>OUTBOARD</span>
                </a>

                <!-- 6. PWC -->
                <a href="motos.html?filter=2-stroke" class="blue-veh-item">
                    <div class="blue-veh-icon">
                        <svg viewBox="0 0 120 52" fill="none">
                            <path d="M16 35L32 27H58L72 18L82 20L76 27L104 33L94 40H22L16 35Z" fill="#D8E6F3"/>
                            <path d="M40 27L52 21H68L62 27H40Z" fill="#8FB0CC"/>
                            <path d="M18 36H98" stroke="#00386B" stroke-width="2.5"/>
                        </svg>
                    </div>
                    <span class="blue-veh-label">PWC</span>
                </a>

                <!-- 7. HEAVY-DUTY ON-ROAD -->
                <a href="diesel.html?filter=signature-series-max-duty" class="blue-veh-item">
                    <div class="blue-veh-icon">
                        <svg viewBox="0 0 120 52" fill="none">
                            <path d="M14 33H52V12C64 12 74 16 78 24L98 26V38H14V33Z" fill="#D8E6F3"/>
                            <rect x="64" y="18" width="10" height="8" fill="#00386B"/>
                            <rect x="47" y="8" width="3.5" height="26" fill="#8FB0CC"/>
                            <circle cx="25" cy="40" r="8" fill="#8FB0CC"/>
                            <circle cx="25" cy="40" r="3.8" fill="#00386B"/>
                            <circle cx="43" cy="40" r="8" fill="#8FB0CC"/>
                            <circle cx="43" cy="40" r="3.8" fill="#00386B"/>
                            <circle cx="86" cy="40" r="8" fill="#8FB0CC"/>
                            <circle cx="86" cy="40" r="3.8" fill="#00386B"/>
                        </svg>
                    </div>
                    <span class="blue-veh-label">HEAVY-DUTY<br>ON-ROAD</span>
                </a>

                <!-- 8. HEAVY-DUTY OFF-ROAD -->
                <a href="diesel.html?filter=heavy-duty-ck4" class="blue-veh-item">
                    <div class="blue-veh-icon">
                        <svg viewBox="0 0 120 52" fill="none">
                            <path d="M12 18L72 14L66 32H18L12 18Z" fill="#8FB0CC"/>
                            <path d="M68 18H90L98 26V36H16V31H66L68 18Z" fill="#D8E6F3"/>
                            <rect x="74" y="21" width="12" height="7" fill="#00386B"/>
                            <circle cx="28" cy="40" r="8.5" fill="#8FB0CC"/>
                            <circle cx="28" cy="40" r="4" fill="#00386B"/>
                            <circle cx="46" cy="40" r="8.5" fill="#8FB0CC"/>
                            <circle cx="46" cy="40" r="4" fill="#00386B"/>
                            <circle cx="84" cy="40" r="8.5" fill="#8FB0CC"/>
                            <circle cx="84" cy="40" r="4" fill="#00386B"/>
                        </svg>
                    </div>
                    <span class="blue-veh-label">HEAVY-DUTY<br>OFF-ROAD</span>
                </a>

                <!-- 9. AGRICULTURE -->
                <a href="diesel.html" class="blue-veh-item">
                    <div class="blue-veh-icon">
                        <svg viewBox="0 0 120 52" fill="none">
                            <path d="M18 14H56L64 26H88V36H18V14Z" fill="#D8E6F3"/>
                            <rect x="34" y="18" width="18" height="10" fill="#00386B"/>
                            <path d="M64 31H110L106 38H64V31Z" fill="#8FB0CC"/>
                            <circle cx="32" cy="39" r="11" fill="#8FB0CC"/>
                            <circle cx="32" cy="39" r="5" fill="#00386B"/>
                            <circle cx="62" cy="41" r="7.5" fill="#8FB0CC"/>
                            <circle cx="62" cy="41" r="3.5" fill="#00386B"/>
                        </svg>
                    </div>
                    <span class="blue-veh-label">AGRICULTURE</span>
                </a>
            </div>
        </div>
    </section>"""


def render_common_footer():
    return """    <!-- FOOTER CORPORATIVO OFICIAL -->
    <footer class="amsoil-footer">
        <div class="container">
            <div class="footer-cols">
                <div>
                    <img src="amsoil-logo.png" alt="AMSOIL Oficial Costa Rica" style="height:48px; width:auto; margin-bottom:14px; background:#FFFFFF; padding:6px 12px; border-radius:2px; display:inline-block;">
                    <p style="font-size:0.86rem; color:#CACACD; max-width:320px;">
                        Portal informativo oficial de lubricantes, fluidos y aditivos 100% sintéticos AMSOIL en Costa Rica (American Lubricants Supply S.A.). The First in Synthetics® desde 1972.
                    </p>
                </div>

                <div>
                    <h4>Categorías del Catálogo (104 Productos)</h4>
                    <ul>
                        <li><a href="automotriz.html">Aceite de Motor Gasolina & Híbrido (26)</a></li>
                        <li><a href="diesel.html">Diesel 100% Sintético (9)</a></li>
                        <li><a href="european.html">European Car Formula (7)</a></li>
                        <li><a href="motos.html">Motocicletas, Enduro, ATV/UTV & Marino (25)</a></li>
                        <li><a href="transmision.html">Transmisión Automática, CVT & Diferenciales Gear (17)</a></li>
                        <li><a href="aditivos.html">Aditivos, Coolant, Frenos & Grasas (20)</a></li>
                    </ul>
                </div>

                <div>
                    <h4>Herramientas & Ubicaciones</h4>
                    <ul>
                        <li><a href="index.html#lookup-widget">Buscador de Vehículos con IA</a></li>
                        <li><a href="ingenieria.html">¿Por qué AMSOIL? Índice de las 104 Fichas Técnicas</a></li>
                        <li><a href="contacto.html#puntos-de-venta">Dónde Encontrar Talleres y Puntos de Venta</a></li>
                        <li><a href="contacto.html#formulario-contacto">Contáctenos</a></li>
                    </ul>
                </div>

                <div>
                    <h4>Contacto Oficial CR</h4>
                    <ul>
                        <li><a href="contacto.html">📍 American Lubricants Supply S.A. • Costa Rica</a></li>
                        <li><a href="contacto.html">📞 +506 2200-0000</a></li>
                        <li><a href="contacto.html">💬 WhatsApp: +506 8800-0000</a></li>
                        <li><a href="https://www.amsoil.com" target="_blank" rel="noopener">Sitio Corporativo AMSOIL USA ↗</a></li>
                    </ul>
                </div>
            </div>

            <div class="footer-copy">
                <span>© 2026 AMSOIL Costa Rica (American Lubricants Supply S.A.). Todas las marcas registradas pertenecen a AMSOIL INC., Superior, Wisconsin, USA.</span>
                <span>Catálogo Oficial Verificado: 104 Referencias 100% Sintéticas</span>
            </div>
        </div>
    </footer>

    <script src="catalogo-datos.js"></script>
    <script src="js/main.js"></script>"""


# 1. BUILD INDEX.HTML
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
    <title>AMSOIL Costa Rica | Lubricantes 100% Sintéticos — The First in Synthetics®</title>
    <meta name="description" content="AMSOIL Costa Rica (American Lubricants Supply S.A.): Lubricantes 100% sintéticos formulados en Estados Unidos para motor, pickups 4x4, motocicletas y transmisión.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,600;0,700;0,800;1,700;1,800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>

{render_common_header("index")}

    <!-- DOCK INTERACTIVO COMPACTO -->
    <section class="vehicle-lookup-dock" id="lookup-widget">
        <div class="container">
            <div class="lookup-dock-card">
                <div class="lookup-tabs-bar">
                    <button type="button" class="lookup-mode-tab">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M14 16H9m10 0h3v-3.15a1 1 0 00-.84-.99L16 11l-2.7-3.6a1 1 0 00-.8-.4H5.24a2 2 0 00-1.8 1.1l-.8 1.63A6 6 0 002 12.42V16h2"/><circle cx="6.5" cy="16.5" r="2.5"/><circle cx="16.5" cy="16.5" r="2.5"/></svg>
                        <span>Encuentra el aceite ideal para tu vehículo</span>
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
                                BUSCAR →
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

                    <div id="aiLoadingState" style="display:none; padding:16px; margin-top:14px; background:#F9FAFB; border-left:3px solid #CC262F; font-size:0.9rem;">
                        Consultando especificaciones para tu vehículo...
                    </div>

                    <div id="aiResultPanel" class="amsoil-guide-results" style="display: none;">
                        <div class="guide-results-header">
                            <div>
                                <div style="display:flex; gap:8px; margin-bottom:6px; flex-wrap:wrap;">
                                    <span id="resCategoryBadge" class="tier-kicker" style="background:#CC262F; margin:0;">GUÍA DE APLICACIÓN AMSOIL</span>
                                    <span id="resMileageBadge" class="tier-kicker" style="background:#2C73B7; color:#FFFFFF; margin:0; display:none;">ALTO KILOMETRAJE</span>
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
                                <span>Filtro de Referencia</span>
                                <strong id="resFilter">90915-YZZD2</strong>
                            </div>
                        </div>

                        <div class="guide-alerts-row">
                            <div class="guide-alert">
                                <strong>Nota Técnica OEM</strong>
                                <span id="resWarning"></span>
                            </div>
                            <div id="resMileageBox" class="guide-alert mileage-note" style="display:none;">
                                <strong>Recomendación por Kilometraje</strong>
                                <span id="resMileageAdvice"></span>
                            </div>
                        </div>

                        <div class="guide-sub-heading">
                            <span>Aceites de Motor Recomendados</span>
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

    <!-- 4 PRODUCTOS DESTACADOS EN UNA SOLA FILA LIMPIA -->
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

    <!-- BLOQUE DIVIDIDO "WHY AMSOIL" EN MODO CLARO -->
    <section class="section-block-white">
        <div class="container">
            <div class="why-amsoil-split">
                <div class="why-left-content">
                    <span class="kicker">INGENIERÍA SINTÉTICA</span>
                    <h2>¿POR QUÉ ELEGIR AMSOIL?</h2>
                    <p>
                        AMSOIL formula con bases 100% sintéticas puras que resisten la evaporación por calor extremo, mantienen los pistones limpios y protegen los turbocompresores frente al desgaste prematuro.
                    </p>
                    <div style="display:flex; gap:12px; flex-wrap:wrap;">
                        <a href="ingenieria.html" class="btn btn-red">VER PRUEBAS Y FICHAS TÉCNICAS</a>
                        <a href="contacto.html" class="btn btn-outline-dark">PUNTOS DE VENTA EN CR</a>
                    </div>
                </div>

                <div class="why-right-chart">
                    <span style="font-family:var(--font-heading); font-weight:800; color:#2C73B7; font-size:0.82rem; letter-spacing:1px;">PRUEBA DE DESGASTE ASTM SEQUENCE IVA</span>
                    <h3 style="font-family:var(--font-heading); font-size:1.5rem; margin:6px 0 18px; color:#0F1416; text-transform:uppercase;">Menor Desgaste = Mayor Vida del Motor</h3>

                    <div class="astm-bar-item">
                        <div class="astm-bar-label" style="color:#374151;">
                            <span>Límite Máximo Permitido API SP</span>
                            <strong>90 µm</strong>
                        </div>
                        <div class="astm-track"><div class="astm-fill" style="width:90%; background:#D1D5DB;"></div></div>
                    </div>

                    <div class="astm-bar-item">
                        <div class="astm-bar-label" style="color:#374151;">
                            <span>Sintético Comercial Promedio</span>
                            <strong>48 µm</strong>
                        </div>
                        <div class="astm-track"><div class="astm-fill" style="width:52%; background:#2C73B7;"></div></div>
                    </div>

                    <div class="astm-bar-item" style="margin-bottom:0;">
                        <div class="astm-bar-label" style="color:#0F1416;">
                            <span>★ AMSOIL Signature Series 100% Synthetic</span>
                            <strong style="color:#CC262F;">20 µm (75% Más Protección)</strong>
                        </div>
                        <div class="astm-track"><div class="astm-fill" style="width:22%; background:#CC262F;"></div></div>
                    </div>
                </div>
            </div>
        </div>
    </section>

{render_common_footer()}
</body>
</html>
"""
    (BASE_DIR / "index.html").write_text(html_content, encoding="utf-8")


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
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,600;0,700;0,800;1,700;1,800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>

{render_common_header("automotriz", "Escribe tu vehículo, viscosidad (ej. 0W-20, 5W-30) o código AMSOIL...")}

    <div class="cat-breadcrumb-bar">
        <div class="container">
            <a href="index.html">Inicio</a> &nbsp;/&nbsp; <span>Aceite de Motor Gasolina, Híbrido y Competencia ({len(items)} Referencias Oficiales)</span>
        </div>
    </div>

    <section class="cat-header-banner">
        <div class="container">
            <h1>ACEITE DE MOTOR AUTOMOTRIZ ({len(items)} PRODUCTOS)</h1>
            <p>Explora las {len(items)} referencias oficiales de AMSOIL Costa Rica para motores de gasolina americanos, japoneses y coreanos, Turbo-GDI, híbridos, alto kilometraje, competencia y asentamiento de motores (Break-In Oil).</p>
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
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,600;0,700;0,800;1,700;1,800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>

{render_common_header("diesel", "Buscar aceite Diesel (Signature Series Max-Duty, Heavy-Duty, dexosD, 15W-40, 5W-40)...")}

    <div class="cat-breadcrumb-bar">
        <div class="container">
            <a href="index.html">Inicio</a> &nbsp;/&nbsp; <span>Diesel 100% Sintético API CK-4 & GM dexosD ({len(items)} Referencias Oficiales)</span>
        </div>
    </div>

    <section class="cat-header-banner">
        <div class="container">
            <h1>ACEITES DE MOTOR 100% SINTÉTICOS DIESEL ({len(items)} PRODUCTOS)</h1>
            <p>Líneas Signature Series Max-Duty, Heavy-Duty y 100% Synthetic Diesel GM dexosD. Hasta 6 veces más protección contra desgaste del motor en la prueba Detroit Diesel DD13 Scuffing.</p>
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
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,600;0,700;0,800;1,700;1,800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>

{render_common_header("european", "Buscar norma europea (VW 504/507, 508/509, BMW LL-04, MB 229.51, Porsche A40)...")}

    <div class="cat-breadcrumb-bar">
        <div class="container">
            <a href="index.html">Inicio</a> &nbsp;/&nbsp; <span>AMSOIL European Car Formula 100% Synthetic ({len(items)} Referencias Oficiales)</span>
        </div>
    </div>

    <section class="cat-header-banner">
        <div class="container">
            <h1>AMSOIL EUROPEAN CAR FORMULA 100% SYNTHETIC ({len(items)} PRODUCTOS)</h1>
            <p>Línea completa de lubricantes 100% sintéticos formulados específicamente para vehículos europeos de gasolina y turbodiésel (BMW, Mercedes-Benz, Audi, Volkswagen, Porsche, Volvo, Land Rover y MINI) con protección avanzada para filtros de partículas DPF/GPF (Low-SAPS, Mid-SAPS y Full-SAPS).</p>
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
    <title>Motocicletas, Enduro, 2 Tiempos, ATV/UTV y Marino (25 Referencias) | AMSOIL Costa Rica</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,600;0,700;0,800;1,700;1,800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>

{render_common_header("motos", "Buscar aceite para moto, enduro, 2 tiempos, ATV/UTV o motor marino...")}

    <div class="cat-breadcrumb-bar">
        <div class="container">
            <a href="index.html">Inicio</a> &nbsp;/&nbsp; <span>Motocicletas, Enduro, 2 Tiempos, ATV/UTV y Marino ({len(items)} Referencias Oficiales)</span>
        </div>
    </div>

    <section class="cat-header-banner">
        <div class="container">
            <h1>MOTOCICLETAS, ENDURO, ATV/UTV Y MARINO ({len(items)} PRODUCTOS)</h1>
            <p>Lubricantes 100% sintéticos certificados JASO MA/MA2 para embrague húmedo, cajas de transmisión de motocross, sintéticos de 2 Tiempos (DOMINATOR®, INTERCEPTOR®, Saber®) y motores fuera de borda 4T/2T.</p>
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
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,600;0,700;0,800;1,700;1,800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>

{render_common_header("transmision", "Buscar fluido ATF, CVT, DCT, 75W-90 Easy-Pack, 75W-140 o caja manual...")}

    <div class="cat-breadcrumb-bar">
        <div class="container">
            <a href="index.html">Inicio</a> &nbsp;/&nbsp; <span>Transmisión / Gear & Diferenciales 4x4 ({len(items)} Referencias Oficiales)</span>
        </div>
    </div>

    <section class="cat-header-banner">
        <div class="container">
            <h1>TRANSMISIÓN AUTOMÁTICA ATF/CVT/DCT Y DIFERENCIALES SEVERE GEAR® ({len(items)} PRODUCTOS)</h1>
            <p>Protección 100% sintética para cajas automáticas de 6 a 10 velocidades, transmisiones continuas CVT, doble embrague DCT, cajas manuales y diferenciales hipoidales 4x4 con el envase flexible patentado Easy-Pack®.</p>
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


# 5B. BUILD ADITIVOS.HTML (21 ADITIVOS / COOLANT / FRENOS / GRASAS PRODUCTS)
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
    <title>Aditivos de Combustible, Coolant, Frenos DOT 3/4 y Grasas Sintéticas ({len(items)} Referencias) | AMSOIL Costa Rica</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,600;0,700;0,800;1,700;1,800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>

{render_common_header("aditivos", "Buscar aditivo P.i., Diesel All-In-One, Coolant, líquido de frenos DOT 4 o grasa...")}

    <div class="cat-breadcrumb-bar">
        <div class="container">
            <a href="index.html">Inicio</a> &nbsp;/&nbsp; <span>Aditivos de Combustible, Coolant, Frenos y Grasas Sintéticas ({len(items)} Referencias Oficiales)</span>
        </div>
    </div>

    <section class="cat-header-banner">
        <div class="container">
            <h1>ADITIVOS DE COMBUSTIBLE, COOLANT, FRENOS Y GRASAS SINTÉTICAS ({len(items)} PRODUCTOS)</h1>
            <p>Limpiadores de inyectores P.i.® y Diesel All-In-One, anticongelantes y mejoradores térmicos Dominator® Coolant Boost, líquidos de frenos 100% sintéticos DOT 3 y DOT 4, dirección hidráulica, Engine Flush y grasas poliméricas NLGI #2.</p>
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


# 6. BUILD INGENIERIA.HTML (ALL 105 PRODUCTS DIRECTORY + ASTM CHARTS)
def build_ingenieria():
    rows_html = ""
    for item in CATALOG:
        img = pick_primary_image(item)
        img_src = img["rel_path"] if img else "amsoil-logo.png"
        als_codes = ", ".join(item.get("als_codes") or []) or "Consultar"
        specs = item.get("tech_sheet", {}).get("specs") or "Especificación AMSOIL"
        short_specs = specs if len(specs) <= 75 else specs[:72] + "..."
        rows_html += f"""
                        <tr data-catalog-row="{html.escape((item['display_name'] + ' ' + item['amsoil_code'] + ' ' + als_codes + ' ' + item['viscosity'] + ' ' + item['category_name']).lower())}">
                            <td style="width:64px; text-align:center;">
                                <img src="{html.escape(img_src)}" alt="{html.escape(item['display_name'])}" style="height:48px; width:auto; object-fit:contain;" loading="lazy">
                            </td>
                            <td><strong style="color:var(--amsoil-red);">{html.escape(item['amsoil_code'])}</strong><br><span style="font-size:0.75rem; color:var(--amsoil-shark);">{html.escape(als_codes)}</span></td>
                            <td>
                                <strong>{html.escape(item['display_name'])}</strong>
                                <div style="font-size:0.78rem; color:var(--amsoil-blue); font-weight:700;">{html.escape(item['category_short'])} • {html.escape(item['line_name'])}</div>
                            </td>
                            <td><strong>{html.escape(item['viscosity'])}</strong></td>
                            <td style="font-size:0.82rem;">{html.escape(short_specs)}</td>
                            <td>
                                <button type="button" class="btn-pds-trigger" style="padding:6px 10px; font-size:0.78rem;" data-open-pds="{html.escape(item['id'])}">
                                    📋 Ver Ficha (PDS)
                                </button>
                            </td>
                        </tr>"""

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>¿Por qué AMSOIL? Ingeniería Sintética e Índice de las 104 Fichas Técnicas | AMSOIL Costa Rica</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,600;0,700;0,800;1,700;1,800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>

{render_common_header("ingenieria", "Buscar código técnico AMSOIL (ASM, ASL, DME, DEO, SVG, MCF) o código CR (AM10012)...")}

    <div class="cat-breadcrumb-bar">
        <div class="container">
            <a href="index.html">Inicio</a> &nbsp;/&nbsp; <span>¿Por qué AMSOIL? Ingeniería Sintética e Índice Completo de 104 Fichas Técnicas</span>
        </div>
    </div>

    <section class="cat-header-banner">
        <div class="container">
            <h1>INGENIERÍA SINTÉTICA E ÍNDICE GENERAL DE 104 FICHAS TÉCNICAS (PDS)</h1>
            <p>En 1972, AMSOIL introdujo el primer aceite 100% sintético del mundo certificado por el Instituto Americano del Petróleo (API). Consulta aquí los parámetros ASTM y abre la Ficha Técnica en español de cualquiera de las 104 referencias oficiales en Costa Rica.</p>
        </div>
    </section>

    <section class="section-block-white">
        <div class="container">
            <div class="why-amsoil-split">
                <div class="why-left-content">
                    <span class="kicker">ESTÁNDARES DE INGENIERÍA</span>
                    <h2>¿QUÉ SIGNIFICAN ESTAS PRUEBAS EN LAS CARRETERAS DE COSTA RICA?</h2>
                    <p>
                        Los ascensos pronunciados (Cambronero, Cerro de la Muerte, Zurquí) y las presas diarias con alta humedad tropical someten al lubricante a un estrés térmico extremo. AMSOIL mantiene su película protectora sin evaporarse ni formar depósitos.
                    </p>
                    <a href="index.html#lookup-widget" class="btn btn-red">BUSCAR EL ACEITE PARA MI MOTOR</a>
                </div>
                <div class="why-right-chart">
                    <div class="astm-bar-item">
                        <div class="astm-bar-label">
                            <span>PROTECCIÓN CONTRA DESGASTE (DETROIT DIESEL DD13)</span>
                            <strong style="color:#CC262F;">6X SUPERIOR AL LÍMITE</strong>
                        </div>
                        <div class="astm-track"><div class="astm-fill" style="width:94%; background-color:#CC262F;"></div></div>
                    </div>
                    <div class="astm-bar-item">
                        <div class="astm-bar-label">
                            <span>CONTROL DE VOLATILIDAD TÉRMICA (ASTM D5800 NOACK)</span>
                            <strong style="color:#2C73B7;">5.1% A 6.7% (LÍMITE API: 15%)</strong>
                        </div>
                        <div class="astm-track"><div class="astm-fill" style="width:88%; background-color:#2C73B7;"></div></div>
                    </div>
                    <div class="astm-bar-item" style="margin-bottom:0;">
                        <div class="astm-bar-label">
                            <span>PROTECCIÓN CONTRA PRE-IGNICIÓN TURBO (LSPI)</span>
                            <strong style="color:#CC262F;">100% PROTECCIÓN</strong>
                        </div>
                        <div class="astm-track"><div class="astm-fill" style="width:100%; background-color:#CC262F;"></div></div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="section-block-white">
        <div class="container">
            <div class="amsoil-sec-header" style="flex-wrap:wrap; gap:16px;">
                <h2 class="amsoil-sec-title">DIRECTORIO INTERACTIVO DE LAS 104 REFERENCIAS AMSOIL COSTA RICA</h2>
                <div style="flex:1; max-width:420px;">
                    <input type="text" id="catalogTableSearchInput" class="lookup-input" placeholder="🔍 Filtrar las 104 referencias por nombre, viscosidad o código (ej. 5W-30, DME, AM10012)...">
                </div>
            </div>

            <div class="table-clean-wrap">
                <table class="amsoil-clean-table">
                    <thead>
                        <tr>
                            <th>Envase</th>
                            <th>Código AMSOIL / CR</th>
                            <th>Producto y Línea Oficial</th>
                            <th>Grado / Tipo</th>
                            <th>Especificaciones Principales (API / OEM)</th>
                            <th>Ficha Técnica (PDS)</th>
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


# 7. UPDATE CONTACTO.HTML LOGO, HEADER & SCRIPTS
def update_contacto():
    contacto_path = BASE_DIR / "contacto.html"
    if not contacto_path.exists():
        return
    txt = contacto_path.read_text(encoding="utf-8")
    txt = txt.replace('src="assets/logos/amsoil-logo.png"', 'src="amsoil-logo.png"')
    txt = txt.replace('href="css/styles.css?v=20261020b"', 'href="css/styles.css"')
    if '<div class="amsoil-utility-bar">' in txt and '<div class="cat-breadcrumb-bar">' in txt:
        start_idx = txt.index('<div class="amsoil-utility-bar">')
        end_idx = txt.index('<div class="cat-breadcrumb-bar">')
        txt = txt[:start_idx] + render_common_header("contacto") + "\n\n    " + txt[end_idx:]
    if '<footer class="amsoil-footer">' in txt and '</body>' in txt:
        f_start = txt.index('<footer class="amsoil-footer">')
        f_end = txt.index('</body>')
        txt = txt[:f_start] + render_common_footer() + "\n" + txt[f_end:]
    contacto_path.write_text(txt, encoding="utf-8")


if __name__ == "__main__":
    build_index()
    build_automotriz()
    build_diesel()
    build_european()
    build_motos()
    build_transmision()
    build_aditivos()
    build_ingenieria()
    update_contacto()
    print("Successfully built all pages with 104 real 100% synthetic products!")
