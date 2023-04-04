import sys

import requests
from dictionary.information import *
from flask import Blueprint, render_template, session, request

sys.path.insert(1, '../')

resilience_routes = Blueprint('resilience_routes', __name__)
BASE_URL = 'http://localhost:8000/api/v1'


# -------------------------------------------RESILIENCE_ANALYSIS-----------------------------

@resilience_routes.route('/resilience/malicious', endpoint='resilience_malicious', methods=['GET', 'POST'])
def resilience_analysis_malicious():
    filename2 = session['filename2']
    graph_path1 = '../static/no_graph.html'
    graph_path2 = '../static/no_graph.html'

    operator = None
    res_operator = {
        'greater_than': '>',
        'less_than': '<',
        'greater_than_or_equal_to': '>=',
        'less_than_or_equal_to': '<='
    }

    attack_types = ['degree_centrality', 'betweenness_centrality', 'closeness_centrality', 'eigenvector_centrality',
                    'load_centrality', 'kcore', 'degree', 'pagerank', 'triangles']

    attack_type = None
    number_of_nodes_malicious = None
    number_of_threshold = None
    number_of_clusters = None

    if request.method == 'POST':
        attack_type = request.form.get('attack_type')
        number_of_threshold = request.form.get('number_of_threshold')
        number_of_nodes_malicious = request.form.get('number_of_nodes_malicious')
        number_of_clusters = request.form.get('number_of_clusters')
        operator = res_operator[request.form.get('threshold_operator')]

        # visualise before and after
        json_data = requests.get(BASE_URL + f'/resilience/{filename2}/malicious',
                                 params={'attack_type': attack_type,
                                         'number_of_nodes_malicious': number_of_nodes_malicious,
                                         'number_of_clusters':number_of_clusters,
                                         'operator': operator}).json()

        graph_path1 = json_data['network_before'].replace('application/', '')
        graph_path2 = json_data['network_after'].replace('application/', '')

    return render_template('resilience/resilience_analyisis_malicious.html', session_id=filename2, attack_types=attack_types,
                           number_of_threshold=number_of_threshold, number_of_clusters=number_of_clusters,
                           number_of_nodes_malicious=number_of_nodes_malicious, graph_path1=graph_path1,
                           graph_path2=graph_path2)

@resilience_routes.route('/resilience/random', endpoint='resilience_random', methods=['GET', 'POST'])
def resilience_analyisis_random():
    filename2 = session['filename2']
    graph_path1 = '../static/no_graph.html'
    graph_path2 = '../static/no_graph.html'

    number_of_nodes_random = None
    number_of_edges = None
    number_of_clusters = None

    if request.method == 'POST':
        number_of_edges = request.form.get('number_of_edges')
        number_of_nodes_random = request.form.get('number_of_nodes_random')
        number_of_clusters = request.form.get('number_of_clusters')
        operator = res_operator[request.form.get('threshold_operator')]

        # visualise before and after
        json_data = requests.get(BASE_URL + f'/resilience/{filename2}/random',
                                 params={'number_of_nodes_random': number_of_nodes_random,
                                         'number_of_clusters':number_of_clusters,
                                         'number_of_edges': number_of_edges}).json()

        graph_path1 = json_data['network_before'].replace('application/', '')
        graph_path2 = json_data['network_after'].replace('application/', '')

    return render_template('resilience/resilience_analyisis_random.html', session_id=filename2,
                           number_of_edges=number_of_edges, number_of_clusters=number_of_clusters,
                           number_of_nodes_random=number_of_nodes_random, graph_path1=graph_path1,
                           graph_path2=graph_path2)
  
@resilience_routes.route('/resilience/cluster', endpoint='resilience_cluster', methods=['GET', 'POST'])
def resilience_analyisis_random():
    filename2 = session['filename2']
    graph_path1 = '../static/no_graph.html'
    graph_path2 = '../static/no_graph.html'

    number_of_nodes_random = None
    number_of_edges = None
    number_of_clusters = None

    if request.method == 'POST':
        number_of_edges = request.form.get('number_of_edges')
        number_of_nodes_random = request.form.get('number_of_nodes_random')
        number_of_clusters = request.form.get('number_of_clusters')
        operator = res_operator[request.form.get('threshold_operator')]

        # visualise before and after
        json_data = requests.get(BASE_URL + f'/resilience/{filename2}/random',
                                 params={'number_of_nodes_random': number_of_nodes_random,
                                         'number_of_clusters':number_of_clusters,
                                         'number_of_edges': number_of_edges}).json()

        graph_path1 = json_data['network_before'].replace('application/', '')
        graph_path2 = json_data['network_after'].replace('application/', '')

    return render_template('resilience/resilience_analyisis_cluster.html', session_id=filename2,
                           number_of_edges=number_of_edges, number_of_clusters=number_of_clusters,
                           number_of_nodes_random=number_of_nodes_random, graph_path1=graph_path1,
                           graph_path2=graph_path2)
  