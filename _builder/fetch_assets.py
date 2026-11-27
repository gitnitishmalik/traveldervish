"""Downloads every photo and font the website uses into website/assets so nothing loads from external links.
Photos: Unsplash (free Unsplash License). Fonts: Fontshare (ITF Free Font License), woff2.
Run:  python _builder/fetch_assets.py
"""
import os, re, sys, urllib.request

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "website")
IMG = os.path.join(ROOT, "assets", "img")
FONT = os.path.join(ROOT, "assets", "fonts")
os.makedirs(IMG, exist_ok=True); os.makedirs(FONT, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"}

# name: (unsplash photo id, width, height)
PHOTOS = {
    "region-india":            ("photo-1650530777057-3a7dbc24bf6c", 900, 1000),
    "region-international":    ("photo-1551418843-01c6b62e864d", 900, 1000),
    "card-rajasthan":          ("photo-1599661046827-dacff0c0f09a", 900, 640),
    "card-thailand":           ("photo-1762950297584-23ea657c1bf8", 900, 640),
    "dest-delhi":              ("photo-1549526725-5c188c251c37", 600, 800),
    "dest-jaisalmer":          ("photo-1549944850-84e00be4203b", 600, 800),
    "dest-jodhpur":            ("photo-1590090750575-17b2cd4ceb85", 600, 800),
    "dest-udaipur":            ("photo-1633702738734-443da2c18f3c", 600, 800),
    "dest-jaipur":             ("photo-1545126178-862cdb469409", 600, 800),
    "dest-ranthambore":        ("photo-1549480017-d76466a4b7e8", 600, 800),
    "dest-agra":               ("photo-1587135941948-670b381f08ce", 600, 800),
    "dest-bangkok":            ("photo-1780776386940-769d45f5bd2e", 600, 800),
    "dest-pattaya":            ("photo-1644902617098-45abe72a7445", 600, 800),
    "dest-koh-larn":           ("photo-1646646504790-5bc33b86865c", 600, 800),
    "about-tuktuk":            ("photo-1508009603885-50cf7c579365", 800, 600),
    "gal-udaipur-lake":        ("photo-1633702738734-443da2c18f3c", 1400, 900),
    "gal-hawa-mahal":          ("photo-1650530777057-3a7dbc24bf6c", 1400, 900),
    "gal-amber-fort":          ("photo-1599661046827-dacff0c0f09a", 1400, 900),
    "gal-jodhpur-blue":        ("photo-1590090750575-17b2cd4ceb85", 1400, 900),
    "gal-camel-sunset":        ("photo-1510952267577-fc96d5ca660a", 1400, 900),
    "gal-tiger":               ("photo-1549480017-d76466a4b7e8", 1400, 900),
    "gal-taj-mahal":           ("photo-1587135941948-670b381f08ce", 1400, 900),
    "gal-jama-masjid":         ("photo-1549526725-5c188c251c37", 1400, 900),
    "gal-mehrangarh":          ("photo-1567771971104-545efaf89ddb", 1400, 900),
    "gal-wat-arun":            ("photo-1762950297584-23ea657c1bf8", 1400, 900),
    "gal-grand-palace":        ("photo-1780776386940-769d45f5bd2e", 1400, 900),
    "gal-sanctuary-of-truth":  ("photo-1644902617098-45abe72a7445", 1400, 900),
    "gal-thai-bay":            ("photo-1673627114937-ca220aad736d", 1400, 900),
    "gal-koh-larn-beach":      ("photo-1551418843-01c6b62e864d", 1400, 900),
    "gal-chinatown":           ("photo-1508009603885-50cf7c579365", 1400, 900),
    "gal-street-food":         ("photo-1506781961370-37a89d6b3095", 1400, 900),
    "gal-longtail":            ("photo-1646646504790-5bc33b86865c", 1400, 900),
    "gal-yaowarat-neon":       ("photo-1694501898583-7caca30dde01", 1400, 900),
}

# Smaller copies for phones and thumbnails ("<name>-sm.webp"); build.py adds them to srcset automatically.
VARIANTS = {"gal-": (700, 450), "card-": (560, 398), "region-": (540, 600)}
# Photos that come from local files instead of Unsplash: name -> (source, width, height, small width or None, crop box or None)
HERE = os.path.dirname(os.path.abspath(__file__))
LOCAL = {
    "hero-about":    (os.path.join(HERE, "..", "_flow", "frames", "05-about-jodhpur-blue.jpg"), 1920, 1080, 960, None),
    "hero-contact":  (os.path.join(HERE, "..", "_flow", "frames", "06-contact-wat-arun-night.jpg"), 1920, 1080, 960, None),
    "brand-sunrise": (os.path.join(HERE, "..", "WhatsApp Image 2026-11-26 at 3.44.34 PM.jpeg"), 1086, 600, None, (0, 690, 1086, 1290)),
}
QUALITY, QUALITY_SM = 60, 62   # WebP quality (fallback for older browsers)
AVIF_CRF, AVIF_CRF_SM = 35, 33  # AVIF quality (served first): about a third smaller than the WebP at the same look

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read()

def save_webp(im, name, q, crf=None):
    """Writes <name>.webp and <name>.avif (AVIF via ffmpeg + libaom; skipped if ffmpeg is missing)."""
    import subprocess, tempfile
    out = os.path.join(IMG, name + ".webp")
    im.save(out, "WEBP", quality=q, method=6)
    msg = f"img  {name}.webp {os.path.getsize(out)//1024} KB"
    tmp = os.path.join(tempfile.gettempdir(), "td-avif-src.png")
    im.save(tmp, "PNG")
    avif = os.path.join(IMG, name + ".avif")
    try:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-c:v", "libaom-av1", "-still-picture", "1", "-crf", str(crf or AVIF_CRF),
                        "-cpu-used", "5", "-row-mt", "1", "-pix_fmt", "yuv420p", avif], check=True)
        msg += f" | .avif {os.path.getsize(avif)//1024} KB"
    except (OSError, subprocess.CalledProcessError):
        msg += " | avif skipped (ffmpeg not found)"
    print(msg)

def photos(force=False):
    import io
    from PIL import Image
    for name, (pid, w, h) in PHOTOS.items():
        sm = next((v for k, v in VARIANTS.items() if name.startswith(k)), None)
        if not force and os.path.exists(os.path.join(IMG, name + ".webp")) and (not sm or os.path.exists(os.path.join(IMG, name + "-sm.webp"))):
            continue
        src = Image.open(io.BytesIO(get(f"https://images.unsplash.com/{pid}?w={w}&h={h}&fit=crop&crop=entropy&q=90&fm=jpg"))).convert("RGB")
        save_webp(src, name, QUALITY, AVIF_CRF)
        if sm:
            save_webp(src.resize(sm, Image.LANCZOS), name + "-sm", QUALITY_SM, AVIF_CRF_SM)
    for name, (path, w, h, smw, crop) in LOCAL.items():
        if not force and os.path.exists(os.path.join(IMG, name + ".avif")):
            continue
        src = Image.open(path).convert("RGB")
        if crop:
            src = src.crop(crop)
        src = src.resize((w, h), Image.LANCZOS)
        save_webp(src, name, QUALITY - 2 if smw else 72, AVIF_CRF)
        if smw:
            save_webp(src.resize((smw, smw * h // w), Image.LANCZOS), name + "-sm", QUALITY, AVIF_CRF_SM)

# Font faces the site actually uses: (family, weight, style, file name). Others are never requested.
USED_FACES = [("Boska", 500, "normal", "boska-500"), ("Boska", 500, "italic", "boska-500i"),
              ("Bespoke Stencil", 500, "normal", "bespoke-stencil-500"), ("Bespoke Stencil", 700, "normal", "bespoke-stencil-700"),
              ("Amulya", 400, "normal", "amulya-400"), ("Amulya", 500, "normal", "amulya-500"), ("Amulya", 700, "normal", "amulya-700")]
# Characters kept in each font: Latin, Latin-1, punctuation, rupee, arrow, sparkle
UNICODES = list(range(0x20, 0x7F)) + list(range(0xA0, 0x100)) + list(range(0x2010, 0x2028)) + list(range(0x2030, 0x203B)) + [0x20B9, 0x2122, 0x2192, 0x2726]
# Size-matched system fonts shown while a web font loads, so text does not jump when it swaps in
FALLBACKS = {"Boska": ("Georgia", "georgia.ttf"), "Bespoke Stencil": ("Arial", "arial.ttf"), "Amulya": ("Arial", "arial.ttf")}
FONT_SRC = os.path.join(HERE, "fonts-src")
CSS_OUT = os.path.join(HERE, "src", "fonts.css")
FREQ = {" ": .1874, "e": .0973, "t": .0703, "a": .0618, "o": .0597, "i": .0566, "n": .0539, "s": .0517, "r": .0477, "h": .0429,
        "l": .0329, "d": .0313, "u": .0222, "c": .0216, "m": .0189, "f": .0175, "p": .0153, "g": .0151, "y": .0144, "w": .0143,
        "b": .0119, "v": .0083, "k": .0067, "x": .0018, "j": .0012, "q": .0009, "z": .0007}

def download_fonts():
    """Original files from Fontshare into _builder/fonts-src (skipped when already there)."""
    os.makedirs(FONT_SRC, exist_ok=True)
    for fam_q in ["boska@500,501", "bespoke-stencil@500,700", "amulya@400,500,700"]:
        css = get("https://api.fontshare.com/v2/css?f[]=" + fam_q + "&display=swap").decode()
        for b in re.findall(r"@font-face\s*\{(.*?)\}", css, re.S):
            fam = re.search(r"font-family:\s*'([^']+)'", b).group(1)
            wt = re.search(r"font-weight:\s*(\d+)", b).group(1)
            st = re.search(r"font-style:\s*(\w+)", b).group(1)
            fname = f"{fam.lower().replace(' ', '-')}-{wt}{'i' if st == 'italic' else ''}.woff2"
            out = os.path.join(FONT_SRC, fname)
            if not os.path.exists(out):
                open(out, "wb").write(get("https:" + re.search(r"url\('([^']+\.woff2)'\)", b).group(1)))
                print("font", fname)

def _avg_width(font):
    cmap, hmtx, upm = font.getBestCmap(), font["hmtx"], font["head"].unitsPerEm
    tot = sum(f * hmtx[cmap[ord(c)]][0] for c, f in FREQ.items() if ord(c) in cmap)
    return tot / sum(f for c, f in FREQ.items() if ord(c) in cmap) / upm

def fonts():
    """Subset the used faces into website/assets/fonts and write _builder/src/fonts.css (with metric-matched fallbacks)."""
    from fontTools.ttLib import TTFont
    from fontTools import subset
    if not all(os.path.exists(os.path.join(FONT_SRC, f + ".woff2")) for *_, f in USED_FACES):
        download_fonts()
    for old in os.listdir(FONT):
        os.remove(os.path.join(FONT, old))
    css = ["/* Generated by _builder/fetch_assets.py: Boska, Bespoke Stencil and Amulya (Indian Type Foundry, ITF Free Font License) */"]
    metrics = {}
    for fam, wt, st, fname in USED_FACES:
        opts = subset.Options(); opts.flavor = "woff2"; opts.layout_features = ["*"]; opts.name_IDs = ["*"]; opts.notdef_outline = True
        font = TTFont(os.path.join(FONT_SRC, fname + ".woff2"))
        if fam not in metrics:
            hh = font["hhea"]
            metrics[fam] = (_avg_width(font), hh.ascent / font["head"].unitsPerEm, abs(hh.descent) / font["head"].unitsPerEm, hh.lineGap / font["head"].unitsPerEm)
        sub = subset.Subsetter(opts); sub.populate(unicodes=UNICODES); sub.subset(font)
        out = os.path.join(FONT, fname + ".woff2"); font.flavor = "woff2"; font.save(out)
        print(f"font {fname}.woff2  {os.path.getsize(out)//1024} KB")
        css.append(f"@font-face{{font-family:'{fam}';font-style:{st};font-weight:{wt};font-display:swap;src:url('../fonts/{fname}.woff2') format('woff2')}}")
    for fam, (local_name, local_file) in FALLBACKS.items():
        fb = TTFont(os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", local_file))
        avg, asc, desc, gap = metrics[fam]
        size = avg / _avg_width(fb)
        css.append(f"@font-face{{font-family:'{fam} Fallback';src:local('{local_name}');size-adjust:{size*100:.2f}%;"
                   f"ascent-override:{asc/size*100:.2f}%;descent-override:{desc/size*100:.2f}%;line-gap-override:{gap/size*100:.2f}%}}")
    os.makedirs(os.path.dirname(CSS_OUT), exist_ok=True)
    open(CSS_OUT, "w", encoding="utf-8", newline="\n").write("\n".join(css) + "\n")
    print("wrote _builder/src/fonts.css")

if __name__ == "__main__":
    force = "--force" in sys.argv   # --force re-creates every photo, e.g. after changing QUALITY
    if "--photos-only" not in sys.argv:
        fonts()
    photos(force)
    print("done")
