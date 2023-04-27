const BASE_URL = 'http://localhost:8000/api/v1/hotspot/';

const hotspotVisualisation = (data, hotspotType) => {
    const hotspot_type = hotspotType;
    const graphHotspot = document.getElementById('graphHotspot');
    
    $(graphHotspot).attr('src', '../static/loading.html');
   
    if(hotspot_type === "density")
    {
        $.ajax({
            url: BASE_URL + data.session_id + '/' + hotspot_type,
            data: {
               
            },
            type: 'GET',
            mode: 'no-cors',
            success: function (res) {
                const df_data = JSON.parse(res.data);
    
                const datasetTable = document.getElementById('example-hotspot');
                const graphPath = res.filename.replace('../application/static/', '');
                createTable(datasetTable, df_data.data, df_data.columns, true);
                if (graphPath === "no_graph.html") {
                    $(graphHotspot).attr('src', '../static/' + graphPath);
                } 
                else{
                    $(graphHotspot).attr('src', '../static/uploads/'+ data.session_id+ '/' + graphPath);
                }              
            },
            error: function (data) {
                alert('An error occurred. Please try again.');
                console.log(data);
            }
        });
    }
    else{}
}
