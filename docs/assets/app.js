/* Color & Smile! coloring studio - tap a shape to fill it with color. */
(function () {
  const PALETTE = [
    ['Red', '#ef476f'], ['Orange', '#ff9f1c'], ['Yellow', '#ffd166'], ['Green', '#06d6a0'],
    ['Leaf', '#57cc99'], ['Sky', '#8ee3ff'], ['Blue', '#118ab2'], ['Purple', '#8338ec'],
    ['Pink', '#ffafcc'], ['Peach', '#ffd6a5'], ['Brown', '#a47148'], ['Gray', '#adb5bd'],
    ['Black', '#2b2d42'], ['White', '#ffffff'],
  ];
  const STORE = 'cas-fills-v1';

  function load() { try { return JSON.parse(localStorage.getItem(STORE)) || {}; } catch (e) { return {}; } }
  function save(d) { try { localStorage.setItem(STORE, JSON.stringify(d)); } catch (e) { /* storage off */ } }

  function Studio(root) {
    const pages = window.PAGES;
    let idx = 0, color = PALETTE[0][1], eraser = false, sound = true;
    const fills = load();
    const history = [];

    root.innerHTML = `
      <div class="st-pages" role="tablist" aria-label="Choose a picture"></div>
      <div class="st-main">
        <div class="st-board"><div class="st-art" aria-live="polite"></div></div>
        <div class="st-side">
          <div class="st-palette" role="radiogroup" aria-label="Colors"></div>
          <div class="st-tools">
            <button type="button" class="st-tool" data-act="eraser" aria-pressed="false">Eraser</button>
            <button type="button" class="st-tool" data-act="undo">Undo</button>
            <button type="button" class="st-tool" data-act="clear">Start over</button>
            <button type="button" class="st-tool" data-act="sound" aria-pressed="true">Sound on</button>
            <button type="button" class="st-tool st-dl" data-act="png">Save picture</button>
            <button type="button" class="st-tool st-dl" data-act="print">Print page</button>
          </div>
          <p class="st-hint">Tap a color, then tap any part of the picture. Try the background and the letters too!</p>
        </div>
      </div>`;

    const $pages = root.querySelector('.st-pages');
    const $art = root.querySelector('.st-art');
    const $pal = root.querySelector('.st-palette');
    if (window.IS_ARTIFACT) root.querySelectorAll('.st-dl').forEach(b => b.hidden = true);

    pages.forEach((p, i) => {
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'st-thumb'; b.setAttribute('role', 'tab');
      b.setAttribute('aria-label', p.title); b.innerHTML = p.colored + `<span>${p.title}</span>`;
      b.addEventListener('click', () => show(i));
      $pages.appendChild(b);
    });

    PALETTE.forEach(([name, hex], i) => {
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'st-swatch'; b.style.setProperty('--c', hex);
      b.setAttribute('role', 'radio'); b.setAttribute('aria-label', name); b.title = name;
      b.setAttribute('aria-checked', i === 0 ? 'true' : 'false');
      b.addEventListener('click', () => { color = hex; eraser = false; sync(); beep(520 + i * 30); });
      $pal.appendChild(b);
    });

    function sync() {
      $pal.querySelectorAll('.st-swatch').forEach(s => s.setAttribute('aria-checked', String(!eraser && s.style.getPropertyValue('--c') === color)));
      root.querySelector('[data-act=eraser]').setAttribute('aria-pressed', String(eraser));
      const sb = root.querySelector('[data-act=sound]');
      sb.setAttribute('aria-pressed', String(sound)); sb.textContent = sound ? 'Sound on' : 'Sound off';
    }

    function show(i) {
      idx = i; history.length = 0;
      $art.innerHTML = pages[i].svg;
      const f = fills[pages[i].title] || {};
      $art.querySelectorAll('.rg').forEach((el, n) => {
        const k = key(el, n);
        el.dataset.k = k;
        if (f[k]) el.setAttribute('fill', f[k]);
      });
      $pages.querySelectorAll('.st-thumb').forEach((t, n) => t.setAttribute('aria-selected', String(n === i)));
    }
    function key(el, n) { return el.classList.contains('bg') ? 'bg' : el.classList.contains('lbl') ? 'lbl' : (el.dataset.r || String(n)); }

    $art.addEventListener('click', e => {
      const el = e.target.closest('.rg'); if (!el) return;
      const next = eraser ? '#fff' : color;
      const prev = el.getAttribute('fill');
      if (prev === next) return;
      history.push([el.dataset.k, prev]);
      paint(el, next);
      beep(eraser ? 300 : 660);
    });

    function paint(el, c) {
      el.setAttribute('fill', c);
      el.classList.remove('pop'); void el.getBBox(); el.classList.add('pop');
      const t = pages[idx].title;
      fills[t] = fills[t] || {};
      fills[t][el.dataset.k] = c;
      save(fills);
    }

    root.querySelector('.st-tools').addEventListener('click', e => {
      const act = e.target.closest('button')?.dataset.act; if (!act) return;
      if (act === 'eraser') { eraser = !eraser; sync(); }
      if (act === 'sound') { sound = !sound; sync(); }
      if (act === 'undo') {
        const h = history.pop(); if (!h) return;
        const el = $art.querySelector(`.rg[data-k="${h[0]}"]`); if (el) paint(el, h[1] || '#fff');
      }
      if (act === 'clear') { delete fills[pages[idx].title]; save(fills); show(idx); }
      if (act === 'png') savePng();
      if (act === 'print') printPage();
    });

    function svgString() {
      const svg = $art.querySelector('svg').cloneNode(true);
      svg.setAttribute('width', '1200'); svg.setAttribute('height', '1600');
      return new XMLSerializer().serializeToString(svg);
    }
    function savePng() {
      const img = new Image();
      img.onload = () => {
        const c = document.createElement('canvas'); c.width = 1200; c.height = 1600;
        const g = c.getContext('2d'); g.fillStyle = '#fff'; g.fillRect(0, 0, 1200, 1600); g.drawImage(img, 0, 0);
        c.toBlob(b => {
          const a = document.createElement('a'); a.href = URL.createObjectURL(b);
          a.download = `my-${pages[idx].title.toLowerCase().replace(/\s+/g, '-')}.png`; a.click();
        });
      };
      img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svgString());
    }
    function printPage() {
      const w = window.open('', '_blank'); if (!w) return;
      w.document.write(`<title>${pages[idx].title}</title><style>@page{size:letter;margin:.5in}body{margin:0}svg{width:100%;height:auto;max-height:10in}</style>${$art.innerHTML}`);
      w.document.close(); w.focus(); setTimeout(() => w.print(), 300);
    }

    let ac = null;
    function beep(freq) {
      if (!sound) return;
      try {
        ac = ac || new (window.AudioContext || window.webkitAudioContext)();
        const o = ac.createOscillator(), g = ac.createGain();
        o.type = 'sine'; o.frequency.value = freq; o.frequency.exponentialRampToValueAtTime(freq * 1.6, ac.currentTime + 0.12);
        g.gain.setValueAtTime(0.12, ac.currentTime); g.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + 0.18);
        o.connect(g).connect(ac.destination); o.start(); o.stop(ac.currentTime + 0.2);
      } catch (e) { /* no audio */ }
    }

    const start = Number(root.dataset.start || 0);
    show(start); sync();
    return { show };
  }

  window.ColorStudio = Studio;
  document.querySelectorAll('[data-studio]').forEach(el => { el._studio = Studio(el); });
})();
