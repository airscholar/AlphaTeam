# FILE TO TEST THE FUNCTIONS IN THE SRC FOLDER

from src.NetworkGraphs import NetworkGraphs
from src.resilience import resilience

# networkGraph = NetworkGraphs('../datasets/Dune_Eth_transaction.csv', session_folder='plots', type="CRYPTO")
networkGraph = NetworkGraphs('../datasets/Railway.csv', session_folder='plots', type="RAILWAY")
# spectral_clustering(networkGraph)
# plot_hotspot(networkGraph)
# k_clique_clustering(networkGraph)
graph = resilience(networkGraph, attack='cluster', number_of_clusters=2, cluster_algorithm='spectral', total_clusters=15)

# plot_cluster(networkGraph, 'k_clique', dynamic=False, layout='map')
# edge_betweenness_clustering(networkGraph)
# plot_cluster(networkGraph, 'edge_betweenness', dynamic=False, layout='sfdp')
# plot_cluster(networkGraph, 'k_clique', dynamic=False, layout='twopi')
# plot_cluster(networkGraph, 'spectral', dynamic=False, layout='map')
# # hierarchical_clustering(networkGraph)

# def hierarchical_clustering(G):
#     # create a distance matrix based on the shortest path length between nodes in the graph
#     distance_matrix = nx.floyd_warshall_numpy(G)
#
#     # perform hierarchical clustering using the distance matrix
#     linkage_matrix = linkage(distance_matrix, method='average')
#
#     # plot the dendrogram
#     dendrogram(linkage_matrix, labels=list(G.nodes()))
#     plt.xlabel('Nodes')
#     plt.ylabel('Distance')
#     plt.show()
#
# hierarchical_clustering(networkGraph.Graph)
