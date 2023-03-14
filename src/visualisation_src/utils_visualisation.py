import matplotlib.pyplot as plt
import geopandas as gpd
from plotly import graph_objects as go


# ----------------------------------------------------------------------------------------

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

def get_layout(networkGraphs, title=None, layout_='map'):  # FOR PLOTLY

    if layout_ == 'map':
        layout = go.Layout(
            title=f'<br>{title}',
            titlefont=dict(size=16, color='White'),
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
                center=dict(lat=networkGraphs.mid_lat, lon=networkGraphs.mid_long),
                showland=True,
            ),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
        )

    else:
        layout = go.Layout(
            title=f'<br>{title}',
            titlefont=dict(size=16, color='White'),
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
