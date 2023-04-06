"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Machine Learning for the NetworkX graphs
"""

# ----------------------------------------- Imports ----------------------------------------- #

# Internal imports
import src.utils as utils
from src.utils import memoize

# External imports
import warnings
import networkx as nx
import networkx.algorithms.community as nx_comm
import numpy as np
import pandas as pd
from distinctipy import distinctipy
from kneed import KneeLocator
from sklearn.cluster import SpectralClustering, KMeans, AgglomerativeClustering, DBSCAN

warnings.filterwarnings("ignore")


# ----------------------------------------------------------------------------------------

def short_path_distance(networkx_, from_, to_):
    # return dataframe
    return 0


# ----------------------------------------------------------------------------------------

def create_comm_colors(communities):
    """
    :Function: Create a list of colors for the communities
    :param communities: list of communities
    :type communities: list
    :return: list of colors
    :rtype: list
    """
    colors = distinctipy.get_colors(len(communities))
    colors = [tuple([i * 255 for i in c]) for c in colors]
    # convert rgb tuple to hex
    colors = [f'#{int(c[0]):02x}{int(c[1]):02x}{int(c[2]):02x}' for c in colors]

    return colors


# ----------------------------------------------------------------------------------------
def create_comm_dataframe(communities, colors):
    """
    :Function: Create a dataframe with the Node, communities ID and their colors
    :param communities: list of communities
    :type communities: list
    :param colors: list of colors
    :type colors: list
    :return: dataframe
    :rtype: pd.DataFrame
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

@memoize
def louvain_clustering(networkGraphs, noOfClusters=0):
    """
    :Function: Detect communities based on Louvain clustering with a maximum of `totalCommunities`
    :param networkGraphs: NetworkGraphs
    :type networkGraphs: NetworkGraphs
    :param noOfClusters: maximum number of communities
    :type noOfClusters: int
    :return: dataframe
    :rtype: pd.DataFrame
    """
    if 0 < noOfClusters:
        communities = binary_search('louvain_communities', networkGraphs, noOfClusters)
    else:
        communities = list(nx_comm.louvain_communities(networkGraphs.Graph))

    colors = create_comm_colors(communities)
    df = create_comm_dataframe(communities, colors)

    return df


# ----------------------------------------------------------------------------------------


@memoize
def greedy_modularity_clustering(networkGraphs, noOfClusters=0):
    """
    :Function: Detect communities based on greedy modularity clustering with a maximum of `noOfClusters`
    :param networkGraphs: NetworkGraphs
    :type networkGraphs: NetworkGraphs
    :param noOfClusters: maximum number of communities
    :type noOfClusters: int
    :return: dataframe
    :rtype: pd.DataFrame
    """
    if 0 < noOfClusters:
        communities = binary_search('greedy_modularity_communities', networkGraphs, noOfClusters)
    else:
        communities = list(nx_comm.greedy_modularity_communities(networkGraphs.Graph))

    colors = create_comm_colors(communities)
    df = create_comm_dataframe(communities, colors)
    return df


# ----------------------------------------------------------------------------------------


@memoize
def label_propagation_clustering(networkGraphs, noOfClusters=0):
    """
    :Function: Detect communities based on label propagation
    :param networkGraphs: NetworkGraphs
    :type networkGraphs: NetworkGraphs
    :param noOfClusters: maximum number of communities
    :type noOfClusters: int
    :return: dataframe
    :rtype: pd.DataFrame
    """
    communities = list(
        nx_comm.label_propagation_communities(networkGraphs.Graph))
    colors = create_comm_colors(communities)
    df = create_comm_dataframe(communities, colors)
    return df


# ----------------------------------------------------------------------------------------


@memoize
def asyn_lpa_clustering(networkGraphs, noOfClusters=0):
    """
    :Function: Detect communities based on asynchronous label propagation
    :param networkGraphs: NetworkGraphs
    :type networkGraphs: NetworkGraphs
    :return: dataframe
    :rtype: pd.DataFrame
    """
    communities = list(nx_comm.asyn_lpa_communities(networkGraphs.Graph))
    colors = create_comm_colors(communities)
    df = create_comm_dataframe(communities, colors)
    return df


# ----------------------------------------------------------------------------------------


@memoize
def k_clique_clustering(networkGraphs, noOfClusters=0):
    """
    :Function: Detect communities based on k-clique
    :param networkGraphs: NetworkGraphs
    :type networkGraphs: NetworkGraphs
    :param noOfClusters: maximum number of communities
    :type noOfClusters: int
    :return: dataframe
    :rtype: pd.DataFrame
    """
    communities = list(nx_comm.k_clique_communities(networkGraphs.Graph, 2))
    colors = create_comm_colors(communities)
    df = create_comm_dataframe(communities, colors)
    return df


# ----------------------------------------------------------------------------------------


@memoize
def spectral_clustering(networkGraphs, noOfClusters=0, embedding=None):
    """
    :Function: Detect communities based on spectral
    :param networkGraphs: NetworkGraphs
    :type networkGraphs: NetworkGraphs
    :param noOfClusters: number of clusters
    :type noOfClusters: int
    :param embedding: embedding
    :type embedding: np.array
    :return: dataframe
    :rtype: pd.DataFrame
    """
    G = networkGraphs.Graph

    if embedding is None:
        if 0 < noOfClusters:
            adj_mat = nx.to_numpy_array(G)
            optimal_k = noOfClusters
        else:
            adj_mat, optimal_k = compute_clustering(G)
        clustering = SpectralClustering(optimal_k, affinity='precomputed', eigen_solver='arpack', n_init=100).fit(
            adj_mat)
    elif noOfClusters > 0:
        adj_mat = embedding
        optimal_k = noOfClusters
        clustering = SpectralClustering(n_clusters=optimal_k).fit(adj_mat)
    else:
        raise ValueError('If embedding is provided, noOfClusters must be > 0')

    df = clustering_response(G, clustering, optimal_k)

    return df


# ----------------------------------------------------------------------------------------


@memoize
def compute_clustering(networkGraph, max_range=30):
    """
    :Function: Compute the optimal number of clusters
    :param networkGraph: NetworkGraphs
    :param max_range: maximum range of clusters
    :return: adjacent matrics, optimal number of clusters
    :rtype: numpy array, int
    """
    np.random.seed(0)

    adj_mat = nx.to_numpy_array(networkGraph)

    if max_range >= len(networkGraph.nodes()):
        print('overriding max range', len(networkGraph.nodes()) - 1)
        max_range = len(networkGraph.nodes()) - 1

    # get optimal number of clusters
    wcss = []
    for i in range(1, max_range):
        kmeans = KMeans(n_clusters=i, init='k-means++',
                        random_state=4).fit(adj_mat)
        wcss.append(kmeans.inertia_)

    # find the optimal number of clusters
    optimal_k = KneeLocator(range(1, max_range), wcss,
                            curve='convex', direction='decreasing').elbow
    if optimal_k is None:
        optimal_k = 8
    print('Optimal k is : ', optimal_k)

    return adj_mat, optimal_k


# ----------------------------------------------------------------------------------------


def clustering_response(networkGraph, clustering_alg, optimal_k):
    """
    :Function: Create a dataframe with the Node, communities ID and their colors
    :param networkGraph: NetworkGraphs
    :type networkGraph: NetworkGraphs
    :param clustering_alg: clustering algorithm
    :type clustering_alg: KMeans
    :param optimal_k: optimal number of clusters
    :type optimal_k: int
    :return: dataframe
    :rtype: pd.DataFrame
    """
    clusters = clustering_alg.labels_
    df = pd.DataFrame()
    colors = create_comm_colors(list(range(optimal_k)))
    for i, node in enumerate(networkGraph.nodes()):
        df = pd.concat([df, pd.DataFrame({'Node': node,
                                          'Color': colors[clusters[i]],
                                          'Cluster_id': clusters[i]
                                          }, index=[0])], ignore_index=True)
    return df


# ----------------------------------------------------------------------------------------


@memoize
def kmeans_clustering(networkGraphs, noOfClusters=0, embedding=None):
    """
    :Function: Detect communities based on k-means
    :param networkGraphs: NetworkGraphs
    :type networkGraphs: NetworkGraphs
    :param noOfClusters: number of clusters
    :type noOfClusters: int
    :param embedding: embedding
    :type embedding: np.array
    :return: dataframe
    :rtype: pd.DataFrame
    """
    G = networkGraphs.Graph

    if embedding is None:
        if 0 >= noOfClusters:
            adj_mat, optimal_k = compute_clustering(G)

        else:
            optimal_k = noOfClusters
            adj_mat = nx.to_numpy_array(G)
    elif 0 < noOfClusters:
        adj_mat = embedding
        optimal_k = noOfClusters
    else:
        raise ValueError('If embedding is provide, noOfClusters must be greater than 0')

    clustering = KMeans(n_clusters=optimal_k, init='k-means++',
                        random_state=4, max_iter=10).fit(adj_mat)
    df = clustering_response(G, clustering, optimal_k)

    return df


# ----------------------------------------------------------------------------------------


@memoize
def agglomerative_clustering(networkGraphs, noOfClusters=0, embedding=None):
    """
    :Function: Detect communities based on agglomerative
    :param networkGraphs: NetworkGraphs
    :type networkGraphs: NetworkGraphs
    :param noOfClusters: number of clusters
    :type noOfClusters: int
    :param embedding: embedding
    :type embedding: np.array
    :return: dataframe
    :rtype: pd.DataFrame
    """
    G = networkGraphs.Graph

    if embedding is None:
        if 0 < noOfClusters:
            optimal_k = noOfClusters
            adj_mat = nx.to_numpy_array(G)
        else:
            adj_mat, optimal_k = compute_clustering(G)
    elif 0 < noOfClusters:
        adj_mat = embedding
        optimal_k = noOfClusters
    else:
        raise ValueError('If embedding is provided, noOfClusters must be > 0')

    clustering = AgglomerativeClustering(
        n_clusters=optimal_k, affinity='euclidean', linkage='ward').fit(adj_mat)

    df = clustering_response(G, clustering, optimal_k)

    return df


# ----------------------------------------------------------------------------------------


@memoize
def dbscan_clustering(networkGraphs, noOfClusters=0, embedding=None):
    """
    :Function: Detect communities based on dbscan
    :param networkGraphs: NetworkGraphs
    :type networkGraphs: NetworkGraphs
    :param noOfClusters: number of clusters
    :type noOfClusters: int
    :param embedding: embedding
    :type embedding: np.array
    :return: dataframe
    :rtype: pd.DataFrame
    """
    G = networkGraphs.Graph

    if embedding is None:
        if 0 < noOfClusters:
            optimal_k = noOfClusters
            adj_mat = nx.to_numpy_array(G)
        else:
            adj_mat, optimal_k = compute_clustering(G)
    elif 0 < noOfClusters:
        adj_mat = embedding
        optimal_k = noOfClusters
    else:
        raise ValueError('If embedding is provided, noOfClusters must be > 0')

    # compute DBSCAN clustering algorithm on Graph
    db = DBSCAN(eps=0.3, min_samples=optimal_k).fit(adj_mat)
    labels = db.labels_
    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)
    df = clustering_response(G, db, n_clusters_)

    return df


# ----------------------------------------------------------------------------------------



def get_communities(networkGraphs, method, noOfClusters=0, embedding=None):
    """
    :Function: Get communities based on the method
    :param networkGraphs: NetworkGraphs
    :type networkGraphs: NetworkGraphs
    :param method: method to use
    :type method: str
    :param noOfClusters: size of the cluster
    :type noOfClusters: int
    :return: dataframe
    """
    if method not in ['louvain', 'greedy_modularity', 'label_propagation', 'asyn_lpa',
                      'k_clique', 'spectral', 'kmeans', 'agglomerative', 'hierarchical', 'dbscan']:
        print(ValueError("Invalid cluster type", "please choose from the following: 'louvain', 'greedy_modularity', "
                                                 "'label_propagation', 'asyn_lpa',"
                                                 "'k_clique', 'spectral', 'kmeans' "
                                                 "'agglomerative', 'hierarchical', 'dbscan'"))
        df = utils.return_nan(networkGraphs, 'Cluster')
        return df

    if method == 'louvain':
        return louvain_clustering(networkGraphs, noOfClusters=noOfClusters)
    elif method == 'greedy_modularity':
        return greedy_modularity_clustering(networkGraphs, noOfClusters=noOfClusters)
    elif method == 'label_propagation':
        return label_propagation_clustering(networkGraphs, noOfClusters=noOfClusters)
    elif method == 'asyn_lpa':
        return asyn_lpa_clustering(networkGraphs, noOfClusters=noOfClusters)
    elif method == 'k_clique':
        return k_clique_clustering(networkGraphs, noOfClusters=noOfClusters)
    elif method == 'kmeans':
        return kmeans_clustering(networkGraphs, noOfClusters=noOfClusters, embedding=embedding)
    elif method == 'spectral':
        return spectral_clustering(networkGraphs, noOfClusters=noOfClusters, embedding=embedding)
    elif method == 'agglomerative':
        return agglomerative_clustering(networkGraphs, noOfClusters=noOfClusters, embedding=embedding)
    elif method == 'dbscan':
        return dbscan_clustering(networkGraphs, noOfClusters=noOfClusters, embedding=embedding)
    else:
        return None


# ----------------------------------------------------------------------------------------


def get_hotspot(networkGraphs):
    """
    :Function: Get hotspot
    :param networkGraphs:
    :type networkGraphs: NetworkGraphs
    :return: dataframe
    :rtype: pd.DataFrame
    """
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


# ----------------------------------------------------------------------------------------


@memoize
def binary_search(func, networkGraphs, noOfClusters=0):
    """
    :Function: Perform binary search for optimal resolution parameter
    :param func: the function to use
    :type func: str
    :param networkGraphs: NetworkGraphs
    :type networkGraphs: NetworkGraphs
    :param noOfClusters: number of clusters
    :type noOfClusters: int
    :return: dataframe
    :rtype: pd.DataFrame
    """
    lower_bound, upper_bound = 0, None
    step = 0.1
    tolerance = 0.0001
    function = getattr(nx_comm, func)
    prev_resolution = None
    communities = None

    # Perform binary search for optimal resolution parameter
    for i in range(500):
        if upper_bound is None:
            resolution = lower_bound + step
        else:
            resolution = (lower_bound + upper_bound) / 2

        communities = list(function(networkGraphs.Graph, resolution=resolution))
        num_communities = len(communities)

        # Check convergence criterion
        if i > 0 and abs(resolution - prev_resolution) < tolerance:
            break

        # Update bounds based on number of communities
        if num_communities < noOfClusters:
            if upper_bound is not None:
                step /= 2
            lower_bound = resolution
        elif num_communities > noOfClusters:
            upper_bound = resolution
        else:
            break
        prev_resolution = resolution

    return communities
