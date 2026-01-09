const BACKEND_URL = "http://localhost:8000";

const searchForm = document.getElementById("searchForm");
const resultsGrid = document.getElementById("resultsGrid");
const loader = document.getElementById("loader");

// 1. BUSCAR VUELOS
searchForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const origin = document.getElementById("origin").value.toUpperCase();
    const destination = document.getElementById("destination").value.toUpperCase();
    const date = document.getElementById("date").value;

    loader.classList.remove("hidden");
    resultsGrid.innerHTML = "";

    try {
        const response = await fetch(`${BACKEND_URL}/search?origin=${origin}&dest=${destination}&date=${date}`);
        const data = await response.json();
        
        loader.classList.add("hidden");
        renderFlights(data.flights, { origin, destination, date });
    } catch (error) {
        loader.innerText = "❌ Error al conectar con el backend.";
        console.error(error);
    }
});

// 2. RENDERIZAR RESULTADOS
function renderFlights(flights, searchParams) {
    if (!flights || flights.length === 0) {
        resultsGrid.innerHTML = "<p>No se encontraron vuelos para esta fecha.</p>";
        return;
    }

    flights.slice(0, 5).forEach((flight, index) => {
        const price = flight.price.total;
        const currency = flight.price.currency;
        
        const card = document.createElement("div");
        card.className = "flight-card-container";
        card.innerHTML = `
            <div class="flight-card">
                <div>
                    <span class="price-tag">${price} ${currency}</span>
                    <p>Vuelo directo o con escalas disponible</p>
                </div>
                <button onclick="showAlertForm(${index}, ${price})">🔔 Alertarme si baja</button>
            </div>
            <div id="alert-form-${index}" class="alert-form-inline hidden">
                <input type="email" id="email-${index}" placeholder="Tu email" required>
                <button onclick="createAlert(${index}, '${searchParams.origin}', '${searchParams.destination}', '${searchParams.date}', ${price})" style="background: var(--success)">Activar Alerta</button>
            </div>
        `;
        resultsGrid.appendChild(card);
    });
}

// 3. MOSTRAR FORMULARIO DE ALERTA
window.showAlertForm = (index) => {
    const form = document.getElementById(`alert-form-${index}`);
    form.classList.toggle("hidden");
};

// 4. CREAR ALERTA EN EL BACKEND (DYNAMODB)
window.createAlert = async (index, origin, destination, date, currentPrice) => {
    const email = document.getElementById(`email-${index}`).value;
    
    if (!email) {
        alert("Por favor ingresa tu email");
        return;
    }

    const payload = {
        email: email,
        origin: origin,
        destination: destination,
        date: date,
        current_price: parseFloat(currentPrice)
    };

    try {
        const response = await fetch(`${BACKEND_URL}/subscribe`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            showToast("✅ ¡Alerta activada! Te avisaremos vía email.");
            document.getElementById(`alert-form-${index}`).innerHTML = "<p style='color:green'>✔ Suscrito correctamente</p>";
        }
    } catch (error) {
        alert("Error al crear la alerta");
    }
};

function showToast(msg) {
    const toast = document.getElementById("notification-toast");
    toast.innerText = msg;
    toast.classList.remove("hidden");
    setTimeout(() => toast.classList.add("hidden"), 4000);
}