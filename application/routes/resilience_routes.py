from flask import Blueprint, render_template, session, request, redirect, url_for
import csv
import sys
import scipy as sp
from flask_caching import Cache
import matplotlib.pyplot as plt
import re
import time
import shutil
from dictionary.information import *

sys.path.insert(1, '../')
from src.utils import *
from src.NetworkGraphs import *
from src.metrics import *
from src.preprocessing import *
from src.visualisation import *
from src.resilience import *
from flask import g

resilience_routes = Blueprint('resilience_routes', __name__)

networkGraphs2 = None

#-------------------------------------------RESILIENCE_ANALYSIS-----------------------------

@resilience_routes.route('/resilience/malicious', endpoint='resilience_malicious', methods=['GET', 'POST'])
def resilience_analyisis_malicious():
    attack = 'malicious'
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    tab_main =  session.get('tab_main', 'tab1')
    layout = session.get('layout_malicious', 'degree_centrality')
    layout2 = session.get('layout2_malicious', 'equal_to')
    
    if layout2 == "greater_than":
        operator = ">"
    elif layout2 == "less_than":
        operator = "<"
    elif layout2 == "equal_to":
        operator = "="
    else:
        operator = None

    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    number_of_nodes = session.get('number_of_nodes', None)
    number_of_edges = session.get('number_of_edges', None)
    number_of_threashold = session.get('number_of_threashold', None)

    val1 = session.get('val1', None)
    val2 = session.get('val2', None)
    val3 = session.get('val3', None)
    val4 = session.get('val4', None)

    # here we use number of nodes
    global networkGraphs2
    if val3 != layout:
        session['val3'] = layout
    
    if val1 != number_of_nodes:
        session['val1'] = number_of_nodes
        tab_main = 'tab1'
        session['tab_main'] = tab_main
        networkGraphs2, df2 = resilience(networkGraphs, attack=attack, metric=layout, number_of_nodes=int(number_of_nodes))
    
    # here we use number of edges
    if val2 != number_of_threashold:
        session['val2'] = number_of_threashold
        tab_main = 'tab2'
        session['tab_main'] = tab_main
        networkGraphs2, df2 = resilience(networkGraphs, attack=attack, metric=layout, threshold=int(number_of_threashold), operator=operator)
 
    if val4 != layout2:
        session['val4'] = layout2
        tab_main = 'tab2'
        session['tab_main'] = tab_main
        if(number_of_threashold is not None):
            networkGraphs2, df2 = resilience(networkGraphs, attack=attack, metric=layout, threshold=int(number_of_threashold), operator=operator)

    return template_resilience_tabs('resilience/resilience_analyisis_malicious.html', number_of_nodes, number_of_edges, number_of_threashold, layout, layout2, tab_main, attack)

@resilience_routes.route('/resilience/cluster', endpoint='resilience_cluster', methods=['GET', 'POST'])
def resilience_analyisis_cluster():
    layout = 'louvain'
    
    if request.method == 'POST':
        number_of_cluster_to_generate = request.form.get('number_of_cluster_to_generate', None)
        number_of_cluster_to_generate = int(number_of_cluster_to_generate) if number_of_cluster_to_generate else None
        cluster_to_attack = request.form.get('cluster_to_attack', None)
        cluster_to_attack = int(cluster_to_attack) if cluster_to_attack else None
        layout = request.form.get('layout')
    else:
        number_of_cluster_to_generate = None
        cluster_to_attack = None
 
    return render_template('resilience/resilience_analyisis_cluster.html', layout=layout, number_of_cluster_to_generate=number_of_cluster_to_generate, cluster_to_attack=cluster_to_attack)

@resilience_routes.route('/resilience/random', endpoint='resilience_random', methods=['GET', 'POST'])
def resilience_analyisis_random():
    attack = 'random'
    tab_main =  session.get('tab_main', 'tab1')
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    number_of_nodes = session.get('number_of_nodes', None)
    number_of_edges = session.get('number_of_edges', None)
    number_of_threashold = session.get('number_of_threashold', None)
    layout = session.get('layout_malicious', 'degree_centrality')
    layout2 = session.get('layout2_malicious', 'equal_to')
    
    val1 = session.get('val1', None)
    val2 = session.get('val2', None)
    
    # here we use number of nodes
    global networkGraphs2
    if val1 != number_of_nodes:
        session['val1'] = number_of_nodes
        tab_main = 'tab1'
        session['tab_main'] = tab_main
        networkGraphs2, df2 = resilience(networkGraphs, attack=attack, number_of_nodes=int(number_of_nodes))
    
    # here we use number of edges
    if val2 != number_of_edges:
        session['val2'] = number_of_edges
        tab_main = 'tab2'
        session['tab_main'] = tab_main
        networkGraphs2, df2 = resilience(networkGraphs, attack=attack, number_of_edges=int(number_of_edges))

    print('number_of_nodes',number_of_nodes)
     
    return template_resilience_tabs('resilience/resilience_analyisis_random.html', number_of_nodes, number_of_edges, number_of_threashold, layout, layout2, tab_main, attack)

@resilience_routes.route('/resilience/malicious/upload', endpoint='resilience_malicious_upload', methods=['GET', 'POST'])
def resilience_malicious_upload():
    number_of_nodes = request.form.get('number_of_nodes')
    number_of_threashold = request.form.get('number_of_threashold')
    layout2 = request.form.get('layout2')
    layout = request.form.get('layout')

    if number_of_nodes == '':
        number_of_nodes = None
    if number_of_threashold == '':
        number_of_threashold = None
    session['number_of_nodes'] = number_of_nodes
    session['number_of_threashold'] = number_of_threashold
    session['number_of_threashold'] = number_of_threashold
    session['layout_malicious'] = layout
    session['layout2_malicious'] = layout2
    # do something with the form data
    
    return redirect(url_for('resilience_routes.resilience_malicious'))

@resilience_routes.route('/resilience/random/upload', endpoint='resilience_random_upload', methods=['GET', 'POST'])
def resilience_random_upload():
    number_of_nodes = request.form.get('number_of_nodes')
    number_of_edges = request.form.get('number_of_edges')
    if number_of_nodes == '':
        number_of_nodes = None
    if number_of_edges == '':
        number_of_edges = None
    session['number_of_nodes'] = number_of_nodes
    session['number_of_edges'] = number_of_edges

    # do something with the form data
    
    return redirect(url_for('resilience_routes.resilience_random'))


def template_resilience_tabs(template_name_arg, number_of_nodes_arg, number_of_edges_arg, number_of_threashold_arg, layout_arg, layout2_arg, tab_main_arg, attack_arg):
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    multi_toggle = True
    directed_toggle = True
    number_of_clusters = None
    if networkGraphs.is_spatial():
        visualisation_layout = 'map'
    else:
        visualisation_layout = 'sfdp'
    attack = attack_arg
    attack_name_from_nw = None

    if networkGraphs2 is not None:
        attack_name_from_nw = networkGraphs2.get_attack_vector()
    
    if attack == attack_name_from_nw:
        #if networkGraphs2 is not None:
        # check POST condition
        if request.method == 'POST':
            visualisation_layout = request.form.get('visualisation_layout')
            multi_toggle = bool(request.form.get('multi_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            number_of_clusters = request.form.get('number_of_clusters', None)
            number_of_clusters = int(number_of_clusters) if number_of_clusters else None
        graph_name1 = plot_network(networkGraphs, layout=visualisation_layout, dynamic=False)
        graph_name2 = plot_network(networkGraphs2, layout=visualisation_layout, dynamic=False)
            # degree
        df_degree_centrality_before, graph_degree_centrality_layout_name_1 = plot_metric(networkGraphs, 'degree_centrality', directed=directed_toggle, multi=multi_toggle, dynamic=False, layout=visualisation_layout)
        df_degree_centrality_after, graph_degree_centrality_layout_name_2 = plot_metric(networkGraphs2, 'degree_centrality', directed=directed_toggle, multi=multi_toggle, dynamic=False, layout=visualisation_layout)
        df_degree_centrality_before, graph_degree_centrality_histogram_name_1 = plot_histogram(networkGraphs, 'degree_centrality', directed=directed_toggle, multi=multi_toggle)
        df_degree_centrality_after, graph_degree_centrality_histogram_name_2 = plot_histogram(networkGraphs2, 'degree_centrality', directed=directed_toggle, multi=multi_toggle)
        df_degree_centrality_before, graph_degree_centrality_boxplot_name_1 = plot_boxplot(networkGraphs, 'degree_centrality', directed=directed_toggle, multi=multi_toggle)
        df_degree_centrality_after, graph_degree_centrality_boxplot_name_2 = plot_boxplot(networkGraphs2, 'degree_centrality', directed=directed_toggle, multi=multi_toggle)
        df_degree_centrality_before, graph_degree_centrality_violinplot_name_1 = plot_violin(networkGraphs, 'degree_centrality', directed=directed_toggle, multi=multi_toggle)
        df_degree_centrality_after, graph_degree_centrality_violinplot_name_2 = plot_violin(networkGraphs2, 'degree_centrality', directed=directed_toggle, multi=multi_toggle)
            # enginevector
        df_eigenvector_centrality_before, graph_eigenvector_centrality_layout_name_1 = plot_metric(networkGraphs, 'eigenvector_centrality', directed=directed_toggle, multi=multi_toggle, dynamic=False, layout=visualisation_layout)
        df_eigenvector_centrality_after, graph_eigenvector_centrality_layout_name_2 = plot_metric(networkGraphs2, 'eigenvector_centrality', directed=directed_toggle, multi=multi_toggle, dynamic=False, layout=visualisation_layout)
        df_eigenvector_centrality_before, graph_eigenvector_centrality_histogram_name_1 = plot_histogram(networkGraphs, 'eigenvector_centrality', directed=directed_toggle, multi=multi_toggle)
        df_eigenvector_centrality_after, graph_eigenvector_centrality_histogram_name_2 = plot_histogram(networkGraphs2, 'eigenvector_centrality', directed=directed_toggle, multi=multi_toggle)
        df_eigenvector_centrality_before, graph_eigenvector_centrality_boxplot_name_1 = plot_boxplot(networkGraphs, 'eigenvector_centrality', directed=directed_toggle, multi=multi_toggle)
        df_eigenvector_centrality_after, graph_eigenvector_centrality_boxplot_name_2 = plot_boxplot(networkGraphs2, 'eigenvector_centrality', directed=directed_toggle, multi=multi_toggle)
        df_eigenvector_centrality_before, graph_eigenvector_centrality_violinplot_name_1 = plot_violin(networkGraphs, 'eigenvector_centrality', directed=directed_toggle, multi=multi_toggle)
        df_eigenvector_centrality_after, graph_eigenvector_centrality_violinplot_name_2 = plot_violin(networkGraphs2, 'eigenvector_centrality', directed=directed_toggle, multi=multi_toggle)
            # closeness
        df_closeness_centrality_before, graph_closeness_centrality_layout_name_1 = plot_metric(networkGraphs, 'closeness_centrality', directed=directed_toggle, multi=multi_toggle, dynamic=False, layout=visualisation_layout)
        df_closeness_centrality_after, graph_closeness_centrality_layout_name_2 = plot_metric(networkGraphs2, 'closeness_centrality', directed=directed_toggle, multi=multi_toggle, dynamic=False, layout=visualisation_layout)
        df_closeness_centrality_before, graph_closeness_centrality_histogram_name_1 = plot_histogram(networkGraphs, 'closeness_centrality', directed=directed_toggle, multi=multi_toggle)
        df_closeness_centrality_after, graph_closeness_centrality_histogram_name_2 = plot_histogram(networkGraphs2, 'closeness_centrality', directed=directed_toggle, multi=multi_toggle)
        df_closeness_centrality_before, graph_closeness_centrality_boxplot_name_1 = plot_boxplot(networkGraphs, 'closeness_centrality', directed=directed_toggle, multi=multi_toggle)
        df_closeness_centrality_after, graph_closeness_centrality_boxplot_name_2 = plot_boxplot(networkGraphs2, 'closeness_centrality', directed=directed_toggle, multi=multi_toggle)
        df_closeness_centrality_before, graph_closeness_centrality_violinplot_name_1 = plot_violin(networkGraphs, 'closeness_centrality', directed=directed_toggle, multi=multi_toggle)
        df_closeness_centrality_after, graph_closeness_centrality_violinplot_name_2 = plot_violin(networkGraphs2, 'closeness_centrality', directed=directed_toggle, multi=multi_toggle)
            # betweness
        df_betwenness_centrality_before, graph_betwenness_centrality_layout_name_1 = plot_metric(networkGraphs, 'betweenness_centrality', directed=directed_toggle, multi=multi_toggle, dynamic=False, layout=visualisation_layout)
        df_betwenness_centrality_after, graph_betwenness_centrality_layout_name_2 = plot_metric(networkGraphs2, 'betweenness_centrality', directed=directed_toggle, multi=multi_toggle, dynamic=False, layout=visualisation_layout)
        df_betwenness_centrality_before, graph_betwenness_centrality_histogram_name_1 = plot_histogram(networkGraphs, 'betweenness_centrality', directed=directed_toggle, multi=multi_toggle)
        df_betwenness_centrality_after, graph_betwenness_centrality_histogram_name_2 = plot_histogram(networkGraphs2, 'betweenness_centrality', directed=directed_toggle, multi=multi_toggle)
        df_betwenness_centrality_before, graph_betwenness_centrality_boxplot_name_1 = plot_boxplot(networkGraphs, 'betweenness_centrality', directed=directed_toggle, multi=multi_toggle)
        df_betwenness_centrality_after, graph_betwenness_centrality_boxplot_name_2 = plot_boxplot(networkGraphs2, 'betweenness_centrality', directed=directed_toggle, multi=multi_toggle)
        df_betwenness_centrality_before, graph_betwenness_centrality_violinplot_name_1 = plot_violin(networkGraphs, 'betweenness_centrality', directed=directed_toggle, multi=multi_toggle)
        df_betwenness_centrality_after, graph_betwenness_centrality_violinplot_name_2 = plot_violin(networkGraphs2, 'betweenness_centrality', directed=directed_toggle, multi=multi_toggle)
            #load
        df_load_centrality_before, graph_load_centrality_layout_name_1 = plot_metric(networkGraphs, 'load_centrality', directed=directed_toggle, multi=multi_toggle, dynamic=False, layout=visualisation_layout)
        df_load_centrality_after, graph_load_centrality_layout_name_2 = plot_metric(networkGraphs2, 'load_centrality', directed=directed_toggle, multi=multi_toggle, dynamic=False, layout=visualisation_layout)
        df_load_centrality_before, graph_load_centrality_histogram_name_1 = plot_histogram(networkGraphs, 'load_centrality', directed=directed_toggle, multi=multi_toggle)
        df_load_centrality_after, graph_load_centrality_histogram_name_2 = plot_histogram(networkGraphs2, 'load_centrality', directed=directed_toggle, multi=multi_toggle)
        df_load_centrality_before, graph_load_centrality_boxplot_name_1 = plot_boxplot(networkGraphs, 'load_centrality', directed=directed_toggle, multi=multi_toggle)
        df_load_centrality_after, graph_load_centrality_boxplot_name_2 = plot_boxplot(networkGraphs2, 'load_centrality', directed=directed_toggle, multi=multi_toggle)
        df_load_centrality_before, graph_load_centrality_violinplot_name_1 = plot_violin(networkGraphs, 'load_centrality', directed=directed_toggle, multi=multi_toggle)
        df_load_centrality_after, graph_load_centrality_violinplot_name_2 = plot_violin(networkGraphs2, 'load_centrality', directed=directed_toggle, multi=multi_toggle)
            # kcore
        df_kcore_node_before, graph_kcore_node_layout_name_1 = plot_metric(networkGraphs, 'kcore', directed=directed_toggle, multi=multi_toggle, dynamic=False, layout=visualisation_layout)
        df_kcore_node_after, graph_kcore_node_layout_name_2 = plot_metric(networkGraphs2, 'kcore', directed=directed_toggle, multi=multi_toggle, dynamic=False, layout=visualisation_layout)
        df_kcore_node_before, graph_kcore_node_histogram_name_1 = plot_histogram(networkGraphs, 'kcore', directed=directed_toggle, multi=multi_toggle)
        df_kcore_node_after, graph_kcore_node_histogram_name_2 = plot_histogram(networkGraphs2, 'kcore', directed=directed_toggle, multi=multi_toggle)
        df_kcore_node_before, graph_kcore_node_boxplot_name_1 = plot_boxplot(networkGraphs, 'kcore', directed=directed_toggle, multi=multi_toggle)
        df_kcore_node_after, graph_kcore_node_boxplot_name_2 = plot_boxplot(networkGraphs2, 'kcore', directed=directed_toggle, multi=multi_toggle)
        df_kcore_node_before, graph_kcore_node_violinplot_name_1 = plot_violin(networkGraphs, 'kcore', directed=directed_toggle, multi=multi_toggle)
        df_kcore_node_after, graph_kcore_node_violinplot_name_2 = plot_violin(networkGraphs2, 'kcore', directed=directed_toggle, multi=multi_toggle)
            # degree
        df_degree_node_before, graph_degree_node_layout_name_1 = plot_metric(networkGraphs, 'degree', directed=directed_toggle, multi=multi_toggle, dynamic=False, layout=visualisation_layout)
        df_degree_node_after, graph_degree_node_layout_name_2 = plot_metric(networkGraphs2, 'degree', directed=directed_toggle, multi=multi_toggle, dynamic=False, layout=visualisation_layout)
        df_degree_node_before, graph_degree_node_histogram_name_1 = plot_histogram(networkGraphs, 'degree', directed=directed_toggle, multi=multi_toggle)
        df_degree_node_after, graph_degree_node_histogram_name_2 = plot_histogram(networkGraphs2, 'degree', directed=directed_toggle, multi=multi_toggle)
        df_degree_node_before, graph_degree_node_boxplot_name_1 = plot_boxplot(networkGraphs, 'degree', directed=directed_toggle, multi=multi_toggle)
        df_degree_node_after, graph_degree_node_boxplot_name_2 = plot_boxplot(networkGraphs2, 'degree', directed=directed_toggle, multi=multi_toggle)
        df_degree_node_before, graph_degree_node_violinplot_name_1 = plot_violin(networkGraphs, 'degree', directed=directed_toggle, multi=multi_toggle)
        df_degree_node_after, graph_degree_node_violinplot_name_2 = plot_violin(networkGraphs2, 'degree', directed=directed_toggle, multi=multi_toggle)
            # triangles
        df_triangles_node_before, graph_triangles_node_layout_name_1 = plot_metric(networkGraphs, 'triangles', directed=directed_toggle, multi=multi_toggle, dynamic=False, layout=visualisation_layout)
        df_triangles_node_after, graph_triangles_node_layout_name_2 = plot_metric(networkGraphs2, 'triangles', directed=directed_toggle, multi=multi_toggle, dynamic=False, layout=visualisation_layout)
        df_triangles_node_before, graph_triangles_node_histogram_name_1 = plot_histogram(networkGraphs, 'triangles', directed=directed_toggle, multi=multi_toggle)
        df_triangles_node_after, graph_triangles_node_histogram_name_2 = plot_histogram(networkGraphs2, 'triangles', directed=directed_toggle, multi=multi_toggle)
        df_triangles_node_before, graph_triangles_node_boxplot_name_1 = plot_boxplot(networkGraphs, 'triangles', directed=directed_toggle, multi=multi_toggle)
        df_triangles_node_after, graph_triangles_node_boxplot_name_2 = plot_boxplot(networkGraphs2, 'triangles', directed=directed_toggle, multi=multi_toggle)
        df_triangles_node_before, graph_triangles_node_violinplot_name_1 = plot_violin(networkGraphs, 'triangles', directed=directed_toggle, multi=multi_toggle)
        df_triangles_node_after, graph_triangles_node_violinplot_name_2 = plot_violin(networkGraphs2, 'triangles', directed=directed_toggle, multi=multi_toggle)
            # pagerank
        df_pagerank_node_before, graph_pagerank_node_layout_name_1 = plot_metric(networkGraphs, 'pagerank', directed=directed_toggle, multi=multi_toggle, dynamic=False, layout=visualisation_layout)
        df_pagerank_node_after, graph_pagerank_node_layout_name_2 = plot_metric(networkGraphs2, 'pagerank', directed=directed_toggle, multi=multi_toggle, dynamic=False, layout=visualisation_layout)
        df_pagerank_node_before, graph_pagerank_node_histogram_name_1 = plot_histogram(networkGraphs, 'pagerank', directed=directed_toggle, multi=multi_toggle)
        df_pagerank_node_after, graph_pagerank_node_histogram_name_2 = plot_histogram(networkGraphs2, 'pagerank', directed=directed_toggle, multi=multi_toggle)
        df_pagerank_node_before, graph_pagerank_node_boxplot_name_1 = plot_boxplot(networkGraphs, 'pagerank', directed=directed_toggle, multi=multi_toggle)
        df_pagerank_node_after, graph_pagerank_node_boxplot_name_2 = plot_boxplot(networkGraphs2, 'pagerank', directed=directed_toggle, multi=multi_toggle)
        df_pagerank_node_before, graph_pagerank_node_violinplot_name_1 = plot_violin(networkGraphs, 'pagerank', directed=directed_toggle, multi=multi_toggle)
        df_pagerank_node_after, graph_pagerank_node_violinplot_name_2 = plot_violin(networkGraphs2, 'pagerank', directed=directed_toggle, multi=multi_toggle)

        # clusters seperate condition
        if number_of_clusters is not None:
            df_louvain_before, graph_louvain_name_1 = plot_cluster(networkGraphs, 'louvain', noOfClusters=number_of_clusters,dynamic=False, layout=visualisation_layout)
            df_louvain_after, graph_louvain_name_2 = plot_cluster(networkGraphs2, 'louvain', noOfClusters=number_of_clusters,dynamic=False, layout=visualisation_layout)
            df_greedy_modularity_before, graph_greedy_modularity_name_1 = plot_cluster(networkGraphs, 'greedy_modularity', noOfClusters=number_of_clusters,dynamic=False, layout=visualisation_layout)
            df_greedy_modularity_after, graph_greedy_modularity_name_2 = plot_cluster(networkGraphs2, 'greedy_modularity', noOfClusters=number_of_clusters,dynamic=False, layout=visualisation_layout)
            df_label_propagation_before, graph_label_propagation_name_1 = plot_cluster(networkGraphs, 'label_propagation', noOfClusters=number_of_clusters,dynamic=False, layout=visualisation_layout)
            df_label_propagation_after, graph_label_propagation_name_2 = plot_cluster(networkGraphs2, 'label_propagation', noOfClusters=number_of_clusters,dynamic=False, layout=visualisation_layout)
            df_asyn_lpa_before, graph_asyn_lpa_name_1 = plot_cluster(networkGraphs, 'asyn_lpa', noOfClusters=number_of_clusters,dynamic=False, layout=visualisation_layout)
            df_asyn_lpa_after, graph_asyn_lpa_name_2 = plot_cluster(networkGraphs2, 'asyn_lpa', noOfClusters=number_of_clusters,dynamic=False, layout=visualisation_layout)
            df_k_clique_before, graph_k_clique_name_1 = plot_cluster(networkGraphs, 'spectral', noOfClusters=number_of_clusters,dynamic=False, layout=visualisation_layout)
            df_k_clique_after, graph_k_clique_name_2 = plot_cluster(networkGraphs2, 'spectral', noOfClusters=number_of_clusters,dynamic=False, layout=visualisation_layout)
            df_spectral_before, graph_spectral_name_1 = plot_cluster(networkGraphs, 'spectral', noOfClusters=number_of_clusters,dynamic=False, layout=visualisation_layout)
            df_spectral_after, graph_spectral_name_2 = plot_cluster(networkGraphs2, 'spectral', noOfClusters=number_of_clusters,dynamic=False, layout=visualisation_layout)
            df_kmeans_before, graph_kmeans_name_1 = plot_cluster(networkGraphs, 'kmeans', noOfClusters=number_of_clusters,dynamic=False, layout=visualisation_layout)
            df_kmeans_after, graph_kmeans_name_2 = plot_cluster(networkGraphs2, 'kmeans', noOfClusters=number_of_clusters,dynamic=False, layout=visualisation_layout)
            df_agglomerative_before, graph_agglomerative_name_1 = plot_cluster(networkGraphs, 'agglomerative', noOfClusters=number_of_clusters,dynamic=False, layout=visualisation_layout)
            df_agglomerative_after, graph_agglomerative_name_2 = plot_cluster(networkGraphs2, 'agglomerative', noOfClusters=number_of_clusters,dynamic=False, layout=visualisation_layout)
            df_dbscan_before, graph_dbscan_name_1 = plot_cluster(networkGraphs, 'dbscan', noOfClusters=number_of_clusters,dynamic=False, layout=visualisation_layout)
            df_dbscan_after, graph_dbscan_name_2 = plot_cluster(networkGraphs2, 'dbscan', noOfClusters=number_of_clusters,dynamic=False, layout=visualisation_layout)
        else:
            df_louvain_before, graph_louvain_name_1 = plot_cluster(networkGraphs, 'louvain', noOfClusters=0,dynamic=False, layout=visualisation_layout)                   
            df_louvain_after, graph_louvain_name_2 = plot_cluster(networkGraphs2, 'louvain', noOfClusters=0,dynamic=False, layout=visualisation_layout)                   
            df_greedy_modularity_before, graph_greedy_modularity_name_1 = plot_cluster(networkGraphs, 'greedy_modularity', noOfClusters=0,dynamic=False, layout=visualisation_layout)                   
            df_greedy_modularity_after, graph_greedy_modularity_name_2 = plot_cluster(networkGraphs2, 'greedy_modularity', noOfClusters=0,dynamic=False, layout=visualisation_layout)                   
            df_label_propagation_before, graph_label_propagation_name_1 = plot_cluster(networkGraphs, 'label_propagation', noOfClusters=0,dynamic=False, layout=visualisation_layout)                   
            df_label_propagation_after, graph_label_propagation_name_2 = plot_cluster(networkGraphs2, 'label_propagation', noOfClusters=0,dynamic=False, layout=visualisation_layout)                   
            df_asyn_lpa_before, graph_asyn_lpa_name_1 = plot_cluster(networkGraphs, 'asyn_lpa', noOfClusters=0,dynamic=False, layout=visualisation_layout)                   
            df_asyn_lpa_after, graph_asyn_lpa_name_2 = plot_cluster(networkGraphs2, 'asyn_lpa', noOfClusters=0,dynamic=False, layout=visualisation_layout)                   
            df_k_clique_before, graph_k_clique_name_1 = plot_cluster(networkGraphs, 'spectral', noOfClusters=0,dynamic=False, layout=visualisation_layout)                   
            df_k_clique_after, graph_k_clique_name_2 = plot_cluster(networkGraphs2, 'spectral', noOfClusters=0,dynamic=False, layout=visualisation_layout)
            df_spectral_before, graph_spectral_name_1 = plot_cluster(networkGraphs, 'spectral', noOfClusters=0,dynamic=False, layout=visualisation_layout)                   
            df_spectral_after, graph_spectral_name_2 = plot_cluster(networkGraphs2, 'spectral', noOfClusters=0,dynamic=False, layout=visualisation_layout)
            df_kmeans_before, graph_kmeans_name_1 = plot_cluster(networkGraphs, 'kmeans', noOfClusters=0,dynamic=False, layout=visualisation_layout)                   
            df_kmeans_after, graph_kmeans_name_2 = plot_cluster(networkGraphs2, 'kmeans', noOfClusters=0,dynamic=False, layout=visualisation_layout)
            df_agglomerative_before, graph_agglomerative_name_1 = plot_cluster(networkGraphs, 'agglomerative', noOfClusters=0,dynamic=False, layout=visualisation_layout)                   
            df_agglomerative_after, graph_agglomerative_name_2 = plot_cluster(networkGraphs2, 'agglomerative', noOfClusters=0,dynamic=False, layout=visualisation_layout)
            df_dbscan_before, graph_dbscan_name_1 = plot_cluster(networkGraphs, 'dbscan', noOfClusters=0,dynamic=False, layout=visualisation_layout)                   
            df_dbscan_after, graph_dbscan_name_2 = plot_cluster(networkGraphs2, 'dbscan', noOfClusters=0,dynamic=False, layout=visualisation_layout)
        # end POST condition

        print('no of clusters',number_of_clusters)

        # checking all graphs have graphs
        if graph_name1 == 'no_graph.html':
            graph_path1 = '../static/' + graph_name1
        else:
            graph_path1 = '../static/uploads/' + filename2 + '/' + graph_name1

        if graph_name2 == 'no_graph.html':
            graph_path2 = '../static/' + graph_name2
        else:
            graph_path2 = '../'+ networkGraphs2.session_folder + '/' + graph_name2
        
        if graph_degree_centrality_layout_name_1 == 'no_graph.html':
            graph_degree_centrality_layout_path_1 = '../static/' + graph_degree_centrality_layout_name_1
        else:
            graph_degree_centrality_layout_path_1 = '../static/uploads/' + filename2 + '/' + graph_degree_centrality_layout_name_1

        if graph_degree_centrality_layout_name_2 == 'no_graph.html':
            graph_degree_centrality_layout_path_2 = '../static/' + graph_degree_centrality_layout_name_2
        else:
            graph_degree_centrality_layout_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_degree_centrality_layout_name_2
    
        if graph_degree_centrality_histogram_name_1 == 'no_graph.html':
            graph_degree_centrality_histogram_path_1 = '../static/' + graph_degree_centrality_histogram_name_1
        else:
            graph_degree_centrality_histogram_path_1 = '../static/uploads/' + filename2 + '/' + graph_degree_centrality_histogram_name_1

        if graph_degree_centrality_histogram_name_2 == 'no_graph.html':
            graph_degree_centrality_histogram_path_2 = '../static/' + graph_degree_centrality_histogram_name_2
        else:
            graph_degree_centrality_histogram_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_degree_centrality_histogram_name_2
        
        if graph_degree_centrality_boxplot_name_1 == 'no_graph.html':
            graph_degree_centrality_boxplot_path_1 = '../static/' + graph_degree_centrality_boxplot_name_1
        else:
            graph_degree_centrality_boxplot_path_1 = '../static/uploads/' + filename2 + '/' + graph_degree_centrality_boxplot_name_1

        if graph_degree_centrality_boxplot_name_2 == 'no_graph.html':
            graph_degree_centrality_boxplot_path_2 = '../static/' + graph_degree_centrality_boxplot_name_2
        else:
            graph_degree_centrality_boxplot_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_degree_centrality_boxplot_name_2
        
        if graph_degree_centrality_violinplot_name_1 == 'no_graph.html':
            graph_degree_centrality_violinplot_path_1 = '../static/' + graph_degree_centrality_violinplot_name_1
        else:
            graph_degree_centrality_violinplot_path_1 = '../static/uploads/' + filename2 + '/' + graph_degree_centrality_violinplot_name_1

        if graph_degree_centrality_violinplot_name_2 == 'no_graph.html':
            graph_degree_centrality_violinplot_path_2 = '../static/' + graph_degree_centrality_violinplot_name_2
        else:
            graph_degree_centrality_violinplot_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_degree_centrality_violinplot_name_2
    
        # enginevector path check
        if graph_eigenvector_centrality_layout_name_1 == 'no_graph.html':
            graph_eigenvector_centrality_layout_path_1 = '../static/' + graph_eigenvector_centrality_layout_name_1
        else:
            graph_eigenvector_centrality_layout_path_1 = '../static/uploads/' + filename2 + '/' + graph_eigenvector_centrality_layout_name_1

        if graph_eigenvector_centrality_layout_name_2 == 'no_graph.html':
            graph_eigenvector_centrality_layout_path_2 = '../static/' + graph_eigenvector_centrality_layout_name_2
        else:
            graph_eigenvector_centrality_layout_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_eigenvector_centrality_layout_name_2
    
        if graph_eigenvector_centrality_histogram_name_1 == 'no_graph.html':
            graph_eigenvector_centrality_histogram_path_1 = '../static/' + graph_eigenvector_centrality_histogram_name_1
        else:
            graph_eigenvector_centrality_histogram_path_1 = '../static/uploads/' + filename2 + '/' + graph_eigenvector_centrality_histogram_name_1

        if graph_eigenvector_centrality_histogram_name_2 == 'no_graph.html':
            graph_eigenvector_centrality_histogram_path_2 = '../static/' + graph_eigenvector_centrality_histogram_name_2
        else:
            graph_eigenvector_centrality_histogram_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_eigenvector_centrality_histogram_name_2
        
        if graph_eigenvector_centrality_boxplot_name_1 == 'no_graph.html':
            graph_eigenvector_centrality_boxplot_path_1 = '../static/' + graph_eigenvector_centrality_boxplot_name_1
        else:
            graph_eigenvector_centrality_boxplot_path_1 = '../static/uploads/' + filename2 + '/' + graph_eigenvector_centrality_boxplot_name_1

        if graph_eigenvector_centrality_boxplot_name_2 == 'no_graph.html':
            graph_eigenvector_centrality_boxplot_path_2 = '../static/' + graph_eigenvector_centrality_boxplot_name_2
        else:
            graph_eigenvector_centrality_boxplot_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_eigenvector_centrality_boxplot_name_2
        
        if graph_eigenvector_centrality_violinplot_name_1 == 'no_graph.html':
            graph_eigenvector_centrality_violinplot_path_1 = '../static/' + graph_eigenvector_centrality_violinplot_name_1
        else:
            graph_eigenvector_centrality_violinplot_path_1 = '../static/uploads/' + filename2 + '/' + graph_eigenvector_centrality_violinplot_name_1

        if graph_eigenvector_centrality_violinplot_name_2 == 'no_graph.html':
            graph_eigenvector_centrality_violinplot_path_2 = '../static/' + graph_eigenvector_centrality_violinplot_name_2
        else:
            graph_eigenvector_centrality_violinplot_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_eigenvector_centrality_violinplot_name_2
    
        # closeness
        if graph_closeness_centrality_layout_name_1 == 'no_graph.html':
            graph_closeness_centrality_layout_path_1 = '../static/' + graph_closeness_centrality_layout_name_1
        else:
            graph_closeness_centrality_layout_path_1 = '../static/uploads/' + filename2 + '/' + graph_closeness_centrality_layout_name_1

        if graph_closeness_centrality_layout_name_2 == 'no_graph.html':
            graph_closeness_centrality_layout_path_2 = '../static/' + graph_closeness_centrality_layout_name_2
        else:
            graph_closeness_centrality_layout_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_closeness_centrality_layout_name_2
    
        if graph_closeness_centrality_histogram_name_1 == 'no_graph.html':
            graph_closeness_centrality_histogram_path_1 = '../static/' + graph_closeness_centrality_histogram_name_1
        else:
            graph_closeness_centrality_histogram_path_1 = '../static/uploads/' + filename2 + '/' + graph_closeness_centrality_histogram_name_1

        if graph_closeness_centrality_histogram_name_2 == 'no_graph.html':
            graph_closeness_centrality_histogram_path_2 = '../static/' + graph_closeness_centrality_histogram_name_2
        else:
            graph_closeness_centrality_histogram_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_closeness_centrality_histogram_name_2
        
        if graph_closeness_centrality_boxplot_name_1 == 'no_graph.html':
            graph_closeness_centrality_boxplot_path_1 = '../static/' + graph_closeness_centrality_boxplot_name_1
        else:
            graph_closeness_centrality_boxplot_path_1 = '../static/uploads/' + filename2 + '/' + graph_closeness_centrality_boxplot_name_1

        if graph_closeness_centrality_boxplot_name_2 == 'no_graph.html':
            graph_closeness_centrality_boxplot_path_2 = '../static/' + graph_closeness_centrality_boxplot_name_2
        else:
            graph_closeness_centrality_boxplot_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_closeness_centrality_boxplot_name_2
        
        if graph_closeness_centrality_violinplot_name_1 == 'no_graph.html':
            graph_closeness_centrality_violinplot_path_1 = '../static/' + graph_closeness_centrality_violinplot_name_1
        else:
            graph_closeness_centrality_violinplot_path_1 = '../static/uploads/' + filename2 + '/' + graph_closeness_centrality_violinplot_name_1

        if graph_closeness_centrality_violinplot_name_2 == 'no_graph.html':
            graph_closeness_centrality_violinplot_path_2 = '../static/' + graph_closeness_centrality_violinplot_name_2
        else:
            graph_closeness_centrality_violinplot_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_closeness_centrality_violinplot_name_2
    
        # betwenness
        if graph_betwenness_centrality_layout_name_1 == 'no_graph.html':
            graph_betwenness_centrality_layout_path_1 = '../static/' + graph_betwenness_centrality_layout_name_1
        else:
            graph_betwenness_centrality_layout_path_1 = '../static/uploads/' + filename2 + '/' + graph_betwenness_centrality_layout_name_1

        if graph_betwenness_centrality_layout_name_2 == 'no_graph.html':
            graph_betwenness_centrality_layout_path_2 = '../static/' + graph_betwenness_centrality_layout_name_2
        else:
            graph_betwenness_centrality_layout_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_betwenness_centrality_layout_name_2
    
        if graph_betwenness_centrality_histogram_name_1 == 'no_graph.html':
            graph_betwenness_centrality_histogram_path_1 = '../static/' + graph_betwenness_centrality_histogram_name_1
        else:
            graph_betwenness_centrality_histogram_path_1 = '../static/uploads/' + filename2 + '/' + graph_betwenness_centrality_histogram_name_1

        if graph_betwenness_centrality_histogram_name_2 == 'no_graph.html':
            graph_betwenness_centrality_histogram_path_2 = '../static/' + graph_betwenness_centrality_histogram_name_2
        else:
            graph_betwenness_centrality_histogram_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_betwenness_centrality_histogram_name_2
        
        if graph_betwenness_centrality_boxplot_name_1 == 'no_graph.html':
            graph_betwenness_centrality_boxplot_path_1 = '../static/' + graph_betwenness_centrality_boxplot_name_1
        else:
            graph_betwenness_centrality_boxplot_path_1 = '../static/uploads/' + filename2 + '/' + graph_betwenness_centrality_boxplot_name_1

        if graph_betwenness_centrality_boxplot_name_2 == 'no_graph.html':
            graph_betwenness_centrality_boxplot_path_2 = '../static/' + graph_betwenness_centrality_boxplot_name_2
        else:
            graph_betwenness_centrality_boxplot_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_betwenness_centrality_boxplot_name_2
        
        if graph_betwenness_centrality_violinplot_name_1 == 'no_graph.html':
            graph_betwenness_centrality_violinplot_path_1 = '../static/' + graph_betwenness_centrality_violinplot_name_1
        else:
            graph_betwenness_centrality_violinplot_path_1 = '../static/uploads/' + filename2 + '/' + graph_betwenness_centrality_violinplot_name_1

        if graph_betwenness_centrality_violinplot_name_2 == 'no_graph.html':
            graph_betwenness_centrality_violinplot_path_2 = '../static/' + graph_betwenness_centrality_violinplot_name_2
        else:
            graph_betwenness_centrality_violinplot_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_betwenness_centrality_violinplot_name_2
        
        # load
        if graph_load_centrality_layout_name_1 == 'no_graph.html':
            graph_load_centrality_layout_path_1 = '../static/' + graph_load_centrality_layout_name_1
        else:
            graph_load_centrality_layout_path_1 = '../static/uploads/' + filename2 + '/' + graph_load_centrality_layout_name_1

        if graph_load_centrality_layout_name_2 == 'no_graph.html':
            graph_load_centrality_layout_path_2 = '../static/' + graph_load_centrality_layout_name_2
        else:
            graph_load_centrality_layout_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_load_centrality_layout_name_2
    
        if graph_load_centrality_histogram_name_1 == 'no_graph.html':
            graph_load_centrality_histogram_path_1 = '../static/' + graph_load_centrality_histogram_name_1
        else:
            graph_load_centrality_histogram_path_1 = '../static/uploads/' + filename2 + '/' + graph_load_centrality_histogram_name_1

        if graph_load_centrality_histogram_name_2 == 'no_graph.html':
            graph_load_centrality_histogram_path_2 = '../static/' + graph_load_centrality_histogram_name_2
        else:
            graph_load_centrality_histogram_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_load_centrality_histogram_name_2
        
        if graph_load_centrality_boxplot_name_1 == 'no_graph.html':
            graph_load_centrality_boxplot_path_1 = '../static/' + graph_load_centrality_boxplot_name_1
        else:
            graph_load_centrality_boxplot_path_1 = '../static/uploads/' + filename2 + '/' + graph_load_centrality_boxplot_name_1

        if graph_load_centrality_boxplot_name_2 == 'no_graph.html':
            graph_load_centrality_boxplot_path_2 = '../static/' + graph_load_centrality_boxplot_name_2
        else:
            graph_load_centrality_boxplot_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_load_centrality_boxplot_name_2
        
        if graph_load_centrality_violinplot_name_1 == 'no_graph.html':
            graph_load_centrality_violinplot_path_1 = '../static/' + graph_load_centrality_violinplot_name_1
        else:
            graph_load_centrality_violinplot_path_1 = '../static/uploads/' + filename2 + '/' + graph_load_centrality_violinplot_name_1

        if graph_load_centrality_violinplot_name_2 == 'no_graph.html':
            graph_load_centrality_violinplot_path_2 = '../static/' + graph_load_centrality_violinplot_name_2
        else:
            graph_load_centrality_violinplot_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_load_centrality_violinplot_name_2
      
        # kcore
        if graph_kcore_node_layout_name_1 == 'no_graph.html':
            graph_kcore_node_layout_path_1 = '../static/' + graph_kcore_node_layout_name_1
        else:
            graph_kcore_node_layout_path_1 = '../static/uploads/' + filename2 + '/' + graph_kcore_node_layout_name_1

        if graph_kcore_node_layout_name_2 == 'no_graph.html':
            graph_kcore_node_layout_path_2 = '../static/' + graph_kcore_node_layout_name_2
        else:
            graph_kcore_node_layout_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_kcore_node_layout_name_2
    
        if graph_kcore_node_histogram_name_1 == 'no_graph.html':
            graph_kcore_node_histogram_path_1 = '../static/' + graph_kcore_node_histogram_name_1
        else:
            graph_kcore_node_histogram_path_1 = '../static/uploads/' + filename2 + '/' + graph_kcore_node_histogram_name_1

        if graph_kcore_node_histogram_name_2 == 'no_graph.html':
            graph_kcore_node_histogram_path_2 = '../static/' + graph_kcore_node_histogram_name_2
        else:
            graph_kcore_node_histogram_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_kcore_node_histogram_name_2
        
        if graph_kcore_node_boxplot_name_1 == 'no_graph.html':
            graph_kcore_node_boxplot_path_1 = '../static/' + graph_kcore_node_boxplot_name_1
        else:
            graph_kcore_node_boxplot_path_1 = '../static/uploads/' + filename2 + '/' + graph_kcore_node_boxplot_name_1

        if graph_kcore_node_boxplot_name_2 == 'no_graph.html':
            graph_kcore_node_boxplot_path_2 = '../static/' + graph_kcore_node_boxplot_name_2
        else:
            graph_kcore_node_boxplot_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_kcore_node_boxplot_name_2
        
        if graph_kcore_node_violinplot_name_1 == 'no_graph.html':
            graph_kcore_node_violinplot_path_1 = '../static/' + graph_kcore_node_violinplot_name_1
        else:
            graph_kcore_node_violinplot_path_1 = '../static/uploads/' + filename2 + '/' + graph_kcore_node_violinplot_name_1

        if graph_kcore_node_violinplot_name_2 == 'no_graph.html':
            graph_kcore_node_violinplot_path_2 = '../static/' + graph_kcore_node_violinplot_name_2
        else:
            graph_kcore_node_violinplot_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_kcore_node_violinplot_name_2
        
        # degree
        if graph_degree_node_layout_name_1 == 'no_graph.html':
            graph_degree_node_layout_path_1 = '../static/' + graph_degree_node_layout_name_1
        else:
            graph_degree_node_layout_path_1 = '../static/uploads/' + filename2 + '/' + graph_degree_node_layout_name_1

        if graph_degree_node_layout_name_2 == 'no_graph.html':
            graph_degree_node_layout_path_2 = '../static/' + graph_degree_node_layout_name_2
        else:
            graph_degree_node_layout_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_degree_node_layout_name_2
    
        if graph_degree_node_histogram_name_1 == 'no_graph.html':
            graph_degree_node_histogram_path_1 = '../static/' + graph_degree_node_histogram_name_1
        else:
            graph_degree_node_histogram_path_1 = '../static/uploads/' + filename2 + '/' + graph_degree_node_histogram_name_1

        if graph_degree_node_histogram_name_2 == 'no_graph.html':
            graph_degree_node_histogram_path_2 = '../static/' + graph_degree_node_histogram_name_2
        else:
            graph_degree_node_histogram_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_degree_node_histogram_name_2
        
        if graph_degree_node_boxplot_name_1 == 'no_graph.html':
            graph_degree_node_boxplot_path_1 = '../static/' + graph_degree_node_boxplot_name_1
        else:
            graph_degree_node_boxplot_path_1 = '../static/uploads/' + filename2 + '/' + graph_degree_node_boxplot_name_1

        if graph_degree_node_boxplot_name_2 == 'no_graph.html':
            graph_degree_node_boxplot_path_2 = '../static/' + graph_degree_node_boxplot_name_2
        else:
            graph_degree_node_boxplot_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_degree_node_boxplot_name_2
        
        if graph_degree_node_violinplot_name_1 == 'no_graph.html':
            graph_degree_node_violinplot_path_1 = '../static/' + graph_degree_node_violinplot_name_1
        else:
            graph_degree_node_violinplot_path_1 = '../static/uploads/' + filename2 + '/' + graph_degree_node_violinplot_name_1

        if graph_degree_node_violinplot_name_2 == 'no_graph.html':
            graph_degree_node_violinplot_path_2 = '../static/' + graph_degree_node_violinplot_name_2
        else:
            graph_degree_node_violinplot_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_degree_node_violinplot_name_2
        
        # triangles
        if graph_triangles_node_layout_name_1 == 'no_graph.html':
            graph_triangles_node_layout_path_1 = '../static/' + graph_triangles_node_layout_name_1
        else:
            graph_triangles_node_layout_path_1 = '../static/uploads/' + filename2 + '/' + graph_triangles_node_layout_name_1

        if graph_triangles_node_layout_name_2 == 'no_graph.html':
            graph_triangles_node_layout_path_2 = '../static/' + graph_triangles_node_layout_name_2
        else:
            graph_triangles_node_layout_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_triangles_node_layout_name_2
    
        if graph_triangles_node_histogram_name_1 == 'no_graph.html':
            graph_triangles_node_histogram_path_1 = '../static/' + graph_triangles_node_histogram_name_1
        else:
            graph_triangles_node_histogram_path_1 = '../static/uploads/' + filename2 + '/' + graph_triangles_node_histogram_name_1

        if graph_triangles_node_histogram_name_2 == 'no_graph.html':
            graph_triangles_node_histogram_path_2 = '../static/' + graph_triangles_node_histogram_name_2
        else:
            graph_triangles_node_histogram_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_triangles_node_histogram_name_2
        
        if graph_triangles_node_boxplot_name_1 == 'no_graph.html':
            graph_triangles_node_boxplot_path_1 = '../static/' + graph_triangles_node_boxplot_name_1
        else:
            graph_triangles_node_boxplot_path_1 = '../static/uploads/' + filename2 + '/' + graph_triangles_node_boxplot_name_1

        if graph_triangles_node_boxplot_name_2 == 'no_graph.html':
            graph_triangles_node_boxplot_path_2 = '../static/' + graph_triangles_node_boxplot_name_2
        else:
            graph_triangles_node_boxplot_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_triangles_node_boxplot_name_2
        
        if graph_triangles_node_violinplot_name_1 == 'no_graph.html':
            graph_triangles_node_violinplot_path_1 = '../static/' + graph_triangles_node_violinplot_name_1
        else:
            graph_triangles_node_violinplot_path_1 = '../static/uploads/' + filename2 + '/' + graph_triangles_node_violinplot_name_1

        if graph_triangles_node_violinplot_name_2 == 'no_graph.html':
            graph_triangles_node_violinplot_path_2 = '../static/' + graph_triangles_node_violinplot_name_2
        else:
            graph_triangles_node_violinplot_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_triangles_node_violinplot_name_2
    
        # pagerank
        if graph_pagerank_node_layout_name_1 == 'no_graph.html':
            graph_pagerank_node_layout_path_1 = '../static/' + graph_pagerank_node_layout_name_1
        else:
            graph_pagerank_node_layout_path_1 = '../static/uploads/' + filename2 + '/' + graph_pagerank_node_layout_name_1

        if graph_pagerank_node_layout_name_2 == 'no_graph.html':
            graph_pagerank_node_layout_path_2 = '../static/' + graph_pagerank_node_layout_name_2
        else:
            graph_pagerank_node_layout_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_pagerank_node_layout_name_2
    
        if graph_pagerank_node_histogram_name_1 == 'no_graph.html':
            graph_pagerank_node_histogram_path_1 = '../static/' + graph_pagerank_node_histogram_name_1
        else:
            graph_pagerank_node_histogram_path_1 = '../static/uploads/' + filename2 + '/' + graph_pagerank_node_histogram_name_1

        if graph_pagerank_node_histogram_name_2 == 'no_graph.html':
            graph_pagerank_node_histogram_path_2 = '../static/' + graph_pagerank_node_histogram_name_2
        else:
            graph_pagerank_node_histogram_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_pagerank_node_histogram_name_2
        
        if graph_pagerank_node_boxplot_name_1 == 'no_graph.html':
            graph_pagerank_node_boxplot_path_1 = '../static/' + graph_pagerank_node_boxplot_name_1
        else:
            graph_pagerank_node_boxplot_path_1 = '../static/uploads/' + filename2 + '/' + graph_pagerank_node_boxplot_name_1

        if graph_pagerank_node_boxplot_name_2 == 'no_graph.html':
            graph_pagerank_node_boxplot_path_2 = '../static/' + graph_pagerank_node_boxplot_name_2
        else:
            graph_pagerank_node_boxplot_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_pagerank_node_boxplot_name_2
        
        if graph_pagerank_node_violinplot_name_1 == 'no_graph.html':
            graph_pagerank_node_violinplot_path_1 = '../static/' + graph_pagerank_node_violinplot_name_1
        else:
            graph_pagerank_node_violinplot_path_1 = '../static/uploads/' + filename2 + '/' + graph_pagerank_node_violinplot_name_1

        if graph_pagerank_node_violinplot_name_2 == 'no_graph.html':
            graph_pagerank_node_violinplot_path_2 = '../static/' + graph_pagerank_node_violinplot_name_2
        else:
            graph_pagerank_node_violinplot_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_pagerank_node_violinplot_name_2
        
        # louvain
        if graph_louvain_name_1 == 'no_graph.html':
            graph_louvain_path_1 = '../static/' + graph_louvain_name_1
        else:
            graph_louvain_path_1 = '../static/uploads/' + filename2 + '/' + graph_louvain_name_1

        if graph_louvain_name_2 == 'no_graph.html':
            graph_louvain_path_2 = '../static/' + graph_louvain_name_2
        else:
            graph_louvain_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_louvain_name_2

        # greedy_modularity
        if graph_greedy_modularity_name_1 == 'no_graph.html':
            graph_greedy_modularity_path_1 = '../static/' + graph_greedy_modularity_name_1
        else:
            graph_greedy_modularity_path_1 = '../static/uploads/' + filename2 + '/' + graph_greedy_modularity_name_1

        if graph_greedy_modularity_name_2 == 'no_graph.html':
            graph_greedy_modularity_path_2 = '../static/' + graph_greedy_modularity_name_2
        else:
            graph_greedy_modularity_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_greedy_modularity_name_2
        
        # label_propagation
        if graph_label_propagation_name_1 == 'no_graph.html':
            graph_label_propagation_path_1 = '../static/' + graph_label_propagation_name_1
        else:
            graph_label_propagation_path_1 = '../static/uploads/' + filename2 + '/' + graph_label_propagation_name_1

        if graph_label_propagation_name_2 == 'no_graph.html':
            graph_label_propagation_path_2 = '../static/' + graph_label_propagation_name_2
        else:
            graph_label_propagation_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_label_propagation_name_2

        # asyn_lpa
        if graph_asyn_lpa_name_1 == 'no_graph.html':
            graph_asyn_lpa_path_1 = '../static/' + graph_asyn_lpa_name_1
        else:
            graph_asyn_lpa_path_1 = '../static/uploads/' + filename2 + '/' + graph_asyn_lpa_name_1

        if graph_asyn_lpa_name_2 == 'no_graph.html':
            graph_asyn_lpa_path_2 = '../static/' + graph_asyn_lpa_name_2
        else:
            graph_asyn_lpa_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_asyn_lpa_name_2

        # k_clique
        if graph_k_clique_name_1 == 'no_graph.html':
            graph_k_clique_path_1 = '../static/' + graph_k_clique_name_1
        else:
            graph_k_clique_path_1 = '../static/uploads/' + filename2 + '/' + graph_k_clique_name_1

        if graph_k_clique_name_2 == 'no_graph.html':
            graph_k_clique_path_2 = '../static/' + graph_k_clique_name_2
        else:
            graph_k_clique_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_k_clique_name_2

        # spectral
        if graph_spectral_name_1 == 'no_graph.html':
            graph_spectral_path_1 = '../static/' + graph_spectral_name_1
        else:
            graph_spectral_path_1 = '../static/uploads/' + filename2 + '/' + graph_spectral_name_1

        if graph_spectral_name_2 == 'no_graph.html':
            graph_spectral_path_2 = '../static/' + graph_spectral_name_2
        else:
            graph_spectral_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_spectral_name_2

        # kmeans
        if graph_kmeans_name_1 == 'no_graph.html':
            graph_kmeans_path_1 = '../static/' + graph_kmeans_name_1
        else:
            graph_kmeans_path_1 = '../static/uploads/' + filename2 + '/' + graph_kmeans_name_1

        if graph_kmeans_name_2 == 'no_graph.html':
            graph_kmeans_path_2 = '../static/' + graph_kmeans_name_2
        else:
            graph_kmeans_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_kmeans_name_2

        # agglomerative
        if graph_agglomerative_name_1 == 'no_graph.html':
            graph_agglomerative_path_1 = '../static/' + graph_agglomerative_name_1
        else:
            graph_agglomerative_path_1 = '../static/uploads/' + filename2 + '/' + graph_agglomerative_name_1

        if graph_agglomerative_name_2 == 'no_graph.html':
            graph_agglomerative_path_2 = '../static/' + graph_agglomerative_name_2
        else:
            graph_agglomerative_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_agglomerative_name_2

        # dbscan
        if graph_dbscan_name_1 == 'no_graph.html':
            graph_dbscan_path_1 = '../static/' + graph_dbscan_name_1
        else:
            graph_dbscan_path_1 = '../static/uploads/' + filename2 + '/' + graph_dbscan_name_1

        if graph_dbscan_name_2 == 'no_graph.html':
            graph_dbscan_path_2 = '../static/' + graph_dbscan_name_2
        else:
            graph_dbscan_path_2 = '../'+ networkGraphs2.session_folder + '/' + graph_dbscan_name_2
    else:
        graph_path1 = '../static/no_graph.html' 
        graph_path2 = '../static/no_graph.html' 
        graph_degree_centrality_layout_path_1 = '../static/no_graph.html'
        graph_degree_centrality_layout_path_2 = '../static/no_graph.html'
        graph_degree_centrality_histogram_path_1 = '../static/no_graph.html'
        graph_degree_centrality_histogram_path_2 = '../static/no_graph.html'
        graph_degree_centrality_boxplot_path_1 = '../static/no_graph.html'
        graph_degree_centrality_boxplot_path_2 = '../static/no_graph.html'
        graph_degree_centrality_violinplot_path_1 = '../static/no_graph.html'
        graph_degree_centrality_violinplot_path_2 = '../static/no_graph.html'
        df_degree_centrality_before = pd.DataFrame(0, index=range(5), columns=range(5))
        df_degree_centrality_after = pd.DataFrame(0, index=range(5), columns=range(5))

        graph_eigenvector_centrality_layout_path_1 = '../static/no_graph.html'
        graph_eigenvector_centrality_layout_path_2 = '../static/no_graph.html'
        graph_eigenvector_centrality_histogram_path_1 = '../static/no_graph.html'
        graph_eigenvector_centrality_histogram_path_2 = '../static/no_graph.html'
        graph_eigenvector_centrality_boxplot_path_1 = '../static/no_graph.html'
        graph_eigenvector_centrality_boxplot_path_2 = '../static/no_graph.html'
        graph_eigenvector_centrality_violinplot_path_1 = '../static/no_graph.html'
        graph_eigenvector_centrality_violinplot_path_2 = '../static/no_graph.html'
        df_eigenvector_centrality_before = pd.DataFrame(0, index=range(5), columns=range(5))
        df_eigenvector_centrality_after = pd.DataFrame(0, index=range(5), columns=range(5))

        graph_closeness_centrality_layout_path_1 = '../static/no_graph.html'
        graph_closeness_centrality_layout_path_2 = '../static/no_graph.html'
        graph_closeness_centrality_histogram_path_1 = '../static/no_graph.html'
        graph_closeness_centrality_histogram_path_2 = '../static/no_graph.html'
        graph_closeness_centrality_boxplot_path_1 = '../static/no_graph.html'
        graph_closeness_centrality_boxplot_path_2 = '../static/no_graph.html'
        graph_closeness_centrality_violinplot_path_1 = '../static/no_graph.html'
        graph_closeness_centrality_violinplot_path_2 = '../static/no_graph.html'
        df_closeness_centrality_before = pd.DataFrame(0, index=range(5), columns=range(5))
        df_closeness_centrality_after = pd.DataFrame(0, index=range(5), columns=range(5))

        graph_betwenness_centrality_layout_path_1 = '../static/no_graph.html'
        graph_betwenness_centrality_layout_path_2 = '../static/no_graph.html'
        graph_betwenness_centrality_histogram_path_1 = '../static/no_graph.html'
        graph_betwenness_centrality_histogram_path_2 = '../static/no_graph.html'
        graph_betwenness_centrality_boxplot_path_1 = '../static/no_graph.html'
        graph_betwenness_centrality_boxplot_path_2 = '../static/no_graph.html'
        graph_betwenness_centrality_violinplot_path_1 = '../static/no_graph.html'
        graph_betwenness_centrality_violinplot_path_2 = '../static/no_graph.html'
        df_betwenness_centrality_before = pd.DataFrame(0, index=range(5), columns=range(5))
        df_betwenness_centrality_after = pd.DataFrame(0, index=range(5), columns=range(5))

        graph_load_centrality_layout_path_1 = '../static/no_graph.html'
        graph_load_centrality_layout_path_2 = '../static/no_graph.html'
        graph_load_centrality_histogram_path_1 = '../static/no_graph.html'
        graph_load_centrality_histogram_path_2 = '../static/no_graph.html'
        graph_load_centrality_boxplot_path_1 = '../static/no_graph.html'
        graph_load_centrality_boxplot_path_2 = '../static/no_graph.html'
        graph_load_centrality_violinplot_path_1 = '../static/no_graph.html'
        graph_load_centrality_violinplot_path_2 = '../static/no_graph.html'
        df_load_centrality_before = pd.DataFrame(0, index=range(5), columns=range(5))
        df_load_centrality_after = pd.DataFrame(0, index=range(5), columns=range(5))

        graph_kcore_node_layout_path_1 = '../static/no_graph.html'
        graph_kcore_node_layout_path_2 = '../static/no_graph.html'
        graph_kcore_node_histogram_path_1 = '../static/no_graph.html'
        graph_kcore_node_histogram_path_2 = '../static/no_graph.html'
        graph_kcore_node_boxplot_path_1 = '../static/no_graph.html'
        graph_kcore_node_boxplot_path_2 = '../static/no_graph.html'
        graph_kcore_node_violinplot_path_1 = '../static/no_graph.html'
        graph_kcore_node_violinplot_path_2 = '../static/no_graph.html'
        df_kcore_node_before = pd.DataFrame(0, index=range(5), columns=range(5))
        df_kcore_node_after = pd.DataFrame(0, index=range(5), columns=range(5))
        
        graph_degree_node_layout_path_1 = '../static/no_graph.html'
        graph_degree_node_layout_path_2 = '../static/no_graph.html'
        graph_degree_node_histogram_path_1 = '../static/no_graph.html'
        graph_degree_node_histogram_path_2 = '../static/no_graph.html'
        graph_degree_node_boxplot_path_1 = '../static/no_graph.html'
        graph_degree_node_boxplot_path_2 = '../static/no_graph.html'
        graph_degree_node_violinplot_path_1 = '../static/no_graph.html'
        graph_degree_node_violinplot_path_2 = '../static/no_graph.html'
        df_degree_node_before = pd.DataFrame(0, index=range(5), columns=range(5))
        df_degree_node_after = pd.DataFrame(0, index=range(5), columns=range(5))

        graph_triangles_node_layout_path_1 = '../static/no_graph.html'  
        graph_triangles_node_layout_path_2 = '../static/no_graph.html'
        graph_triangles_node_histogram_path_1 = '../static/no_graph.html'
        graph_triangles_node_histogram_path_2 = '../static/no_graph.html'
        graph_triangles_node_boxplot_path_1 = '../static/no_graph.html'
        graph_triangles_node_boxplot_path_2 = '../static/no_graph.html'
        graph_triangles_node_violinplot_path_1 = '../static/no_graph.html'
        graph_triangles_node_violinplot_path_2 = '../static/no_graph.html'
        df_triangles_node_before = pd.DataFrame(0, index=range(5), columns=range(5))
        df_triangles_node_after = pd.DataFrame(0, index=range(5), columns=range(5))

        graph_pagerank_node_layout_path_1 = '../static/no_graph.html'  
        graph_pagerank_node_layout_path_2 = '../static/no_graph.html'
        graph_pagerank_node_histogram_path_1 = '../static/no_graph.html'
        graph_pagerank_node_histogram_path_2 = '../static/no_graph.html'
        graph_pagerank_node_boxplot_path_1 = '../static/no_graph.html'
        graph_pagerank_node_boxplot_path_2 = '../static/no_graph.html'
        graph_pagerank_node_violinplot_path_1 = '../static/no_graph.html'
        graph_pagerank_node_violinplot_path_2 = '../static/no_graph.html'
        df_pagerank_node_before = pd.DataFrame(0, index=range(5), columns=range(5))
        df_pagerank_node_after = pd.DataFrame(0, index=range(5), columns=range(5))

        graph_louvain_path_1 = '../static/no_graph.html'  
        graph_louvain_path_2 = '../static/no_graph.html'
        df_louvain_before = pd.DataFrame(0, index=range(5), columns=range(5))
        df_louvain_after = pd.DataFrame(0, index=range(5), columns=range(5))

        graph_greedy_modularity_path_1 = '../static/no_graph.html'  
        graph_greedy_modularity_path_2 = '../static/no_graph.html'
        df_greedy_modularity_before = pd.DataFrame(0, index=range(5), columns=range(5))
        df_greedy_modularity_after = pd.DataFrame(0, index=range(5), columns=range(5))

        graph_label_propagation_path_1 = '../static/no_graph.html'  
        graph_label_propagation_path_2 = '../static/no_graph.html'
        df_label_propagation_before = pd.DataFrame(0, index=range(5), columns=range(5))
        df_label_propagation_after = pd.DataFrame(0, index=range(5), columns=range(5))

        graph_asyn_lpa_path_1 = '../static/no_graph.html'  
        graph_asyn_lpa_path_2 = '../static/no_graph.html'
        df_asyn_lpa_before = pd.DataFrame(0, index=range(5), columns=range(5))
        df_asyn_lpa_after = pd.DataFrame(0, index=range(5), columns=range(5))

        graph_k_clique_path_1 = '../static/no_graph.html'  
        graph_k_clique_path_2 = '../static/no_graph.html'
        df_k_clique_before = pd.DataFrame(0, index=range(5), columns=range(5))
        df_k_clique_after = pd.DataFrame(0, index=range(5), columns=range(5))

        graph_spectral_path_1 = '../static/no_graph.html'  
        graph_spectral_path_2 = '../static/no_graph.html'
        df_spectral_before = pd.DataFrame(0, index=range(5), columns=range(5))
        df_spectral_after = pd.DataFrame(0, index=range(5), columns=range(5))

        graph_kmeans_path_1 = '../static/no_graph.html'  
        graph_kmeans_path_2 = '../static/no_graph.html'
        df_kmeans_before = pd.DataFrame(0, index=range(5), columns=range(5))
        df_kmeans_after = pd.DataFrame(0, index=range(5), columns=range(5))

        graph_agglomerative_path_1 = '../static/no_graph.html'  
        graph_agglomerative_path_2 = '../static/no_graph.html'
        df_agglomerative_before = pd.DataFrame(0, index=range(5), columns=range(5))
        df_agglomerative_after = pd.DataFrame(0, index=range(5), columns=range(5))

        graph_dbscan_path_1 = '../static/no_graph.html'  
        graph_dbscan_path_2 = '../static/no_graph.html'
        df_dbscan_before = pd.DataFrame(0, index=range(5), columns=range(5))
        df_dbscan_after = pd.DataFrame(0, index=range(5), columns=range(5))


   
    return render_template(template_name_arg, tab_main=tab_main_arg, visualisation_layout=visualisation_layout, number_of_threashold=number_of_threashold_arg,
        number_of_nodes=number_of_nodes_arg, number_of_edges=number_of_edges_arg, graph1=graph_path1, graph2=graph_path2, layout=layout_arg, layout2=layout2_arg,
        multi_toggle=multi_toggle,directed_toggle=directed_toggle, number_of_clusters=number_of_clusters,
        df_degree_centrality_before=df_degree_centrality_before, df_degree_centrality_after=df_degree_centrality_after, 
        graph_degree_centrality_layout_1=graph_degree_centrality_layout_path_1, graph_degree_centrality_layout_2=graph_degree_centrality_layout_path_2,
        graph_degree_centrality_histogram_1=graph_degree_centrality_histogram_path_1, graph_degree_centrality_histogram_2=graph_degree_centrality_histogram_path_2,
        graph_degree_centrality_boxplot_1=graph_degree_centrality_boxplot_path_1, graph_degree_centrality_boxplot_2=graph_degree_centrality_boxplot_path_2,
        graph_degree_centrality_violinplot_1=graph_degree_centrality_violinplot_path_1, graph_degree_centrality_violinplot_2=graph_degree_centrality_violinplot_path_2,
        
        df_eigenvector_centrality_before=df_eigenvector_centrality_before, df_eigenvector_centrality_after=df_eigenvector_centrality_after, 
        graph_eigenvector_centrality_layout_1=graph_eigenvector_centrality_layout_path_1, graph_eigenvector_centrality_layout_2=graph_eigenvector_centrality_layout_path_2,
        graph_eigenvector_centrality_histogram_1=graph_eigenvector_centrality_histogram_path_1, graph_eigenvector_centrality_histogram_2=graph_eigenvector_centrality_histogram_path_2,
        graph_eigenvector_centrality_boxplot_1=graph_eigenvector_centrality_boxplot_path_1, graph_eigenvector_centrality_boxplot_2=graph_eigenvector_centrality_boxplot_path_2,
        graph_eigenvector_centrality_violinplot_1=graph_eigenvector_centrality_violinplot_path_1, graph_eigenvector_centrality_violinplot_2=graph_eigenvector_centrality_violinplot_path_2,

        df_closeness_centrality_before=df_closeness_centrality_before, df_closeness_centrality_after=df_closeness_centrality_after, 
        graph_closeness_centrality_layout_1=graph_closeness_centrality_layout_path_1, graph_closeness_centrality_layout_2=graph_closeness_centrality_layout_path_2,
        graph_closeness_centrality_histogram_1=graph_closeness_centrality_histogram_path_1, graph_closeness_centrality_histogram_2=graph_closeness_centrality_histogram_path_2,
        graph_closeness_centrality_boxplot_1=graph_closeness_centrality_boxplot_path_1, graph_closeness_centrality_boxplot_2=graph_closeness_centrality_boxplot_path_2,
        graph_closeness_centrality_violinplot_1=graph_closeness_centrality_violinplot_path_1, graph_closeness_centrality_violinplot_2=graph_closeness_centrality_violinplot_path_2,

        df_betwenness_centrality_before=df_betwenness_centrality_before, df_betwenness_centrality_after=df_betwenness_centrality_after, 
        graph_betwenness_centrality_layout_1=graph_betwenness_centrality_layout_path_1, graph_betwenness_centrality_layout_2=graph_betwenness_centrality_layout_path_2,
        graph_betwenness_centrality_histogram_1=graph_betwenness_centrality_histogram_path_1, graph_betwenness_centrality_histogram_2=graph_betwenness_centrality_histogram_path_2,
        graph_betwenness_centrality_boxplot_1=graph_betwenness_centrality_boxplot_path_1, graph_betwenness_centrality_boxplot_2=graph_betwenness_centrality_boxplot_path_2,
        graph_betwenness_centrality_violinplot_1=graph_betwenness_centrality_violinplot_path_1, graph_betwenness_centrality_violinplot_2=graph_betwenness_centrality_violinplot_path_2,

        df_load_centrality_before=df_load_centrality_before, df_load_centrality_after=df_load_centrality_after, 
        graph_load_centrality_layout_1=graph_load_centrality_layout_path_1, graph_load_centrality_layout_2=graph_load_centrality_layout_path_2,
        graph_load_centrality_histogram_1=graph_load_centrality_histogram_path_1, graph_load_centrality_histogram_2=graph_load_centrality_histogram_path_2,
        graph_load_centrality_boxplot_1=graph_load_centrality_boxplot_path_1, graph_load_centrality_boxplot_2=graph_load_centrality_boxplot_path_2,
        graph_load_centrality_violinplot_1=graph_load_centrality_violinplot_path_1, graph_load_centrality_violinplot_2=graph_load_centrality_violinplot_path_2,
        
        df_kcore_node_before=df_kcore_node_before, df_kcore_node_after=df_kcore_node_after, 
        graph_kcore_node_layout_1=graph_kcore_node_layout_path_1, graph_kcore_node_layout_2=graph_kcore_node_layout_path_2,
        graph_kcore_node_histogram_1=graph_kcore_node_histogram_path_1, graph_kcore_node_histogram_2=graph_kcore_node_histogram_path_2,
        graph_kcore_node_boxplot_1=graph_kcore_node_boxplot_path_1, graph_kcore_node_boxplot_2=graph_kcore_node_boxplot_path_2,
        graph_kcore_node_violinplot_1=graph_kcore_node_violinplot_path_1, graph_kcore_node_violinplot_2=graph_kcore_node_violinplot_path_2,

        df_degree_node_before=df_degree_node_before, df_degree_node_after=df_degree_node_after, 
        graph_degree_node_layout_1=graph_degree_node_layout_path_1, graph_degree_node_layout_2=graph_degree_node_layout_path_2,
        graph_degree_node_histogram_1=graph_degree_node_histogram_path_1, graph_degree_node_histogram_2=graph_degree_node_histogram_path_2,
        graph_degree_node_boxplot_1=graph_degree_node_boxplot_path_1, graph_degree_node_boxplot_2=graph_degree_node_boxplot_path_2,
        graph_degree_node_violinplot_1=graph_degree_node_violinplot_path_1, graph_degree_node_violinplot_2=graph_degree_node_violinplot_path_2,

        df_triangles_node_before=df_triangles_node_before, df_triangles_node_after=df_triangles_node_after, 
        graph_triangles_node_layout_1=graph_triangles_node_layout_path_1, graph_triangles_node_layout_2=graph_triangles_node_layout_path_2,
        graph_triangles_node_histogram_1=graph_triangles_node_histogram_path_1, graph_triangles_node_histogram_2=graph_triangles_node_histogram_path_2,
        graph_triangles_node_boxplot_1=graph_triangles_node_boxplot_path_1, graph_triangles_node_boxplot_2=graph_triangles_node_boxplot_path_2,
        graph_triangles_node_violinplot_1=graph_triangles_node_violinplot_path_1, graph_triangles_node_violinplot_2=graph_triangles_node_violinplot_path_2,

        df_pagerank_node_before=df_pagerank_node_before, df_pagerank_node_after=df_pagerank_node_after, 
        graph_pagerank_node_layout_1=graph_pagerank_node_layout_path_1, graph_pagerank_node_layout_2=graph_pagerank_node_layout_path_2,
        graph_pagerank_node_histogram_1=graph_pagerank_node_histogram_path_1, graph_pagerank_node_histogram_2=graph_pagerank_node_histogram_path_2,
        graph_pagerank_node_boxplot_1=graph_pagerank_node_boxplot_path_1, graph_pagerank_node_boxplot_2=graph_pagerank_node_boxplot_path_2,
        graph_pagerank_node_violinplot_1=graph_pagerank_node_violinplot_path_1, graph_pagerank_node_violinplot_2=graph_pagerank_node_violinplot_path_2,
        
        df_louvain_before=df_louvain_before, df_louvain_after=df_louvain_after,
        graph_louvain_1=graph_louvain_path_1, graph_louvain_2=graph_louvain_path_2,
        
        df_greedy_modularity_before=df_greedy_modularity_before, df_greedy_modularity_after=df_greedy_modularity_after,
        graph_greedy_modularity_1=graph_greedy_modularity_path_1, graph_greedy_modularity_2=graph_greedy_modularity_path_2,

        df_label_propagation_before=df_label_propagation_before, df_label_propagation_after=df_label_propagation_after,
        graph_label_propagation_1=graph_label_propagation_path_1, graph_label_propagation_2=graph_label_propagation_path_2,

        df_asyn_lpa_before=df_asyn_lpa_before, df_asyn_lpa_after=df_asyn_lpa_after,
        graph_asyn_lpa_1=graph_asyn_lpa_path_1, graph_asyn_lpa_2=graph_asyn_lpa_path_2,

        df_k_clique_before=df_k_clique_before, df_k_clique_after=df_k_clique_after,
        graph_k_clique_1=graph_k_clique_path_1, graph_k_clique_2=graph_k_clique_path_2,

        df_spectral_before=df_spectral_before, df_spectral_after=df_spectral_after,
        graph_spectral_1=graph_spectral_path_1, graph_spectral_2=graph_spectral_path_2,

        df_kmeans_before=df_kmeans_before, df_kmeans_after=df_kmeans_after,
        graph_kmeans_1=graph_kmeans_path_1, graph_kmeans_2=graph_kmeans_path_2,

        df_agglomerative_before=df_agglomerative_before, df_agglomerative_after=df_agglomerative_after,
        graph_agglomerative_1=graph_agglomerative_path_1, graph_agglomerative_2=graph_agglomerative_path_2,

        df_dbscan_before=df_dbscan_before, df_dbscan_after=df_dbscan_after,
        graph_dbscan_1=graph_dbscan_path_1, graph_dbscan_2=graph_dbscan_path_2)