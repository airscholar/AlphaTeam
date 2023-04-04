const BASE_URL = 'http://localhost:8000/api/v1/resilience/';

function performResilienceMalicious(data) {
    console.log(data)
    $.ajax({
        url: BASE_URL + data.session_id + '/malicious?multi_toggle='
            + data.multi_toggle + '&directed_toggle=' + data.directed_toggle + '&layout='
            + data.layout + '&number_of_clusters=' + data.number_of_clusters
            + '&attack_type=' + data.type_of_attack + '&number_of_nodes_malicious=' + data.number_of_nodes_malicious,
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
        },
        error: function (data) {
            console.log('ERROR', data);
        }
    });
}

function performResilienceMetrics(data, plot_type, section) {
    $.ajax({
        url: BASE_URL + data.session_id + '/' + data.type_of_attack + '/' + plot_type + '?multi_toggle='
            + data.multi_toggle + '&directed_toggle=' + data.directed_toggle + '&layout='
            + data.layout,
        type: 'GET',
        mode: 'no-cors',
        success: function (data) {
            let beforeFrame, afterFrame;
            const prefix = section + '_' + plot_type;

            if (plot_type === 'layout' || plot_type === 'histogram' || plot_type === 'boxplot' || plot_type === 'violin') {
                beforeFrame = document.getElementById(prefix + '_before');
                afterFrame = document.getElementById(prefix + '_after');
            }

            const beforeLayoutPath = data.network_before.replace('application/', '');
            const afterLayoutPath = data.network_after.replace('application/', '');

            $(beforeFrame).attr("src", beforeLayoutPath);
            $(afterFrame).attr("src", afterLayoutPath);


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
        data: {
            multi_toggle: data.multi_toggle,
            directed_toggle: data.directed_toggle,
        },
        success: function (data) {
            const beforeTable = document.getElementById('GM_Table_before');
            const afterTable = document.getElementById('GM_Table_after');
            const resBefore = JSON.parse(data.data_before);
            const resAfter = JSON.parse(data.data_after);
            const columns = resBefore.columns;

            const createTable = (tableElem, data) => {
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
                $(tableElem).DataTable();
            };

            createTable(beforeTable, resBefore.data);
            createTable(afterTable, resAfter.data);
        },
        error: function (data) {
            console.log('ERROR', data);
        }
    });


}

