(function () {
'use strict';
var $ = function (s, c) { return (c || document).querySelector(s); };
var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
var mq = function (q) { return !!(window.matchMedia && window.matchMedia(q).matches); };
var params = new URLSearchParams(window.location.search);
var WA = document.body.getAttribute('data-wa') || '';
var REDUCE = mq('(prefers-reduced-motion: reduce)');
var FINE = mq('(hover: hover) and (pointer: fine)');
var SMALL = mq('(max-width: 899px)');
var SAVE = !!(navigator.connection && navigator.connection.saveData);
var VIDEO_OK = !REDUCE && !SAVE;
var HAS_IO = 'IntersectionObserver' in window;
function whenActive(fn) { if (document.prerendering) document.addEventListener('prerenderingchange', fn, { once: true }); else fn(); }
function whenLoaded(fn) {
whenActive(function () {
if (document.readyState === 'complete') setTimeout(fn, 0);
else window.addEventListener('load', function () { setTimeout(fn, 0); }, { once: true });
});
}
var header = $('.header');
var toTop = $('.to-top');
var overlay = header && header.classList.contains('header--overlay');
var fixed = false, topVis = false, sTick = false;
function onScroll() {
sTick = false;
var y = window.pageYOffset;
if (overlay) {
if (!fixed && y > 120) { fixed = true; header.classList.add('is-fixed'); }
else if (fixed && y < 40) { fixed = false; header.classList.remove('is-fixed'); }
}
if (toTop) {
if (!topVis && y > 800) { topVis = true; toTop.classList.add('is-visible'); }
else if (topVis && y < 700) { topVis = false; toTop.classList.remove('is-visible'); }
}
}
window.addEventListener('scroll', function () { if (!sTick) { sTick = true; requestAnimationFrame(onScroll); } }, { passive: true });
onScroll();
if (toTop) toTop.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: REDUCE ? 'auto' : 'smooth' }); });
var mnav = $('.mobile-nav');
function navOpen(open) {
if (!mnav) return;
mnav.classList.toggle('is-open', open);
document.body.style.overflow = open ? 'hidden' : '';
}
$$('[data-nav-open]').forEach(function (b) { b.addEventListener('click', function () { navOpen(true); }); });
$$('[data-nav-close]').forEach(function (b) { b.addEventListener('click', function () { navOpen(false); }); });
document.addEventListener('keydown', function (e) { if (e.key === 'Escape') navOpen(false); });
function srcFor(el) { return el.getAttribute(SMALL ? 'data-sm' : 'data-hd'); }
function playV(v) { if (!v) return; var p = v.play(); if (p && p.catch) p.catch(function () {}); }
function markPlaying(clip, v) {
var on = function () { clip.classList.add('is-playing'); };
if (!v.paused && v.readyState > 2) on();
v.addEventListener('playing', on);
v.addEventListener('timeupdate', function t() { if (v.currentTime > 0) { on(); v.removeEventListener('timeupdate', t); } });
}
function loadClip(clip) {
var v = $('video', clip);
if (!v) return null;
if (!v.hasAttribute('data-ready')) {
v.setAttribute('data-ready', '');
if (!v.querySelector('source') && !v.getAttribute('src')) { v.preload = 'auto'; v.src = srcFor(clip); }
markPlaying(clip, v);
}
return v;
}
if (!VIDEO_OK) $$('video[autoplay]').forEach(function (v) { v.removeAttribute('autoplay'); v.pause(); v.preload = 'none'; });
$$('[data-hero]').forEach(function (hero) {
var clips = $$('[data-clip]', hero);
var chapters = $$('[data-chapter]', hero);
var seq = hero.hasAttribute('data-hero-seq') && clips.length > 1;
var DUR = 9000, FADE = 1400, cur = 0, timer = null, paused = false, inView = true;
hero.style.setProperty('--chapter-dur', DUR / 1000 + 's');
function bars() {
chapters.forEach(function (b, i) { b.classList.toggle('is-active', i === cur); b.setAttribute('aria-current', i === cur ? 'true' : 'false'); });
var bar = chapters[cur] && $('.chapter__bar i', chapters[cur]);
if (bar) { bar.style.animation = 'none'; void bar.offsetWidth; bar.style.animation = ''; }
}
var warmT = null;
function schedule() {
clearTimeout(timer); clearTimeout(warmT);
if (!seq || paused || !inView) return;
timer = setTimeout(function () { go(cur + 1); }, DUR);
if (VIDEO_OK) warmT = setTimeout(function () { loadClip(clips[(cur + 1) % clips.length]); }, DUR - 4500);
}
function go(n) {
var prev = clips[cur];
cur = (n + clips.length) % clips.length;
var c = clips[cur];
if (prev !== c) {
prev.classList.remove('is-active'); prev.classList.add('is-leaving');
c.classList.remove('is-leaving'); c.classList.add('is-active');
setTimeout(function () {
if (prev.classList.contains('is-active')) return;
prev.classList.remove('is-leaving');
var pv = $('video', prev); if (pv) pv.pause();
}, FADE);
}
if (VIDEO_OK) {
var v = loadClip(c);
if (v) { try { v.currentTime = 0; } catch (e) {} if (!paused) playV(v); }
}
bars(); schedule();
}
if (clips.length && VIDEO_OK) {
var first = loadClip(clips[0]);
whenLoaded(function () {
if (!first || paused || clips[cur] !== clips[0]) return;
first.preload = 'auto'; playV(first);
});
}
if (seq) {
bars(); whenActive(schedule);
chapters.forEach(function (b, i) { b.addEventListener('click', function () { if (i === cur && !paused) return; setPaused(false); go(i); }); });
}
var pauseBtn = $('[data-hero-pause]', hero);
function setPaused(p) {
paused = p;
hero.classList.toggle('is-paused', p);
if (pauseBtn) { pauseBtn.setAttribute('aria-pressed', p ? 'true' : 'false'); pauseBtn.setAttribute('aria-label', p ? 'Play banner video' : 'Pause banner video'); }
var v = clips[cur] && $('video', clips[cur]);
if (p) { clearTimeout(timer); if (v) v.pause(); } else if (v && VIDEO_OK) playV(v);
}
if (pauseBtn) pauseBtn.addEventListener('click', function () { if (paused) { setPaused(false); go(cur); } else setPaused(true); });
if (HAS_IO && clips.length) {
new IntersectionObserver(function (en) {
inView = en[0].isIntersecting;
var v = clips[cur] && $('video', clips[cur]);
if (!inView) { clearTimeout(timer); if (v) v.pause(); }
else if (!paused) { if (v && VIDEO_OK) playV(v); schedule(); }
}, { threshold: 0.02 }).observe(hero);
}
if (REDUCE || !FINE) return;
var stage = $('[data-stage]', hero);
var layers = $$('[data-depth], .sky__sun, .sky__mtn', hero).map(function (el) {
var d = parseFloat(el.style.getPropertyValue('--d')) || 0;
return { el: el, d: el.classList.contains('sky__mtn') ? -d : d };
});
var tx = 0, ty = 0, mx = 0, my = 0, sy = 0, raf = 0;
function paint() {
raf = 0;
mx += (tx - mx) * 0.085; my += (ty - my) * 0.085;
if (stage) stage.style.transform = 'translate3d(' + (mx * -16).toFixed(2) + 'px,' + (my * -11 + sy * 0.28).toFixed(2) + 'px,0)';
for (var i = 0; i < layers.length; i++) {
var L = layers[i];
L.el.style.transform = 'translate3d(' + (mx * L.d).toFixed(2) + 'px,' + (my * Math.abs(L.d) * 0.6).toFixed(2) + 'px,0)';
}
if (Math.abs(tx - mx) > 0.002 || Math.abs(ty - my) > 0.002) raf = requestAnimationFrame(paint);
}
function kick() { if (!raf) raf = requestAnimationFrame(paint); }
hero.addEventListener('pointermove', function (e) {
var r = hero.getBoundingClientRect();
tx = ((e.clientX - r.left) / r.width - 0.5) * 2; ty = ((e.clientY - r.top) / r.height - 0.5) * 2; kick();
}, { passive: true });
hero.addEventListener('pointerleave', function () { tx = 0; ty = 0; kick(); });
window.addEventListener('scroll', function () {
var top = hero.getBoundingClientRect().top;
var v = top < 0 ? Math.min(-top, hero.offsetHeight) : 0;
if (v !== sy) { sy = v; kick(); }
}, { passive: true });
});
if (HAS_IO) {
var idle = new IntersectionObserver(function (entries) {
entries.forEach(function (en) {
en.target.classList.toggle('is-idle', !en.isIntersecting);
var svgs = $$('svg', en.target);
if (en.target.tagName.toLowerCase() === 'svg') svgs.push(en.target);
svgs.forEach(function (svg) {
if (svg.pauseAnimations) { if (en.isIntersecting) svg.unpauseAnimations(); else svg.pauseAnimations(); }
});
});
}, { rootMargin: '100px 0px' });
$$('.ticker, .stamp, .sky, .pbe__path, .duo__arc').forEach(function (el) { idle.observe(el); });
}
var lazy = $$('[data-lazy-video]');
if (lazy.length && HAS_IO && VIDEO_OK) whenLoaded(function () {
var vio = new IntersectionObserver(function (entries) {
entries.forEach(function (en) {
var v = en.target;
if (en.isIntersecting) {
if (!v.getAttribute('src')) { v.src = srcFor(v); v.addEventListener('playing', function () { v.classList.add('is-playing'); }); }
playV(v);
}
else if (v.getAttribute('src')) v.pause();
});
}, { rootMargin: '200px 0px' });
lazy.forEach(function (v) { vio.observe(v); });
});
if (FINE && VIDEO_OK) $$('[data-hover-video]').forEach(function (el) {
var v = $('video', el);
if (!v) return;
el.addEventListener('mouseenter', function () {
if (!v.getAttribute('src')) { v.src = srcFor(v); v.addEventListener('playing', function () { if (el.matches(':hover')) el.classList.add('is-playing'); }); }
else el.classList.add('is-playing');
playV(v);
});
el.addEventListener('mouseleave', function () { el.classList.remove('is-playing'); v.pause(); });
});
if (FINE && !REDUCE) $$('[data-tilt]').forEach(function (el) {
var raf = 0;
el.addEventListener('pointermove', function (e) {
var r = el.getBoundingClientRect();
var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
var max = r.width > 520 ? 4 : 8;
cancelAnimationFrame(raf);
raf = requestAnimationFrame(function () {
el.style.setProperty('--ry', (x * max).toFixed(2) + 'deg');
el.style.setProperty('--rx', (-y * max * 0.75).toFixed(2) + 'deg');
el.style.setProperty('--gx', ((x + 0.5) * 100).toFixed(1) + '%');
el.style.setProperty('--gy', ((y + 0.5) * 100).toFixed(1) + '%');
el.classList.add('is-tilting');
});
});
el.addEventListener('pointerleave', function () {
cancelAnimationFrame(raf);
el.classList.remove('is-tilting');
el.style.setProperty('--rx', '0deg'); el.style.setProperty('--ry', '0deg');
});
});
function ic(n) { return '<svg class="i" aria-hidden="true"><use href="#i-' + n + '"/></svg>'; }
$$('[data-flow]').forEach(function (flow) {
var items = $$('[data-flow-item]', flow), n = items.length;
if (!n) return;
var section = flow.closest('section') || document;
var idxEl = $('[data-flow-index]', section), barEl = $('[data-flow-bar]', section);
var imgs = items.map(function (it) { return $('img', it); });
var shades = items.map(function (it) { return $('.flow__shade', it); });
var memo = items.map(function () { return { t: '', z: '', o: '', s: '', p: '' }; });
var pos = 0, target = 0, sp = 200, iw = 300, perItem = 300, raf = 0, last = 0, active = -1;
var dragging = false, wheeling = false, pid = null, downX = 0, downPos = 0, moved = false, vx = 0, lastX = 0, lastT = 0;
var visible = false, idleUntil = 0;
function clamp(v, lo, hi) { return v < lo ? lo : v > hi ? hi : v; }
function wrap(o) { o = ((o % n) + n) % n; return o > n / 2 ? o - n : o; }
function set(i, key, prop, val, el) { if (memo[i][key] !== val) { memo[i][key] = val; (el || items[i]).style[prop] = val; } }
function measure() {
iw = items[0].offsetWidth || 300;
sp = Math.max(Math.min(iw * 0.55, flow.clientWidth * 0.17), 58);
perItem = Math.max(sp * 1.5, 110);   // pixels of drag that move one card
render();
}
function render() {
for (var i = 0; i < n; i++) {
var o = wrap(i - pos), a = Math.abs(o), c = clamp(o, -1, 1);
var x = o * sp + c * iw * 0.32;
set(i, 't', 'transform', 'translate(-50%,-50%) translate3d(' + x.toFixed(1) + 'px,0,' + (-a * 150).toFixed(1) + 'px) rotateY(' + (-c * 42).toFixed(2) + 'deg)');
set(i, 'z', 'zIndex', String(100 - Math.round(a * 10)));
var op = a > 3.4 ? 0 : a > 2.9 ? (3.4 - a) * 2 : 1;
set(i, 'o', 'opacity', op.toFixed(2));
if (shades[i]) set(i, 's', 'opacity', Math.min(a, 1).toFixed(2), shades[i]);
if (imgs[i]) set(i, 'p', 'transform', 'translate3d(' + (clamp(o, -1.5, 1.5) * -4).toFixed(2) + '%,0,0)', imgs[i]);
}
var k = ((Math.round(pos) % n) + n) % n;
if (k !== active) {
active = k;
items.forEach(function (it, i) { var on = i === k; it.classList.toggle('is-active', on); it.tabIndex = on ? 0 : -1; });
if (idxEl) idxEl.textContent = (k < 9 ? '0' : '') + (k + 1);
if (barEl) barEl.style.transform = 'scaleX(' + ((k + 1) / n).toFixed(3) + ')';
}
}
function tick(t) {
raf = 0;
var dt = last ? Math.min((t - last) / 1000, 0.05) : 0.016;
last = t;
if (!dragging && !wheeling) {
var d = target - pos;
pos += d * (1 - Math.exp(-dt * (REDUCE ? 40 : 9)));
if (Math.abs(d) < 0.0006) pos = target;
}
render();
if (dragging || wheeling || pos !== target) raf = requestAnimationFrame(tick); else last = 0;
}
function kick() { if (!raf) raf = requestAnimationFrame(tick); }
function goTo(t) { target = t; kick(); }
function step(d) { goTo(Math.round(target) + d); hold(); }
function hold() { idleUntil = Date.now() + 7000; }
flow.addEventListener('pointerdown', function (e) {
if (e.pointerType === 'mouse' && e.button !== 0) return;
dragging = true; moved = false; pid = e.pointerId;
downX = lastX = e.clientX; lastT = e.timeStamp; downPos = pos; vx = 0;
target = pos; hold(); kick();
});
flow.addEventListener('pointermove', function (e) {
if (!dragging || e.pointerId !== pid) return;
var dx = e.clientX - downX;
if (!moved) {
if (Math.abs(dx) < 6) return;
moved = true; flow.classList.add('is-dragging');
try { flow.setPointerCapture(pid); } catch (err) {}
}
pos = downPos - dx / perItem;
var dtm = e.timeStamp - lastT;
if (dtm > 0) { vx = 0.75 * ((e.clientX - lastX) / dtm) + 0.25 * vx; lastX = e.clientX; lastT = e.timeStamp; }
kick();
});
function release(e) {
if (!dragging || (e && e.pointerId !== pid)) return;
dragging = false; flow.classList.remove('is-dragging');
if (e && e.timeStamp - lastT > 90) vx = 0;              // finger rested before lifting: no fling
var fling = clamp(-vx * 1000 / perItem * 0.24, -3, 3);   // momentum, in cards
goTo(Math.round(pos + fling)); hold();
setTimeout(function () { moved = false; }, 0);
}
flow.addEventListener('pointerup', release);
flow.addEventListener('pointercancel', release);
flow.addEventListener('lostpointercapture', function (e) { if (dragging) release(e); });
items.forEach(function (it, i) {
it.addEventListener('click', function (e) {
if (moved) { e.preventDefault(); return; }
if (i !== active) { e.preventDefault(); goTo(Math.round(target) + wrap(i - Math.round(target))); hold(); }
});
it.addEventListener('dragstart', function (e) { e.preventDefault(); });
});
var wheelT = null;
flow.addEventListener('wheel', function (e) {
if (Math.abs(e.deltaX) <= Math.abs(e.deltaY) * 1.2) return;
e.preventDefault();
wheeling = true; pos += e.deltaX / (perItem * 1.4); target = pos; hold(); kick();
clearTimeout(wheelT);
wheelT = setTimeout(function () { wheeling = false; goTo(Math.round(pos)); }, 110);
}, { passive: false });
flow.addEventListener('keydown', function (e) {
if (e.key === 'ArrowRight') { step(1); e.preventDefault(); }
if (e.key === 'ArrowLeft') { step(-1); e.preventDefault(); }
});
var nb = $('[data-flow-next]', section), pb = $('[data-flow-prev]', section);
if (nb) nb.addEventListener('click', function () { step(1); });
if (pb) pb.addEventListener('click', function () { step(-1); });
if (HAS_IO) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; }, { threshold: 0.35 }).observe(flow);
if (!REDUCE) setInterval(function () {
if (visible && !document.hidden && !dragging && !wheeling && Date.now() > idleUntil) goTo(Math.round(target) + 1);
}, 4200);
var rto = null;
window.addEventListener('resize', function () { clearTimeout(rto); rto = setTimeout(measure, 120); });
measure();
if (HAS_IO) {
var warm = new IntersectionObserver(function (en) {
if (!en[0].isIntersecting) return;
warm.disconnect();
imgs.forEach(function (im) { if (!im) return; im.loading = 'eager'; if (im.decode) im.decode().catch(function () {}); });
}, { rootMargin: '700px 0px' });
warm.observe(flow);
}
if (!FINE) return;
var cur = document.createElement('div');
cur.className = 'flow-cursor';
cur.setAttribute('aria-hidden', 'true');
cur.innerHTML = '<div class="flow-cursor__in"><span class="flow-cursor__drag">' + ic('arrow-left') + 'Drag' + ic('arrow-right') +
'</span><span class="flow-cursor__view">View' + ic('arrow-up-right') + '</span></div>';
document.body.appendChild(cur);
document.documentElement.classList.add('has-flow-cursor');
var cx = -300, cy = -300, gx = -300, gy = -300, craf = 0;
function cpaint() {
craf = 0;
var k = REDUCE ? 1 : 0.3;
cx += (gx - cx) * k; cy += (gy - cy) * k;
cur.style.transform = 'translate3d(' + cx.toFixed(1) + 'px,' + cy.toFixed(1) + 'px,0)';
if (Math.abs(gx - cx) > 0.2 || Math.abs(gy - cy) > 0.2) craf = requestAnimationFrame(cpaint);
}
flow.addEventListener('pointerenter', function (e) {
if (e.pointerType !== 'mouse') return;
cx = gx = e.clientX; cy = gy = e.clientY; cpaint(); cur.classList.add('is-on');
});
flow.addEventListener('pointermove', function (e) {
if (e.pointerType !== 'mouse') return;
gx = e.clientX; gy = e.clientY;
if (!cur.classList.contains('is-on')) { cx = gx; cy = gy; cur.classList.add('is-on'); }
if (!craf) craf = requestAnimationFrame(cpaint);
var t = e.target.closest ? e.target.closest('[data-flow-item]') : null;
cur.classList.toggle('is-view', !dragging && !!t && t.classList.contains('is-active'));
hold();
});
flow.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse' && !dragging) cur.classList.remove('is-on', 'is-view', 'is-down'); });
flow.addEventListener('pointerdown', function (e) { if (e.pointerType === 'mouse') { cur.classList.add('is-down'); cur.classList.remove('is-view'); } });
window.addEventListener('pointerup', function () { cur.classList.remove('is-down'); });
window.addEventListener('scroll', function () { if (!dragging) cur.classList.remove('is-on', 'is-view'); }, { passive: true });
});
var specOK = HTMLScriptElement.supports && HTMLScriptElement.supports('speculationrules');
if (!specOK && !SAVE) {
var fetched = {};
var pre = function (e) {
var a = e.target.closest && e.target.closest('a[href]');
if (!a || a.target === '_blank' || a.hasAttribute('download') || a.origin !== location.origin) return;
var url = a.href.split('#')[0];
if (fetched[url] || url === location.href.split('#')[0] || !/\.html(\?|$)/.test(url)) return;
fetched[url] = 1;
var l = document.createElement('link'); l.rel = 'prefetch'; l.href = url; document.head.appendChild(l);
};
document.addEventListener('mouseover', pre, { passive: true });
document.addEventListener('touchstart', pre, { passive: true });
}
$$('[data-book-tab]').forEach(function (tab) {
tab.addEventListener('click', function () {
var key = tab.getAttribute('data-book-tab'), root = tab.closest('.booker');
$$('[data-book-tab]', root).forEach(function (t) { var on = t === tab; t.classList.toggle('is-active', on); t.setAttribute('aria-selected', on ? 'true' : 'false'); });
$$('[data-book-panel]', root).forEach(function (p) { p.classList.toggle('is-active', p.getAttribute('data-book-panel') === key); });
});
});
$$('[data-swap]').forEach(function (b) {
b.addEventListener('click', function () {
var f = b.closest('form'), a = f.elements.from, c = f.elements.to, t = a.value;
a.value = c.value; c.value = t;
});
});
$$('[data-pkg-finder]').forEach(function (form) {
var sel = $('[data-pkg-select]', form);
function scope() { var r = form.querySelector('[data-scope]:checked'); return r ? r.value : ''; }
function filter() {
var s = scope();
Array.prototype.forEach.call(sel.options, function (o) {
var t = o.getAttribute('data-type');
if (!t) return;
o.hidden = o.disabled = !!s && t !== s;
});
if (sel.options[sel.selectedIndex] && sel.options[sel.selectedIndex].disabled) sel.value = '';
}
$$('[data-scope]', form).forEach(function (r) { r.addEventListener('change', filter); });
form.addEventListener('submit', function (e) {
e.preventDefault();
var opt = sel.options[sel.selectedIndex], q = new URLSearchParams();
if (form.elements.month.value) q.set('month', form.elements.month.value);
if (form.elements.travellers.value) q.set('travellers', form.elements.travellers.value);
var page = opt && opt.getAttribute('data-page');
if (page) { window.location.href = page + '?' + q.toString() + '#enquire'; return; }
if (sel.value === 'custom') { q.set('journey', 'custom'); window.location.href = 'contact.html?' + q.toString() + '#form'; return; }
window.location.href = 'journeys.html' + (scope() ? '?type=' + scope() : '');
});
});
var today = new Date(); today.setMinutes(today.getMinutes() - today.getTimezoneOffset());
var todayISO = today.toISOString().slice(0, 10);
function syncTrip(form) {
var el = form.elements.trip;
if (!el) return;
var val = el.value;
$$('[data-return-field]', form).forEach(function (f) {
if (f.closest('[data-for][hidden]')) return;
var off = val !== 'return';
f.hidden = off;
var inp = $('input', f);
if (inp) inp.disabled = off;
});
}
function syncService(form) {
var s = form.querySelector('[data-service]:checked');
if (!s) return;
$$('[data-for]', form).forEach(function (g) {
var on = g.getAttribute('data-for').split(' ').indexOf(s.value) > -1;
g.hidden = !on;
$$('input, select, textarea', g).forEach(function (i) { i.disabled = !on; });
});
syncTrip(form);
}
$$('form').forEach(function (form) {
$$('[data-depart]', form).forEach(function (d) {
d.min = todayISO;
d.addEventListener('change', function () {
$$('[data-returndate]', form).forEach(function (r) { r.min = d.value || todayISO; if (r.value && d.value && r.value < d.value) r.value = ''; });
});
});
$$('[data-returndate]', form).forEach(function (r) { r.min = todayISO; });
$$('[data-trip]', form).forEach(function (t) { t.addEventListener('change', function () { syncTrip(form); }); });
$$('[data-service]', form).forEach(function (s) { s.addEventListener('change', function () { syncService(form); }); });
});
var KEYS = ['journey', 'month', 'travellers', 'style', 'from', 'to', 'depart', 'return', 'trip', 'cabin'];
$$('form[data-enquiry]').forEach(function (form) {
var sv = params.get('service'), el = form.elements.service;
if (sv && el) {
if (el.type === 'checkbox') el.checked = (sv === 'both' || sv === 'flight');
else if (!el.tagName && el.length) el.value = sv;
} else if (el && !el.tagName && el.length && (params.get('from') || params.get('to'))) el.value = 'flight';
KEYS.forEach(function (k) {
var v = params.get(k), f = form.elements[k];
if (!v || !f || !f.tagName) return;
if (f.tagName === 'SELECT' && !Array.prototype.some.call(f.options, function (o) { return o.value === v; })) return;
f.value = v;
});
syncService(form); syncTrip(form);
var err = $('.alert--error', form);
if (err && params.get('error')) err.classList.add('is-shown');
var waBtn = $('[data-wa-form]', form);
if (waBtn && WA) waBtn.addEventListener('click', function () {
var f = form.elements, lines = ['Hello Travel Dervish, I would like to plan a trip.'];
var add = function (label, name) { if (f[name] && f[name].value && !f[name].disabled) lines.push(label + ': ' + f[name].value); };
add('Name', 'name'); add('Journey', 'journey'); add('From', 'from'); add('To', 'to'); add('Depart', 'depart'); add('Return', 'return');
add('Travel month', 'month'); add('Travellers', 'travellers'); add('Message', 'message');
window.open('https://wa.me/' + WA + '?text=' + encodeURIComponent(lines.join('\n')), '_blank', 'noopener');
});
});
var req = $('#request');
if (req && (params.get('from') || params.get('to') || params.get('depart'))) {
setTimeout(function () { req.scrollIntoView({ behavior: REDUCE ? 'auto' : 'smooth', block: 'start' }); }, 350);
}
var listing = $('[data-listing]');
if (listing) {
var state = { type: params.get('type') || 'all', style: 'all' };
var apply = function () {
$$('.tab').forEach(function (t) { t.classList.toggle('is-active', t.getAttribute('data-type') === state.type); });
$$('.chip[data-style]').forEach(function (c) { c.classList.toggle('is-active', c.getAttribute('data-style') === state.style); });
var shown = 0;
$$('.lpass', listing).forEach(function (card) {
var ok = (state.type === 'all' || card.getAttribute('data-type') === state.type) &&
(state.style === 'all' || (' ' + card.getAttribute('data-styles') + ' ').indexOf(' ' + state.style + ' ') > -1);
card.classList.toggle('is-hidden', !ok);
if (ok) { shown++; card.classList.add('is-visible'); }
});
var count = $('[data-count-label]');
if (count) count.textContent = shown + (shown === 1 ? ' holiday' : ' holidays');
};
$$('.tab').forEach(function (t) { t.addEventListener('click', function () { state.type = t.getAttribute('data-type'); apply(); }); });
$$('.chip[data-style]').forEach(function (c) { c.addEventListener('click', function () { state.style = c.getAttribute('data-style'); apply(); }); });
apply();
}
function setOpen(item, open) {
var body = item.querySelector('[data-acc-body]');
item.classList.toggle('is-open', open);
item.querySelector('[data-acc-btn]').setAttribute('aria-expanded', open ? 'true' : 'false');
body.style.maxHeight = open ? body.scrollHeight + 'px' : '0px';
}
$$('[data-acc]').forEach(function (item) {
if (item.classList.contains('is-open')) setOpen(item, true);
item.querySelector('[data-acc-btn]').addEventListener('click', function () { setOpen(item, !item.classList.contains('is-open')); });
});
$$('[data-acc-all]').forEach(function (btn) {
btn.addEventListener('click', function () {
var items = $$('[data-acc]', document.getElementById(btn.getAttribute('data-acc-all')));
var openAll = items.some(function (i) { return !i.classList.contains('is-open'); });
items.forEach(function (i) { setOpen(i, openAll); });
btn.textContent = openAll ? 'Collapse all days' : 'Expand all days';
});
});
window.addEventListener('resize', function () {
$$('[data-acc].is-open [data-acc-body]').forEach(function (b) { b.style.maxHeight = b.scrollHeight + 'px'; });
});
$$('[data-acc] img').forEach(function (img) {
img.addEventListener('load', function () { var it = img.closest('[data-acc]'); if (it.classList.contains('is-open')) setOpen(it, true); });
});
var tabLinks = $$('.pkg-tabs a');
if (tabLinks.length && HAS_IO) {
var spy = new IntersectionObserver(function (entries) {
entries.forEach(function (en) {
if (en.isIntersecting) tabLinks.forEach(function (a) { a.classList.toggle('is-active', a.getAttribute('href') === '#' + en.target.id); });
});
}, { rootMargin: '-45% 0px -50% 0px' });
tabLinks.forEach(function (a) { var s = $(a.getAttribute('href')); if (s) spy.observe(s); });
}
var lb = $('.lightbox');
if (lb) {
var items = $$('[data-lightbox]'), idx = 0, lastFocus = null;
var lbImg = $('img', lb), lbCap = $('.lightbox__cap', lb);
var open = function (i) {
idx = (i + items.length) % items.length;
lbImg.src = items[idx].getAttribute('data-lightbox');
lbImg.alt = items[idx].getAttribute('data-caption') || '';
lbCap.textContent = (idx + 1) + ' / ' + items.length + ' — ' + (items[idx].getAttribute('data-caption') || '');
if (!lb.classList.contains('is-open')) { lastFocus = document.activeElement; lb.classList.add('is-open'); document.body.style.overflow = 'hidden'; $('.lightbox__close', lb).focus(); }
};
var close = function () { lb.classList.remove('is-open'); document.body.style.overflow = ''; if (lastFocus) lastFocus.focus(); };
items.forEach(function (el, i) { el.addEventListener('click', function (e) { e.preventDefault(); open(i); }); });
$$('[data-lb-open]').forEach(function (b) { b.addEventListener('click', function () { open(0); }); });
$('.lightbox__close', lb).addEventListener('click', close);
$('.lightbox__prev', lb).addEventListener('click', function () { open(idx - 1); });
$('.lightbox__next', lb).addEventListener('click', function () { open(idx + 1); });
lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
document.addEventListener('keydown', function (e) {
if (!lb.classList.contains('is-open')) return;
if (e.key === 'Escape') close();
if (e.key === 'ArrowLeft') open(idx - 1);
if (e.key === 'ArrowRight') open(idx + 1);
});
}
var countUp = function (el) {
var end = +el.getAttribute('data-count'), t0 = null;
var step = function (t) {
if (!t0) t0 = t;
var p = Math.min((t - t0) / 1500, 1);
el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3)));
if (p < 1) requestAnimationFrame(step);
};
requestAnimationFrame(step);
};
if (HAS_IO) {
var io = new IntersectionObserver(function (entries) {
entries.forEach(function (en) {
if (!en.isIntersecting) return;
en.target.classList.add('is-visible');
if (en.target.hasAttribute('data-count') && !REDUCE) countUp(en.target);
io.unobserve(en.target);
});
}, { threshold: 0.08, rootMargin: '0px 0px 6% 0px' });
$$('[data-reveal], [data-count]').forEach(function (el) { io.observe(el); });
} else {
$$('[data-reveal]').forEach(function (el) { el.classList.add('is-visible'); });
}
var t = params.get('type');
if (t) {
var match = $$('.nav__link, .m-link').filter(function (a) { return a.getAttribute('href') === 'journeys.html?type=' + t; });
if (match.length) {
$$('.nav__link, .m-link').forEach(function (a) { a.classList.remove('is-active'); });
match.forEach(function (a) { a.classList.add('is-active'); });
}
}
$$('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
