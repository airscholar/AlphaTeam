tooltips = {
    'multi': 'Enable or disable the ability to have multiple edges between two nodes, allowing for richer network analysis and representation.',
    'directed': 'Switch between directed and undirected graph analysis to account for the direction of connections in your network.',
    'dynamic': 'Activate to enable interactive node movement, allowing you to rearrange and explore the network structure more intuitively.',
    'layout_dropdown': "Select from a variety of graph layouts to optimize the visualization and interpretation of your network's structure and relationships.",
    'network_tab': 'Interactively view and explore your graph, gaining insights into the structure and relationships within your network data.',
    'temporal_tab': 'Examine the changes and trends in your network data over time, revealing patterns, growth, and evolution within the graph.',
    'heatmap_tab': 'Discover patterns and relationships in your network data through a color-coded matrix, providing an intuitive and visually appealing representation of connections and strengths.',
    'layout_tab': 'Interactively view and explore your graph, gaining insights into the structure and relationships within your network data.',
    'histogram_tab': 'Gain insights into the distribution of network metrics by visualizing them as histograms, simplifying the identification of patterns and trends within your data set.',
    'boxplot_tab': 'Analyze the distribution and variability of network metrics using boxplots, offering a clear view of central tendencies, dispersion, and potential outliers in your data set.',
    'violinplot_tab': 'Examine the distribution and density of network metrics with violin plots, providing a comprehensive visualization of data distribution, central tendencies, and potential outliers.',
    'number_of_clusters': 'Enter the desired number of clusters to generate, allowing for a customizable partitioning of your network data for more focused analysis and interpretation.',
    'parameters': 'Customize the p and q parameters to optimize the Node2Vec analysis for your network data, balancing the exploration of local and global information and adjusting the search strategy for optimal performance.',
    'dimension': 'Specify the number of dimensions for embedding your network data, optimizing the representation and analysis of complex structures and relationships within the graph.',
    'model_dropdown': 'Choose from a range of Graph Neural Network (GNN) models to best suit your network analysis needs, leveraging advanced techniques for data representation and interpretation.',
    'features_checkbox': 'Select to include network metrics as input features for GNN training, enriching the learning process with additional information and potentially improving model performance.',
    'attack_summary': "Review the details of changes made during resilience analysis, including node and edge removals, to better understand the impact on your network's robustness and vulnerability.",
    'type_of_attack': "Select the network metric to compute for the malicious resilience analysis, enabling you to evaluate the impact of targeted attacks on specific network properties and assess the network's vulnerability to such attacks.",
    'node_tab': "Enter the desired number of nodes to remove from the network for resilience analysis, allowing you to evaluate the impact of node deletions on the network's overall stability and vulnerability.",
    'threshold_tab': "Enter the threshold value for the network metric that will be used to determine which nodes to remove during the malicious resilience analysis, allowing you to simulate targeted attacks on nodes with high metric values and evaluate the network's vulnerability to such attacks.",
    'edge_tab': "Enter the desired number of edges to randomly remove from the network for resilience analysis, enabling you to assess the impact of random deletions on the network's overall stability and vulnerability.",
    'type_of_cluster': 'Choose from a range of clustering algorithms to use in resilience analysis, enabling a more nuanced and targeted approach to network partitioning and vulnerability assessment.',
    'number_of_cluster_to_generate': 'Specify the total number of clusters to generate for resilience analysis, enabling a customized partitioning of the network to better understand its vulnerability to disruption.',
    'number_of_cluster_to_attack': "Indicate the number of clusters to be removed during resilience analysis, allowing you to simulate targeted attacks or disruptions and assess the impact on your network's stability and robustness.",
    'list_of_nodes': 'Enter a list of nodes to remove from the network for a personalized resilience analysis, allowing you to evaluate the impact of specific node deletions on the overall network stability.',
    '': '...',
    '': '...',
    '': '...',
    '': '...',
    '': '...',
    '': '...',
    '': '...',
    '': '...',
    '': '...',
}

description = {
    'all_centrality': 'Centrality is a concept that is widely used in network analysis to measure the importance of '
                      'individual nodes (or vertices) in a network. It is a way of quantifying the "centrality" or '
                      '"importance" of a node in a network by taking into account its relationships with other nodes.',
    'centrality_degree': 'This is the simplest measure of centrality and is based on the number of edges ('
                         'connections) a node has. In directed networks, degree centrality can be divided into '
                         'in-degree (number of incoming edges) and out-degree (number of outgoing edges) '
                         'centralities. Nodes with higher degree centrality are considered more important.',
    'centrality_eigenvector': 'This measure takes into account not only the number of connections a node has but also '
                              'the quality of those connections. Nodes with high eigenvector centrality are connected '
                              'to other well-connected nodes, and therefore, they have a higher influence within the '
                              'network.',
    'centrality_closeness': 'This measure calculates the average shortest path length between a node and all other '
                            'nodes in the network. Nodes with lower average shortest path lengths have higher '
                            'closeness centrality, indicating that they can reach other nodes more quickly, '
                            'making them more central in the network.',
    'centrality_betwenness': 'Betweenness centrality quantifies the number of times a node acts as a bridge along the '
                             'shortest path between two other nodes. Nodes with higher betweenness centrality are '
                             'critical for maintaining connectivity within the network and can control the flow of '
                             'information or resources.',
    'centrality_load': 'Load centrality is a measure in network analysis that quantifies the importance of a node '
                       'based on the amount of flow (e.g., information or resources) it handles within a network. It '
                       'is closely related to betweenness centrality',
    'node_all': '.. node_all page ..',
    'node_degree': '.. node_degree page ..',
    'node_kcore': '<i>k-core computation allows for Directed but not Multi graphs.</i>',
    'node_triangle': '.. node_triangle page ..',
    'node_pagerank': '.. node_pagerank page ..',
    'visualisation': '.. visualisaion page ..',
    'global_metrics': '.. global metrics page ..',
    'louvain': '.. louvain page ..',
    'greedy_modularity': '.. greedy_modularity page ..',
    'label_propagation': '.. label_propagation page ..',
    'asyn_lpa': '.. asyn_lpa page ..',
    'k_clique': '.. k_clique page ..',
    'spectral': '.. spectral page ..',
    'kmeans': '.. kmeans ..',
    'agglomerative': '.. agglomerative ..',
    'dbscan': '.. dbscan page ..',
    'hotspot_density': '.. hotspot density page ..',
    'resilience_analysis_malicious': '.. resilience_analysis_malicious page ..',
    'resilience_analyisis_random': '.. resilience_analyisis_random page ..',
    'resilience_analyisis_cluster': '.. resilience_analyisis_cluster ..',
    'resilience_analyisis_custom': '.. resilience_analyisis_custom ..',
    'node2vec_embedding': '.. node2vec_embedding ..',
    'node2vec_agglomerative': '.. node2vec_agglomerative ..',
    'node2vec_kmeans': '.. node2vec_kmeans ..',
    'node2vec_spectral': '.. node2vec_spectral ..',
    'dlembedding_embedding': '.. dlembedding_embedding ..',
    'dlembedding_agglomerative': '.. dlembedding_agglomerative ..',
    'dlembedding_kmeans': '.. dlembedding_kmeans ..',
    'dlembedding_spectral': '.. dlembedding_spectral ..',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',

}
