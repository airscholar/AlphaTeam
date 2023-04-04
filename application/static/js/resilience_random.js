const BASE_URL = 'http://localhost:8000/api/v1/resilience/';

function performResilienceRandom(data) {
    console.log(data)
    $.ajax({
        url: `${BASE_URL}${data.session_id}/random`,
        data:{
            number_of_edges: data.number_of_edges,
            number_of_nodes: data.number_of_nodes,
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
