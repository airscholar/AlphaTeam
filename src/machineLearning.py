"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Machine Learning for the NetworkX graphs
"""

import warnings

import matplotlib.pyplot as plt
import networkx as nx
import networkx.algorithms.community as nx_comm
import numpy as np
import pandas as pd
from distinctipy import distinctipy
from kneed import KneeLocator
from sklearn.cluster import SpectralClustering, KMeans

warnings.filterwarnings("ignore")


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
    Create a list of colors for the communities
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
    Create a dataframe with the Node, communities ID and their colors
    :param communities: list of communities
    :param colors: list of colors
    :return: dataframe
    """
    df = pd.DataFrame()
    print(communities)
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
    Detect communities based on Louvain clustering
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
    Detect communities based on edge betweenness
    :param networkGraphs: NetworkGraphs
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


def k_means_clustering(networkGraphs):
    """
    :Function: Detect communities based on k-means
    :param networkGraphs: NetworkGraphs
    :return: dataframe
    """
    df = pd.DataFrame()
    return df


def spectral_clustering(networkGraphs):
    """
    :Function: Detect communities based on spectral
    :param networkGraphs: NetworkGraphs
    :return: dataframe
    """
    np.random.seed(0)
    G = networkGraphs.Graph

    pos = networkGraphs.pos['sfdp']

    # Get adjacency-matrix as numpy-array
    adj_mat = nx.to_numpy_array(G)

    # get optimal number of clusters
    wcss = []
    for i in range(1, 100):
        kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42, max_iter=100, n_init='auto').fit(adj_mat)
        wcss.append(kmeans.inertia_)

    optimal_k = KneeLocator(range(1, 100), wcss, curve='convex', direction='decreasing')
    print('optimal k is : ', optimal_k.elbow)

    optimal_k.plot_knee()
    plt.show()

    # Cluster
    sc = SpectralClustering(optimal_k.elbow, affinity='precomputed', n_init=100, assign_labels='discretize', )
    sc.fit(adj_mat)

    # Compare ground-truth and clustering-results
    clusters = sc.labels_
    # get the nodes in each cluster
    # print(adj_mat, sc.__dict__)
    # get the nodes in each cluster
    clusters_comm = []
    # for i in range(optimal_k.elbow):
    #     clusters_comm.append([node for node in G.nodes() if clusters[node] == i])

    # print(clusters, clusters_comm)

    df = pd.DataFrame()

    colors = create_comm_colors(list(range(optimal_k.elbow)))

    # assign colors to each node
    for i, node in enumerate(G.nodes()):
        df = pd.concat([df, pd.DataFrame({'Node': node,
                                          'Color': colors[clusters[i]],
                                          'Cluster_id': clusters[i]
                                          }, index=[0])], ignore_index=True)

    # # Plot
    # colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(set(sc.labels_)))]
    # colors = [colors[i] for i in sc.labels_]

    # nx.draw(G, pos, node_color=colors, with_labels=False, node_size=5)

    return df

    # Generate walks
    # node2vec = Node2Vec(networkGraphs.Graph, dimensions=16, walk_length=80, num_walks=50, workers=4)

    # # Learn embeddings
    # model = node2vec.fit(window=10, min_count=1, batch_words=4)
    #
    # # Save the embedding in file embedding.emb using the gensim format
    # model.wv.save_word2vec_format("spectral_embedding.emb", binary=False)
    #
    # # Load embeddings using gensim
    # model = gensim.models.KeyedVectors.load_word2vec_format("spectral_embedding.emb")
    # print(model.__dict__)
    # print(model.index_to_key)
    # # Load embeddings
    # embedding_matrix = model.vectors
    #
    # # Remove node index from embedding matrix
    # Z = embedding_matrix[:, 1:]
    # print(Z[0], embedding_matrix)
    #
    # # Automate selection of optimal number of clusters
    # scores = []
    # for k in range(2, 11):
    #     clustering = SpectralClustering(n_clusters=k, random_state=0).fit(Z)
    #     score = silhouette_score(Z, clustering.labels_)
    #     scores.append(score)
    # optimal_k = np.argmax(scores) + 5
    # print("Optimal number of clusters: ", optimal_k, " with silhouette score: ", scores[optimal_k - 5])
    # # plot scores to find optimal number of clusters
    # # plt.plot(range(2, 11), scores)
    # # plt.xlabel('Number of clusters')
    # # plt.ylabel('Silhouette score')
    # # plt.title('Silhouette score for different number of clusters')
    # # plt.show()
    #
    # # Cluster nodes using optimal number of clusters based on the nodes from the embedding matrix
    # rs = np.random.seed(1337)
    # clustering = SpectralClustering(n_clusters=optimal_k, eigen_solver='arpack', affinity="nearest_neighbors",
    #                                 random_state=rs).fit(Z)
    # labels = clustering.labels_
    #
    # cmap = cm.get_cmap('viridis', optimal_k)
    #
    # pos = networkGraphs.pos['sfdp']
    # # Map the clustering labels to colors in the colormap
    # colors = [cmap(i) for i in labels]
    #
    # # Plot clusters
    # plt.figure(figsize=(10, 10))
    # plt.axis('off')
    # nx.draw_networkx_nodes(networkGraphs.Graph, pos, node_size=10, node_color=colors)
    # plt.show()
    return None


# ----------------------------------------------------------------------------------------

def get_communities(networkGraphs, method):
    """
    Get communities based on the method
    :param networkGraphs: NetworkGraphs
    :param method: str - method to use
    :return: dataframe
    """
    if method not in ['louvain', 'greedy_modularity', 'label_propagation', 'asyn_lpa', 'girvan_newman',
                      'edge_betweenness', 'k_clique', 'spectral']:
        ValueError("Invalid cluster type", "please choose from the following: 'louvain', 'greedy_modularity', "
                                           "'label_propagation', 'asyn_lpa', 'girvan_newman', 'edge_betweenness', "
                                           "'k_clique', 'spectral'")
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
    # elif method == 'kmeans':
    #     return kmeans_clustering(networkGraphs)
    elif method == 'spectral':
        return spectral_clustering(networkGraphs)
    # elif method == 'Agglomerative':
    #     return Agglomerative_clustering(networkGraphs)
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
