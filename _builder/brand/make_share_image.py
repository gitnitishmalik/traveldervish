"""Makes the link-preview card (WhatsApp / Facebook / LinkedIn) and the iPhone home-screen icon from the real logo and fonts.
Run:  python _builder/brand/make_share_image.py      (needs Playwright + Google Chrome, and Pillow)
Writes website/assets/img/og-travel-dervish.jpg (1200x630) and website/assets/img/apple-touch-icon.png (180x180).
"""
import io, pathlib
from playwright.sync_api import sync_playwright
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parent.parent / "website"
IMG = SITE / "assets" / "img"
logo_svg = (IMG / "logo-dark.svg").read_text(encoding="utf-8").replace("<svg ", '<svg class="logo" ', 1)
fav_svg = (IMG / "favicon.svg").read_text(encoding="utf-8").replace("<svg ", '<svg style="width:180px;height:180px;display:block" ', 1)

CARD = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:'Boska';font-weight:500;src:url('http://travel.local/assets/fonts/boska-500.woff2')}}
@font-face{{font-family:'Boska';font-style:italic;font-weight:500;src:url('http://travel.local/assets/fonts/boska-500i.woff2')}}
@font-face{{font-family:'Amulya';font-weight:500;src:url('http://travel.local/assets/fonts/amulya-500.woff2')}}
html,body{{margin:0;width:1200px;height:630px}}
body{{position:relative;overflow:hidden;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#121110;
  background:radial-gradient(ellipse 75% 60% at 50% 118%,#F9D998 0%,#FBEFD6 38%,#FBF6EC 70%);font-family:'Amulya',Arial,sans-serif}}
.logo{{width:860px;height:auto;display:block}}
.rule{{width:120px;height:5px;border-radius:3px;background:#FCC800;margin:40px 0 32px}}
h1{{margin:0;font-family:'Boska',Georgia,serif;font-weight:500;font-size:60px;letter-spacing:-.01em;line-height:1.05}}
h1 em{{font-style:italic}}
.motto{{display:flex;align-items:center;gap:24px;margin-top:30px;font-weight:500;font-size:20px;letter-spacing:.42em}}
.motto i{{display:block;width:1.5px;height:20px;background:#121110;opacity:.5}}
.bar{{position:absolute;left:0;right:0;bottom:0;height:14px;background:#FCC800}}
</style></head><body>
{logo_svg}
<div class="rule"></div>
<h1>Your Travel Partner for <em>Every</em> Journey</h1>
<div class="motto"><span>PLAN</span><i></i><span>BOOK</span><i></i><span>EXPLORE</span></div>
<div class="bar"></div>
</body></html>"""

ICON = f"""<!doctype html><html><body style="margin:0;width:180px;height:180px;background:#121110">{fav_svg}</body></html>"""

def serve(route):
    path = route.request.url.split("travel.local/", 1)[1]
    f = SITE / path
    if f.is_file():
        route.fulfill(status=200, body=f.read_bytes(), headers={"Content-Type": "font/woff2", "Access-Control-Allow-Origin": "*"})
    else:
        route.fulfill(status=404, body="")

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome", headless=True)
    pg = b.new_page(viewport={"width": 1200, "height": 630})
    pg.route("http://travel.local/**", serve)
    pg.set_content(CARD); pg.wait_for_timeout(300)
    pg.evaluate("document.fonts.ready")
    card = Image.open(io.BytesIO(pg.screenshot())).convert("RGB")
    out = IMG / "og-travel-dervish.jpg"
    card.save(out, "JPEG", quality=90, optimize=True, progressive=True)
    print("wrote", out.name, card.size, out.stat().st_size // 1024, "KB")
    pg.set_viewport_size({"width": 180, "height": 180})
    pg.set_content(ICON); pg.wait_for_timeout(100)
    icon = Image.open(io.BytesIO(pg.screenshot())).convert("RGB")
    icon.save(IMG / "apple-touch-icon.png", "PNG", optimize=True)
    print("wrote apple-touch-icon.png", icon.size)
    b.close()
