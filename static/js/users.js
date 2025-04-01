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