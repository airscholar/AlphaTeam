from flask import Blueprint, render_template, session, request, redirect, url_for
import csv
import sys
import scipy as sp
from flask_caching import Cache
import matplotlib.pyplot as plt
import re
import time
import shutil

sys.path.insert(1, '../')

from src.NetworkGraphs import *
from src.metrics import *
from src.preprocessing import *
from src.visualisation import *
from flask import g

cluster_routes = Blueprint('cluster_routes', __name__)


#-------------------------------------------ML-CLUSTERING-----------------------------------

@cluster_routes.route('/clustering/louvain', endpoint='clustering_louvanian', methods=['GET', 'POST'])
def clustering_louvanian():
    number_of_clusters = None
    networkGraphs = session['network_graphs']
    filename2 = session['filename2']
    clusterType = 'louvain'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    
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

    print(number_of_clusters)

    return render_template('clustering_louvanian.html', example=df, number_of_clusters=number_of_clusters,
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, method_name='Louvain')

@cluster_routes.route('/clustering/greedy_modularity', endpoint='clustering_greedy_modularity', methods=['GET', 'POST'])
def clustering_greedy_modularity():
    networkGraphs = session['network_graphs']
    filename2 = session['filename2']
    clusterType = 'greedy_modularity'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    
    if request.method == 'POST':
            multi_toggle = bool(request.form.get('multi_toggle'))
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
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

    return render_template('clustering_greedy_modularity.html', example=df,
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, method_name='Greedy Modularity')

@cluster_routes.route('/clustering/label_propagation', endpoint='clustering_label_propagation', methods=['GET', 'POST'])
def clustering_label_propagation():
    networkGraphs = session['network_graphs']
    filename2 = session['filename2']
    clusterType = 'label_propagation'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    
    if request.method == 'POST':
            multi_toggle = bool(request.form.get('multi_toggle'))
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
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

    return render_template('clustering_label_propagation.html', example=df,
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, method_name='Label Propagation')

@cluster_routes.route('/clustering/asyn_lpa', endpoint='clustering_asyn_lpa', methods=['GET', 'POST'])
def clustering_asyn_lpa():
    networkGraphs = session['network_graphs']
    filename2 = session['filename2']
    clusterType = 'asyn_lpa'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    
    if request.method == 'POST':
            multi_toggle = bool(request.form.get('multi_toggle'))
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
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

    return render_template('clustering_asyn_lpa.html', example=df,
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, method_name='Asyn Lpa')

@cluster_routes.route('/clustering/girvan_newman', endpoint='clustering_girvan_newman', methods=['GET', 'POST'])
def clustering_girvan_newman():
    networkGraphs = session['network_graphs']
    filename2 = session['filename2']
    clusterType = 'girvan_newman'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    
    if request.method == 'POST':
            multi_toggle = bool(request.form.get('multi_toggle'))
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
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

    return render_template('clustering_girvan_newman.html', example=df,
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, method_name='Girvan Newman')

@cluster_routes.route('/clustering/edge_betweenness', endpoint='clustering_edge_betweenness', methods=['GET', 'POST'])
def clustering_edge_betweenness():
    networkGraphs = session['network_graphs']
    filename2 = session['filename2']
    clusterType = 'edge_betweenness'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    
    if request.method == 'POST':
            multi_toggle = bool(request.form.get('multi_toggle'))
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
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

    return render_template('clustering_edge_betweenness.html', example=df,
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, method_name='Edge Betweenness')

@cluster_routes.route('/clustering/k_clique', endpoint='clustering_k_clique', methods=['GET', 'POST'])
def clustering_k_clique():
    networkGraphs = session['network_graphs']
    filename2 = session['filename2']
    clusterType = 'k_clique'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    
    if request.method == 'POST':
            multi_toggle = bool(request.form.get('multi_toggle'))
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
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

    return render_template('clustering_k_clique.html', example=df,
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, method_name='K Clique')

@cluster_routes.route('/clustering/spectral', endpoint='clustering_spectral', methods=['GET', 'POST'])
def clustering_spectral():
    networkGraphs = session['network_graphs']
    filename2 = session['filename2']
    clusterType = 'spectral'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    
    if request.method == 'POST':
            multi_toggle = bool(request.form.get('multi_toggle'))
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
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

    return render_template('clustering_spectral.html', example=df,
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, method_name='spectrals')

@cluster_routes.route('/clustering/kmeans', endpoint='clustering_kmeans', methods=['GET', 'POST'])
def clustering_kmeans():
    networkGraphs = session['network_graphs']
    filename2 = session['filename2']
    clusterType = 'kmeans'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    
    if request.method == 'POST':
            multi_toggle = bool(request.form.get('multi_toggle'))
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
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

    return render_template('clustering_kmeans.html', example=df,
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, method_name='KMeans')

@cluster_routes.route('/clustering/agglomerative', endpoint='clustering_agglomerative', methods=['GET', 'POST'])
def clustering_agglomerative():
    networkGraphs = session['network_graphs']
    filename2 = session['filename2']
    clusterType = 'agglomerative'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    
    if request.method == 'POST':
            multi_toggle = bool(request.form.get('multi_toggle'))
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
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

    return render_template('clustering_agglomerative.html', example=df,
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, method_name='Agglomerative')

@cluster_routes.route('/clustering/dbscan', endpoint='clustering_dbscan', methods=['GET', 'POST'])
def clustering_dbscan():
    networkGraphs = session['network_graphs']
    filename2 = session['filename2']
    clusterType = 'dbscan'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    
    if request.method == 'POST':
            multi_toggle = bool(request.form.get('multi_toggle'))
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
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

    return render_template('clustering_dbscan.html', example=df,
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, method_name='Dbscan')

@cluster_routes.route('/clustering/hierarchical', endpoint='clustering_hierarchical', methods=['GET', 'POST'])
def clustering_hierarchical():
    networkGraphs = session['network_graphs']
    filename2 = session['filename2']
    clusterType = 'hierarchical'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    
    if request.method == 'POST':
            multi_toggle = bool(request.form.get('multi_toggle'))
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
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

    return render_template('clustering_hierarchical.html', example=df,
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, method_name='Hierarchical')
