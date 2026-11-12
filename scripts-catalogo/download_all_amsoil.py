import os
import re
import json
import csv
import hashlib
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

OUT_DIR = "/Users/Osito/.gemini/antigravity/scratch/amsoil-imagenes"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load TunedYota hdata
with open("/Users/Osito/.gemini/antigravity/brain/48d94f77-04d9-4160-91d5-2fece2c0bfad/.system_generated/steps/106/content.md") as f:
    text = f.read()
m = re.search(r'<script id="hdata" type="application/json">(\[.*?\])</script>', text)
hdata = json.loads(m.group(1))

ty_by_base = {}
for item in hdata:
    s = item["s"]
    if s == "RDCBCN-EA":
        ty_by_base["RDCB"] = item
    elif s == "MOBCN-EA":
        ty_by_base["MOB"] = item
    else:
        for suf in ["QT-EA", "1G-EA", "TP-EA", "05-EA", "55-EA", "27-EA", "PK-EA", "PCN-EA", "CN-EA", "BE-EA", "TB-EA", "CR-EA", "4SC-EA", "SC-EA", "SP-EA", "BA-EA", "35-EA", "-EA"]:
            if s.endswith(suf):
                base = s[:-len(suf)]
                ty_by_base[base] = item
                break

# 2. Load AMSOIL PR sitemap
with open("/Users/Osito/.gemini/antigravity/brain/48d94f77-04d9-4160-91d5-2fece2c0bfad/.system_generated/steps/72/content.md") as f:
    pr_text = f.read()
pr_blocks = re.findall(r"<url>(.*?)</url>", pr_text, re.S)
pr_map = {}
for b in pr_blocks:
    loc = re.search(r"<loc>([^<]+)</loc>", b).group(1)
    imgs = re.findall(r"<image:loc>([^<]+)</image:loc>", b)
    slug = loc.split("/")[-1]
    pr_map[slug] = [re.sub(r"/v1/fit/.*", "", img) for img in imgs]

# 3. Load products list from discover_presentations.py
import sys
sys.path.insert(0, "/Users/Osito/.gemini/antigravity/brain/48d94f77-04d9-4160-91d5-2fece2c0bfad/scratch")
from discover_presentations import PRODUCTS

# Human-readable Spanish presentation labels by suffix
SUFFIX_LABELS = {
    "QT": ("cuarto-1qt", "Botella 1 Cuarto (946 mL)"),
    "PK": ("easy-pack-1qt", "Easy-Pack 1 Cuarto (946 mL)"),
    "1G": ("galon-1gal", "Galón (3.78 L)"),
    "TP": ("garrafa-2.5gal", "Garrafa 2.5 Galones (9.46 L)"),
    "05": ("cubeta-5gal", "Cubeta 5 Galones (18.9 L)"),
    "16": ("barril-16gal", "Barril 16 Galones (60.5 L)"),
    "30": ("estanon-30gal", "Estañón 30 Galones (113.5 L)"),
    "55": ("estanon-55gal", "Estañón 55 Galones (208 L)"),
    "DR": ("estanon-55gal", "Estañón 55 Galones (208 L)"),
    "27": ("tote-275gal", "Tote 275 Galones (1041 L)"),
    "CN": ("botella-cn", "Botella / Envase Individual"),
    "PCN": ("botella-8oz", "Botella 8 oz (237 mL)"),
    "BCN": ("botella-16oz", "Botella 16 oz (473 mL)"),
    "HG": ("medio-galon-64oz", "Medio Galón 64 oz (1.89 L)"),
    "BE": ("botella-12oz", "Botella 12 oz (354 mL)"),
    "TB": ("tubo-4oz", "Tubo 4 oz (118 mL)"),
    "CR": ("cartucho-tubo-14oz", "Cartucho / Tubo de Grasa (14 oz)"),
    "35": ("cubeta-35lb", "Cubeta 35 lbs"),
    "99": ("cunete-120lb", "Cuñete 120 lbs"),
    "4SC": ("lata-spray-4oz", "Lata Aerosol 4.5 oz"),
    "SC": ("lata-spray", "Lata Aerosol"),
    "SP": ("lata-spray", "Lata Aerosol"),
    "BA": ("botella-4oz", "Botella 4 oz (118 mL)"),
}

STANDARD_SUFFIXES = [
    "QT", "PK", "1G", "TP", "05", "16", "30", "55", "27",
    "PCN", "BCN", "CN", "HG", "BE", "TB", "CR", "35", "99", "4SC", "SC", "SP", "BA"
]

def is_valid_image(data):
    if not data or len(data) < 4500:
        return False, None
    if data[:3] == b"\xff\xd8\xff":
        return True, "jpg"
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return True, "png"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return True, "webp"
    return False, None

def curl_bytes(url):
    try:
        res = subprocess.run(
            ["curl", "-sL", "--max-time", "15", "-A", "Mozilla/5.0", url],
            capture_output=True
        )
        if res.returncode == 0:
            return res.stdout
    except Exception:
        pass
    return b""

def process_product(idx, prod):
    cat, line, item_slug, display_name, base, als_codes, pr_slug = prod
    prod_dir = os.path.join(OUT_DIR, cat, line, item_slug)
    os.makedirs(prod_dir, exist_ok=True)

    # Remove old files if re-running
    for f in os.listdir(prod_dir):
        try:
            os.remove(os.path.join(prod_dir, f))
        except Exception:
            pass

    ty_item = ty_by_base.get(base)
    ty_pkgs = {}
    cutout_url = None
    canonical_ty_sku = None

    if ty_item:
        canonical_ty_sku = ty_item["s"].lower()
        if ty_item["u"].startswith("/"):
            html_bytes = curl_bytes("https://tunedyota.com" + ty_item["u"])
            html = html_bytes.decode("utf-8", "ignore")
            rows = re.findall(r"<tr><td>([^<]+)</td><td>([^<]+)</td></tr>", html)
            for pkg_name, stock_num in rows:
                s_clean = re.sub(r"-(EA|CA)$", "", stock_num.strip())
                if s_clean not in ty_pkgs:
                    ty_pkgs[s_clean] = pkg_name.strip()
            m_img = re.search(r'<img class="pdp-img[^"]*" src="([^"]+)"', html)
            if m_img:
                cutout_url = "https://tunedyota.com" + m_img.group(1)

    # Build ordered list of SKUs to check
    candidate_skus = []
    for s in ty_pkgs.keys():
        if s not in candidate_skus:
            candidate_skus.append(s)
    extra_suffixes = ["QT", "PK", "1G", "TP", "05", "30", "55", "27", "35", "99"] if ty_pkgs else STANDARD_SUFFIXES
    for suf in extra_suffixes:
        s = f"{base}{suf}"
        if s not in candidate_skus:
            candidate_skus.append(s)
    # Special case for ADS (Diesel Injector Clean + Cetane Boost uses ADSPCN, ADSCN, ADS1G, ADS05, ADS55)
    if base == "ADS":
        for s in ["ADSPCN", "ADSCN", "ADS1G", "ADS05", "ADS55"]:
            if s not in candidate_skus:
                candidate_skus.append(s)
    # Special case for DEO / DMO
    if base == "DEO":
        for suf in ["QT", "1G", "TP", "05", "55", "27"]:
            s = f"DMO{suf}"
            if s not in candidate_skus:
                candidate_skus.append(s)

    seen_hashes = set()
    downloaded = []

    # 1. Try each presentation SKU on Shopify CDN and OzMotorsport
    for sku in candidate_skus:
        # Determine suffix
        suf = sku[len(base):] if sku.startswith(base) else sku[3:]
        slug_prefix, label_es = SUFFIX_LABELS.get(suf, (f"presentacion-{suf.lower()}", ty_pkgs.get(sku, f"Presentación {sku}")))
        if sku in ty_pkgs:
            label_es = f"{label_es} ({ty_pkgs[sku]})"

        urls_to_try = [
            ("shopify_nlt", f"https://cdn.shopify.com/s/files/1/0757/5738/7973/files/NLT410-AM{sku}.jpg"),
        ]
        if (sku in ty_pkgs) or (not ty_pkgs and suf in ["QT", "PK", "1G", "TP", "55", "CN", "CR", "SC"]):
            urls_to_try.append(("ozmotorsport", f"https://www.ozmotorsport.com/assets/full/{sku}.jpg"))
            urls_to_try.append(("tunedyota_full", f"https://tunedyota.com/images/amsoil/full/{sku.lower()}-ea.jpg"))
        for src_name, url in urls_to_try:
            data = curl_bytes(url)
            ok, ext = is_valid_image(data)
            if ok:
                h = hashlib.sha256(data).hexdigest()
                if h not in seen_hashes:
                    seen_hashes.add(h)
                    fname = f"{slug_prefix}-{sku}.{ext}"
                    fpath = os.path.join(prod_dir, fname)
                    with open(fpath, "wb") as out:
                        out.write(data)
                    downloaded.append({
                        "filename": fname,
                        "rel_path": f"{cat}/{line}/{item_slug}/{fname}",
                        "sku": sku,
                        "presentation": label_es,
                        "source": src_name,
                        "source_url": url,
                        "bytes": len(data)
                    })
                break

    # 2. Check OzMotorsport base code image (often a group/family shot or high-res studio shot)
    oz_base_url = f"https://www.ozmotorsport.com/assets/full/{base}.jpg"
    data = curl_bytes(oz_base_url)
    ok, ext = is_valid_image(data)
    if ok:
        h = hashlib.sha256(data).hexdigest()
        if h not in seen_hashes:
            seen_hashes.add(h)
            fname = f"vista-general-{base}.{ext}"
            fpath = os.path.join(prod_dir, fname)
            with open(fpath, "wb") as out:
                out.write(data)
            downloaded.append({
                "filename": fname,
                "rel_path": f"{cat}/{line}/{item_slug}/{fname}",
                "sku": base,
                "presentation": "Vista General / Familia de Presentaciones",
                "source": "ozmotorsport_base",
                "source_url": oz_base_url,
                "bytes": len(data)
            })

    # 3. Check TunedYota canonical image if we haven't already got it
    if canonical_ty_sku:
        ty_full_url = f"https://tunedyota.com/images/amsoil/full/{canonical_ty_sku}.jpg"
        data = curl_bytes(ty_full_url)
        ok, ext = is_valid_image(data)
        if ok:
            h = hashlib.sha256(data).hexdigest()
            if h not in seen_hashes:
                seen_hashes.add(h)
                sku_clean = canonical_ty_sku.upper().replace("-EA", "")
                fname = f"envase-principal-{sku_clean}.{ext}"
                fpath = os.path.join(prod_dir, fname)
                with open(fpath, "wb") as out:
                    out.write(data)
                downloaded.append({
                    "filename": fname,
                    "rel_path": f"{cat}/{line}/{item_slug}/{fname}",
                    "sku": sku_clean,
                    "presentation": "Envase Principal (1000x1000)",
                    "source": "tunedyota_canonical",
                    "source_url": ty_full_url,
                    "bytes": len(data)
                })

    # 4. Check TunedYota transparent WebP cutout
    if cutout_url:
        data = curl_bytes(cutout_url)
        ok, ext = is_valid_image(data)
        if ok:
            h = hashlib.sha256(data).hexdigest()
            if h not in seen_hashes:
                seen_hashes.add(h)
                fname = f"recorte-fondo-transparente-{base}.{ext}"
                fpath = os.path.join(prod_dir, fname)
                with open(fpath, "wb") as out:
                    out.write(data)
                downloaded.append({
                    "filename": fname,
                    "rel_path": f"{cat}/{line}/{item_slug}/{fname}",
                    "sku": base,
                    "presentation": "Recorte con Fondo Transparente (WebP)",
                    "source": "tunedyota_cutout",
                    "source_url": cutout_url,
                    "bytes": len(data)
                })

    # 5. Check AMSOIL PR Wix images
    if pr_slug and pr_slug in pr_map:
        for i, wix_url in enumerate(pr_map[pr_slug], 1):
            data = curl_bytes(wix_url)
            ok, ext = is_valid_image(data)
            if ok:
                h = hashlib.sha256(data).hexdigest()
                if h not in seen_hashes:
                    seen_hashes.add(h)
                    fname = f"catalogo-latam-{base}-{i}.{ext}"
                    fpath = os.path.join(prod_dir, fname)
                    with open(fpath, "wb") as out:
                        out.write(data)
                    downloaded.append({
                        "filename": fname,
                        "rel_path": f"{cat}/{line}/{item_slug}/{fname}",
                        "sku": f"{base}-{i}",
                        "presentation": f"Imagen Catálogo LATAM #{i}",
                        "source": "amsoilpr_wix",
                        "source_url": wix_url,
                        "bytes": len(data)
                    })

    print(f"[{idx+1:02d}/{len(PRODUCTS)}] {cat}/{line}/{item_slug} ({base}) -> {len(downloaded)} imágenes")
    return {
        "index": idx + 1,
        "category": cat,
        "line": line,
        "item_slug": item_slug,
        "display_name": display_name,
        "amsoil_code": base,
        "als_codes": als_codes,
        "folder": f"{cat}/{line}/{item_slug}",
        "available_packages_official": [{"sku": k, "name": v} for k, v in ty_pkgs.items()],
        "images": downloaded
    }

def main():
    results = [None] * len(PRODUCTS)
    with ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(process_product, i, p): i for i, p in enumerate(PRODUCTS)}
        for fut in as_completed(futures):
            i = futures[fut]
            results[i] = fut.result()

    total_imgs = sum(len(r["images"]) for r in results)
    empty_prods = [r for r in results if len(r["images"]) == 0]
    print(f"\nDONE! Total products: {len(results)}, Total images downloaded: {total_imgs}, Empty products: {len(empty_prods)}")
    for ep in empty_prods:
        print("  EMPTY:", ep["folder"], ep["amsoil_code"])

    with open(os.path.join(OUT_DIR, "catalogo-imagenes.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    with open(os.path.join(OUT_DIR, "catalogo-imagenes.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Categoria", "Linea", "Viscosidad_o_Tipo", "Nombre_Producto", "Codigo_AMSOIL", "Codigos_Lista_ALS", "SKU_Presentacion", "Presentacion", "Archivo_Imagen", "Ruta_Relativa", "URL_Origen", "Tamano_Bytes"])
        for r in results:
            als_str = ", ".join(r["als_codes"])
            for img in r["images"]:
                w.writerow([
                    r["category"],
                    r["line"],
                    r["item_slug"],
                    r["display_name"],
                    r["amsoil_code"],
                    als_str,
                    img["sku"],
                    img["presentation"],
                    img["filename"],
                    img["rel_path"],
                    img["source_url"],
                    img["bytes"]
                ])

if __name__ == "__main__":
    main()
