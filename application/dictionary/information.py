tooltips = {
    'multi': 'Enable or disable the ability to have multiple edges between two nodes, allowing for richer network '
             'analysis and representation.',

    'directed': 'Switch between directed and undirected graph analysis to account for the direction of connections in '
                'your network.',

    'dynamic': 'Activate to enable interactive node movement, allowing you to rearrange and explore the network '
               'structure more intuitively.',

    'layout_dropdown': "Select from a variety of graph layouts to optimize the visualization and interpretation of "
                       "your network's structure and relationships.",

    'network_tab': 'Interactively view and explore your graph, gaining insights into the structure and relationships '
                   'within your network data.',

    'temporal_tab': 'Examine the changes and trends in your network data over time, revealing patterns, growth, '
                    'and evolution within the graph.',

    'heatmap_tab': 'Discover patterns and relationships in your network data through a color-coded matrix, providing '
                   'an intuitive and visually appealing representation of connections and strengths.',
    'layout_tab': 'Interactively view and explore your graph, gaining insights into the structure and relationships '
                  'within your network data.',

    'histogram_tab': 'Gain insights into the distribution of network metrics by visualizing them as histograms, '
                     'simplifying the identification of patterns and trends within your data set.',

    'boxplot_tab': 'Analyze the distribution and variability of network metrics using boxplots, offering a clear view '
                   'of central tendencies, dispersion, and potential outliers in your data set.',

    'violinplot_tab': 'Examine the distribution and density of network metrics with violin plots, providing a '
                      'comprehensive visualization of data distribution, central tendencies, and potential outliers.',

    'number_of_clusters': 'Enter the desired number of clusters to generate, allowing for a customizable partitioning '
                          'of your network data for more focused analysis and interpretation.',

    'parameters': 'Customize the p and q parameters to optimize the Node2Vec analysis for your network data, '
                  'balancing the exploration of local and global information and adjusting the search strategy for '
                  'optimal performance.',

    'dimension': 'Specify the number of dimensions for embedding your network data, optimizing the representation and '
                 'analysis of complex structures and relationships within the graph.',

    'model_dropdown': 'Choose from a range of Graph Neural Network (GNN) models to best suit your network analysis '
                      'needs, leveraging advanced techniques for data representation and interpretation.',

    'features_checkbox': 'Select to include network metrics as input features for GNN training, enriching the '
                         'learning process with additional information and potentially improving model performance.',

    'attack_summary': "Review the details of changes made during resilience analysis, including node and edge "
                      "removals, to better understand the impact on your network's robustness and vulnerability.",

    'type_of_attack': "Select the network metric to compute for the malicious resilience analysis, enabling you to "
                      "evaluate the impact of targeted attacks on specific network properties and assess the "
                      "network's vulnerability to such attacks.",

    'node_tab': "Enter the desired number of nodes to remove from the network for resilience analysis, allowing you "
                "to evaluate the impact of node deletions on the network's overall stability and vulnerability.",

    'threshold_tab': "Enter the threshold value for the network metric that will be used to determine which nodes to "
                     "remove during the malicious resilience analysis, allowing you to simulate targeted attacks on "
                     "nodes with high metric values and evaluate the network's vulnerability to such attacks.",

    'edge_tab': "Enter the desired number of edges to randomly remove from the network for resilience analysis, "
                "enabling you to assess the impact of random deletions on the network's overall stability and "
                "vulnerability.",

    'type_of_cluster': 'Choose from a range of clustering algorithms to use in resilience analysis, enabling a more '
                       'nuanced and targeted approach to network partitioning and vulnerability assessment.',

    'number_of_cluster_to_generate': 'Specify the total number of clusters to generate for resilience analysis, '
                                     'enabling a customized partitioning of the network to better understand its '
                                     'vulnerability to disruption.',

    'number_of_cluster_to_attack': "Indicate the number of clusters to be removed during resilience analysis, "
                                   "allowing you to simulate targeted attacks or disruptions and assess the impact on "
                                   "your network's stability and robustness.",

    'list_of_nodes': 'Enter a list of nodes to remove from the network for a personalized resilience analysis, '
                     'allowing you to evaluate the impact of specific node deletions on the overall network stability.',

}

description = {
    'all_centrality': "Centrality <b>quantifies the importance or influence</b> of nodes within a network based on "
                      "their connections and relationships. By identifying key nodes, centrality measures help "
                      "uncover <b>critical hubs</b>, <b>efficient information spreaders</b>, or <b>bridges between "
                      "subgroups</b>. Analyzing centrality provides valuable insights into network dynamics and the "
                      "significance of specific nodes.",

    'centrality_degree': "Degree centrality evaluates a node's importance based on its <b>number of connections</b>. "
                         "Nodes with high degree centrality have more connections, making them influential in the "
                         "network. This measure is useful for identifying key nodes that impact information flow or "
                         "network connectivity.",

    'centrality_eigenvector': "Eigenvector centrality measures a node's importance by considering not only its "
                              "<b>direct connections</b> but also the <b>influence of its neighbors</b>. Nodes with "
                              "high eigenvector centrality are connected to other highly connected nodes, amplifying "
                              "their impact within the network. This measure highlights nodes that might be "
                              "strategically positioned to reach or influence a large portion of the network, "
                              "even if they have fewer direct connections.",

    'centrality_closeness': "Closeness centrality assesses a node's importance based on its <b>proximity to all other "
                            "nodes</b> in the network. A node with high closeness centrality can reach other nodes "
                            "quickly, making it central in terms of information flow or interaction. This measure is "
                            "useful for identifying nodes that can efficiently <b>disseminate information</b> or act "
                            "as intermediaries between distant parts of the network.",

    'centrality_betwenness': "Betweenness centrality quantifies a node's importance based on its role as a <b>bridge "
                             "between other nodes</b> in the network. Nodes with high betweenness centrality lie on a "
                             "significant number of shortest paths between other nodes, indicating their potential to "
                             "control or facilitate the flow of information. This measure is useful for identifying "
                             "nodes that can <b>connect different parts</b> of the network or detect potential "
                             "bottlenecks.",

    'centrality_load': "Load centrality measures a node's importance by evaluating its <b>contribution to the total "
                       "flow</b> within the network. Nodes with high load centrality have a significant impact on the "
                       "flow of information or resources, as they handle a large portion of the network's traffic. "
                       "This measure is useful for identifying nodes that are <b>critical for maintaining "
                       "connectivity</b> and ensuring efficient communication or resource distribution across the "
                       "network.",

    'node_all': "Node metrics provide a comprehensive understanding of a node's role and importance within a network. "
                "These measures encompass various aspects of connectivity, influence, and centrality. Analyzing these "
                "metrics helps identify key nodes, influential spreaders, and potential bottlenecks, "
                "offering valuable insights into the network's structure, information flow, and overall dynamics.",

    'node_degree': "Node degree is a fundamental metric that indicates the <b>number of connections</b> a node has "
                   "within a network. By examining the degree, one can identify well-connected or isolated nodes, "
                   "providing insights into the node's potential influence and role in the network.",

    'node_kcore': "Node k-core is a metric that assesses a node's position within the network's <b>core "
                  "structure</b>. A node belongs to a k-core if it is part of a subgraph where all nodes have at "
                  "least <b>k connections</b> within the subgraph. Higher k-core values indicate that a node is more "
                  "centrally embedded within a densely connected group. Analyzing k-core helps identify nodes that "
                  "are part of <b>stable, highly interconnected subgroups</b>, which can be crucial for understanding "
                  "the network's resilience and community structure. <i>K-Core computation allows for Directed but "
                  "not Multi graphs.</i>",

    'node_triangle': "Node triangles represent a metric that evaluates the <b>local clustering</b> of a node within a "
                     "network. A triangle is formed when a node and two of its neighbors are connected, creating a "
                     "<b>closed loop of three nodes</b>. By examining the number of triangles a node participates in, "
                     "one can assess its tendency to form tightly connected groups. This metric helps identify nodes "
                     "that contribute to the network's <b>cohesion and community structure</b>, revealing potential "
                     "subgroups or areas of high connectivity.",

    'node_pagerank': "Node PageRank is a metric that estimates a node's <b>relative importance</b> within a network, "
                     "considering both the <b>quantity and quality</b> of its connections. Inspired by the algorithm "
                     "used by Google Search, PageRank assigns a higher score to nodes connected to other high-ranking "
                     "nodes. This measure helps identify influential nodes that may not have the most connections but "
                     "are connected to other significant nodes, providing valuable insights into the <b>network's "
                     "hierarchy and power distribution</b>.",

    'visualisation': "The visualization page offers an interactive and intuitive way to explore and analyze your "
                     "network data. By leveraging various <b>graph layouts</b>, you can uncover patterns, trends, "
                     "and relationships within the network more effectively. The visualization tools allow you to "
                     "focus on specific nodes or subgraphs, adjust the level of detail, and customize the appearance "
                     "to better understand the <b>structure, dynamics, and key features</b> of your network. "
                     "Experiment with different settings to gain valuable insights and reveal hidden aspects of your "
                     "data.",

    'global_metrics': "The Global Metrics page provides an overview of your network's overall structure and "
                      "properties through a comprehensive set of aggregated metrics. These metrics offer insights "
                      "into various aspects of your network, including connectivity, centrality, cohesion, "
                      "and efficiency. By examining these global measures, you can gain a deeper understanding of the "
                      "network's characteristics and identify patterns or trends that may influence its behavior. "
                      "Comparing global metrics across different networks or over time can also help reveal "
                      "underlying relationships and highlight the impact of network changes.",

    'louvain': "The Louvain clustering page showcases the <b>community structure</b> of your network using the "
               "Louvain community detection algorithm. This method identifies groups of nodes with dense internal "
               "connections and sparse external links. Analyzing Louvain clustering reveals network organization, "
               "relationships between communities, and node roles within these groups, aiding in the detection of "
               "shared interests or functional modules.",

    'greedy_modularity': "The Greedy Modularity clustering highlights the <b>community structure</b> within your "
                         "network using the Greedy Modularity optimization algorithm. This method discovers groups of "
                         "nodes with strong internal connections and fewer external links. Examining "
                         "greedy_modularity results uncovers network organization, inter-community relationships, "
                         "and individual node roles, which can be valuable for detecting common interests or "
                         "functional clusters.",

    'label_propagation': "The label_propagation clustering page displays the <b>community structure</b> of your "
                         "network using the Label Propagation algorithm. This method identifies groups of nodes with "
                         "dense internal connections and minimal external links. By exploring label propagation "
                         "results, you can uncover network organization, relationships between communities, "
                         "and individual node roles, providing insights into shared interests or functional groups.",

    'asyn_lpa': "The Asynchronous Label Propagation clustering clustering presents the <b>community structure</b> "
                "within your network using the Asynchronous Label Propagation algorithm. This method detects groups "
                "of nodes with high internal connectivity and sparse external connections. Investigating asyn_lpa "
                "results reveals network organization, inter-community relationships, and node roles within groups, "
                "offering insights into shared interests or functional subgroups.",

    'k_clique': "The K-Clique clustering page showcases the <b>community structure</b> of your network using the "
                "K-Clique Percolation method. This algorithm identifies groups of nodes that form cliques of size "
                "<b>k</b>, where nodes are densely interconnected. By examining K_clique results, you can uncover "
                "network organization, relationships between communities, and individual node roles, "
                "providing valuable insights into shared interests or functional clusters.",

    'spectral': "The Spectral clustering page highlights the <b>community structure</b> within your network using the "
                "Spectral Clustering algorithm. This method uncovers groups of nodes with strong internal connections "
                "and fewer links to other groups, based on the network's <b>spectral properties</b>. Analyzing "
                "spectral clustering results reveals network organization, inter-community relationships, "
                "and individual node roles, offering insights into shared interests or functional modules.",

    'kmeans': 'The K-Means clustering displays the <b>community structure</b> within your network using the '
              'K-Means Clustering algorithm. This method groups nodes based on their <b>topological similarity</b> in '
              'the network, finding clusters with strong internal connections and fewer external links. Examining '
              'K-Means Clustering results uncovers network organization, relationships between communities, '
              'and individual node roles, providing insights into shared interests or functional groups.',

    'agglomerative': "The Agglomerative clustering illustrates the <b>community structure</b> within your "
                     "network using the Agglomerative Hierarchical Clustering algorithm. This method progressively "
                     "merges nodes or clusters with the highest similarity, resulting in a hierarchy of nested groups "
                     "with strong internal connections and fewer external links. Analyzing agglomerative clustering "
                     "reveals network organization, inter-community relationships, and individual node roles, "
                     "offering insights into shared interests or functional subgroups.",

    'dbscan': "The DBSCAN clustering presents the <b>community structure</b> within your network using the "
              "DBSCAN (Density-Based Spatial Clustering of Applications with Noise) algorithm. This method identifies "
              "clusters of nodes with high <b>density</b> and minimal connections to other groups while classifying "
              "sparsely connected nodes as noise. Exploring DBSCAN results uncovers network organization, "
              "relationships between communities, and individual node roles, providing insights into shared interests "
              "or functional groups.",

    'hotspot_density': "Hotspot density visualizes <b>high-density regions</b> within your network using a "
                       "heatmap-like representation. Hotspots represent areas where nodes are densely interconnected, "
                       "suggesting strong relationships or shared interests among the group members. By examining "
                       "hotspot density, you can identify significant clusters, gain insights into the network's "
                       "community structure, and uncover key areas that may have a substantial impact on the "
                       "network's overall dynamics and information flow.",

    'resilience_analysis_malicious': "The malicious resilience analysis evaluates your network's <b>resilience "
                                     "to targeted attacks</b> based on node metrics. By simulating the removal of "
                                     "nodes with the highest centrality, degree, or other relevant metrics, "
                                     "this analysis helps you understand the network's vulnerability to malicious "
                                     "activities. Examining the impact of these targeted removals on network "
                                     "connectivity and structure can inform strategies to <b>enhance robustness</b> "
                                     "and protect critical nodes or subgroups from potential threats.",

    'resilience_analyisis_random': "The random resilience analysis assesses your network's <b>resilience to "
                                   "random failures</b> by simulating the removal of nodes without considering their "
                                   "metrics. This analysis helps gauge the network's ability to withstand unexpected "
                                   "disruptions or errors. By examining the impact of random removals on network "
                                   "connectivity and structure, you can identify potential vulnerabilities and "
                                   "develop strategies to <b>improve robustness</b> and maintain the stability of the "
                                   "network under various conditions.",

    'resilience_analyisis_cluster': "The cluster resilience analysis investigates your network's <b>resilience "
                                    "against attacks or failures within specific clusters</b>. By simulating the "
                                    "removal of nodes within identified communities or high-density regions, "
                                    "this analysis helps you evaluate the network's ability to maintain connectivity "
                                    "and overall structure under targeted or random disruptions. Understanding the "
                                    "impact of these removals on cluster stability can inform strategies to "
                                    "<b>strengthen resilience</b> and safeguard critical subgroups from potential "
                                    "threats.",

    'resilience_analyisis_custom': "The custom resilience analysis allows you to assess your network's "
                                   "<b>resilience by simulating the removal of user-selected nodes</b>. This "
                                   "customizable analysis helps you examine the network's vulnerability to specific "
                                   "disruptions, whether targeted or random. By analyzing the impact of removing the "
                                   "chosen nodes on network connectivity and structure, you can gain insights into "
                                   "potential weaknesses and develop strategies to <b>enhance robustness</b> and "
                                   "protect critical nodes or subgroups from potential threats.",

    'node2vec_embedding': "The Node2Vec embedding presents the results of the <b>Node2Vec algorithm</b>, "
                          "which generates low-dimensional vector representations of nodes in your network. These "
                          "embeddings capture the network's topology and node relationships, preserving both local "
                          "and global structural information. By analyzing node2vec embeddings, you can uncover "
                          "patterns, identify similar nodes, and perform various machine learning tasks, "
                          "such as clustering, classification, or link prediction, to gain <b>deeper insights</b> "
                          "into your network's structure and dynamics.",

    'node2vec_agglomerative': "The Node2Vec with agglomerative clustering combines <b>Node2Vec embeddings</b> and "
                              "<b>Agglomerative Hierarchical Clustering</b> to reveal the community structure within "
                              "your network. Node2Vec captures the network's topology, while Agglomerative Clustering "
                              "groups similar nodes based on their embeddings. This combination allows for a deeper "
                              "understanding of network organization, relationships between communities, "
                              "and node roles within subgroups.",

    'node2vec_kmeans': "The Node2Vec with K-Means clustering merges <b>Node2Vec embeddings</b> and <b>K-Means "
                       "Clustering</b> to"
                       "highlight the community structure within your network. Node2Vec captures the network's "
                       "topological features, while K-Means Clustering groups similar nodes using their embeddings. "
                       "Examining the joint results provides insights into network organization, relationships "
                       "between communities, and individual node roles, unveiling shared interests or functional "
                       "clusters.",

    'node2vec_spectral': "The Node2Vec with spectral clustering integrates <b>Node2Vec embeddings</b> with <b>Spectral "
                         "Clustering</b> to uncover your network's community structure. Node2Vec embeddings preserve "
                         "network topology, and Spectral Clustering groups nodes based on these representations. By "
                         "analyzing the combined results, you can gain insights into network organization, "
                         "inter-community relationships, and individual node roles, revealing shared interests or "
                         "functional modules.",

    'dlembedding_embedding': "The Deep Learning Embedding showcases the <b>GNN embeddings</b> generated for your "
                             "network. GNNs are powerful models that capture the network's topology and node "
                             "features, creating low-dimensional vector representations of nodes that preserve both "
                             "local and global structural information. By analyzing GNN embeddings, you can uncover "
                             "hidden patterns, identify similar nodes, and perform various machine learning tasks, "
                             "such as clustering, classification, or link prediction, to gain <b>deeper insights</b> "
                             "into your network's structure and dynamics.",

    'dlembedding_agglomerative': "The Deep Learning Embedding with agglomerative clustering combines <b>GNN "
                                 "embeddings</b> and <b>Agglomerative"
                                 "Hierarchical Clustering</b> to reveal the community structure within your network. "
                                 "GNN captures the network's topology and node features, while Agglomerative "
                                 "Clustering groups similar nodes based on their embeddings. This combination allows "
                                 "for a deeper understanding of network organization, relationships between "
                                 "communities, and node roles within subgroups.",

    'dlembedding_spectral': "The Deep Learning Embedding with spectral clustering integrates <b>GNN embeddings</b> "
                            "and <b>Spectral Clustering</b> to uncover your network's community structure. GNN "
                            "embeddings preserve network topology and node features, and Spectral Clustering groups "
                            "nodes based on these representations. This combination enables deeper insights into "
                            "network organization, inter-community relationships, and individual node roles, "
                            "revealing shared interests or functional modules.",

    'dlembedding_kmeans': "The Deep Learning Embedding with K-Means clustering merges <b>GNN embeddings</b> and "
                          "<b>K-Means Clustering</b> to highlight the community structure within your network. GNN "
                          "captures the network's topological features and node attributes, while K-Means Clustering "
                          "groups similar nodes using their embeddings. This combination provides a more "
                          "comprehensive understanding of network organization, relationships between communities, "
                          "and individual node roles, unveiling shared interests or functional clusters.",
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',

}
