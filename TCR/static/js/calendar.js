document.addEventListener("DOMContentLoaded", function() {
    // Funkce pro získání CSRF tokenu z cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Vytvoří nebo vrátí existující modal pro rezervaci
    function createModal(date) {
        let modal = document.getElementById("reservationModal");
        if (!modal) {
            modal = document.createElement("div");
            modal.id = "reservationModal";
            modal.classList.add("modal");
            modal.innerHTML = `
                <div class="modal-content">
                    <span class="close">&times;</span>
                    <h2>Vytvořit rezervaci pro ${date}</h2>
                    <form id="reservationForm">
                        <label for="start_hour">Začátek (hodina):</label>
                        <input type="number" id="start_hour" name="start_hour" min="0" max="23" required>
                        <label for="end_hour">Konec (hodina):</label>
                        <input type="number" id="end_hour" name="end_hour" min="1" max="24" required>
                        <input type="hidden" name="date" value="${date}">
                        <button type="submit">Potvrdit rezervaci</button>
                    </form>
                </div>
            `;
            document.body.appendChild(modal);

            // Zavírací tlačítko modalu
            modal.querySelector(".close").addEventListener("click", closeModal);
            // Zavření modalu při kliknutí mimo jeho obsah
            window.addEventListener("click", function(event) {
                if (event.target === modal) {
                    closeModal();
                }
            });
        }
        return modal;
    }

    function openModal(modal) {
        modal.style.display = "block";
    }

    function closeModal() {
        let modal = document.getElementById("reservationModal");
        if (modal) {
            modal.style.display = "none";
        }
    }

    // Připojení posluchače k tlačítkům "Rezervovat"
    const reserveButtons = document.querySelectorAll(".reserve-btn");
    reserveButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            const date = button.getAttribute("data-date");
            const modal = createModal(date);
            openModal(modal);

            // Připojení event listeneru pro odeslání formuláře
            const form = modal.querySelector("#reservationForm");
            form.addEventListener("submit", function(e) {
                e.preventDefault();

                const formData = new FormData(form);
                const startHour = formData.get("start_hour");
                const endHour = formData.get("end_hour");
                const reservationDate = formData.get("date");

                // Základní validace: konečná hodina musí být větší než začáteční
                if (parseInt(endHour) <= parseInt(startHour)) {
                    alert("Koncová hodina musí být větší než začáteční.");
                    return;
                }

                const data = {
                    date: reservationDate,
                    start_hour: startHour,
                    end_hour: endHour
                };

                // Odeslání AJAX požadavku
                fetch("/reservations/create/", {
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
                    alert("Rezervace byla úspěšně vytvořena.");
                    closeModal();
                    // Aktualizaci kalendáře lze provést buď dynamicky, nebo znovunačtením stránky:
                    location.reload();
                })
                .catch(error => {
                    alert("Došlo k chybě: " + error.message);
                });
            }, { once: true }); // Listener se odstraní po prvním odeslání
        });
    });
});