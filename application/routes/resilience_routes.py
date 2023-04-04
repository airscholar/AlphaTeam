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

    return render_template('resilience/resilience_analyisis_malicious.html', session_id=filename2, attack_types=attack_types,
                           number_of_threshold=number_of_threshold, number_of_clusters=number_of_clusters,
                           number_of_nodes_malicious=number_of_nodes_malicious, graph_path1=graph_path1,
                           graph_path2=graph_path2)