# Repositorio de Imágenes y Datos — AMSOIL Costa Rica (American Lubricants Supply S.A.)

Este directorio contiene **627 imágenes verificadas de alta resolución (84 MB)** organizadas en **105 carpetas de productos y viscosidades**, junto con índices estructurados en JSON, JS y CSV listos para ser consumidos por cualquier página o aplicación web.

## 📍 Ubicaciones Disponibles en el Sistema

1. **Carpeta Principal en Documentos:**
   `/Users/Osito/Documents/AMSOIL-Costa-Rica/`
2. **Espejo en el Scratch de Antigravity (accesible desde el Sandbox sin permisos adicionales):**
   `/Users/Osito/.gemini/antigravity/scratch/amsoil-imagenes/`

---

## 🗂️ Archivos Índice para Consumir Programáticamente

| Archivo | Descripción |
| :--- | :--- |
| `catalogo-imagenes.json` | JSON completo con los **105 productos**, nombres, viscosidades, código oficial AMSOIL (`amsoil_code`), códigos de American Lubricants Supply (`als_codes`, `als_presentations`), ficha técnica en español (`tech_sheet`: `summary`, `benefits`, `specs`, `service_life`) y arreglo `images` con las rutas relativas (`rel_path`), SKU de envase (`sku`) y etiqueta corta (`short_label`). |
| `catalogo-datos.js` | Mismo contenido exportado como `window.AMSOIL_CATALOG = [...]` para carga directa mediante `<script src="catalogo-datos.js"></script>` sin restricciones CORS en `file://`. |
| `catalogo-imagenes.csv` | Tabla plana con las 627 imágenes (`product_index`, `category`, `line`, `viscosity`, `amsoil_code`, `als_codes`, `display_name`, `presentation`, `sku`, `rel_path`, `bytes`). |
| `amsoil-logo.png` | Logotipo oficial AMSOIL en alta resolución con fondo transparente (`596x184` RGBA PNG). |

---

## 📁 Estructura de Carpetas de Imágenes

Las imágenes están organizadas jerárquicamente en **3 niveles**:
`<categoría>/<línea-de-producto>/<viscosidad-o-tipo>/<presentación>-<SKU>.<ext>`

### Las 5 Categorías Principales:
1. `01-motor-gasolina/`
   - `oe-synthetic/` (`0w-16`, `0w-20`, `5w-20`, `5w-30`, `10w-30`)
   - `xl-synthetic/` (`0w-20`, `5w-20`, `5w-30`, `10w-30`, `10w-40`, `10w-40-25gal`)
   - `european-car-formula/` (`0w-20-ls-vw`, `5w-30-ls`, `0w-40-fs`, `5w-40-ms`, `5w-40-fs`)
   - `hybrid/` (`0w-16`, `0w-20`)
   - `signature-series/` (`0w-20`, `0w-30`, `5w-20`, `5w-30`, `10w-30`, `0w-40`, `5w-50`)
   - `racing-zrod-dominator/` (`z-rod-10w-30`, `z-rod-10w-40`, `z-rod-20w-50`, `dominator-5w-20`, `dominator-10w-30`, `dominator-15w-50`, `dominator-60`, `briggs-stratton-4t`, `assembly-lube`)
   - `high-mileage/` (`0w-20`, `5w-20`, `5w-30`, `10w-30`)
2. `02-motor-diesel/`
   - `heavy-duty-ck4/` (`5w-40`, `10w-30`, `15w-40`)
   - `commercial-synthetic-blend/` (`15w-40-blend`)
   - `diesel-dexos-d/` (`0w-20-dexos-d`)
   - `signature-series-max-duty/` (`5w-30`, `5w-40`, `10w-30`, `15w-40`)
3. `03-transmision-y-diferenciales/`
   - `severe-gear-y-diferenciales/` (`75w-85`, `75w-90`, `75w-110`, `75w-140`, `80w-90`, `severe-gear-ep-75w-90`, `severe-gear-ep-75w-140`, `severe-gear-racing-190`, `severe-gear-racing-250`, `slip-lock-additive`)
   - `transmision-automatica-atf-cvt-dct/` (`oe-atf`, `signature-atf`, `Torque-Drive-atf`, `cvt-fluid`, `dct-fluid`, `super-shift-atf`)
4. `04-motocicletas-atv-marino/`
   - `4t-motorcycle/` (`10w-30`, `10w-40`)
   - `v-twin/` (`20w-50`, `20w-40`, `15w-60`, `primary-fluid`, `transmission-fluid`)
   - `2-stroke/` (`saber-100-1`, `dominator-2t`, `interceptor-2t`)
   - `atv-utv/` (`10w-40`, `5w-50`, `power-train-fluid`)
   - `dirt-bike/` (`10w-40`, `10w-50`, `10w-60`, `transmission-fluid`)
   - `metric-motorcycle/` (`10w-30`, `10w-40`, `15w-50`)
   - `marino/` (`10w-30-marine`, `10w-40-marine`, `25w-40-marine-blend`)
5. `05-aditivos-grasas-coolant-varios/`
   - `fluidos-frenos-direccion-varios/` (`power-steering`, `dot3-dot4-brake`, `dominator-dot4-racing-brake`, `engine-transmission-flush`, `15w-40-high-zinc`)
   - `aditivos-combustible/` (`pi-performance-improver`, `upper-cylinder-lubricant`, `diesel-injector-clean`, `dominator-octane-boost`, `motorcycle-octane-boost`, `dominant-coolant-boost`, `diesel-all-in-one`, `diesel-cetane-boost`, `gasoline-stabilizer`)
   - `grasas-y-lubricantes/` (`synthetic-polymeric-offroad`, `synthetic-multi-purpose`, `synthetic-water-resistant`, `arctic-synthetic`, `heavy-duty-metal-protector`, `mud-slinger`, `chain-lube`, `mp-metal-protector`, `silicone-spray`, `power-foam`, `miracle-wash`, `firearm-cleaner`)
   - `coolant-anticongelante/` (`passenger-car-light-truck-coolant`, `heavy-duty-antifreeze-coolant`, `propylene-glycol-antifreeze`)

---

## 🏷️ Convención de Nombres de Archivos de Presentación

Dentro de cada carpeta de producto encontrarás las imágenes nombradas por tipo de envase:
- `cuarto-1qt-<SKU>.jpg` — Botella de 1 Cuarto (946 mL)
- `easypack-1qt-<SKU>.jpg` — Envase flexible Easy-Pack de 1 Cuarto
- `galon-1gal-<SKU>.jpg` — Galón (3.78 L)
- `garrafa-2.5gal-<SKU>.jpg` — Garrafa de 2.5 Galones (9.46 L)
- `cubeta-5gal-<SKU>.jpg` — Cubeta / Pail de 5 Galones (18.9 L)
- `barril-16gal-<SKU>.jpg` / `barril-30gal-<SKU>.jpg` — Barriles de 16 y 30 Galones
- `estanon-55gal-<SKU>.jpg` — Estañón de 55 Galones (208 L)
- `tote-275gal-<SKU>.jpg` — Tote de 275 Galones (1041 L)
- `cartucho-14oz-<SKU>.jpg` / `cubeta-35lb-<SKU>.jpg` / `barril-120lb-<SKU>.jpg` — Grasas
- `spray-aerosol-<SKU>.jpg` — Aerosoles y Sprays
- `familia-presentaciones-<CODE>.jpg` — Fotografía grupal de la familia de envases
- `recorte-transparente-<SKU>.webp` — Imagen con fondo transparente recortado
