import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt


def static_visualisation(NetworkX_):
    # return plotly figure
    return 0


def dyn_visualisation(NetworkX_):
    # return html file
    return 0


def plot_static_on_map(networkx_, title, directed=True):
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    china = world[world['name'] == 'China']
    china.plot(figsize=(10, 10))

    if directed:
        pos = nx.get_node_attributes(networkx_, 'pos')
        nx.draw(networkx_, pos, with_labels=False, node_size=3, node_color='red')
    else:
        # convert to undirected
        networkx_ = networkx_.to_undirected()
        pos = nx.get_node_attributes(networkx_, 'pos')
        nx.draw(networkx_, pos, with_labels=False, node_size=3, node_color='red')

    # plot axes
    plt.axis('on')
    plt.title(title)

    return plt


def plot_shortest_distance(NetworkX_, path_):
    # return plotly figure
    return 0


def plot_metrics(NetworkX_, dataFrame_, title_):
    # return plotly figure
    return 0


def plot_metrics_on_map(NetworkX_, dataFrame_, title_):
    # return plotly figure
    return 0


def plot_histogram(NetworkX_, dataFrame_, title_):
    # return plotly figure
    return 0
