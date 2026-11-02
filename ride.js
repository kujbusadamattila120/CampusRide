/* Campus Ride – jaratkezelo logika */
'use strict';

const defaultRides = [
  { id: 1, name: 'Kovács Péter', rating: 4.9, avatar: 'https://i.pravatar.cc/80?img=12',
    from: 'Debrecen, Tócóskert', to: 'Mechwart Technikum', time: '07:15', seats: 3, price: 400, phone: '+36 30 123 4567' },
  { id: 2, name: 'Nagy Anna', rating: 5.0, avatar: 'https://i.pravatar.cc/80?img=47',
    from: 'Debrecen, Nagyerdő', to: 'Debreceni Egyetem IK', time: '07:40', seats: 2, price: 300, phone: '+36 20 555 1234' },
  { id: 3, name: 'Szabó Gábor', rating: 4.7, avatar: 'https://i.pravatar.cc/80?img=15',
    from: 'Ebes', to: 'Debrecen Belváros', time: '08:50', seats: 1, price: 600, phone: '+36 70 987 6543' },
];

let allRides = loadRides();
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
  updateStats();
  refreshIcons();
}

renderRides();

function notify(message, type = 'info') {
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

grid.addEventListener('click', (e) => {
  const btn = e.target.closest('.join-btn');
  if (!btn) return;

  const id = Number(btn.closest('.ride-card').dataset.id);
  const ride = allRides.find(r => r.id === id);
  if (!ride || ride.seats === 0) return;

  ride.seats -= 1;
  joinedCount += 1;
  saveRides();
  renderRides();
  notify(`Csatlakoztál ${ride.name} járatához!`);
});

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

  const error = validateRide(data);
  if (error) {
    notify(error, 'error');
    return;
  }

  allRides.unshift({
    id: Date.now(),
    rating: 5.0,
    avatar: `https://i.pravatar.cc/80?u=${encodeURIComponent(data.name)}`,
    ...data,
  });
  saveRides();
  filters.from = '';
  filters.to = '';
  document.getElementById('search-form').reset();
  renderRides();
  createForm.reset();
  notify('Járat sikeresen meghirdetve!', 'success');
  document.getElementById('rides').scrollIntoView({ behavior: 'smooth' });
});

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

function updateStats() {
  const active = allRides.filter(r => r.seats > 0).length;
  const co2 = Math.round(142 + joinedCount * 3.2);
  const money = 48500 + joinedCount * 1200;

  document.getElementById('stat-rides').textContent = active;
  document.getElementById('stat-co2').textContent = `${co2} kg`;
  document.getElementById('stat-money').textContent = `${money.toLocaleString('hu-HU')} Ft`;
}

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
