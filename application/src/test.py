# FILE TO TEST THE FUNCTIONS IN THE SRC FOLDER
from src.NetworkGraphs import NetworkGraphs
from src.preprocessing import *
from src.metrics import *
from src.visualisation import *

# ----------------------------------------------------------------------------------------

networkGraphs = NetworkGraphs('../datasets/Railway.csv', type="RAILWAY", spatial =True)
# plot_static_on_map(networkGraphs, 'Railway Network Undirected Graph', directed=False).show()
kcore = compute_kcore(networkGraphs)
print(kcore.head())
un_kcore = compute_kcore(networkGraphs, directed=False)
print(un_kcore.head())
triangle = compute_triangles(networkGraphs, directed=False)
print(triangle.head())
un_triangle = compute_triangles(networkGraphs, directed=False)
print(un_triangle.head())
degree = compute_nodes_degree(networkGraphs, directed=False)
print(degree.head())
un_degree = compute_nodes_degree(networkGraphs, directed=False)
print(un_degree.head())
kcore_cdf = compute_CCDF(kcore,kcore.columns[1])
print(kcore_cdf.head())

histogram(kcore, 'K-Core',title='K-Core Histogram')
histogram(un_kcore, 'K-Core',title='UnK-Core Histogram')
histogram(triangle, 'Triangle',title='Triangle Histogram')
histogram(un_triangle, 'Triangle',title='UnTriangle Histogram')
histogram(degree, 'Degree',title='Degree Histogram')
histogram(un_degree, 'Degree',title='UnDegree Histogram')
histogram(kcore_cdf, 'CCDF',title='K-Core CCDF Histogram')
histogram(kcore_cdf, 'CDF',title='K-Core CDF Histogram')


# ----------------------------------------------------------------------------------------

# global_metrics = compute_global_metrics(networkx)
# print(global_metrics.head())

# ----------------------------------------------------------------------------------------

# directed_node_metrics = compute_node_metrics(networkGraphs, directed=False)
# print(directed_node_metrics.head())

# ----------------------------------------------------------------------------------------

# undirected_node_metrics = compute_node_metrics(networkx, directed=False)
# print(undirected_node_metrics.head())

# ----------------------------------------------------------------------------------------

# plt_directed = plot_static_on_map(networkx, 'Railway Network Directed Graph', directed=True)
# plt_directed.show()

# ----------------------------------------------------------------------------------------
#
# plt_undirected = plot_static_on_map(networkx, 'Railway Network Undirected Graph', directed=False)
# plt_undirected.show()

# ----------------------------------------------------------------------------------------
#
# temporal_graphs = create_temporal_subgraph(multi_networkx)
# print(len(temporal_graphs))
# slider, plt = plot_temporal_graphs(temporal_graphs)
# display(slider)
# plt.show()

# ----------------------------------------------------------------------------------------

# degree_centrality = compute_degree_centrality(networkGraphs, directed=False)
# print(degree_centrality.head())
# un_directed_degree_centrality = compute_degree_centrality(networkx, directed=False)
# print(un_directed_degree_centrality.head())
#
# betweenes_centrality = compute_betweeness_centrality(networkx)
# print(betweenes_centrality.head())
# un_directed_betweenes_centrality = compute_betweeness_centrality(networkx, directed=False)
# print(un_directed_betweenes_centrality.head())
#
# closeness_centrality = compute_closeness_centrality(networkx)
# print(closeness_centrality.head())
# un_directed_closeness_centrality = compute_closeness_centrality(networkx, directed=False)
# print(un_directed_closeness_centrality.head())
#
# eigenvector_centrality = compute_eigen_centrality(networkx)
# print(eigenvector_centrality.head())
# un_directed_eigenvector_centrality = compute_eigen_centrality(networkx, directed=False)
# print(un_directed_eigenvector_centrality.head())

# ----------------------------------------------------------------------------------------


import geopandas as gpd
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
#
# #plot the section of the map with min and max lat and long
ax = world.plot(edgecolor='black')
ax.set_xlim(networkGraphs.get_min_long(), networkGraphs.get_max_long())
ax.set_ylim(networkGraphs.get_min_lat(), networkGraphs.get_max_lat())
ax.set_title('Railway Network')
plt.show()
plot_static_on_map(networkGraphs, 'Railway Network Undirected Graph', directed=False).show()