import sys

from application.dictionary.information import *
from flask import Blueprint, render_template, session
from application.routes.template_metrics import *

from application.routes.template_metrics import process_single_metric
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
                           description=description['node_all'],tooltip_multi=tooltips['multi'],
                           metricsType=metrics, session_id=filename2)

@node_routes.route('/node/degree', endpoint='node_degree', methods=['GET', 'POST'])
def node_degree():
    return process_single_metric('degree', 'metrics/nodes/node_degree.html', 'Node Degree', 'node_degree')


@node_routes.route('/node/kcore', endpoint='node_kcore', methods=['GET', 'POST'])
def node_kcore():
    return process_single_metric('kcore', 'metrics/nodes/node_kcore.html', 'Node K Core', 'node_kcore')


@node_routes.route('/node/triangle', endpoint='node_triangle', methods=['GET', 'POST'])
def node_triangle():
    return process_single_metric('triangles', 'metrics/nodes/node_triangle.html', 'Node Triangle', 'node_triangle')


@node_routes.route('/node/pagerank', endpoint='node_pagerank', methods=['GET', 'POST'])
def node_pagerank():
    return process_single_metric('pagerank', 'metrics/nodes/node_pagerank.html', 'Node Page Rank', 'node_pagerank')
