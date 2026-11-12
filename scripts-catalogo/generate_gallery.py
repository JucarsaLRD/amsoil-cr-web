import json
import os

OUT_DIR = "/Users/Osito/.gemini/antigravity/scratch/amsoil-imagenes"
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
<title>Catálogo de Imágenes AMSOIL ({total_products} Productos · {total_images} Imágenes)</title>
<style>
  :root {{
    --bg: #0f172a;
    --card: #1e293b;
    --border: #334155;
    --text: #f8fafc;
    --muted: #94a3b8;
    --red: #e11d48;
    --blue: #0284c7;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: var(--bg);
    color: var(--text);
    padding: 28px;
  }}
  header {{
    max-width: 1400px;
    margin: 0 auto 24px;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--border);
  }}
  h1 {{ font-size: 26px; font-weight: 800; }}
  .stats {{ color: var(--muted); font-size: 14px; margin-top: 4px; }}
  .search-box {{
    padding: 12px 16px;
    width: 360px;
    max-width: 100%;
    border-radius: 10px;
    border: 1px solid var(--border);
    background: var(--card);
    color: var(--text);
    font-size: 15px;
  }}
  .grid {{
    max-width: 1400px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
    gap: 20px;
  }}
  .prod-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }}
  .badges {{ display: flex; flex-wrap: wrap; gap: 6px; font-size: 11px; font-weight: 700; text-transform: uppercase; }}
  .badge {{ padding: 3px 8px; border-radius: 6px; background: #334155; color: #e2e8f0; }}
  .badge.amsoil {{ background: var(--red); color: #fff; }}
  .badge.als {{ background: var(--blue); color: #fff; }}
  .prod-title {{ font-size: 17px; font-weight: 700; line-height: 1.3; }}
  .folder-path {{ font-family: monospace; font-size: 12px; color: var(--muted); background: #0f172a; padding: 6px 10px; border-radius: 6px; word-break: break-all; }}
  .imgs-row {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(105px, 1fr));
    gap: 10px;
    margin-top: 4px;
  }}
  .img-item {{
    background: #fff;
    border-radius: 8px;
    padding: 6px;
    text-align: center;
    color: #0f172a;
    text-decoration: none;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    transition: transform 0.15s;
  }}
  .img-item:hover {{ transform: translateY(-2px); }}
  .img-item img {{
    width: 100%;
    height: 95px;
    object-fit: contain;
  }}
  .img-sku {{ font-size: 11px; font-weight: 800; margin-top: 6px; color: #0f172a; }}
  .img-pres {{ font-size: 10px; color: #475569; line-height: 1.2; margin-top: 2px; }}
</style>
</head>
<body>
<header>
  <div>
    <h1>Catálogo de Imágenes AMSOIL — American Lubricants Supply S.A.</h1>
    <div class="stats">{total_products} productos/viscosidades organizados en carpetas · {total_images} imágenes de presentaciones descargadas</div>
  </div>
  <input class="search-box" id="q" type="search" placeholder="Buscar por nombre, viscosidad, código ALS o AMSOIL...">
</header>
<div class="grid" id="grid">
"""

for p in catalog:
    als = ", ".join(p["als_codes"])
    search_str = f"{p['display_name']} {p['amsoil_code']} {als} {p['folder']}".lower()
    html += f"""
  <div class="prod-card" data-search="{search_str}">
    <div class="badges">
      <span class="badge amsoil">AMSOIL: {p['amsoil_code']}</span>
      <span class="badge als">ALS: {als}</span>
      <span class="badge">{p['line']}</span>
    </div>
    <div class="prod-title">{p['display_name']}</div>
    <div class="folder-path">📁 {p['folder']}/</div>
    <div class="imgs-row">
"""
    for img in p["images"]:
        html += f"""
      <a class="img-item" href="{img['rel_path']}" target="_blank" title="{img['presentation']} ({img['filename']})">
        <img src="{img['rel_path']}" loading="lazy" alt="{img['sku']}">
        <div class="img-sku">{img['sku']}</div>
        <div class="img-pres">{img['presentation'].split('(')[0].strip()}</div>
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
