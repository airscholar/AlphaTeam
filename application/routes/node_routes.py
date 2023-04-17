import sys

from application.dictionary.information import *
from flask import Blueprint, render_template, session
from application.routes.template_metrics import *

from application.routes.template_metrics import process_single_metric
from backend.common.common import process_metric

sys.path.insert(1, '../')
from src.metrics import *

node_routes = Blueprint('node_routes', __name__)


# -------------------------------------------NODE--------------------------------------------

@node_routes.route('/node_all', endpoint='node_all', methods=['GET', 'POST'])
def node_all():
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)

    metrics = 'nodes'

    graph_names, graph_paths, df, tab, layout, multi_toggles, directed_toggles = process_metric(networkGraphs,
                                                                                                filename2, metrics)

    return render_template('nodes/node_all.html', example=df, tab=tab, method_name='All Nodes',
                           description=description['node_all'],
                           multi_toggle=multi_toggles[0], directed_toggle=directed_toggles[0], layout=layout,
                           graph1=graph_paths[0],
                           multi_toggle2=multi_toggles[1], directed_toggle2=directed_toggles[1], layout2=layout,
                           graph2=graph_paths[1],
                           multi_toggle3=multi_toggles[2], directed_toggle3=directed_toggles[2], layout3=layout,
                           graph3=graph_paths[2],
                           multi_toggle4=multi_toggles[3], directed_toggle4=directed_toggles[3], layout4=layout,
                           graph4=graph_paths[3])


@node_routes.route('/node/degree', endpoint='node_degree', methods=['GET', 'POST'])
def node_degree():
    return process_single_metric('degree', 'nodes/node_degree.html', 'Node Degree', 'node_degree')


@node_routes.route('/node/kcore', endpoint='node_kcore', methods=['GET', 'POST'])
def node_kcore():
    return process_single_metric('kcore', 'nodes/node_kcore.html', 'Node K Core', 'node_kcore')


@node_routes.route('/node/triangle', endpoint='node_triangle', methods=['GET', 'POST'])
def node_triangle():
    return process_single_metric('triangles', 'nodes/node_triangle.html', 'Node Triangle', 'node_triangle')


@node_routes.route('/node/pagerank', endpoint='node_pagerank', methods=['GET', 'POST'])
def node_pagerank():
    return process_single_metric('pagerank', 'nodes/node_pagerank.html', 'Node Page Rank', 'node_pagerank')
