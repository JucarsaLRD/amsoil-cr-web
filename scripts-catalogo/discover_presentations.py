import json
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor

# Load TunedYota hdata
with open("/Users/Osito/.gemini/antigravity/brain/48d94f77-04d9-4160-91d5-2fece2c0bfad/.system_generated/steps/106/content.md") as f:
    text = f.read()
m = re.search(r'<script id="hdata" type="application/json">(\[.*?\])</script>', text)
hdata = json.loads(m.group(1))

ty_by_sku = {}
ty_by_base = {}
for item in hdata:
    s = item["s"]
    ty_by_sku[s] = item
    # strip known suffixes
    for suf in ["QT-EA", "1G-EA", "TP-EA", "05-EA", "55-EA", "27-EA", "PK-EA", "PCN-EA", "CN-EA", "BE-EA", "TB-EA", "CR-EA", "4SC-EA", "SC-EA", "SP-EA", "BA-EA", "35-EA", "-EA"]:
        if s.endswith(suf):
            base = s[:-len(suf)]
            ty_by_base[base] = item
            break

# Load AMSOIL PR sitemap
with open("/Users/Osito/.gemini/antigravity/brain/48d94f77-04d9-4160-91d5-2fece2c0bfad/.system_generated/steps/72/content.md") as f:
    pr_text = f.read()
pr_blocks = re.findall(r"<url>(.*?)</url>", pr_text, re.S)
pr_map = {}
for b in pr_blocks:
    loc = re.search(r"<loc>([^<]+)</loc>", b).group(1)
    imgs = re.findall(r"<image:loc>([^<]+)</image:loc>", b)
    slug = loc.split("/")[-1]
    pr_map[slug] = [re.sub(r"/v1/fit/.*", "", img) for img in imgs]

# Define all 88 products from the user's PDF catalog
# Format: (folder_category, folder_line, folder_item, display_name, base_code, als_codes, pr_slug_hint)
PRODUCTS = [
    # 01-motor-gasolina / oe-synthetic
    ("01-motor-gasolina", "oe-synthetic", "0w-20", "AMSOIL OE 0W-20 100% Synthetic Motor Oil", "OEZ", ["AM28012"], "oez-sae-0w-20"),
    ("01-motor-gasolina", "oe-synthetic", "5w-20", "AMSOIL OE 5W-20 100% Synthetic Motor Oil", "OEM", ["AM29012"], "oem-sae-5w-20"),
    ("01-motor-gasolina", "oe-synthetic", "5w-30", "AMSOIL OE 5W-30 100% Synthetic Motor Oil", "OEF", ["AM86012", "AM86004", "AM86055"], "oef-sae-5w-30"),
    ("01-motor-gasolina", "oe-synthetic", "5w-40", "AMSOIL OE 5W-40 100% Synthetic Motor Oil", "OEB", ["AM87012"], "oeb-sae-5w-40"),
    ("01-motor-gasolina", "oe-synthetic", "10w-30", "AMSOIL OE 10W-30 100% Synthetic Motor Oil", "OET", ["AM06012", "AM06004", "AM06055"], "oet-sae-10w-30"),
    ("01-motor-gasolina", "oe-synthetic", "10w-40", "AMSOIL OE 10W-40 100% Synthetic Motor Oil", "OEH", ["AM24012"], "oeh-sae-10w-40-qt"),
    ("01-motor-gasolina", "oe-synthetic", "20w-50", "AMSOIL OE 20W-50 100% Synthetic Motor Oil", "OER", ["AM02012", "AM02055"], "oer-sae-20w-50-qt"),

    # 01-motor-gasolina / xl-synthetic
    ("01-motor-gasolina", "xl-synthetic", "5w-30", "AMSOIL XL 5W-30 100% Synthetic Motor Oil", "XLF", ["AMX8612"], "xlf-sae-5w-30"),
    ("01-motor-gasolina", "xl-synthetic", "10w-30", "AMSOIL XL 10W-30 100% Synthetic Motor Oil", "XLT", ["AMX0612"], "xlt-sae-10w-30"),

    # 01-motor-gasolina / european-car-formula
    ("01-motor-gasolina", "european-car-formula", "0w-20-ls-vw", "AMSOIL European Car Formula 0W-20 LS-VW Synthetic Motor Oil", "EZT", ["AME2812"], "ezt-sae-0w-20-ls-vw-qt"),
    ("01-motor-gasolina", "european-car-formula", "0w-20-ls", "AMSOIL European Car Formula 0W-20 LS Synthetic Motor Oil", "AFE", ["AME2812"], "afe-sae-0w-20-ls-qt"),
    ("01-motor-gasolina", "european-car-formula", "0w-30-ms", "AMSOIL European Car Formula 0W-30 MS Synthetic Motor Oil", "EOT", ["AME8912"], "0w-30-ms-100-synthetic-european-motor-oil"),
    ("01-motor-gasolina", "european-car-formula", "0w-40-fs", "AMSOIL European Car Formula 0W-40 FS Synthetic Motor Oil", "EFO", ["AME8812"], "efo-sae-0w-40"),
    ("01-motor-gasolina", "european-car-formula", "5w-30-ls", "AMSOIL European Car Formula 5W-30 LS Synthetic Motor Oil", "AEL", ["AML8612", "AML86004", "AML86055"], "ael-sae-5w-30"),
    ("01-motor-gasolina", "european-car-formula", "5w-40-fs", "AMSOIL European Car Formula 5W-40 FS Synthetic Motor Oil", "EFM", ["AMF8712"], None),
    ("01-motor-gasolina", "european-car-formula", "5w-40-ms-acea-c3", "AMSOIL European Car Formula 5W-40 MS Synthetic Motor Oil", "AFL", ["AME8712"], "afl-sae-5w-40"),

    # 01-motor-gasolina / hybrid
    ("01-motor-gasolina", "hybrid", "0w-16", "AMSOIL 0W-16 100% Synthetic Hybrid Motor Oil", "HE016", ["AMH27012"], "he016-sae-0w-16-híbrido-qt"),
    ("01-motor-gasolina", "hybrid", "0w-20", "AMSOIL 0W-20 100% Synthetic Hybrid Motor Oil", "HE020", ["AMH28012"], "he020-sae-0w-20-híbrido-qt"),

    # 01-motor-gasolina / signature-series
    ("01-motor-gasolina", "signature-series", "0w-20", "AMSOIL Signature Series 0W-20 100% Synthetic Motor Oil", "ASM", ["AMS2812"], "asm"),
    ("01-motor-gasolina", "signature-series", "0w-40", "AMSOIL Signature Series 0W-40 100% Synthetic Motor Oil", "AZF", ["AMS4012"], "azf"),
    ("01-motor-gasolina", "signature-series", "5w-20", "AMSOIL Signature Series 5W-20 100% Synthetic Motor Oil", "ALM", ["AMS4112"], "alm"),
    ("01-motor-gasolina", "signature-series", "5w-30", "AMSOIL Signature Series 5W-30 100% Synthetic Motor Oil", "ASL", ["AMS8612", "AMS8604", "AMS86055"], "asl"),
    ("01-motor-gasolina", "signature-series", "5w-50", "AMSOIL Signature Series 5W-50 100% Synthetic Motor Oil", "AMR", ["AMM88012"], None),
    ("01-motor-gasolina", "signature-series", "10w-30", "AMSOIL Signature Series 10W-30 100% Synthetic Motor Oil", "ATM", ["AMS0612"], None),

    # 01-motor-gasolina / racing-zrod-dominator
    ("01-motor-gasolina", "racing-zrod-dominator", "z-rod-10w-30", "AMSOIL Z-ROD 10W-30 100% Synthetic Motor Oil", "ZRT", ["AMZ06012"], "zrt-10w-30"),
    ("01-motor-gasolina", "racing-zrod-dominator", "z-rod-10w-40", "AMSOIL Z-ROD 10W-40 100% Synthetic Motor Oil", "ZRD", ["AMZ24012"], "zrd-sae-10w-40-qt"),
    ("01-motor-gasolina", "racing-zrod-dominator", "z-rod-20w-50", "AMSOIL Z-ROD 20W-50 100% Synthetic Motor Oil", "ZRF", ["AMZ02012"], "zrf-sae-20w-50"),
    ("01-motor-gasolina", "racing-zrod-dominator", "briggs-stratton-4t-racing", "AMSOIL Synthetic 4T Racing Oil (Briggs & Stratton)", "GBS", ["AMBS012"], "briggs-stratton-synthetic-4t-racing-oil"),
    ("01-motor-gasolina", "racing-zrod-dominator", "dominator-10w-40", "AMSOIL DOMINATOR 10W-40 100% Synthetic Racing Oil", "RD40", ["AMR8412"], "dominator-10w-40-100-synthetic-racing-oil"),
    ("01-motor-gasolina", "racing-zrod-dominator", "dominator-15w-50", "AMSOIL DOMINATOR 15W-50 100% Synthetic Racing Oil", "RD50", ["AMR8512"], "rd50"),

    # 01-motor-gasolina / high-mileage
    ("01-motor-gasolina", "high-mileage", "5w-30", "AMSOIL 5W-30 100% Synthetic High-Mileage Motor Oil", "HM530", ["AM93012"], None),
    ("01-motor-gasolina", "high-mileage", "10w-30", "AMSOIL 10W-30 100% Synthetic High-Mileage Motor Oil", "HM1030", ["AM92012"], None),

    # 02-motor-diesel / heavy-duty-ck4
    ("02-motor-diesel", "heavy-duty-ck4", "5w-40", "AMSOIL Heavy-Duty 5W-40 100% Synthetic Diesel Oil", "ADO", ["AM30012", "AM30004", "AM30055"], "ado-sae-5w-40"),
    ("02-motor-diesel", "heavy-duty-ck4", "10w-30", "AMSOIL Heavy-Duty 10W-30 100% Synthetic Diesel Oil", "ADN", ["AM26012", "AM26004", "AM26002", "AM26055"], "adn"),
    ("02-motor-diesel", "heavy-duty-ck4", "15w-40", "AMSOIL Heavy-Duty 15W-40 100% Synthetic Diesel Oil", "ADP", ["AM84012", "AM84004", "AM84002", "AM84055"], "adp-sae-15w-40"),

    # 02-motor-diesel / commercial-synthetic-blend
    ("02-motor-diesel", "commercial-synthetic-blend", "15w-40", "AMSOIL 15W-40 Commercial-Grade Synthetic-Blend Diesel Oil", "SBDF", ["AM05055"], "sbdf-2-5-gal"),

    # 02-motor-diesel / diesel-dexos-d
    ("02-motor-diesel", "diesel-dexos-d", "0w-20", "AMSOIL 0W-20 100% Synthetic Diesel Oil (dexosD)", "DP020", ["AM27012"], "dp020-synthetic-diesel-oil-sae-0w-20-qt"),
    ("02-motor-diesel", "diesel-dexos-d", "5w-30", "AMSOIL 5W-30 100% Synthetic Diesel Oil (dexosD)", "DP530", ["AM85012"], "dp530-synthetic-diesel-oil-sae-5w-30-qt"),

    # 02-motor-diesel / signature-series-max-duty
    ("02-motor-diesel", "signature-series-max-duty", "5w-30", "AMSOIL Signature Series Max-Duty 5W-30 Synthetic Diesel Oil", "DHD", ["AMM86012", "AMM86004", "AMM86055"], "dhd-sae-5w-30"),
    ("02-motor-diesel", "signature-series-max-duty", "5w-40", "AMSOIL Signature Series Max-Duty 5W-40 Synthetic Diesel Oil", "DEO", ["AMM30012", "AMM30002"], "dmo-sae-5w-40"),
    ("02-motor-diesel", "signature-series-max-duty", "10w-30", "AMSOIL Signature Series Max-Duty 10W-30 Synthetic Diesel Oil", "DTT", ["AMM06012", "AMM06004"], "dtt-sea-10w-30-gal"),
    ("02-motor-diesel", "signature-series-max-duty", "15w-40", "AMSOIL Signature Series Max-Duty 15W-40 Synthetic Diesel Oil", "DME", ["AMM07012", "AMM07004"], "dme-sae-15w-40"),

    # 03-transmision-y-diferenciales / severe-gear-y-diferenciales
    ("03-transmision-y-diferenciales", "severe-gear-y-diferenciales", "severe-gear-75w-85", "AMSOIL SEVERE GEAR 75W-85 100% Synthetic Gear Lube", "SVL", ["AM62012"], "severe-gear-75w-85-100-synthetic-gear-lube"),
    ("03-transmision-y-diferenciales", "severe-gear-y-diferenciales", "severe-gear-75w-90", "AMSOIL SEVERE GEAR 75W-90 100% Synthetic Gear Lube", "SVG", ["AM66012"], "svg-sea-75w-90"),
    ("03-transmision-y-diferenciales", "severe-gear-y-diferenciales", "severe-gear-75w-140", "AMSOIL SEVERE GEAR 75W-140 100% Synthetic Gear Lube", "SVO", ["AM64012"], "svo-sae-75w-140"),
    ("03-transmision-y-diferenciales", "severe-gear-y-diferenciales", "severe-gear-80w-90", "AMSOIL SEVERE GEAR 80W-90 100% Synthetic Gear Lube", "AGL", ["AM58012"], "agl-sae-80w-90"),
    ("03-transmision-y-diferenciales", "severe-gear-y-diferenciales", "long-life-gear-75w-90", "AMSOIL 75W-90 Long Life 100% Synthetic Gear Lube", "FGR", ["AM63012"], "fgr-sae-75w-90"),
    ("03-transmision-y-diferenciales", "severe-gear-y-diferenciales", "manual-transaxle-75w-90-gl4", "AMSOIL 75W-90 Manual Transmission & Transaxle Gear Lube", "MTG", ["AM65012"], "mtg"),
    ("03-transmision-y-diferenciales", "severe-gear-y-diferenciales", "manual-synchromesh-5w-30", "AMSOIL 5W-30 Manual Synchromesh Transmission Fluid", "MTF", ["AM11012"], "mtf"),
    ("03-transmision-y-diferenciales", "severe-gear-y-diferenciales", "slip-lock-differential-additive", "AMSOIL Slip Lock Differential Additive", "ADA", ["AM160-012"], None),

    # 03-transmision-y-diferenciales / transmision-automatica-atf-cvt-dct
    ("03-transmision-y-diferenciales", "transmision-automatica-atf-cvt-dct", "torque-drive-atf", "AMSOIL Torque-Drive 100% Synthetic Automatic Transmission Fluid", "ATD", ["AM20004", "AM20002", "AM20055"], "atd"),
    ("03-transmision-y-diferenciales", "transmision-automatica-atf-cvt-dct", "oe-multi-vehicle-atf-red", "AMSOIL OE Multi-Vehicle 100% Synthetic ATF (Red)", "OTF", ["AM22012", "AM22004", "AM22002"], "otf-oe"),
    ("03-transmision-y-diferenciales", "transmision-automatica-atf-cvt-dct", "signature-series-multi-vehicle-atf-red", "AMSOIL Signature Series Multi-Vehicle 100% Synthetic ATF (Red)", "ATF", ["AMS22012"], "atf-3"),
    ("03-transmision-y-diferenciales", "transmision-automatica-atf-cvt-dct", "oe-fuel-efficient-atf-blue", "AMSOIL OE Fuel-Efficient 100% Synthetic ATF (Blue)", "OTL", ["AMF22012", "AMF22004"], "otl-oe"),
    ("03-transmision-y-diferenciales", "transmision-automatica-atf-cvt-dct", "signature-series-fuel-efficient-atf-blue", "AMSOIL Signature Series Fuel-Efficient 100% Synthetic ATF (Blue)", "ATL", ["AMFS22012"], "atl"),
    ("03-transmision-y-diferenciales", "transmision-automatica-atf-cvt-dct", "cvt-fluid", "AMSOIL 100% Synthetic CVT Fluid", "CVT", ["AM61012"], None),
    ("03-transmision-y-diferenciales", "transmision-automatica-atf-cvt-dct", "dct-fluid", "AMSOIL 100% Synthetic DCT Fluid", "DCT", ["AMDCT012"], None),
    ("03-transmision-y-diferenciales", "transmision-automatica-atf-cvt-dct", "signature-series-ulv-atf", "AMSOIL Signature Series ULV 100% Synthetic ATF", "ULV", ["AM91012"], "signature-series-ulv-100-synthetic-automatic-transmission-fluid"),
    ("03-transmision-y-diferenciales", "transmision-automatica-atf-cvt-dct", "super-shift-racing-atf", "AMSOIL Super Shift Racing Transmission Fluid", "ART", ["AM08012"], None),

    # 05-aditivos-grasas-coolant-varios / fluidos-frenos-direccion-varios
    ("05-aditivos-grasas-coolant-varios", "fluidos-frenos-direccion-varios", "dot-3-4-brake-fluid", "AMSOIL DOT 3 & DOT 4 100% Synthetic Brake Fluid", "BFLV", ["AM79012"], "bf3"),
    ("05-aditivos-grasas-coolant-varios", "fluidos-frenos-direccion-varios", "dominator-dot-4-racing-brake-fluid", "AMSOIL DOMINATOR DOT 4 100% Synthetic Racing Brake Fluid", "BFR", ["AMD79012"], "bfr"),
    ("05-aditivos-grasas-coolant-varios", "fluidos-frenos-direccion-varios", "power-steering-fluid", "AMSOIL 100% Synthetic Multi-Vehicle Power Steering Fluid", "PSF", ["AM80012"], None),
    ("05-aditivos-grasas-coolant-varios", "fluidos-frenos-direccion-varios", "engine-assembly-lube", "AMSOIL Engine Assembly Lube", "EAL", ["AM90012"], None),
    ("05-aditivos-grasas-coolant-varios", "fluidos-frenos-direccion-varios", "break-in-oil-sae-30", "AMSOIL SAE 30 Break-In Oil", "BRK", ["AM39012"], "brk-sae-30"),
    ("05-aditivos-grasas-coolant-varios", "fluidos-frenos-direccion-varios", "compressor-oil-iso-68", "AMSOIL ISO 68 100% Synthetic Compressor Oil", "PCJ", ["AM19055"], "iso68-2-5-gal"),
    ("05-aditivos-grasas-coolant-varios", "fluidos-frenos-direccion-varios", "saber-professional-2-stroke", "AMSOIL SABER Professional 100% Synthetic 2-Stroke Oil", "ATP", ["AM89012"], "atp"),
    ("05-aditivos-grasas-coolant-varios", "fluidos-frenos-direccion-varios", "engine-and-transmission-flush", "AMSOIL Engine & Transmission Flush", "FLSH", ["AM162-012"], "flsh-16-oz-bottle"),

    # 05-aditivos-grasas-coolant-varios / aditivos-combustible
    ("05-aditivos-grasas-coolant-varios", "aditivos-combustible", "diesel-injector-clean-cetane-boost", "AMSOIL Diesel Injector Clean + Cetane Boost", "ADS", ["AM161-012"], "ads-diesel-cetane-boost"),
    ("05-aditivos-grasas-coolant-varios", "aditivos-combustible", "upper-cylinder-lubricant-gasoline", "AMSOIL Upper Cylinder Lubricant Gasoline Additive", "UCL", ["AM164-012"], None),
    ("05-aditivos-grasas-coolant-varios", "aditivos-combustible", "dominator-octane-boost", "AMSOIL DOMINATOR Octane Boost", "AOB", ["AM167-006"], "aob"),
    ("05-aditivos-grasas-coolant-varios", "aditivos-combustible", "pi-performance-improver", "AMSOIL P.i. Performance Improver Gasoline Additive", "API", ["AM165-012"], "api"),
    ("05-aditivos-grasas-coolant-varios", "aditivos-combustible", "motorcycle-octane-boost", "AMSOIL Motorcycle Octane Boost", "MOB", ["AM163-012"], "mob"),

    # 05-aditivos-grasas-coolant-varios / grasas-y-lubricantes
    ("05-aditivos-grasas-coolant-varios", "grasas-y-lubricantes", "polymeric-off-road-grease-nlgi-2", "AMSOIL NLGI #2 Synthetic Polymeric Off-Road Grease", "GPOR2", ["AM47010"], "gpor2"),
    ("05-aditivos-grasas-coolant-varios", "grasas-y-lubricantes", "chain-lube-spray", "AMSOIL Chain Lube", "ACL", ["AMCL006"], "acl-1"),
    ("05-aditivos-grasas-coolant-varios", "grasas-y-lubricantes", "multi-purpose-grease-nlgi-2", "AMSOIL Synthetic Multi-Purpose Grease NLGI #2", "GLC", ["AM52010"], "synthetic-multi-purpose-grease"),
    ("05-aditivos-grasas-coolant-varios", "grasas-y-lubricantes", "red-grease-120-lbs", "AMSOIL 100% Synthetic Red Grease (Cuñete 120 lbs / Línea GLC)", "GLC", ["AM52120"], "multiuso-glc"),

    # 05-aditivos-grasas-coolant-varios / coolant-anticongelante
    ("05-aditivos-grasas-coolant-varios", "coolant-anticongelante", "passenger-car-antifreeze-50-50-yellow", "AMSOIL Passenger Car & Light Truck Antifreeze & Coolant 50/50", "ANTPC", ["AM83004"], None),
    ("05-aditivos-grasas-coolant-varios", "coolant-anticongelante", "heavy-duty-antifreeze-50-50-red", "AMSOIL Heavy-Duty Antifreeze & Coolant 50/50", "ANTHD", ["AM88004"], "anthd"),
    ("05-aditivos-grasas-coolant-varios", "coolant-anticongelante", "powersports-antifreeze-coolant", "AMSOIL Powersports Antifreeze & Coolant", "PSAF", ["AMPS82012"], "psaf-powersports-coolant"),
    ("05-aditivos-grasas-coolant-varios", "coolant-anticongelante", "dominator-coolant-boost", "AMSOIL DOMINATOR Coolant Boost", "RDCB", ["AM166-006"], "rdcb-1"),

    # 04-motocicletas-atv-marino / 4t-motorcycle
    ("04-motocicletas-atv-marino", "4t-motorcycle", "10w-30", "AMSOIL 4T Performance 10W-30 Synthetic Motorcycle Oil", "MC3", ["AM31012"], "mc3"),
    ("04-motocicletas-atv-marino", "4t-motorcycle", "10w-40", "AMSOIL 4T Performance 10W-40 Synthetic Motorcycle Oil", "MC4", ["AM23012", "AM23055"], "mc4"),
    ("04-motocicletas-atv-marino", "4t-motorcycle", "20w-50", "AMSOIL 4T Performance 20W-50 Synthetic Motorcycle Oil", "MC5", ["AM21012"], "4t-performance-20w-50"),
    ("04-motocicletas-atv-marino", "4t-motorcycle", "shock-therapy-suspension-fluid-10", "AMSOIL Shock Therapy #10 Medium Suspension Fluid", "STM", ["AM41012"], "stm-qt"),

    # 04-motocicletas-atv-marino / v-twin
    ("04-motocicletas-atv-marino", "v-twin", "sae-60", "AMSOIL SAE 60 100% Synthetic V-Twin Motorcycle Oil", "MCS", ["AM25012"], "mcs"),
    ("04-motocicletas-atv-marino", "v-twin", "15w-60", "AMSOIL 15W-60 100% Synthetic V-Twin Motorcycle Oil", "MSV", ["AM35012"], "msv"),
    ("04-motocicletas-atv-marino", "v-twin", "20w-40", "AMSOIL 20W-40 100% Synthetic V-Twin Motorcycle Oil", "MVI", ["AM36012"], "mvi"),
    ("04-motocicletas-atv-marino", "v-twin", "20w-50", "AMSOIL 20W-50 100% Synthetic V-Twin Motorcycle Oil", "MCV", ["AM32012"], "mcv"),
    ("04-motocicletas-atv-marino", "v-twin", "primary-fluid", "AMSOIL 100% Synthetic V-Twin Primary Fluid", "MVP", ["AM33012"], "mvp-qt"),
    ("04-motocicletas-atv-marino", "v-twin", "transmission-fluid", "AMSOIL 100% Synthetic V-Twin Transmission Fluid", "MVT", ["AM34012"], None),

    # 04-motocicletas-atv-marino / 2-stroke
    ("04-motocicletas-atv-marino", "2-stroke", "dominator-2-stroke-racing", "AMSOIL DOMINATOR 100% Synthetic 2-Stroke Racing Oil", "TDR", ["AMD13012"], "tdr"),
    ("04-motocicletas-atv-marino", "2-stroke", "interceptor-2-stroke", "AMSOIL INTERCEPTOR 100% Synthetic 2-Stroke Oil", "AIT", ["AMI0012"], "ait-1"),

    # 04-motocicletas-atv-marino / atv-utv
    ("04-motocicletas-atv-marino", "atv-utv", "5w-40", "AMSOIL 5W-40 100% Synthetic ATV/UTV Motor Oil", "AUV54", ["AMAU8712"], "auv54-sae-5w-40-qt"),
    ("04-motocicletas-atv-marino", "atv-utv", "5w-50", "AMSOIL 5W-50 100% Synthetic ATV/UTV Motor Oil", "AUV50", ["AMAU012"], "auv50"),
    ("04-motocicletas-atv-marino", "atv-utv", "10w-40", "AMSOIL 10W-40 100% Synthetic ATV/UTV Motor Oil", "AUV40", ["AMAU24012"], None),
    ("04-motocicletas-atv-marino", "atv-utv", "dct-fluid", "AMSOIL 100% Synthetic ATV/UTV Dual-Clutch Transmission Fluid", "AUDCT", ["AMAU2512"], None),
    ("04-motocicletas-atv-marino", "atv-utv", "transmission-and-differential-fluid", "AMSOIL 100% Synthetic ATV/UTV Transmission & Differential Fluid", "AUDT", ["AMAU6212"], "audt"),

    # 04-motocicletas-atv-marino / dirt-bike
    ("04-motocicletas-atv-marino", "dirt-bike", "10w-40", "AMSOIL 10W-40 100% Synthetic Dirt Bike Oil", "DB40", ["AMD2412"], "db40"),
    ("04-motocicletas-atv-marino", "dirt-bike", "10w-50", "AMSOIL 10W-50 100% Synthetic Dirt Bike Oil", "DB50", ["AMD2512"], "db50"),
    ("04-motocicletas-atv-marino", "dirt-bike", "transmission-fluid", "AMSOIL 100% Synthetic Dirt Bike Transmission Fluid", "DBTF", ["AMD2612"], None),

    # 04-motocicletas-atv-marino / metric-motorcycle
    ("04-motocicletas-atv-marino", "metric-motorcycle", "5w-40", "AMSOIL 5W-40 100% Synthetic Metric Motorcycle Oil", "MMF", ["AM42012"], "5w-40-100-synthetic-motorcycle-oil"),
    ("04-motocicletas-atv-marino", "metric-motorcycle", "10w-30", "AMSOIL 10W-30 100% Synthetic Metric Motorcycle Oil", "MCT", ["AM40012"], "métrico-10w-30"),
    ("04-motocicletas-atv-marino", "metric-motorcycle", "10w-40", "AMSOIL 10W-40 100% Synthetic Metric Motorcycle Oil", "MCF", ["AM37012"], "mcf"),
    ("04-motocicletas-atv-marino", "metric-motorcycle", "15w-50", "AMSOIL 15W-50 100% Synthetic Metric Motorcycle Oil", "MFF", ["AM38012"], "mff-sae-15w-50-qt"),

    # 04-motocicletas-atv-marino / marino
    ("04-motocicletas-atv-marino", "marino", "hp-marine-2-stroke", "AMSOIL HP Marine 100% Synthetic 2-Stroke Oil", "HPM", ["AM13012"], "hpm"),
]

print(f"Total defined products: {len(PRODUCTS)}")
