"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Resilience of the network
"""

# -------------------------------------- IMPORT ---------------------------------------------

import random

import src.machineLearning as ml
from src.NetworkGraphs import NetworkGraphs
<<<<<<< Updated upstream
=======
from src.preprocessing import convert_to_DiGraph
from src.visualisation import plot_cluster
>>>>>>> Stashed changes

# -------------------------------------- FUNCTIONS -------------------------------------------



def resilience(networkGraph, attack, **kwargs):
    """
    :Function: Compute the resilience of the networkGraph
    Attack can be:
        - "random"
        - "malicious"
        - "cluster"
    Args of the attacks:
        - "random":
            - "number_of_nodes": Number of nodes to be removed
            - "number_of_edges": Number of edges to be removed
        - "malicious":
            - "metric": Metric to be used to select the nodes to be removed
            - "number_of_nodes": Number of nodes to be removed
            - "threshold": Threshold to be used to select the nodes to be removed
        - "cluster":
            - "cluster_algorithm": Algorithm to be used to compute the clusters
            - "total_clusters": Total number of clusters to be generated
            - "number_of_clusters": Number of clusters to be removed
    :param networkGraph: NetworkGraph
    :type networkGraph: NetworkGraph
    :param attack: Attack to be performed
    :type attack: str
    :param kwargs: Arguments of the attack to be performed
    :type kwargs: dict
    :return: NetworkGraph with the nodes removed
    :rtype: NetworkGraph
    """
    return 0


# ------------------------------------------------------------------------------------------


def resilience_random(networkGraph, number_of_nodes, number_of_edges):
    """
    :Function: Compute the resilience of the networkGraph using the random attack
    :param networkGraph: NetworkGraph
    :type networkGraph: NetworkGraph
    :param number_of_nodes: Number of nodes to be removed
    :type number_of_nodes: int
    :param number_of_edges: Number of edges to be removed
    :type number_of_edges: int
    :return: NetworkGraph with the nodes removed
    :rtype: NetworkGraph
    """
    return 0


# ------------------------------------------------------------------------------------------


def resilience_malicious(networkGraph, metric, number_of_nodes, threshold):
    """
    :Function: Compute the resilience of the networkGraph using the malicious attack
    :param networkGraph: NetworkGraph
    :type networkGraph: NetworkGraph
    :param metric: Metric to be used to select the nodes to be removed
    :type metric: str
    :param number_of_nodes: Number of nodes to be removed
    :type number_of_nodes: int
    :param threshold: Threshold to be used to select the nodes to be removed
    :type threshold: float
    :return: NetworkGraph with the nodes removed
    :rtype: NetworkGraph
    """
    return 0


# ------------------------------------------------------------------------------------------


def resilience_cluster(networkGraph, cluster_algorithm, total_clusters, number_of_clusters):
    """
    :Function: Compute the resilience of the networkGraph using the cluster attack
    :param networkGraph: NetworkGraph
    :type networkGraph: NetworkGraph
    :param cluster_algorithm: Algorithm to be used to compute the clusters
    :type cluster_algorithm: str
    :param total_clusters: Total number of clusters to be generated
    :type total_clusters: int
    :param number_of_clusters: Number of clusters to be removed
    :type number_of_clusters: int
    :return: NetworkGraph with the nodes removed
    :rtype: NetworkGraph
    """
    G = copy_networkGraph(networkGraph)
    if cluster_algorithm not in ['louvain', 'greedy_modularity', 'label_propagation', 'asyn_lpa',
                                 'k_clique', 'spectral', 'kmeans', 'agglomerative', 'hierarchical', 'dbscan']:
        print(ValueError("Invalid cluster type", "please choose from the following: 'louvain', 'greedy_modularity', "
                                                 "'label_propagation', 'asyn_lpa',"
                                                 "'k_clique', 'spectral', 'kmeans' "
                                                 "'agglomerative', 'hierarchical', 'dbscan'"))
        return 0

    if number_of_clusters > total_clusters:
        print(ValueError("Invalid number of clusters",
                         "please choose a number of clusters smaller than the total number of clusters"))
        return 0
    elif number_of_clusters <= 0:
        print(ValueError("Invalid number of clusters, please choose a positive number"))
        return 0

    clusters = ml.get_communities(G, cluster_algorithm, total_clusters)

    if number_of_clusters > 0:
        cluster_ids = clusters['Cluster_id'].unique()
        cluster_ids = random.sample(sorted(cluster_ids), number_of_clusters)
        clusters_to_remove = clusters[clusters['Cluster_id'].isin(cluster_ids)]
        nodes_to_remove = []
        for cluster in clusters_to_remove.iterrows():
            nodes_to_remove.append(cluster[1]['Node'])
        networkGraph = remove_nodes(G, nodes_to_remove)

    return networkGraph


# ------------------------------------------------------------------------------------------


def copy_networkGraph(networkGraph):
    """
    :Function: Copy the networkGraph object
    :param neworkGraph: NetworkGraph
    :type neworkGraph: NetworkGraph
    :return: Copy of the networkGraph
    :rtype: NetworkGraph
    """
<<<<<<< Updated upstream
    return 0
=======
    if networkGraph.session_folder not in idx.keys():
        idx[networkGraph.session_folder] = 0
    else:
        idx[networkGraph.session_folder] = idx[networkGraph.session_folder] + 1
    session_folder = f'{networkGraph.session_folder}/resilience{idx[networkGraph.session_folder]}'
    return NetworkGraphs(networkGraph.filename, type=networkGraph.type, session_folder=session_folder)
>>>>>>> Stashed changes


# ------------------------------------------------------------------------------------------


def remove_nodes(networkGraph, nodes):
    """
    :Function: Remove the nodes from the networkGraph
    :param networkGraph: NetworkGraph
    :type networkGraph: NetworkGraph
    :param nodes: Nodes to be removed
    :type nodes: list
    :return: NetworkGraph with the nodes removed
    :rtype: NetworkGraph
    """
    return 0


# ------------------------------------------------------------------------------------------


def remove_edges(networkGraph, edges):
    """
    :Function: Remove the edges from the networkGraph
    :param networkGraph: NetworkGraph
    :type networkGraph: NetworkGraph
    :param edges: Edges to be removed
    :type edges: list
    :return: NetworkGraph with the edges removed
    :rtype: NetworkGraph
    """
    return 0

# ------------------------------------------------------------------------------------------
