import sys

from application.dictionary.information import *
from flask import Blueprint, render_template, session
from application.routes.template_metrics import *

from backend.common.common import process_metric

sys.path.insert(1, '../')
from src.metrics import *

centrality_routes = Blueprint('centrality_routes', __name__)


# -------------------------------------------CENTRALITY--------------------------------------

@centrality_routes.route('/centrality', endpoint='centrality', methods=['GET', 'POST'])
def centrality_all():
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)

    metrics = 'centralities'

    graph_names, graph_paths, df, tab, layout, multi_toggles, directed_toggles = process_metric(networkGraphs,
                                                                                                filename2, metrics)

    return render_template('centrality/centrality_all.html', example=df, tab=tab, method_name='All Centrality',
                           description=description['all_centrality'], tooltip_multi=tooltips['multi'],
                           multi_toggle=multi_toggles[0], directed_toggle=directed_toggles[0], layout=layout,
                           graph1=graph_paths[0],
                           multi_toggle2=multi_toggles[1], directed_toggle2=directed_toggles[1], layout2=layout,
                           graph2=graph_paths[1],
                           multi_toggle3=multi_toggles[2], directed_toggle3=directed_toggles[2], layout3=layout,
                           graph3=graph_paths[2],
                           multi_toggle4=multi_toggles[3], directed_toggle4=directed_toggles[3], layout4=layout,
                           graph4=graph_paths[3])


@centrality_routes.route('/centrality/degree', endpoint='degree', methods=['GET', 'POST'])
def centrality_degree():
    return process_single_metric('degree_centrality', 'centrality/centrality_degree.html', 'Degree Centrality',
                                 'centrality_degree')


@centrality_routes.route('/centrality/eigenvector', endpoint='eigenvector', methods=['GET', 'POST'])
def centrality_eigenvector():
    return process_single_metric('eigenvector_centrality', 'centrality/centrality_eigenvector.html',
                                 'Eigenvector Centrality', 'centrality_eigenvector')


@centrality_routes.route('/centrality/closeness', endpoint='closeness', methods=['GET', 'POST'])
def centrality_closeness():
    return process_single_metric('closeness_centrality', 'centrality/centrality_closeness.html', 'Closeness Centrality',
                                 'centrality_closeness')


@centrality_routes.route('/centrality/betwenness', endpoint='betwenness', methods=['GET', 'POST'])
def centrality_betwenness():
    return process_single_metric('betweenness_centrality', 'centrality/centrality_betwenness.html',
                                 'Betwenness Centrality', 'centrality_betwenness')


@centrality_routes.route('/centrality/load', endpoint='load', methods=['GET', 'POST'])
def centrality_load():
    return process_single_metric('load_centrality', 'centrality/centrality_load.html', 'Load Centrality',
                                 'centrality_load')
