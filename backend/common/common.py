import pandas as pd
import requests
from flask import request

BASE_URL = 'http://localhost:8000/api/v1/metrics/'

def get_multi_toggle(args):
    multi_toggle = args.get('multi', 'false')
    multi_toggle = True if multi_toggle in ['true', 'True'] else False
    return multi_toggle

def get_directed_toggle(args):
    directed_toggle = args.get('directed', 'false')
    directed_toggle = True if directed_toggle in ['true', 'True'] else False
    return directed_toggle

def get_dynamic_toggle(args):
    dynamic_toggle = args.get('dynamic', 'false')
    dynamic_toggle = True if dynamic_toggle in ['true', 'True'] else False
    return dynamic_toggle

def get_layout(args):
    layout = args.get('layout', 'sfdp')
    return layout

def extract_args(args):
    multi_toggle = get_multi_toggle(args)
    directed_toggle = get_directed_toggle(args)
    dynamic_toggle = get_dynamic_toggle(args)
    layout = get_layout(args)

    return directed_toggle, multi_toggle, dynamic_toggle, layout


def process_metric(networkGraphs, filename2, metrics):
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
    multi_toggles = [multi_toggle, multi_toggle2, multi_toggle3, multi_toggle4]
    directed_toggles = [directed_toggle, directed_toggle2, directed_toggle3, directed_toggle4]

    return graph_names, graph_paths, df, tab, layout, multi_toggles, directed_toggles
