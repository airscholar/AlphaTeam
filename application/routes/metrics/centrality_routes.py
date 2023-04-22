import sys

from application.dictionary.information import *
from flask import Blueprint, render_template, session
from application.routes.template_metrics import *

from backend.common.common import process_metric

sys.path.insert(1, '../../')
from src.metrics import *

centrality_routes = Blueprint('centrality_routes', __name__)


# -------------------------------------------CENTRALITY--------------------------------------

@centrality_routes.route('/centrality', endpoint='centrality', methods=['GET', 'POST'])
def centrality_all():
    filename2 = session['filename2']
    metrics = 'centralities'

    #graph_names, graph_paths, df, tab, layout, multi_toggles, directed_toggles = process_metric(networkGraphs,
    #                                                                                            filename2, metrics)

    return render_template('metrics/centrality/centrality_all.html', method_name='All Centrality',
                           description=description['all_centrality'], tooltip_multi=tooltips['multi'],
                           metricsType=metrics, session_id=filename2)


@centrality_routes.route('/centrality/degree', endpoint='degree', methods=['GET', 'POST'])
def centrality_degree():
    return process_single_metric('degree_centrality', 'metrics/centrality/centrality_degree.html', 'Degree Centrality',
                                 'centrality_degree')


@centrality_routes.route('/centrality/eigenvector', endpoint='eigenvector', methods=['GET', 'POST'])
def centrality_eigenvector():
    return process_single_metric('eigenvector_centrality', 'metrics/centrality/centrality_eigenvector.html',
                                 'Eigenvector Centrality', 'centrality_eigenvector')


@centrality_routes.route('/centrality/closeness', endpoint='closeness', methods=['GET', 'POST'])
def centrality_closeness():
    return process_single_metric('closeness_centrality', 'metrics/centrality/centrality_closeness.html', 'Closeness Centrality',
                                 'centrality_closeness')


@centrality_routes.route('/centrality/betwenness', endpoint='betwenness', methods=['GET', 'POST'])
def centrality_betwenness():
    return process_single_metric('betweenness_centrality', 'metrics/centrality/centrality_betwenness.html',
                                 'Betwenness Centrality', 'centrality_betwenness')


@centrality_routes.route('/centrality/load', endpoint='load', methods=['GET', 'POST'])
def centrality_load():
    return process_single_metric('load_centrality', 'metrics/centrality/centrality_load.html', 'Load Centrality',
                                 'centrality_load')
