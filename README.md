# Travel Dervish · travel.designdervish.com

**Your Travel Partner for Every Journey.** A self-contained travel-agency website for flight tickets and holiday packages, India and international.
Every photo, video, font, icon, script and PDF is stored inside the site. Nothing loads from outside links, so it runs on any static host. It is published on Cloudflare Pages; only the enquiry-form mailer runs on Hostinger.

## Folder guide

| Path | What it is | Upload? |
|---|---|---|
| `website/` | **The live website.** Cloudflare Pages publishes this folder from GitHub | Via GitHub |
| `hostinger-forms/send-enquiry.php` | The enquiry-form mailer. Lives on Hostinger at `public_html/travel-forms/` | **Yes, to Hostinger** |
| `travel-dervish-website.zip` | Zip of `website/`, only needed if you ever host the site on Hostinger again | No |
| `_builder/content.py` | **All editable content**: contact details, packages, FAQs, banner scenes, airport list | No |
| `_builder/src/` | **Design source**: `style.css`, `main.js`, `fonts.css`. Edit these, then build | No |
| `_builder/build.py` | Builds every page: minifies `src/`, builds the stylesheet into each page and writes `website/assets/js/site.js` | No |
| `_builder/fetch_assets.py` | Re-creates the photos as AVIF + WebP (Unsplash originals, needs ffmpeg for AVIF) and the trimmed fonts | No |
| `_builder/encode_video.sh` | Turns a Google Flow clip into web banner files (crops off the Flow mark) | No |
| `_builder/fonts-src/` | Full original font files (the site uses trimmed copies) | No |
| `_builder/brand/` | Traced logo paths, favicon, and `make_share_image.py` (makes the WhatsApp/Facebook link-preview card `og-travel-dervish.jpg` and the iPhone icon) | No |
| `_builder/unused-assets/` | Fonts and photos from the previous theme, kept in case you want them back | No |
| `_flow/frames/` | The start-frame photos used to generate the Flow clips | No |

**After any change:** run `python _builder/build.py`, then re-zip the *contents* of `website/` (or ask Claude to rebuild).

## Pages

| Page | File |
|---|---|
| Home: video banner (4 Flow clips, India + international), **Flight Tickets / Travel Packages** booking widget, ticker, services, India / International tiles, boarding-pass holiday cards, Plan · Book · Explore, 3D destination coverflow, signature-journey video, tagline video band, gallery, FAQ | `index.html` |
| Holidays, with India / International tabs and style filters | `journeys.html` (`?type=india`, `?type=international`) |
| Flights: fare-request form (one way, round trip, multi-city, cabin), why book with us, FAQ | `flights.html` |
| Rajasthan Heritage, Culture & Wildlife Tour / Thailand Holiday: video banner, gallery, itinerary, quote form | `rajasthan-heritage-tour.html`, `thailand-holiday-package.html` |
| About · Contact (Holiday / Flight / Flight + holiday switch) · Thank-you · 404 | `about.html`, `contact.html`, `thank-you.html`, `404.html` |
| Form handler: emails every enquiry, flight details included (runs on Hostinger) | `hostinger-forms/send-enquiry.php` |

## Theme: "Golden Hour" (built from the Travel Dervish logo and poster)

- **Colours:** logo yellow `#FCC800`, warm black `#121110`, sunrise cream `#FBF6EC`, sand `#F3EADA`, ember `#E8711C`
- **Fonts** (Indian Type Foundry via Fontshare, free for commercial use, self-hosted): **Boska** for headlines, **Bespoke Stencil** for labels and buttons, **Amulya** for text
- **Motion:** video chapters with progress bars and a pause button; 3D mouse parallax; tilt-and-glare cards; 3D coverflow; a code-built sunrise sky (Flights, Thank-you, 404)

## Speed and smoothness

Measured in Chrome (desktop and phone emulation) on every page:
- **The banner appears in 0.12–0.16 s on phones.**
- **Layout shift is 0** everywhere, with no JavaScript errors.
- **First-visit download of the home page:** 0.75 MB on phones, 1.2 MB on desktops (was 1.46 MB and 2.76 MB). About half of that is the banner video, which starts only after the page has loaded.
- Dragging the destinations carousel and scrolling run at about 90 frames per second.

- **Photos:**
  - Every photo is served as **AVIF**, about a third lighter than WebP at the same look: 3.1 MB vs 4.9 MB for the whole set. WebP stays as an automatic fallback for older browsers.
  - Phones and thumbnails get smaller copies (`-sm`), chosen automatically.
  - Video stills further down the page load only as you scroll.
- **Fonts:** only the 7 styles in use, trimmed to the characters the site needs: 98 KB in total (was 316 KB). Size-matched Georgia/Arial fallbacks mean text doesn't jump when the fonts arrive. The 4 fonts needed first are preloaded.
- **Videos:**
  - 0.77–1.4 MB in HD, 0.34–0.55 MB on phones.
  - The banner's first frame shows instantly as an image; the video starts once the page has loaded. Each next clip is fetched about 4.5 s before it's shown.
  - Off-screen videos pause; video is skipped for "reduce motion" and data-saver users.
- **No render-blocking files:** the stylesheet is built into each page (one round-trip less before the first paint). Each page carries only the icons it uses, and the script loads after the page (version-tagged, cached for a year).
- **Instant pages:**
  - Chrome and Edge pre-render the next page as soon as a link is hovered (or pressed on touch screens), so the click opens it immediately. Other browsers prefetch on hover or touch.
  - Pre-rendered pages hold their videos and timers until they're actually opened.
  - Pages cross-fade into each other instead of flashing white (Chrome, Edge, Safari 18+).
- **Smoothness fixes:**
  - The header can't flicker at the scroll threshold.
  - Parallax moves layers directly on the GPU, and only on desktops with a mouse.
  - Banner clips cross-fade without the zoom snapping.
  - The glass blur on the booking box runs only on desktops.
  - Looping decorations rest while off-screen.
- **Destinations carousel ("Places we'll take you"):**
  - Cards follow the mouse or finger 1:1, glide on with momentum and settle smoothly.
  - Desktops get a custom yellow "← Drag →" cursor that turns into "View ↗" over the front card. Laptop trackpads can side-swipe; arrow keys and the round buttons also work. (No counter or "drag to explore" line under the cards.)
  - On phones it swipes; a vertical swipe still scrolls the page.
  - All photos are decoded before the section comes into view.
- **Server (`.htaccess`):** Brotli/Gzip compression (pages shrink to about a quarter of their size in transit), a 1-year cache for JS and fonts, 30 days for photos and videos, and no cache for HTML pages, so changes show immediately.

## Banner videos (Google Flow)

| Clip | Used on | Files |
|---|---|---|
| Camel caravan, Thar desert | Home (scene 1), tagline band, Holidays CTA | `desert-hd/sm.mp4` |
| Longtail boats, tropical bay | Home (scene 2), Thailand page, International tile, CTA bands | `bay-hd/sm.mp4` |
| Boat on Lake Pichola | Home (scene 3), Holidays page, India tile, signature section, About CTA | `lake-hd/sm.mp4` |
| Amber Fort above Maota Lake | Home (scene 4), Rajasthan page | `fort-hd/sm.mp4` |

Each clip is trimmed past Flow's opening morph and turned into a seamless loop. The **Flow sparkle mark is removed** by cropping the frame just before the corner where it sits; nothing is blurred or smudged.
Google's invisible SynthID watermark stays inside the files.
About and Contact use photo banners with slow 3D motion.
**To add a clip:** generate it in Flow, then run `sh _builder/encode_video.sh <clip.mp4> <name> <start> <end>`.
Then, in `build.py`, change that page's `page_hero("hero-about", ..., kind="still")` to `page_hero("<name>", ...)`.

---

## 1. Before going live

| What | Now | Where to change |
|---|---|---|
| Phone (shown on its own, no name) | `+91 99105 61078` | `_builder/content.py` → `SITE` |
| Email shown and enquiry inbox | `travel@designdervish.com` | `content.py` → `SITE["email"]` and `hostinger-forms/send-enquiry.php` → `$TO` |
| Sender address for enquiry emails | `no-reply@designdervish.com` | `send-enquiry.php` → `$FROM` (must be on a domain you host at Hostinger) |
| WhatsApp | **Switched off** (number pre-filled as 919910561078) | `content.py` → `SITE["show_whatsapp"] = True` |
| Instagram / Facebook / Pinterest | generic links | `content.py` → `SITE` |

**Please check:** the poster prints the email as `travel@designdrvish.com` (no "e"). The site uses `travel@designdervish.com`. Make sure that mailbox exists.
**Also review:** the flight wording, the FAQ answers and the About text. Prices show "On request" because the PDFs have none.

## 2. Hosting: Cloudflare Pages (website) + Hostinger (enquiry emails)

The website is published by **Cloudflare Pages** straight from GitHub (free, business use allowed): push a change and it's live in about a minute.
Cloudflare can't run PHP, so the one form-mailer file stays on your Hostinger hosting.
Your main site designdervish.com is not affected.

**A. Put the form mailer on Hostinger (do this first)**
1. hPanel → *Files* → *File Manager* → open `public_html` (the main site's folder, next to `wp-content`).
2. Create a new folder `travel-forms`, open it, and upload `hostinger-forms/send-enquiry.php`.
3. Open `https://designdervish.com/travel-forms/send-enquiry.php` in the browser. It should jump to the Travel Dervish contact page, which means it works.
4. Make sure the mailboxes `travel@designdervish.com` (receives enquiries) and `no-reply@designdervish.com` (sender) exist under hPanel → *Emails*.

**B. Put the project on GitHub**
Create a **private** repository (for example `travel-dervish`) and push this project folder. `.gitignore` already leaves out the zips, drafts and full font files.

**C. Create the Cloudflare Pages project**
1. Cloudflare dashboard → *Workers & Pages* → *Create* → *Pages* → *Import an existing Git repository* → connect GitHub → pick the repo.
2. Project name: `travel-dervish`. This gives the preview address `travel-dervish.pages.dev`; the form mailer only accepts that name, so change it in `send-enquiry.php` if you pick another.
3. Framework preset **None**, build command **(leave empty)**, build output directory **`website`** → *Save and Deploy*.
4. Test `https://travel-dervish.pages.dev`, including one enquiry from Contact and one from Flights.

**D. Connect travel.designdervish.com**
1. In the Pages project: *Custom domains* → *Set up a custom domain* → `travel.designdervish.com`. Cloudflare asks you to add a **CNAME** record.
2. hPanel → *Domains* → designdervish.com → *DNS / Nameservers* (DNS records):
   - delete the **A** record named `travel` (and any AAAA record for `travel`)
   - add a **CNAME** record: name `travel`, target `travel-dervish.pages.dev`
   If hPanel won't allow it because the Hostinger subdomain exists, delete the `travel` subdomain under *Domains → Subdomains* first. Your files are safe on your computer and on GitHub.
3. Back in Cloudflare, click *Check DNS* / *Activate*. It turns **Active** with HTTPS, usually within minutes (allow up to a few hours).

**E. Updating the site later**
Edit `_builder/content.py` or `_builder/src/`, run `python _builder/build.py`, then commit and push. Cloudflare publishes it automatically.

**Optional:** add the site in Google Search Console and submit `https://travel.designdervish.com/sitemap.xml`.

## 3. Adding a new package

1. Add its photos to `PHOTOS` in `_builder/fetch_assets.py` and run `python _builder/fetch_assets.py --photos-only`. Put the PDF in `website/assets/pdf/`.
2. Copy one entry in `PACKAGES` in `_builder/content.py`: set `"type"` (`"india"` / `"international"`), `"slug"`, `"file"`, `"ends"` (from/to on the card) and `"video"` (a clip name or `None`).
3. Run `python _builder/build.py`. Add its URL to the sitemap list in `build_extras()`.

## Notes

- **Photos:** Unsplash, free Unsplash License (IDs in `_builder/fetch_assets.py`). The backpack-at-sunrise image comes from your brand poster.
- **Videos:** generated by you in Google Flow. **Fonts:** Boska, Bespoke Stencil, Amulya (ITF Free Font License).
- **PDF itineraries:** your originals. Some photos inside them look web-sourced (one carries a "danso.info" watermark).
