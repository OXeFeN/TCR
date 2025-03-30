document.addEventListener("DOMContentLoaded", function() {
  console.log("calendar.js loaded");

  // Připojení listeneru ke všem dlaždicím dne
  const dayTiles = document.querySelectorAll(".calendar-day");
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
    // Vytvoření modálního okna, pokud ještě neexistuje
    modal = document.createElement("div");
    modal.id = "reservationModal";
    modal.classList.add("modal");
    modal.innerHTML = `
      <div class="modal-content">
        <span class="close">&times;</span>
        <h2>Rezervace pro ${date}</h2>
        <form id="reservationForm">
          <label for="start_hour">Začátek (hodina):</label>
          <input type="number" id="start_hour" name="start_hour" min="6" max="21" required>
          <label for="end_hour">Konec (hodina):</label>
          <input type="number" id="end_hour" name="end_hour" min="7" max="22" required>
          <input type="hidden" name="date" value="${date}">
          <button type="submit" class="btn btn-custom">Vytvořit rezervaci</button>
        </form>
      </div>
    `;
    document.body.appendChild(modal);

    // Zavření modálu po kliknutí na "X"
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
    // Aktualizujeme titulek a skryté pole pro datum, pokud modál již existuje
    modal.querySelector("h2").innerText = `Rezervace pro ${date}`;
    modal.querySelector("input[name='date']").value = date;
  }
  modal.style.display = "block";
}

// Funkce, která odesílá data rezervace přes AJAX
function submitReservationForm(modal) {
  const form = modal.querySelector("#reservationForm");
  const formData = new FormData(form);
  const data = {
    date: formData.get("date"),
    start_hour: formData.get("start_hour"),
    end_hour: formData.get("end_hour")
  };

  if (parseInt(data.end_hour) <= parseInt(data.start_hour)) {
    alert("Koncová hodina musí být větší než začáteční.");
    return;
  }

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
    // Volitelně obnovit stránku, aby se aktualizoval kalendář
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