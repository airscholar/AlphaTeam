from flask import Blueprint, request
from flask_jsonpify import jsonify

from src.utils import get_networkGraph
from src.visualisation import *

metrics_bp = Blueprint('metrics', __name__, url_prefix="/api/v1/metrics")


def extract_args(args):
    directed_toggle = args.get('directed', 'false')
    directed_toggle = True if directed_toggle in ['true', 'True'] else False
    multi_toggle = args.get('multi', 'false')
    multi_toggle = True if multi_toggle in ['true', 'True'] else False
    dynamic_toggle = args.get('dynamic', 'false')
    dynamic_toggle = True if dynamic_toggle in ['true', 'True'] else False
    layout = args.get('layout', 'sfdp')

    return directed_toggle, multi_toggle, dynamic_toggle, layout

@metrics_bp.route('<session_id>/<metric>/all')
def compute_all_metrics(session_id, metric):
    directed_toggle, multi_toggle, dynamic_toggle, layout = extract_args(request.args)

    G = get_networkGraph(session_id)

    dataframe, file_name = plot_all_metrics(G, metric, directed=directed_toggle, multi=multi_toggle, layout=layout)
    df_json = dataframe.to_json(orient='split')

    return jsonify({"message": "Success", "data": df_json, "file": file_name})

@metrics_bp.route('<session_id>/<metric>')
def compute_metrics(session_id, metric):
    directed_toggle, multi_toggle, dynamic_toggle, layout = extract_args(request.args)

    G = get_networkGraph(session_id)

    dataframe, file_name = plot_metric(G, metric, directed=directed_toggle, multi=multi_toggle, dynamic=dynamic_toggle,
                                       layout=layout)
    df_json = dataframe.to_json(orient='split')

    return jsonify({"message": "Success", "data": df_json, "file": file_name})


@metrics_bp.route('<session_id>/<metric>/<plot_type>')
def plot_graph(session_id, metric, plot_type):
    directed_toggle, multi_toggle, dynamic_toggle, layout = extract_args(request.args)

    G = get_networkGraph(session_id)

    dataframe = None
    file_name = None

    if plot_type == 'histogram':
        dataframe, file_name = plot_histogram(G, metric, directed=directed_toggle, multi=multi_toggle)
    elif plot_type == 'boxplot':
        dataframe, file_name = plot_boxplot(G, metric, directed=directed_toggle, multi=multi_toggle)
    elif plot_type == 'violin':
        dataframe, file_name = plot_violin(G, metric, directed=directed_toggle, multi=multi_toggle)

    df_json = dataframe.to_json(orient='split')

    data = {"message": "Success", "data": df_json, "file": file_name}

    return jsonify(data)