import sys

import requests
from application.dictionary.information import *
from flask import Blueprint, render_template, session, request

sys.path.insert(1, '../')
from src.metrics import *

cluster_routes = Blueprint('cluster_routes', __name__)

# -------------------------------------------ML-CLUSTERING-----------------------------------
BASE_URL = 'http://localhost:8000/api/v1/clusters/'


def get_cluster_details(filename2, clusterType, dynamic_toggle, number_of_clusters, layout):
    url_query = f'?dynamic={dynamic_toggle}&no_of_clusters={number_of_clusters}&layout={layout}'

    json_data = requests.get(f'{BASE_URL}{filename2}/{clusterType}' + url_query).json()

    df = pd.read_json(json_data['data'], orient='split')
    graph_name = json_data['file']

    return df, graph_name


def compute_clustering(networkGraphs, clusterType, filename2):
    multi_toggle = False
    dynamic_toggle = False
    directed_toggle = False
    number_of_clusters = 0
    layout = 'map' if networkGraphs.is_spatial() else 'sfdp'

    if request.method == 'POST':
        number_of_clusters = request.form.get('number_of_clusters', None)
        multi_toggle = bool(request.form.get('multi_toggle'))
        dynamic_toggle = bool(request.form.get('dynamic_toggle'))
        directed_toggle = bool(request.form.get('directed_toggle'))
        layout = request.form.get('layout')
        number_of_clusters = int(number_of_clusters) if number_of_clusters else None

    df, graph_name = get_cluster_details(filename2, clusterType, dynamic_toggle, number_of_clusters, layout)

    if graph_name == 'no_graph.html':
        graph_path = '../static/' + graph_name
    else:
        graph_path = '../static/uploads/' + filename2 + '/' + graph_name

    return df, graph_path, number_of_clusters, multi_toggle, dynamic_toggle, directed_toggle, layout, clusterType


@cluster_routes.route('/clustering/louvain', endpoint='clustering_louvanian', methods=['GET', 'POST'])
def clustering_louvanian():
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)

    df, graph_path, number_of_clusters, multi_toggle, dynamic_toggle, directed_toggle, layout, \
        clusterType = compute_clustering(networkGraphs, 'louvain', filename2)

    return render_template('cluster/clustering_louvanian.html', example=df, number_of_clusters=number_of_clusters,
                           multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle,
                           layout=layout, graph1=graph_path, method_name='Louvain')


@cluster_routes.route('/clustering/greedy_modularity', endpoint='clustering_greedy_modularity', methods=['GET', 'POST'])
def clustering_greedy_modularity():
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)

    df, graph_path1, number_of_clusters, multi_toggle, dynamic_toggle, directed_toggle, layout, \
        clusterType = compute_clustering(networkGraphs, 'greedy_modularity', filename2)

    return render_template('cluster/clustering_greedy_modularity.html', example=df,
                           number_of_clusters=number_of_clusters,
                           multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle,
                           layout=layout, graph1=graph_path1, method_name='Greedy Modularity')


@cluster_routes.route('/clustering/label_propagation', endpoint='clustering_label_propagation', methods=['GET', 'POST'])
def clustering_label_propagation():
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)

    df, graph_path1, number_of_clusters, multi_toggle, dynamic_toggle, directed_toggle, layout, \
        clusterType = compute_clustering(networkGraphs, 'label_propagation', filename2)

    return render_template('cluster/clustering_label_propagation.html', example=df,
                           number_of_clusters=number_of_clusters,
                           multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle,
                           layout=layout, graph1=graph_path1, method_name='Label Propagation')


@cluster_routes.route('/clustering/asyn_lpa', endpoint='clustering_asyn_lpa', methods=['GET', 'POST'])
def clustering_asyn_lpa():
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)

    df, graph_path1, number_of_clusters, multi_toggle, dynamic_toggle, directed_toggle, layout, \
        clusterType = compute_clustering(networkGraphs, 'asyn_lpa', filename2)

    return render_template('cluster/clustering_asyn_lpa.html', example=df, number_of_clusters=number_of_clusters,
                           multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle,
                           layout=layout, graph1=graph_path1, method_name='Asyn Lpa')


@cluster_routes.route('/clustering/k_clique', endpoint='clustering_k_clique', methods=['GET', 'POST'])
def clustering_k_clique():
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)

    df, graph_path1, number_of_clusters, multi_toggle, dynamic_toggle, directed_toggle, layout, \
        clusterType = compute_clustering(networkGraphs, 'k_clique', filename2)

    return render_template('cluster/clustering_k_clique.html', example=df, number_of_clusters=number_of_clusters,
                           multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle,
                           layout=layout, graph1=graph_path1, method_name='K Clique')

@cluster_routes.route('/clustering/spectral', endpoint='clustering_spectral', methods=['GET', 'POST'])
def clustering_spectral():
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)

    df, graph_path1, number_of_clusters, multi_toggle, dynamic_toggle, directed_toggle, layout, \
        clusterType = compute_clustering(networkGraphs, 'spectral', filename2)

    return render_template('cluster/clustering_spectral.html', example=df, number_of_clusters=number_of_clusters,
                           multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle,
                           layout=layout, graph1=graph_path1, method_name='Spectral')


@cluster_routes.route('/clustering/kmeans', endpoint='clustering_kmeans', methods=['GET', 'POST'])
def clustering_kmeans():
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)

    df, graph_path1, number_of_clusters, multi_toggle, dynamic_toggle, directed_toggle, layout, \
        clusterType = compute_clustering(networkGraphs, 'kmeans', filename2)

    return render_template('cluster/clustering_kmeans.html', example=df, number_of_clusters=number_of_clusters,
                           multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle,
                           layout=layout, graph1=graph_path1, method_name='KMeans')


@cluster_routes.route('/clustering/agglomerative', endpoint='clustering_agglomerative', methods=['GET', 'POST'])
def clustering_agglomerative():
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)

    df, graph_path1, number_of_clusters, multi_toggle, dynamic_toggle, directed_toggle, layout, \
        clusterType = compute_clustering(networkGraphs, 'agglomerative', filename2)

    return render_template('cluster/clustering_agglomerative.html', example=df, number_of_clusters=number_of_clusters,
                           multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle,
                           layout=layout, graph1=graph_path1, method_name='Agglomerative')


@cluster_routes.route('/clustering/dbscan', endpoint='clustering_dbscan', methods=['GET', 'POST'])
def clustering_dbscan():
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)

    df, graph_path1, number_of_clusters, multi_toggle, dynamic_toggle, directed_toggle, layout, \
        clusterType = compute_clustering(networkGraphs, 'dbscan', filename2)

    return render_template('cluster/clustering_dbscan.html', example=df, number_of_clusters=number_of_clusters,
                           multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle,
                           layout=layout, graph1=graph_path1, method_name='Dbscan')
