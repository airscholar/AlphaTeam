const BASE_URL = 'http://localhost:8000/api/v1/resilience/';

function performResilienceMalicious(data) {
    console.log(data)
    $.ajax({
        url: BASE_URL + data.session_id + '/malicious',
        data: {
            attack_type: data.type_of_attack,
            number_of_nodes_malicious: data.number_of_nodes_malicious,
            operator: data.threshold_operator,
            number_of_thresholds: data.number_of_threshold,
        },
        type: 'GET',
        mode: 'no-cors',
        success: function (data) {
            let beforeFrame = document.getElementById('before_frame');
            let afterFrame = document.getElementById('after_frame');
            var beforeHeatmap = document.getElementById('before_heatmap');
            var afterHeatmap = document.getElementById('after_heatmap');

            const beforePath = data.network_before.replace('application/', '');
            const afterPath = data.network_after.replace('application/', '');
            beforeHeatmapPath = data.heatmap_before.replace('application/', '');
            afterHeatmapPath = data.heatmap_after.replace('application/', '');

            $(beforeFrame).attr("src", beforePath);
            $(afterFrame).attr("src", afterPath);
            $(beforeHeatmap).attr("src", beforeHeatmapPath);
            $(afterHeatmap).attr("src", afterHeatmapPath);

            let attackSummary = document.getElementById('AS_Table');
            const resBefore = JSON.parse(data.data);
            const columns = resBefore.columns;

            createTable(attackSummary, resBefore.data, columns);
        },
        error: function (data) {
            console.log('ERROR', data);
        }
    });
}

function performResilienceMetrics(data, plot_type, section) {
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

function performResilienceCluster(data, plot_type, section) {
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

function retrieveGeneralMetrics(data) {
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

            createTable(beforeTable, resBefore.data, columns);
            createTable(afterTable, resAfter.data, columns);
        },
        error: function (data) {
            console.log('ERROR', data);
        }
    });
}

const createTable = (tableElem, data, columns, isCluster=false) => {
    tableElem.innerHTML = '';
    tableElem.innerHTML = '';

    if ($.fn.DataTable.isDataTable(tableElem)) {
        $(tableElem).DataTable().destroy();
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
    if (!isCluster) $(tableElem).DataTable();
    else
        $(tableElem).DataTable({
            "scrollX": true,
        });
};

function performVisualisation(data) {
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
            console.log('ERROR', data);
        }
    });
}
