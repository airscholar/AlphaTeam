import sys

from flask import Blueprint, render_template, session

from application.dictionary.information import *

sys.path.insert(1, '../../')
from src.metrics import *

centrality_routes = Blueprint('centrality_routes', __name__)


# -------------------------------------------CENTRALITY--------------------------------------
@centrality_routes.route('/centrality', endpoint='centrality', methods=['GET', 'POST'])
def centrality_all():
    filename2 = session['filename2']
    metrics = 'centralities'
    networkGraphs = get_networkGraph(filename2)
    if networkGraphs.is_spatial():
        is_spatial = 'yes'
    else:
        is_spatial = 'no'

    return render_template('metrics/centrality/centrality_all.html', method_name='All Centrality',
                           is_spatial=is_spatial,
                           description=description['all_centrality'], tooltip_multi=tooltips['multi'],
                           tooltip_layout_tab=tooltips['layout_tab'], tooltip_histogram_tab=tooltips['histogram_tab'],
                           tooltip_boxplot_tab=tooltips['boxplot_tab'],
                           tooltip_violinplot_tab=tooltips['violinplot_tab'],
                           tooltip_directed=tooltips['directed'], tooltip_layout=tooltips['layout_dropdown'],
                           metricsType=metrics, session_id=filename2)


@centrality_routes.route('/centrality/degree', endpoint='degree', methods=['GET', 'POST'])
def centrality_degree():
    filename2 = session['filename2']
    metrics = 'degree_centrality'
    networkGraphs = get_networkGraph(filename2)
    if networkGraphs.is_spatial():
        is_spatial = 'yes'
    else:
        is_spatial = 'no'

    return render_template('metrics/centrality/centrality_degree.html', method_name='Degree Centrality',
                           is_spatial=is_spatial,
                           description=description['centrality_degree'], tooltip_multi=tooltips['multi'],
                           tooltip_layout_tab=tooltips['layout_tab'], tooltip_histogram_tab=tooltips['histogram_tab'],
                           tooltip_boxplot_tab=tooltips['boxplot_tab'],
                           tooltip_violinplot_tab=tooltips['violinplot_tab'],
                           tooltip_directed=tooltips['directed'], tooltip_layout=tooltips['layout_dropdown'],
                           tooltip_dynamic=tooltips['dynamic'],
                           metricsType=metrics, session_id=filename2)


@centrality_routes.route('/centrality/eigenvector', endpoint='eigenvector', methods=['GET', 'POST'])
def centrality_eigenvector():
    filename2 = session['filename2']
    metrics = 'eigenvector_centrality'
    networkGraphs = get_networkGraph(filename2)
    if networkGraphs.is_spatial():
        is_spatial = 'yes'
    else:
        is_spatial = 'no'

    return render_template('metrics/centrality/centrality_eigenvector.html', method_name='Eigenvector Centrality',
                           is_spatial=is_spatial,
                           description=description['centrality_eigenvector'], tooltip_multi=tooltips['multi'],
                           tooltip_layout_tab=tooltips['layout_tab'], tooltip_histogram_tab=tooltips['histogram_tab'],
                           tooltip_boxplot_tab=tooltips['boxplot_tab'],
                           tooltip_violinplot_tab=tooltips['violinplot_tab'],
                           tooltip_directed=tooltips['directed'], tooltip_layout=tooltips['layout_dropdown'],
                           tooltip_dynamic=tooltips['dynamic'],
                           metricsType=metrics, session_id=filename2)


@centrality_routes.route('/centrality/closeness', endpoint='closeness', methods=['GET', 'POST'])
def centrality_closeness():
    filename2 = session['filename2']
    metrics = 'closeness_centrality'
    networkGraphs = get_networkGraph(filename2)
    if networkGraphs.is_spatial():
        is_spatial = 'yes'
    else:
        is_spatial = 'no'

    return render_template('metrics/centrality/centrality_closeness.html', method_name='Closeness Centrality',
                           is_spatial=is_spatial,
                           description=description['centrality_closeness'], tooltip_multi=tooltips['multi'],
                           tooltip_layout_tab=tooltips['layout_tab'], tooltip_histogram_tab=tooltips['histogram_tab'],
                           tooltip_boxplot_tab=tooltips['boxplot_tab'],
                           tooltip_violinplot_tab=tooltips['violinplot_tab'],
                           tooltip_directed=tooltips['directed'], tooltip_layout=tooltips['layout_dropdown'],
                           tooltip_dynamic=tooltips['dynamic'],
                           metricsType=metrics, session_id=filename2)


@centrality_routes.route('/centrality/betwenness', endpoint='betwenness', methods=['GET', 'POST'])
def centrality_betwenness():
    filename2 = session['filename2']
    metrics = 'betweenness_centrality'
    networkGraphs = get_networkGraph(filename2)
    if networkGraphs.is_spatial():
        is_spatial = 'yes'
    else:
        is_spatial = 'no'

    return render_template('metrics/centrality/centrality_betwenness.html', method_name='Betwenness Centrality',
                           is_spatial=is_spatial,
                           description=description['centrality_betwenness'], tooltip_multi=tooltips['multi'],
                           tooltip_layout_tab=tooltips['layout_tab'], tooltip_histogram_tab=tooltips['histogram_tab'],
                           tooltip_boxplot_tab=tooltips['boxplot_tab'],
                           tooltip_violinplot_tab=tooltips['violinplot_tab'],
                           tooltip_directed=tooltips['directed'], tooltip_layout=tooltips['layout_dropdown'],
                           tooltip_dynamic=tooltips['dynamic'],
                           metricsType=metrics, session_id=filename2)


@centrality_routes.route('/centrality/load', endpoint='load', methods=['GET', 'POST'])
def centrality_load():
    filename2 = session['filename2']
    metrics = 'load_centrality'
    networkGraphs = get_networkGraph(filename2)
    if networkGraphs.is_spatial():
        is_spatial = 'yes'
    else:
        is_spatial = 'no'

    return render_template('metrics/centrality/centrality_load.html', method_name='Load Centrality',
                           is_spatial=is_spatial,
                           description=description['centrality_load'], tooltip_multi=tooltips['multi'],
                           tooltip_layout_tab=tooltips['layout_tab'], tooltip_histogram_tab=tooltips['histogram_tab'],
                           tooltip_boxplot_tab=tooltips['boxplot_tab'],
                           tooltip_violinplot_tab=tooltips['violinplot_tab'],
                           tooltip_directed=tooltips['directed'], tooltip_layout=tooltips['layout_dropdown'],
                           tooltip_dynamic=tooltips['dynamic'],
                           metricsType=metrics, session_id=filename2)
