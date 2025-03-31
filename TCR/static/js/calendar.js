document.addEventListener("DOMContentLoaded", function() {
  console.log("calendar.js loaded");

  // Připojení listeneru pouze ke dlaždicím, které nejsou disabled
  const dayTiles = document.querySelectorAll(".calendar-day:not(.disabled)");
  dayTiles.forEach(function(tile) {
    tile.addEventListener("click", function() {
      const date = tile.getAttribute("data-date");
      openReservationModal(date);
    });
  });
});

// Funkce, která otevře modální okno pro rezervaci
function openReservationModal(date) {
  let modal = document.getElementById("reservationModal");
  if (!modal) {
    modal = document.createElement("div");
    modal.id = "reservationModal";
    modal.classList.add("modal");
    modal.innerHTML = `
      <div class="modal-content">
        <span class="close">&times;</span>
        <h2>Rezervace pro ${date}</h2>
        <form id="reservationForm">
          <label for="time_interval">Vyberte časový interval:</label>
          <select id="time_interval" name="time_interval">
            <option value="">Načítání...</option>
          </select>
          <input type="hidden" name="date" value="${date}">
          <button type="submit" class="btn btn-custom">Vytvořit rezervaci</button>
        </form>
      </div>
    `;
    document.body.appendChild(modal);

    // Listener pro zavření modálu pomocí tlačítka "X"
    modal.querySelector(".close").addEventListener("click", function() {
      modal.style.display = "none";
    });
    // Zavření modálu při kliknutí mimo jeho obsah
    modal.addEventListener("click", function(event) {
      if (event.target === modal) {
        modal.style.display = "none";
      }
    });
    // Listener pro odeslání formuláře
    modal.querySelector("#reservationForm").addEventListener("submit", function(e) {
      e.preventDefault();
      submitReservationForm(modal);
    });
  } else {
    // Aktualizace titulku a skrytého pole pro datum, pokud modál již existuje
    modal.querySelector("h2").innerText = `Rezervace pro ${date}`;
    modal.querySelector("input[name='date']").value = date;
  }
  modal.style.display = "block";
  
  // Načtení dostupných časových intervalů pro zvolené datum
  loadAvailableIntervals(date);
}

// Funkce pro načtení dostupných intervalů
function loadAvailableIntervals(date) {
  const select = document.getElementById("time_interval");
  // Vyprázdnění selectu
  select.innerHTML = "";
  fetch("/reservation/available_intervals/?date=" + date)
    .then(response => {
      if (!response.ok) {
        throw new Error("Chyba při načítání dostupných termínů");
      }
      return response.json();
    })
    .then(data => {
      if (data.length === 0) {
        let option = document.createElement("option");
        option.value = "";
        option.textContent = "Žádné dostupné termíny";
        select.appendChild(option);
      } else {
        data.forEach(interval => {
          let option = document.createElement("option");
          option.value = interval.start + "-" + interval.end;
          option.textContent = `${interval.start}:00 - ${interval.end}:00`;
          select.appendChild(option);
        });
      }
    })
    .catch(error => {
      console.error("Error loading intervals:", error);
      let option = document.createElement("option");
      option.value = "";
      option.textContent = "Chyba při načítání termínů";
      select.appendChild(option);
    });
}

// Funkce, která odesílá data rezervace přes AJAX
function submitReservationForm(modal) {
  const form = modal.querySelector("#reservationForm");
  const formData = new FormData(form);
  const date = formData.get("date");
  const interval = formData.get("time_interval");

  if (!interval) {
    alert("Prosím vyberte časový interval.");
    return;
  }

  const parts = interval.split("-");
  const start_hour = parseInt(parts[0], 10);
  const end_hour = parseInt(parts[1], 10);

  const data = {
    date: date,
    start_hour: start_hour,
    end_hour: end_hour
  };

  fetch("/reservation/create/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken")
    },
    body: JSON.stringify(data)
  })
  .then(response => {
    if (!response.ok) {
      throw new Error("Chyba při vytváření rezervace.");
    }
    return response.json();
  })
  .then(result => {
    alert(result.message);
    modal.style.display = "none";
    location.reload();
  })
  .catch(error => {
    alert("Došlo k chybě: " + error.message);
  });
}

// Pomocná funkce pro získání CSRF tokenu z cookies
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}