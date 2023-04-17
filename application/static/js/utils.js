const createTable = (tableElem, data, columns, isCluster = false) => {
    tableElem.innerHTML = '';
    tableElem.innerHTML = '';

    if ($.fn.DataTable.isDataTable(tableElem)) {
        let table = $(tableElem).DataTable();
        if (table && table.table().node().parentNode) {
            table.destroy();
        }
    }

    if (tableElem.tHead) {
        tableElem.tHead.remove();
    }

    const headerRow = tableElem.createTHead().insertRow(0);
    for (let i = 0; i < columns.length; i++) {
        headerRow.insertCell(i).innerHTML = columns[i];
    }
    const body = tableElem.createTBody();
    for (let i = 0; i < data.length; i++) {
        const row = body.insertRow(i);
        for (let j = 0; j < data[i].length; j++) {
            row.insertCell(j).innerHTML = data[i][j];
        }
    }
    $(tableElem).DataTable({
        "scrollX": true,
    });
}