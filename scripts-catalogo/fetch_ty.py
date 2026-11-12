import json
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor

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

from discover_presentations_defs import PRODUCTS

def fetch_ty_packages(prod):
    cat, line, item_slug, name, base, als_codes, pr_slug = prod
    ty_item = ty_by_base.get(base)
    pkgs = []
    cutout_webp = None
    if ty_item and ty_item["u"].startswith("/"):
        url = "https://tunedyota.com" + ty_item["u"]
        res = subprocess.run(["curl", "-s", url], capture_output=True, text=True)
        html = res.stdout
        # Extract Packages & sizes table rows
        rows = re.findall(r"<tr><td>([^<]+)</td><td>([^<]+)</td></tr>", html)
        for pkg_name, stock_num in rows:
            pkgs.append((pkg_name.strip(), stock_num.strip()))
        # Check cutout webp
        m_img = re.search(r'<img class="pdp-img[^"]*" src="([^"]+)"', html)
        if m_img:
            cutout_webp = "https://tunedyota.com" + m_img.group(1)
    return base, pkgs, cutout_webp

if __name__ == "__main__":
    print("Fetching package tables from TunedYota...")
