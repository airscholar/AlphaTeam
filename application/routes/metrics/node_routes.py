import sys

from application.dictionary.information import *
from flask import Blueprint, render_template, session

from backend.common.common import process_metric

sys.path.insert(1, '../../')
from src.metrics import *

node_routes = Blueprint('node_routes', __name__)


# -------------------------------------------NODE--------------------------------------------

@node_routes.route('/node_all', endpoint='node_all', methods=['GET', 'POST'])
def node_all():
    filename2 = session['filename2']
    metrics = 'nodes'

    return render_template('metrics/nodes/node_all.html', method_name='All Nodes',
                           description=description['node_all'], tooltip_multi=tooltips['multi'],
                           tooltip_layout_tab=tooltips['layout_tab'], tooltip_histogram_tab=tooltips['histogram_tab'],
                           tooltip_boxplot_tab=tooltips['boxplot_tab'], tooltip_violinplot_tab=tooltips['violinplot_tab'],
                           tooltip_directed=tooltips['directed'], tooltip_layout=tooltips['layout_dropdown'],
                           metricsType=metrics, session_id=filename2)

@node_routes.route('/node/degree', endpoint='node_degree', methods=['GET', 'POST'])
def node_degree():
    filename2 = session['filename2']
    metrics = 'degree'

    return render_template('metrics/nodes/node_degree.html', method_name='Node Degree',
                           description=description['node_degree'], tooltip_multi=tooltips['multi'],
                           tooltip_layout_tab=tooltips['layout_tab'], tooltip_histogram_tab=tooltips['histogram_tab'],
                           tooltip_boxplot_tab=tooltips['boxplot_tab'], tooltip_violinplot_tab=tooltips['violinplot_tab'],
                           tooltip_directed=tooltips['directed'], tooltip_layout=tooltips['layout_dropdown'],
                           tooltip_dynamic=tooltips['dynamic'],
                           metricsType=metrics, session_id=filename2)

@node_routes.route('/node/kcore', endpoint='node_kcore', methods=['GET', 'POST'])
def node_kcore():
    filename2 = session['filename2']
    metrics = 'kcore'

    return render_template('metrics/nodes/node_kcore.html', method_name='Node K Core',
                           description=description['node_kcore'], tooltip_multi=tooltips['multi'],
                           tooltip_layout_tab=tooltips['layout_tab'], tooltip_histogram_tab=tooltips['histogram_tab'],
                           tooltip_boxplot_tab=tooltips['boxplot_tab'], tooltip_violinplot_tab=tooltips['violinplot_tab'],
                           tooltip_directed=tooltips['directed'], tooltip_layout=tooltips['layout_dropdown'],
                           tooltip_dynamic=tooltips['dynamic'],
                           metricsType=metrics, session_id=filename2)

@node_routes.route('/node/triangle', endpoint='node_triangle', methods=['GET', 'POST'])
def node_triangle():
    filename2 = session['filename2']
    metrics = 'triangles'

    return render_template('metrics/nodes/node_triangle.html', method_name='Node Triangle',
                           description=description['node_triangle'], tooltip_multi=tooltips['multi'],
                           tooltip_layout_tab=tooltips['layout_tab'], tooltip_histogram_tab=tooltips['histogram_tab'],
                           tooltip_boxplot_tab=tooltips['boxplot_tab'], tooltip_violinplot_tab=tooltips['violinplot_tab'],
                           tooltip_directed=tooltips['directed'], tooltip_layout=tooltips['layout_dropdown'],
                           tooltip_dynamic=tooltips['dynamic'],
                           metricsType=metrics, session_id=filename2)

@node_routes.route('/node/pagerank', endpoint='node_pagerank', methods=['GET', 'POST'])
def node_pagerank():
    filename2 = session['filename2']
    metrics = 'pagerank'

    return render_template('metrics/nodes/node_pagerank.html', method_name='Node Page Rank',
                           description=description['node_pagerank'], tooltip_multi=tooltips['multi'],
                           tooltip_layout_tab=tooltips['layout_tab'], tooltip_histogram_tab=tooltips['histogram_tab'],
                           tooltip_boxplot_tab=tooltips['boxplot_tab'], tooltip_violinplot_tab=tooltips['violinplot_tab'],
                           tooltip_directed=tooltips['directed'], tooltip_layout=tooltips['layout_dropdown'],
                           tooltip_dynamic=tooltips['dynamic'],
                           metricsType=metrics, session_id=filename2)