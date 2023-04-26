const BASE_URL = 'http://3.221.153.241:8000/api/v1/visualisation/';

const basicVisualisation = (data, plotType, id) => {
    const plot_type = plotType;
    const graph = document.getElementById(id);
    $(graph).attr('src', '../static/loading.html');

    if(plot_type === "spatial" || plot_type === "temporal")
    {
        $.ajax({
            url: BASE_URL + data.session_id + '/plot_network' + '/' + plot_type,
            data: {
                dynamic_toggle: data.dynamicToggle,
                layout: data.layout,
            },
            type: 'GET',
            mode: 'no-cors',    
            success: function (res) {    
                const graphPath = res.filename.replace('../application/static/', '');
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
    else{
        $.ajax({
            url: BASE_URL + data.session_id + '/' + plot_type,
            data: {
                dynamic_toggle: data.dynamicToggle,
                layout: data.layout,
            },
            type: 'GET',
            mode: 'no-cors',    
            success: function (res) {    
                const graphPath = res.filename.replace('../application/static/', '');
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
    }