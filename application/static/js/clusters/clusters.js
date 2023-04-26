const BASE_URL = 'http://3.221.153.241:8000/api/v1/clusters/';

const clusteringVisualisation = (data) => {
    const graphCluster = document.getElementById('graph_cluster');
    $(graphCluster).attr('src', '../static/loading.html');
    $.ajax({
        url: BASE_URL + data.session_id + '/' + data.clusterType,
        data: {
            dynamic: data.dynamicToggle,
            no_of_clusters: data.numberOfClusters,
            layout: data.layout,
        },
        type: 'GET',
        mode: 'no-cors',
        success: function (res) {
            const df_data = JSON.parse(res.data);

            const datasetTable = document.getElementById('example-clusters');

            createTable(datasetTable, df_data.data, df_data.columns, true);
            if (res.filename === "no_graph.html") {
                $(graphCluster).attr('src', '../static/' + res.filename);
            } 
            else{
                $(graphCluster).attr('src', '../static/uploads/'+ data.session_id+ '/' + res.filename);
            }              
        },
        error: function (data) {
            alert('An error occurred. Please try again.');

            console.log(data);
        }
    });
}