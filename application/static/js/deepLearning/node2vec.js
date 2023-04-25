const BASE_URL = 'http://localhost:8000/api/v1/deeplearning/';

const performNode2VecEmbeddingVisualisation = (data) => {
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

            $(graphEmbedding).attr('src', '../../'+res.filename);
        },
        error: function (data) {
            alert('An error occurred. Please try again.');

            console.log(data);
        }
    });
}

const performNode2VecEmbClusteringVisualisation = (data) => {
    const graphEmbedding = document.getElementById('graph_embedding_cluster_frame');
    $(graphEmbedding).attr('src', '../../../../static/loading.html');
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

            $(graphEmbedding).attr('src', '../../'+res.filename);
            console.log('success');
        },
        error: function (data) {
            alert('An error occurred. Please try again.');

            console.log(data);
        }
    });
}
