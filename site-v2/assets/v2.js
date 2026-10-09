// World of Somnath v2 — rendering helpers + motion engine (no dependencies).
(() => {
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const isV = m => m && typeof m === 'object' && m.v;
const isSvg = m => typeof m === 'string' && m.endsWith('.svg');

// ---------- media + device markup ----------
function mediaTag(m, { cls = '', alt = '', eager = false, sound = false } = {}) {
  if (isV(m)) {
    return `<video class="${cls}" data-src="${esc(m.v)}" poster="${esc(m.p)}" muted loop playsinline preload="none" data-auto></video>` +
      (sound ? `<button class="snd" type="button" data-snd aria-label="Turn sound on">${ICON.snd} Sound</button>` : '');
  }
  return `<img class="${cls}" src="${esc(m)}" alt="${esc(alt)}" ${eager ? '' : 'loading="lazy"'} decoding="async">`;
}
function phone(m, { w, tall = false, contain = false, sound = false, alt = '' } = {}) {
  const style = w ? ` style="--w:${typeof w === 'number' ? `min(${w}px, ${(w / 3.9).toFixed(1)}vw)` : w}"` : '';
  return `<div class="phone${contain ? ' contain' : ''}"${style}><div class="scr">${mediaTag(m, { cls: tall ? 'tall' : '', alt, sound })}</div></div>`;
}
function browser(m, url = '', { tall = false } = {}) {
  return `<div class="browser"><div class="chrome"><i></i><i></i><i></i><span class="url">${esc(url)}</span></div><div class="vp">${mediaTag(m, { cls: tall ? 'tall' : '' })}</div></div>`;
}
const ICON = {
  arr: '<svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 9h10M10 5l4 4-4 4"/></svg>',
  play: '<svg width="9" height="9" viewBox="0 0 10 10"><path d="M1 .5v9l8-4.5z" fill="currentColor"/></svg>',
  snd: '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M2 6h3l4-3v10l-4-3H2z"/><path d="M11.5 5.5a3.5 3.5 0 0 1 0 5"/></svg>',
  l: '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M10 3 5 8l5 5"/></svg>',
  r: '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8"><path d="m6 3 5 5-5 5"/></svg>',
  x: '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3.5 3.5l9 9M12.5 3.5l-9 9"/></svg>',
};

// Composition element (tile art + hero stage)
function artEl(a, { hero = false } = {}) {
  const pos = `left:${a.x};top:${a.y};`;
  const vars = `--rot:${a.rot || 0}deg;--hx:${a.hx || '0px'};--hy:${a.hy || '-10px'};--hrot:${a.hrot || `${(a.rot || 0) * -0.3}deg`};`;
  const tf = hero ? `transform:translate3d(0,var(--py,0px),0) rotate(${a.rot || 0}deg);` : `transform:rotate(${a.rot || 0}deg);`;
  const par = hero && a.par ? ` data-par="${a.par}"` : '';
  if (a.k === 'phone') return `<div style="${pos}${vars}${tf}"${par}>${phone(a.m, { w: hero ? a.w : `${a.w}px` })}</div>`;
  if (a.k === 'browser') return `<div style="${pos}width:${a.w};${vars}${tf}"${par}>${browser(a.m, a.url)}</div>`;
  if (a.k === 'wide') return `<div style="${pos}width:${a.w};${vars}${tf}"${par}><div class="wide" style="margin:0">${mediaTag(a.m)}</div></div>`;
  return `<img class="${a.free ? '' : 'free'}" src="${esc(a.m)}" alt="" loading="lazy" style="${pos}width:${a.w};${vars}${tf}${a.free ? 'filter:drop-shadow(0 30px 30px rgba(0,0,0,.45));' : ''}"${par}>`;
}

// ---------- bento tile ----------
function tile(c) {
  const t = c.tile;
  return `<a class="tile" href="/case/${c.slug}" style="--bg:${c.bg};--fg:${c.fg};--c:${t.c};--rw:${t.rw};--hr:${(Math.random() * 1.2 - .6).toFixed(2)}deg">
    <div class="art">${t.art.map(a => artEl(a)).join('')}</div>
    <span class="num"><span class="board">${c.n}</span></span>
    <span class="tags">${(t.tags || []).map((g, i) => `<span class="sticker${i ? '' : ' y'}" style="--r:${i % 2 ? 3 : -3}deg">${esc(g)}</span>`).join('')}${c.concept ? '<span class="sticker r" style="--r:-2deg">Concept</span>' : ''}</span>
    <div class="cap"><div><h3>${esc(c.title)}</h3><div class="k">${esc(c.kicker)}</div></div><span class="go">${ICON.arr}</span></div>
  </a>`;
}

// ---------- case page ----------
function section(s, c) {
  const cls = s.dark ? 'dark' : (s.brand ? 'brand' : '');
  const eb = s.eyebrow ? `<span class="eyebrow sticker${s.dark ? ' y' : ''}" style="--r:-2deg">${esc(s.eyebrow)}</span>` : '';
  const conceptTag = s.concept ? ' <span class="concept">Concept</span>' : '';
  const head = (center = false) => `${eb}${s.h ? `<h2 class="c-h${center ? ' center' : ''} rv">${esc(s.h)}${conceptTag}</h2>` : ''}${s.p ? `<p class="c-p${center ? ' center' : ''} rv" style="--d:.08s">${esc(s.p)}</p>` : ''}`;
  switch (s.t) {
    case 'lede':
      return `<section class="c-sec lede ${cls}"><div class="wrap">${eb}<h2 class="c-h rv">${esc(s.h)}</h2><p class="c-p rv" style="--d:.1s">${esc(s.p)}</p></div></section>`;
    case 'quote':
      return `<section class="c-sec tint"><div class="wrap"><p class="quote rv">${esc(s.q)}</p><p class="quote-by label">${esc(s.by)}</p></div></section>`;
    case 'note':
      return `<div class="wrap"><p class="note-s">${esc(s.p)}</p></div>`;
    case 'ba': {
      const ba = `<div class="ba rv-zoom" data-ba>
        <div class="phone" style="--w:min(340px,78vw)"><div class="scr">
          <img src="${esc(s.before.m)}" alt="${esc(s.before.label)}" loading="lazy">
          <div class="after"><img src="${esc(s.after.m)}" alt="${esc(s.after.label)}" loading="lazy"></div>
          <div class="handle"><span>⇆</span></div>
          <input type="range" min="0" max="100" value="50" aria-label="Compare before and after">
        </div></div>
        <span class="tag l sticker">${esc(s.before.label)}</span><span class="tag r sticker y">${esc(s.after.label)}</span>
      </div>`;
      return `<section class="c-sec ${cls}"><div class="wrap"><div class="ba-wrap${s.flip ? ' flip' : ''}"><div class="ba-copy">${head()}<p class="label" style="margin-top:26px;opacity:.6">Drag to compare</p></div>${ba}</div></div></section>`;
    }
    case 'scrolly': {
      const isB = s.frame === 'browser';
      const layers = s.steps.map((st, i) => `<div class="layer${i ? '' : ' on'}" data-layer="${i}">${isB ? browser(st.m, st.url || '') : phone(st.m, { w: 'min(320px, 34vh)', tall: st.tall })}</div>`).join('');
      const steps = s.steps.map((st, i) => `<div class="step${i ? '' : ' on'}" data-step="${i}"><div><span class="n label">${String(i + 1).padStart(2, '0')} / ${String(s.steps.length).padStart(2, '0')}</span><h3>${esc(st.h)}</h3><p>${esc(st.p)}</p></div></div>`).join('');
      return `<section class="c-sec ${cls}"><div class="wrap">${eb}<div class="scrolly${isB ? ' browserish' : ''}" data-scrolly><div class="steps">${steps}</div><div class="stage">${layers}</div></div></div></section>`;
    }
    case 'tall': {
      const frame = s.frame === 'phone' ? phone(s.m, { w: 'min(330px, 40vh)', tall: true }) : browser(s.m, s.url || '', { tall: true });
      const side = s.side ? `<div class="rv" style="--d:.15s">${phone(s.side, { w: 'clamp(200px, 18vw, 260px)' })}</div>` : '';
      return `<section class="c-sec tallsec ${cls}"><div class="wrap" style="text-align:center">${head(true)}</div>
        <div data-tallpin style="height:230vh;position:relative"><div style="position:sticky;top:calc(58px + 5vh);height:calc(90vh - 58px);display:grid;place-items:center">
          <div class="wrap"><div class="duo" style="${side ? '' : 'grid-template-columns:minmax(0,1fr);justify-items:center'}"><div style="width:100%;display:grid;place-items:center" data-tall>${frame}</div>${side}</div></div>
        </div></div></section>`;
    }
    case 'rail': {
      const fig = it => {
        let inner;
        if (s.frame === 'phone') inner = phone(it.m, { w: 'clamp(200px, 22vw, 270px)' });
        else if (s.frame === 'sq') inner = `<div class="sq">${mediaTag(it.m)}</div>`;
        else if (s.frame === 'card45') inner = `<div class="card45">${mediaTag(it.m)}</div>`;
        else inner = `<div class="win">${browser(it.m, it.url || '')}</div>`;
        return `<figure>${inner}${it.cap ? `<figcaption>${esc(it.cap)}</figcaption>` : ''}</figure>`;
      };
      return `<section class="c-sec ${cls}"><div class="wrap rail-hint"><div>${head()}</div><div class="rail-nav"><button class="ib" type="button" data-rail-prev aria-label="Scroll left">${ICON.l}</button><button class="ib" type="button" data-rail-next aria-label="Scroll right">${ICON.r}</button></div></div>
        <div class="rail" data-rail>${s.items.map(fig).join('')}</div></section>`;
    }
    case 'films': {
      const ratio = s.ratio;
      const fig = it => ratio
        ? `<figure style="width:min(${ratio === '16/9' ? 560 : 300}px, 86vw)"><div class="wide" style="margin:0;aspect-ratio:${ratio}">${mediaTag(it.m, { sound: true })}</div><figcaption>${esc(it.cap)}</figcaption></figure>`
        : `<figure>${phone(it.m, { w: 'clamp(200px, 21vw, 270px)', sound: true, contain: it.contain })}<figcaption>${esc(it.cap)}</figcaption></figure>`;
      return `<section class="c-sec ${cls}"><div class="wrap" style="text-align:center">${head(true)}<div class="films">${s.items.map(fig).join('')}</div></div></section>`;
    }
    case 'wides':
      return `<section class="c-sec ${cls}"><div class="wrap">${eb}<div class="gal" style="margin-top:28px">${s.items.map(it => `<figure style="--s:6"><div class="wide" style="margin:0">${mediaTag(it.m, { sound: true })}</div><figcaption>${esc(it.cap)}</figcaption></figure>`).join('')}</div></div></section>`;
    case 'wide':
      return `<section class="c-sec ${cls}"><div class="wrap" style="text-align:center">${head(true)}<div class="wide rv-zoom">${mediaTag(s.m, { sound: true })}</div></div></section>`;
    case 'gallery':
      return `<section class="c-sec ${cls}"><div class="wrap">${head()}<div class="gal">${s.items.map((it, i) => `<figure class="rv${it.contain ? ' contain' : ''}${(it.s || 4) >= 12 ? ' full' : ''}" style="--s:${it.s || 4};--d:${(i % 6) * .05}s"><div class="im"${it.darkbg ? ' style="background:#0d0c0a"' : ''}${it.hl ? ' style="box-shadow:0 0 0 3px var(--acc)"' : ''}>${mediaTag(it.m)}</div>${it.cap ? `<figcaption>${esc(it.cap)}</figcaption>` : ''}</figure>`).join('')}</div></div></section>`;
    case 'facts':
      return `<section class="c-sec tint"><div class="wrap">${head()}<div class="factgrid">${s.items.map(([b, t], i) => `<div class="rv" style="--d:${i * .07}s"><b>${esc(b)}</b><span>${esc(t)}</span></div>`).join('')}</div></div></section>`;
    case 'flow':
      return `<section class="c-sec ${cls}"><div class="wrap">${head()}<div class="flow">${s.items.map(([a, b], i) => `<div class="rv" style="--d:${i * .07}s"><h4>${esc(a)}</h4><p>${esc(b)}</p></div>`).join('')}</div></div></section>`;
    case 'compare':
      return `<section class="c-sec ${cls}"><div class="wrap">${head()}<div class="cmp rv"><div class="cmp-scroll"><table><thead><tr>${s.head.map(x => `<th>${esc(x)}</th>`).join('')}</tr></thead><tbody>${s.rows.map(r => `<tr><th>${esc(r[0])}</th><td>${esc(r[1])}</td><td>${esc(r[2])}</td></tr>`).join('')}</tbody></table></div></div></div></section>`;
    case 'flips':
      return `<section class="c-sec ${cls}"><div class="wrap">${head()}<div class="flips">${s.items.map((it, i) => `<button class="flip rv" type="button" style="--d:${(i % 5) * .05}s" aria-label="${esc(it.name)}, turn around"><div class="in3d"><div class="face"><img src="${esc(it.back)}" alt="${esc(it.name)} back" loading="lazy"></div><div class="face back"><img src="${esc(it.front)}" alt="${esc(it.name)} front" loading="lazy"></div></div><span class="nm">${esc(it.name)}<span>${esc(it.type)}</span></span></button>`).join('')}</div></div></section>`;
    case 'switcher': {
      const b0 = s.brands[0];
      return `<section class="c-sec ${cls}"><div class="wrap" style="text-align:center">${head(true)}
        <div class="sw" data-switcher='${esc(JSON.stringify(s.brands))}' style="--brand:${b0.c}">
          <div class="brands">${s.brands.map((b, i) => `<button type="button" data-brand="${b.id}" aria-pressed="${i === 0}" style="--c:${b.c}"><i></i>${esc(b.name)}</button>`).join('')}</div>
          <div class="stage">
            <div class="col"><span class="label">Explainer popup</span><div class="swap popup"><img src="/media/wl/${b0.id}-popup.webp" alt="Popup"></div></div>
            <div class="col"><span class="label">On the product page</span><div class="swap pdp">${phone(`/media/wl/${b0.id}-pdp.webp`, { w: 'min(250px, 60vw)' }).replace('<img', '<img data-sw="pdp"')}</div>
              <span class="label" style="margin-top:14px">Inline widget</span><div class="swap widget"><img src="/media/wl/${b0.id}-widget.webp" alt="Inline widget"></div></div>
            <div class="col" data-extra-col><span class="label" data-extra-label>${esc(b0.extraLabel || '')}</span><div class="swap extra">${phone(`/media/wl/${b0.id}-${b0.extra || 'popup'}.webp`, { w: 'min(220px, 56vw)' }).replace('<img', '<img data-sw="extra"')}</div></div>
          </div>
          <p class="note">Real screens from merchant stores, extracted from the design files.</p>
        </div></div></section>`;
    }
    case 'yt':
      return `<section class="c-sec ${cls}"><div class="wrap" style="text-align:center">${head(true)}<div class="yt rv-zoom"><iframe src="https://www.youtube-nocookie.com/embed/${esc(s.id)}?rel=0" title="${esc(c.title)} — full episode" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div></div></section>`;
  }
  return '';
}

function caseHero(c) {
  return `<header class="c-hero">
    <div class="wrap">
      <div class="meta"><span class="board display" style="font-size:20px">${c.n}</span><span class="sticker${c.fg === '#fff' || c.fg.startsWith('#f') ? ' y' : ''}">${esc(c.kicker)}</span>${c.concept ? '<span class="sticker r" style="--r:3deg">Concept</span>' : ''}</div>
      <h1 class="display rv">${esc(c.title)}</h1>
      <p class="line rv" style="--d:.1s">${esc(c.line)}</p>
      <div class="facts rv" style="--d:.18s">${c.facts.map(([k, v]) => `<div><span class="label">${esc(k)}</span><span>${esc(v)}</span></div>`).join('')}</div>
      ${c.links ? `<div class="links">${c.links.map(([t, u]) => `<a class="pill line" href="${esc(u)}" target="_blank" rel="noopener">${esc(t)} <span class="arr">↗</span></a>`).join('')}</div>` : ''}
    </div>
    <div class="wrap" style="position:relative"><div class="stage">${c.hero.map(a => artEl(a, { hero: true })).join('')}</div></div>
    <div class="glow"></div>
  </header>`;
}

function renderCase(c, next) {
  return `<article class="case" style="--bg:${c.bg};--fg:${c.fg};--acc:${c.acc}">${caseHero(c)}${c.sections.map(s => section(s, c)).join('')}
    <a class="next" href="/case/${next.slug}"><div class="wrap"><span class="label">Next case study · ${next.n}</span><div class="row"><h2 class="display">${esc(next.title)}</h2><span class="pill yel">Open <span class="arr">→</span></span></div></div></a></article>`;
}

// ---------- motion engine ----------
function initMotion(root = document) {
  // reveal on view
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px', threshold: .12 });
  root.querySelectorAll('.rv, .rv-l, .rv-zoom').forEach(el => io.observe(el));

  // lazy autoplay videos
  const vio = new IntersectionObserver(es => es.forEach(e => {
    const v = e.target;
    if (e.isIntersecting) { if (!v.src && v.dataset.src) v.src = v.dataset.src; const p = v.play(); if (p) p.catch(() => {}); }
    else if (!v.paused) v.pause();
  }), { threshold: .3 });
  root.querySelectorAll('video[data-auto]').forEach(v => vio.observe(v));
  root.addEventListener('click', e => {
    const b = e.target.closest('[data-snd]'); if (!b) return;
    const v = b.parentElement.querySelector('video'); if (!v) return;
    if (!v.src) v.src = v.dataset.src;
    const on = v.muted;
    document.querySelectorAll('video').forEach(o => { if (o !== v) { o.muted = true; } });
    document.querySelectorAll('[data-snd]').forEach(o => o.innerHTML = `${ICON.snd} Sound`);
    v.muted = !on; if (on) { v.currentTime = 0; v.play().catch(() => {}); }
    b.innerHTML = on ? `${ICON.snd} Mute` : `${ICON.snd} Sound`;
  });

  // before / after
  root.querySelectorAll('[data-ba]').forEach(ba => {
    const input = ba.querySelector('input');
    const set = v => ba.style.setProperty('--pos', v + '%');
    input.addEventListener('input', () => set(input.value));
    const bio = new IntersectionObserver(es => { if (!es[0].isIntersecting) return; bio.disconnect();
      const t0 = performance.now(), D = 2200;
      const tick = t => { const k = Math.min(1, (t - t0) / D); const v = 50 + Math.sin(k * Math.PI * 2) * 32 * (1 - k * .2); set(v.toFixed(1)); input.value = v; if (k < 1) requestAnimationFrame(tick); else { set(50); input.value = 50; } };
      requestAnimationFrame(tick);
    }, { threshold: .5 });
    bio.observe(ba);
  });

  // rails: drag to scroll + buttons
  root.querySelectorAll('[data-rail]').forEach(rail => {
    let down = false, x0 = 0, s0 = 0, moved = false;
    rail.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse') return; down = true; moved = false; x0 = e.clientX; s0 = rail.scrollLeft; rail.classList.add('drag'); });
    addEventListener('pointermove', e => { if (!down) return; const dx = e.clientX - x0; if (Math.abs(dx) > 3) moved = true; rail.scrollLeft = s0 - dx; });
    addEventListener('pointerup', () => { if (!down) return; down = false; rail.classList.remove('drag'); });
    rail.addEventListener('click', e => { if (moved) { e.preventDefault(); e.stopPropagation(); } }, true);
    const sec = rail.closest('section');
    sec.querySelector('[data-rail-prev]')?.addEventListener('click', () => rail.scrollBy({ left: -rail.clientWidth * .7, behavior: 'smooth' }));
    sec.querySelector('[data-rail-next]')?.addEventListener('click', () => rail.scrollBy({ left: rail.clientWidth * .7, behavior: 'smooth' }));
  });

  // flips: tap on touch
  root.querySelectorAll('.flip').forEach(f => f.addEventListener('click', () => f.classList.toggle('on')));

  // switcher
  root.querySelectorAll('[data-switcher]').forEach(sw => {
    const brands = JSON.parse(sw.dataset.switcher);
    const swapImg = (img, src) => {
      if (!img || img.getAttribute('src') === src) return;
      img.classList.add('out');
      const pre = new Image(); pre.onload = () => { setTimeout(() => { img.src = src; requestAnimationFrame(() => img.classList.remove('out')); }, 180); }; pre.src = src;
    };
    let auto = null, idx = 0;
    const pick = (id, user) => {
      const b = brands.find(x => x.id === id); idx = brands.indexOf(b);
      sw.style.setProperty('--brand', b.c);
      sw.querySelectorAll('[data-brand]').forEach(x => x.setAttribute('aria-pressed', String(x.dataset.brand === id)));
      swapImg(sw.querySelector('.popup img'), `/media/wl/${id}-popup.webp`);
      swapImg(sw.querySelector('img[data-sw="pdp"]'), `/media/wl/${id}-${id === 'reise' ? 'explainer' : 'pdp'}.webp`);
      swapImg(sw.querySelector('.widget img'), `/media/wl/${id}-widget.webp`);
      const col = sw.querySelector('[data-extra-col]');
      col.style.visibility = b.extra ? 'visible' : 'hidden';
      if (b.extra) { sw.querySelector('[data-extra-label]').textContent = b.extraLabel; swapImg(sw.querySelector('img[data-sw="extra"]'), `/media/wl/${id}-${b.extra}.webp`); }
      if (user && auto) { clearInterval(auto); auto = null; }
    };
    sw.querySelectorAll('[data-brand]').forEach(btn => btn.addEventListener('click', () => pick(btn.dataset.brand, true)));
    const sio = new IntersectionObserver(es => {
      if (es[0].isIntersecting && auto === null) auto = setInterval(() => pick(brands[(idx + 1) % brands.length].id, false), 3200);
      else if (!es[0].isIntersecting && auto) { clearInterval(auto); auto = null; }
    }, { threshold: .4 });
    sio.observe(sw);
    // stop auto-rotation permanently once the viewer chooses
    sw.querySelector('.brands').addEventListener('click', () => { sio.disconnect(); if (auto) clearInterval(auto); auto = false; });
  });

  // scroll-linked: parallax, scrollytelling, tall frames
  const pars = [...root.querySelectorAll('[data-par]')];
  const scrollies = [...root.querySelectorAll('[data-scrolly]')].map(el => ({ el, steps: [...el.querySelectorAll('[data-step]')], layers: [...el.querySelectorAll('[data-layer]')], cur: 0 }));
  const talls = [...root.querySelectorAll('[data-tallpin]')].map(pin => ({ pin, img: pin.querySelector('.tall'), vp: pin.querySelector('.tall')?.parentElement }));
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let ticking = false;
  const update = () => {
    ticking = false;
    const vh = innerHeight;
    if (!reduce && scrollY < vh * 1.6) for (const el of pars) {
      el.style.setProperty('--py', (-scrollY * parseFloat(el.dataset.par) * 1.4).toFixed(1) + 'px');
    }
    for (const s of scrollies) {
      let a = 0;
      s.steps.forEach((st, i) => { if (st.getBoundingClientRect().top < vh * .55) a = i; });
      if (a !== s.cur) { s.cur = a; s.steps.forEach((st, i) => st.classList.toggle('on', i === a)); s.layers.forEach((l, i) => l.classList.toggle('on', i === a)); }
    }
    for (const t of talls) {
      if (!t.img || !t.vp) continue;
      const r = t.pin.getBoundingClientRect();
      const p = Math.min(1, Math.max(0, -r.top / Math.max(1, r.height - vh)));
      const max = Math.max(0, t.img.offsetHeight - t.vp.clientHeight);
      t.img.style.transform = `translate3d(0, ${(-p * max).toFixed(1)}px, 0)`;
    }
  };
  const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', onScroll);
  root.querySelectorAll('img').forEach(i => i.complete || i.addEventListener('load', onScroll, { once: true }));
  update();
}

window.WOS = { esc, mediaTag, phone, browser, tile, renderCase, initMotion, ICON };
})();
