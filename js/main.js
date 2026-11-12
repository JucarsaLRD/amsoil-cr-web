/**
 * AMSOIL COSTA RICA — INTERACTIVIDAD OFICIAL CON CATÁLOGO REAL (105 PRODUCTOS / 627 IMÁGENES)
 * Incluye:
 * 1. Selector Interactivo de Envases Reales en Cada Tarjeta (Cuarto, Easy-Pack, Galón, Cubeta, Estañón, Tote)
 * 2. Modal de Ficha Técnica Oficial (PDS) en Español + Galería de Envases + Códigos ALS Costa Rica
 * 3. Buscador Global del Header y Filtro en Tiempo Real de las 105 Referencias
 * 4. Recomendador de Vehículos con IA + Fotografías Reales de Envases
 * 5. Filtro de Categorías y Directorio Interactivo de Puntos de Venta / Talleres en Contáctenos
 */

document.addEventListener('DOMContentLoaded', () => {
    const CATALOG = Array.isArray(window.AMSOIL_CATALOG) ? window.AMSOIL_CATALOG : [];
    const CATALOG_BY_ID = {};
    const CATALOG_BY_CODE = {};

    CATALOG.forEach((item) => {
        CATALOG_BY_ID[item.id] = item;
        if (item.amsoil_code) {
            CATALOG_BY_CODE[item.amsoil_code.toUpperCase()] = item;
        }
    });

    function getPrimaryPhotoForCode(codeStr) {
        if (!codeStr || CATALOG.length === 0) return 'amsoil-logo.png';
        const parts = codeStr.split(/[\/,\s]+/).map((s) => s.trim().toUpperCase()).filter(Boolean);
        for (const p of parts) {
            const found = CATALOG_BY_CODE[p];
            if (found && found.images && found.images.length > 0) {
                const cutout = found.images.find((im) => im.filename.includes('recorte-fondo-transparente'));
                return (cutout || found.images[0]).rel_path;
            }
        }
        return '01-motor-gasolina/signature-series/5w-30/recorte-fondo-transparente-ASL.webp';
    }

    function findCatalogItemByCodeOrText(codeStr, titleStr) {
        if (codeStr) {
            const parts = codeStr.split(/[\/,\s()]+/).map((s) => s.trim().toUpperCase()).filter(Boolean);
            for (const p of parts) {
                if (CATALOG_BY_CODE[p]) return CATALOG_BY_CODE[p];
            }
        }
        if (titleStr) {
            const t = titleStr.toLowerCase();
            const match = CATALOG.find((it) => it.display_name.toLowerCase().includes(t) || t.includes(it.amsoil_code.toLowerCase()));
            if (match) return match;
        }
        return CATALOG_BY_ID['asl-5w-30'] || CATALOG[0];
    }

    // =========================================================================
    // 1. SELECTOR DE PRESENTACIÓN / ENVASE EN CADA TARJETA (.pres-switch-btn)
    // =========================================================================
    document.addEventListener('click', (e) => {
        const presBtn = e.target.closest('.pres-switch-btn');
        if (presBtn) {
            e.preventDefault();
            const tile = presBtn.closest('.amsoil-prod-tile');
            if (!tile) return;
            const imgEl = tile.querySelector('.prod-tile-photo');
            const newSrc = presBtn.dataset.imgSrc;
            if (imgEl && newSrc) {
                imgEl.src = newSrc;
            }
            tile.querySelectorAll('.pres-switch-btn').forEach((b) => b.classList.remove('active'));
            presBtn.classList.add('active');
        }
    });

    // =========================================================================
    // 2. MODAL DE FICHA TÉCNICA COMPLETA (PDS) CON GALERÍA DE ENVASES REALES
    // =========================================================================
    let modalBackdrop = document.getElementById('amsoilPdsModalBackdrop');
    if (!modalBackdrop) {
        modalBackdrop = document.createElement('div');
        modalBackdrop.id = 'amsoilPdsModalBackdrop';
        modalBackdrop.className = 'pds-modal-backdrop';
        modalBackdrop.innerHTML = `
            <div class="pds-modal-box" role="dialog" aria-modal="true" aria-labelledby="pdsModalTitle">
                <div class="pds-modal-top">
                    <div>
                        <span class="kicker" id="pdsModalCategory">FICHA TÉCNICA OFICIAL (PDS)</span>
                        <h3 id="pdsModalTitle">AMSOIL Product Data Sheet</h3>
                        <div id="pdsModalCode" style="font-size:0.86rem; color:#CACACD; margin-top:4px; font-weight:600;"></div>
                    </div>
                    <button type="button" class="pds-modal-close" id="pdsModalCloseBtn" aria-label="Cerrar Ficha Técnica">✕</button>
                </div>
                <div class="pds-modal-body">
                    <div class="pds-modal-hero-grid">
                        <div class="pds-modal-img-stage">
                            <img id="pdsModalMainImg" src="amsoil-logo.png" alt="Envase Oficial AMSOIL">
                            <div id="pdsModalImgCaption" style="font-size:0.78rem; font-weight:700; color:var(--amsoil-bunker); margin-top:8px; text-align:center;"></div>
                            <div id="pdsModalThumbs" class="pds-modal-thumbs"></div>
                        </div>
                        <div>
                            <p id="pdsModalSummary" style="font-size:0.95rem; color:#0F1416; margin-bottom:12px; line-height:1.55;"></p>
                            <h4 style="font-family:var(--font-heading); font-weight:800; font-size:1.08rem; text-transform:uppercase; color:var(--amsoil-red); margin-bottom:6px;">
                                Beneficios Técnicos Comprobados
                            </h4>
                            <ul id="pdsModalBenefits" class="pds-benefits-list"></ul>
                            <div class="pds-norm-box" style="margin-bottom:10px;">
                                <strong>Especificaciones, Aprobaciones y Normas Cubiertas (API / ACEA / JASO / OEM)</strong>
                                <span id="pdsModalNorms"></span>
                            </div>
                            <div class="pds-norm-box" style="border-left-color:var(--amsoil-red); margin-bottom:0;">
                                <strong>Intervalo de Servicio Recomendado (Vida Útil)</strong>
                                <span id="pdsModalServiceLife"></span>
                            </div>
                        </div>
                    </div>

                    <h4 style="font-family:var(--font-heading); font-weight:800; font-size:1.18rem; text-transform:uppercase; color:#0F1416; margin-bottom:10px;">
                        Presentaciones y Códigos Oficiales en Costa Rica (American Lubricants Supply S.A.)
                    </h4>
                    <div class="table-clean-wrap">
                        <table class="amsoil-clean-table" style="min-width:100%;">
                            <thead>
                                <tr>
                                    <th>Código / SKU</th>
                                    <th>Presentación / Envase</th>
                                    <th>Descripción Técnica Oficial</th>
                                    <th>Vista de Envase</th>
                                </tr>
                            </thead>
                            <tbody id="pdsModalTableBody"></tbody>
                        </table>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(modalBackdrop);

        const closeBtn = document.getElementById('pdsModalCloseBtn');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => modalBackdrop.classList.remove('open'));
        }
        modalBackdrop.addEventListener('click', (e) => {
            if (e.target === modalBackdrop) modalBackdrop.classList.remove('open');
        });
    }

    function openProductPdsModal(productIdOrItem) {
        const item = typeof productIdOrItem === 'string'
            ? (CATALOG_BY_ID[productIdOrItem] || findCatalogItemByCodeOrText(productIdOrItem, productIdOrItem))
            : productIdOrItem;
        if (!item) return;

        const tech = item.tech_sheet || {};
        const alsCodes = (item.als_codes || []).join(', ');
        document.getElementById('pdsModalCategory').textContent = `FICHA TÉCNICA OFICIAL (PDS) • ${item.category_name.toUpperCase()} • ${item.line_name.toUpperCase()}`;
        document.getElementById('pdsModalTitle').textContent = item.display_name;
        document.getElementById('pdsModalCode').textContent = `CÓDIGO AMSOIL: ${item.amsoil_code} • GRADO: ${item.viscosity || 'N/A'}${alsCodes ? ' • CÓDIGO ALS COSTA RICA: ' + alsCodes : ''}`;
        document.getElementById('pdsModalSummary').textContent = tech.summary || '';
        document.getElementById('pdsModalNorms').textContent = tech.specs || 'Especificación Oficial AMSOIL INC.';
        document.getElementById('pdsModalServiceLife').textContent = tech.service_life || 'Consultar manual del fabricante o guía técnica AMSOIL.';

        const benefitsUl = document.getElementById('pdsModalBenefits');
        benefitsUl.innerHTML = '';
        (tech.benefits || []).forEach((b) => {
            const li = document.createElement('li');
            li.textContent = b;
            benefitsUl.appendChild(li);
        });

        const images = item.images || [];
        const mainImg = document.getElementById('pdsModalMainImg');
        const imgCaption = document.getElementById('pdsModalImgCaption');
        const thumbsWrap = document.getElementById('pdsModalThumbs');
        thumbsWrap.innerHTML = '';

        const primaryImg = images.find((im) => im.filename.includes('recorte-fondo-transparente')) || images[0];
        if (primaryImg) {
            mainImg.src = primaryImg.rel_path;
            imgCaption.textContent = `${primaryImg.presentation || primaryImg.short_label} (${primaryImg.sku})`;
        }

        images.forEach((im) => {
            if (im.filename.includes('catalogo-latam')) return;
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'pds-thumb-btn' + (primaryImg && im.rel_path === primaryImg.rel_path ? ' active' : '');
            btn.textContent = im.filename.includes('recorte-fondo-transparente') ? 'Recorte PNG' : (im.short_label || im.sku);
            btn.addEventListener('click', () => {
                mainImg.src = im.rel_path;
                imgCaption.textContent = `${im.presentation || im.short_label} (${im.sku})`;
                thumbsWrap.querySelectorAll('.pds-thumb-btn').forEach((b) => b.classList.remove('active'));
                btn.classList.add('active');
            });
            thumbsWrap.appendChild(btn);
        });

        const tbody = document.getElementById('pdsModalTableBody');
        tbody.innerHTML = '';

        // Mostrar primero códigos oficiales de Costa Rica (ALS)
        (item.als_presentations || []).forEach((als) => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong style="color:var(--amsoil-red);">${als.code}</strong> <span style="font-size:0.75rem; color:var(--amsoil-blue);">(CR)</span></td>
                <td><strong>${als.presentation}</strong></td>
                <td>${als.description_pdf}</td>
                <td><span style="font-size:0.78rem; font-weight:700; color:var(--amsoil-shark);">Stock Costa Rica</span></td>
            `;
            tbody.appendChild(tr);
        });

        // Mostrar también todas las presentaciones fotográficas disponibles de AMSOIL USA
        images.forEach((im) => {
            if (!im.is_container || im.filename.includes('envase-principal')) return;
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${im.sku}</strong></td>
                <td>${im.short_label || im.presentation}</td>
                <td>${im.presentation}</td>
                <td><button type="button" class="pres-switch-btn" data-modal-preview="${im.rel_path}" data-modal-caption="${im.presentation} (${im.sku})">👁️ Ver Foto</button></td>
            `;
            tbody.appendChild(tr);
        });

        tbody.querySelectorAll('[data-modal-preview]').forEach((btn) => {
            btn.addEventListener('click', () => {
                mainImg.src = btn.dataset.modalPreview;
                imgCaption.textContent = btn.dataset.modalCaption;
            });
        });

        modalBackdrop.classList.add('open');
    }

    document.addEventListener('click', (e) => {
        const trigger = e.target.closest('[data-open-pds]');
        if (trigger) {
            e.preventDefault();
            openProductPdsModal(trigger.dataset.openPds);
        }
    });

    // =========================================================================
    // 3. BUSCADOR GLOBAL DEL HEADER Y FILTRO DE TABLA DE 105 PRODUCTOS
    // =========================================================================
    const headerGlobalSearchForm = document.getElementById('headerGlobalSearchForm');
    const headerGlobalSearchInput = document.getElementById('headerGlobalSearchInput');
    const aiVehicleQuery = document.getElementById('aiVehicleQuery');
    const aiVehicleMileage = document.getElementById('aiVehicleMileage');
    const selectEquipType = document.getElementById('selectEquipType');

    if (headerGlobalSearchForm && headerGlobalSearchInput) {
        headerGlobalSearchForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const q = headerGlobalSearchInput.value.trim();

            // Si el cliente hace clic en el botón sin haber escrito texto, llevarlo directo al buscador de vehículo
            if (!q) {
                const dock = document.getElementById('lookup-widget');
                if (dock) {
                    dock.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    if (aiVehicleQuery) aiVehicleQuery.focus();
                } else {
                    window.location.href = 'index.html#lookup-widget';
                }
                return;
            }

            // 1. Si estamos en la tabla de las 105 referencias (ingenieria.html), filtrar en vivo
            const catalogTableSearchInput = document.getElementById('catalogTableSearchInput');
            if (catalogTableSearchInput) {
                catalogTableSearchInput.value = q;
                catalogTableSearchInput.dispatchEvent(new Event('input'));
                catalogTableSearchInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
                return;
            }

            // 2. Si estamos en una página de categoría con tarjetas y la búsqueda coincide con productos de esa página
            const catTiles = document.querySelectorAll('.cat-page-layout .amsoil-prod-tile');
            if (catTiles.length > 0) {
                const qLower = q.toLowerCase();
                const qNorm = qLower.replace(/[-\s]/g, '');
                let matchCount = 0;
                catTiles.forEach((tile) => {
                    const text = (tile.textContent || '').toLowerCase();
                    const subcat = (tile.dataset.subcat || '').toLowerCase();
                    if (text.includes(qLower) || subcat.includes(qNorm)) {
                        tile.style.display = 'flex';
                        matchCount++;
                    } else {
                        tile.style.display = 'none';
                    }
                });
                if (matchCount > 0) {
                    const grid = document.querySelector('.cat-page-layout .amsoil-product-grid');
                    if (grid) grid.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    return;
                }
                // Si no coincidió con tarjetas de la categoría (ej. escribió un vehículo), restaurar y enviar al buscador general
                catTiles.forEach((tile) => { tile.style.display = 'flex'; });
            }

            // 3. Ejecutar búsqueda unificada (Vehículo, Motor, Maquinaria, Viscosidad o Tipo de Aceite)
            if (aiVehicleQuery) {
                aiVehicleQuery.value = q;
                const dock = document.getElementById('lookup-widget');
                if (dock) dock.scrollIntoView({ behavior: 'smooth', block: 'start' });
                executeAiLookup(q, aiVehicleMileage ? aiVehicleMileage.value : '');
            } else {
                window.location.href = `index.html?q=${encodeURIComponent(q)}#lookup-widget`;
            }
        });
    }

    const catalogTableSearchInput = document.getElementById('catalogTableSearchInput');
    if (catalogTableSearchInput) {
        catalogTableSearchInput.addEventListener('input', () => {
            const term = catalogTableSearchInput.value.trim().toLowerCase();
            document.querySelectorAll('[data-catalog-row]').forEach((row) => {
                const hay = row.dataset.catalogRow || '';
                row.style.display = !term || hay.includes(term) ? '' : 'none';
            });
        });
    }

    // =========================================================================
    // 4. RECOMENDADOR DE VEHÍCULOS Y BUSCADOR DE VISCOSIDAD / ACEITE AMSOIL
    // =========================================================================
    const aiAdvisorForm = document.getElementById('aiAdvisorForm');
    const aiLoadingState = document.getElementById('aiLoadingState');
    const aiResultPanel = document.getElementById('aiResultPanel');
    const presetChips = document.querySelectorAll('.preset-chip');

    const resCategoryBadge = document.getElementById('resCategoryBadge');
    const resMileageBadge = document.getElementById('resMileageBadge');
    const resVehicleTitle = document.getElementById('resVehicleTitle');
    const resVehicleSubtitle = document.getElementById('resVehicleSubtitle');
    const resViscosity = document.getElementById('resViscosity');
    const resCapacity = document.getElementById('resCapacity');
    const resNorm = document.getElementById('resNorm');
    const resFilter = document.getElementById('resFilter');
    const resWarning = document.getElementById('resWarning');
    const resMileageBox = document.getElementById('resMileageBox');
    const resMileageAdvice = document.getElementById('resMileageAdvice');
    const resAmsoilTiersGrid = document.getElementById('resAmsoilTiersGrid');
    const resFluidPackageGrid = document.getElementById('resFluidPackageGrid');

    function buildLocalAmsoilAdvisory(query, mileage) {
        const q = query.toLowerCase().trim();
        const qNorm = q.replace(/[-\s]/g, '');
        const km = mileage ? parseInt(mileage, 10) : null;
        const isHighMileage = km !== null && km >= 100000;

        // Si el cliente buscó directamente una viscosidad, código o tipo de aceite en el catálogo (ej. "5W-30", "75W-90", "ATF", "CVT", "DOT 4", "DME")
        const catalogMatches = CATALOG.filter((it) => {
            const viscNorm = (it.viscosity || '').toLowerCase().replace(/[-\s]/g, '');
            const codeLower = (it.amsoil_code || '').toLowerCase();
            const nameLower = (it.display_name || '').toLowerCase();
            const lineLower = (it.line_name || '').toLowerCase();
            return (
                (viscNorm && viscNorm === qNorm) ||
                codeLower === q ||
                nameLower.includes(q) ||
                lineLower.includes(q)
            );
        });

        const isVehicleKeyword = /(toyota|hilux|fortuner|prado|corolla|rav4|yaris|isuzu|d-max|dmax|ford|ranger|f-150|mitsubishi|l200|montero|nissan|frontier|navara|sentra|versa|honda|cr-v|crv|civic|hyundai|tucson|santa fe|kia|sportage|mazda|suzuki|vitara|jimny|chevrolet|vw|volkswagen|amarok|bmw|mercedes|audi|porsche|subaru|yamaha|ktm|crf|kawasaki|harley|polaris|can-am|cat|caterpillar|john deere|cummins|freightliner|mack|volvo|hino)/i.test(q);

        if (catalogMatches.length > 0 && !isVehicleKeyword) {
            const firstMatch = catalogMatches[0];
            const topThree = catalogMatches.slice(0, 3);
            const restMatches = catalogMatches.slice(3, 9);
            return {
                title: `Resultados de Catálogo: "${query.toUpperCase()}" (${catalogMatches.length} productos)`,
                subtitle: `${firstMatch.category_name} • ${firstMatch.line_name}`,
                categoryLabel: 'BÚSQUEDA DIRECTA DE PRODUCTO / VISCOSIDAD',
                viscosity: firstMatch.viscosity || 'Múltiples',
                capacity: `${catalogMatches.length} Referencias Oficiales`,
                norm: (firstMatch.tech_sheet && firstMatch.tech_sheet.specs ? firstMatch.tech_sheet.specs.split(',')[0] : 'API / OEM'),
                filter: `Código: ${firstMatch.amsoil_code}`,
                warning: firstMatch.tech_sheet?.summary || 'Haz clic en "Ver Ficha PDS" en cualquiera de los productos encontrados para revisar sus presentaciones y ficha técnica.',
                isHighMileage: false,
                reportedMileage: null,
                mileageAdvice: null,
                tiers: topThree.map((it, idx) => ({
                    badge: idx === 0 ? 'COINCIDENCIA PRINCIPAL' : it.category_short.toUpperCase(),
                    title: it.display_name,
                    code: it.amsoil_code,
                    interval: it.viscosity !== 'N/A' ? `SAE ${it.viscosity}` : '100% Sintético',
                    rationale: it.tech_sheet?.summary || ''
                })),
                fluids: restMatches.map((it) => ({
                    category: `${it.category_short} • SAE ${it.viscosity}`,
                    product: `${it.display_name} (${it.amsoil_code})`,
                    note: it.tech_sheet?.specs || ''
                }))
            };
        }

        let spec = {
            title: query,
            subtitle: 'Especificación Técnica Analizada • AMSOIL Costa Rica',
            categoryLabel: 'AUTOMOTRIZ GASOLINA / TURBO',
            viscosity: '5W-30',
            capacity: '4.7 Litros (5.0 Qt)',
            norm: 'API SP / ILSAC GF-6A',
            filter: 'OEM / Equivalente Sintético',
            warning: 'Utilizar lubricante 100% sintético para evitar formación de lodos en tráfico severo y proteger el tren de válvulas.',
            tiers: [],
            fluids: []
        };

        if (q.includes('hilux') || q.includes('fortuner') || q.includes('prado') || q.includes('1gd') || q.includes('2gd')) {
            spec = {
                title: query,
                subtitle: 'Motor Turbodiésel Toyota 1GD-FTV / 2GD-FTV Common-Rail Intercooler',
                categoryLabel: 'PICKUP / SUV TURBODIÉSEL 4X4',
                viscosity: '5W-30 / 15W-40',
                capacity: '7.5 Litros (7.9 Qt) con filtro',
                norm: 'API CK-4 / ACEA C2/C3 (Si equipa DPF)',
                filter: '90915-YZZD2 / Donaldson P550388',
                warning: 'En unidades con Filtro de Partículas Diésel (DPF Euro V/VI), emplear formulación Low-SAPS (5W-30) para evitar saturación de cenizas. En modelos sin DPF o trabajo pesado extremo, usar 15W-40 Max-Duty.'
            };
        } else if (q.includes('d-max') || q.includes('dmax') || q.includes('isuzu') || q.includes('4jj')) {
            spec = {
                title: query,
                subtitle: 'Motor Isuzu 3.0L / 2.5L Turbodiésel VGS Common-Rail',
                categoryLabel: 'PICKUP 4X4 TRABAJO PESADO',
                viscosity: '15W-40 / 5W-30',
                capacity: '7.6 Litros (8.0 Qt) con filtro',
                norm: 'API CK-4 / JASO DH-2',
                filter: '8-98165071-0 / Baldwin B7452',
                warning: 'Los motores Isuzu 4JJ1/4JJ3 requieren excelente control de hollín y estabilidad al cizallamiento para proteger la cadena de distribución y el turbocompresor VGS.'
            };
        } else if (q.includes('ranger') || q.includes('bi-turbo') || q.includes('everest')) {
            spec = {
                title: query,
                subtitle: 'Motor Ford EcoBlue / Puma Turbodiésel 4x4',
                categoryLabel: 'PICKUP 4X4 TURBODIÉSEL',
                viscosity: '5W-30',
                capacity: '6.8 a 8.6 Litros (según motor 2.0L / 3.2L)',
                norm: 'Ford WSS-M2C913-D / ACEA C2/A5/B5',
                filter: 'JU2Z-6731-A / Mann HU 7002 z',
                warning: 'En motores Ford 2.0L Bi-Turbo con faja bañada en aceite (wet belt), es crítico usar únicamente lubricante 100% sintético de baja fricción y respetar el intervalo.'
            };
        } else if (q.includes('l200') || q.includes('montero') || q.includes('4n15') || q.includes('mitsubishi')) {
            spec = {
                title: query,
                subtitle: 'Motor Mitsubishi 2.4L MIVEC Turbodiésel (4N15) / 2.5L DID',
                categoryLabel: 'PICKUP / SUV 4X4 DIÉSEL',
                viscosity: '5W-30 / 15W-40',
                capacity: '8.3 Litros (8.8 Qt) con filtro',
                norm: 'API CK-4 / ACEA C3 / JASO DL-1',
                filter: '1230A182 / Mann W 930/26',
                warning: 'El motor 4N15 con bloque de aluminio y alzado variable MIVEC requiere rápida lubricación en frío y limpieza extrema en los conductos hidráulicos.'
            };
        } else if (q.includes('rav4') || q.includes('prius') || q.includes('hibrid') || q.includes('hybrid') || q.includes('corolla')) {
            spec = {
                title: query,
                subtitle: 'Sistema Híbrido / Gasolina Dynamic Force Ciclo Atkinson',
                categoryLabel: 'VEHÍCULO HÍBRIDO / GASOLINA MODERNO',
                viscosity: '0W-16 (o 0W-20)',
                capacity: '4.5 Litros (4.8 Qt) con filtro',
                norm: 'API SP / ILSAC GF-6B',
                filter: '90915-YZZN1 / AMSOIL EA15K09',
                warning: 'Los motores híbridos experimentan constantes arranques y paradas en frío (Stop/Start), generando condensación de agua y dilución por combustible. Usar AMSOIL Hybrid 0W-16 o Signature Series.'
            };
        } else if (q.includes('cr-v') || q.includes('crv') || q.includes('civic') || q.includes('tucson') || q.includes('turbo')) {
            spec = {
                title: query,
                subtitle: 'Motor Gasolina Inyección Directa Turbo (GDI / T-GDI)',
                categoryLabel: 'SUV / SEDÁN TURBO GASOLINA',
                viscosity: '0W-20 / 5W-30',
                capacity: '3.7 a 4.8 Litros con filtro',
                norm: 'API SP / ILSAC GF-6A / dexos1 Gen 3',
                filter: '15400-PLM-A02 / AMSOIL EA15K13',
                warning: 'Los motores Turbo de inyección directa son propensos a pre-ignición a baja velocidad (LSPI) y dilución de gasolina en el cárter. AMSOIL Signature Series ofrece 100% de protección contra LSPI.'
            };
        } else if (q.includes('moto') || q.includes('yamaha') || q.includes('yz') || q.includes('ktm') || q.includes('crf') || q.includes('enduro') || q.includes('4t')) {
            spec = {
                title: query,
                subtitle: 'Motor 4 Tiempos de Alta Revolución con Embrague Húmedo Integrado',
                categoryLabel: 'MOTOCICLETA / ENDURO / ATV 4T',
                viscosity: '10W-40 (o 10W-50 / 20W-50)',
                capacity: '1.1 a 2.8 Litros (según cilindrada)',
                norm: 'JASO MA / MA2 • API SG/SL/CF',
                filter: 'HF140 / HF204',
                warning: 'No utilizar aceites de automóvil con modificadores de fricción en motocicletas con embrague bañado en aceite. Utilizar AMSOIL Metric o DIRT 4T certificado JASO MA2.'
            };
        } else if (q.includes('cat') || q.includes('caterpillar') || q.includes('320') || q.includes('john deere') || q.includes('freightliner') || q.includes('cummins') || q.includes('mack')) {
            spec = {
                title: query,
                subtitle: 'Motor Turbodiésel de Servicio Pesado / Maquinaria Amarilla',
                categoryLabel: 'MAQUINARIA PESADA & FLOTAS DIÉSEL',
                viscosity: '15W-40',
                capacity: '28.0 a 38.0 Litros (según configuración)',
                norm: 'API CK-4 / CAT ECF-3 / Cummins CES 20086',
                filter: '1R-1808 / Donaldson P551808',
                warning: 'En operación pesada por horas en clima tropical, controlar la oxidación térmica, dilución por azufre y retención de TBN con AMSOIL Signature Series Max-Duty 15W-40.'
            };
        }

        const isDiesel = spec.categoryLabel.includes('DIÉSEL') || spec.categoryLabel.includes('PESADO');
        const isMoto = spec.categoryLabel.includes('MOTO');

        if (isMoto) {
            spec.tiers = [
                {
                    badge: 'RECOMENDADO POWERSPORTS',
                    title: 'AMSOIL 100% Synthetic Metric Motorcycle Oil 10W-40',
                    code: 'MCF',
                    interval: 'Hasta 2X el intervalo OEM',
                    rationale: 'Máxima resistencia al cizallamiento en caja de cambios y acople firme de embrague húmedo JASO MA2.'
                },
                {
                    badge: 'ESPECIAL ENDURO / MOTOCROSS',
                    title: 'AMSOIL DIRT 10W-40 Synthetic Dirt Bike Oil',
                    code: 'DB40',
                    interval: 'Competencia y Barro Severo',
                    rationale: 'Diseñado específicamente para arranques de competencia y control de temperatura en senderos técnicos.'
                },
                {
                    badge: 'ALTA CILINDRADA / V-TWIN',
                    title: 'AMSOIL 20W-50 Synthetic V-Twin Motorcycle Oil',
                    code: 'MCV',
                    interval: 'Servicio Extendido Ruta',
                    rationale: 'Película gruesa para motores enfriados por aire o de gran torque sometidos a calor intenso.'
                }
            ];
            spec.fluids = [
                { category: 'Transmisión / Primaria Moto', product: 'AMSOIL Synthetic Dirt Bike Transmission Fluid (DBTF)', note: 'Para motos con compartimento de transmisión separado.' },
                { category: 'Aditivo de Combustible Moto', product: 'AMSOIL Motorcycle Octane Boost (MOB)', note: 'Maximiza la potencia y limpia el sistema de combustible en motores 4T y 2T.' },
                { category: 'Cadena y Suspensión', product: 'AMSOIL Chain Lube (ACL) & Shock Therapy® (STM)', note: 'No salpica ni atrae arena o barro en rutas de Costa Rica.' }
            ];
        } else if (isDiesel) {
            spec.tiers = [
                {
                    badge: 'RECOMENDADO MAX-DUTY DIESEL',
                    title: `AMSOIL Signature Series Max-Duty ${spec.viscosity.split('/')[0].trim()} Synthetic Diesel`,
                    code: spec.viscosity.includes('5W-30') ? 'DHD' : 'DME',
                    interval: '6X Protección Desgaste',
                    rationale: '6 veces más protección contra el desgaste del motor que el estándar Detroit Diesel DD13 y control total de hollín.'
                },
                {
                    badge: 'SERVICIO PESADO HEAVY-DUTY',
                    title: 'AMSOIL Heavy-Duty 100% Synthetic Diesel Oil 15W-40',
                    code: 'ADP',
                    interval: 'Trabajo Pesado Continuo',
                    rationale: 'Excelente protección térmica para turbocompresores y motores con alto kilometraje bajo carga.'
                },
                {
                    badge: 'ESPECIALIZADO DPF LOW-SAPS',
                    title: 'AMSOIL European 5W-30 Low-SAPS Synthetic',
                    code: 'AEL',
                    interval: 'Norma ACEA C2/C3',
                    rationale: 'Para unidades diésel modernas Euro V / Euro VI equipadas con filtros de partículas DPF sensibles.'
                }
            ];
            spec.fluids = [
                { category: 'Transmisión Automática / Manual', product: 'AMSOIL Signature Series Synthetic ATF (ATF)', note: 'Evita sobrecalentamiento de caja en ascensos con remolque o carga 4x4.' },
                { category: 'Diferenciales Delantero y Trasero 4x4', product: 'AMSOIL SEVERE GEAR® 75W-90 Easy-Pack (SVG)', note: 'Protección de presión extrema GL-5 frente a barro, agua y alto torque.' },
                { category: 'Sistema de Inyección Diésel', product: 'AMSOIL Diesel Injector Clean + Cetane Boost (ADS)', note: 'Lubrica la bomba e inyectores Common-Rail, limpia depósitos y eleva el cetano.' },
                { category: 'Lavado Interno Preventivo', product: 'AMSOIL Engine and Transmission Flush (FLSH)', note: 'Disuelve depósitos de hollín y barniz antes de instalar aceite 100% sintético.' },
                { category: 'Engrase de Chasis y Crucetas 4x4', product: 'AMSOIL Synthetic Polymeric Off-Road Grease (GPOR2)', note: 'Con disulfuro de molibdeno; resiste el lavado por agua en ríos y lluvia.' },
                { category: 'Sistema de Frenos y Enfriamiento', product: 'AMSOIL DOT 3 & DOT 4 Synthetic Brake Fluid (BFLV)', note: 'Punto de ebullición superior para descensos prolongados de montaña.' }
            ];
        } else {
            const primaryVisc = spec.viscosity.split('(')[0].split('/')[0].trim();
            const sigCode = primaryVisc === '0W-16' ? 'ASB' : (primaryVisc === '0W-20' ? 'ASM' : 'ASL');
            spec.tiers = [
                {
                    badge: 'LÍNEA INSIGNIA SIGNATURE SERIES',
                    title: `AMSOIL Signature Series ${primaryVisc} 100% Synthetic`,
                    code: sigCode,
                    interval: '75% Más Protección',
                    rationale: '75% más protección contra pérdida de potencia y desgaste. Máxima limpieza de pistones y turbo.'
                },
                {
                    badge: isHighMileage ? 'RECOMENDADO ALTO KILOMETRAJE (+100K KM)' : 'LÍNEA EXTENDIDA XL / HYBRID',
                    title: isHighMileage
                        ? `AMSOIL High-Mileage ${primaryVisc} 100% Synthetic`
                        : `AMSOIL XL / Hybrid ${primaryVisc} 100% Synthetic`,
                    code: isHighMileage ? 'HM530' : (primaryVisc === '0W-16' ? 'HE016' : 'XLF'),
                    interval: 'Protección Extendida',
                    rationale: isHighMileage
                        ? 'Formulado con acondicionadores de sellos que revitalizan retenes resecos, previenen fugas y reducen el consumo en motores con más de 100,000 km.'
                        : 'Protección reforzada contra degradación térmica y arranques frecuentes en ciudad.'
                },
                {
                    badge: 'LÍNEA OE (MANTENIMIENTO DE FÁBRICA)',
                    title: `AMSOIL OE ${primaryVisc} 100% Synthetic Motor Oil`,
                    code: primaryVisc === '0W-16' ? 'OES' : (primaryVisc === '0W-20' ? 'OEZ' : 'OEF'),
                    interval: 'Intervalo OEM Oficial',
                    rationale: 'Protección 100% sintética pura para cambios en el intervalo estándar del fabricante.'
                }
            ];
            spec.fluids = [
                { category: 'Transmisión Automática / CVT', product: 'AMSOIL Signature Fuel-Efficient ATF (ATL) / CVT (CVT)', note: 'Protección contra fricción y calor en cajas automáticas modernas y CVT.' },
                { category: 'Diferencial / AWD (Si aplica)', product: 'AMSOIL SEVERE GEAR® 75W-90 Easy-Pack (SVG)', note: 'Para versiones 4WD / AWD con diferencial trasero o caja de transferencia.' },
                { category: 'Limpieza de Inyectores Gasolina', product: 'AMSOIL P.i.® Performance Improver (API)', note: 'Limpia inyectores directos GDI, válvulas y cámara de combustión en un solo tanque.' },
                { category: 'Lavado Interno de Motor', product: 'AMSOIL Engine and Transmission Flush (FLSH)', note: 'Recomendado especialmente en motores con alto kilometraje para liberar anillos.' },
                { category: 'Líquido de Frenos Sintético', product: 'AMSOIL DOT 3 & DOT 4 Brake Fluid (BFLV)', note: 'Evita la sensación de pedal esponjoso en bajadas de montaña.' },
                { category: 'Refrigerante / Anticongelante', product: 'AMSOIL Passenger Car Antifreeze & Coolant (ANTPC)', note: 'Fórmula de larga duración para radiadores de aluminio modernos.' }
            ];
        }

        let mileageAdvice = null;
        if (km !== null && km > 0) {
            if (isHighMileage) {
                mileageAdvice = `Kilometraje registrado: ${km.toLocaleString('es-CR')} km. Por superar los 100,000 km, se recomienda lavado interno previo con AMSOIL Engine Flush y considerar AMSOIL High-Mileage o Signature Series para proteger sellos y retenes.`;
            } else {
                mileageAdvice = `Kilometraje registrado: ${km.toLocaleString('es-CR')} km. El motor mantiene tolerancias óptimas de fábrica; aplicar viscosidad OEM original con AMSOIL 100% Sintético.`;
            }
        }

        return {
            ...spec,
            isHighMileage,
            reportedMileage: km,
            mileageAdvice
        };
    }

    function renderAiAdvisoryResult(data, fallbackQuery) {
        if (!aiResultPanel) return;
        if (aiLoadingState) aiLoadingState.style.display = 'none';
        aiResultPanel.style.display = 'block';

        if (resVehicleTitle) resVehicleTitle.textContent = data.title || fallbackQuery;
        if (resVehicleSubtitle) resVehicleSubtitle.textContent = data.subtitle || 'Especificación técnica verificada por el Asesor AMSOIL Costa Rica';
        if (resViscosity) resViscosity.textContent = data.viscosity || '5W-30';
        if (resCapacity) resCapacity.textContent = data.capacity || 'Consultar manual';
        if (resNorm) resNorm.textContent = data.norm || 'API SP / OEM';
        if (resFilter) resFilter.textContent = data.filter || 'OEM Equivalente';
        if (resWarning) resWarning.textContent = data.warning || 'Utilizar siempre lubricación 100% sintética certificada.';

        const catMap = {
            turismo_gasolina: 'AUTOMOTRIZ GASOLINA / TURBO',
            turismo_hibrido: 'TECNOLOGÍA HÍBRIDA (HEV / PHEV)',
            turismo_diesel: 'PICKUP / SUV TURBODIÉSEL 4X4',
            pesado_flota: 'TRANSPORTE PESADO & FLOTAS',
            maquinaria: 'MAQUINARIA PESADA & AGRO'
        };
        if (resCategoryBadge) {
            resCategoryBadge.textContent = data.categoryLabel || catMap[data.vehicleCategory] || 'APLICACIÓN AMSOIL VERIFICADA';
        }

        if (resMileageBadge) {
            if (data.isHighMileage) {
                resMileageBadge.style.display = 'inline-block';
                resMileageBadge.textContent = `ALTO KILOMETRAJE (${(data.reportedMileage || 100000).toLocaleString('es-CR')} KM)`;
            } else {
                resMileageBadge.style.display = 'none';
            }
        }

        if (resMileageBox && resMileageAdvice) {
            if (data.mileageAdvice) {
                resMileageBox.style.display = 'block';
                resMileageAdvice.textContent = data.mileageAdvice;
            } else {
                resMileageBox.style.display = 'none';
            }
        }

        if (resAmsoilTiersGrid) {
            resAmsoilTiersGrid.innerHTML = '';
            let tiersList = [];
            if (Array.isArray(data.tiers)) {
                tiersList = data.tiers;
            } else if (data.amsoilTiers) {
                tiersList = [data.amsoilTiers.p1, data.amsoilTiers.p2, data.amsoilTiers.p3].filter(Boolean);
            }

            tiersList.forEach((tier, idx) => {
                const catItem = findCatalogItemByCodeOrText(tier.code, tier.title);
                const photoSrc = getPrimaryPhotoForCode(tier.code || (catItem ? catItem.amsoil_code : 'ASL'));
                const card = document.createElement('div');
                card.className = `guide-tier-box ${idx === 0 ? 'recommended' : ''}`;
                card.innerHTML = `
                    <div>
                        <span class="tier-kicker">${tier.badge || 'OPCIÓN AMSOIL'}</span>
                        <div class="guide-tier-img-wrap">
                            <img src="${photoSrc}" alt="${tier.title || 'AMSOIL'}">
                            <div>
                                <h4>${tier.title || ''}</h4>
                                <span style="font-size:0.78rem; font-weight:700; color:var(--amsoil-blue);">Código: ${tier.code || 'AMSOIL'}</span>
                            </div>
                        </div>
                        <p>${tier.rationale || ''}</p>
                    </div>
                    <div class="guide-tier-meta" style="align-items:center;">
                        <span style="color:var(--amsoil-red);">${tier.interval || '100% Sintético'}</span>
                        ${catItem ? `<button type="button" class="pres-switch-btn" data-open-pds="${catItem.id}">📋 Ver Ficha PDS</button>` : ''}
                    </div>
                `;
                resAmsoilTiersGrid.appendChild(card);
            });
        }

        if (resFluidPackageGrid) {
            resFluidPackageGrid.innerHTML = '';
            let fluidsList = [];
            if (Array.isArray(data.fluids)) {
                fluidsList = data.fluids;
            } else if (Array.isArray(data.fluidPackage)) {
                fluidsList = data.fluidPackage.filter((f) => !f.is_primary);
            }

            fluidsList.forEach((fl) => {
                const catItem = findCatalogItemByCodeOrText(fl.product, fl.product);
                const fCard = document.createElement('div');
                fCard.className = 'guide-fluid-card';
                fCard.innerHTML = `
                    <span>${fl.category || 'FLUIDO COMPLEMENTARIO'}</span>
                    <h5>${fl.product || ''}</h5>
                    <p>${fl.note || ''}</p>
                    ${catItem ? `<button type="button" class="pres-switch-btn" style="margin-top:6px;" data-open-pds="${catItem.id}">📋 Ver Ficha Técnica</button>` : ''}
                `;
                resFluidPackageGrid.appendChild(fCard);
            });
        }
    }

    async function executeAiLookup(query, mileage) {
        if (!query || !aiResultPanel) return;
        const fullQuery = selectEquipType && selectEquipType.value ? `${selectEquipType.value} - ${query}` : query;

        if (aiLoadingState) aiLoadingState.style.display = 'block';
        aiResultPanel.style.display = 'none';

        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 5000);

            const resp = await fetch('/api/lookup', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: fullQuery, mileage }),
                signal: controller.signal
            });
            clearTimeout(timeoutId);

            if (resp.ok) {
                const serverData = await resp.json();
                renderAiAdvisoryResult(serverData, query);
                return;
            }
        } catch (err) {
            // Fallback instantáneo
        }

        setTimeout(() => {
            const localData = buildLocalAmsoilAdvisory(fullQuery, mileage);
            renderAiAdvisoryResult(localData, query);
        }, 200);
    }

    if (aiAdvisorForm) {
        aiAdvisorForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const q = aiVehicleQuery ? aiVehicleQuery.value.trim() : '';
            const km = aiVehicleMileage ? aiVehicleMileage.value.trim() : '';
            executeAiLookup(q, km);
        });
    }

    presetChips.forEach((chip) => {
        chip.addEventListener('click', () => {
            const q = chip.dataset.query;
            const km = chip.dataset.km || '';
            if (aiVehicleQuery) aiVehicleQuery.value = q;
            if (aiVehicleMileage) aiVehicleMileage.value = km;
            executeAiLookup(q, km);
        });
    });

    const urlParams = new URLSearchParams(window.location.search);
    const paramQ = urlParams.get('q');
    const paramFilter = urlParams.get('filter');

    if (paramQ && aiVehicleQuery) {
        aiVehicleQuery.value = paramQ;
        executeAiLookup(paramQ, '');
    }

    // =========================================================================
    // 5. FILTRO EN PÁGINAS INTERNAS DE CATEGORÍA (Sidebar Filter + URL ?filter=)
    // =========================================================================
    const sidebarFilterLinks = document.querySelectorAll('[data-subfilter]');
    const catProductTiles = document.querySelectorAll('[data-subcat]');

    function applySubfilter(target, labelText) {
        const tLower = (target || 'all').toLowerCase();
        sidebarFilterLinks.forEach((l) => {
            l.classList.toggle('active', l.dataset.subfilter === target);
        });
        let visibleCount = 0;
        catProductTiles.forEach((tile) => {
            const tokens = (tile.dataset.subcat || '').toLowerCase().split(/\s+/).filter(Boolean);
            if (tLower === 'all' || tokens.includes(tLower)) {
                tile.style.display = 'flex';
                visibleCount++;
            } else {
                tile.style.display = 'none';
            }
        });

        let filterBanner = document.getElementById('activeSubfilterBanner');
        const mainContainer = document.querySelector('.cat-page-layout main');
        if (mainContainer && !filterBanner) {
            filterBanner = document.createElement('div');
            filterBanner.id = 'activeSubfilterBanner';
            filterBanner.style.cssText = 'display:none; align-items:center; justify-content:space-between; gap:12px; background:#F4F5F7; border-left:4px solid #CC262F; padding:12px 18px; margin-bottom:20px; border-radius:2px;';
            mainContainer.insertBefore(filterBanner, mainContainer.firstChild);
        }
        if (filterBanner) {
            if (tLower === 'all') {
                filterBanner.style.display = 'none';
            } else {
                const displayLabel = labelText || target.toUpperCase();
                filterBanner.style.display = 'flex';
                filterBanner.innerHTML = `
                    <div style="font-size:0.92rem; color:#0F1416;">
                        Filtro activo: <strong style="color:#CC262F;">${displayLabel}</strong> <span>(${visibleCount} ${visibleCount === 1 ? 'producto' : 'productos'})</span>
                    </div>
                    <button type="button" class="pres-switch-btn" id="clearSubfilterBtn" style="background:#0F1416; color:#FFFFFF; border-color:#0F1416;">
                        ✕ Ver todos los productos (${catProductTiles.length})
                    </button>
                `;
                const clearBtn = document.getElementById('clearSubfilterBtn');
                if (clearBtn) {
                    clearBtn.addEventListener('click', () => {
                        applySubfilter('all');
                        if (window.history && window.history.replaceState) {
                            window.history.replaceState({}, '', window.location.pathname);
                        }
                    });
                }
            }
        }
    }

    if (catProductTiles.length > 0) {
        sidebarFilterLinks.forEach((link) => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                applySubfilter(link.dataset.subfilter, link.textContent.trim());
            });
        });

        if (paramFilter) {
            const matchingMenuLink = document.querySelector(`.mega-menu a[href*="filter=${paramFilter}"]`);
            applySubfilter(paramFilter, matchingMenuLink ? matchingMenuLink.textContent.trim() : paramFilter);
        }

        // Interceptar clics del mega-menú o franja azul cuando ya estamos en esa misma página de categoría
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a[href*="?filter="]');
            if (!link) return;
            const href = link.getAttribute('href') || '';
            const [pagePart, queryPart] = href.split('?');
            const currentFile = window.location.pathname.split('/').pop() || 'index.html';
            if (pagePart === currentFile && queryPart) {
                const sp = new URLSearchParams(queryPart);
                const flt = sp.get('filter');
                if (flt) {
                    e.preventDefault();
                    applySubfilter(flt, link.textContent.trim());
                    if (window.history && window.history.replaceState) {
                        window.history.replaceState({}, '', `${pagePart}?filter=${flt}`);
                    }
                    const layoutEl = document.querySelector('.cat-page-layout');
                    if (layoutEl) layoutEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }
        });
    }

    // =========================================================================
    // 6. FILTRO DE PUNTOS DE VENTA Y TALLERES POR PROVINCIA + MAPA (contacto.html)
    // =========================================================================
    const provincePills = document.querySelectorAll('[data-prov-filter]');
    const dealerCards = document.querySelectorAll('[data-province]');
    const crInteractiveMap = document.getElementById('crInteractiveMapFrame');

    if (provincePills.length > 0 && dealerCards.length > 0) {
        provincePills.forEach((pill) => {
            pill.addEventListener('click', () => {
                const prov = pill.dataset.provFilter;
                const mapQuery = pill.dataset.mapQuery;

                provincePills.forEach((p) => p.classList.remove('active'));
                pill.classList.add('active');

                dealerCards.forEach((card) => {
                    if (prov === 'all' || card.dataset.province === prov) {
                        card.style.display = 'flex';
                    } else {
                        card.style.display = 'none';
                    }
                });

                if (crInteractiveMap && mapQuery) {
                    crInteractiveMap.src = `https://www.openstreetmap.org/export/embed.html?bbox=${mapQuery}&layer=mapnik`;
                }
            });
        });
    }

    const focusMapBtns = document.querySelectorAll('[data-bbox]');
    if (focusMapBtns.length > 0 && crInteractiveMap) {
        focusMapBtns.forEach((btn) => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const bbox = btn.dataset.bbox;
                const title = btn.dataset.dealerTitle;
                if (bbox) {
                    crInteractiveMap.src = `https://www.openstreetmap.org/export/embed.html?bbox=${bbox}&layer=mapnik`;
                    const mapTitleEl = document.getElementById('activeMapLocationTitle');
                    if (mapTitleEl && title) {
                        mapTitleEl.textContent = `Ubicación seleccionada: ${title}`;
                    }
                }
            });
        });
    }

    const contactForm = document.getElementById('amsoilContactForm');
    const contactFeedback = document.getElementById('contactFormFeedback');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const name = document.getElementById('contactName')?.value.trim() || 'Cliente';
            const zone = document.getElementById('contactZone')?.value || 'Costa Rica';
            if (contactFeedback) {
                contactFeedback.style.display = 'block';
                contactFeedback.textContent = `✓ Gracias ${name}. Hemos recibido tu mensaje desde ${zone}. Nuestro equipo de AMSOIL Costa Rica te contactará a la brevedad.`;
            }
            contactForm.reset();
        });
    }

    // =========================================================================
    // 7. BANNER TRANSITORIO PRINCIPAL (CARRUSEL HERO ESTILO AMSOIL.COM)
    // =========================================================================
    const heroCarousel = document.getElementById('amsoilHeroCarousel');
    if (heroCarousel) {
        const slides = heroCarousel.querySelectorAll('.hero-carousel-slide');
        const dots = heroCarousel.querySelectorAll('.carousel-dot');
        const prevBtn = heroCarousel.querySelector('.carousel-arrow-btn.prev');
        const nextBtn = heroCarousel.querySelector('.carousel-arrow-btn.next');
        const pauseBtn = heroCarousel.querySelector('.carousel-pause-btn');

        let currentSlide = 0;
        let isPaused = false;
        let timerId = null;

        function showSlide(index) {
            currentSlide = (index + slides.length) % slides.length;
            slides.forEach((sl, i) => sl.classList.toggle('active', i === currentSlide));
            dots.forEach((dt, i) => dt.classList.toggle('active', i === currentSlide));
        }

        function startTimer() {
            stopTimer();
            if (!isPaused) {
                timerId = setInterval(() => {
                    showSlide(currentSlide + 1);
                }, 6000);
            }
        }

        function stopTimer() {
            if (timerId) {
                clearInterval(timerId);
                timerId = null;
            }
        }

        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                showSlide(currentSlide - 1);
                startTimer();
            });
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                showSlide(currentSlide + 1);
                startTimer();
            });
        }

        dots.forEach((dot, idx) => {
            dot.addEventListener('click', () => {
                showSlide(idx);
                startTimer();
            });
        });

        if (pauseBtn) {
            pauseBtn.addEventListener('click', () => {
                isPaused = !isPaused;
                pauseBtn.setAttribute('aria-label', isPaused ? 'Reproducir banner' : 'Pausar banner');
                pauseBtn.innerHTML = isPaused
                    ? '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>'
                    : '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="5" width="4" height="14"/><rect x="14" y="5" width="4" height="14"/></svg>';
                if (isPaused) {
                    stopTimer();
                } else {
                    startTimer();
                }
            });
        }

        startTimer();
    }
});

