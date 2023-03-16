"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Machine Learning for the NetworkX graphs
"""

import networkx.algorithms.community as nx_comm
import pandas as pd
from distinctipy import distinctipy


# ----------------------------------------------------------------------------------------

def short_path_distance(networkx_, from_, to_):
    # return dataframe
    return 0


# ----------------------------------------------------------------------------------------
def get_cold_spot(networkx_):
    # return dataframe
    return 0


# ----------------------------------------------------------------------------------------
def get_hot_spot(networkx_):
    # return dataframe
    return 0


# ----------------------------------------------------------------------------------------

def create_comm_colors(communities):
    """
    :Function: Create a list of colors for the communities
    :param communities: list of communities
    :return: list of colors
    """
    colors = distinctipy.get_colors(len(communities))
    colors = [tuple([i * 255 for i in c]) for c in colors]
    # convert rgb tuple to hex
    colors = [f'#{int(c[0]):02x}{int(c[1]):02x}{int(c[2]):02x}' for c in colors]

    return colors


# ----------------------------------------------------------------------------------------
def create_comm_dataframe(communities, colors):
    """
    :Function: Create a dataframe for the communities
    :param communities: list of communities
    :param colors: list of colors
    :return: dataframe
    """
    df = pd.DataFrame()
    for idx, community in enumerate(communities):
        color = colors.pop()
        for node in community:
            df = pd.concat([df, pd.DataFrame({'Node': node,
                                              'Color': color,
                                              'Cluster_id': idx
                                              }, index=[0])], ignore_index=True)
    return df


# ----------------------------------------------------------------------------------------
def louvain_clustering(networkGraphs):
    """
    :Function: Detect communities based on Louvain
    :param networkGraphs: NetworkGraphs
    :return: dataframe
    """
    communities = list(nx_comm.louvain_communities(networkGraphs.Graph))
    colors = create_comm_colors(communities)
    df = create_comm_dataframe(communities, colors)

    return df


# ----------------------------------------------------------------------------------------

def greedy_modularity_clustering(networkGraphs):
    """
    Detect communities based on greedy modularity.
    :param networkGraphs: NetworkGraphs
    :return: dataframe
    """
    communities = list(nx_comm.greedy_modularity_communities(networkGraphs.Graph))
    colors = create_comm_colors(communities)
    df = create_comm_dataframe(communities, colors)
    return df


# ----------------------------------------------------------------------------------------

def label_propagation_clustering(networkGraphs):
    """
    Detect communities based on label propagation
    :param networkGraphs: NetworkGraphs
    :return: dataframe
    """
    communities = list(nx_comm.label_propagation_communities(networkGraphs.Graph))
    colors = create_comm_colors(communities)
    df = create_comm_dataframe(communities, colors)
    return df


# ----------------------------------------------------------------------------------------

def asyn_lpa_clustering(networkGraphs):
    """
    Detect communities based on asynchronous label propagation
    :param networkGraphs: NetworkGraphs
    :return: dataframe
    """
    communities = list(nx_comm.asyn_lpa_communities(networkGraphs.Graph))
    colors = create_comm_colors(communities)
    df = create_comm_dataframe(communities, colors)
    return df


# ----------------------------------------------------------------------------------------

def girvan_newman_clustering(networkGraphs):
    """
    Detect communities based on Girvan Newman
    :param networkGraphs: NetworkGraphs
    :return: dataframe
    """
    communities = list(nx_comm.girvan_newman(networkGraphs.Graph))
    colors = create_comm_colors(communities)
    df = create_comm_dataframe(communities, colors)
    return df


# ----------------------------------------------------------------------------------------

def edge_betweenness_clustering(networkGraphs):
    """
    :Function: Detect communities based on edge betweenness
    :param networkGraphs: NetworkGraphs
    :type networkGraphs: NetworkGraphs
    :return: dataframe
    """
    communities = list(nx_comm.centrality.girvan_newman(networkGraphs.Graph))
    colors = create_comm_colors(communities)
    df = create_comm_dataframe(communities, colors)
    return df


# ----------------------------------------------------------------------------------------

def k_clique_clustering(networkGraphs):
    """
    Detect communities based on k-clique
    :param networkGraphs: NetworkGraphs
    :return: dataframe
    """
    communities = list(nx_comm.k_clique_communities(networkGraphs.Graph, 3))
    colors = create_comm_colors(communities)
    df = create_comm_dataframe(communities, colors)
    return df


# ----------------------------------------------------------------------------------------

def get_communities(networkGraphs, method):
    """
    Get communities based on the method
    :param networkGraphs: NetworkGraphs
    :param method: str - method to use
    :return: dataframe
    """
    if method not in ['louvain', 'greedy_modularity', 'label_propagation', 'asyn_lpa', 'girvan_newman',
                      'edge_betweenness', 'k_clique']:
        ValueError("Invalid cluster type", "please choose from the following: 'louvain', 'greedy_modularity', "
                                           "'label_propagation', 'asyn_lpa', 'girvan_newman', 'edge_betweenness', 'k_clique'")
        return

    if method == 'louvain':
        return louvain_clustering(networkGraphs)
    elif method == 'greedy_modularity':
        return greedy_modularity_clustering(networkGraphs)
    elif method == 'label_propagation':
        return label_propagation_clustering(networkGraphs)
    elif method == 'asyn_lpa':
        return asyn_lpa_clustering(networkGraphs)
    elif method == 'girvan_newman':
        return girvan_newman_clustering(networkGraphs)
    elif method == 'edge_betweenness':
        return edge_betweenness_clustering(networkGraphs)
    elif method == 'k_clique':
        return k_clique_clustering(networkGraphs)
    else:
        return None


def get_hotspot(networkGraphs):
    data = []
    for node in networkGraphs.Graph.nodes():
        temp = {'Degree': networkGraphs.Graph.degree(node),
                'Latitude': networkGraphs.pos['map'][node][1],
                'Longitude': networkGraphs.pos['map'][node][0],
                'Node': node,
                'Edges': networkGraphs.Graph.edges(node)
                }

        data.append(temp)

    df = pd.DataFrame(data)

    return df
