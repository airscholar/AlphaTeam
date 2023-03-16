# FILE TO TEST THE FUNCTIONS IN THE SRC FOLDER
import matplotlib.pyplot as plt

from NetworkGraphs import NetworkGraphs
from preprocessing import *
from metrics import *
from visualisation import *
from machineLearning import *
import time

networkGraph = NetworkGraphs('../datasets/Railway.csv', type="RAILWAY")

plot_hotspot(networkGraph)

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



# customGraphs = NetworkGraphs('../datasets/CRYPTO.csv', type="CRYPTO")
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

