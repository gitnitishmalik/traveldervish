"""Travel Dervish static site generator (page templates).
All editable content (contact details, packages, FAQs, banner clips) is in content.py.
Run:  python _builder/build.py      Output: ../website  (upload the CONTENTS of that folder to Hostinger)
"""
import os, sys, json, html, math, random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from content import SITE, HERO_CHAPTERS, AIRPORTS, PACKAGES, DESTINATIONS, FAQS, FLIGHT_FAQS  # noqa: E402

OUT = os.path.join(HERE, "..", "website")
SRC = os.path.join(HERE, "src")
ASSET_V = {"css": "0", "js": "0"}
INLINE_CSS = ""
PKG = {p["slug"]: p for p in PACKAGES}
WA_ON = SITE["show_whatsapp"]
WA_LINK = f"https://wa.me/{SITE['whatsapp']}?text=" + "Hello%20Travel%20Dervish%2C%20I%27d%20like%20to%20plan%20a%20trip."

# ----------------------------------------------------------------------------------
# Images
# ----------------------------------------------------------------------------------
DIMS = {
    "hero": (1920, 1080), "poster": (1280, 720), "region": (900, 1000), "card": (900, 640), "dest": (600, 800),
    "spot-jodhpur-fort": (900, 1100), "spot-camel-caravan": (900, 640), "band": (1920, 900), "page": (1920, 700),
    "about-market": (800, 1000), "about-tuktuk": (800, 600), "gal": (1400, 900), "brand-sunrise": (1086, 600),
}
def dims(name):
    for k, v in DIMS.items():
        if name == k or name.startswith(k):
            return v
    return (1200, 800)

# Smaller "-sm" copies (made by fetch_assets.py / encode_video.sh) are offered through srcset so phones and thumbnails load less
SM_W = {"gal-": 700, "card-": 560, "region-": 540, "hero-": 960, "poster-": 768}
SIZES = {"gal-": "(max-width: 860px) 50vw, 25vw", "card-": "(max-width: 760px) 92vw, (max-width: 1024px) 46vw, 400px",
         "region-": "(max-width: 760px) 92vw, 46vw", "hero-": "100vw", "poster-": "100vw"}
IMG_DIR = os.path.join(OUT, "assets", "img")

def srcset(name, sizes=None, ext="webp"):
    w, _ = dims(name)
    pre = next((k for k in SM_W if name.startswith(k)), None)
    if not pre or not os.path.exists(os.path.join(IMG_DIR, f"{name}-sm.{ext}")):
        return ""
    return f' srcset="assets/img/{name}-sm.{ext} {SM_W[pre]}w, assets/img/{name}.{ext} {w}w" sizes="{sizes or SIZES[pre]}"'

def avif_source(name, sizes=None):
    """AVIF is about a third lighter than WebP; browsers that can't show it fall back to the WebP <img>."""
    if not os.path.exists(os.path.join(IMG_DIR, name + ".avif")):
        return ""
    return f'<source type="image/avif"{srcset(name, sizes, "avif") or f' srcset="assets/img/{name}.avif"'}>'

def picture(name, img_tag, sizes=None):
    src = avif_source(name, sizes)
    return f"<picture>{src}{img_tag}</picture>" if src else img_tag

def img(name, alt, cls="", lazy=True, extra="", sizes=None):
    w, h = dims(name)
    c = f' class="{cls}"' if cls else ""
    l = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    return picture(name, f'<img src="assets/img/{name}.webp"{srcset(name, sizes)} alt="{html.escape(alt)}" width="{w}" height="{h}"{c}{l}{extra}>', sizes)

def video_attrs(key):
    return f'data-hd="assets/video/{key}-hd.mp4" data-sm="assets/video/{key}-sm.mp4"'

def lazy_video(key, cls="bgvideo"):
    """A muted looping clip that loads only when scrolled near; until then a lazy AVIF still of its first frame shows."""
    still_img = (f'<img class="{cls}" src="assets/img/poster-{key}.webp"{srcset("poster-" + key)} alt="" width="1280" height="720" '
                 f'loading="lazy" decoding="async">')
    return (picture("poster-" + key, still_img) +
            f'<video class="{cls}" muted loop playsinline preload="none" {video_attrs(key)} data-lazy-video aria-hidden="true"></video>')

# ----------------------------------------------------------------------------------
# Icons + logo (one inline SVG sprite: no icon font, no external files)
# ----------------------------------------------------------------------------------
ICONS = {
    "pin": '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
    "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><path d="M16 4.8a3.2 3.2 0 0 1 0 6.4M21 20c0-2.8-1.8-5.1-4.3-5.8"/>',
    "car": '<path d="M3 13l2-6h14l2 6v5H3z"/><circle cx="7.5" cy="15.5" r="1.3"/><circle cx="16.5" cy="15.5" r="1.3"/><path d="M5 18v2M19 18v2M3 13h18"/>',
    "bed": '<path d="M3 18V7M3 14h18v4M21 18v-4a3 3 0 0 0-3-3h-7v3"/><circle cx="7" cy="11" r="1.8"/>',
    "route": '<circle cx="6" cy="18" r="2.2"/><circle cx="18" cy="6" r="2.2"/><path d="M8.2 18H15a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h6.8"/>',
    "compass": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="M3.5 6.5l8.5 6.5 8.5-6.5"/>',
    "whatsapp": '<path d="M20 11.6A8.4 8.4 0 0 1 7.6 19L3.5 20.5 5 16.5A8.4 8.4 0 1 1 20 11.6z"/><path d="M9 8.5c0 3.6 2.9 6.5 6.5 6.5l1-1.6-2-1-1 1a4.6 4.6 0 0 1-2.4-2.4l1-1-1-2z"/>',
    "instagram": '<rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r=".9"/>',
    "facebook": '<path d="M14 8h3V4h-3a4 4 0 0 0-4 4v3H7v4h3v6h4v-6h3l1-4h-4V8z"/>',
    "pinterest": '<circle cx="12" cy="12" r="9"/><path d="M10.5 20.5l2-8.5M10.2 13.6c-1-3.6 1-6.6 3.4-6.6 2.3 0 3.5 1.6 3.5 3.5 0 2.6-1.6 4.5-3.6 4.5-1 0-1.8-.6-1.6-1.6"/>',
    "arrow-right": '<path d="M4 12h16M14 6l6 6-6 6"/>',
    "arrow-left": '<path d="M20 12H4M10 6l-6 6 6 6"/>',
    "arrow-up": '<path d="M12 20V4M6 10l6-6 6 6"/>',
    "arrow-up-right": '<path d="M7 17L17 7M8 7h9v9"/>',
    "chevron": '<path d="M6 9l6 6 6-6"/>',
    "chevron-right": '<path d="M9 6l6 6-6 6"/>',
    "download": '<path d="M12 4v11M7 10l5 5 5-5M4 20h16"/>',
    "menu": '<path d="M4 7h16M4 12h10M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6L6 18"/>',
    "search": '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>',
    "send": '<path d="M21 3L3 10.5l7 3 3 7z"/><path d="M10 13.5L21 3"/>',
    "plane": '<path d="M21 15.5v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0v5l-8 5v2l8-2.5V18l-2 1.5V21l3.5-1 3.5 1v-1.5L13 18v-5z"/>',
    "plane-fill": '<path fill="currentColor" stroke="none" d="M21 15.5v-2l-8-5V3.5a1.5 1.5 0 0 0-3 0v5l-8 5v2l8-2.5V18l-2 1.5V21l3.5-1 3.5 1v-1.5L13 18v-5z"/>',
    "takeoff": '<path d="M3 20.5h18"/><path d="M4.5 14.2l2.2 2.6 12.6-4a1.8 1.8 0 0 0-1-3.5l-4.2 1.2-5.6-4.4-2 .6 3.3 5.1-3.6 1-2-1.4-1.6.5z"/>',
    "ticket": '<path d="M3 9V7a1.5 1.5 0 0 1 1.5-1.5h15A1.5 1.5 0 0 1 21 7v2a3 3 0 0 0 0 6v2a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 17v-2a3 3 0 0 0 0-6z"/><path d="M6.5 12h4"/><path d="M12.5 13.8l4.6-3.2c.5-.3 1.1.2.8.7l-3.2 4.6-.9-.6-.1-1.4-1.4-.1z"/>',
    "mountain": '<path d="M2.5 20l6.2-9.5 4 6 2.8-3.8 6 7.3z"/><path d="M17 3.2a2.6 2.6 0 0 1 2.6 2.6c0 2-2.6 4.7-2.6 4.7s-2.6-2.7-2.6-4.7A2.6 2.6 0 0 1 17 3.2z"/>',
    "swap": '<path d="M7 4L3 8l4 4M3 8h14M17 20l4-4-4-4M21 16H7"/>',
    "drag": '<path d="M8 7l-5 5 5 5M16 7l5 5-5 5M3 12h18"/>',
    "luggage": '<rect x="6" y="7" width="12" height="13" rx="2"/><path d="M9 7V4.5h6V7M9.5 11v5M14.5 11v5M8.5 20v1.5M15.5 20v1.5"/>',
    "passport": '<rect x="5" y="3" width="14" height="18" rx="2"/><circle cx="12" cy="10.5" r="3.5"/><path d="M8.5 10.5h7M12 7c1 1 1.3 2.2 1.3 3.5S13 13 12 14c-1-1-1.3-2.2-1.3-3.5S11 8 12 7zM9 17.5h6"/>',
    "star": '<path d="M12 3.5l2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 16.9l-5.2 2.7 1-5.8L3.5 9.7l5.9-.9z"/>',
    "sparkle": '<path d="M12 3l2 6 6 2-6 2-2 6-2-6-6-2 6-2z"/><path d="M19 3v3M17.5 4.5h3"/>',
    "shield": '<path d="M12 3l8 3v6c0 4.5-3.4 8.2-8 9-4.6-.8-8-4.5-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2.5M12 19v2.5M2.5 12H5M19 12h2.5M5.3 5.3l1.8 1.8M16.9 16.9l1.8 1.8M5.3 18.7l1.8-1.8M16.9 7.1l1.8-1.8"/>',
    "temple": '<path d="M12 2.5l1.5 3h-3z"/><path d="M6 9.5h12l-2-4H8z"/><path d="M5 20.5h14M7 9.5v11M17 9.5v11M10.5 20.5v-5h3v5"/>',
    "wave": '<path d="M2.5 15c2 0 2-1.5 4-1.5s2 1.5 4 1.5 2-1.5 4-1.5 2 1.5 4 1.5 2-1.5 3-1.5"/><path d="M2.5 19c2 0 2-1.5 4-1.5s2 1.5 4 1.5 2-1.5 4-1.5 2 1.5 4 1.5 2-1.5 3-1.5"/><circle cx="16" cy="7" r="3"/>',
    "paw": '<circle cx="7" cy="9" r="1.8"/><circle cx="11" cy="6" r="1.8"/><circle cx="15" cy="6.5" r="1.8"/><circle cx="18" cy="10" r="1.8"/><path d="M8.5 16.5c0-2.5 1.8-4.5 3.8-4.5s3.7 2 3.7 4.5c0 2-1.5 3-3.7 3s-3.8-1-3.8-3z"/>',
    "dune": '<path d="M2.5 18.5c3-4 6-6 9.5-6s6.5 2 9.5 6"/><path d="M2.5 18.5h19"/><circle cx="17" cy="6.5" r="2.5"/>',
    "city": '<path d="M3 21V9l5-3v15M8 21V4l7 3v14M15 21V11l6 2v8M3 21h18"/>',
    "food": '<path d="M7 3v8M5 3v5a2 2 0 0 0 4 0V3M7 11v10M17 3c-2 1-3 3.5-3 6.5h3V21"/>',
    "boat": '<path d="M3 15l2 5h14l2-5z"/><path d="M12 15V4l6 9h-6"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8v.01"/>',
    "grid": '<rect x="3.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.5"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.5 3.8 5.5 3.8 9s-1.3 6.5-3.8 9c-2.5-2.5-3.8-5.5-3.8-9S9.5 5.5 12 3z"/>',
    "heart": '<path d="M12 20s-7.5-4.6-9-9.3C2 7.2 4.2 4.5 7.2 4.5c2 0 3.6 1.2 4.8 3 1.2-1.8 2.8-3 4.8-3 3 0 5.2 2.7 4.2 6.2C19.5 15.4 12 20 12 20z"/>',
    "map": '<path d="M9 4L3 6.5v13.5L9 17.5l6 2.5 6-2.5V4l-6 2.5z"/><path d="M9 4v13.5M15 6.5V20"/>',
    "pause": '<path d="M9 6v12M15 6v12"/>',
    "play": '<path d="M8 5.5v13l10.5-6.5z"/>',
    "user": '<circle cx="12" cy="8" r="3.8"/><path d="M4.5 20.5c0-4.1 3.4-7 7.5-7s7.5 2.9 7.5 7"/>',
}
def icon(name, cls="i"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'

_vb, _dy, _dk = open(os.path.join(HERE, "brand", "logo-paths.txt"), encoding="utf-8").read().split("\n")[:3]
LOGO_VB = _vb
SCRIPT_ICONS = {"arrow-left", "arrow-right", "arrow-up-right"}   # drawn by site.js (carousel cursor)

def sprite(names):
    return ('<svg xmlns="http://www.w3.org/2000/svg" style="display:none">'
            + "".join(f'<symbol id="i-{k}" viewBox="0 0 24 24">{v}</symbol>' for k, v in ICONS.items() if k in names)
            + f'<symbol id="brand" viewBox="{LOGO_VB}"><path fill="#FCC800" fill-rule="evenodd" d="{_dy}"/>'
            + f'<path fill="currentColor" fill-rule="evenodd" d="{_dk}"/></symbol></svg>')

def logo(cls=""):
    return (f'<a href="index.html" class="logo {cls}" aria-label="Travel Dervish home">'
            f'<svg class="logo__mark" viewBox="0 0 {LOGO_VB.split()[2]} {LOGO_VB.split()[3]}" aria-hidden="true"><use href="#brand"/></svg></a>')

def motto(light=False):
    return f'<div class="motto{" motto--light" if light else ""}"><span>Plan</span><i></i><span>Book</span><i></i><span>Explore</span></div>'

def head(kicker, title, lead="", center=False, light=False, extra=""):
    cls = "head" + (" head--center" if center else "") + (" head--light" if light else "")
    lp = f'<p class="lead">{lead}</p>' if lead else ""
    return f'<div class="{cls}" data-reveal><span class="kicker">{kicker}</span><h2 class="title">{title}</h2>{lp}{extra}</div>'

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
def month_select(id_, name="month"):
    opts = '<option value="">Flexible</option>' + "".join(f'<option value="{m}">{m}</option>' for m in MONTHS)
    return f'<select id="{id_}" name="{name}">{opts}</select>'

PAX = [("1", "1 traveller"), ("2", "2 travellers"), ("3-4", "3&ndash;4 travellers"), ("5-8", "5&ndash;8 travellers"), ("9+", "9+ travellers")]
def pax_select(id_, selected="2"):
    return f'<select id="{id_}" name="travellers">' + "".join(
        f'<option value="{v}"{" selected" if v == selected else ""}>{t}</option>' for v, t in PAX) + "</select>"

CABINS = ["Economy", "Premium economy", "Business", "First"]
def cabin_select(id_):
    return f'<select id="{id_}" name="cabin">' + "".join(f'<option value="{c}">{c}</option>' for c in CABINS) + "</select>"

AIRPORT_LIST = ('<datalist id="airports">' + "".join(f'<option value="{c} ({code})"></option>' for c, code in AIRPORTS) + "</datalist>")

def short_dur(p):
    return f'{p["days_n"]}D / {p["days_n"] - 1}N'

# ----------------------------------------------------------------------------------
# Shared layout
# ----------------------------------------------------------------------------------
NAV = [("home", "Home", "index.html"), ("journeys", "Holidays", "journeys.html"), ("india", "India", "journeys.html?type=india"),
       ("international", "International", "journeys.html?type=international"), ("flights", "Flights", "flights.html"),
       ("about", "About", "about.html"), ("contact", "Contact", "contact.html")]

def socials(cls="i"):
    return "".join(f'<a href="{SITE[k]}" target="_blank" rel="noopener" aria-label="{k.title()}">{icon(k, cls)}</a>'
                   for k in ("instagram", "facebook", "pinterest"))

def header(active, overlay):
    links = "".join(f'<a class="nav__link{" is-active" if k == active else ""}" href="{u}">{t}</a>' for k, t, u in NAV)
    mlinks = "".join(f'<a class="m-link{" is-active" if k == active else ""}" href="{u}"><span>{t}</span>{icon("arrow-right", "i i--sm")}</a>' for k, t, u in NAV)
    wa_m = (f'<a href="{WA_LINK}" target="_blank" rel="noopener" class="btn btn--line-light btn--block">{icon("whatsapp", "i i--sm")} WhatsApp us</a>' if WA_ON else "")
    return f'''
<div class="topbar"><div class="container topbar__inner">
  {motto(light=True)}
  <div class="topbar__right">
    <a href="tel:{SITE["phone_link"]}">{icon("phone", "i i--sm")}<span>{SITE["phone_display"]}</span></a>
    <a href="mailto:{SITE["email"]}" class="hide-sm">{icon("mail", "i i--sm")}<span>{SITE["email"]}</span></a>
    <div class="topbar__social">{socials("i i--sm")}</div>
  </div>
</div></div>
<header class="header{" header--overlay" if overlay else " header--solid"}">
  <div class="container header__inner">
    {logo()}
    <nav class="nav" aria-label="Main">{links}</nav>
    <div class="header__actions">
      <a href="contact.html" class="btn btn--sun btn--sm hide-xs">Plan my trip {icon("arrow-right", "i i--sm")}</a>
      <button class="nav-toggle" data-nav-open aria-label="Open menu">{icon("menu")}</button>
    </div>
  </div>
</header>
<div class="mobile-nav" aria-label="Mobile menu">
  <div class="mobile-nav__top">{logo("logo--light")}<button class="mobile-nav__close" data-nav-close aria-label="Close menu">{icon("close")}</button></div>
  <nav class="mobile-nav__links">{mlinks}</nav>
  <div class="mobile-nav__foot">
    <a href="contact.html" class="btn btn--sun btn--lg btn--block">{icon("send", "i i--sm")} Plan my trip</a>
    <a href="tel:{SITE["phone_link"]}" class="btn btn--line-light btn--block">{icon("phone", "i i--sm")} Call {SITE["phone_display"]}</a>
    {wa_m}
    {motto(light=True)}
  </div>
</div>'''

def footer():
    pk = "".join(f'<a href="{x["file"]}">{x["short"]}</a>' for x in PACKAGES)
    wa_li = (f'<li>{icon("whatsapp")}<a href="{WA_LINK}" target="_blank" rel="noopener">Chat on WhatsApp</a></li>' if WA_ON else "")
    wa_float = (f'<a href="{WA_LINK}" class="wa-float" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{icon("whatsapp")}</a>' if WA_ON else "")
    return f'''
<footer class="footer">
  <div class="footer__glow" aria-hidden="true"></div>
  <div class="container footer__top">
    <div>
      {logo("logo--light logo--lg")}
      <p class="footer__tag">Your travel partner for <em>every</em> journey.</p>
      {motto(light=True)}
    </div>
    <a href="contact.html" class="footer__cta"><span>Start planning</span>{icon("arrow-up-right")}</a>
  </div>
  <div class="container footer__grid">
    <div><h4>Holidays</h4><div class="footer__links">{pk}<a href="journeys.html?type=india">India holidays</a><a href="journeys.html?type=international">International holidays</a><a href="journeys.html">All holidays</a></div></div>
    <div><h4>Services</h4><div class="footer__links"><a href="flights.html">Flight tickets</a><a href="journeys.html">Holiday packages</a><a href="contact.html?journey=custom">Custom itineraries</a><a href="contact.html?service=both">Flight + holiday</a></div></div>
    <div><h4>Company</h4><div class="footer__links"><a href="about.html">About us</a><a href="contact.html">Contact</a><a href="{SITE["parent"]}" target="_blank" rel="noopener">Design Dervish {icon("arrow-up-right", "i i--sm")}</a></div></div>
    <div>
      <h4>Get in touch</h4>
      <ul class="footer__contact">
        <li>{icon("phone")}<a href="tel:{SITE["phone_link"]}">{SITE["phone_display"]}</a></li>
        {wa_li}
        <li>{icon("mail")}<a href="mailto:{SITE["email"]}">{SITE["email"]}</a></li>
        <li>{icon("pin")}<span>{SITE["city"]}</span></li>
      </ul>
      <div class="socials">{socials()}</div>
    </div>
  </div>
  <div class="container footer__bottom">
    <span>&copy; <span data-year>2026</span> Travel Dervish. All rights reserved.</span>
    <span>A <a href="{SITE["parent"]}" target="_blank" rel="noopener">Design Dervish</a> venture</span>
  </div>
</footer>
{wa_float}
<button class="to-top" aria-label="Back to top">{icon("arrow-up")}</button>'''

LIGHTBOX = f'''
<div class="lightbox" role="dialog" aria-label="Photo viewer">
  <button class="lightbox__close" aria-label="Close">{icon("close")}</button>
  <button class="lightbox__prev" aria-label="Previous photo">{icon("arrow-left")}</button>
  <img src="" alt="">
  <button class="lightbox__next" aria-label="Next photo">{icon("arrow-right")}</button>
  <div class="lightbox__cap"></div>
</div>'''

import hashlib, re as _re

def minify_css(css):
    # keep strings, drop comments, then squeeze whitespace outside strings
    tok = _re.compile(r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|(/\*.*?\*/)', _re.S)
    css = tok.sub(lambda m: m.group(1) or "", css)
    parts = _re.split(r'("(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')', css)
    for i in range(0, len(parts), 2):
        t = _re.sub(r"\s+", " ", parts[i])
        t = _re.sub(r"\s*([{};,>])\s*", r"\1", t)
        t = _re.sub(r":\s+", ":", t)
        parts[i] = t.replace(";}", "}")
    return "".join(parts).strip()

def minify_js(js):
    # conservative: drop whole-line comments and indentation; keep line breaks
    out = []
    for line in js.split("\n"):
        t = line.strip()
        if not t or t.startswith("//") or (t.startswith("/*") and t.endswith("*/")):
            continue
        out.append(t)
    return "\n".join(out) + "\n"

def build_assets():
    css = open(os.path.join(SRC, "fonts.css"), encoding="utf-8").read() + "\n" + open(os.path.join(SRC, "style.css"), encoding="utf-8").read()
    global INLINE_CSS
    css = minify_css(css)
    INLINE_CSS = css.replace("url('../fonts/", "url('assets/fonts/")
    print(f"inlined CSS  {len(INLINE_CSS)//1024} KB per page")
    old = os.path.join(OUT, "assets", "css", "site.css")   # earlier builds used an external stylesheet
    if os.path.exists(old):
        os.remove(old)
    js = minify_js(open(os.path.join(SRC, "main.js"), encoding="utf-8").read())
    for sub, name, data, key in (("js", "site.js", js, "js"),):
        os.makedirs(os.path.join(OUT, "assets", sub), exist_ok=True)
        open(os.path.join(OUT, "assets", sub, name), "w", encoding="utf-8", newline="\n").write(data)
        ASSET_V[key] = hashlib.md5(data.encode("utf-8")).hexdigest()[:8]
        print(f"built assets/{sub}/{name}  {len(data)//1024} KB")

def minify_html(doc):
    return "\n".join(l.strip() for l in doc.split("\n") if l.strip()) + "\n"

def lcp_preload(body):
    m = _re.search(r'(?:<picture>(<source type="image/avif"[^>]*>))?<img[^>]*fetchpriority="high"[^>]*>', body)
    if not m:
        return ""
    if m.group(1):
        ss = _re.search(r' srcset="([^"]+)"', m.group(1)); sz = _re.search(r' sizes="([^"]+)"', m.group(1))
        href = ss.group(1).split(",")[-1].strip().split(" ")[0]
        extra = (f' imagesrcset="{ss.group(1)}"' if "," in ss.group(1) else "") + (f' imagesizes="{sz.group(1)}"' if sz else "")
        return f'<link rel="preload" as="image" type="image/avif" href="{href}"{extra} fetchpriority="high">'
    tag = m.group(0)
    src = _re.search(r' src="([^"]+)"', tag).group(1)
    ss = _re.search(r' srcset="([^"]+)"', tag); sz = _re.search(r' sizes="([^"]+)"', tag)
    extra = (f' imagesrcset="{ss.group(1)}" imagesizes="{sz.group(1)}"' if ss and sz else "")
    return f'<link rel="preload" as="image" href="{src}"{extra} fetchpriority="high">'

# Chrome/Edge: fetch and pre-render the next page as soon as a link is hovered (or pressed on touch), so clicks open instantly
_SPEC_WHERE = {"and": [{"href_matches": "/*"}, {"not": {"href_matches": "/assets/*"}},
                       {"not": {"selector_matches": "[download], [target=_blank]"}}]}
SPECULATION = ('<script type="speculationrules">' + json.dumps({"prefetch": [{"where": _SPEC_WHERE, "eagerness": "moderate"}],
               "prerender": [{"where": _SPEC_WHERE, "eagerness": "moderate"}]}) + '</script>')

FONT_PRELOAD = "".join(f'<link rel="preload" href="assets/fonts/{f}.woff2" as="font" type="font/woff2" crossorigin>'
                       for f in ("boska-500", "boska-500i", "amulya-400", "bespoke-stencil-500"))

def clean_links(doc):
    """index.html -> /, about.html -> about, journeys.html?type=india -> journeys?type=india (links, forms, data-page)."""
    doc = _re.sub(r'(href|action|data-page)="index\.html(?=["#?])', r'\1="/', doc)
    return _re.sub(r'(href|action|data-page)="([a-z0-9-]+)\.html(?=["#?])', r'\1="\2', doc)

def page(fname, title, desc, body, active="", overlay=True, og="poster-desert", jsonld=None, lightbox=False, datalist=False):
    canon = SITE["url"] + "/" + ("" if fname == "index.html" else fname.removesuffix(".html"))
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    wa_attr = f' data-wa="{SITE["whatsapp"]}"' if WA_ON else ""
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Travel Dervish">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE["url"]}/assets/img/og-travel-dervish.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Travel Dervish: Your Travel Partner for Every Journey">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE["url"]}/assets/img/og-travel-dervish.jpg">
<meta name="theme-color" content="#121110">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
{lcp_preload(body)}
{FONT_PRELOAD}
<style>{INLINE_CSS}</style>
{SPECULATION}
<script>document.documentElement.className += ' js';</script>
{ld}
</head>
<body{wa_attr}>
@@SPRITE@@
<a class="sr-only" href="#main">Skip to content</a>
{header(active, overlay)}
<main id="main">
{body}
</main>
{footer()}
{AIRPORT_LIST if datalist else ""}
{LIGHTBOX if lightbox else ""}
<script src="assets/js/site.js?v={ASSET_V["js"]}" defer></script>
</body>
</html>
'''
    doc = clean_links(doc)
    if fname == "404.html":   # the 404 page is shown at any address, so its relative links must start from the site root
        doc = doc.replace("<head>", '<head>\n<base href="/">', 1)
    used = set(_re.findall(r'#i-([\w-]+)', doc)) | (SCRIPT_ICONS if "data-flow" in doc else set())
    doc = doc.replace("@@SPRITE@@", sprite(used))
    with open(os.path.join(OUT, fname), "w", encoding="utf-8", newline="\n") as f:
        f.write(minify_html(doc))
    print("built", fname)

# ----------------------------------------------------------------------------------
# Banners
# ----------------------------------------------------------------------------------
def clip(key, active=True, first=True):
    load = ' fetchpriority="high"' if first else ' loading="lazy" decoding="async" fetchpriority="low"'
    if first:  # the poster (= first video frame) paints instantly; the script starts the video once the page has loaded
        vid = (f'<video muted loop playsinline preload="none" aria-hidden="true">'
               f'<source src="assets/video/{key}-hd.mp4" type="video/mp4" media="(min-width: 900px)">'
               f'<source src="assets/video/{key}-sm.mp4" type="video/mp4"></video>')
    else:
        vid = '<video muted loop playsinline preload="none" aria-hidden="true"></video>'
    poster = picture("poster-" + key, f'<img class="clip__poster" src="assets/img/poster-{key}.webp"{srcset("poster-" + key)} alt="" width="1280" height="720"{load}>')
    return f'<div class="clip{" is-active" if active else ""}" data-clip {video_attrs(key)}>{poster}{vid}</div>'

def still(name, alt):
    return f'<div class="clip is-active clip--still">{img(name, alt, lazy=False)}</div>'

def ridge(seed, base, amp, w=1440, h=320, step=60):
    rnd = random.Random(seed)
    ph = [rnd.uniform(0, 6.28) for _ in range(3)]
    pts = [(x, base - amp * (0.55 * math.sin(x / 230 + ph[0]) + 0.3 * math.sin(x / 97 + ph[1]) + 0.15 * math.sin(x / 41 + ph[2])))
           for x in range(0, w + step, step)]
    d = f"M0 {h}L0 {pts[0][1]:.0f}"
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        d += f"Q{x0} {y0:.0f} {(x0 + x1) / 2:.0f} {(y0 + y1) / 2:.0f}"
    return d + f"L{w} {pts[-1][1]:.0f}L{w} {h}Z"

def sky_scene():
    """Code-built 3D banner: sunrise sky, layered mountains, drifting mist and a plane on a contrail arc."""
    def mtn(n, seed, base, amp, depth):
        return (f'<svg class="sky__mtn sky__mtn--{n}" style="--d:{depth}" viewBox="0 0 1440 320" preserveAspectRatio="none">'
                f'<path d="{ridge(seed, base, amp)}"/></svg>')
    return f'''
<div class="sky" aria-hidden="true">
  <div class="sky__sun" style="--d:4"></div>
  <div class="sky__clouds"></div>
  {mtn(3, 7, 150, 70, 6)}{mtn(2, 19, 190, 60, 14)}<div class="sky__mist"></div>{mtn(1, 31, 245, 45, 26)}
  <svg class="sky__flight" viewBox="0 0 1440 700" preserveAspectRatio="xMidYMid slice">
    <path id="sky-arc" class="sky__trail" d="M-80 560 C 360 470, 820 220, 1540 120"/>
    <g class="sky__plane"><use href="#i-plane-fill" x="-16" y="-16" width="32" height="32" transform="rotate(90)"/>
      <animateMotion dur="16s" repeatCount="indefinite" rotate="auto"><mpath href="#sky-arc"/></animateMotion></g>
  </svg>
</div>'''

def crumbs_html(crumbs):
    return f'<a href="index.html">Home</a>' + "".join(
        f'{icon("chevron-right", "i i--xs")}' + (f'<a href="{u}">{t}</a>' if u else f'<span>{t}</span>') for t, u in crumbs)

def page_hero(media, eyebrow, title, text, crumbs, kind="video", alt=""):
    if kind == "video":
        stage = clip(media)
    elif kind == "sky":
        stage = sky_scene()
    else:
        stage = still(media, alt)
    return f'''
<section class="phero phero--{kind}" data-hero>
  <div class="hero__stage" data-stage>{stage}</div>
  <div class="hero__shade"></div>
  <div class="container phero__inner">
    <nav class="breadcrumb" aria-label="Breadcrumb">{crumbs_html(crumbs)}</nav>
    <span class="kicker kicker--light">{eyebrow}</span>
    <h1 class="phero__title">{title}</h1>
    <p class="phero__text">{text}</p>
  </div>
  <div class="edge" aria-hidden="true"></div>
</section>'''

# ----------------------------------------------------------------------------------
# Reusable blocks
# ----------------------------------------------------------------------------------
def stamp(id_, ring, center, cls=""):
    return f'''<span class="stamp {cls}" aria-hidden="true"><svg viewBox="0 0 120 120"><defs><path id="{id_}" d="M60 60m-43 0a43 43 0 1 1 86 0a43 43 0 1 1-86 0"/></defs>
<circle cx="60" cy="60" r="56"/><circle cx="60" cy="60" r="33"/><text><textPath href="#{id_}" textLength="266" lengthAdjust="spacing">{ring}</textPath></text></svg><b>{center}</b></span>'''

def pass_card(p):
    a, b = p["ends"]
    scope = "International" if p["type"] == "international" else "India"
    return f'''
<article class="pass" data-tilt data-reveal>
  <a href="{p["file"]}" class="pass__media" tabindex="-1" aria-hidden="true">{img(p["card_img"], p["card_alt"])}
    <span class="badge {p["badge_cls"]}">{p["badge"]}</span><span class="pass__scope">{icon("globe" if scope == "International" else "temple", "i i--sm")}{scope}</span></a>
  <div class="pass__body">
    <div class="pass__route">
      <div><small>From</small><b>{a}</b></div>
      <div class="pass__fly"><span></span>{icon("plane-fill", "i pass__plane")}<span></span><small>{p["via"]}</small></div>
      <div class="ta-r"><small>To</small><b>{b}</b></div>
    </div>
    <h3 class="pass__title"><a href="{p["file"]}">{p["short"]}</a></h3>
    <p class="pass__text">{p["summary"]}</p>
  </div>
  <div class="pass__stub">
    <dl class="pass__meta"><div><dt>Duration</dt><dd>{short_dur(p)}</dd></div><div><dt>Stops</dt><dd>{p["dest_n"]}</dd></div><div><dt>Fare</dt><dd>On request</dd></div></dl>
    <div class="pass__foot"><span class="barcode" aria-hidden="true"></span><a href="{p["file"]}" class="btn btn--ink btn--sm">View journey {icon("arrow-right", "i i--sm")}</a></div>
  </div>
  <i class="glare" aria-hidden="true"></i>
</article>'''

def pass_blank():
    return f'''
<article class="pass pass--blank" data-tilt data-reveal>
  <div class="pass__blank">
    {stamp("st-custom", "ANYWHERE &#10022; ANY DATE &#10022; YOUR WAY &#10022; ", icon("compass", "i"), "stamp--ink")}
    <span class="kicker">Something else in mind?</span>
    <h3>Write your own <em>route</em></h3>
    <p>India or abroad &mdash; tell us where you&rsquo;d like to go and we&rsquo;ll build the plan, flights included.</p>
  </div>
  <div class="pass__body">
    <div class="pass__route pass__route--blank">
      <div><small>From</small><b>Your city</b></div>
      <div class="pass__fly"><span></span>{icon("plane-fill", "i pass__plane")}<span></span></div>
      <div class="ta-r"><small>To</small><b>Anywhere</b></div>
    </div>
    <ul class="ticks ticks--sm"><li>{icon("check")} Share places, dates &amp; group size</li><li>{icon("check")} Get a day-by-day plan &amp; quote</li><li>{icon("check")} Add flights if you need them</li></ul>
  </div>
  <div class="pass__stub"><a href="contact.html?journey=custom" class="btn btn--sun btn--block">Start planning {icon("arrow-right", "i i--sm")}</a></div>
  <i class="glare" aria-hidden="true"></i>
</article>'''

def pbe_block(title="Plan. Book. <em>Explore.</em>", kicker="How it works"):
    steps = [("compass", "Plan", "Tell us where, when and who&rsquo;s travelling. We suggest the route, flights and stays, with a clear quote."),
             ("ticket", "Book", "Happy with the plan? We book your flights, hotels and transfers and send every confirmation."),
             ("mountain", "Explore", "Travel with your day-by-day itinerary and a number to call if anything changes on the way.")]
    st = "".join(f'<div class="pbe__step" data-reveal><span class="pbe__num">0{n}</span><div class="pbe__icon">{icon(i, "i i--lg")}</div><h3>{t}</h3><p>{d}</p></div>'
                 for n, (i, t, d) in enumerate(steps, 1))
    return f'''
<section class="section section--ink pbe">
  <div class="container">
    {head(kicker, title, "Three steps from first message to first sunrise.", center=True, light=True)}
    <div class="pbe__track">
      <svg class="pbe__path" viewBox="0 0 1200 150" aria-hidden="true">
        <path id="pbe-arc" d="M60 118 C 300 -10, 480 -10, 600 70 S 900 160, 1140 34"/>
        <g class="pbe__plane"><use href="#i-plane-fill" x="-15" y="-15" width="30" height="30" transform="rotate(90)"/>
          <animateMotion dur="10s" repeatCount="indefinite" rotate="auto"><mpath href="#pbe-arc"/></animateMotion></g>
      </svg>
      <div class="pbe__steps">{st}</div>
    </div>
  </div>
</section>'''

def cta_band(video="bay"):
    wa = (f'<a href="{WA_LINK}" target="_blank" rel="noopener" class="btn btn--ghost btn--lg">{icon("whatsapp", "i i--sm")} WhatsApp us</a>' if WA_ON else "")
    return f'''
<section class="vband vband--cta">
  {lazy_video(video)}
  <div class="vband__shade"></div>
  <div class="container vband__inner" data-reveal>
    {motto(light=True)}
    <h2 class="vband__title">Ready when <em>you</em> are.</h2>
    <p class="vband__text">Tell us your dates and who&rsquo;s travelling &mdash; we&rsquo;ll come back with flights, a day-by-day plan and a clear quote.</p>
    <div class="btns btns--center">
      <a href="contact.html" class="btn btn--sun btn--lg">{icon("send", "i i--sm")} Send an enquiry</a>
      <a href="tel:{SITE["phone_link"]}" class="btn btn--ghost btn--lg">{icon("phone", "i i--sm")} Call us</a>
      {wa}
    </div>
  </div>
</section>'''

def faq_list(items, open_first=True):
    out = []
    for n, (q, a) in enumerate(items):
        o = " is-open" if (n == 0 and open_first) else ""
        out.append(f'<div class="faq__item{o}" data-acc><button class="faq__q" data-acc-btn aria-expanded="false"><span>{q}</span><i class="faq__plus" aria-hidden="true"></i></button>'
                   f'<div class="faq__a" data-acc-body><p>{a}</p></div></div>')
    return f'<div class="faq">{"".join(out)}</div>'

def help_card(title="Still have questions?", text="Call or email us &mdash; we&rsquo;re happy to talk through dates, budgets and ideas."):
    wa = (f'<a href="{WA_LINK}" target="_blank" rel="noopener" class="btn btn--line btn--sm">{icon("whatsapp", "i i--sm")} WhatsApp</a>' if WA_ON else "")
    return f'''<div class="help-card"><span class="help-card__icon">{icon("phone", "i i--lg")}</span><h3>{title}</h3><p>{text}</p>
  <div class="btns"><a href="tel:{SITE["phone_link"]}" class="btn btn--ink btn--sm">{icon("phone", "i i--sm")} {SITE["phone_display"]}</a><a href="contact.html" class="btn btn--line btn--sm">{icon("mail", "i i--sm")} Enquire</a>{wa}</div></div>'''

def faq_section(items, kicker="Good to know", title="Frequently asked <em>questions</em>", lead="Quick answers about booking, flights and what&rsquo;s included. Can&rsquo;t find yours? Just ask.", sand=True):
    return f'''
<section class="section{" section--sand" if sand else ""}">
  <div class="container faq-layout">
    <div>{head(kicker, title, lead)}<div data-reveal>{help_card()}</div></div>
    <div data-reveal>{faq_list(items)}</div>
  </div>
</section>'''

# ---------- Forms ----------
def flight_fields(sfx, required=False):
    req = " required" if required else ""
    return f'''
    <div class="form-row">
      <div class="field"><label for="f-from-{sfx}">Flying from{" *" if required else ""}</label><input id="f-from-{sfx}" name="from" list="airports" placeholder="City or airport" autocomplete="off"{req}></div>
      <div class="field"><label for="f-to-{sfx}">Flying to{" *" if required else ""}</label><input id="f-to-{sfx}" name="to" list="airports" placeholder="City or airport" autocomplete="off"{req}></div>
    </div>
    <div class="form-row">
      <div class="field"><label for="f-trip-{sfx}">Trip type</label><select id="f-trip-{sfx}" name="trip" data-trip><option value="return">Round trip</option><option value="oneway">One way</option><option value="multicity">Multi-city</option></select></div>
      <div class="field"><label for="f-cabin-{sfx}">Cabin class</label>{cabin_select("f-cabin-" + sfx)}</div>
    </div>
    <div class="form-row">
      <div class="field"><label for="f-depart-{sfx}">Departure date{" *" if required else ""}</label><input id="f-depart-{sfx}" name="depart" type="date" data-depart{req}></div>
      <div class="field" data-return-field><label for="f-return-{sfx}">Return date</label><input id="f-return-{sfx}" name="return" type="date" data-returndate></div>
    </div>'''

def enquiry_form(mode="contact", journey_value="", page_name="contact"):
    """mode: contact (service switch: package / flight / both), flight (flight only), compact (package page sidebar)."""
    opts = [(x["slug"], f'{x["short"]} ({short_dur(x)})') for x in PACKAGES] + [("custom", "Custom trip / not sure yet")]
    jsel = '<option value="">Choose a holiday</option>' + "".join(f'<option value="{v}"{" selected" if v == journey_value else ""}>{t}</option>' for v, t in opts)
    styles = "".join(f'<option value="{v}">{t}</option>' for v, t in [("", "Any style"), ("heritage", "Heritage &amp; culture"), ("beach", "Beach &amp; islands"), ("wildlife", "Wildlife"), ("honeymoon", "Honeymoon"), ("family", "Family"), ("group", "Group tour")])
    s = page_name
    contact_rows = f'''
    <div class="form-row">
      <div class="field"><label for="f-name-{s}">Full name *</label><input id="f-name-{s}" name="name" required autocomplete="name"></div>
      <div class="field"><label for="f-email-{s}">Email *</label><input id="f-email-{s}" name="email" type="email" required autocomplete="email"></div>
    </div>
    <div class="form-row">
      <div class="field"><label for="f-phone-{s}">Phone *</label><input id="f-phone-{s}" name="phone" type="tel" required autocomplete="tel"></div>
      <div class="field"><label for="f-pax-{s}">Travellers</label>{pax_select("f-pax-" + s)}</div>
    </div>'''
    msg = f'<div class="field"><label for="f-msg-{s}">Tell us more</label><textarea id="f-msg-{s}" name="message" placeholder="Places you&rsquo;d like to see, flexible dates, hotel preference, special occasions..."></textarea></div>'
    if mode == "compact":
        fields = f'''
    <div class="field"><label for="f-name-{s}">Full name *</label><input id="f-name-{s}" name="name" required autocomplete="name"></div>
    <div class="field"><label for="f-phone-{s}">Phone *</label><input id="f-phone-{s}" name="phone" type="tel" required autocomplete="tel"></div>
    <div class="field"><label for="f-email-{s}">Email *</label><input id="f-email-{s}" name="email" type="email" required autocomplete="email"></div>
    <div class="form-row">
      <div class="field"><label for="f-month-{s}">Travel month</label>{month_select("f-month-" + s)}</div>
      <div class="field"><label for="f-pax-{s}">Travellers</label>{pax_select("f-pax-" + s)}</div>
    </div>
    <label class="check"><input type="checkbox" name="service" value="both"><span>Add flight tickets to my quote</span></label>
    <input type="hidden" name="journey" value="{journey_value}">'''
        submit = "Get my free quote"
    elif mode == "flight":
        fields = f'''<input type="hidden" name="service" value="flight">
    {flight_fields(s, required=True)}
    {contact_rows}
    {msg}'''
        submit = "Get fare options"
    else:
        seg = "".join(f'<label><input type="radio" name="service" value="{v}"{" checked" if v == "package" else ""} data-service><span>{icon(i, "i i--sm")} {t}</span></label>'
                      for v, i, t in [("package", "mountain", "Holiday package"), ("flight", "ticket", "Flight tickets"), ("both", "plane", "Flight + holiday")])
        fields = f'''
    <fieldset class="seg-field"><legend>What can we help with?</legend><div class="seg seg--block">{seg}</div></fieldset>
    {contact_rows}
    <div class="form-group" data-for="package both">
      <div class="form-row">
        <div class="field"><label for="f-journey-{s}">Holiday</label><select id="f-journey-{s}" name="journey">{jsel}</select></div>
        <div class="field"><label for="f-month-{s}">Travel month</label>{month_select("f-month-" + s)}</div>
      </div>
      <div class="field"><label for="f-style-{s}">Trip style</label><select id="f-style-{s}" name="style">{styles}</select></div>
    </div>
    <div class="form-group" data-for="flight both" hidden>{flight_fields(s)}</div>
    {msg}'''
        submit = "Send my enquiry"
    wa = (f'<div class="or">or</div><button type="button" class="btn btn--line btn--block" data-wa-form>{icon("whatsapp", "i i--sm")} Send on WhatsApp</button>' if WA_ON else "")
    return f'''
<form class="form" action="{SITE["form_endpoint"]}" method="post" data-enquiry>
  <div class="alert alert--error" role="alert">Sorry, your enquiry could not be sent. Please check the required fields, or call us on {SITE["phone_display"]}.</div>
  {fields}
  <div class="hp" aria-hidden="true"><label>Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label></div>
  <input type="hidden" name="page" value="{page_name}">
  <button type="submit" class="btn btn--sun btn--block btn--lg">{icon("send", "i i--sm")} {submit}</button>
  {wa}
  <p class="form-note">We reply with options and a clear quote. Your details are only used to answer your enquiry.</p>
</form>'''

# ----------------------------------------------------------------------------------
# Pages
# ----------------------------------------------------------------------------------
def booker():
    pkg_opts = "".join(f'<option value="{x["slug"]}" data-type="{x["type"]}" data-page="{x["file"]}">{x["short"]} &middot; {short_dur(x)}</option>' for x in PACKAGES)
    return f'''
<div class="booker" id="book">
  <div class="booker__tabs" role="tablist" aria-label="What would you like to book?">
    <button type="button" role="tab" class="booker__tab is-active" aria-selected="true" data-book-tab="flight">{icon("ticket", "i i--xl")}<span>Flight<br>Tickets</span></button>
    <span class="booker__or" aria-hidden="true">or</span>
    <button type="button" role="tab" class="booker__tab" aria-selected="false" data-book-tab="package">{icon("mountain", "i i--xl")}<span>Travel<br>Packages</span></button>
  </div>
  <form class="booker__panel is-active" data-book-panel="flight" action="flights.html" method="get">
    <div class="seg seg--sm" role="radiogroup" aria-label="Trip type">
      <label><input type="radio" name="trip" value="return" checked data-trip><span>Round trip</span></label>
      <label><input type="radio" name="trip" value="oneway" data-trip><span>One way</span></label>
      <label><input type="radio" name="trip" value="multicity" data-trip><span>Multi-city</span></label>
    </div>
    <div class="bf-route">
      <label class="bf"><span>From</span><input name="from" list="airports" placeholder="Delhi (DEL)" autocomplete="off"></label>
      <button type="button" class="bf-swap" data-swap aria-label="Swap from and to">{icon("swap", "i i--sm")}</button>
      <label class="bf"><span>To</span><input name="to" list="airports" placeholder="Where to?" autocomplete="off"></label>
    </div>
    <div class="bf-row">
      <label class="bf"><span>Depart</span><input type="date" name="depart" data-depart></label>
      <label class="bf" data-return-field><span>Return</span><input type="date" name="return" data-returndate></label>
    </div>
    <div class="bf-row">
      <label class="bf"><span>Travellers</span>{pax_select("bk-pax")}</label>
      <label class="bf"><span>Cabin</span>{cabin_select("bk-cabin")}</label>
    </div>
    <button type="submit" class="btn btn--sun btn--block">{icon("search", "i i--sm")} Get fare options</button>
  </form>
  <form class="booker__panel" data-book-panel="package" action="journeys.html" method="get" data-pkg-finder>
    <div class="seg seg--sm" role="radiogroup" aria-label="Where would you like to go?">
      <label><input type="radio" name="type" value="" checked data-scope><span>Anywhere</span></label>
      <label><input type="radio" name="type" value="india" data-scope><span>India</span></label>
      <label><input type="radio" name="type" value="international" data-scope><span>International</span></label>
    </div>
    <label class="bf"><span>Holiday</span><select name="journey" data-pkg-select><option value="">Show me all holidays</option>{pkg_opts}<option value="custom">Plan a custom trip</option></select></label>
    <div class="bf-row">
      <label class="bf"><span>Month</span>{month_select("bk-month")}</label>
      <label class="bf"><span>Travellers</span>{pax_select("bk-pax2")}</label>
    </div>
    <button type="submit" class="btn btn--sun btn--block">{icon("search", "i i--sm")} Find my holiday</button>
  </form>
</div>'''

def build_home():
    clips = "".join(clip(k, active=(n == 0), first=(n == 0)) for n, (k, *_r) in enumerate(HERO_CHAPTERS))
    chapters = "".join(
        f'<button type="button" class="chapter{" is-active" if n == 0 else ""}" data-chapter="{n}" aria-label="Show scene {n + 1}: {lbl}">'
        f'<span class="chapter__bar"><i></i></span><span class="chapter__scope">{scope}</span><strong>{lbl}</strong><small>{line}</small></button>'
        for n, (k, lbl, scope, line) in enumerate(HERO_CHAPTERS))
    tick_items = ["Flight tickets", "India holidays", "International holidays", "Honeymoons", "Family trips", "Group tours", "Custom itineraries", "Day-by-day plans"]
    ticks = "".join(f"<span>{t}</span><i>&#10022;</i>" for t in tick_items)
    india_n = sum(x["dest_n"] for x in PACKAGES if x["type"] == "india")
    intl_n = sum(x["dest_n"] for x in PACKAGES if x["type"] == "international")
    flow = "".join(f'''<a class="flow__item" href="{PKG[k]["file"]}" data-flow-item draggable="false">{img(f, f"{n}, {c}", extra=' draggable="false"')}<span class="flow__shade"></span><div class="flow__info"><span class="flow__country">{icon("pin", "i i--xs")}{c}</span><h4>{n}</h4><span>{s}</span></div></a>'''
                   for f, n, c, s, k in DESTINATIONS)
    r = PKG["rajasthan"]
    chips = "".join(f"<span>{s}</span>" for s in r["route"][:-1])
    moments = [("gal-hawa-mahal", "Hawa Mahal, Jaipur"), ("gal-koh-larn-beach", "Koh Larn beach"), ("gal-tiger", "Tiger, Ranthambore"),
               ("gal-grand-palace", "Grand Palace, Bangkok"), ("gal-jodhpur-blue", "Blue City, Jodhpur"), ("gal-street-food", "Thai street food")]
    mom = "".join(f'<a href="#" data-lightbox="assets/img/{f}.webp" data-caption="{c}">{img(f, c, sizes="(max-width: 860px) 100vw, 50vw" if n == 0 else None)}<span>{c}</span></a>' for n, (f, c) in enumerate(moments))
    body = f'''
<section class="hero" data-hero data-hero-seq aria-label="Travel Dervish: flight tickets and holiday packages">
  <div class="hero__stage" data-stage>{clips}</div>
  <div class="hero__shade"></div>
  <div class="container hero__inner">
    <div class="hero__content" data-depth style="--d:-10">
      {motto(light=True)}
      <h1 class="hero__title"><span class="ln"><span>Your travel partner</span></span> <span class="ln"><span>for <em>every</em> journey</span></span></h1>
      <p class="hero__text">Flight tickets and holiday packages across India and around the world &mdash; planned, booked and looked after by one team.</p>
      <div class="hero__actions">
        <a href="journeys.html" class="btn btn--sun btn--lg">Explore holidays {icon("arrow-right", "i i--sm")}</a>
        <a href="flights.html" class="btn btn--ghost btn--lg">{icon("plane", "i i--sm")} Book flights</a>
      </div>
    </div>
    {booker()}
  </div>
  <div class="container hero__bottom">
    <div class="chapters" aria-label="Banner scenes">{chapters}</div>
    <button type="button" class="hero__pause" data-hero-pause aria-label="Pause banner video" aria-pressed="false">{icon("pause", "i i--sm")}{icon("play", "i i--sm")}</button>
  </div>
</section>

<div class="ticker" aria-hidden="true"><div class="ticker__track">{ticks}{ticks}</div></div>

<section class="section services" id="services">
  <div class="container">
    {head("What we do", "Flight tickets <em>or</em> travel packages", "Book just the flight, or let us plan the whole holiday. Either way, one team looks after you from the first message.", center=True)}
    <div class="duo">
      <article class="duo__card duo__card--sky" data-tilt data-reveal>
        <div class="duo__top"><span class="duo__icon">{icon("ticket", "i i--xl")}</span><span class="duo__num">01</span></div>
        <h3>Flight Tickets</h3>
        <p>Domestic and international flights. Send us your route and dates and we&rsquo;ll come back with fare options to choose from.</p>
        <ul class="ticks"><li>{icon("check")} Domestic &amp; international routes</li><li>{icon("check")} One way, round trip &amp; multi-city</li><li>{icon("check")} Fare options before you book</li></ul>
        <a href="flights.html" class="btn btn--ink">Request a fare {icon("arrow-right", "i i--sm")}</a>
        <svg class="duo__arc" viewBox="0 0 400 140" aria-hidden="true"><path d="M10 130 C 120 20, 260 10, 390 60"/></svg>
        <i class="glare" aria-hidden="true"></i>
      </article>
      <div class="duo__or" aria-hidden="true"><span>or</span></div>
      <article class="duo__card duo__card--photo" data-tilt data-reveal>
        {img("brand-sunrise", "Backpack, hat, camera and map on a mountain top at sunrise", "duo__bg")}
        <div class="duo__top"><span class="duo__icon">{icon("mountain", "i i--xl")}</span><span class="duo__num">02</span></div>
        <h3>Travel Packages</h3>
        <p>Day-by-day holidays across India and abroad, with stays, transfers and sightseeing planned around your dates.</p>
        <ul class="ticks"><li>{icon("check")} India &amp; international itineraries</li><li>{icon("check")} Hotels, transfers &amp; local experiences</li><li>{icon("check")} Tailored to your group &amp; pace</li></ul>
        <a href="journeys.html" class="btn btn--sun">Explore packages {icon("arrow-right", "i i--sm")}</a>
        <i class="glare" aria-hidden="true"></i>
      </article>
    </div>
  </div>
</section>

<section class="section section--sand">
  <div class="container">
    {head("Choose your world", "Holidays at <em>home</em> &amp; <em>abroad</em>", "Heritage trails and lake cities in India, beaches and big cities overseas &mdash; with more destinations on the way.", center=True)}
    <div class="worlds">
      <a class="world" href="journeys.html?type=india" data-tilt data-hover-video data-reveal>
        {img("region-india", "Hawa Mahal facade, Jaipur")}
        <video muted loop playsinline preload="none" {video_attrs("lake")} aria-hidden="true"></video>
        {stamp("st-india", "DOMESTIC &#10022; TRAVEL DERVISH &#10022; INDIA &#10022; ", "IN")}
        <div class="world__body"><span class="world__count">{icon("temple", "i i--sm")} {india_n} destinations</span><h3>India</h3><p>Heritage, desert, lakes &amp; wildlife</p></div>
        <span class="world__go">{icon("arrow-up-right")}</span>
        <i class="glare" aria-hidden="true"></i>
      </a>
      <a class="world" href="journeys.html?type=international" data-tilt data-hover-video data-reveal>
        {img("region-international", "Longtail boat on turquoise water")}
        <video muted loop playsinline preload="none" {video_attrs("bay")} aria-hidden="true"></video>
        {stamp("st-world", "INTERNATIONAL &#10022; TRAVEL DERVISH &#10022; WORLD &#10022; ", icon("globe", "i"))}
        <div class="world__body"><span class="world__count">{icon("globe", "i i--sm")} {intl_n} destinations</span><h3>International</h3><p>Beaches, temples &amp; city life</p></div>
        <span class="world__go">{icon("arrow-up-right")}</span>
        <i class="glare" aria-hidden="true"></i>
      </a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="head-split">{head("Featured holidays", "Hand-planned <em>journeys</em>")}<a href="journeys.html" class="link-arrow" data-reveal>View all holidays {icon("arrow-right")}</a></div>
    <div class="passes">{"".join(pass_card(x) for x in PACKAGES[:5])}{pass_blank()}</div>
  </div>
</section>

{pbe_block()}

<section class="section section--sand flow-section">
  <div class="container">
    <div class="head-split">{head("On our itineraries", "Places we&rsquo;ll <em>take you</em>")}
      <div class="round-nav" data-reveal><button class="round-btn" data-flow-prev aria-label="Previous destination">{icon("arrow-left")}</button><button class="round-btn round-btn--fill" data-flow-next aria-label="Next destination">{icon("arrow-right")}</button></div></div>
  </div>
  <div class="flow" data-flow tabindex="0" aria-roledescription="carousel" aria-label="Destinations. Drag, swipe or use the arrow keys to browse."><div class="flow__stage">{flow}</div></div>
</section>

<section class="section spotlight">
  <div class="container spotlight__grid">
    <div class="spotlight__media" data-reveal>
      <div class="vframe" data-tilt>{lazy_video("lake", "vframe__video")}<i class="glare" aria-hidden="true"></i></div>
      <div class="spot-badge"><strong>16</strong><span>days</span></div>
      {stamp("st-raj", "SIGNATURE JOURNEY &#10022; RAJASTHAN &#10022; ", icon("sun", "i"), "stamp--sun spotlight__stamp")}
    </div>
    <div data-reveal>
      <span class="kicker">Signature journey</span>
      <h2 class="title">Rajasthan: forts, deserts &amp; <em>tigers</em></h2>
      <p class="lead">{r["overview"]}</p>
      <div class="route-chips">{chips}</div>
      <ul class="ticks">
        <li>{icon("check")} Sunset camel safari option at Sam Sand Dunes</li>
        <li>{icon("check")} Boat ride on Lake Pichola to Jag Mandir</li>
        <li>{icon("check")} Jaipur food walk and cycle-rickshaw ride</li>
        <li>{icon("check")} Jungle safari in Ranthambore and Taj Mahal at sunrise</li>
      </ul>
      <div class="btns">
        <a href="{r["file"]}" class="btn btn--sun">View itinerary {icon("arrow-right", "i i--sm")}</a>
        <a href="{r["pdf"]}" class="btn btn--ghost" download>{icon("download", "i i--sm")} Download PDF</a>
      </div>
    </div>
  </div>
</section>

<section class="vband">
  {lazy_video("desert")}
  <div class="vband__shade"></div>
  <div class="container vband__inner" data-reveal>
    {motto(light=True)}
    <p class="vband__quote">&ldquo;Your travel partner for <em>every</em> journey.&rdquo;</p>
    <div class="stats">
      <div class="stat"><strong data-count="13">13</strong><span>Destinations on our itineraries</span></div>
      <div class="stat"><strong data-count="21">21</strong><span>Days of ready-made plans</span></div>
      <div class="stat"><strong data-count="2">2</strong><span>Ways to travel: flights &amp; packages</span></div>
      <div class="stat"><strong>{icon("globe", "i")}</strong><span>India &amp; international</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    {head("Moments from the road", "A glimpse of <em>what awaits</em>", center=True)}
    <div class="moments" data-reveal>{mom}</div>
  </div>
</section>

{faq_section(FAQS)}

{cta_band("bay")}'''
    ld = {"@context": "https://schema.org", "@type": "TravelAgency", "name": "Travel Dervish", "url": SITE["url"], "slogan": SITE["tagline"],
          "email": SITE["email"], "telephone": SITE["phone_link"], "logo": SITE["url"] + "/assets/img/logo-dark.svg",
          "address": {"@type": "PostalAddress", "addressLocality": "Delhi", "addressCountry": "IN"},
          "parentOrganization": {"@type": "Organization", "name": "Design Dervish", "url": SITE["parent"]}}
    page("index.html", "Travel Dervish | Flight Tickets & Holiday Packages in India and Abroad",
         "Travel Dervish, your travel partner for every journey: domestic and international flight tickets and day-by-day holiday packages across India and abroad.",
         body, "home", jsonld=ld, lightbox=True, datalist=True)

def lpass(p):
    route = "".join(f"<span>{s}</span>" for s in p["route"])
    cats = "".join(f'<li>{icon("sparkle")}{c}</li>' for c in p["categories"][:3])
    return f'''
<article class="lpass" data-type="{p["type"]}" data-styles="{p["styles"]}" data-reveal>
  <a href="{p["file"]}" class="lpass__media" tabindex="-1" aria-hidden="true">{img(p["card_img"], p["card_alt"], sizes="(max-width: 760px) 92vw, 380px")}<span class="badge {p["badge_cls"]}">{p["badge"]}</span></a>
  <div class="lpass__body">
    <div class="lpass__region">{icon("globe" if p["type"] == "international" else "temple", "i i--sm")}{p["region"]}</div>
    <h3><a href="{p["file"]}">{p["title"].replace("&", "&amp;")}</a></h3>
    <div class="lpass__route">{route}</div>
    <p>{p["summary"]}</p>
    <ul class="lpass__cats">{cats}</ul>
  </div>
  <div class="lpass__stub">
    <dl class="pass__meta pass__meta--col"><div><dt>Duration</dt><dd>{p["duration"]}</dd></div><div><dt>Destinations</dt><dd>{p["dest_n"]} stops</dd></div><div><dt>Fare</dt><dd>On request</dd></div></dl>
    <span class="barcode" aria-hidden="true"></span>
    <div class="btns btns--col">
      <a href="{p["file"]}" class="btn btn--ink btn--sm btn--block">View itinerary {icon("arrow-right", "i i--sm")}</a>
      <a href="{p["pdf"]}" class="btn btn--line btn--sm btn--block" download>{icon("download", "i i--sm")} PDF</a>
    </div>
  </div>
</article>'''

def build_journeys():
    chips = [("all", "compass", "All styles"), ("heritage", "temple", "Heritage"), ("desert", "dune", "Desert"),
             ("wildlife", "paw", "Wildlife"), ("beach", "wave", "Beach"), ("city", "city", "City life")]
    ch = "".join(f'<button class="chip{" is-active" if k == "all" else ""}" data-style="{k}">{icon(i)}{t}</button>' for k, i, t in chips)
    body = f'''
{page_hero("lake", "Find your journey", "Holidays at home <em>&amp;</em> abroad", "India journeys and international escapes, each with a day-by-day itinerary you can download.", [("Holidays", "")])}
<section class="section">
  <div class="container">
    <div class="filters" data-reveal>
      <div class="tabs" role="tablist">
        <button class="tab is-active" data-type="all">All holidays</button>
        <button class="tab" data-type="india">{icon("temple", "i i--sm")} India</button>
        <button class="tab" data-type="international">{icon("globe", "i i--sm")} International</button>
      </div>
      <div class="chips">{ch}</div>
    </div>
    <p class="count-line">Showing <strong data-count-label>{len(PACKAGES)} holidays</strong></p>
    <div class="listing" data-listing>{"".join(lpass(x) for x in PACKAGES)}</div>
    <div class="suggest" data-reveal>
      {stamp("st-suggest", "MORE JOURNEYS ON THE WAY &#10022; ", icon("compass", "i"), "stamp--ink")}
      <div><span class="kicker">More journeys on the way</span>
      <h3>Don&rsquo;t see your destination yet?</h3>
      <p>We&rsquo;re adding new India and international holidays. Tell us where you&rsquo;d like to go and we&rsquo;ll plan it, flights included.</p></div>
      <a href="contact.html?journey=custom" class="btn btn--sun">{icon("send", "i i--sm")} Suggest a destination</a>
    </div>
  </div>
</section>
{pbe_block()}
{cta_band("desert")}'''
    page("journeys.html", "Holidays | India & International Holiday Packages | Travel Dervish",
         "Browse Travel Dervish holidays: the 16-day Rajasthan heritage, culture and wildlife tour and the 5-day Thailand holiday. Filter by India or international and travel style.",
         body, "journeys", og="poster-lake")

def build_package(p):
    others = [x for x in PACKAGES if x is not p][:2]
    g = p["gallery"]
    gal = ""
    for n, (f, c) in enumerate(g[:5]):
        cls = "g-main" if n == 0 else ("g-hide-sm" if n >= 3 else "")
        gal += f'<button class="{cls}" data-lightbox="assets/img/{f}.webp" data-caption="{c}" aria-label="Open photo: {c}">{img(f, c, sizes="(max-width: 760px) 100vw, 50vw" if n == 0 else None)}</button>'
    extra = "".join(f'<span hidden data-lightbox="assets/img/{f}.webp" data-caption="{c}"></span>' for f, c in g[5:])
    chips = "".join(f"<span>{c}</span>" for c in p["categories"])
    facts = "".join(f'<div class="fact"><div class="fact__icon">{icon(i)}</div><div><small>{k}</small><strong>{v}</strong></div></div>' for i, k, v in p["facts"])
    hl = "".join(f"<li>{icon('check')}<span>{h}</span></li>" for h in p["highlights"])
    route = "".join(f"<li><i></i><span>{s}</span><small>{d}</small></li>" for s, d in zip(p["route"], p["route_days"]))
    days = ""
    for n, (title, km, hrs, paras, stay, im) in enumerate(p["days"], 1):
        meta = ""
        if km: meta += f'<span>{icon("route")}{km}</span>'
        if hrs: meta += f'<span>{icon("clock")}{hrs}</span>'
        meta += f'<span>{icon("bed")}{stay}</span>'
        body_html = "".join(f"<p>{x}</p>" for x in paras)
        if im: body_html += img(im[0], im[1], sizes="(max-width: 1024px) 92vw, 700px")
        days += f'''
<div class="day{" is-open" if n == 1 else ""}" data-acc>
  <button class="day__head" data-acc-btn aria-expanded="false">
    <span class="day__num"><small>Day</small><strong>{n:02d}</strong></span>
    <span><span class="day__title">{title}</span><span class="day__meta">{meta}</span></span>
    <i class="faq__plus" aria-hidden="true"></i>
  </button>
  <div class="day__body" data-acc-body><div class="day__inner">{body_html}<span class="day__stay">{icon("bed", "i i--sm")} Overnight: {stay}</span></div></div>
</div>'''
    table = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in p["table"])
    notes = "".join(f"<li>{icon('info')}<span>{x}</span></li>" for x in p["notes"])
    stage = clip(p["video"]) if p.get("video") else still(p["card_img"], p["card_alt"])
    body = f'''
<section class="phero phero--pkg" data-hero>
  <div class="hero__stage" data-stage>{stage}</div>
  <div class="hero__shade"></div>
  <div class="container phero__inner">
    <nav class="breadcrumb" aria-label="Breadcrumb">{crumbs_html([(p["region"], "journeys.html?type=" + p["type"]), (p["short"], "")])}</nav>
    <div class="chips chips--light"><span class="badge {p["badge_cls"]}">{p["badge"]}</span>{chips}</div>
    <h1 class="phero__title">{p["title"].replace("&", "&amp;")}</h1>
    <p class="phero__text">{icon("pin", "i i--sm")} {p["location"].replace("&", "&amp;")} &nbsp;&middot;&nbsp; {p["duration"]}</p>
    <div class="btns">
      <a href="#enquire" class="btn btn--sun btn--lg">{icon("send", "i i--sm")} Enquire now</a>
      <a href="{p["pdf"]}" class="btn btn--ghost btn--lg" download>{icon("download", "i i--sm")} Download PDF</a>
    </div>
  </div>
  <div class="edge" aria-hidden="true"></div>
</section>

<div class="container pkg-top">
  <div class="facts" data-reveal>{facts}</div>
  <div class="pkg-gallery">{gal}<button class="pkg-gallery__all" data-lb-open>{icon("grid", "i i--sm")} View all {len(g)} photos</button></div>
  {extra}
</div>

<div class="container pkg-layout">
  <div>
    <nav class="pkg-tabs" aria-label="Sections">
      <a href="#overview" class="is-active">Overview</a><a href="#highlights">Highlights</a><a href="#route">Route</a>
      <a href="#itinerary">Itinerary</a><a href="#details">Details</a><a href="#notes">Good to know</a>
    </nav>
    <section class="pkg-section" id="overview"><h2>{icon("compass")} Overview</h2><p>{p["overview"]}</p></section>
    <section class="pkg-section" id="highlights"><h2>{icon("sparkle")} Tour highlights</h2><ul class="highlights">{hl}</ul></section>
    <section class="pkg-section" id="route"><h2>{icon("map")} The route</h2><ol class="route">{route}</ol></section>
    <section class="pkg-section" id="itinerary">
      <h2>{icon("route")}<span class="grow">Day-by-day itinerary</span><button class="btn btn--line btn--sm" data-acc-all="days">Expand all days</button></h2>
      <div class="itinerary" id="days">{days}</div>
    </section>
    <section class="pkg-section" id="details"><h2>{icon("info")} Package details</h2><dl class="overview-table">{table}</dl></section>
    <section class="pkg-section" id="notes"><h2>{icon("shield")} Good to know</h2><ul class="notes">{notes}</ul></section>
  </div>
  <aside class="aside" id="enquire">
    <div class="aside-card">
      <div class="aside-card__head"><span class="kicker kicker--light">{p["duration"]}</span><strong>Price on request</strong><span>Tailored quote for your dates &amp; group</span></div>
      <div class="aside-card__body">{enquiry_form("compact", p["slug"], p["slug"])}</div>
    </div>
    <div class="aside-mini"><div class="fact__icon">{icon("download")}</div><div><strong>Full itinerary (PDF)</strong><a href="{p["pdf"]}" download>Download the day-by-day plan</a></div></div>
    <div class="aside-mini"><div class="fact__icon">{icon("ticket")}</div><div><strong>Need flights too?</strong><a href="flights.html">Request a fare quote</a></div></div>
  </aside>
</div>

<section class="section section--sand">
  <div class="container">
    <div class="head-split">{head("You may also like", "More <em>journeys</em>")}<a href="journeys.html" class="link-arrow" data-reveal>View all holidays {icon("arrow-right")}</a></div>
    <div class="passes">{"".join(pass_card(x) for x in others)}{pass_blank()}</div>
  </div>
</section>'''
    ld = {"@context": "https://schema.org", "@type": "TouristTrip", "name": p["title"], "description": html.unescape(p["meta"]),
          "touristType": p["categories"], "provider": {"@type": "TravelAgency", "name": "Travel Dervish", "url": SITE["url"]},
          "itinerary": {"@type": "ItemList", "itemListElement": [
              {"@type": "ListItem", "position": n, "name": f"Day {n}: " + html.unescape(d[0])} for n, d in enumerate(p["days"], 1)]}}
    page(p["file"], f'{html.unescape(p["title"])} | {p["duration"]} | Travel Dervish', p["meta"], body, p["type"],
         og=p["card_img"], jsonld=ld, lightbox=True)

def build_flights():
    why = [("globe", "Domestic &amp; international", "Flights within India and to destinations abroad, one way, round trip or multi-city."),
           ("ticket", "Fare options first", "We send the options and fares we find, so you can choose before anything is booked."),
           ("luggage", "Flights + holiday", "Pair your tickets with a holiday package and we&rsquo;ll plan the dates around each other."),
           ("phone", "A person to call", f"Questions about your booking? Call us on {SITE['phone_display']}.")]
    w = "".join(f'<div class="why" data-reveal><span class="why__icon">{icon(i, "i i--lg")}</span><div><h3>{t}</h3><p>{d}</p></div></div>' for i, t, d in why)
    body = f'''
{page_hero("", "Domestic &amp; international", "Flight tickets, <em>sorted</em>", "Tell us where and when you&rsquo;re flying. We&rsquo;ll come back with fare options for your route &mdash; and a holiday plan too, if you want one.", [("Flights", "")], kind="sky")}
<section class="section flights">
  <div class="container flights__grid">
    <div class="panel panel--ticket" id="request" data-reveal>
      <div class="panel__head"><span class="panel__icon">{icon("ticket", "i i--lg")}</span><div><span class="kicker">Fare request</span><h2>Where are you flying?</h2></div></div>
      {enquiry_form("flight", page_name="flights")}
    </div>
    <div class="flights__side">
      {head("Why book with us", "One team for <em>every</em> ticket")}
      <div class="whys">{w}</div>
      <div class="mini-pass" data-reveal>
        <div><small>Prefer to talk?</small><strong>Call us</strong><a href="tel:{SITE["phone_link"]}">{SITE["phone_display"]}</a></div>
        <span class="barcode" aria-hidden="true"></span>
      </div>
    </div>
  </div>
</section>
<section class="section section--sand">
  <div class="container">
    <div class="head-split">{head("Make it a holiday", "Add a <em>day-by-day</em> plan")}<a href="journeys.html" class="link-arrow" data-reveal>View all holidays {icon("arrow-right")}</a></div>
    <div class="passes">{"".join(pass_card(x) for x in PACKAGES[:2])}{pass_blank()}</div>
  </div>
</section>
{faq_section(FLIGHT_FAQS, "Flight questions", "Before you <em>fly</em>", "The essentials about fare requests and bookings.", sand=False)}
{cta_band("bay")}'''
    page("flights.html", "Flight Tickets | Domestic & International Flights | Travel Dervish",
         "Request domestic and international flight tickets from Travel Dervish: one way, round trip or multi-city, with fare options before you book.",
         body, "flights", overlay=False, og="brand-sunrise", datalist=True)

def build_about():
    values = [("heart", "Thoughtfully paced", "Routes with realistic drive times and room to actually enjoy each place."),
              ("shield", "Clear &amp; upfront", "Inclusions, optional extras and seasonal notes are spelled out before you book."),
              ("food", "Local at heart", "Markets, food walks, temple visits and lake rides &mdash; not just monuments."),
              ("ticket", "Flights included", "Book only the ticket, or let us fit flights and holiday together.")]
    val = "".join(f'<div class="value" data-tilt data-reveal><span class="why__icon">{icon(i, "i i--lg")}</span><h3>{t}</h3><p>{d}</p><i class="glare" aria-hidden="true"></i></div>' for i, t, d in values)
    body = f'''
{page_hero("hero-about", "Our story", "About <em>Travel Dervish</em>", "Your travel partner for every journey &mdash; a travel venture of Design Dervish, Delhi.", [("About", "")], kind="still", alt="Blue-washed lanes of Jodhpur")}
<section class="section">
  <div class="container split">
    <div class="collage" data-reveal>
      {img("brand-sunrise", "Backpack, hat and camera on a mountain top at sunrise", "c1")}
      {img("about-tuktuk", "Tuk-tuks on a Bangkok street at night", "c2")}
      {stamp("st-about", "PLAN &#10022; BOOK &#10022; EXPLORE &#10022; ", icon("compass", "i"), "stamp--sun collage__stamp")}
    </div>
    <div data-reveal>
      <span class="kicker">Who we are</span>
      <h2 class="title">Journeys designed with <em>intent</em></h2>
      <p class="lead">Travel Dervish is the travel venture of Design Dervish, a design and branding studio in Delhi. We bring the same eye for detail to travel: sensible routes, clear day-by-day plans and the experiences that make a place memorable.</p>
      <p class="lead">We book flight tickets and plan holiday packages across India and abroad &mdash; starting with a 16-day Rajasthan journey and a 5-day Thailand holiday, with more on the way.</p>
      <ul class="ticks">
        <li>{icon("check")} Domestic &amp; international flight tickets</li>
        <li>{icon("check")} India journeys and international escapes</li>
        <li>{icon("check")} Day-wise itineraries with drive times</li>
        <li>{icon("check")} Quotes tailored to your dates and group</li>
      </ul>
      <div class="btns"><a href="journeys.html" class="btn btn--ink">Explore holidays {icon("arrow-right", "i i--sm")}</a><a href="contact.html" class="btn btn--line">Talk to us</a></div>
    </div>
  </div>
</section>
<section class="section section--sand">
  <div class="container">
    {head("What we believe", "How we <em>plan journeys</em>", center=True)}
    <div class="values">{val}</div>
  </div>
</section>
{pbe_block("From first message to <em>first sunrise</em>", "Working with us")}
{cta_band("lake")}'''
    page("about.html", "About Us | Travel Dervish, a Design Dervish venture",
         "Travel Dervish is the travel venture of Design Dervish, Delhi: flight tickets and day-by-day holidays across India and abroad.",
         body, "about", og="hero-about")

def build_contact():
    wa_card = (f'<a class="info-card" href="{WA_LINK}" target="_blank" rel="noopener"><span class="why__icon">{icon("whatsapp", "i i--lg")}</span><div><small>Fastest reply</small><strong>Chat on WhatsApp</strong></div></a>' if WA_ON else "")
    body = f'''
{page_hero("hero-contact", "Let&rsquo;s plan together", "Plan your <em>trip</em>", "Flights, a holiday or both &mdash; tell us where and when and we&rsquo;ll send options and a clear quote.", [("Contact", "")], kind="still", alt="Wat Arun lit up at night on the Chao Phraya River")}
<section class="section">
  <div class="container contact-grid">
    <div class="panel" id="form" data-reveal>
      <div class="panel__head"><span class="panel__icon">{icon("send", "i i--lg")}</span><div><span class="kicker">Enquiry</span><h2>Send us your plan</h2></div></div>
      <p class="panel__lead">Fields marked * are required. We usually reply with options and a quote.</p>
      {enquiry_form("contact", page_name="contact")}
    </div>
    <aside class="contact-side" data-reveal>
      <div class="person">
        {img("brand-sunrise", "Backpack and camera on a mountain top at sunrise", "person__img")}
        <div class="person__body">
          <span class="kicker">Talk to us</span>
          <a href="tel:{SITE["phone_link"]}" class="person__name">{SITE["phone_display"]}</a>
          <a href="mailto:{SITE["email"]}" class="person__line">{icon("mail", "i i--sm")} {SITE["email"]}</a>
          <span class="person__line">{icon("pin", "i i--sm")} {SITE["city"]}</span>
          {motto()}
        </div>
      </div>
      {wa_card}
      <div class="help-card"><span class="help-card__icon">{icon("download", "i i--lg")}</span><h3>Download an itinerary</h3><p>See the full day-by-day plan before you enquire.</p>
        <div class="btns"><a href="{PKG["rajasthan"]["pdf"]}" class="btn btn--ink btn--sm" download>{icon("download", "i i--sm")} Rajasthan</a><a href="{PKG["thailand"]["pdf"]}" class="btn btn--line btn--sm" download>{icon("download", "i i--sm")} Thailand</a></div></div>
    </aside>
  </div>
</section>
{faq_section(FAQS[:4], "Before you ask", "Common <em>questions</em>", "The essentials about booking and what&rsquo;s included.")}'''
    page("contact.html", "Contact & Enquiries | Plan Your Trip | Travel Dervish",
         f"Send Travel Dervish an enquiry or call {SITE['phone_display']} to book flight tickets or plan a holiday in India or abroad.",
         body, "contact", og="hero-contact", datalist=True)

def build_simple(fname, title, desc, inner):
    body = f'''<section class="center-page"><div class="center-page__sky" aria-hidden="true">{sky_scene()}</div><div class="center-page__card" data-reveal>{inner}</div></section>'''
    page(fname, title, desc, body, "", overlay=False)

def build_misc():
    wa = (f'<a href="{WA_LINK}" target="_blank" rel="noopener" class="btn btn--line">{icon("whatsapp", "i i--sm")} WhatsApp us</a>' if WA_ON else "")
    build_simple("thank-you.html", "Thank You | Travel Dervish", "Your enquiry has been sent to Travel Dervish.", f'''
<div class="check-circle">{icon("check")}</div>
{motto()}
<h1>Thank you &mdash; enquiry <em>received!</em></h1>
<p>We&rsquo;ll get back to you with options and a clear quote. For anything urgent, call us on <a href="tel:{SITE["phone_link"]}">{SITE["phone_display"]}</a>.</p>
<div class="btns btns--center"><a href="journeys.html" class="btn btn--ink">Browse holidays</a><a href="index.html" class="btn btn--line">Back to home</a>{wa}</div>''')
    build_simple("404.html", "Page Not Found | Travel Dervish", "This page could not be found.", f'''
<div class="big">4{icon("plane-fill", "i")}4</div>
<h1>Looks like you took a <em>wrong turn</em></h1>
<p>The page you&rsquo;re looking for doesn&rsquo;t exist. Let&rsquo;s get you back on the route.</p>
<div class="btns btns--center"><a href="index.html" class="btn btn--sun">{icon("arrow-left", "i i--sm")} Back to home</a><a href="journeys.html" class="btn btn--line">See holidays</a></div>''')

def build_extras():
    pages = ["", "journeys", "flights", "rajasthan-heritage-tour", "thailand-holiday-package", "about", "contact"]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
         "".join(f"  <url><loc>{SITE['url']}/{u}</loc></url>\n" for u in pages) + "</urlset>\n"
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8", newline="\n").write(sm)
    open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8", newline="\n").write(f"User-agent: *\nAllow: /\nSitemap: {SITE['url']}/sitemap.xml\n")
    fav = open(os.path.join(HERE, "brand", "favicon.svg"), encoding="utf-8").read()
    open(os.path.join(OUT, "assets", "img", "favicon.svg"), "w", encoding="utf-8", newline="\n").write(fav)
    print("built sitemap.xml, robots.txt, favicon.svg")

if __name__ == "__main__":
    build_assets()
    build_home(); build_journeys(); build_flights()
    for p in PACKAGES: build_package(p)
    build_about(); build_contact(); build_misc(); build_extras()
