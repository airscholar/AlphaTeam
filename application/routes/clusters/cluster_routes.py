import sys

import requests
from application.dictionary.information import *
from flask import Blueprint, render_template, session, request

sys.path.insert(1, '../../')
from src.metrics import *

cluster_routes = Blueprint('cluster_routes', __name__)

# -------------------------------------------ML-CLUSTERING-----------------------------------
BASE_URL = 'http://localhost:8000/api/v1/clusters/'

@cluster_routes.route('/clustering/louvain', endpoint='clustering_louvanian', methods=['GET', 'POST'])
def clustering_louvanian():
    filename2 = session['filename2']
    clusterType = 'louvain'
    
    return render_template('clusters/clustering_louvanian.html', session_id=filename2, clusterType=clusterType, method_name='Louvain',
    #tooltips starts from here
    description=description['louvain'], tooltip_dynamic=tooltips['dynamic'],
    tooltip_layout=tooltips['layout_dropdown'], tooltip_number_of_clusters=tooltips['number_of_clusters'])


@cluster_routes.route('/clustering/greedy_modularity', endpoint='clustering_greedy_modularity', methods=['GET', 'POST'])
def clustering_greedy_modularity():
    filename2 = session['filename2']
    clusterType = 'greedy_modularity'
    
    return render_template('clusters/clustering_greedy_modularity.html', session_id=filename2, clusterType=clusterType, method_name='Greedy Modularity',
    #tooltips starts from here
    description=description['greedy_modularity'], tooltip_dynamic=tooltips['dynamic'],
    tooltip_layout=tooltips['layout_dropdown'], tooltip_number_of_clusters=tooltips['number_of_clusters'])



@cluster_routes.route('/clustering/label_propagation', endpoint='clustering_label_propagation', methods=['GET', 'POST'])
def clustering_label_propagation():
    filename2 = session['filename2']
    clusterType = 'label_propagation'
    
    return render_template('clusters/clustering_label_propagation.html', session_id=filename2, clusterType=clusterType, method_name='Label Propagation',
    #tooltips starts from here
    description=description['label_propagation'], tooltip_dynamic=tooltips['dynamic'],
    tooltip_layout=tooltips['layout_dropdown'], tooltip_number_of_clusters=tooltips['number_of_clusters'])


@cluster_routes.route('/clustering/asyn_lpa', endpoint='clustering_asyn_lpa', methods=['GET', 'POST'])
def clustering_asyn_lpa():
    filename2 = session['filename2']
    clusterType = 'asyn_lpa'
    
    return render_template('clusters/clustering_asyn_lpa.html', session_id=filename2, clusterType=clusterType, method_name='Asyn Lpa',
    #tooltips starts from here
    description=description['asyn_lpa'], tooltip_dynamic=tooltips['dynamic'],
    tooltip_layout=tooltips['layout_dropdown'], tooltip_number_of_clusters=tooltips['number_of_clusters'])

@cluster_routes.route('/clustering/k_clique', endpoint='clustering_k_clique', methods=['GET', 'POST'])
def clustering_k_clique():
    filename2 = session['filename2']
    clusterType = 'k_clique'
    
    return render_template('clusters/clustering_k_clique.html', session_id=filename2, clusterType=clusterType, method_name='K Clique',
    #tooltips starts from here
    description=description['k_clique'], tooltip_dynamic=tooltips['dynamic'],
    tooltip_layout=tooltips['layout_dropdown'], tooltip_number_of_clusters=tooltips['number_of_clusters'])

@cluster_routes.route('/clustering/spectral', endpoint='clustering_spectral', methods=['GET', 'POST'])
def clustering_spectral():
    filename2 = session['filename2']
    clusterType = 'spectral'
    
    return render_template('clusters/clustering_spectral.html', session_id=filename2, clusterType=clusterType, method_name='Spectral',
    #tooltips starts from here
    description=description['spectral'], tooltip_dynamic=tooltips['dynamic'],
    tooltip_layout=tooltips['layout_dropdown'], tooltip_number_of_clusters=tooltips['number_of_clusters'])

@cluster_routes.route('/clustering/kmeans', endpoint='clustering_kmeans', methods=['GET', 'POST'])
def clustering_kmeans():
    filename2 = session['filename2']
    clusterType = 'kmeans'
    
    return render_template('clusters/clustering_kmeans.html', session_id=filename2, clusterType=clusterType, method_name='KMeans',
    #tooltips starts from here
    description=description['kmeans'], tooltip_dynamic=tooltips['dynamic'],
    tooltip_layout=tooltips['layout_dropdown'], tooltip_number_of_clusters=tooltips['number_of_clusters'])

@cluster_routes.route('/clustering/agglomerative', endpoint='clustering_agglomerative', methods=['GET', 'POST'])
def clustering_agglomerative():
    filename2 = session['filename2']
    clusterType = 'agglomerative'
    
    return render_template('clusters/clustering_agglomerative.html', session_id=filename2, clusterType=clusterType, method_name='Agglomerative',
    #tooltips starts from here
    description=description['agglomerative'], tooltip_dynamic=tooltips['dynamic'],
    tooltip_layout=tooltips['layout_dropdown'], tooltip_number_of_clusters=tooltips['number_of_clusters'])


@cluster_routes.route('/clustering/dbscan', endpoint='clustering_dbscan', methods=['GET', 'POST'])
def clustering_dbscan():
    filename2 = session['filename2']
    clusterType = 'dbscan'
    
    return render_template('clusters/clustering_dbscan.html', session_id=filename2, clusterType=clusterType, method_name='Dbscan',
    #tooltips starts from here
    description=description['dbscan'], tooltip_dynamic=tooltips['dynamic'],
    tooltip_layout=tooltips['layout_dropdown'], tooltip_number_of_clusters=tooltips['number_of_clusters'])
