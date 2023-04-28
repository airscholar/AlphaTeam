from flask import Blueprint, request, jsonify

from backend.common.common import get_arg_dynamic_toggle, get_arg_layout
from src.utils import get_networkGraph
from src.visualisation import plot_cluster

cluster_bp = Blueprint('clusters', __name__, url_prefix="/api/v1/clusters")


def get_arg_no_of_clusters(args):
    """
    :Function: Get the number of clusters from the request args
    :param args: number of clusters
    :type: int
    :return: number of clusters
    :rtype: int
    """
    no_of_clusters = args.get('no_of_clusters', 0, type=int)
    return no_of_clusters


@cluster_bp.route('/<session_id>/<clustering_alg>')
def compute_clustering(session_id, clustering_alg):
    """
    Compute the clustering for the network graph
    :param session_id: the session id
    :param clustering_alg: the clustering algorithm
    :return: the jsonified response
    """
    dynamic_toggle = get_arg_dynamic_toggle(request.args)
    layout = get_arg_layout(request.args)

    no_of_clusters = get_arg_no_of_clusters(request.args)

    G = get_networkGraph(session_id)

    df, filename = plot_cluster(G, clustering_alg, noOfClusters=no_of_clusters, dynamic=dynamic_toggle, layout=layout)

    df_json = df.to_json(orient='split')

    return jsonify({"message": "Success", "data": df_json, "filename": filename})
