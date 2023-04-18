
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

const performEmbClusteringVisualisationDlEmbedding = (data) => {
    const graphEmbedding = document.getElementById('graph_embedding_cluster_frame');
    $(graphEmbedding).attr('src', '../../../static/loading.html');
    const BASE_URL = 'http://localhost:8000/api/v1/deeplearning/'
    $.ajax({
        url: BASE_URL + data.session_id + '/dl_embedding_clusters',
        data: {
            model: data.model,
            features:  data.feature.join(','),
            layout: data.layout,
            cluster_algorithm: data.cluster_alg,
            number_of_clusters: data.number_of_clusters,
            dimension: data.dimension,
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
