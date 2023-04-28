import sys

from flask import Blueprint, render_template, session, request

sys.path.insert(1, '../')
from src.metrics import *
from src.visualisation import *

cluster_routes = Blueprint('cluster_routes', __name__)


# -------------------------------------------ML-CLUSTERING-----------------------------------
@cluster_routes.route('/clustering/louvain', endpoint='clustering_louvanian', methods=['GET', 'POST'])
def clustering_louvanian():
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    clusterType = 'louvain'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    number_of_clusters = None

    if request.method == 'POST':
        number_of_clusters = request.form.get('number_of_clusters', None)
        multi_toggle = bool(request.form.get('multi_toggle'))
        dynamic_toggle = bool(request.form.get('dynamic_toggle'))
        directed_toggle = bool(request.form.get('directed_toggle'))
        layout = request.form.get('layout')
        number_of_clusters = int(number_of_clusters) if number_of_clusters else None
        df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
    else:
        df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
    graph1 = session['graph_name1']

    if graph1 == 'no_graph.html':
        graph_path1 = '../static/' + graph1
    else:
        graph_path1 = '../static/uploads/' + filename2 + '/' + graph1

    return render_template('cluster/clustering_louvanian.html', example=df, number_of_clusters=number_of_clusters,
                           multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle,
                           layout=layout, graph1=graph_path1, method_name='Louvain')


@cluster_routes.route('/clustering/greedy_modularity', endpoint='clustering_greedy_modularity', methods=['GET', 'POST'])
def clustering_greedy_modularity():
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    clusterType = 'greedy_modularity'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    number_of_clusters = None

    if request.method == 'POST':
        number_of_clusters = request.form.get('number_of_clusters', None)
        multi_toggle = bool(request.form.get('multi_toggle'))
        dynamic_toggle = bool(request.form.get('dynamic_toggle'))
        directed_toggle = bool(request.form.get('directed_toggle'))
        layout = request.form.get('layout')
        number_of_clusters = int(number_of_clusters) if number_of_clusters else None
        df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
    else:
        df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
    graph1 = session['graph_name1']

    if graph1 == 'no_graph.html':
        graph_path1 = '../static/' + graph1
    else:
        graph_path1 = '../static/uploads/' + filename2 + '/' + graph1

    return render_template('cluster/clustering_greedy_modularity.html', example=df,
                           number_of_clusters=number_of_clusters,
                           multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle,
                           layout=layout, graph1=graph_path1, method_name='Greedy Modularity')


@cluster_routes.route('/clustering/label_propagation', endpoint='clustering_label_propagation', methods=['GET', 'POST'])
def clustering_label_propagation():
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    clusterType = 'label_propagation'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    number_of_clusters = None

    if request.method == 'POST':
        number_of_clusters = request.form.get('number_of_clusters', None)
        multi_toggle = bool(request.form.get('multi_toggle'))
        dynamic_toggle = bool(request.form.get('dynamic_toggle'))
        directed_toggle = bool(request.form.get('directed_toggle'))
        layout = request.form.get('layout')
        number_of_clusters = int(number_of_clusters) if number_of_clusters else None
        df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
    else:
        df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
    graph1 = session['graph_name1']

    if graph1 == 'no_graph.html':
        graph_path1 = '../static/' + graph1
    else:
        graph_path1 = '../static/uploads/' + filename2 + '/' + graph1

    return render_template('cluster/clustering_label_propagation.html', example=df,
                           number_of_clusters=number_of_clusters,
                           multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle,
                           layout=layout, graph1=graph_path1, method_name='Label Propagation')


@cluster_routes.route('/clustering/asyn_lpa', endpoint='clustering_asyn_lpa', methods=['GET', 'POST'])
def clustering_asyn_lpa():
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    clusterType = 'asyn_lpa'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    number_of_clusters = None

    if request.method == 'POST':
        number_of_clusters = request.form.get('number_of_clusters', None)
        multi_toggle = bool(request.form.get('multi_toggle'))
        dynamic_toggle = bool(request.form.get('dynamic_toggle'))
        directed_toggle = bool(request.form.get('directed_toggle'))
        layout = request.form.get('layout')
        number_of_clusters = int(number_of_clusters) if number_of_clusters else None
        df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
    else:
        df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
    graph1 = session['graph_name1']

    if graph1 == 'no_graph.html':
        graph_path1 = '../static/' + graph1
    else:
        graph_path1 = '../static/uploads/' + filename2 + '/' + graph1

    return render_template('cluster/clustering_asyn_lpa.html', example=df, number_of_clusters=number_of_clusters,
                           multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle,
                           layout=layout, graph1=graph_path1, method_name='Asyn Lpa')


@cluster_routes.route('/clustering/k_clique', endpoint='clustering_k_clique', methods=['GET', 'POST'])
def clustering_k_clique():
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    clusterType = 'k_clique'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    number_of_clusters = None

    if request.method == 'POST':
        number_of_clusters = request.form.get('number_of_clusters', None)
        multi_toggle = bool(request.form.get('multi_toggle'))
        dynamic_toggle = bool(request.form.get('dynamic_toggle'))
        directed_toggle = bool(request.form.get('directed_toggle'))
        layout = request.form.get('layout')
        number_of_clusters = int(number_of_clusters) if number_of_clusters else None
        df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
    else:
        df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
    graph1 = session['graph_name1']

    if graph1 == 'no_graph.html':
        graph_path1 = '../static/' + graph1
    else:
        graph_path1 = '../static/uploads/' + filename2 + '/' + graph1

    return render_template('cluster/clustering_k_clique.html', example=df, number_of_clusters=number_of_clusters,
                           multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle,
                           layout=layout, graph1=graph_path1, method_name='K Clique')


@cluster_routes.route('/clustering/spectral', endpoint='clustering_spectral', methods=['GET', 'POST'])
def clustering_spectral():
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    clusterType = 'spectral'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    number_of_clusters = None

    if request.method == 'POST':
        number_of_clusters = request.form.get('number_of_clusters', None)
        multi_toggle = bool(request.form.get('multi_toggle'))
        dynamic_toggle = bool(request.form.get('dynamic_toggle'))
        directed_toggle = bool(request.form.get('directed_toggle'))
        layout = request.form.get('layout')
        number_of_clusters = int(number_of_clusters) if number_of_clusters else None
        df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
    else:
        df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
    graph1 = session['graph_name1']

    if graph1 == 'no_graph.html':
        graph_path1 = '../static/' + graph1
    else:
        graph_path1 = '../static/uploads/' + filename2 + '/' + graph1

    return render_template('cluster/clustering_spectral.html', example=df, number_of_clusters=number_of_clusters,
                           multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle,
                           layout=layout, graph1=graph_path1, method_name='spectrals')


@cluster_routes.route('/clustering/kmeans', endpoint='clustering_kmeans', methods=['GET', 'POST'])
def clustering_kmeans():
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    clusterType = 'kmeans'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    number_of_clusters = None

    if request.method == 'POST':
        number_of_clusters = request.form.get('number_of_clusters', None)
        multi_toggle = bool(request.form.get('multi_toggle'))
        dynamic_toggle = bool(request.form.get('dynamic_toggle'))
        directed_toggle = bool(request.form.get('directed_toggle'))
        layout = request.form.get('layout')
        number_of_clusters = int(number_of_clusters) if number_of_clusters else None
        df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
    else:
        df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
    graph1 = session['graph_name1']

    if graph1 == 'no_graph.html':
        graph_path1 = '../static/' + graph1
    else:
        graph_path1 = '../static/uploads/' + filename2 + '/' + graph1

    return render_template('cluster/clustering_kmeans.html', example=df, number_of_clusters=number_of_clusters,
                           multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle,
                           layout=layout, graph1=graph_path1, method_name='KMeans')


@cluster_routes.route('/clustering/agglomerative', endpoint='clustering_agglomerative', methods=['GET', 'POST'])
def clustering_agglomerative():
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    clusterType = 'agglomerative'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    number_of_clusters = None

    if request.method == 'POST':
        number_of_clusters = request.form.get('number_of_clusters', None)
        multi_toggle = bool(request.form.get('multi_toggle'))
        dynamic_toggle = bool(request.form.get('dynamic_toggle'))
        directed_toggle = bool(request.form.get('directed_toggle'))
        layout = request.form.get('layout')
        number_of_clusters = int(number_of_clusters) if number_of_clusters else None
        df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
    else:
        df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
    graph1 = session['graph_name1']

    if graph1 == 'no_graph.html':
        graph_path1 = '../static/' + graph1
    else:
        graph_path1 = '../static/uploads/' + filename2 + '/' + graph1

    return render_template('cluster/clustering_agglomerative.html', example=df, number_of_clusters=number_of_clusters,
                           multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle,
                           layout=layout, graph1=graph_path1, method_name='Agglomerative')


@cluster_routes.route('/clustering/dbscan', endpoint='clustering_dbscan', methods=['GET', 'POST'])
def clustering_dbscan():
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    clusterType = 'dbscan'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    number_of_clusters = None

    if request.method == 'POST':
        number_of_clusters = request.form.get('number_of_clusters', None)
        multi_toggle = bool(request.form.get('multi_toggle'))
        dynamic_toggle = bool(request.form.get('dynamic_toggle'))
        directed_toggle = bool(request.form.get('directed_toggle'))
        layout = request.form.get('layout')
        number_of_clusters = int(number_of_clusters) if number_of_clusters else None
        df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
    else:
        df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
    graph1 = session['graph_name1']

    if graph1 == 'no_graph.html':
        graph_path1 = '../static/' + graph1
    else:
        graph_path1 = '../static/uploads/' + filename2 + '/' + graph1

    return render_template('cluster/clustering_dbscan.html', example=df, number_of_clusters=number_of_clusters,
                           multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle,
                           layout=layout, graph1=graph_path1, method_name='Dbscan')


@cluster_routes.route('/clustering/hierarchical', endpoint='clustering_hierarchical', methods=['GET', 'POST'])
def clustering_hierarchical():
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    clusterType = 'hierarchical'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    number_of_clusters = None

    if request.method == 'POST':
        number_of_clusters = request.form.get('number_of_clusters', None)
        multi_toggle = bool(request.form.get('multi_toggle'))
        dynamic_toggle = bool(request.form.get('dynamic_toggle'))
        directed_toggle = bool(request.form.get('directed_toggle'))
        layout = request.form.get('layout')
        number_of_clusters = int(number_of_clusters) if number_of_clusters else None
        df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
    else:
        df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
    graph1 = session['graph_name1']

    if graph1 == 'no_graph.html':
        graph_path1 = '../static/' + graph1
    else:
        graph_path1 = '../static/uploads/' + filename2 + '/' + graph1

    return render_template('cluster/clustering_hierarchical.html', example=df, number_of_clusters=number_of_clusters,
                           multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle,
                           layout=layout, graph1=graph_path1, method_name='Hierarchical')
