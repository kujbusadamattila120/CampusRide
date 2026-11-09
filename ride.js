/* Campus Ride – járáskezelő logika + LocalStorage mentés */
'use strict';

const defaultRides = [
  { id: 1, name: 'Kovács Péter', rating: 4.9, avatar: 'https://i.pravatar.cc/80?img=12',
    from: 'Debrecen, Tócóskert', to: 'Mechwart Technikum', date: '2026-11-11', time: '07:15', seats: 3, price: 400, phone: '+36 30 123 4567' },
  { id: 2, name: 'Nagy Anna', rating: 5.0, avatar: 'https://i.pravatar.cc/80?img=47',
    from: 'Debrecen, Nagyerdő', to: 'Debreceni Egyetem IK', date: '2026-11-11', time: '07:40', seats: 3, price: 300, phone: '+36 20 555 1234' },
  { id: 3, name: 'Szabó Gábor', rating: 4.7, avatar: 'https://i.pravatar.cc/80?img=15',
    from: 'Ebes', to: 'Debrecen Belváros', date: '2026-11-11', time: '08:50', seats: 3, price: 600, phone: '+36 70 987 6543' },
];

let allRides = loadRides();
let joinedCount = loadJoinedCount();
const filters = { from: '', to: '' };

const grid = document.getElementById('rides-grid');
const emptyState = document.getElementById('empty-state');

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Segédfüggvény a szavak nagybetűvel történő kezdéséhez (pl. "kovács péter" -> "Kovács Péter")
function capitalizeWords(str) {
  if (!str) return '';
  return str
    .toLowerCase()
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

function refreshIcons() {
  if (window.lucide) window.lucide.createIcons();
}

function sortRidesByDateTime(ridesArray) {
  return ridesArray.sort((a, b) => {
    const dtA = `${a.date || '2026-11-11'}T${a.time || '00:00'}`;
    const dtB = `${b.date || '2026-11-11'}T${b.time || '00:00'}`;
    return dtA.localeCompare(dtB);
  });
}

function visibleRides() {
  const filtered = allRides.filter(r =>
    r.from.toLowerCase().includes(filters.from) && r.to.toLowerCase().includes(filters.to)
  );
  return sortRidesByDateTime(filtered);
}

function calculateCountdown(dateStr, timeStr) {
  if (!dateStr || !timeStr) return 'Nincs megadva időpont';
  const targetTime = new Date(`${dateStr}T${timeStr}:00`).getTime();
  if (isNaN(targetTime)) return 'Érvénytelen időpont';

  const now = new Date().getTime();
  const diff = targetTime - now;

  if (diff <= 0) return 'A járat már elindult vagy lejárt';

  const days = Math.floor(diff / (1000 * 60 * 60 * 24));
  const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
  const seconds = Math.floor((diff % (1000 * 60)) / 1000);

  let parts = [];
  if (days > 0) parts.push(`${days} nap`);
  if (hours > 0 || days > 0) parts.push(`${hours} óra`);
  parts.push(`${minutes} perc`);
  parts.push(`${seconds} mp`);

  return parts.join(' ');
}

function rideCard(r) {
  const full = r.seats === 0;
  const ratingHtml = (r.rating !== undefined && r.rating !== null)
    ? `<span class="rating"><i data-lucide="star"></i>${Number(r.rating).toFixed(1)}</span>`
    : `<span class="rating" style="color: var(--muted); font-weight: normal;">Nincs értékelés</span>`;

  const rideDate = r.date || '2026-11-11';
  const formattedName = capitalizeWords(r.name);
  const formattedFrom = capitalizeWords(r.from);
  const formattedTo = capitalizeWords(r.to);

  return `
    <article class="card ride-card" data-id="${r.id}">
      <div class="ride-top">
        <img class="avatar" src="${r.avatar}" alt="${escapeHtml(formattedName)}">
        <div class="driver">
          <strong>${escapeHtml(formattedName)}</strong>
          ${ratingHtml}
        </div>
        <span class="price-pill"><b>${r.price} Ft</b> / fő</span>
      </div>
      <div class="route">
        <div><i data-lucide="map-pin" class="pin"></i>${escapeHtml(formattedFrom)}</div>
        <div><i data-lucide="navigation" class="nav-ic"></i>${escapeHtml(formattedTo)}</div>
      </div>
      <div class="ride-bottom">
        <div class="meta">
          <span><i data-lucide="calendar"></i>Dátum: <b>${escapeHtml(rideDate)}</b></span>
          <span><i data-lucide="clock"></i>Indulás: <b>${escapeHtml(r.time)}</b></span>
          <span><i data-lucide="users"></i>Szabad helyek: <b>${r.seats} fő</b></span>
        </div>
        <div style="display: flex; gap: 8px; align-items: center;">
          <button class="btn btn-sm delete-btn" style="background: #dc2626; color: #fff; padding: 8px 10px;" title="Járat törlése">
            <i data-lucide="trash-2"></i>
          </button>
          <button class="btn btn-primary btn-sm join-btn" ${full ? 'disabled' : ''}>
            ${full ? 'Betelt' : '<i data-lucide="user-plus"></i>Csatlakozom'}
          </button>
        </div>
      </div>
      <div class="countdown-bar" data-date="${rideDate}" data-time="${r.time}">
        <i data-lucide="timer"></i> Visszaszámlálás: <span class="countdown-text">${calculateCountdown(rideDate, r.time)}</span>
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

// Visszaszámlálók másodpercenkénti frissítése
setInterval(() => {
  document.querySelectorAll('.countdown-bar').forEach(bar => {
    const date = bar.dataset.date;
    const time = bar.dataset.time;
    const textSpan = bar.querySelector('.countdown-text');
    if (textSpan) {
      textSpan.textContent = calculateCountdown(date, time);
    }
  });
}, 1000);

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
  const delBtn = e.target.closest('.delete-btn');
  if (delBtn) {
    const id = Number(delBtn.closest('.ride-card').dataset.id);
    allRides = allRides.filter(r => r.id !== id);
    saveRides();
    renderRides();
    notify('Járat sikeresen törölve!', 'success');
    return;
  }

  const btn = e.target.closest('.join-btn');
  if (!btn) return;

  const id = Number(btn.closest('.ride-card').dataset.id);
  const ride = allRides.find(r => r.id === id);
  if (!ride || ride.seats === 0) return;

  ride.seats -= 1;
  joinedCount += 1;
  saveRides();
  saveJoinedCount();
  renderRides();
  notify(`Csatlakoztál ${capitalizeWords(ride.name)} járatához!`);
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
    date: value('c-date'),
    time: value('c-time'),
    seats: Number(value('c-seats')),
    price: Number(value('c-price')),
  };

  const error = validateRide(data);
  if (error) {
    notify(error, 'error');
    return;
  }

  allRides.push({
    id: Date.now(),
    rating: null,
    avatar: `https://i.pravatar.cc/80?u=${encodeURIComponent(data.name)}`,
    ...data,
  });
  
  sortRidesByDateTime(allRides);
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
  if (!d.date) return 'Add meg az indulási dátumot!';
  if (!d.time) return 'Add meg az indulási időt!';
  if (!(d.seats >= 1 && d.seats <= 6)) return 'A szabad helyek száma 1 és 6 között lehet!';
  if (!(d.price >= 0 && d.price <= 5000)) return 'Az ár 0 és 5000 Ft között lehet!';
  return null;
}

const searchForm = document.getElementById('search-form');
const dateInput = document.getElementById('s-date');

if (dateInput) {
  dateInput.min = new Date().toISOString().split('T')[0];
}

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
  let rides = defaultRides.map(r => ({ ...r }));
  try {
    const raw = localStorage.getItem('campusride.rides');
    if (raw) {
      const saved = JSON.parse(raw);
      const defaultIds = defaultRides.map(d => d.id);
      
      const savedDefaults = saved.filter(r => defaultIds.includes(r.id));
      const customRides = saved.filter(r => !defaultIds.includes(r.id));
      
      const activeDefaults = defaultRides.map(def => {
        const found = savedDefaults.find(s => s.id === def.id);
        return found ? { ...def, ...found, date: found.date || def.date } : { ...def };
      });
      
      const fixedCustomRides = customRides.map(r => ({
        ...r,
        date: r.date || '2026-11-11'
      }));
      
      rides = [...activeDefaults, ...fixedCustomRides];
    }
  } catch (err) {
    console.warn('A mentett járatok nem olvashatók be', err);
  }
  
  return sortRidesByDateTime(rides);
}

function saveRides() {
  try {
    localStorage.setItem('campusride.rides', JSON.stringify(allRides));
  } catch (err) {
    console.warn('A járatok mentése sikertelen', err);
  }
}

function loadJoinedCount() {
  try {
    const raw = localStorage.getItem('campusride.joinedCount');
    return raw ? Number(raw) : 0;
  } catch (err) {
    console.warn('A csatlakozások száma nem olvasható be', err);
    return 0;
  }
}

function saveJoinedCount() {
  try {
    localStorage.setItem('campusride.joinedCount', joinedCount);
  } catch (err) {
    console.warn('A csatlakozások mentése sikertelen', err);
  }
}