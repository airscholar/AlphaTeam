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
    if (!isCluster) $(tableElem).DataTable();
    else
        $(tableElem).DataTable({
            "scrollX": true,
        });
}

const performEmbeddingVisualisation = (data) => {
    const BASE_URL = 'http://localhost:8000/api/v1/deeplearning/'
    const graphEmbedding = document.getElementById('graph_embedding_frame');
    $(graphEmbedding).attr('src', '../static/loading.html');
    $.ajax({
        url: BASE_URL + data.session_id + '/node2vec',
        data: {
            layout: data.layout,
            p: data.p_value,
            q: data.q_value,
        },
        type: 'GET',
        mode: 'no-cors',
        success: function (res) {
            const df_data = JSON.parse(res.data);

            const datasetTable = document.getElementById('embedding-metrics');

            createTable(datasetTable, df_data.data, df_data.columns, true);

            $(graphEmbedding).attr('src', '../' + res.filename);
        },
        error: function (data) {
            alert('An error occurred. Please try again.');

            console.log(data);
        }
    });
}

const performEmbClusteringVisualisation = (data) => {
    const graphEmbedding = document.getElementById('graph_embedding_cluster_frame');
    $(graphEmbedding).attr('src', '../../../static/loading.html');
    const BASE_URL = 'http://localhost:8000/api/v1/deeplearning/'
    $.ajax({
        url: BASE_URL + data.session_id + '/node2vec_clusters',
        data: {
            cluster_algorithm: data.cluster_alg,
            number_of_clusters: data.number_of_clusters,
            layout: data.layout,
            p: data.p_value,
            q: data.q_value,
        },
        type: 'GET',
        mode: 'no-cors',
        success: function (res) {
            const df_data = JSON.parse(res.data);

            const datasetTable = document.getElementById('embedding-metrics');

            createTable(datasetTable, df_data.data, df_data.columns, true);

            $(graphEmbedding).attr('src', '../../' + res.filename);
        },
        error: function (data) {
            alert('An error occurred. Please try again.');

            console.log(data);
        }
    });
}

// Dl embedding

const performEmbeddingVisualisationDlEmbedding = (data) => {
    const BASE_URL = 'http://localhost:8000/api/v1/deeplearning/'
    const graphEmbedding = document.getElementById('graph_embedding_frame');
    $(graphEmbedding).attr('src', '../static/loading.html');
    $.ajax({
        url: BASE_URL + data.session_id + '/dl_embedding',
        data: {
            model: data.model,
            dimension: data.dimension,
            layout: data.layout,
            features: data.feature.join(',')
        },
        type: 'GET',
        mode: 'no-cors',
        success: function (res) {
            const df_data = JSON.parse(res.data);

            const datasetTable = document.getElementById('embedding-metrics');

            createTable(datasetTable, df_data.data, df_data.columns, true);

            $(graphEmbedding).attr('src', '../' + res.filename);
        },
        error: function (data) {
            alert('An error occurred. Please try again.');

            console.log(data);
        }
    });
}