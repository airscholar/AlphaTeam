import sys

import requests
from application.dictionary.information import *
from flask import render_template, session, request

sys.path.insert(1, '../')
from src.metrics import *
from src.preprocessing import *
from src.visualisation import *

BASE_URL = 'http://localhost:8000/api/v1/metrics/'


def process_single_metric(metrics_arg, template_name_arg, method_name_arg, description_key_arg):
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    metrics = metrics_arg
    multi_toggle = False
    dynamic_toggle = False
    directed_toggle = True
    tab = 'tab1'

    layout = 'map' if networkGraphs.is_spatial() else 'sfdp'

    if request.method == 'POST':
        multi_toggle = bool(request.form.get('multi_toggle'))
        dynamic_toggle = bool(request.form.get('dynamic_toggle'))
        directed_toggle = bool(request.form.get('directed_toggle'))
        layout = request.form.get('layout')

    url_query = f'?directed={directed_toggle}&multi={multi_toggle}&dynamic={dynamic_toggle}'

    json_data = requests.get(f'{BASE_URL}{filename2}/{metrics}' + url_query + '&layout=' + layout).json()
    df = pd.read_json(json_data['data'], orient='split')
    graph_name1 = json_data['file']

    session['graph_name1'] = graph_name1

    json_data = requests.get(f'{BASE_URL}{filename2}/{metrics}/histogram' + url_query).json()
    graph_name2 = json_data['file']

    json_data = requests.get(f'{BASE_URL}{filename2}/{metrics}/boxplot' + url_query).json()
    graph_name3 = json_data['file']

    json_data = requests.get(f'{BASE_URL}{filename2}/{metrics}/violin' + url_query).json()
    graph_name4 = json_data['file']

    graph_names = [graph_name1, graph_name2, graph_name3, graph_name4]
    graph_paths = [
        '../static/uploads/' + filename2 + '/' + graph_name if graph_name != 'no_graph.html'
        else '../static/no_graph.html'
        for graph_name in graph_names]

    return render_template(template_name_arg, example=df, tab=tab, method_name=method_name_arg,
                           description=description[description_key_arg],
                           multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle,
                           layout=layout, graph1=graph_paths[0], graph2=graph_paths[1], graph3=graph_paths[2],
                           graph4=graph_paths[3])
