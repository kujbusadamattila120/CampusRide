// Az alap járatok (ezekkel indul az oldal, amíg nincs mentett adat)
const defaultRides = [
  { id: 1, name: 'Kovács Péter', rating: 4.9, avatar: 'https://i.pravatar.cc/80?img=12', from: 'Debrecen, Tócóskert', to: 'Mechwart Technikum',   time: '07:15', seats: 3, price: 400 },
  { id: 2, name: 'Nagy Anna',    rating: 5.0, avatar: 'https://i.pravatar.cc/80?img=47', from: 'Debrecen, Nagyerdő',  to: 'Debreceni Egyetem IK', time: '07:40', seats: 2, price: 300 },
  { id: 3, name: 'Szabó Gábor',  rating: 4.7, avatar: 'https://i.pravatar.cc/80?img=15', from: 'Ebes',                to: 'Debrecen Belváros',    time: '08:50', seats: 1, price: 600 },
];

// Időpont szerint rendezi a járatokat (a legkorábbi indulás van elöl)
function sortByTime(list) {
  return list.sort((a, b) => a.time.localeCompare(b.time));
}

// Betölti a mentett járatokat a localStorage-ból.
// Ha még nincs mentett adat, az alap járatokat (defaultRides) használja.
function loadRides() {
  const saved = localStorage.getItem('campusride.rides');
  const list = saved ? JSON.parse(saved) : [...defaultRides];
  return sortByTime(list);
}

// Elmenti az aktuális járatokat (allRides) JSON formátumban a localStorage-ba.
// Így frissítés után is megmaradnak az adatok.
function saveRides() {
  localStorage.setItem('campusride.rides', JSON.stringify(allRides));
  localStorage.setItem('campusride.joined', joined);
}

let allRides = loadRides();
let joined = Number(localStorage.getItem('campusride.joined')) || 0; // ennyien csatlakoztak eddig

const list = document.getElementById('rides-list');

// A járatok kirajzolása az oldalra
function showRides(rideList) {
  list.innerHTML = '';

  for (const ride of rideList) {
    let button = `<button class="button small" onclick="joinRide(${ride.id})"><i data-lucide="user-plus"></i>Csatlakozom</button>`;
    if (ride.seats === 0) {
      button = '<button class="button small" disabled>Betelt</button>';
    }

    list.innerHTML += `
      <div class="card">
        <div class="ride-top">
          <img class="avatar" src="${ride.avatar}" alt="">
          <div>
            <b>${ride.name}</b><br>
            <span class="rating">★ ${ride.rating.toFixed(1)}</span>
          </div>
          <span class="price"><b>${ride.price} Ft</b> / fő</span>
        </div>
        <div class="route">
          <p class="from"><i data-lucide="map-pin"></i>${ride.from}</p>
          <p class="to"><i data-lucide="navigation"></i>${ride.to}</p>
        </div>
       <div class="ride-bottom">
          <div>
            <small><i data-lucide="clock"></i>Indulás: <b>${ride.time}</b></small>
            <small><i data-lucide="users"></i>Szabad helyek: <b>${ride.seats} fő</b></small>
          </div>
          <div class="actions">
            <button class="button small delete" onclick="deleteRide(${ride.id})" title="Járat törlése"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg></button>
            ${button}
          </div>
        </div>
      </div>`;
  }

  updateStats();
  lucide.createIcons(); // az ikonok kirajzolása
}

// Statisztika frissítése
function updateStats() {
  let active = 0;
  for (const ride of allRides) {
    if (ride.seats > 0) active++;
  }
  document.getElementById('stat-rides').textContent = active;
  document.getElementById('stat-co2').textContent = 142 + joined * 3;
  document.getElementById('stat-money').textContent = (48500 + joined * 1200).toLocaleString('hu-HU');
}

// Csatlakozás egy járathoz
function joinRide(id) {
  const ride = allRides.find(r => r.id === id);
  ride.seats--;
  joined++;
  saveRides();
  showRides(allRides);
  alert('Csatlakoztál ' + ride.name + ' járatához!');
}

// Keresés: a megadott szöveget keresi a járatok indulásában és érkezésében
function searchRides() {
  const from = document.getElementById('search-from').value.toLowerCase();
  const to = document.getElementById('search-to').value.toLowerCase();

  const result = allRides.filter(r =>
    r.from.toLowerCase().includes(from) && r.to.toLowerCase().includes(to)
  );

  if (result.length === 0) {
    alert('Nincs találat.');
  }
  showRides(result);
}
// Jár törlése az azonosítója alapján
function deleteRide(id) {
  if (confirm('Biztosan törölni szeretnéd ezt a járatot?')) {
    // Kiszűrjük a törlendő járatot a tömbből
    allRides = allRides.filter(r => r.id !== id);
    
    // Frissítjük a LocalStorage-ot és az oldalt
    saveRides();
    showRides(allRides);
  }
}
// Új járat hozzáadása az űrlapból
function addRide(event) {
  event.preventDefault(); // ne töltse újra az oldalt

  const name = document.getElementById('new-name').value;
  const from = document.getElementById('new-from').value;
  const to = document.getElementById('new-to').value;

  if (from.toLowerCase() === to.toLowerCase()) {
    alert('Az indulás és az érkezés nem lehet ugyanaz!');
    return;
  }

  allRides.push({
    id: Date.now(),
    name: name,
    rating: 5.0,
    avatar: 'https://i.pravatar.cc/80?u=' + encodeURIComponent(name),
    from: from,
    to: to,
    time: document.getElementById('new-time').value,
    seats: Number(document.getElementById('new-seats').value),
    price: Number(document.getElementById('new-price').value),
  });

  sortByTime(allRides);
  saveRides();
  event.target.reset();
  showRides(allRides);
  alert('Járat sikeresen meghirdetve!');
}

// Induláskor kirajzoljuk a járatokat
showRides(allRides);