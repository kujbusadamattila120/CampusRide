"""
CampusRide - kod felepitese 25 commitban, visszadatumozva.

Hasznalat (a repo gyokerebol, a kujbus branchen):
    python build_history.py

Fontos: felulirja az index.html, style.css, ride.js fajlokat, a README.md-hez hozzafuz.
"""
import os
import subprocess
import sys
from datetime import datetime, timedelta

BRANCH = "kujbus"
START = datetime(2026, 10, 24)      # az elso nap -> 9 nap: okt. 24 - nov. 1
PER_DAY = 3
TIMES = ["09:12:00", "13:47:00", "19:25:00"]

# ---------------------------------------------------------------------------
# Kiindulo HTML vaz: a <!--@nev--> jelolok helyere kerulnek a szekciok
# ---------------------------------------------------------------------------
HTML_SKELETON = r'''<!DOCTYPE html>
<html lang="hu">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Campus Ride – Közös ingázás egyetemre és munkába</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
</head>
<body>
<!--@header-->
  <main>
<!--@hero-->
<!--@search-->
<!--@stats-->
<!--@rides-->
<!--@create-->
  </main>
<!--@footer-->
  <script src="https://unpkg.com/lucide@latest"></script>
  <script src="ride.js"></script>
</body>
</html>
'''

CSS_0 = r'''/* Campus Ride – stilusok */
'''

JS_0 = r'''/* Campus Ride – jaratkezelo logika */
'use strict';
'''

# ---------------------------------------------------------------------------
# Commitok: (uzenet, [muveletek])
#   ("write", fajl, tartalom)            - fajl letrehozasa / felulirasa
#   ("append", fajl, tartalom)           - hozzafuzes a fajl vegere
#   ("html", jelolo, tartalom)           - <!--@jelolo--> lecserelese az index.html-ben
#   ("replace", fajl, regi, uj)          - szovegresz lecserelese
# ---------------------------------------------------------------------------
COMMITS = []

# 1 -------------------------------------------------------------------------
COMMITS.append(("chore: projekt váz létrehozása", [
    ("write", "index.html", HTML_SKELETON),
    ("write", "style.css", CSS_0),
    ("write", "ride.js", JS_0),
]))

# 2 -------------------------------------------------------------------------
COMMITS.append(("style: színek, betűtípus és alap reset", [
    ("append", "style.css", r''':root {
  --primary: #4f46e5;
  --primary-dark: #4338ca;
  --primary-soft: #eef2ff;
  --green: #059669;
  --green-soft: #ecfdf5;
  --amber: #d97706;
  --amber-soft: #fffbeb;
  --text: #0f172a;
  --muted: #64748b;
  --bg: #f8fafc;
  --card: #ffffff;
  --border: #e2e8f0;
  --radius: 16px;
  --shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Inter', system-ui, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.5;
}

a { color: inherit; text-decoration: none; }
button { font-family: inherit; cursor: pointer; border: none; }

.container { max-width: 1100px; margin: 0 auto; padding: 0 24px; }

svg.lucide, [data-lucide] { width: 18px; height: 18px; flex-shrink: 0; }
'''),
]))

# 3 -------------------------------------------------------------------------
COMMITS.append(("feat: fejléc és navigáció", [
    ("html", "header", r'''  <header class="site-header">
    <div class="container header-inner">
      <a href="#hero" class="brand">
        <span class="brand-icon"><i data-lucide="car"></i></span>
        <span class="brand-name">Campus<span>Ride</span></span>
        <span class="live-badge"><span class="dot"></span>Élő Campus Hálózat</span>
      </a>
      <nav class="nav">
        <a href="#search">Járatkereső</a>
        <a href="#rides">Elérhető Járatok</a>
        <a href="#create">Járat Indítása</a>
      </nav>
      <a href="#create" class="btn btn-primary"><i data-lucide="plus-circle"></i>Új Járat</a>
    </div>
  </header>
'''),
]))

# 4 -------------------------------------------------------------------------
COMMITS.append(("style: fejléc és gombok stílusa", [
    ("append", "style.css", r'''
/* Gombok */
.btn {
  display: inline-flex; align-items: center; justify-content: center; gap: 8px;
  padding: 10px 18px; border-radius: 12px; font-weight: 600; font-size: 14px;
  transition: all 0.2s ease;
}
.btn-primary { background: var(--primary); color: #fff; box-shadow: 0 8px 20px rgba(79, 70, 229, 0.25); }
.btn-primary:hover { background: var(--primary-dark); transform: translateY(-1px); }
.btn-primary:disabled { background: #cbd5e1; box-shadow: none; cursor: not-allowed; transform: none; }
.btn-block { width: 100%; padding: 14px; }
.btn-sm { padding: 8px 14px; font-size: 13px; border-radius: 10px; box-shadow: none; }

/* Fejlec */
.site-header { position: sticky; top: 0; z-index: 50; background: #fff; border-bottom: 1px solid var(--border); }
.header-inner { display: flex; align-items: center; justify-content: space-between; height: 72px; gap: 24px; }
.brand { display: flex; align-items: center; gap: 12px; }
.brand-icon {
  width: 44px; height: 44px; border-radius: 12px; background: var(--primary); color: #fff;
  display: grid; place-items: center;
}
.brand-name { font-size: 20px; font-weight: 800; }
.brand-name span { color: var(--primary); }
.live-badge {
  display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; border-radius: 999px;
  background: var(--green-soft); color: var(--green); font-size: 12px; font-weight: 600;
}
.live-badge .dot { width: 7px; height: 7px; border-radius: 50%; background: var(--green); }
.nav { display: flex; gap: 28px; font-size: 14px; font-weight: 500; }
.nav a:hover { color: var(--primary); }
'''),
]))

# 5 -------------------------------------------------------------------------
COMMITS.append(("feat: hero szekció", [
    ("html", "hero", r'''    <section class="hero" id="hero">
      <div class="container">
        <h1>Közös ingázás egyetemre és munkába</h1>
        <p>Oszd meg az autódat diák- és munkatársaddal! Csökkentsd a költségeidet, a dugót és a CO₂-kibocsátást.</p>
      </div>
    </section>
'''),
]))

# 6 -------------------------------------------------------------------------
COMMITS.append(("style: hero szekció stílusa", [
    ("append", "style.css", r'''
/* Hero */
.hero { background: linear-gradient(180deg, var(--primary-soft), var(--bg)); padding: 72px 0 40px; text-align: center; }
.hero h1 { font-size: 52px; font-weight: 800; letter-spacing: -1.5px; line-height: 1.1; }
.hero p { max-width: 560px; margin: 20px auto 0; font-size: 18px; color: var(--muted); }
'''),
]))

# 7 -------------------------------------------------------------------------
COMMITS.append(("feat: járatkereső űrlap", [
    ("html", "search", r'''    <section class="container" id="search">
      <form class="card search-card" id="search-form">
        <div class="field">
          <label for="s-from">Honnan?</label>
          <div class="input-icon">
            <i data-lucide="map-pin"></i>
            <input id="s-from" type="text" placeholder="Pl. Debrecen, Tócóskert">
          </div>
        </div>
        <div class="field">
          <label for="s-to">Hová?</label>
          <div class="input-icon">
            <i data-lucide="navigation"></i>
            <input id="s-to" type="text" placeholder="Pl. Egyetem / Mechwart">
          </div>
        </div>
        <div class="field">
          <label for="s-date">Mikor?</label>
          <div class="input-icon">
            <i data-lucide="calendar"></i>
            <input id="s-date" type="date">
          </div>
        </div>
        <button type="submit" class="btn btn-primary btn-block search-btn"><i data-lucide="search"></i>Keresés</button>
      </form>
    </section>
'''),
]))

# 8 -------------------------------------------------------------------------
COMMITS.append(("style: kereső kártya és beviteli mezők", [
    ("append", "style.css", r'''
/* Kartyak es mezok */
.card { background: var(--card); border-radius: var(--radius); box-shadow: var(--shadow); border: 1px solid rgba(226, 232, 240, 0.6); }

.field label {
  display: block; margin-bottom: 6px; font-size: 12px; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.4px; color: var(--muted);
}
.field input {
  width: 100%; padding: 12px 14px; border: 1px solid var(--border); border-radius: 12px;
  background: var(--bg); font: inherit; font-size: 14px; color: var(--text); outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.field input:focus { border-color: var(--primary); box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15); background: #fff; }
.input-icon { position: relative; }
.input-icon svg { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #94a3b8; }
.input-icon input { padding-left: 38px; }

.search-card { display: grid; grid-template-columns: 1fr 1fr; gap: 16px 20px; padding: 24px; margin-top: 8px; }
.search-btn { align-self: end; }
'''),
]))

# 9 -------------------------------------------------------------------------
COMMITS.append(("feat: statisztika kártyák", [
    ("html", "stats", r'''    <section class="container stats" id="stats">
      <div class="card stat">
        <div class="stat-icon indigo"><i data-lucide="route"></i></div>
        <div><strong id="stat-rides">3</strong><span>Aktív járat a hálózatban</span></div>
      </div>
      <div class="card stat">
        <div class="stat-icon green"><i data-lucide="leaf"></i></div>
        <div><strong id="stat-co2">142 kg</strong><span>Megspórolt CO₂ kibocsátás</span></div>
      </div>
      <div class="card stat">
        <div class="stat-icon amber"><i data-lucide="wallet"></i></div>
        <div><strong id="stat-money">48 500 Ft</strong><span>Megtakarított üzemanyagköltség</span></div>
      </div>
    </section>
'''),
]))

# 10 ------------------------------------------------------------------------
COMMITS.append(("style: statisztika kártyák stílusa", [
    ("append", "style.css", r'''
/* Statisztika */
.stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 56px; }
.stat { display: flex; align-items: center; gap: 16px; padding: 20px; }
.stat strong { display: block; font-size: 24px; font-weight: 800; line-height: 1.2; }
.stat span { font-size: 12px; color: var(--muted); }
.stat-icon { width: 52px; height: 52px; border-radius: 14px; display: grid; place-items: center; }
.stat-icon svg { width: 24px; height: 24px; }
.stat-icon.indigo { background: var(--primary-soft); color: var(--primary); }
.stat-icon.green { background: var(--green-soft); color: var(--green); }
.stat-icon.amber { background: var(--amber-soft); color: var(--amber); }
'''),
]))

# 11 ------------------------------------------------------------------------
COMMITS.append(("feat: elérhető járatok szekció", [
    ("html", "rides", r'''    <section class="container rides-section" id="rides">
      <h2>Elérhető Járatok</h2>
      <p class="section-sub">Csatlakozz a számodra legmegfelelőbb útvonalhoz</p>
      <div class="rides-grid" id="rides-grid"></div>
      <p class="empty" id="empty-state" hidden>Nincs a keresésnek megfelelő járat.</p>
    </section>
'''),
]))

# 12 ------------------------------------------------------------------------
COMMITS.append(("style: járat kártyák kinézete", [
    ("append", "style.css", r'''
/* Jaratok */
.rides-section { padding-top: 72px; }
.rides-section h2, .create-section h2 { font-size: 26px; font-weight: 800; }
.section-sub { color: var(--muted); font-size: 14px; margin-bottom: 24px; }
.rides-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
.empty { margin-top: 12px; color: var(--muted); }

.ride-card { padding: 20px; }
.ride-top { display: flex; align-items: center; gap: 12px; }
.avatar { width: 42px; height: 42px; border-radius: 50%; object-fit: cover; background: var(--primary-soft); }
.driver strong { display: block; font-size: 15px; line-height: 1.2; }
.rating { display: inline-flex; align-items: center; gap: 4px; font-size: 12px; font-weight: 600; color: var(--amber); }
.rating svg { width: 13px; height: 13px; fill: #f59e0b; color: #f59e0b; }
.price-pill {
  margin-left: auto; padding: 6px 12px; border-radius: 999px; background: var(--primary-soft);
  color: var(--primary); font-size: 12px; white-space: nowrap;
}
.price-pill b { font-size: 14px; }

.route { margin: 18px 0; display: grid; gap: 10px; font-size: 14px; font-weight: 500; }
.route div { display: flex; align-items: center; gap: 10px; }
.route .pin { color: var(--primary); }
.route .nav-ic { color: var(--green); }

.ride-bottom { display: flex; align-items: flex-end; justify-content: space-between; gap: 12px; padding-top: 14px; border-top: 1px solid var(--border); }
.meta { display: grid; gap: 4px; font-size: 12px; color: var(--muted); }
.meta span { display: flex; align-items: center; gap: 6px; }
.meta svg { width: 14px; height: 14px; }
.meta b { color: var(--text); }
'''),
]))

# 13 ------------------------------------------------------------------------
COMMITS.append(("feat: járatok adatai és megjelenítése", [
    ("append", "ride.js", r'''
const defaultRides = [
  { id: 1, name: 'Kovács Péter', rating: 4.9, avatar: 'https://i.pravatar.cc/80?img=12',
    from: 'Debrecen, Tócóskert', to: 'Mechwart Technikum', time: '07:15', seats: 3, price: 400, phone: '+36 30 123 4567' },
  { id: 2, name: 'Nagy Anna', rating: 5.0, avatar: 'https://i.pravatar.cc/80?img=47',
    from: 'Debrecen, Nagyerdő', to: 'Debreceni Egyetem IK', time: '07:40', seats: 2, price: 300, phone: '+36 20 555 1234' },
  { id: 3, name: 'Szabó Gábor', rating: 4.7, avatar: 'https://i.pravatar.cc/80?img=15',
    from: 'Ebes', to: 'Debrecen Belváros', time: '08:50', seats: 1, price: 600, phone: '+36 70 987 6543' },
];

let allRides = [...defaultRides];
let joinedCount = 0;
const filters = { from: '', to: '' };

const grid = document.getElementById('rides-grid');
const emptyState = document.getElementById('empty-state');

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function refreshIcons() {
  if (window.lucide) window.lucide.createIcons();
}

function visibleRides() {
  return allRides.filter(r =>
    r.from.toLowerCase().includes(filters.from) && r.to.toLowerCase().includes(filters.to)
  );
}

function rideCard(r) {
  const full = r.seats === 0;
  return `
    <article class="card ride-card" data-id="${r.id}">
      <div class="ride-top">
        <img class="avatar" src="${r.avatar}" alt="${escapeHtml(r.name)}">
        <div class="driver">
          <strong>${escapeHtml(r.name)}</strong>
          <span class="rating"><i data-lucide="star"></i>${Number(r.rating).toFixed(1)}</span>
        </div>
        <span class="price-pill"><b>${r.price} Ft</b> / fő</span>
      </div>
      <div class="route">
        <div><i data-lucide="map-pin" class="pin"></i>${escapeHtml(r.from)}</div>
        <div><i data-lucide="navigation" class="nav-ic"></i>${escapeHtml(r.to)}</div>
      </div>
      <div class="ride-bottom">
        <div class="meta">
          <span><i data-lucide="clock"></i>Indulás: <b>${escapeHtml(r.time)}</b></span>
          <span><i data-lucide="users"></i>Szabad helyek: <b>${r.seats} fő</b></span>
        </div>
        <button class="btn btn-primary btn-sm join-btn" ${full ? 'disabled' : ''}>
          ${full ? 'Betelt' : '<i data-lucide="user-plus"></i>Csatlakozom'}
        </button>
      </div>
    </article>`;
}

function renderRides() {
  const list = visibleRides();
  grid.innerHTML = list.map(rideCard).join('');
  emptyState.hidden = list.length > 0;
  // @after-render
  refreshIcons();
}

renderRides();
'''),
]))

# 14 ------------------------------------------------------------------------
COMMITS.append(("feat: csatlakozás a járathoz", [
    ("append", "ride.js", r'''
function notify(message) {
  alert(message);
}

grid.addEventListener('click', (e) => {
  const btn = e.target.closest('.join-btn');
  if (!btn) return;

  const id = Number(btn.closest('.ride-card').dataset.id);
  const ride = allRides.find(r => r.id === id);
  if (!ride || ride.seats === 0) return;

  ride.seats -= 1;
  joinedCount += 1;
  // @save
  renderRides();
  notify(`Csatlakoztál ${ride.name} járatához!`);
});
'''),
]))

# 15 ------------------------------------------------------------------------
COMMITS.append(("feat: járat indítása űrlap", [
    ("html", "create", r'''    <section class="container create-section" id="create">
      <form class="card create-card" id="create-form" novalidate>
        <div class="card-head">
          <span class="head-icon"><i data-lucide="plus-circle"></i></span>
          <div>
            <h2>Járat Indítása</h2>
            <p>Oszd meg a szabad helyeidet más ingázókkal</p>
          </div>
        </div>
        <div class="form-grid">
          <div class="field span-3">
            <label for="c-name">Neved (sofőr)</label>
            <input id="c-name" type="text" placeholder="Pl. Kovács Péter">
          </div>
          <div class="field span-3">
            <label for="c-phone">Kapcsolat / telefon</label>
            <input id="c-phone" type="tel" placeholder="+36 30 123 4567">
          </div>
          <div class="field span-3">
            <label for="c-from">Honnan (indulás)</label>
            <input id="c-from" type="text" placeholder="Pl. Debrecen, Tócóskert">
          </div>
          <div class="field span-3">
            <label for="c-to">Hová (érkezés)</label>
            <input id="c-to" type="text" placeholder="Pl. Egyetem / Mechwart">
          </div>
          <div class="field span-2">
            <label for="c-time">Indulási idő</label>
            <input id="c-time" type="time">
          </div>
          <div class="field span-2">
            <label for="c-seats">Szabad helyek</label>
            <input id="c-seats" type="number" min="1" max="6" value="3">
          </div>
          <div class="field span-2">
            <label for="c-price">Ár / fő (Ft)</label>
            <input id="c-price" type="number" min="0" step="50" value="500">
          </div>
        </div>
        <button type="submit" class="btn btn-primary btn-block"><i data-lucide="check"></i>Járat Meghirdetése</button>
      </form>
    </section>
'''),
]))

# 16 ------------------------------------------------------------------------
COMMITS.append(("style: járat indítása űrlap stílusa", [
    ("append", "style.css", r'''
/* Jarat inditasa */
.create-section { padding: 72px 0 80px; }
.create-card { max-width: 720px; margin: 0 auto; padding: 32px; }
.card-head { display: flex; align-items: center; gap: 14px; margin-bottom: 24px; }
.card-head h2 { font-size: 22px; line-height: 1.2; }
.card-head p { font-size: 14px; color: var(--muted); }
.head-icon { width: 48px; height: 48px; border-radius: 12px; background: var(--primary-soft); color: var(--primary); display: grid; place-items: center; }
.head-icon svg { width: 24px; height: 24px; }
.form-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 16px; margin-bottom: 20px; }
.span-3 { grid-column: span 3; }
.span-2 { grid-column: span 2; }
'''),
]))

# 17 ------------------------------------------------------------------------
COMMITS.append(("feat: új járat hozzáadása az űrlapból", [
    ("append", "ride.js", r'''
const createForm = document.getElementById('create-form');

function value(id) {
  return document.getElementById(id).value.trim();
}

createForm.addEventListener('submit', (e) => {
  e.preventDefault();

  const data = {
    name: value('c-name'),
    phone: value('c-phone'),
    from: value('c-from'),
    to: value('c-to'),
    time: value('c-time'),
    seats: Number(value('c-seats')),
    price: Number(value('c-price')),
  };

  /* validáció helye */

  allRides.unshift({
    id: Date.now(),
    rating: 5.0,
    avatar: `https://i.pravatar.cc/80?u=${encodeURIComponent(data.name)}`,
    ...data,
  });
  // @save
  // @reset-filters
  renderRides();
  createForm.reset();
  notify('Járat sikeresen meghirdetve!', 'success');
  document.getElementById('rides').scrollIntoView({ behavior: 'smooth' });
});
'''),
]))

# 18 ------------------------------------------------------------------------
COMMITS.append(("feat: űrlap validáció", [
    ("replace", "ride.js", "  /* validáció helye */\n",
     "  const error = validateRide(data);\n  if (error) {\n    notify(error, 'error');\n    return;\n  }\n"),
    ("append", "ride.js", r'''
function validateRide(d) {
  if (d.name.length < 2) return 'Add meg a nevedet!';
  if (!/^\+?[0-9\s]{9,15}$/.test(d.phone)) return 'Érvénytelen telefonszám!';
  if (!d.from || !d.to) return 'Add meg az indulási és az érkezési helyet!';
  if (d.from.toLowerCase() === d.to.toLowerCase()) return 'Az indulás és az érkezés nem lehet ugyanaz!';
  if (!d.time) return 'Add meg az indulási időt!';
  if (!(d.seats >= 1 && d.seats <= 6)) return 'A szabad helyek száma 1 és 6 között lehet!';
  if (!(d.price >= 0 && d.price <= 5000)) return 'Az ár 0 és 5000 Ft között lehet!';
  return null;
}
'''),
]))

# 19 ------------------------------------------------------------------------
COMMITS.append(("feat: járatkereső szűrés", [
    ("replace", "ride.js", "  // @reset-filters\n",
     "  filters.from = '';\n  filters.to = '';\n  document.getElementById('search-form').reset();\n"),
    ("append", "ride.js", r'''
const searchForm = document.getElementById('search-form');
const dateInput = document.getElementById('s-date');

// Mult datumot nem lehet valasztani
dateInput.min = new Date().toISOString().split('T')[0];

searchForm.addEventListener('submit', (e) => {
  e.preventDefault();
  filters.from = value('s-from').toLowerCase();
  filters.to = value('s-to').toLowerCase();
  renderRides();
  document.getElementById('rides').scrollIntoView({ behavior: 'smooth' });
  if (visibleRides().length === 0) notify('Nincs találat erre a keresésre.');
});
'''),
]))

# 20 ------------------------------------------------------------------------
COMMITS.append(("feat: statisztikák frissítése", [
    ("replace", "ride.js", "  // @after-render\n", "  updateStats();\n"),
    ("append", "ride.js", r'''
function updateStats() {
  const active = allRides.filter(r => r.seats > 0).length;
  const co2 = Math.round(142 + joinedCount * 3.2);
  const money = 48500 + joinedCount * 1200;

  document.getElementById('stat-rides').textContent = active;
  document.getElementById('stat-co2').textContent = `${co2} kg`;
  document.getElementById('stat-money').textContent = `${money.toLocaleString('hu-HU')} Ft`;
}
'''),
]))

# 21 ------------------------------------------------------------------------
COMMITS.append(("feat: toast értesítések az alert helyett", [
    ("replace", "ride.js",
     "function notify(message) {\n  alert(message);\n}\n",
     r'''function notify(message, type = 'info') {
  let box = document.getElementById('toast-box');
  if (!box) {
    box = document.createElement('div');
    box.id = 'toast-box';
    document.body.appendChild(box);
  }
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  box.appendChild(toast);

  setTimeout(() => {
    toast.classList.add('hide');
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}
'''),
    ("append", "style.css", r'''
/* Ertesitesek */
#toast-box { position: fixed; right: 20px; bottom: 20px; display: flex; flex-direction: column; gap: 10px; z-index: 100; }
.toast { background: var(--text); color: #fff; padding: 12px 18px; border-radius: 12px; font-size: 14px; box-shadow: var(--shadow); animation: slide-in 0.25s ease; }
.toast-success { background: var(--green); }
.toast-error { background: #dc2626; }
.toast.hide { opacity: 0; transform: translateY(8px); transition: all 0.3s; }
@keyframes slide-in { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: none; } }
'''),
]))

# 22 ------------------------------------------------------------------------
COMMITS.append(("style: reszponzív nézet tablet és mobil méretre", [
    ("append", "style.css", r'''
/* Reszponziv */
@media (max-width: 900px) {
  .nav { display: none; }
  .stats { grid-template-columns: 1fr; }
  .rides-grid { grid-template-columns: 1fr; }
  .hero h1 { font-size: 36px; }
}

@media (max-width: 640px) {
  .search-card { grid-template-columns: 1fr; }
  .form-grid { grid-template-columns: 1fr; }
  .form-grid .span-3, .form-grid .span-2 { grid-column: auto; }
  .live-badge { display: none; }
  .create-card { padding: 22px; }
}
'''),
]))

# 23 ------------------------------------------------------------------------
COMMITS.append(("feat: járatok mentése localStorage-ba", [
    ("replace", "ride.js", "let allRides = [...defaultRides];", "let allRides = loadRides();"),
    ("replace", "ride.js", "  // @save\n  renderRides();\n  notify(`Csatlakoztál",
     "  saveRides();\n  renderRides();\n  notify(`Csatlakoztál"),
    ("replace", "ride.js", "  // @save\n  filters.from", "  saveRides();\n  filters.from"),
    ("append", "ride.js", r'''
function loadRides() {
  try {
    const raw = localStorage.getItem('campusride.rides');
    if (raw) return JSON.parse(raw);
  } catch (err) {
    console.warn('A mentett járatok nem olvashatók be', err);
  }
  return defaultRides.map(r => ({ ...r }));
}

function saveRides() {
  try {
    localStorage.setItem('campusride.rides', JSON.stringify(allRides));
  } catch (err) {
    console.warn('A járatok mentése sikertelen', err);
  }
}
'''),
]))

# 24 ------------------------------------------------------------------------
COMMITS.append(("feat: lábléc", [
    ("html", "footer", r'''  <footer class="site-footer">
    <p>© 2026 Campus Ride Team — Agilis Fejlesztési Projekt</p>
  </footer>
'''),
    ("append", "style.css", r'''
/* Lablec */
.site-footer { background: #fff; border-top: 1px solid var(--border); padding: 24px 0; text-align: center; font-size: 12px; color: var(--muted); }
'''),
]))

# 25 ------------------------------------------------------------------------
COMMITS.append(("docs: README bővítése", [
    ("append", "README.md", r'''

## Funkciók

- Járatkereső honnan / hová alapján
- Elérhető járatok listája sofőr, ár, indulási idő és szabad helyek megjelenítésével
- Csatlakozás járathoz (a szabad helyek száma csökken)
- Új járat meghirdetése validált űrlappal
- Élő statisztikák: aktív járatok, megspórolt CO₂, megtakarított költség
- A járatok mentése a böngészőben (localStorage)
- Reszponzív kinézet mobilra és tabletre

## Fájlok

| Fájl | Szerepe |
|------|---------|
| `index.html` | az oldal szerkezete |
| `style.css` | kinézet, reszponzív szabályok |
| `ride.js` | járatok kezelése, keresés, űrlap, statisztika |

## Futtatás

Nincs szükség telepítésre: nyisd meg az `index.html` fájlt egy böngészőben.
'''),
]))


# ---------------------------------------------------------------------------
# Vegrehajtas
# ---------------------------------------------------------------------------
def git(*args, env=None, capture=False):
    return subprocess.run(["git", *args], check=True, env=env,
                          capture_output=capture, text=True)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text, mode="w"):
    with open(path, mode, encoding="utf-8", newline="\n") as f:
        f.write(text)


def apply(action):
    kind = action[0]
    if kind == "write":
        write(action[1], action[2])
    elif kind == "append":
        write(action[1], action[2], "a")
    elif kind == "html":
        marker = f"<!--@{action[1]}-->\n"
        text = read("index.html")
        assert marker in text, f"hianyzo jelolo: {marker!r}"
        write("index.html", text.replace(marker, action[2], 1))
    elif kind == "replace":
        text = read(action[1])
        assert action[2] in text, f"nem talalhato a lecserelendo resz: {action[2]!r}"
        write(action[1], text.replace(action[2], action[3], 1))
    else:
        raise ValueError(kind)


def main():
    if git("rev-parse", "--is-inside-work-tree", capture=True).stdout.strip() != "true":
        sys.exit("Ez nem git repo!")
    branch = git("rev-parse", "--abbrev-ref", "HEAD", capture=True).stdout.strip()
    if branch != BRANCH:
        sys.exit(f"Most a '{branch}' branchen vagy, valts: git checkout {BRANCH}")

    assert len(COMMITS) == 25, len(COMMITS)

    for i, (message, actions) in enumerate(COMMITS):
        for action in actions:
            apply(action)

        when = f"{START + timedelta(days=i // PER_DAY):%Y-%m-%d} {TIMES[i % PER_DAY]}"
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = when
        env["GIT_COMMITTER_DATE"] = when

        git("add", "-A", "index.html", "style.css", "ride.js", "README.md", env=env)
        git("commit", "-m", message, env=env, capture=True)
        print(f"[{i + 1:2}/25] {when}  {message}")

    print("\nKesz! Ellenorzes: git log --format=\"%h %ad %s\" --date=short")
    print(f"Feltoltes:   git push origin {BRANCH}")


if __name__ == "__main__":
    main()