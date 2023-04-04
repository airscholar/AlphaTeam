from flask import Blueprint, request
from flask_jsonpify import jsonify

from src.metrics import compute_global_metrics
from src.resilience import resilience
from src.utils import get_networkGraph, set_networkGraph
from src.visualisation import *
from backend.common.common import *

resilience_bp = Blueprint('resilience', __name__, url_prefix="/api/v1/resilience")


@resilience_bp.route('<session_id>/<metric>/<plot_type>/')
def compute_metrics(session_id, metric, plot_type):
    directed_toggle = get_directed_toggle(request.args)
    multi_toggle = get_multi_toggle(request.args)
    layout = get_layout(request.args)

    networkGraphs = get_networkGraph(session_id)
    networkGraphs2 = get_networkGraph(session_id + '_resilience')

    df = None
    df1 = None
    file_name = None
    file_name1 = None

    if plot_type == 'layout':
        df, file_name = plot_metric(networkGraphs, metric, directed=directed_toggle, multi=multi_toggle,
                                    layout=layout, fullPath=True)
        df1, file_name1 = plot_metric(networkGraphs2, metric, directed=directed_toggle, multi=multi_toggle,
                                      layout=layout, fullPath=True)
    elif plot_type == 'histogram':
        df, file_name = plot_histogram(networkGraphs, metric, directed=directed_toggle, multi=multi_toggle, fullPath=True)
        df1, file_name1 = plot_histogram(networkGraphs2, metric, directed=directed_toggle, multi=multi_toggle, fullPath=True)
    elif plot_type == 'boxplot':
        df, file_name = plot_boxplot(networkGraphs, metric, directed=directed_toggle, multi=multi_toggle, fullPath=True)
        df1, file_name1 = plot_boxplot(networkGraphs2, metric, directed=directed_toggle, multi=multi_toggle, fullPath=True)
    elif plot_type == 'violin':
        df, file_name = plot_violin(networkGraphs, metric, directed=directed_toggle, multi=multi_toggle, fullPath=True)
        df1, file_name1 = plot_violin(networkGraphs2, metric, directed=directed_toggle, multi=multi_toggle, fullPath=True)

    df_json = df.to_json(orient='split')
    df_json1 = df1.to_json(orient='split')
    return jsonify({"message": "Success", "data_before": df_json, "data_after": df_json1, "network_before": file_name,
                    "network_after": file_name1})


@resilience_bp.route('<session_id>/<cluster_type>')
def compute_cluster(session_id, cluster_type):
    layout = get_layout(request.args)
    noOfClusters = request.args.get('noOfClusters', 0)

    networkGraphs = get_networkGraph(session_id)
    networkGraphs2 = get_networkGraph(session_id + '_resilience')

    df, file_name = plot_cluster(networkGraphs, cluster_type, noOfClusters=noOfClusters, dynamic=False, layout=layout,
                                 fullPath=True)
    df1, file_name1 = plot_cluster(networkGraphs2, cluster_type, noOfClusters=noOfClusters, dynamic=False,
                                   layout=layout, fullPath=True)

    df_json = df.to_json(orient='split')
    df_json1 = df1.to_json(orient='split')
    return jsonify({"message": "Success", "data_before": df_json, "data_after": df_json1, "network_before": file_name,
                    "network_after": file_name1})


@resilience_bp.route('<session_id>/global_metrics')
def global_metrics(session_id):
    directed_toggle = get_directed_toggle(request.args)
    multi_toggle = get_multi_toggle(request.args)

    networkGraphs = get_networkGraph(session_id)
    networkGraphs2 = get_networkGraph(session_id + '_resilience')

    df1 = compute_global_metrics(networkGraphs, directed=directed_toggle, multi=multi_toggle)
    df2 = compute_global_metrics(networkGraphs2, directed=directed_toggle, multi=multi_toggle)

    df_json = df1.to_json(orient='split')
    df_json1 = df2.to_json(orient='split')

    return jsonify({"message": "Success", "data_before": df_json, "data_after": df_json1})


@resilience_bp.route('<session_id>/visualisation')
def visualisation(session_id):
    layout = get_layout(request.args)

    networkGraphs = get_networkGraph(session_id)
    networkGraphs2 = get_networkGraph(session_id + '_resilience')

    file_name1 = plot_network(networkGraphs, fullPath=True, layout=layout)
    file_name2 = plot_network(networkGraphs2, fullPath=True, layout=layout)

    return jsonify({"message": "Success", "before_frame": file_name1, "after_frame": file_name2})