window.addEventListener("DOMContentLoaded", (event) => {
    // Simple-DataTables
    // https://github.com/fiduswriter/Simple-DataTables/wiki

    const datatablesSimple = document.getElementById("datatablesSimple");
    if (datatablesSimple) {
        new simpleDatatables.DataTable(datatablesSimple);
    }

    // This function will loop through all the elements that have the "data-table" class
    // and create a data table sortable and filterable table.
    const dataTableClass = document.querySelectorAll(".data-table");
    for (let i = 0; i < dataTableClass.length; i++) {
        if (dataTableClass[i]) {
            new simpleDatatables.DataTable(dataTableClass[i]);
        }
    }
});
