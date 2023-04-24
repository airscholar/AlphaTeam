import sys

from application.dictionary.information import *
from flask import Blueprint, render_template, session

from backend.common.common import process_metric

sys.path.insert(1, '../../')
from src.metrics import *

centrality_routes = Blueprint('centrality_routes', __name__)


# -------------------------------------------CENTRALITY--------------------------------------

@centrality_routes.route('/centrality', endpoint='centrality', methods=['GET', 'POST'])
def centrality_all():
    filename2 = session['filename2']
    metrics = 'centralities'

    return render_template('metrics/centrality/centrality_all.html', method_name='All Centrality',
                           description=description['all_centrality'], tooltip_multi=tooltips['multi'],
                           metricsType=metrics, session_id=filename2)

@centrality_routes.route('/centrality/degree', endpoint='degree', methods=['GET', 'POST'])
def centrality_degree():
    filename2 = session['filename2']
    metrics = 'degree_centrality'

    return render_template('metrics/centrality/centrality_degree.html', method_name='Degree Centrality',
                           description=description['centrality_degree'], tooltip_multi=tooltips['multi'],
                           metricsType=metrics, session_id=filename2)

@centrality_routes.route('/centrality/eigenvector', endpoint='eigenvector', methods=['GET', 'POST'])
def centrality_eigenvector():
    filename2 = session['filename2']
    metrics = 'eigenvector_centrality'

    return render_template('metrics/centrality/centrality_eigenvector.html', method_name='Eigenvector Centrality',
                           description=description['centrality_eigenvector'], tooltip_multi=tooltips['multi'],
                           metricsType=metrics, session_id=filename2)

@centrality_routes.route('/centrality/closeness', endpoint='closeness', methods=['GET', 'POST'])
def centrality_closeness():
    filename2 = session['filename2']
    metrics = 'closeness_centrality'

    return render_template('metrics/centrality/centrality_closeness.html', method_name='Closeness Centrality',
                           description=description['centrality_closeness'], tooltip_multi=tooltips['multi'],
                           metricsType=metrics, session_id=filename2)

@centrality_routes.route('/centrality/betwenness', endpoint='betwenness', methods=['GET', 'POST'])
def centrality_betwenness():
    filename2 = session['filename2']
    metrics = 'betweenness_centrality'

    return render_template('metrics/centrality/centrality_betwenness.html', method_name='Betwenness Centrality',
                           description=description['centrality_betwenness'], tooltip_multi=tooltips['multi'],
                           metricsType=metrics, session_id=filename2)

@centrality_routes.route('/centrality/load', endpoint='load', methods=['GET', 'POST'])
def centrality_load():
    filename2 = session['filename2']
    metrics = 'load_centrality'

    return render_template('metrics/centrality/centrality_load.html', method_name='Load Centrality',
                           description=description['centrality_load'], tooltip_multi=tooltips['multi'],
                           metricsType=metrics, session_id=filename2)