import sys

import requests
from flask import Blueprint, render_template, session

from application.dictionary.information import *
from src.utils import get_networkGraph

sys.path.insert(1, '../../')

resilience_routes = Blueprint('resilience_routes', __name__)
BASE_URL = 'http://localhost:8000/api/v1'


# -------------------------------------------RESILIENCE_ANALYSIS-----------------------------
@resilience_routes.route('/resilience/malicious', endpoint='resilience_malicious', methods=['GET'])
def resilience_analysis_malicious():
    """
    :Function: Visualise the malicious resilience analysis
    :return: the malicious resilience analysis page
    """
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
                           graph_path2=graph_path2,
                           tooltip_attack_summary=tooltips['attack_summary'], tooltip_multi=tooltips['multi'],
                           tooltip_directed=tooltips['directed'], tooltip_layout_dropdown=tooltips['layout_dropdown'],
                           tooltip_number_of_clusters=tooltips['number_of_clusters'],
                           description=description['resilience_analysis_malicious'],
                           tooltip_type_of_attack=tooltips['type_of_attack'], tooltip_node_tab=tooltips['node_tab'],
                           tooltip_threshold_tab=tooltips['threshold_tab'])


@resilience_routes.route('/resilience/random', endpoint='resilience_random', methods=['GET'])
def resilience_analysis_random():
    """
    :Function: Visualise the random resilience analysis
    :return: the random resilience analysis page
    """
    filename2 = session['filename2']
    graph_path1 = '../static/no_graph.html'
    graph_path2 = '../static/no_graph.html'

    return render_template('resilience/resilience_analyisis_random.html', session_id=filename2,
                           number_of_edges=0, number_of_clusters=0,
                           number_of_nodes_random=0, graph_path1=graph_path1,
                           graph_path2=graph_path2,
                           tooltip_attack_summary=tooltips['attack_summary'], tooltip_multi=tooltips['multi'],
                           tooltip_directed=tooltips['directed'], tooltip_layout_dropdown=tooltips['layout_dropdown'],
                           tooltip_number_of_clusters=tooltips['number_of_clusters'],
                           description=description['resilience_analyisis_random'],
                           tooltip_node_tab=tooltips['node_tab'],
                           tooltip_edge_tab=tooltips['edge_tab'])


@resilience_routes.route('/resilience/cluster', endpoint='resilience_cluster', methods=['GET', 'POST'])
def resilience_analysis_cluster():
    """
    :Function: Visualise the cluster resilience analysis
    :return: the cluster resilience analysis page
    """
    filename2 = session['filename2']
    graph_path1 = '../static/no_graph.html'
    graph_path2 = '../static/no_graph.html'

    cluster_algorithm = None
    total_clusters = None
    number_of_clusters = None

    return render_template('resilience/resilience_analyisis_cluster.html', session_id=filename2,
                           layout3=cluster_algorithm, cluster_to_attack=number_of_clusters,
                           number_of_cluster_to_generate=total_clusters, graph_path1=graph_path1,
                           graph_path2=graph_path2,
                           tooltip_attack_summary=tooltips['attack_summary'], tooltip_multi=tooltips['multi'],
                           tooltip_directed=tooltips['directed'], tooltip_layout_dropdown=tooltips['layout_dropdown'],
                           tooltip_number_of_clusters=tooltips['number_of_clusters'],
                           description=description['resilience_analyisis_cluster'],
                           tooltip_type_of_cluster=tooltips['type_of_cluster'],
                           tooltip_number_of_cluster_to_generate=tooltips['number_of_cluster_to_generate'],
                           tooltip_number_of_cluster_to_attack=tooltips['number_of_cluster_to_attack'])


@resilience_routes.route('/resilience/custom', endpoint='resilience_custom', methods=['GET', 'POST'])
def resilience_analysis_custom():
    """
    :Function: Visualise the custom resilience analysis
    :return: the custom resilience analysis page
    """
    filename2 = session['filename2']
    graph_path1 = '../static/no_graph.html'
    graph_path2 = '../static/no_graph.html'

    cluster_algorithm = None
    total_clusters = None
    number_of_clusters = None

    NetworkGraph = get_networkGraph(filename2)
    layout = 'map' if NetworkGraph.is_spatial() else 'sfdp'

    json_data = requests.get(
        f'{BASE_URL}/visualisation/{filename2}/plot_network/spatial?dynamic=False&layout={layout}').json()
    graph_input_custom = json_data['filename']
    graph_input_custom = f"../static/uploads/{filename2}/" + graph_input_custom

    return render_template('resilience/resilience_analyisis_custom.html', session_id=filename2,
                           layout3=cluster_algorithm, cluster_to_attack=number_of_clusters,
                           number_of_cluster_to_generate=total_clusters, graph_path1=graph_path1,
                           graph_path2=graph_path2, graph_input_custom=graph_input_custom,
                           tooltip_attack_summary=tooltips['attack_summary'], tooltip_multi=tooltips['multi'],
                           tooltip_directed=tooltips['directed'], tooltip_layout_dropdown=tooltips['layout_dropdown'],
                           tooltip_number_of_clusters=tooltips['number_of_clusters'],
                           description=description['resilience_analyisis_custom'],
                           tooltip_list_of_nodes=tooltips['list_of_nodes'])
