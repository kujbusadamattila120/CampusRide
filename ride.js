
const initialRides = [
    { driver: "Kovács Péter", from: "Debrecen, Tócóskert", to: "Mechwart Technikum", seats: 2 },
    { driver: "Nagy Anna", from: "Debrecen, Nagyerdő", to: "Debreceni Egyetem IK", seats: 3 },
    { driver: "Szabó Gábor", from: "Ebes", to: "Debrecen Belváros", seats: 1 }
];


function renderRides() {
    const listContainer = document.getElementById("ride-list");
    listContainer.innerHTML = "";

    initialRides.forEach((ride, index) => {
        const div = document.createElement("div");
        div.className = "ride-item";
        div.innerHTML = `
            <h3>${ride.from} ➔ ${ride.to}</h3>
            <p><strong>Sofőr:</strong> ${ride.driver}</p>
            <p><strong>Szabad helyek:</strong> ${ride.seats} fő</p>
            <button onclick="joinRide(${index})" class="btn" style="margin-top:0.5rem; padding: 0.4rem 0.8rem; font-size: 0.85rem;">Csatlakozás</button>
        `;
        listContainer.appendChild(div);
    });
}


function joinRide(index) {
    if (initialRides[index].seats > 0) {
        initialRides[index].seats--;
        alert(`Sikeresen csatlakoztál ${initialRides[index].driver} járatához!`);
        renderRides();
    } else {
        alert("Sajnáljuk, ezen a járaton már nincs több szabad hely!");
    }
}


document.getElementById("add-ride-form").addEventListener("submit", function(e) {
    e.preventDefault();

    const driver = document.getElementById("driver").value;
    const from = document.getElementById("from").value;
    const to = document.getElementById("to").value;
    const seats = parseInt(document.getElementById("seats").value);

    initialRides.push({ driver, from, to, seats });
    renderRides();

    
    this.reset();
    alert("Járat sikeresen meghirdetve!");
});


renderRides();