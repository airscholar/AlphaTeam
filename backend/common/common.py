import pandas as pd
import requests
from flask import request

BASE_URL = 'http://localhost:8000/api/v1/metrics/'


def get_arg_multi_toggle(args):
    """
    :Function: Get the multi toggle from the request args
    :param args: the request args (such as multi_toggle, multi)
    :type args: dict
    :return: boolean value of the multi toggle or multi
    :rtype: bool
    """
    if 'multi_toggle' in args:
        multi_toggle = args.get('multi_toggle', 'false')
    elif 'multi' in args:
        multi_toggle = args.get('multi', 'false')
    else:
        raise ValueError('multi_toggle or multi not found in args')
    return True if multi_toggle in ['true', 'True', True] else False


def get_arg_directed_toggle(args):
    """
    :Function: Get the directed toggle from the request args
    :param args: the request args (such as directed_toggle, directed)
    :type args: dict
    :return: boolean value of the directed toggle or directed
    :rtype: bool
    """
    if 'directed_toggle' in args:
        directed_toggle = args.get('directed_toggle', 'false')
    elif 'directed' in args:
        directed_toggle = args.get('directed', 'false')
    else:
        raise ValueError('directed_toggle or directed not found in args')
    return True if directed_toggle in ['true', 'True', True] else False


def get_arg_dynamic_toggle(args):
    """
    :Function: Get the dynamic toggle from the request args
    :param args: the request args (such as dynamic_toggle, dynamic)
    :type args: dict
    :return: boolean value of the dynamic toggle or dynamic
    :rtype: bool
    """
    dynamic_toggle = args.get('dynamic', 'false')
    dynamic_toggle = True if dynamic_toggle in ['true', 'True', True] else False
    return dynamic_toggle


def get_arg_layout(args):
    """
    :Function: Get the layout from the request args
    :param args: the layout argument (default is sfdp)
    :type args: dict
    :return: the layout
    :rtype: str
    """
    layout = args.get('layout', 'sfdp')
    return layout


def extract_args(args):
    """
    :Function: Extract the arguments from the request args
    :param args: the request args
    :type args: dict
    :return: the multi toggle, directed toggle, dynamic toggle, and layout
    :rtype: tuple
    """
    multi_toggle = get_arg_multi_toggle(args)
    directed_toggle = get_arg_directed_toggle(args)
    dynamic_toggle = get_arg_dynamic_toggle(args)
    layout = get_arg_layout(args)

    return directed_toggle, multi_toggle, dynamic_toggle, layout


def process_metric(networkGraphs, filename2, metrics):
    """
    :Function: Process the network graph and metrics
    :param networkGraphs: the network graph
    :type networkGraphs: NetworkGraphs
    :param filename2: the session id
    :type filename2: str
    :param metrics: the metrics
    :type metrics: list
    :return: the processed metrics
    :rtype: tuple
    """
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
