# FILE TO TEST THE FUNCTIONS IN THE SRC FOLDER
import matplotlib.pyplot as plt

from src.NetworkGraphs import NetworkGraphs
from src.metrics import *
from src.visualisation import *
from src.machineLearning import *
from src.utils import *
import time
import plotly.express as px
from threading import Thread

networkGraph = NetworkGraphs("../datasets/Railway.csv", type="RAILWAY",session_folder="uploads/584545")

# create empty plotly graph with text "No graph to display"
plotly_graph = go.Figure()
plotly_graph.update_layout(
    title="No graph to display",
    xaxis_title="",
    yaxis_title="",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="#7f7f7f"
    )
)
plotly_graph.write_html("no_graph.html")




print(get_metrics(networkGraph, "degree_centrality",directed=True, multi=True))



# plot_histogram(networkGraph, 'degree_centrality', directed=False, multi=False)
# plot_histogram(networkGraph, 'kcore', directed=False, multi=False)
# plot_histogram(networkGraph, 'triangles', directed=True, multi=True)
# plot_histogram(networkGraph, 'closeness_centrality', directed=False, multi=False)
# plot_histogram(networkGraph, 'betweenness_centrality', directed=False, multi=False)
# plot_histogram(networkGraph, 'eigenvector_centrality', directed=False, multi=False)
# plot_histogram(networkGraph, 'load_centrality', directed=False, multi=False)
# plot_histogram(networkGraph, 'pagerank', directed=False, multi=False)
# plot_histogram(networkGraph, 'centralities', directed=False, multi=False)
# plot_histogram(networkGraph, 'nodes', directed=False, multi=False)

# df = compute_node_metrics(networkGraph, directed=False, multi=False)
# generate_histogram_metric(df , "histo.html")
# plot_cluster(networkGraph, 'greedy_modularity', layout='map')
# plot_hotspot(networkGraph)


# plot_metric(networkGraph, 'degree_centrality', directed=False, dynamic=False, layout='map', plot=True)
# plot_metric(networkGraph, 'kcore', directed=False, dynamic=False, layout='map', plot=True)
# plot_metric(networkGraph, 'triangles', directed=False, dynamic=False, layout='map', plot=True)
# plot_metric(networkGraph, 'closeness_centrality', directed=False, dynamic=False, layout='map', plot=True)
# plot_metric(networkGraph, 'betweenness_centrality', directed=False, dynamic=False, layout='map', plot=True)
# plot_metric(networkGraph, 'eigenvector_centrality', directed=False, dynamic=False, layout='map', plot=True)
# plot_all_metrics(networkGraph, "nodes" ,directed=False, dynamic=False, layout='map', plot=True)
# plot_all_metrics(networkGraph, "centralities" ,directed=False, dynamic=False, layout='map', plot=True)
# plot_cluster(networkGraph, 'louvain', layout='map', plot=True)
# plot_cluster(networkGraph, 'greedy_modularity', layout='map', plot=True)
#
#
# plot_metric(networkGraph, 'degree_centrality', directed=False, dynamic=False, layout='twopi', plot=True)
# plot_metric(networkGraph, 'kcore', directed=False, dynamic=False, layout='twopi', plot=True)
# plot_all_metrics(networkGraph, "nodes" ,directed=False, dynamic=False, layout='twopi', plot=True)
# plot_all_metrics(networkGraph, "centralities" ,directed=False, dynamic=False, layout='twopi', plot=True)
# plot_cluster(networkGraph, 'louvain', layout='twopi', plot=True)
# plot_cluster(networkGraph, 'greedy_modularity', layout='twopi', plot=True)


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

