import matplotlib.pyplot as plt
import geopandas as gpd
from plotly import graph_objects as go
from utils import memoize
from tqdm import tqdm


# ----------------------------------------------------------------------------------------

@memoize
def plot_map(networkGraphs, background=True, edges=True):  # FOR MATPLOTLIB
    """
    :Function: Plot the map of the location of the graphs
    :param networkGraphs: Network graphs
    :param background: Boolean to indicate if the background is to be plotted or not
    :param edges: Boolean to indicate if the edges are to be plotted or not
    :return: Matplotlib plot
    """
    if not networkGraphs.is_spatial():
        return 0

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    world = world[(world.pop_est > 0) & (world.name != "Antarctica")]
    ax = world.plot(figsize=(10, 10), edgecolor='black' if edges else 'white',
                    color='white' if background else None)
    ax.set_xlim(networkGraphs.get_min_long(), networkGraphs.get_max_long())
    ax.set_ylim(networkGraphs.get_min_lat(), networkGraphs.get_max_lat())

    return plt


# ----------------------------------------------------------------------------------------

@memoize
def get_layout(networkGraphs, title=None, layout_='map'):  # FOR PLOTLY

    if layout_ == 'map':
        layout = go.Layout(
            title=f'<br>{title}',
            titlefont=dict(size=16, color='Black'),
            showlegend=False,
            hovermode='closest',
            annotations=[
                dict(
                    text="Alpha Team - 2023",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002,
                    font=dict(color='black')
                )
            ],
            geo=dict(
                scope='world',
                lataxis_range=[networkGraphs.min_lat, networkGraphs.max_lat],
                lonaxis_range=[networkGraphs.min_long, networkGraphs.max_long],
                center=dict(lat=networkGraphs.mid_lat,
                            lon=networkGraphs.mid_long),
                showland=True,
            ),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )

    else:
        layout = go.Layout(
            title=f'<br>{title}',
            titlefont=dict(size=16, color='Black'),
            showlegend=False,
            hovermode='closest',
            annotations=[
                dict(
                    text="Alpha Team - 2023",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002,
                    font=dict(color='black')
                )
            ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )

    return layout


# ----------------------------------------------------------------------------------------

@memoize
def generate_edge_trace(Graph, pos, layout):
    """
    :Function: Generate the edge trace for the plotly plot, leveraging the memoize decorator for cache optimization
    :param Graph: Network graph
    :param pos: Position of the nodes
    :param layout: Layout of the plot
    :return: Edge trace
    """
    if layout == 'map':
        edge_trace = go.Scattergeo(
            lon=[], lat=[], hoverinfo='none', mode='lines', line=dict(width=0.5, color='#888'))

    else:
        edge_trace = go.Scatter(
            x=[], y=[], hoverinfo='none', mode='lines', line=dict(width=0.5, color='#888'))

    for edge in tqdm(Graph.edges()):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        if layout == 'map':
            edge_trace['lon'] += (x0, x1, None)
            edge_trace['lat'] += (y0, y1, None)
        else:
            edge_trace['x'] += (x0, x1, None)
            edge_trace['y'] += (y0, y1, None)

    return edge_trace
