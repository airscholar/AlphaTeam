import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display


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


def plot_temporal_graphs(temporal_graphs):
    # Create a figure and subplot
    fig, ax = plt.subplots()

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    china = world[world['name'] == 'China']
    # Draw the first graph
    china.plot(ax=ax)
    nx.draw(temporal_graphs[0], pos=nx.get_node_attributes(temporal_graphs[0], 'pos'), with_labels=False, node_size=1,
            node_color='red', ax=ax)
    ax.set_title(f"Temporal Graph at {0 // 1440}:{(0 // 60) % 24:02d}:{0 % 60:02d}")

    # Create a slider widget
    slider = widgets.IntSlider(min=0, max=len(temporal_graphs) - 1, value=0, description='Timeframe')

    # Define a function to update the plot when the slider is changed
    def update_plot(val):
        val = val['new']
        ax.clear()
        china.plot(ax=ax)
        nx.draw(temporal_graphs[val], pos=nx.get_node_attributes(temporal_graphs[0], 'pos'), with_labels=False,
                node_size=1, node_color='red', ax=ax)
        ax.set_title(f"Temporal Graph at {val // 1440}:{(val // 60) % 24:02d}:{val % 60:02d}")
        plt.show()

    # Attach the update function to the slider
    slider.observe(update_plot, names='value')

    return [slider, plt]
    # # Display the slider widget and plot
    # display(slider)
    # plt.show()


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
