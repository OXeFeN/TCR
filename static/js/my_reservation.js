document.addEventListener("DOMContentLoaded", function() {
    // Vybereme všechny formuláře, jejichž action obsahuje "delete/"
    const deleteForms = document.querySelectorAll("form[action*='delete/']");
    deleteForms.forEach(function(form) {
      form.addEventListener("submit", function(event) {
        if (!confirm("Opravdu chcete smazat rezervaci?")) {
          event.preventDefault();
        }
      });
    });
  });
  