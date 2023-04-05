from flask import Blueprint, request, jsonify

from backend.common.common import get_arg_dynamic_toggle, get_arg_layout
from src.utils import get_networkGraph
from src.visualisation import plot_cluster

cluster_bp = Blueprint('clusters', __name__, url_prefix="/api/v1/clusters")


@cluster_bp.route('/<session_id>/<clustering_alg>')
def compute_clustering(session_id, clustering_alg):
    dynamic_toggle = get_arg_dynamic_toggle(request.args)
    layout = get_arg_layout(request.args)

    no_of_clusters = request.args.get('no_of_clusters', default=0, type=int)

    G = get_networkGraph(session_id)

    df, filename = plot_cluster(G, clustering_alg, noOfClusters=no_of_clusters, dynamic=dynamic_toggle, layout=layout)

    df_json = df.to_json(orient='split')

    return jsonify({"message": "Success", "data": df_json, "file": filename})
