document.addEventListener("DOMContentLoaded", function() {
    const dayCells = document.querySelectorAll(".day-cell");
  
    dayCells.forEach(function(cell) {
      cell.addEventListener("click", function() {
        const date = cell.getAttribute("data-date");
        // Zde můžete otevřít modální okno nebo vykonat AJAX požadavek pro zobrazení detailů rezervací
        alert("Kliknuto na den: " + date);
      });
    });
  });  