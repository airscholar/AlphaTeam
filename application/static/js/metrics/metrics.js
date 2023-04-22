const BASE_URL = 'http://localhost:8000/api/v1/metrics/';

const metricsAllVisualisation = (data, plotType) => {
    const plot_type = plotType;
    const graph1 = document.getElementById('graph1');
    const graph2 = document.getElementById('graph2');
    const graph3 = document.getElementById('graph3');
    const graph4 = document.getElementById('graph4');
    $(graph1).attr('src', '../static/loading.html');
    $(graph2).attr('src', '../static/loading.html');
    $(graph3).attr('src', '../static/loading.html');
    $(graph4).attr('src', '../static/loading.html');
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
                    $(graph1).attr('src', '../static/' + graphPath);
                } 
                else{
                    $(graph1).attr('src', '../static/uploads/'+ data.session_id+ '/' + graphPath);
                }              
            },
            error: function (data) {
                alert('An error occurred. Please try again.');
                console.log(data);
            }
        });
    }
    else if(plot_type === "histogram"){
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
                    $(graph2).attr('src', '../' + res.filename.replace('application/', ''));
                } 
                else{
                    $(graph2).attr('src', '../static/uploads/'+ data.session_id+ '/' + res.filename);
                }              
            },
            error: function (data) {
                alert('An error occurred. Please try again.');
                console.log(data);
            }
        });
    }
    else if(plot_type === "boxplot"){
        $.ajax({
            url: BASE_URL + data.session_id + '/' + data.metricsType + '/' + plot_type,
            data: {
                directed: data.directedToggle3,
                multi: data.multiToggle3,
            },
            type: 'GET',
            mode: 'no-cors',
            success: function (res) {
                const df_data = JSON.parse(res.data);
    
                const datasetTable = document.getElementById('example-metrics-all');
    
                createTable(datasetTable, df_data.data, df_data.columns, true);
                if (res.filename === "no_graph.html") {
                    $(graph3).attr('src', '../' + res.filename.replace('application/', ''));
                } 
                else{
                    $(graph3).attr('src', '../static/uploads/'+ data.session_id+ '/' + res.filename);
                }              
            },
            error: function (data) {
                alert('An error occurred. Please try again.');
                console.log(data);
            }
        });
    }
    else if(plot_type === "violin"){
        $.ajax({
            url: BASE_URL + data.session_id + '/' + data.metricsType + '/' + plot_type,
            data: {
                directed: data.directedToggle4,
                multi: data.multiToggle4,
            },
            type: 'GET',
            mode: 'no-cors',
            success: function (res) {
                const df_data = JSON.parse(res.data);
    
                const datasetTable = document.getElementById('example-metrics-all');
    
                createTable(datasetTable, df_data.data, df_data.columns, true);
                if (res.filename === "no_graph.html") {
                    $(graph4).attr('src', '../' + res.filename.replace('application/', ''));
                } 
                else{
                    $(graph4).attr('src', '../static/uploads/'+ data.session_id+ '/' + res.filename);
                }              
            },
            error: function (data) {
                alert('An error occurred. Please try again.');
                console.log(data);
            }
        });
    }
}