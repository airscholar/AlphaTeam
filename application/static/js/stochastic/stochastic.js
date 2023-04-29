const BASE_URL = 'http://localhost:8000/api/v1/metrics/';

const stochasticClusteringCoefficientVisualisation = (data, plotType, id) => {
    const plot_type = plotType;
    const graph = document.getElementById(id);
    $(graph).attr('src', '../static/loading.html');

        $.ajax({
            url: BASE_URL + data.session_id + '/clustering_coefficient' + '/' + plot_type,
            data: {
                dynamic_toggle: data.dynamicToggle,
                layout: data.layout,
            },
            type: 'GET',
            mode: 'no-cors',    
            success: function (res) {    
                const df_data = JSON.parse(res.data);

                const graphPath = res.filename.replace('../application/static/', '');
                if (graphPath === "no_graph.html") {
                    $(graph).attr('src', '../static/' + graphPath);
                } 
                else{
                    $(graph).attr('src', '../static/uploads/'+ data.session_id+ '/' + graphPath);
                }
                const datasetTable = document.getElementById('example-stochastic');
                createTable(datasetTable, df_data.data, df_data.columns, true);
            },
            error: function (data) {
                alert('An error occurred. Please try again.');
                console.log(data);
            }
        });
  
}

const stochasticShortestPathVisualisation = (data, plotType, id) => {
    const plot_type = plotType;
    const graph = document.getElementById(id);
    $(graph).attr('src', '../static/loading.html');

        $.ajax({
            url: BASE_URL + data.session_id + '/shortest_path' + '/' + plot_type,
            data: {
                dynamic_toggle: data.dynamicToggle,
                layout: data.layout,
            },
            type: 'GET',
            mode: 'no-cors',    
            success: function (res) {    
                const df_data = JSON.parse(res.data);

                const graphPath = res.filename.replace('../application/static/', '');
                if (graphPath === "no_graph.html") {
                    $(graph).attr('src', '../static/' + graphPath);
                } 
                else{
                    $(graph).attr('src', '../static/uploads/'+ data.session_id+ '/' + graphPath);
                }

                const datasetTable = document.getElementById('example-stochastic');
                createTable(datasetTable, df_data.data, df_data.columns, true);

            },
            error: function (data) {
                alert('An error occurred. Please try again.');
                console.log(data);
            }
        });
  
}