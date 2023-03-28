"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Resilience of the network
"""

# -------------------------------------- IMPORT ---------------------------------------------

from src.NetworkGraphs import NetworkGraphs

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
    if attack == "random":
        for key in kwargs.keys():
            if key not in ["number_of_nodes", "number_of_edges"]:
                print(f"Argument {key} not recognized")
                return 0
        nrb_nodes = kwargs["number_of_nodes"] if "number_of_nodes" in kwargs.keys() else 0
        nrb_edges = kwargs["number_of_edges"] if "number_of_edges" in kwargs.keys() else 0
        return resilience_random(networkGraph, nrb_nodes, nrb_edges)

    elif attack == "malicious":
        for key in kwargs.keys():
            if key not in ["metric", "number_of_nodes", "threshold"]:
                print(f"Argument {key} not recognized")
                return 0
        metric = kwargs["metric"]
        nrb_nodes = kwargs["number_of_nodes"] if "number_of_nodes" in kwargs.keys() else 0
        threshold = kwargs["threshold"] if "threshold" in kwargs.keys() else 0
        return resilience_malicious(networkGraph, metric, nrb_nodes, threshold)

    elif attack == "cluster":
        for key in kwargs.keys():
            if key not in ["cluster_algorithm", "total_clusters", "number_of_clusters"]:
                print(f"Argument {key} not recognized")
                return 0
        cluster_algorithm = kwargs["cluster_algorithm"]
        total_clusters = kwargs["total_clusters"]
        number_of_clusters = kwargs["number_of_clusters"]
        return resilience_cluster(networkGraph, cluster_algorithm, total_clusters, number_of_clusters)

    else:
        print("Attack not recognized")
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
    return 0


# ------------------------------------------------------------------------------------------


def copy_networkGraph(networkGraph):
    """
    :Function: Copy the networkGraph object
    :param neworkGraph: NetworkGraph
    :type neworkGraph: NetworkGraph
    :return: Copy of the networkGraph
    :rtype: NetworkGraph
    """
    return 0


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
