// Potvrzení pro jednotlivé smazání uživatele
function confirmSingleDelete() {
  return confirm("Opravdu chcete tohoto uživatele smazat?");
}

// Potvrzení pro hromadné smazání
function confirmBulkDelete() {
  const checked = document.querySelectorAll('input[name="user_ids_to_delete"]:checked');
  if (checked.length === 0) {
    alert("Nejprve vyberte alespoň jednoho uživatele ke smazání.");
    return false;
  }
  return confirm(`Opravdu chcete smazat ${checked.length} uživatele(ů)?`);
}

// Vybrat/odškrtnout všechny checkboxy
function toggleAllUsers(source) {
  const checkboxes = document.querySelectorAll('input[name="user_ids_to_delete"]');
  checkboxes.forEach(cb => {
    cb.checked = source.checked;
    toggleHighlight(cb);
  });
}

// Zvýraznění řádku při změně stavu checkboxu
function toggleHighlight(cb) {
  const li = cb.closest('li');
  if (li) {
    li.classList.toggle('highlighted', cb.checked);
  }
}

// Synchronizace checkboxu „Vybrat vše“ podle ostatních
function updateSelectAll() {
  const checkboxes = document.querySelectorAll('input[name="user_ids_to_delete"]');
  const selectAll = document.getElementById('select-all');
  if (!selectAll) return;
  const allChecked = Array.from(checkboxes).every(cb => cb.checked);
  selectAll.checked = allChecked;
}

// Iniciace po načtení stránky
document.addEventListener('DOMContentLoaded', function () {
  const checkboxes = document.querySelectorAll('input[name="user_ids_to_delete"]');

  checkboxes.forEach(function (cb) {
    toggleHighlight(cb); // pro případ obnovy stránky s výběrem

    cb.addEventListener('change', function () {
      toggleHighlight(cb);
      updateSelectAll();
    });
  });

  // Nastavit původní stav „Vybrat vše“
  updateSelectAll();
});