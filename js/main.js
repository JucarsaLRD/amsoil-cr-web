/**
 * AMSOIL COSTA RICA — INTERACTIVIDAD OFICIAL BAJO MANUAL DE MARCA AMSOIL INC.
 * Fuente: AMSOIL_BrandStyleGuide_7-26.pdf
 *
 * Cumplimiento estricto:
 * - Paleta oficial: #005BAA (Pantone 286), #ED1C24 (Pantone 485), #BCBEC0 (Cool Gray 6), #000000, #FFFFFF
 * - Tipografía digital oficial: Open Sans (Bold 700, Regular 400, Light 300)
 * - Nomenclatura oficial de productos + símbolos ® y cero códigos de almacén frente al cliente
 * - Máximo 1 logotipo AMSOIL por superficie visual (sin logos duplicados en modales o placeholders)
 */

document.addEventListener('DOMContentLoaded', () => {
    const CATALOG_HOME = 'index-catalogo.html';
    const TRANSPARENT_PIXEL = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';

    const ICON_DOC_SVG = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="8" y1="13" x2="16" y2="13"/><line x1="8" y1="17" x2="13" y2="17"/></svg>';
    const ICON_BOTTLE_SVG = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 3h6v3l3 4v10a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V10l3-4V3z"/></svg>';

    const CATALOG = Array.isArray(window.AMSOIL_CATALOG) ? window.AMSOIL_CATALOG : [];
    const CATALOG_BY_ID = {};
    const CATALOG_BY_CODE = {};

    CATALOG.forEach((item) => {
        CATALOG_BY_ID[item.id] = item;
        if (item.amsoil_code) {
            CATALOG_BY_CODE[item.amsoil_code.toUpperCase()] = item;
        }
    });

    function cleanPresentationLabel(rawLabel) {
        if (!rawLabel) return 'Envase Oficial';
        return rawLabel
            .replace(/\s*\([A-Z0-9-]{2,12}\)\s*/g, '')
            .replace('Vista Recorte PNG/WebP', 'Envase Oficial')
            .replace('Recorte con Fondo Transparente (WebP)', 'Envase Oficial AMSOIL')
            .trim();
    }

    function getPrimaryPhotoForCode(codeStr) {
        if (!codeStr || CATALOG.length === 0) {
            return '01-motor-gasolina/signature-series/5w-30/recorte-fondo-transparente-ASL.webp';
        }
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
            const t = titleStr.toLowerCase().replace(/®/g, '');
            const match = CATALOG.find((it) => {
                const dn = (it.display_name || '').toLowerCase().replace(/®/g, '');
                return dn.includes(t) || t.includes(dn);
            });
            if (match) return match;
        }
        return CATALOG_BY_ID['asl-5w-30'] || CATALOG[0];
    }

    // =========================================================================
    // 1. SELECTOR DE PRESENTACIÓN / ENVASE EN CADA TARJETA (.pres-switch-btn)
    // =========================================================================
    document.addEventListener('click', (e) => {
        const presBtn = e.target.closest('.pres-switch-btn');
        if (presBtn && presBtn.dataset.imgSrc) {
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
                        <span class="kicker" id="pdsModalCategory">Ficha Técnica Oficial (PDS)</span>
                        <h3 id="pdsModalTitle">AMSOIL Product Data Sheet</h3>
                        <div id="pdsModalMeta" style="font-size:0.85rem; color:var(--amsoil-cool-gray); margin-top:4px; font-weight:400;"></div>
                    </div>
                    <button type="button" class="pds-modal-close" id="pdsModalCloseBtn" aria-label="Cerrar Ficha Técnica">✕</button>
                </div>
                <div class="pds-modal-body">
                    <div class="pds-modal-hero-grid">
                        <div class="pds-modal-img-stage">
                            <img id="pdsModalMainImg" src="${TRANSPARENT_PIXEL}" alt="Envase Oficial AMSOIL">
                            <div id="pdsModalImgCaption" style="font-size:0.78rem; font-weight:700; color:var(--text-primary); margin-top:8px; text-align:center;"></div>
                            <div id="pdsModalThumbs" class="pds-modal-thumbs"></div>
                        </div>
                        <div>
                            <p id="pdsModalSummary" style="font-size:0.95rem; font-weight:300; color:var(--text-primary); margin-bottom:14px; line-height:1.6;"></p>
                            <h4 style="font-family:var(--font-heading); font-weight:700; font-size:1.02rem; color:var(--amsoil-red); margin-bottom:6px;">
                                Protección y Beneficios Técnicos Comprobados
                            </h4>
                            <ul id="pdsModalBenefits" class="pds-benefits-list"></ul>
                            <div class="pds-norm-box" style="margin-bottom:10px;">
                                <strong>Especificaciones, Aprobaciones y Normas Cubiertas (API / ACEA / JASO / OEM)</strong>
                                <span id="pdsModalNorms"></span>
                            </div>
                            <div class="pds-norm-box" style="border-left-color:var(--amsoil-red); margin-bottom:0;">
                                <strong>Intervalo de Servicio Recomendado</strong>
                                <span id="pdsModalServiceLife"></span>
                            </div>
                        </div>
                    </div>

                    <h4 style="font-family:var(--font-heading); font-weight:700; font-size:1.08rem; color:var(--text-primary); margin-bottom:10px;">
                        Presentaciones y Envases Disponibles en Costa Rica
                    </h4>
                    <div class="table-clean-wrap">
                        <table class="amsoil-clean-table" style="min-width:100%;">
                            <thead>
                                <tr>
                                    <th>Presentación</th>
                                    <th>Formato de Envase</th>
                                    <th>Disponibilidad</th>
                                    <th>Vista</th>
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
        const gradePart = item.viscosity && item.viscosity !== 'N/A' ? ` • Grado: ${item.viscosity}` : '';
        document.getElementById('pdsModalCategory').textContent = `Ficha Técnica Oficial (PDS) • ${item.category_short || item.category_name}`;
        document.getElementById('pdsModalTitle').textContent = item.display_name;
        document.getElementById('pdsModalMeta').textContent = `${item.line_name}${gradePart}`;
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
            mainImg.alt = item.display_name;
            imgCaption.textContent = cleanPresentationLabel(primaryImg.short_label || primaryImg.presentation);
        }

        images.forEach((im) => {
            if (im.filename.includes('catalogo-latam')) return;
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'pds-thumb-btn' + (primaryImg && im.rel_path === primaryImg.rel_path ? ' active' : '');
            btn.textContent = im.filename.includes('recorte-fondo-transparente')
                ? 'Vista Principal'
                : cleanPresentationLabel(im.short_label || im.presentation);
            btn.addEventListener('click', () => {
                mainImg.src = im.rel_path;
                imgCaption.textContent = cleanPresentationLabel(im.presentation || im.short_label);
                thumbsWrap.querySelectorAll('.pds-thumb-btn').forEach((b) => b.classList.remove('active'));
                btn.classList.add('active');
            });
            thumbsWrap.appendChild(btn);
        });

        const tbody = document.getElementById('pdsModalTableBody');
        tbody.innerHTML = '';

        // Presentaciones disponibles en Costa Rica (sin exponer códigos de almacén)
        (item.als_presentations || []).forEach((als) => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong style="color:var(--amsoil-blue);">${als.presentation}</strong></td>
                <td>${item.display_name}</td>
                <td><span style="font-size:0.8rem; font-weight:700; color:var(--text-primary);">Distribución Oficial CR</span></td>
                <td><span style="font-size:0.78rem; color:var(--text-muted);">Empaque Oficial</span></td>
            `;
            tbody.appendChild(tr);
        });

        // Presentaciones fotográficas oficiales AMSOIL INC.
        images.forEach((im) => {
            if (!im.is_container || im.filename.includes('envase-principal')) return;
            const cleanShort = cleanPresentationLabel(im.short_label || im.presentation);
            const cleanFull = cleanPresentationLabel(im.presentation);
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${cleanShort}</strong></td>
                <td>${cleanFull}</td>
                <td><span style="font-size:0.8rem; color:var(--text-secondary);">Envase AMSOIL INC.</span></td>
                <td><button type="button" class="pres-switch-btn" data-modal-preview="${im.rel_path}" data-modal-caption="${cleanFull}">${ICON_BOTTLE_SVG} Ver Envase</button></td>
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
    // 3. BUSCADOR GLOBAL DEL HEADER Y FILTRO DE DIRECTORIO TÉCNICO
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

            if (!q) {
                const dock = document.getElementById('lookup-widget');
                if (dock) {
                    dock.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    if (aiVehicleQuery) aiVehicleQuery.focus();
                } else {
                    window.location.href = `${CATALOG_HOME}#lookup-widget`;
                }
                return;
            }

            const catalogTableSearchInput = document.getElementById('catalogTableSearchInput');
            if (catalogTableSearchInput) {
                catalogTableSearchInput.value = q;
                catalogTableSearchInput.dispatchEvent(new Event('input'));
                catalogTableSearchInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
                return;
            }

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
                catTiles.forEach((tile) => { tile.style.display = 'flex'; });
            }

            if (aiVehicleQuery) {
                aiVehicleQuery.value = q;
                const dock = document.getElementById('lookup-widget');
                if (dock) dock.scrollIntoView({ behavior: 'smooth', block: 'start' });
                executeAiLookup(q, aiVehicleMileage ? aiVehicleMileage.value : '');
            } else {
                window.location.href = `${CATALOG_HOME}?q=${encodeURIComponent(q)}#lookup-widget`;
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
    // 4. RECOMENDADOR TÉCNICO DE VEHÍCULOS Y APLICACIONES AMSOIL
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

        const catalogMatches = CATALOG.filter((it) => {
            const viscNorm = (it.viscosity || '').toLowerCase().replace(/[-\s]/g, '');
            const nameLower = (it.display_name || '').toLowerCase();
            const lineLower = (it.line_name || '').toLowerCase();
            return (
                (viscNorm && viscNorm === qNorm) ||
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
                title: `Resultados del Catálogo: "${query}" (${catalogMatches.length} productos)`,
                subtitle: `${firstMatch.category_name} • ${firstMatch.line_name}`,
                categoryLabel: 'Búsqueda Directa de Viscosidad o Línea',
                viscosity: firstMatch.viscosity || 'Múltiples',
                capacity: `${catalogMatches.length} Referencias Oficiales`,
                norm: (firstMatch.tech_sheet && firstMatch.tech_sheet.specs ? firstMatch.tech_sheet.specs.split(',')[0] : 'API / OEM'),
                filter: firstMatch.category_short || 'AMSOIL INC.',
                warning: firstMatch.tech_sheet?.summary || 'Selecciona "Ver Ficha Técnica" en cualquiera de los productos encontrados para revisar sus especificaciones ASTM y envases.',
                isHighMileage: false,
                reportedMileage: null,
                mileageAdvice: null,
                tiers: topThree.map((it, idx) => ({
                    badge: idx === 0 ? 'Coincidencia Principal' : it.category_short,
                    title: it.display_name,
                    code: it.amsoil_code,
                    lineSubtitle: it.line_name,
                    interval: it.viscosity !== 'N/A' ? `SAE ${it.viscosity}` : 'Formulación Especializada',
                    rationale: it.tech_sheet?.summary || ''
                })),
                fluids: restMatches.map((it) => ({
                    category: `${it.category_short} • ${it.viscosity}`,
                    product: it.display_name,
                    code: it.amsoil_code,
                    note: it.tech_sheet?.specs || ''
                }))
            };
        }

        let spec = {
            title: query,
            subtitle: 'Especificación Técnica Analizada • AMSOIL Costa Rica',
            categoryLabel: 'Automotriz Gasolina / Turbo',
            viscosity: '5W-30',
            capacity: '4.7 Litros (5.0 Qt)',
            norm: 'API SP / ILSAC GF-6A',
            filter: 'OEM / Equivalente Sintético',
            warning: 'Diseñado con bases 100% sintéticas para máxima protección contra depósitos térmicos y desgaste del tren de válvulas.',
            tiers: [],
            fluids: []
        };

        if (q.includes('hilux') || q.includes('fortuner') || q.includes('prado') || q.includes('1gd') || q.includes('2gd')) {
            spec = {
                title: query,
                subtitle: 'Motor Turbodiésel Toyota 1GD-FTV / 2GD-FTV Common-Rail Intercooler',
                categoryLabel: 'Pickup / SUV Turbodiésel 4x4',
                viscosity: '5W-30 / 15W-40',
                capacity: '7.5 Litros (7.9 Qt) con filtro',
                norm: 'API CK-4 / ACEA C2/C3 (Unidades con DPF)',
                filter: '90915-YZZD2 / Donaldson P550388',
                warning: 'En unidades con Filtro de Partículas Diésel (DPF Euro V/VI), emplear formulación Low-SAPS 5W-30 para proteger el postratamiento. En modelos sin DPF bajo remolque pesado, emplear 15W-40 Max-Duty.'
            };
        } else if (q.includes('d-max') || q.includes('dmax') || q.includes('isuzu') || q.includes('4jj')) {
            spec = {
                title: query,
                subtitle: 'Motor Isuzu 3.0L / 2.5L Turbodiésel VGS Common-Rail',
                categoryLabel: 'Pickup 4x4 Trabajo Pesado',
                viscosity: '15W-40 / 5W-30',
                capacity: '7.6 Litros (8.0 Qt) con filtro',
                norm: 'API CK-4 / JASO DH-2',
                filter: '8-98165071-0 / Baldwin B7452',
                warning: 'Los motores Isuzu 4JJ1/4JJ3 demandan alta estabilidad al cizallamiento y control de hollín para proteger la cadena de distribución y el turbocompresor VGS.'
            };
        } else if (q.includes('ranger') || q.includes('bi-turbo') || q.includes('everest')) {
            spec = {
                title: query,
                subtitle: 'Motor Ford EcoBlue / Puma Turbodiésel 4x4',
                categoryLabel: 'Pickup 4x4 Turbodiésel',
                viscosity: '5W-30',
                capacity: '6.8 a 8.6 Litros (según motor 2.0L / 3.2L)',
                norm: 'Ford WSS-M2C913-D / ACEA C2/A5/B5',
                filter: 'JU2Z-6731-A / Mann HU 7002 z',
                warning: 'En motores Ford 2.0L Bi-Turbo con faja húmeda (wet belt), es indispensable utilizar lubricante 100% sintético formulado para baja fricción y respetar rigurosamente el intervalo.'
            };
        } else if (q.includes('l200') || q.includes('montero') || q.includes('4n15') || q.includes('mitsubishi')) {
            spec = {
                title: query,
                subtitle: 'Motor Mitsubishi 2.4L MIVEC Turbodiésel (4N15) / 2.5L DID',
                categoryLabel: 'Pickup / SUV 4x4 Diésel',
                viscosity: '5W-30 / 15W-40',
                capacity: '8.3 Litros (8.8 Qt) con filtro',
                norm: 'API CK-4 / ACEA C3 / JASO DL-1',
                filter: '1230A182 / Mann W 930/26',
                warning: 'El motor 4N15 con bloque de aluminio y sistema MIVEC requiere fluidez inmediata en arranque y máxima limpieza en los actuadores hidráulicos.'
            };
        } else if (q.includes('rav4') || q.includes('prius') || q.includes('hibrid') || q.includes('hybrid') || q.includes('corolla')) {
            spec = {
                title: query,
                subtitle: 'Sistema Híbrido / Gasolina Dynamic Force Ciclo Atkinson',
                categoryLabel: 'Vehículo Híbrido / Gasolina Moderno',
                viscosity: '0W-16 (o 0W-20)',
                capacity: '4.5 Litros (4.8 Qt) con filtro',
                norm: 'API SP / ILSAC GF-6B',
                filter: '90915-YZZN1',
                warning: 'Los motores híbridos operan con ciclos constantes de paro y arranque que generan condensación de humedad y dilución de combustible. AMSOIL 100% Synthetic Hybrid Motor Oil neutraliza la corrosión y protege al instante.'
            };
        } else if (q.includes('cr-v') || q.includes('crv') || q.includes('civic') || q.includes('tucson') || q.includes('turbo')) {
            spec = {
                title: query,
                subtitle: 'Motor Gasolina Inyección Directa Turbo (GDI / T-GDI)',
                categoryLabel: 'SUV / Sedán Turbo Gasolina',
                viscosity: '0W-20 / 5W-30',
                capacity: '3.7 a 4.8 Litros con filtro',
                norm: 'API SP / ILSAC GF-6A / GM dexos1 Gen 3',
                filter: '15400-PLM-A02',
                warning: 'Los motores Turbo de inyección directa exigen protección total contra la pre-ignición a baja velocidad (LSPI). AMSOIL Signature Series alcanzó 100% de protección contra LSPI en pruebas ASTM.'
            };
        } else if (q.includes('moto') || q.includes('yamaha') || q.includes('yz') || q.includes('ktm') || q.includes('crf') || q.includes('enduro') || q.includes('4t')) {
            spec = {
                title: query,
                subtitle: 'Motor 4 Tiempos de Alta Revolución con Embrague Húmedo Integrado',
                categoryLabel: 'Motocicleta / Enduro / ATV 4T',
                viscosity: '10W-40 (o 10W-50 / 20W-50)',
                capacity: '1.1 a 2.8 Litros (según cilindrada)',
                norm: 'JASO MA / MA2 • API SG/SL/CF',
                filter: 'HF140 / HF204',
                warning: 'Emplear exclusivamente lubricantes formulados sin modificadores de fricción para embrague húmedo JASO MA2, garantizando cambios precisos y máxima resistencia al calor.'
            };
        } else if (q.includes('cat') || q.includes('caterpillar') || q.includes('320') || q.includes('john deere') || q.includes('freightliner') || q.includes('cummins') || q.includes('mack')) {
            spec = {
                title: query,
                subtitle: 'Motor Turbodiésel de Servicio Pesado / Flota y Maquinaria',
                categoryLabel: 'Flotas Pesadas y Maquinaria Diésel',
                viscosity: '15W-40',
                capacity: '28.0 a 38.0 Litros (según configuración)',
                norm: 'API CK-4 / CAT ECF-3 / Cummins CES 20086',
                filter: '1R-1808 / Donaldson P551808',
                warning: 'Formulado para reducir el costo total de propiedad (TCO) en operación continua bajo carga severa, manteniendo la retención de TBN y entregando 6X más protección contra desgaste en Detroit Diesel DD13.'
            };
        }

        const isDiesel = spec.categoryLabel.toUpperCase().includes('DIÉSEL') || spec.categoryLabel.toUpperCase().includes('PESADO');
        const isMoto = spec.categoryLabel.toUpperCase().includes('MOTO');

        if (isMoto) {
            spec.tiers = [
                {
                    badge: 'Recomendado Powersports',
                    title: 'AMSOIL 10W-40 100% Synthetic Metric Motorcycle Oil',
                    code: 'MCF',
                    lineSubtitle: 'Certificación JASO MA2 • Embrague Húmedo',
                    interval: 'Cambios Suaves y Precisos',
                    rationale: 'Diseñado específicamente para proteger engranajes y embragues húmedos frente al calor extremo y altas RPM.'
                },
                {
                    badge: 'Enduro y Motocross',
                    title: 'AMSOIL 10W-40 100% Synthetic Dirt Bike Oil',
                    code: 'DB40',
                    lineSubtitle: 'Competencia Off-Road • JASO MA',
                    interval: 'Sensación Consistente de Embrague',
                    rationale: 'Formulado para arranques explosivos en pista y máxima resistencia al desgaste en barro y senderos exigentes.'
                },
                {
                    badge: 'Alta Cilindrada / V-Twin',
                    title: 'AMSOIL 20W-50 100% Synthetic V-Twin Motorcycle Oil',
                    code: 'MCV',
                    lineSubtitle: 'Motores Enfriados por Aire • JASO MA2',
                    interval: '6X Mayor Resistencia a Degradación',
                    rationale: 'Película sintética robusta para motores V-Twin de alto torque sometidos a temperaturas extremas.'
                }
            ];
            spec.fluids = [
                { category: 'Transmisión Separada Moto', product: 'AMSOIL 100% Synthetic Dirt Bike Transmission Fluid', code: 'DBTF', note: 'Protección especializada para cajas de cambios de 2 y 4 tiempos.' },
                { category: 'Aditivo de Combustible Moto', product: 'AMSOIL Motorcycle Octane Boost', code: 'MOB', note: 'Maximiza la potencia, ayuda a eliminar el cascabeleo y limpia depósitos.' },
                { category: 'Suspensión de Alto Rendimiento', product: 'AMSOIL Shock Therapy® #10 Medium Suspension Fluid', code: 'STM', note: 'Controla la fricción y evita la pérdida de amortiguación por espuma.' }
            ];
        } else if (isDiesel) {
            const primaryDieselVisc = spec.viscosity.split('/')[0].trim();
            spec.tiers = [
                {
                    badge: 'Máxima Protección Max-Duty',
                    title: `AMSOIL Signature Series Max-Duty ${primaryDieselVisc} 100% Synthetic Diesel Oil`,
                    code: primaryDieselVisc.includes('5W-30') ? 'DHD' : 'DME',
                    lineSubtitle: 'API CK-4 • Serie Insignia Turbodiésel',
                    interval: '6X Más Protección Contra Desgaste',
                    rationale: 'Entrega 6 veces más protección contra el desgaste del motor que el estándar Detroit Diesel DD13 y mantiene los turbos limpios.'
                },
                {
                    badge: 'Servicio Pesado Heavy-Duty',
                    title: 'AMSOIL Heavy-Duty 15W-40 100% Synthetic Diesel Oil',
                    code: 'ADP',
                    lineSubtitle: 'API CK-4 • Trabajo Continuo',
                    interval: '4X Más Protección Contra Desgaste',
                    rationale: 'Estabilidad térmica superior y bajo consumo de aceite para pickups de carga, camiones y maquinaria.'
                },
                {
                    badge: 'Especializado DPF Euro V/VI',
                    title: 'AMSOIL European Car Formula 5W-30 LS 100% Synthetic Motor Oil',
                    code: 'AEL',
                    lineSubtitle: 'Low-SAPS • ACEA C3',
                    interval: 'Protección Avanzada de DPF',
                    rationale: 'Formulación baja en cenizas sulfatadas diseñada para proteger filtros de partículas diésel modernos.'
                }
            ];
            spec.fluids = [
                { category: 'Transmisión Automática', product: 'AMSOIL Signature Series Multi-Vehicle 100% Synthetic ATF (Red)', code: 'ATF', note: 'Resiste el calor severo al remolcar o ascender pendientes pronunciadas.' },
                { category: 'Diferenciales 4x4', product: 'AMSOIL SEVERE GEAR® 75W-90 100% Synthetic Gear Lube', code: 'SVG', note: 'Película de presión extrema en envase flexible Easy-Pack para cambios limpios.' },
                { category: 'Inyección Common-Rail', product: 'AMSOIL Diesel Injector Clean + Cetane Boost', code: 'ADS', note: 'Limpia inyectores diésel, lubrica bombas de alta presión y eleva el cetano hasta en 8 puntos.' },
                { category: 'Lavado Interno Preventivo', product: 'AMSOIL Engine & Transmission Flush', code: 'FLSH', note: 'Disuelve lodos y depósitos de hollín antes de instalar lubricante 100% sintético.' },
                { category: 'Chasis y Crucetas Off-Road', product: 'AMSOIL NLGI #2 100% Synthetic Polymeric Off-Road Grease', code: 'GPOR2', note: 'Reforzada contra impacto extremo y lavado por agua o barro.' },
                { category: 'Sistema de Frenos', product: 'AMSOIL DOT 3 & DOT 4 100% Synthetic Brake Fluid', code: 'BFLV', note: 'Alto punto de ebullición para frenadas firmes y seguras con carga en montaña.' }
            ];
        } else {
            const primaryVisc = spec.viscosity.split('(')[0].split('/')[0].trim();
            const sigCode = primaryVisc === '0W-16' ? 'HE016' : (primaryVisc === '0W-20' ? 'ASM' : 'ASL');
            spec.tiers = [
                {
                    badge: 'Línea Insignia Signature Series',
                    title: primaryVisc === '0W-16'
                        ? 'AMSOIL 0W-16 100% Synthetic Hybrid Motor Oil'
                        : `AMSOIL Signature Series ${primaryVisc} 100% Synthetic Motor Oil`,
                    code: sigCode,
                    lineSubtitle: 'API SP / ILSAC GF-6 • Máximo Rendimiento',
                    interval: '75% Más Protección Contra Desgaste',
                    rationale: 'Ingenierizado para máxima protección y rendimiento: 75% más protección contra desgaste y 40% pistones más limpios en pruebas ASTM.'
                },
                {
                    badge: isHighMileage ? 'Especializado Alto Kilometraje' : 'Protección Extendida XL / Hybrid',
                    title: isHighMileage
                        ? `AMSOIL ${primaryVisc === '0W-16' ? '5W-30' : primaryVisc} 100% Synthetic High-Mileage Motor Oil`
                        : (primaryVisc === '0W-20'
                            ? 'AMSOIL 0W-20 100% Synthetic Hybrid Motor Oil'
                            : 'AMSOIL XL 5W-30 100% Synthetic Motor Oil'),
                    code: isHighMileage ? 'HM530' : (primaryVisc === '0W-20' ? 'HE020' : 'XLF'),
                    lineSubtitle: isHighMileage ? 'Acondicionadores de Sellos Activos' : 'Resistencia Térmica Reforzada',
                    interval: 'Protección Comprobada',
                    rationale: isHighMileage
                        ? 'Formulado para motores con más de 100,000 km: revitaliza retenes, previene fugas y combate la degradación.'
                        : 'Neutraliza ácidos y protege frente a ciclos constantes de arranque y tráfico urbano.'
                },
                {
                    badge: 'Mantenimiento OEM',
                    title: `AMSOIL OE ${primaryVisc === '0W-16' ? '0W-20' : primaryVisc} 100% Synthetic Motor Oil`,
                    code: primaryVisc === '0W-20' || primaryVisc === '0W-16' ? 'OEZ' : 'OEF',
                    lineSubtitle: 'API SP / ILSAC GF-6 • Intervalo OEM',
                    interval: '100% Sintético Puro',
                    rationale: 'Protección superior contra desgaste y LSPI durante todo el intervalo recomendado por el fabricante.'
                }
            ];
            spec.fluids = [
                { category: 'Transmisión Automática / CVT', product: 'AMSOIL Signature Series Fuel-Efficient 100% Synthetic ATF (Blue)', code: 'ATL', note: 'Cambios suaves y máxima estabilidad frente al calor en transmisiones modernas.' },
                { category: 'Diferencial / AWD', product: 'AMSOIL SEVERE GEAR® 75W-90 100% Synthetic Gear Lube', code: 'SVG', note: 'Protección extrema para diferenciales traseros y cajas de transferencia AWD/4WD.' },
                { category: 'Sistema de Combustible Gasolina', product: 'AMSOIL P.i.® Performance Improver Gasoline Additive', code: 'API', note: 'Elimina depósitos difíciles en inyectores y válvulas para restaurar potencia y economía de combustible.' },
                { category: 'Lavado Interno de Motor', product: 'AMSOIL Engine & Transmission Flush', code: 'FLSH', note: 'Limpia depósitos acumulados y libera anillos en un solo servicio.' },
                { category: 'Líquido de Frenos Sintético', product: 'AMSOIL DOT 3 & DOT 4 100% Synthetic Brake Fluid', code: 'BFLV', note: 'Respuesta firme del pedal y protección contra corrosión interna.' },
                { category: 'Sistema de Enfriamiento', product: 'AMSOIL Passenger Car & Light Truck Antifreeze & Coolant 50/50', code: 'ANTPC', note: 'Fórmula premezclada de larga duración para bloques y radiadores de aluminio.' }
            ];
        }

        let mileageAdvice = null;
        if (km !== null && km > 0) {
            if (isHighMileage) {
                mileageAdvice = `Kilometraje registrado: ${km.toLocaleString('es-CR')} km. Para motores sobre 100,000 km recomendamos realizar limpieza previa con AMSOIL Engine & Transmission Flush y proteger con AMSOIL 100% Synthetic High-Mileage Motor Oil o AMSOIL Signature Series.`;
            } else {
                mileageAdvice = `Kilometraje registrado: ${km.toLocaleString('es-CR')} km. Mantén la viscosidad OEM de fábrica con lubricación 100% sintética AMSOIL para conservar los componentes internos limpios y sin desgaste.`;
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
        if (resVehicleSubtitle) resVehicleSubtitle.textContent = data.subtitle || 'Especificación técnica verificada por AMSOIL Costa Rica';
        if (resViscosity) resViscosity.textContent = data.viscosity || '5W-30';
        if (resCapacity) resCapacity.textContent = data.capacity || 'Consultar manual';
        if (resNorm) resNorm.textContent = data.norm || 'API SP / OEM';
        if (resFilter) resFilter.textContent = data.filter || 'OEM Equivalente';
        if (resWarning) resWarning.textContent = data.warning || 'Utilizar siempre lubricación 100% sintética certificada.';

        const catMap = {
            turismo_gasolina: 'Automotriz Gasolina / Turbo',
            turismo_hibrido: 'Tecnología Híbrida (HEV / PHEV)',
            turismo_diesel: 'Pickup / SUV Turbodiésel 4x4',
            pesado_flota: 'Transporte Pesado y Flotas',
            maquinaria: 'Maquinaria Pesada y Agro'
        };
        if (resCategoryBadge) {
            resCategoryBadge.textContent = data.categoryLabel || catMap[data.vehicleCategory] || 'Guía de Aplicación AMSOIL';
        }

        if (resMileageBadge) {
            if (data.isHighMileage) {
                resMileageBadge.style.display = 'inline-block';
                resMileageBadge.textContent = `Alto Kilometraje (${(data.reportedMileage || 100000).toLocaleString('es-CR')} km)`;
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
                const displayTitle = catItem ? catItem.display_name : (tier.title || '');
                const subLine = tier.lineSubtitle || (catItem ? catItem.line_name : 'Lubricante Sintético Especializado');
                const photoSrc = getPrimaryPhotoForCode(tier.code || (catItem ? catItem.amsoil_code : 'ASL'));
                const card = document.createElement('div');
                card.className = `guide-tier-box ${idx === 0 ? 'recommended' : ''}`;
                card.innerHTML = `
                    <div>
                        <span class="tier-kicker">${tier.badge || 'Recomendación AMSOIL'}</span>
                        <div class="guide-tier-img-wrap">
                            <img src="${photoSrc}" alt="${displayTitle}">
                            <div>
                                <h4>${displayTitle}</h4>
                                <span style="font-size:0.76rem; font-weight:700; color:var(--amsoil-blue);">${subLine}</span>
                            </div>
                        </div>
                        <p>${tier.rationale || ''}</p>
                    </div>
                    <div class="guide-tier-meta">
                        <span style="color:var(--amsoil-red);">${tier.interval || 'Protección Comprobada'}</span>
                        ${catItem ? `<button type="button" class="pres-switch-btn" data-open-pds="${catItem.id}">${ICON_DOC_SVG} Ficha PDS</button>` : ''}
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
                const catItem = findCatalogItemByCodeOrText(fl.code || fl.product, fl.product);
                const cleanProdTitle = catItem ? catItem.display_name : (fl.product || '').replace(/\s*\([A-Z0-9-]{2,8}\)\s*$/g, '');
                const fCard = document.createElement('div');
                fCard.className = 'guide-fluid-card';
                fCard.innerHTML = `
                    <span>${fl.category || 'Fluido Complementario'}</span>
                    <h5>${cleanProdTitle}</h5>
                    <p>${fl.note || ''}</p>
                    ${catItem ? `<button type="button" class="pres-switch-btn" style="margin-top:8px;" data-open-pds="${catItem.id}">${ICON_DOC_SVG} Ver Ficha Técnica</button>` : ''}
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
            // Respaldo instantáneo local
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
    // 5. FILTRO EN PÁGINAS DE CATEGORÍA (?filter=...)
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
            filterBanner.style.cssText = 'display:none; align-items:center; justify-content:space-between; gap:12px; background:var(--bg-light); border:1px solid var(--border-gray); border-left:4px solid var(--amsoil-red); padding:12px 18px; margin-bottom:20px; border-radius:2px;';
            mainContainer.insertBefore(filterBanner, mainContainer.firstChild);
        }
        if (filterBanner) {
            if (tLower === 'all') {
                filterBanner.style.display = 'none';
            } else {
                const displayLabel = labelText || target;
                filterBanner.style.display = 'flex';
                filterBanner.innerHTML = `
                    <div style="font-size:0.92rem; color:var(--text-primary);">
                        Filtro activo: <strong style="color:var(--amsoil-red);">${displayLabel}</strong> <span>(${visibleCount} ${visibleCount === 1 ? 'producto' : 'productos'})</span>
                    </div>
                    <button type="button" class="pres-switch-btn" id="clearSubfilterBtn" style="background:var(--amsoil-black); color:var(--amsoil-white); border-color:var(--amsoil-black);">
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

        document.addEventListener('click', (e) => {
            const link = e.target.closest('a[href*="?filter="]');
            if (!link) return;
            const href = link.getAttribute('href') || '';
            const [pagePart, queryPart] = href.split('?');
            const currentFile = window.location.pathname.split('/').pop() || CATALOG_HOME;
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
                contactFeedback.textContent = `✓ Gracias ${name}. Hemos recibido tu consulta desde ${zone}. Un especialista técnico de AMSOIL Costa Rica te responderá a la brevedad.`;
            }
            contactForm.reset();
        });
    }

    // =========================================================================
    // 7. CARRUSEL PRINCIPAL DE PRODUCTOS Y RENDIMIENTO
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
