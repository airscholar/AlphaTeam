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
    layout = 'degree_centrality'
    layout2 = 'equal_to'
    tab_main = 'tab1'
    
    if request.method == 'POST':
        number_of_levels = request.form.get('number_of_levels', None)
        number_of_levels = int(number_of_levels) if number_of_levels else None
        number_of_threashold = request.form.get('number_of_threashold', None)
        layout2 = request.form.get('layout2')
        number_of_threashold = int(number_of_threashold) if number_of_threashold else None
        layout = request.form.get('layout')
    else:
        number_of_levels = None
        number_of_threashold = None
        session['val1'] = None
        session['val2'] = None

    val1 = session.get('val1', None)
    val2 = session.get('val2', None)
    if val1 != number_of_levels:
        session['val1'] = number_of_levels
        tab_main = 'tab1'
    if val2 != number_of_threashold:
        session['val2'] = number_of_threashold
        tab_main = 'tab2'
 
    return render_template('resilience/resilience_analyisis_malicious.html', tab_main=tab_main, 
    layout=layout, layout2=layout2, number_of_levels=number_of_levels, number_of_threashold=number_of_threashold)

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
    tab_main = 'tab1'
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    number_of_nodes = session.get('number_of_nodes', None)
    number_of_edges = session.get('number_of_edges', None)

    val1 = session.get('val1', None)
    val2 = session.get('val2', None)
    
    # here we use number of nodes
    if val1 != number_of_nodes:
        session['val1'] = number_of_nodes
        tab_main = 'tab1'
        global networkGraphs2
        networkGraphs2 = resilience(networkGraphs, attack='random', number_of_nodes=int(number_of_nodes))
    
    # here we use number of edges
    if val2 != number_of_edges:
        session['val2'] = number_of_edge
        tab_main = 'tab2'

    print('number_of_nodes',number_of_nodes)
     
    return template_resilience_tabs('resilience/resilience_analyisis_random.html', number_of_nodes, number_of_edges, tab_main)
    #return render_template('resilience/resilience_analyisis_random.html', tab_main=tab_main, number_of_nodes=number_of_nodes, number_of_edges=number_of_edges)

def template_resilience_tabs(template_name_arg, number_of_nodes_arg, number_of_edges_arg, tab_main_arg):
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    multi_toggle = True
    directed_toggle = True
    if networkGraphs.is_spatial():
        visualisation_layout = 'map'
    else:
        visualisation_layout = 'sfdp'
    
    if networkGraphs2 is not None:
        # check POST condition
        if request.method == 'POST':
            visualisation_layout = request.form.get('visualisation_layout')
            multi_toggle = bool(request.form.get('multi_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
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

        # end POST condition

        print('visualisation layout',visualisation_layout)

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

    return render_template(template_name_arg, tab_main=tab_main_arg, visualisation_layout=visualisation_layout,
        number_of_nodes=number_of_nodes_arg, number_of_edges=number_of_edges_arg, graph1=graph_path1, graph2=graph_path2,
        multi_toggle=multi_toggle,directed_toggle=directed_toggle,
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
        graph_pagerank_node_violinplot_1=graph_pagerank_node_violinplot_path_1, graph_pagerank_node_violinplot_2=graph_pagerank_node_violinplot_path_2)







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