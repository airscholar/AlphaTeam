import sys

from dictionary.information import *
from flask import Blueprint, render_template, session, request
from routes.template_metrics import *

sys.path.insert(1, '../')
from src.metrics import *
from src.preprocessing import *
import requests

node_routes = Blueprint('node_routes', __name__)

# -------------------------------------------NODE--------------------------------------------
BASE_URL = 'http://localhost:8000/api/v1/metrics/'


@node_routes.route('/node_all', endpoint='node_all', methods=['GET', 'POST'])
def node_all():
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)

    metrics = 'nodes'
    multi_toggle = None
    multi_toggle2 = None
    multi_toggle3 = None
    multi_toggle4 = None

    directed_toggle = None
    directed_toggle2 = None
    directed_toggle3 = None
    directed_toggle4 = None
    tab = 'tab1'

    layout = 'map' if networkGraphs.is_spatial() else 'sfdp'

    if request.method == 'POST':
        if request.form.get('multi_toggle') is not None and request.form.get('directed_toggle') is not None \
                and request.form.get('layout') is not None:
            multi_toggle = bool(request.form.get('multi_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
            tab = 'tab1'

        if request.form.get('multi_toggle2') is not None and request.form.get('directed_toggle2') is not None:
            multi_toggle2 = bool(request.form.get('multi_toggle2'))
            directed_toggle2 = bool(request.form.get('directed_toggle2'))
            tab = 'tab2'

        if request.form.get('multi_toggle3') is not None and request.form.get('directed_toggle3') is not None:
            multi_toggle3 = bool(request.form.get('multi_toggle3'))
            directed_toggle3 = bool(request.form.get('directed_toggle3'))
            tab = 'tab3'

        if request.form.get('multi_toggle4') is not None and request.form.get('directed_toggle4') is not None:
            multi_toggle4 = bool(request.form.get('multi_toggle4'))
            directed_toggle4 = bool(request.form.get('directed_toggle4'))
            tab = 'tab4'
    else:
        multi_toggle = True
        multi_toggle2 = True
        multi_toggle3 = True
        multi_toggle4 = True

        directed_toggle = False
        directed_toggle2 = False
        directed_toggle3 = False
        directed_toggle4 = False

    url_query = f'?directed={directed_toggle}&multi={multi_toggle}'
    json_data = requests.get(f'{BASE_URL}{filename2}/{metrics}/all' + url_query).json()
    df = pd.read_json(json_data['data'], orient='split')
    graph_name1 = json_data['file']

    url_query = f'?directed={directed_toggle2}&multi={multi_toggle2}'
    json_data = requests.get(f'{BASE_URL}{filename2}/{metrics}/histogram' + url_query).json()
    graph_name2 = json_data['file']

    url_query = f'?directed={directed_toggle3}&multi={multi_toggle3}'
    json_data = requests.get(f'{BASE_URL}{filename2}/{metrics}/boxplot' + url_query).json()
    graph_name3 = json_data['file']

    url_query = f'?directed={directed_toggle4}&multi={multi_toggle4}'
    json_data = requests.get(f'{BASE_URL}{filename2}/{metrics}/violin' + url_query).json()
    graph_name4 = json_data['file']

    graph_names = [graph_name1, graph_name2, graph_name3, graph_name4]
    graph_paths = [
        '../static/uploads/' + filename2 + '/' + graph_name if graph_name != 'no_graph.html'
        else '../static/no_graph.html'
        for graph_name in graph_names]

    return render_template('nodes/node_all.html', example=df, tab=tab, method_name='All Nodes',
                           description=description['node_all'],
                           multi_toggle=multi_toggle, directed_toggle=directed_toggle, layout=layout,
                           graph1=graph_paths[0],
                           multi_toggle2=multi_toggle2, directed_toggle2=directed_toggle2, layout2=layout,
                           graph2=graph_paths[1],
                           multi_toggle3=multi_toggle3, directed_toggle3=directed_toggle3, layout3=layout,
                           graph3=graph_paths[2],
                           multi_toggle4=multi_toggle4, directed_toggle4=directed_toggle4, layout4=layout,
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
