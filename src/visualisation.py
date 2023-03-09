import geopandas as gpd
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

#----------------------------------------------------------------------

def static_visualisation(NetworkX_):
# return plotly figure
    return 0

#----------------------------------------------------------------------

def dyn_visualisation(NetworkX_):
#return html file
    return 0

#----------------------------------------------------------------------

def static_on_map(NetworkX_, title, directed=True):
    '''
    :Function static_on_map(): Plot static map
    :param NetworkX_: NetworkX Graph
    :param title: Title of the plot
    :param directed:
    :return: 0
    '''

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

#----------------------------------------------------------------------

def plot_shortest_distance(NetworkX_, path_):
# return plotly figure
    return 0

#----------------------------------------------------------------------

def plot_metrics(NetworkX_, dataFrame_, title_):
# return plotly figure
    return 0

#----------------------------------------------------------------------

def plot_metrics_on_map(NetworkX_, dataFrame_, title_):
# return plotly figure
    return 0

#----------------------------------------------------------------------

def plot_histogram(NetworkX_, dataFrame_, title_):
    '''
    :Function plot_histogram(): Plot histogram
    :param NetworkX_: NetworkX Graph
    :param dataFrame_: Data frame of the file
    :param title: Title of the graph
    :return: 0
    '''

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

#----------------------------------------------------------------------

def degree_distribution(dataFrame_):
    '''
    :Function degree_distribution: Plot Degree distribution graph
    :param dataFrame_: Data frame of the file
    :return: 0
    '''
    # Calculate the frequency of each degree
    degree_counts = dataFrame_['st_id'].value_counts().reset_index()
    degree_counts.columns = ['st_id', 'frequency']

    # Normalize the frequency
    degree_counts['frequency'] = degree_counts['frequency'] / degree_counts['frequency'].sum()

    # Plot the degree distribution
    plt.scatter(degree_counts['st_id'], degree_counts['frequency'], color='blue')
    plt.xlabel('Number of Nodes(st_id)')
    plt.ylabel('Frequency')
    plt.title('Degree Distribution')
    plt.show()

    return 0

#----------------------------------------------------------------------

def cumulative_distribution(dataFrame_):
    '''
    :Function cumulative_distribution(): Plot cumulative distribution graph
    :param dataFrame_: Data Frame of the file
    :return: 0
    '''
    # create a dictionary to store the degrees of each node
    degree_dict = {}

    # loop over the nodes in the dataframe and count their degrees
    for node in dataFrame_['st_id']:
        degree = dataFrame_[dataFrame_['st_id'] == node].index.size
        degree_dict[node] = degree

    # create a dataframe from the degree dictionary
    degree_df = pd.DataFrame.from_dict(degree_dict, orient='index', columns=['degree'])

    # calculate the degree CDF
    degree_cdf = degree_df['degree'].value_counts(normalize=True).sort_index().cumsum()

    # plot the degree CDF
    plt.plot(degree_cdf.index, degree_cdf.values, marker='o')
    plt.xlabel('Degree')
    plt.ylabel('CDF')
    plt.title('Degree CDF Plot')
    plt.show()

    return 0

#----------------------------------------------------------------------

def comp_cumulative_distribution(dataFrame_):
    '''
    :Function comp_cumulative_distribution(): Plot complementary distribution graph
    :param dataFrame_: Data frame of the file
    :return: 0
    '''
    # create a dictionary to store the degrees of each node
    degree_dict = {}

    # loop over the nodes in the dataframe and count their degrees
    for node in dataFrame_['st_id']:
        degree = dataFrame_[dataFrame_['st_id'] == node].index.size
        degree_dict[node] = degree

    # create a dataframe from the degree dictionary
    degree_df = pd.DataFrame.from_dict(degree_dict, orient='index', columns=['degree'])

    # calculate the degree CCDF
    degree_ccdf = 1 - degree_df['degree'].value_counts(normalize=True).sort_index().cumsum()

    # plot the degree CCDF
    plt.loglog(degree_ccdf.index, degree_ccdf.values, marker='o')
    plt.xlabel('Degree')
    plt.ylabel('CCDF')
    plt.title('Degree CCDF Plot')
    plt.show()

    return 0

#----------------------------------------------------------------------

def kcore_distribution(NetworkX_, dataFrame_):
    '''
    :Function kcore_distribution(): Plot k-core distribution graph
    :param NetworkX_: NetworkX Graph
    :param dataFrame_: Data frame of the file
    :return: 0
    '''
    # Compute the K-core distribution of the graph
    kcore = nx.core_number(NetworkX_)
    hist = nx.classes.function.degree_histogram(kcore)

    # Plot the K-core distribution using Matplotlib
    plt.loglog(range(len(hist)), hist, 'o', label='K-core')
    plt.xlabel('K')
    plt.ylabel('Number of nodes')
    plt.legend()
    plt.show()

    return 0

#----------------------------------------------------------------------

def kcore_cumulative_distribution(NetworkX_, dataFrame_):
    '''
    :Function kcore_cumulative_distribution(): Plot k-core cumulative distribution graph
    :param NetworkX_: NetworkX Graph
    :param dataFrame_: Data frame of the file
    :return: 0
    '''
    # Calculate the k-core decomposition and get the core number for each node
    core_numbers = nx.core_number(NetworkX_)

    # Calculate the CDF of the core numbers
    cdf = pd.Series(core_numbers).value_counts().sort_index().cumsum()

    # Plot the CDF
    plt.plot(cdf.index, cdf / cdf.max(), '-o')
    plt.xlabel('Core number')
    plt.ylabel('Cumulative distribution function')
    plt.show()

    return 0

def kcore_comp_cumulative_distribution(NetworkX_, dataFrame_):
    '''
    :Function kcore_cumulative_distribution(): Plot k-core complementary cumulative distribution graph
    :param NetworkX_: NetworkX Graph
    :param dataFrame_: Data frame of the file
    :return: 0
    '''
    # Calculate the k-core decomposition and get the core number for each node
    core_numbers = nx.core_number(NetworkX_)

    # Calculate the CCDF of the core numbers
    ccdf = pd.Series(core_numbers).value_counts().sort_index(ascending=False).cumsum()

    # Plot the CCDF
    plt.loglog(ccdf.index, 1 - ccdf / ccdf.max(), '-o')
    plt.xlabel('Core number')
    plt.ylabel('Complementary cumulative distribution function')
    plt.show()

    return 0

#----------------------------------------------------------------------

def triangle_distribution(NetworkX_,dataFrame_):
    '''
    :Function triangle_distribution(): Plot traingle distribution graph
    :param NetworkX_: NetworkX Graph
    :param dataFrame_: Data frame of the file
    :return: 0
    '''
    # Create an empty graph and add nodes
    NetworkX_ = nx.Graph()
    NetworkX_.add_nodes_from(dataFrame_['st_id'])

    # Generate a random graph with the same number of nodes
    H = nx.gnm_random_graph(len(dataFrame_), len(dataFrame_))

    # Merge the two graphs
    NetworkX_.add_edges_from(H.edges())

    # Calculate the triangle distribution
    triangles = nx.triangles(NetworkX_)
    triangle_distribution = pd.Series(triangles).value_counts().sort_index()

    # Plot the triangle distribution
    plt.plot(triangle_distribution.index, triangle_distribution.values, '-o')
    plt.xlabel('Number of triangles')
    plt.ylabel('Number of nodes')
    plt.show()

    return 0

#----------------------------------------------------------------------

def triangle_cumulative_distribution(NetworkX_,dataFrame_):
    '''
    :Function triangle_cumulative_distribution(): Plot traingle cumulative distribution graph
    :param NetworkX_: NetworkX Graph
    :param dataFrame_: Data frame of the file
    :return: 0
    '''
    # Create an empty graph and add nodes
    NetworkX_ = nx.Graph()
    NetworkX_.add_nodes_from(dataFrame_['st_id'])

    # Generate a random graph with the same number of nodes
    H = nx.gnm_random_graph(len(dataFrame_), len(dataFrame_))

    # Merge the two graphs
    NetworkX_.add_edges_from(H.edges())

    # Calculate the triangle distribution
    triangles = nx.triangles(NetworkX_)
    triangle_distribution = pd.Series(triangles).value_counts().sort_index()

    # Calculate the triangle CDF
    triangle_cdf = triangle_distribution.cumsum() / triangle_distribution.sum()

    # Plot the triangle CDF
    plt.plot(triangle_cdf.index, triangle_cdf.values)
    plt.xlabel('Number of triangles')
    plt.ylabel('Cumulative probability')
    plt.show()

    return 0

#----------------------------------------------------------------------

def triangle_comp_cumulative_distribution(NetworkX_,dataFrame_):
    '''
    :Function triangle_comp_cumulative_distribution(): Plot traingle complemenatry cumulative distribution graph
    :param NetworkX_: NetworkX Graph
    :param dataFrame_: Data frame of the file
    :return: 0
    '''
    # Create an empty graph and add nodes
    NetworkX_ = nx.Graph()
    NetworkX_.add_nodes_from(dataFrame_['st_id'])

    # Generate a random graph with the same number of nodes
    H = nx.gnm_random_graph(len(dataFrame_), len(dataFrame_))

    # Merge the two graphs
    NetworkX_.add_edges_from(H.edges())

    # Calculate the triangle distribution
    triangles = nx.triangles(NetworkX_)
    triangle_distribution = pd.Series(triangles).value_counts().sort_index()

    # Calculate the triangle CCDF
    triangle_ccdf = 1 - triangle_distribution.cumsum() / triangle_distribution.sum()

    # Plot the triangle CCDF
    plt.plot(triangle_ccdf.index, triangle_ccdf.values)
    plt.xlabel('Number of triangles')
    plt.ylabel('Complementary cumulative probability')
    plt.show()

    return 0

#----------------------------------------------------------------------
