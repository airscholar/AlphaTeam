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

const retrieveGeneralMetrics = (data) => {
    $.ajax({
        url: `${BASE_URL}${data.session_id}/global_metrics`,
        type: 'GET',
        mode: 'no-cors',
        data: {
            multi_toggle: data.multi_toggle,
            directed_toggle: data.directed_toggle,
        },
        success: function (data) {
            const beforeTable = document.getElementById('GM_table_before');
            const afterTable = document.getElementById('GM_table_after');
            const resBefore = JSON.parse(data.data_before);
            const resAfter = JSON.parse(data.data_after);
            const columns = resBefore.columns;

            createTable(afterTable, resAfter.data, columns);
            createTable(beforeTable, resBefore.data, columns);
        },
        error: function (data) {
            alert('An error occurred. Please try again.');

            console.log('ERROR', data);
        }
    });
}

const performVisualisation = (data) => {
    beforeFrame = document.getElementById('before_frame');
    afterFrame = document.getElementById('after_frame');
    $(beforeFrame).attr("src", '../static/loading.html');
    $(afterFrame).attr("src", '../static/loading.html');
    console.log(data)
    $.ajax({
        url: BASE_URL + data.session_id + '/visualisation',
        data: {
            layout: data.layout,
        },
        type: 'GET',
        mode: 'no-cors',
        success: function (data) {
            let beforeFrame = document.getElementById('before_frame');
            let afterFrame = document.getElementById('after_frame');

            const beforePath = data.before_frame.replace('application/', '');
            const afterPath = data.after_frame.replace('application/', '');

            $(beforeFrame).attr("src", beforePath);
            $(afterFrame).attr("src", afterPath);
        },
        error: function (data) {
            alert('An error occurred. Please try again.');
            console.log('ERROR', data);
        }
    });
}

const performResilienceMetrics = (data, plot_type, section) => {
    const prefix = section + '_' + plot_type;
    beforeFrame = document.getElementById(prefix + '_before');
    afterFrame = document.getElementById(prefix + '_after');
    $(beforeFrame).attr("src", '../static/loading.html');
    $(afterFrame).attr("src", '../static/loading.html');
    $.ajax({
        url: BASE_URL + data.session_id + '/' + data.type_of_attack + '/' + plot_type,
        data: {
            multi_toggle: data.multi_toggle,
            directed_toggle: data.directed_toggle,
            layout: data.layout,
        },
        type: 'GET',
        mode: 'no-cors',
        success: function (data) {
            let beforeFrame, afterFrame, beforeTable, afterTable;
            const prefix = section + '_' + plot_type;
            const tablePrefix = section + '_' + plot_type + '_table';

            if (plot_type === 'layout' || plot_type === 'histogram' || plot_type === 'boxplot' || plot_type === 'violin') {
                beforeFrame = document.getElementById(prefix + '_before');
                afterFrame = document.getElementById(prefix + '_after');

                beforeTable = document.getElementById(tablePrefix + '_before');
                afterTable = document.getElementById(tablePrefix + '_after');
            }

            const beforeLayoutPath = data.network_before.replace('application/', '');
            const afterLayoutPath = data.network_after.replace('application/', '');

            $(beforeFrame).attr("src", beforeLayoutPath);
            $(afterFrame).attr("src", afterLayoutPath);

            const resBefore = JSON.parse(data.data_before);
            const resAfter = JSON.parse(data.data_after);

            const columns = resBefore.columns;

            createTable(beforeTable, resBefore.data, columns);
            createTable(afterTable, resAfter.data, columns);
        },
        error: function (data) {
            alert('An error occurred. Please try again.');
            console.log('ERROR', data);
        }
    });
}

const performResilienceCluster = (data, plot_type, section) => {
    const prefix = section + '_' + plot_type;
    beforeFrame = document.getElementById(prefix + '_before');
    afterFrame = document.getElementById(prefix + '_after');
    $(beforeFrame).attr("src", '../static/loading.html');
    $(afterFrame).attr("src", '../static/loading.html');
    $.ajax({
        url: BASE_URL + data.session_id + '/' + data.type_of_attack,
        data: {
            layout: data.layout,
            noOfClusters: data.number_of_clusters,
        },
        type: 'GET',
        mode: 'no-cors',
        success: function (data) {
            let beforeFrame, afterFrame, beforeTable, afterTable;
            const prefix = section + '_' + plot_type;
            const clusteringPrefix = section + '_table';

            if (plot_type === 'louvain' || plot_type === 'greedy_modularity' || plot_type === 'label_propagation' || plot_type === 'asyn_lpa'
                || plot_type === 'k_clique' || plot_type === 'spectral' || plot_type === 'kmeans'
                || plot_type === 'agglomerative' || plot_type === 'dbscan') {
                beforeFrame = document.getElementById(prefix + '_before');
                afterFrame = document.getElementById(prefix + '_after');

                beforeTable = document.getElementById(clusteringPrefix + '_before');
                afterTable = document.getElementById(clusteringPrefix + '_after');
            }

            const beforeLayoutPath = data.network_before.replace('application/', '');
            const afterLayoutPath = data.network_after.replace('application/', '');

            $(beforeFrame).attr("src", beforeLayoutPath);
            $(afterFrame).attr("src", afterLayoutPath);

            const resBefore = JSON.parse(data.data_before);
            const resAfter = JSON.parse(data.data_after);

            const columns = resBefore.columns;

            createTable(beforeTable, resBefore.data, columns, true);
            createTable(afterTable, resAfter.data, columns, true);
        },
        error: function (data) {
            alert('An error occurred. Please try again.');
            console.log('ERROR', data);
        }
    });
}