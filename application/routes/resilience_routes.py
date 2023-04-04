import sys

import requests
from dictionary.information import *
from flask import Blueprint, render_template, session, request

sys.path.insert(1, '../')

resilience_routes = Blueprint('resilience_routes', __name__)
BASE_URL = 'http://localhost:8000/api/v1'


# -------------------------------------------RESILIENCE_ANALYSIS-----------------------------

@resilience_routes.route('/resilience/malicious', endpoint='resilience_malicious', methods=['GET'])
def resilience_analysis_malicious():
    filename2 = session['filename2']
    graph_path1 = '../static/no_graph.html'
    graph_path2 = '../static/no_graph.html'

    attack_types = ['degree_centrality', 'betweenness_centrality', 'closeness_centrality', 'eigenvector_centrality',
                    'load_centrality', 'kcore', 'degree', 'pagerank', 'triangles']

    number_of_nodes_malicious = None
    number_of_threshold = None
    number_of_clusters = None

    return render_template('resilience/resilience_analyisis_malicious.html', session_id=filename2,
                           attack_types=attack_types,
                           number_of_threshold=number_of_threshold, number_of_clusters=number_of_clusters,
                           number_of_nodes_malicious=number_of_nodes_malicious, graph_path1=graph_path1,
                           graph_path2=graph_path2)


@resilience_routes.route('/resilience/random', endpoint='resilience_random', methods=['GET'])
def resilience_analyisis_random():
    filename2 = session['filename2']
    graph_path1 = '../static/no_graph.html'
    graph_path2 = '../static/no_graph.html'

    return render_template('resilience/resilience_analyisis_random.html', session_id=filename2,
                           number_of_edges=0, number_of_clusters=0,
                           number_of_nodes_random=0, graph_path1=graph_path1,
                           graph_path2=graph_path2)


@resilience_routes.route('/resilience/cluster', endpoint='resilience_cluster', methods=['GET', 'POST'])
def resilience_analyisis_random():
    filename2 = session['filename2']
    graph_path1 = '../static/no_graph.html'
    graph_path2 = '../static/no_graph.html'

    cluster_algorithm = None
    total_clusters = None
    number_of_clusters = None

    if request.method == 'POST':
        cluster_algorithm = request.form.get('layout3')
        total_clusters = request.form.get('number_of_cluster_to_generate')
        number_of_clusters = request.form.get('cluster_to_attack')

        # visualise before and after
        json_data = requests.get(BASE_URL + f'/resilience/{filename2}/random',
                                 params={'cluster_algorithm': cluster_algorithm,
                                         'total_clusters': total_clusters,
                                         'number_of_clusters': number_of_clusters}).json()

        graph_path1 = json_data['network_before'].replace('application/', '')
        graph_path2 = json_data['network_after'].replace('application/', '')

    return render_template('resilience/resilience_analyisis_cluster.html', session_id=filename2,
                           layout3=cluster_algorithm, cluster_to_attack=number_of_clusters,
                           number_of_cluster_to_generate=total_clusters, graph_path1=graph_path1,
                           graph_path2=graph_path2)
