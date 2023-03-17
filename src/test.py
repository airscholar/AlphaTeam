# FILE TO TEST THE FUNCTIONS IN THE SRC FOLDER
import matplotlib.pyplot as plt

from src.NetworkGraphs import NetworkGraphs
from src.preprocessing import *
from src.metrics import *
from src.visualisation import *
from src.machineLearning import *
import time

# networkGraph = NetworkGraphs('../datasets/Railway.csv', type="RAILWAY")
# networkGraph = NetworkGraphs('../datasets/Dune_Eth_transaction.csv', session_folder='plots', type="CRYPTO")
networkGraph = NetworkGraphs('../datasets/Railway.csv', session_folder='plots', type="RAILWAY")
# spectral_clustering(networkGraph)

plot_cluster(networkGraph, 'spectral', dynamic=False, layout='sfdp')

# pos = networkGraph.pos['twopi']
# nx.draw(networkGraph.Graph, pos, with_labels=False, node_size=2)
# plt.title('Network Graph')
# plt.show()
# from node2vec import Node2Vec
# from sklearn.cluster import DBSCAN, SpectralClustering, AgglomerativeClustering
# import numpy as np
#
# # Generate walks
# node2vec = Node2Vec(networkGraph.Graph, dimensions=16, walk_length=80, num_walks=50, workers=4)
# # Learn embeddings
# model = node2vec.fit(window=10, min_count=1, batch_words=4)
# model.wv.save_word2vec_format("embedding.emb")
#
# # Load embeddings
# X = np.loadtxt("embedding.emb", skiprows=1)
# # Remove node index from X
# Z = X[:, 1:]
#
# # Cluster nodes using DBSCAN
# clustering = DBSCAN(eps=1.0, min_samples=5).fit(Z)
# labels = clustering.labels_
#
# # Plot the graph with the cluster labels
# pos = networkGraph.pos['map']
# nx.draw(networkGraph.Graph, pos, node_color=labels, with_labels=False, node_size=2)
# plt.title('DBSCAN Clustering')
# plt.show()
#
# # Spectral clustering
# from sklearn.metrics import silhouette_score
#
# # Automate selection of optimal number of clusters
# scores = []
# for k in range(2, 11):
#     clustering = SpectralClustering(n_clusters=k, random_state=0).fit(Z)
#     score = silhouette_score(Z, clustering.labels_)
#     scores.append(score)
# optimal_k = np.argmax(scores) + 2
#
# # Cluster nodes using optimal number of clusters
# clustering = SpectralClustering(n_clusters=optimal_k, random_state=0).fit(Z)
# labels = clustering.labels_
#
# # Plot the graph with the cluster labels
# pos = networkGraph.pos['map']
# nx.draw(networkGraph.Graph, pos, node_color=labels, with_labels=False, node_size=2)
# plt.title('Spectral Clustering')
# plt.show()
#
# #Agglomerative clustering
# score = []
# for k in range(2, 11):
#     clustering = AgglomerativeClustering(n_clusters=k).fit(Z)
#     score = silhouette_score(Z, clustering.labels_)
#     scores.append(score)
# optimal_k = np.argmax(scores) + 2
#
# # Cluster nodes using optimal number of clusters
# clustering = AgglomerativeClustering(n_clusters=optimal_k).fit(Z)
#
# labels = clustering.labels_
#
# # Plot the graph with the cluster labels
# pos = networkGraph.pos['map']
# nx.draw(networkGraph.Graph, pos, node_color=labels, with_labels=False, node_size=2)
# plt.title('Agglomerative Clustering')
# plt.show()
#
# # KMeans clustering
# from sklearn.cluster import KMeans
# import numpy as np
#
# X = np.loadtxt("embedding.emb", skiprows=1)  # load the embedding of the nodes of the graph
#
# # sort the embedding based on node index in the first column in X
# X = X[X[:, 0].argsort()]
# # print(X)
# Z = X[0:X.shape[0], 1:X.shape[1]]  # remove the node index from X and save in Z
#
# # Automate selection of optimal number of clusters
# scores = []
# for k in range(2, 11):
#     clustering = KMeans(n_clusters=k, random_state=0).fit(Z)
#     score = silhouette_score(Z, clustering.labels_)
#     scores.append(score)
# optimal_k = np.argmax(scores) + 2
#
# # Cluster nodes using optimal number of clusters
# clustering = KMeans(n_clusters=optimal_k, random_state=0).fit(Z)
# labels = clustering.labels_
#
# # Plot the graph with the cluster labels
# pos = networkGraph.pos['map']
# nx.draw(networkGraph.Graph, pos, node_color=labels, with_labels=False, node_size=2)
# plt.title('KMeans Clustering')
# plt.show()




# from node2vec import Node2Vec
# from sklearn.cluster import KMeans
# import gensim
#
# # Generate walks
# node2vec = Node2Vec(networkGraph.Graph, dimensions=16, walk_length=80, num_walks=50, workers=4)
# # Learn embeddings
# model = node2vec.fit(window=10, min_count=1, batch_words=4)
#
# # Save the embedding in file embedding.emb using the gensim format
# model.wv.save_word2vec_format("embedding.emb", binary=False)
#
# # Load embeddings using gensim
# model = gensim.models.KeyedVectors.load_word2vec_format("embedding.emb")
#
# # Get the embedding matrix
# embedding_matrix = model.vectors
#
# # Remove node index from embedding matrix
# Z = embedding_matrix[:, 1:]
#
# # Cluster nodes using KMeans
# kmeans = KMeans(n_clusters=6, random_state=0).fit(Z)
# labels = kmeans.labels_
#
# # Plot the graph with the cluster labels
# pos = networkGraph.pos['twopi']
# nx.draw(networkGraph.Graph, pos, node_color=labels, with_labels=False, node_size=4)
# plt.show()

# from node2vec import Node2Vec
# from sklearn.cluster import KMeans
# import gensim
#
# # Generate walks
# node2vec = Node2Vec(networkGraph.Graph, dimensions=16, walk_length=80, num_walks=50, workers=4)
# # Learn embeddings
# model = node2vec.fit(window=10, min_count=1, batch_words=4)
#
# # Save the embedding in file embedding.emb using the gensim format
# model.wv.save_word2vec_format("embedding.emb", binary=False)
#
# # Load embeddings using gensim
# model = gensim.models.KeyedVectors.load_word2vec_format("embedding.emb")
#
# # Get the embedding matrix
# embedding_matrix = model.vectors
#
# # Remove node index from embedding matrix
# Z = embedding_matrix[:, 1:]
#
# # Cluster nodes using KMeans
# kmeans = KMeans(n_clusters=6, random_state=0).fit(Z)
# labels = kmeans.labels_
#
# # Plot the graph with the cluster labels
# pos = networkGraph.pos['sfdp']
# nx.draw(networkGraph.Graph, pos, node_color=labels, with_labels=False, node_size=4)
# plt.show()



# from node2vec import Node2Vec
#
# # Generate walks
# node2vec = Node2Vec(networkGraph.Graph, dimensions=2, walk_length=20, num_walks=10,workers=4)
# # Learn embeddings
# model = node2vec.fit(window=10, min_count=1, batch_words=4)
# # model.wv.most_similar('1')
# model.wv.save_word2vec_format("embedding.emb")  # save the embedding in file embedding.emb
#
# from sklearn.cluster import KMeans
# import numpy as np
#
# X = np.loadtxt("embedding.emb", skiprows=1)  # load the embedding of the nodes of the graph
#
# # sort the embedding based on node index in the first column in X
# X = X[X[:, 0].argsort()]
# # print(X)
# Z = X[0:X.shape[0], 1:X.shape[1]]  # remove the node index from X and save in Z
# kmeans = KMeans(n_clusters=6, random_state=0).fit(Z)  # apply kmeans on Z
# labels = kmeans.labels_  # get the cluster labels of the nodes.
#
# # print unique labels
# print(np.unique(labels))
#
# # plot elbow curve to find the optimal number of clusters
# distortions = []
# K = range(1, 10)
# for k in K:
#     kmeanModel = KMeans(n_clusters=k)
#     kmeanModel.fit(Z)
#     distortions.append(kmeanModel.inertia_)
# plt.plot(K, distortions, 'bx-')
# plt.xlabel('k')
# plt.ylabel('Distortion')
# plt.title('The Elbow Curve showing the optimal k')
# plt.show()
#
# # plot the graph with the cluster labels
# pos = networkGraph.pos['map']
# nx.draw(networkGraph.Graph, pos, node_color=labels, with_labels=False, node_size=2)
# plt.show()

# plot_hotspot(networkGraph)

# kcore = compute_kcore(networkGraph, directed=False)
# plot_metrics_on_map(networkGraph, kcore, 'Kcore', 'kcore')

# louv_df = louvain_clustering(networkGraph)
# print(louv_df)
# print(color_map)
# print(list(networkGraph.Graph.nodes))
# pos = nx.nx_agraph.graphviz_layout(networkGraph.Graph, prog='sfdp')
# print(pos)

# plot_cluster(networkGraph, 'louvain', 'Louvan Clustering')
# plot_cluster(networkGraph, 'greedy_modularity', 'Greedy Modularity Clustering')
# plot_cluster(networkGraph, 'label_propagation', 'Label Propagation Clustering')
# plot_cluster(networkGraph, 'asyn_lpa', 'Asyn LPA Clustering')
# plot_cluster(networkGraph, 'girvan_newman', 'Girvan Newman Clustering')
# plot_cluster(networkGraph, 'edge_betweenness', 'Edge Betweenness Clustering')
# plot_cluster(networkGraph, 'k_clique', 'K Clique Clustering')


# customGraphs = NetworkGraphs('../datasets/Dune_Eth_transaction.csv', type="CRYPTO")
# louvain_clustering(customGraphs)


#
# degree = compute_degree_centrality(customGraphs, directed=False)
# print(degree.head())
# plt = plot_metrics(customGraphs, degree)
# plt.show()
#
# kcore = compute_kcore(customGraphs, directed=False)
# print(kcore.head())
# plt =plot_metrics(customGraphs, kcore)
# plt.show()
#
# triangle = compute_triangles(customGraphs, directed=False)
# print(triangle.head())
# plt = plot_metrics(customGraphs, triangle)
# plt.show()
#
# degree = compute_degree_centrality(customGraphs, directed=False)
# print(degree.head())
# plt = plot_metrics(customGraphs, degree,'neato')
# plt.show()
#
# kcore = compute_kcore(customGraphs, directed=False)
# print(kcore.head())
# plt = plot_metrics(customGraphs, kcore,'neato')
# plt.show()
#
# triangle = compute_triangles(customGraphs, directed=False)
# print(triangle.head())
# plt = plot_metrics(customGraphs, triangle,'neato')
# plt.show()
#
# degree = compute_degree_centrality(customGraphs, directed=False)
# print(degree.head())
# plt = plot_metrics(customGraphs, degree,'twopi')
# plt.show()
#
# kcore = compute_kcore(customGraphs, directed=False)
# print(kcore.head())
# plt = plot_metrics(customGraphs, kcore,'twopi')
# plt.show()
#
# triangle = compute_triangles(customGraphs, directed=False)
# print(triangle.head())
# plt = plot_metrics(customGraphs, triangle,'twopi')
# plt.show()
#
# degree = compute_degree_centrality(customGraphs, directed=False)
# print(degree.head())
# plt = plot_metrics(customGraphs, degree,'sfdp')
# plt.show()
#
# kcore = compute_kcore(customGraphs, directed=False)
# print(kcore.head())
# plt = plot_metrics(customGraphs, kcore,'sfdp')
# plt.show()
#
# triangle = compute_triangles(customGraphs, directed=False)
# print(triangle.head())
# plt = plot_metrics(customGraphs, triangle,'sfdp')
# plt.show()

# plt = static_visualisation(customGraphs, layout='neato', title='Railway Graph NEATO')
# plt.show()
#
# plt = static_visualisation(customGraphs, layout='twopi', title='Railway Graph TWOPI')
# plt.show()
#
# plt = static_visualisation(customGraphs, layout='sfdp', title='Railway Graph SFDP')
# plt.show()
#
# plt = static_visualisation(customGraphs, layout='map', title='Railway Graph MAP')
# plt.show()


# # ----------------------------------------------------------------------------------------
#
# # global_metrics = compute_global_metrics(networkx)
# # print(global_metrics.head())
#
# # ----------------------------------------------------------------------------------------
#
# # directed_node_metrics = compute_node_metrics(networkGraphs, directed=False)
# # print(directed_node_metrics.head())
#
# # ----------------------------------------------------------------------------------------
#
# # undirected_node_metrics = compute_node_metrics(networkx, directed=False)
# # print(undirected_node_metrics.head())
#
# # ----------------------------------------------------------------------------------------
#
# # plt_directed = plot_static_on_map(networkx, 'Railway Network Directed Graph', directed=True)
# # plt_directed.show()
#
# # ----------------------------------------------------------------------------------------
# #
# # plt_undirected = plot_static_on_map(networkx, 'Railway Network Undirected Graph', directed=False)
# # plt_undirected.show()
#
# # ----------------------------------------------------------------------------------------
# #
# # temporal_graphs = create_temporal_subgraph(multi_networkx)
# # print(len(temporal_graphs))
# # slider, plt = plot_temporal_graphs(temporal_graphs)
# # display(slider)
# # plt.show()
#
# # ----------------------------------------------------------------------------------------
#
# # degree_centrality = compute_degree_centrality(networkGraphs, directed=False)
# # print(degree_centrality.head())
# # un_directed_degree_centrality = compute_degree_centrality(networkx, directed=False)
# # print(un_directed_degree_centrality.head())
# #
# # betweenes_centrality = compute_betweeness_centrality(networkx)
# # print(betweenes_centrality.head())
# # un_directed_betweenes_centrality = compute_betweeness_centrality(networkx, directed=False)
# # print(un_directed_betweenes_centrality.head())
# #
# # closeness_centrality = compute_closeness_centrality(networkx)
# # print(closeness_centrality.head())
# # un_directed_closeness_centrality = compute_closeness_centrality(networkx, directed=False)
# # print(un_directed_closeness_centrality.head())
# #
# # eigenvector_centrality = compute_eigen_centrality(networkx)
# # print(eigenvector_centrality.head())
# # un_directed_eigenvector_centrality = compute_eigen_centrality(networkx, directed=False)
# # print(un_directed_eigenvector_centrality.head())
#
# # ----------------------------------------------------------------------------------------
#
#
# # import geopandas as gpd
# # world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
# # #
# # # #plot the section of the map with min and max lat and long
# # ax = world.plot(edgecolor='black')
# # ax.set_xlim(networkGraphs.get_min_long(), networkGraphs.get_max_long())
# # ax.set_ylim(networkGraphs.get_min_lat(), networkGraphs.get_max_lat())
# # ax.set_title('Railway Network')
# # plt.show()
# # plot_static_on_map(networkGraphs, 'Railway Network Undirected Graph', directed=False).show()
# # static_visualisation(networkGraphs, 'Railway Network Undirected Graph', directed=False, multi=False, background=False, edges=False).show()
#
# # china = world[world['name'] == 'China']
# # print(china)
# metrics = compute_node_metrics(networkGraphs, directed=False)
# plot_metrics_on_map(networkGraphs, metrics, 'Metrics Centrality Undirected', directed=False).show()
# metrics = compute_node_metrics(networkGraphs, directed=True)
# plot_metrics_on_map(networkGraphs, metrics, 'Metrics Centrality Directed', directed=True).show()
