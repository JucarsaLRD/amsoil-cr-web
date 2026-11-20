import json
import os

OUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
json_path = os.path.join(OUT_DIR, "catalogo-imagenes.json")

with open(json_path, "r", encoding="utf-8") as f:
    catalog = json.load(f)

total_products = len(catalog)
total_images = sum(len(p["images"]) for p in catalog)

html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Galería de Envases AMSOIL ({total_products} Productos · {total_images} Presentaciones)</title>
<meta name="theme-color" content="#000000">
<link rel="icon" type="image/png" href="favicon.png">
<link rel="apple-touch-icon" href="assets/logos/amsoil-insignia.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300;0,400;0,700;1,400&display=swap" rel="stylesheet">
<style>
  :root {{
    --amsoil-blue: #005BAA;
    --amsoil-red: #ED1C24;
    --amsoil-gray: #BCBEC0;
    --amsoil-black: #000000;
    --amsoil-white: #FFFFFF;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Open Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    background: var(--amsoil-white);
    color: var(--amsoil-black);
  }}
  header {{
    background: var(--amsoil-black);
    color: var(--amsoil-white);
    border-bottom: 4px solid var(--amsoil-red);
    padding: 18px 28px;
  }}
  .header-inner {{
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
  }}
  .brand-row {{
    display: flex;
    align-items: center;
    gap: 24px;
    flex-wrap: wrap;
  }}
  .logo-wrap {{
    background: var(--amsoil-black);
    padding: 16px 20px;
    display: inline-flex;
    align-items: center;
  }}
  .logo-wrap img {{
    width: 172px;
    min-width: 150px;
    height: auto;
    display: block;
  }}
  h1 {{
    font-size: 22px;
    font-weight: 700;
    line-height: 1.25;
    color: var(--amsoil-white);
  }}
  .stats {{
    color: var(--amsoil-gray);
    font-size: 13.5px;
    font-weight: 300;
    margin-top: 4px;
  }}
  .search-box {{
    padding: 11px 15px;
    width: 360px;
    max-width: 100%;
    border-radius: 4px;
    border: 1px solid var(--amsoil-gray);
    background: var(--amsoil-white);
    color: var(--amsoil-black);
    font-family: 'Open Sans', sans-serif;
    font-size: 14px;
  }}
  .search-box:focus {{
    outline: 2px solid var(--amsoil-blue);
    border-color: var(--amsoil-blue);
  }}
  .grid {{
    max-width: 1400px;
    margin: 28px auto 48px;
    padding: 0 28px;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
    gap: 20px;
  }}
  .prod-card {{
    background: var(--amsoil-white);
    border: 1px solid var(--amsoil-gray);
    border-top: 3px solid var(--amsoil-blue);
    border-radius: 4px;
    padding: 18px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }}
  .badges {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    font-size: 11px;
    font-weight: 700;
  }}
  .badge {{
    padding: 3px 9px;
    border-radius: 3px;
    background: var(--amsoil-blue);
    color: var(--amsoil-white);
  }}
  .badge.visc {{
    background: var(--amsoil-red);
    color: var(--amsoil-white);
  }}
  .prod-title {{
    font-size: 16.5px;
    font-weight: 700;
    line-height: 1.3;
    color: var(--amsoil-black);
  }}
  .folder-path {{
    font-family: monospace;
    font-size: 11.5px;
    color: var(--amsoil-black);
    background: rgba(188, 190, 192, 0.22);
    border: 1px solid var(--amsoil-gray);
    padding: 5px 9px;
    border-radius: 3px;
    word-break: break-all;
  }}
  .imgs-row {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(105px, 1fr));
    gap: 10px;
    margin-top: 4px;
  }}
  .img-item {{
    background: var(--amsoil-white);
    border: 1px solid var(--amsoil-gray);
    border-radius: 4px;
    padding: 8px 6px;
    text-align: center;
    color: var(--amsoil-black);
    text-decoration: none;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    transition: border-color 0.15s;
  }}
  .img-item:hover {{
    border-color: var(--amsoil-blue);
  }}
  .img-item img {{
    width: 100%;
    height: 95px;
    object-fit: contain;
  }}
  .img-pres {{
    font-size: 11px;
    font-weight: 700;
    color: var(--amsoil-black);
    line-height: 1.25;
    margin-top: 6px;
  }}
</style>
</head>
<body>
<header>
  <div class="header-inner">
    <div class="brand-row">
      <a href="index-catalogo.html" class="logo-wrap" aria-label="AMSOIL — The First in Synthetics®">
        <img src="amsoil-logo.png" alt="AMSOIL — The First in Synthetics®" width="596" height="184">
      </a>
      <div>
        <h1>Galería de Presentaciones — American Lubricants Supply S.A.</h1>
        <div class="stats">{total_products} productos AMSOIL organizados en carpetas · {total_images} imágenes de envases oficiales</div>
      </div>
    </div>
    <input class="search-box" id="q" type="search" placeholder="Buscar por nombre de producto, línea o viscosidad...">
  </div>
</header>
<div class="grid" id="grid">
"""

for p in catalog:
    visc_badge = f'<span class="badge visc">{p["viscosity"]}</span>' if p.get("viscosity") else ""
    line_label = p.get("line_name") or p.get("line", "")
    search_str = f"{p['display_name']} {line_label} {p.get('viscosity', '')} {p['folder']}".lower()
    html += f"""
  <div class="prod-card" data-search="{search_str}">
    <div class="badges">
      <span class="badge">{line_label}</span>
      {visc_badge}
    </div>
    <div class="prod-title">{p['display_name']}</div>
    <div class="folder-path">{p['folder']}/</div>
    <div class="imgs-row">
"""
    for img in p["images"]:
        pres_clean = img.get("short_label") or img["presentation"].split("(")[0].strip()
        html += f"""
      <a class="img-item" href="{img['rel_path']}" target="_blank" title="{p['display_name']} — {pres_clean}">
        <img src="{img['rel_path']}" loading="lazy" alt="{p['display_name']} ({pres_clean})">
        <div class="img-pres">{pres_clean}</div>
      </a>
"""
    html += """
    </div>
  </div>
"""

html += """
</div>
<script>
  const q = document.getElementById('q');
  const cards = document.querySelectorAll('.prod-card');
  q.addEventListener('input', () => {
    const val = q.value.toLowerCase().trim();
    cards.forEach(c => {
      c.style.display = c.dataset.search.includes(val) ? '' : 'none';
    });
  });
</script>
</body>
</html>
"""

with open(os.path.join(OUT_DIR, "galeria.html"), "w", encoding="utf-8") as f:
    f.write(html)

print("Generated:", os.path.join(OUT_DIR, "galeria.html"))
