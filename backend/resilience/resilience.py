from flask import Blueprint, request
from flask_jsonpify import jsonify

from src.resilience import resilience
from src.utils import get_networkGraph
from src.visualisation import *

resilience_bp = Blueprint('resilience', __name__, url_prefix="/api/v1/resilience")


def extract_args():
    args = request.args

    attack_type = args.get('attack_type')
    number_of_nodes_malicious = args.get('number_of_nodes_malicious')
    number_of_threshold = args.get('number_of_threshold')
    operator = args.get('operator')
    directed_toggle = args.get('directed_toggle')
    multi_toggle = args.get('multi_toggle')
    layout = args.get('layout')

    return attack_type, number_of_nodes_malicious, number_of_threshold, operator, directed_toggle, multi_toggle, layout


@resilience_bp.route('<session_id>/malicious')
def compute_malicious(session_id):
    attack_type, number_of_nodes_malicious, number_of_threshold, \
        operator, directed_toggle, multi_toggle, layout = extract_args()

    networkGraphs = get_networkGraph(session_id)

    networkGraphs2, df = resilience(networkGraphs, attack='malicious', metric=attack_type,
                                    number_of_nodes=number_of_nodes_malicious, threshold=number_of_threshold,
                                    operator=operator)

    before = plot_network(networkGraphs, layout=layout, dynamic=False, fullPath=True)
    after = plot_network(networkGraphs2, layout=layout, dynamic=False, fullPath=True)

    df_json = df.to_json(orient='split')

    return jsonify({"message": "Success", "data": df_json, "network_before": before, "network_after": after})


@resilience_bp.route('<session_id>/<metric>/<plot_type>')
def compute_metrics(session_id, metric, plot_type):
    attack_type, number_of_nodes_malicious, number_of_threshold, \
        operator, directed_toggle, multi_toggle, layout = extract_args()

    networkGraphs = get_networkGraph(session_id)

    networkGraphs2, _ = resilience(networkGraphs, attack='malicious', metric=metric,
                                   number_of_nodes=number_of_nodes_malicious, threshold=number_of_threshold,
                                   operator=operator)
    df = None
    df1 = None
    file_name = None
    file_name1 = None

    if plot_type == 'layout':
        df, file_name = plot_metric(networkGraphs, metric, directed=directed_toggle, multi=multi_toggle,
                                    layout=layout, fullPath=True)
        df1, file_name1 = plot_metric(networkGraphs2, metric, directed=directed_toggle, multi=multi_toggle,
                                      layout=layout, fullPath=True)
    elif plot_type == 'histogram':
        df, file_name = plot_histogram(networkGraphs, metric, directed=directed_toggle, multi=multi_toggle, fullPath=True)
        df1, file_name1 = plot_histogram(networkGraphs2, metric, directed=directed_toggle, multi=multi_toggle, fullPath=True)
    elif plot_type == 'boxplot':
        df, file_name = plot_boxplot(networkGraphs, metric, directed=directed_toggle, multi=multi_toggle, fullPath=True)
        df1, file_name1 = plot_boxplot(networkGraphs2, metric, directed=directed_toggle, multi=multi_toggle, fullPath=True)
    elif plot_type == 'violin':
        df, file_name = plot_violin(networkGraphs, metric, directed=directed_toggle, multi=multi_toggle, fullPath=True)
        df1, file_name1 = plot_violin(networkGraphs2, metric, directed=directed_toggle, multi=multi_toggle, fullPath=True)

    df_json = df.to_json(orient='split')
    df_json1 = df1.to_json(orient='split')
    return jsonify({"message": "Success", "data_before": df_json, "data_after": df_json1, "network_before": file_name,
                    "network_after": file_name1})

@resilience_bp.route('<session_id>/<cluster_type>')
def compute_cluster(session_id, cluster_type):
    attack_type, number_of_nodes_malicious, number_of_threshold, \
        operator, directed_toggle, multi_toggle, layout = extract_args()

    networkGraphs = get_networkGraph(session_id)

    networkGraphs2, _ = resilience(networkGraphs, attack='malicious', metric=metric,
                                   number_of_nodes=number_of_nodes_malicious, threshold=number_of_threshold,
                                   operator=operator)
    df = None
    df1 = None
    file_name = None
    file_name1 = None

    if cluster_type == 'louvain':
        df, file_name = plot_cluster(networkGraphs, 'louvain', noOfClusters=0, dynamic=False, layout=layout, fullPath=True)
        df1, file_name1 = plot_cluster(networkGraphs, 'louvain', noOfClusters=0, dynamic=False, layout=layout, fullPath=True)
    elif cluster_type == 'greedy_modularity':
        df, file_name = plot_histogram(networkGraphs, metric, directed=directed_toggle, multi=multi_toggle, fullPath=True)
        df1, file_name1 = plot_histogram(networkGraphs2, metric, directed=directed_toggle, multi=multi_toggle, fullPath=True)
   
    df_json = df.to_json(orient='split')
    df_json1 = df1.to_json(orient='split')
    return jsonify({"message": "Success", "data_before": df_json, "data_after": df_json1, "network_before": file_name,
                    "network_after": file_name1})

df_louvain_before, graph_louvain_name_1 = plot_cluster(networkGraphs, 'louvain', noOfClusters=0,dynamic=False, layout=visualisation_layout)                   
            df_louvain_after, graph_louvain_name_2 = plot_cluster(networkGraphs2, 'louvain', noOfClusters=0,dynamic=False, layout=visualisation_layout)                   
            df_greedy_modularity_before, graph_greedy_modularity_name_1 = plot_cluster(networkGraphs, 'greedy_modularity', noOfClusters=0,dynamic=False, layout=visualisation_layout)                   
            df_greedy_modularity_after, graph_greedy_modularity_name_2 = plot_cluster(networkGraphs2, 'greedy_modularity', noOfClusters=0,dynamic=False, layout=visualisation_layout)                   
            df_label_propagation_before, graph_label_propagation_name_1 = plot_cluster(networkGraphs, 'label_propagation', noOfClusters=0,dynamic=False, layout=visualisation_layout)                   
            df_label_propagation_after, graph_label_propagation_name_2 = plot_cluster(networkGraphs2, 'label_propagation', noOfClusters=0,dynamic=False, layout=visualisation_layout)                   
            df_asyn_lpa_before, graph_asyn_lpa_name_1 = plot_cluster(networkGraphs, 'asyn_lpa', noOfClusters=0,dynamic=False, layout=visualisation_layout)                   
            df_asyn_lpa_after, graph_asyn_lpa_name_2 = plot_cluster(networkGraphs2, 'asyn_lpa', noOfClusters=0,dynamic=False, layout=visualisation_layout)                   
            df_k_clique_before, graph_k_clique_name_1 = plot_cluster(networkGraphs, 'k_clique', noOfClusters=0,dynamic=False, layout=visualisation_layout)                   
            df_k_clique_after, graph_k_clique_name_2 = plot_cluster(networkGraphs2, 'k_clique', noOfClusters=0,dynamic=False, layout=visualisation_layout)
            df_spectral_before, graph_spectral_name_1 = plot_cluster(networkGraphs, 'spectral', noOfClusters=0,dynamic=False, layout=visualisation_layout)                   
            df_spectral_after, graph_spectral_name_2 = plot_cluster(networkGraphs2, 'spectral', noOfClusters=0,dynamic=False, layout=visualisation_layout)
            df_kmeans_before, graph_kmeans_name_1 = plot_cluster(networkGraphs, 'kmeans', noOfClusters=0,dynamic=False, layout=visualisation_layout)                   
            df_kmeans_after, graph_kmeans_name_2 = plot_cluster(networkGraphs2, 'kmeans', noOfClusters=0,dynamic=False, layout=visualisation_layout)
            df_agglomerative_before, graph_agglomerative_name_1 = plot_cluster(networkGraphs, 'agglomerative', noOfClusters=0,dynamic=False, layout=visualisation_layout)                   
            df_agglomerative_after, graph_agglomerative_name_2 = plot_cluster(networkGraphs2, 'agglomerative', noOfClusters=0,dynamic=False, layout=visualisation_layout)
            df_dbscan_before, graph_dbscan_name_1 = plot_cluster(networkGraphs, 'dbscan', noOfClusters=0,dynamic=False, layout=visualisation_layout)                   
            df_dbscan_after, graph_dbscan_name_2 = plot_cluster(networkGraphs2, 'dbscan', noOfClusters=0,dynamic=False, layout=visualisation_layout)
        