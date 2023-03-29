"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Resilience of the network
"""

# -------------------------------------- IMPORT ---------------------------------------------

import random

import src.machineLearning as ml
from src.NetworkGraphs import NetworkGraphs
from src.metrics import *
from src.preprocessing import convert_to_DiGraph

# -------------------------------------- FUNCTIONS -------------------------------------------


idx = {}


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
                - 'kcore'
                - 'degree'
                - 'triangles'
                - 'pagerank'
                - 'betweenness_centrality'
                - 'closeness_centrality'
                - 'eigenvector_centrality'
                - 'load_centrality'
                - 'degree_centrality'
            - 'directed': True or False
            - 'multi': True or False
            - "number_of_nodes": Number of nodes to be removed
            - "threshold": Threshold to be used to select the nodes to be removed
            - "operator" can be:
                    - ">"
                    - "<"
                    - ">="
                    - "<="
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
    if attack == "random":
        for key in kwargs.keys():
            if key not in ["number_of_nodes", "number_of_edges"]:
                raise ValueError(f"Argument {key} not recognized")
        return resilience_random(networkGraph, **kwargs)

    elif attack == "malicious":
        for key in kwargs.keys():
            if key not in ["metric", "number_of_nodes", "threshold", "operator", "multi", "directed"]:
                raise ValueError(f"Argument {key} not recognized")
        if "metric" not in kwargs.keys():
            raise ValueError("Metric not specified")
        return resilience_malicious(networkGraph, **kwargs)

    elif attack == "cluster":
        for key in kwargs.keys():
            if key not in ["cluster_algorithm", "total_clusters", "number_of_clusters"]:
                print(f"Argument {key} not recognized")
                return 0

        if "cluster_algorithm" not in kwargs.keys():
            raise ValueError("Cluster algorithm not specified")
        return resilience_cluster(networkGraph, **kwargs)
    elif attack == "cluster_custom":
        for key in kwargs.keys():
            if key not in ["cluster_algorithm", "total_clusters", "cluster_ids"]:
                print(f"Argument {key} not recognized")
                return 0
        if "cluster_algorithm" not in kwargs.keys():
            raise ValueError("Cluster algorithm not specified")
        return resilience_cluster_custom(networkGraph, **kwargs)
    else:
        print("Attack not recognized")
        return 0


# ------------------------------------------------------------------------------------------


def resilience_random(networkGraph, number_of_nodes=0, number_of_edges=0):
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
    G = copy_networkGraph(networkGraph)

    if number_of_nodes > 0:
        nodes = G.MultiDiGraph.nodes()
        nodes_to_remove = random.sample(nodes, number_of_nodes)
        G = remove_nodes(G, nodes_to_remove)

    if number_of_edges > 0:
        edges = G.MultiDiGraph.edges()
        edges_to_remove = random.sample(sorted(edges), number_of_edges)
        G = remove_edges(G, edges_to_remove)

    return G


# ------------------------------------------------------------------------------------------


def resilience_malicious(networkGraph, metric=None, number_of_nodes=None, threshold=None, operator='>', multi=False,
                         directed=False):
    """
    :Function: Compute the resilience of the networkGraph using the malicious attack
    Metrics:
        - 'kcore'
        - 'degree'
        - 'triangles'
        - 'pagerank'
        - 'betweenness_centrality'
        - 'closeness_centrality'
        - 'eigenvector_centrality'
        - 'load_centrality'
        - 'degree_centrality'
    operators:
        - ">" (default)
        - "<"
        - ">="
        - "<="
    :param networkGraph: NetworkGraph
    :type networkGraph: NetworkGraph
    :param metric: Metric to be used to select the nodes to be removed
    :type metric: str
    :param number_of_nodes: Number of nodes to be removed
    :type number_of_nodes: int
    :param threshold: Threshold to be used to select the nodes to be removed
    :type threshold: float
    :param operator: Operator to be used to select the nodes to be removed
    :type operator: str
    :param multi: True if the graph is multi
    :type multi: bool
    :param directed: True if the graph is directed
    :type directed: bool
    :return: NetworkGraph with the nodes removed
    :rtype: NetworkGraph
    """
    G = copy_networkGraph(networkGraph)

    df = get_metrics(G, metric, directed=directed, multi=multi)
    metric = df.columns[1]
    df = df.sort_values(by=metric, ascending=False)

    if threshold:
        nodes_to_remove = execute_threshold(df, metric, threshold, operator)

    if number_of_nodes:
        nodes_to_remove = df['Node'][:number_of_nodes].values

    G = remove_nodes(G, nodes_to_remove)
    return G


# ------------------------------------------------------------------------------------------


def resilience_cluster(networkGraph, cluster_algorithm=None, total_clusters=0, number_of_clusters=0):
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
    :param networkGraph: NetworkGraph
    :type networkGraph: NetworkGraph
    :return: Copy of the networkGraph
    :rtype: NetworkGraph
    """
    if networkGraph.session_folder not in idx.keys():
        idx[networkGraph.session_folder] = 0
    else:
        idx[networkGraph.session_folder] = idx[networkGraph.session_folder] + 1
    session_folder = f'{networkGraph.session_folder}/resilience{idx[networkGraph.session_folder]}'
    return NetworkGraphs(networkGraph.filename, type=networkGraph.type, session_folder=session_folder)


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
    for node in nodes:
        networkGraph.MultiDiGraph.remove_node(node)

    networkGraph.DiGraph = convert_to_DiGraph(networkGraph.MultiDiGraph)
    networkGraph.Graph, networkGraph.MultiGraph = networkGraph.DiGraph.to_undirected(
    ), networkGraph.MultiDiGraph.to_undirected()
    networkGraph.update_attributes()
    return networkGraph


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
    for edge in edges:
        networkGraph.MultiDiGraph.remove_edge(edge[0], edge[1])

    networkGraph.DiGraph = convert_to_DiGraph(networkGraph.MultiDiGraph)
    networkGraph.Graph, networkGraph.MultiGraph = networkGraph.DiGraph.to_undirected(
    ), networkGraph.MultiDiGraph.to_undirected()
    networkGraph.update_attributes()
    return networkGraph


# ------------------------------------------------------------------------------------------


def execute_threshold(df, metric, threshold, operator='>'):
    """
    :Function: Execute the threshold operation
    :param df: DataFrame with the metrics
    :type df: DataFrame
    :param threshold: Threshold to be used to select the nodes to be removed
    :type threshold: float
    :param operator: Operator to be used to select the nodes to be removed
    :type operator: str
    :return: DataFrame with the nodes to be removed
    :rtype: DataFrame
    """
    if operator == '>':
        nodes_to_remove = df[df[metric] > threshold]['Node'].values
    elif operator == '<':
        nodes_to_remove = df[df[metric] < threshold]['Node'].values
    elif operator == '>=':
        nodes_to_remove = df[df[metric] >= threshold]['Node'].values
    elif operator == '<=':
        nodes_to_remove = df[df[metric] <= threshold]['Node'].values
    else:
        raise ValueError(f"Operator {operator} not supported")

    return nodes_to_remove


def resilience_cluster_custom(networkGraph, cluster_algorithm=None, total_clusters=None, cluster_ids=None):
    """
    :Function: Compute the clusters of the networkGraph
    :param networkGraph: NetworkGraph
    :type networkGraph: NetworkGraph
    :param cluster_algorithm: Algorithm to be used to compute the clusters
    :type cluster_algorithm: str
    :param total_clusters: Total number of clusters
    :type total_clusters: int
    :param cluster_ids: Cluster ids to be removed
    :type cluster_ids: list
    """
    if cluster_algorithm not in ['louvain', 'greedy_modularity', 'label_propagation', 'asyn_lpa',
                                 'k_clique', 'spectral', 'kmeans', 'agglomerative', 'hierarchical', 'dbscan']:
        print(ValueError("Invalid cluster type", "please choose from the following: 'louvain', 'greedy_modularity', "
                                                 "'label_propagation', 'asyn_lpa',"
                                                 "'k_clique', 'spectral', 'kmeans' "
                                                 "'agglomerative', 'hierarchical', 'dbscan'"))
        return 0

    G = copy_networkGraph(networkGraph)
    clusters = ml.get_communities(networkGraph, cluster_algorithm, total_clusters)

    if cluster_ids is not None and len(cluster_ids) > 0:
        for cluster_id in cluster_ids:
            nodes_to_remove = clusters[clusters['Cluster_id'] == cluster_id]['Node'].values
            G = remove_nodes(G, nodes_to_remove)

    return G
