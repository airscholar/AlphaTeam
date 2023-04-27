const BASE_URL = 'http://localhost:8000/api/v1/metrics/';

const metricsAllVisualisation = (data, plotType, id) => {
    const plot_type = plotType;
    const graph = document.getElementById(id);
    $(graph).attr('src', '../static/loading.html');
    
    if(plot_type === "layout")
    {
        $.ajax({
            url: BASE_URL + data.session_id + '/' + data.metricsType + '/all',
            data: {
                directed: data.directedToggle,
                multi: data.multiToggle,
                layout: data.layout,
            },
            type: 'GET',
            mode: 'no-cors',    
            success: function (res) {
                const df_data = JSON.parse(res.data);
    
                const datasetTable = document.getElementById('example-metrics-all');
                const graphPath = res.filename.replace('../application/static/', '');
                createTable(datasetTable, df_data.data, df_data.columns, true);
                if (graphPath === "no_graph.html") {
                    $(graph).attr('src', '../static/' + graphPath);
                } 
                else{
                    $(graph).attr('src', '../static/uploads/'+ data.session_id+ '/' + graphPath);
                }              
            },
            error: function (data) {
                alert('An error occurred. Please try again.');
                console.log(data);
            }
        });
    }
    else {
        $.ajax({
            url: BASE_URL + data.session_id + '/' + data.metricsType + '/' + plot_type,
            data: {
                directed: data.directedToggle2,
                multi: data.multiToggle2,
            },
            type: 'GET',
            mode: 'no-cors',
            success: function (res) {
                const df_data = JSON.parse(res.data);
    
                const datasetTable = document.getElementById('example-metrics-all');
    
                createTable(datasetTable, df_data.data, df_data.columns, true);
                if (res.filename === "no_graph.html") {
                    $(graph).attr('src', '../' + res.filename.replace('application/', ''));
                } 
                else{
                    $(graph).attr('src', '../static/uploads/'+ data.session_id+ '/' + res.filename);
                }              
            },
            error: function (data) {
                alert('An error occurred. Please try again.');
                console.log(data);
            }
        });
    }
    }

const metricsSingleVisualisation = (data, plotType, id) => {
    const plot_type = plotType;
    const graph = document.getElementById(id);
    $(graph).attr('src', '../static/loading.html');

    if(plot_type === "layout")
    {
        $.ajax({
            url: BASE_URL + data.session_id + '/' + data.metricsType,
            data: {
                directed: data.directedToggle,
                multi: data.multiToggle,
                layout: data.layout,
                dynamic: data.dynamicToggle,
            },
            type: 'GET',
            mode: 'no-cors',
            success: function (res) {
                const df_data = JSON.parse(res.data);
    
                const datasetTable = document.getElementById('example-metrics-single');
                const graphPath = res.filename.replace('../application/static/', '');
                createTable(datasetTable, df_data.data, df_data.columns, true);
                if (graphPath === "no_graph.html") {
                    $(graph).attr('src', '../static/' + graphPath);
                } 
                else{
                    $(graph).attr('src', '../static/uploads/'+ data.session_id+ '/' + graphPath);
                }              
            },
            error: function (data) {
                alert('An error occurred. Please try again.');
                console.log(data);
            }
        });
    }
    else {
        $.ajax({
            url: BASE_URL + data.session_id + '/' + data.metricsType + '/' + plot_type,
            data: {
                directed: data.directedToggle2,
                multi: data.multiToggle2,
            },
            type: 'GET',
            mode: 'no-cors',
            success: function (res) {
                const df_data = JSON.parse(res.data);
    
                const datasetTable = document.getElementById('example-metrics-single');
    
                createTable(datasetTable, df_data.data, df_data.columns, true);
                if (res.filename === "no_graph.html") {
                    $(graph).attr('src', '../' + res.filename.replace('application/', ''));
                } 
                else{
                    $(graph).attr('src', '../static/uploads/'+ data.session_id+ '/' + res.filename);
                }              
            },
            error: function (data) {
                alert('An error occurred. Please try again.');
                console.log(data);
            }
        });
    }
   }
