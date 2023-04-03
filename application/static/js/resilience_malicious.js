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
            var beforeFrame = document.getElementById('before_frame');
            var afterFrame = document.getElementById('after_frame');

            beforePath = data.network_before.replace('application/', '');
            afterPath = data.network_after.replace('application/', '');

            $(beforeFrame).attr("src", beforePath);
            $(afterFrame).attr("src", afterPath);
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
            + data.layout + '&number_of_clusters=' + data.number_of_clusters
            + '&attack_type=' + data.type_of_attack + '&number_of_nodes_malicious=' + data.number_of_nodes_malicious,
        type: 'GET',
        mode: 'no-cors',
        success: function (data) {
            let beforeFrame, afterFrame;
            const prefix = section + '_' + plot_type;

            if (plot_type === 'layout' || plot_type === 'histogram' || plot_type === 'boxplot' || plot_type === 'violin') {
                beforeFrame = document.getElementById(prefix + '_before');
                afterFrame = document.getElementById(prefix + '_after');
            }

            beforeLayoutPath = data.network_before.replace('application/', '');
            afterLayoutPath = data.network_after.replace('application/', '');

            $(beforeFrame).attr("src", beforeLayoutPath);
            $(afterFrame).attr("src", afterLayoutPath);


        },
        error: function (data) {
            alert('An error occurred. Please try again.');
            console.log('ERROR', data);
        }
    });
}

