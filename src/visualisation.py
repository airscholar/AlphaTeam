import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt

def static_visualisation(NetworkX_):
# return plotly figure
    return 0

def dyn_visualisation(NetworkX_):
#return html file
    return 0

def static_on_map(NetworkX_, title, directed=True):
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    china = world[world['name'] == 'China']
    china.plot(figsize=(10, 10))

    if directed:
        pos = nx.get_node_attributes(NetworkX_, 'pos')
        nx.draw(NetworkX_, pos, with_labels=False, node_size=3, node_color='red')
    else:
        # convert to undirected
        NetworkX_ = NetworkX_.to_undirected()
        pos = nx.get_node_attributes(NetworkX_, 'pos')
        nx.draw(NetworkX_, pos, with_labels=False, node_size=3, node_color='red')

    # plot axes
    plt.axis('on')
    plt.title(title)
    plt.show()

    return 0

def plot_shortest_distance(NetworkX_, path_):
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    china = world[world['name'] == 'China']
    china.plot(figsize=(10, 10))
    pos = nx.get_node_attributes(NetworkX_, 'pos')
    nx.draw(NetworkX_, pos, with_labels=False, node_size=3, node_color='red')

    #Plot the Shortest Path
    source = input("\nEnter the Start Node: ")
    target = input("\nEnter the Target Node: ")
    nx.shortest_path(NetworkX_, source=source, target=target)

    plt.axis('on')
    plt.title("Shortest Path between the entered source and target:")
    plt.show()

    # return plotly figure
    return 0

def plot_metrics(NetworkX_, dataFrame_, title_):
# return plotly figure
    return 0

def plot_metrics_on_map(NetworkX_, dataFrame_, title_):
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    china = world[world['name'] == 'China']
    china.plot(figsize=(10, 10))

    id = input("\nEnter your desired metrics to be displayed:"
               "\n1.Degree Centrality \n2.Closeness Centrality "
               "\n3.Betweenness Centrality \n4.Eigenvector Centrality \n")

    if id == 1:
        '''Degree Centrality'''
        # Calculate the degree centrality for each node
        degree_centralities = nx.degree_centrality(NetworkX_)

        # Plot the graph with node size proportional to degree centrality
        nx.draw(NetworkX_, with_labels=True, node_size=[v * 1000 for v in degree_centralities.values()])
        plt.show()


    elif id == 2:
        '''Closeness Centrality'''
        # Calculate the closeness centrality for each node
        closeness_centralities = nx.closeness_centrality(NetworkX_)

        # Plot the graph with node size proportional to closeness centrality
        nx.draw(NetworkX_, with_labels=True, node_size=[v * 1000 for v in closeness_centralities.values()])
        plt.show()

    elif id == 3:
        '''Betweenness Centrality'''
        # Calculate the betweenness centrality for each node
        betweenness_centralities = nx.betweenness_centrality(NetworkX_)

        # Plot the graph with node size proportional to betweenness centrality
        nx.draw(NetworkX_, with_labels=True, node_size=[v * 1000 for v in betweenness_centralities.values()])
        plt.show()

    elif id == 4:
        '''Eigenvector Centrality'''
        # Calculate the eigen vector centrality for each node
        eigen_centralities = nx.eigenvector_centrality(NetworkX_)

        # Plot the graph with node size proportional to eigen vector centrality
        nx.draw(NetworkX_, with_labels=True, node_size=[v * 1000 for v in eigen_centralities.values()])
        plt.show()

    # return plotly figure
    return 0

def plot_histogram(NetworkX_, dataFrame_, title_):
    id = input("\nEnter ID of the below options:"
               "\n1.Histogram of Longitude \n2.Histogram of Latitude "
               "\n3.Histogram of Station Number \n4.Histogram of Station ID \n")


    if id == 1:
        column_name = dataFrame_['lon']

        # Create a histogram of the column data
        plt.hist(column_name)
        plt.title('Histogram of Longitude')
        plt.xlabel('Longitude')
        plt.ylabel('Frequency')

        # Display the plot
        plt.show()

    elif id == 2:
        column_name = dataFrame_['lat']

        # Create a histogram of the column data
        plt.hist(column_name)
        plt.title('Histogram of Latitude')
        plt.xlabel('Latitude')
        plt.ylabel('Frequency')

        # Display the plot
        plt.show()

    elif id == 3:
        column_name = dataFrame_['st_no']

        # Create a histogram of the column data
        plt.hist(column_name)
        plt.title('Histogram of Station Number')
        plt.xlabel('Station Number')
        plt.ylabel('Frequency')

        # Display the plot
        plt.show()

    elif id == 4:
        column_name = dataFrame_['st_id']

        # Create a histogram of the column data
        plt.hist(column_name)
        plt.title('Histogram of Station ID')
        plt.xlabel('Station ID')
        plt.ylabel('Frequency')

        # Display the plot
        plt.show()

    # return plotly figure
    return 0

