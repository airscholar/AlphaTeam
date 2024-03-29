from flask import Blueprint, request
from flask_jsonpify import jsonify

from backend.common.common import extract_args
from src.utils import get_networkGraph
from src.visualisation import *

metrics_bp = Blueprint('metrics', __name__, url_prefix="/api/v1/metrics")


@metrics_bp.route('<session_id>/<metric>/all')
def compute_all_metrics(session_id, metric):
    """
    :Function: Compute all metrics for the network
    :param session_id: the session id
    :type session_id: str
    :param metric: the metric to compute
    :type metric: str
    :return: the metric values
    :rtype: json
    """
    directed_toggle, multi_toggle, dynamic_toggle, layout = extract_args(request.args)

    G = get_networkGraph(session_id)

    dataframe, file_name = plot_all_metrics(G, metric, directed=directed_toggle, multi=multi_toggle, layout=layout)
    df_json = dataframe.to_json(orient='split')

    return jsonify({"message": "Success", "data": df_json, "filename": file_name})


@metrics_bp.route('<session_id>/<metric>')
def compute_metrics(session_id, metric):
    """
    :Function: Compute the metric for the network
    :param session_id: the session id
    :type session_id: str
    :param metric: the metric to compute
    :type session_id: str
    :return: the metric values
    :rtype: json
    """
    directed_toggle, multi_toggle, dynamic_toggle, layout = extract_args(request.args)

    G = get_networkGraph(session_id)

    dataframe, file_name = plot_metric(G, metric, directed=directed_toggle, multi=multi_toggle, dynamic=dynamic_toggle,
                                       layout=layout)
    df_json = dataframe.to_json(orient='split')

    return jsonify({"message": "Success", "data": df_json, "filename": file_name})


@metrics_bp.route('<session_id>/<metric>/<plot_type>')
def plot_graph(session_id, metric, plot_type):
    """
    :Function: Plot the graph for the metric
    :param session_id: the session id
    :type session_id: str
    :param metric: the metric to compute
    :type metric: str
    :param plot_type: the type of plot
    :type plot_type: str
    :return: jsonified response
    :rtype: json
    """
    if metric in ['shortest_path', 'clustering_coefficient']:
        directed_toggle = False
        multi_toggle = False
    else:
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

    data = {"message": "Success", "data": df_json, "filename": file_name}

    return jsonify(data)
