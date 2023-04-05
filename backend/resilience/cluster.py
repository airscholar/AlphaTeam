from flask import Blueprint, request
from flask_jsonpify import jsonify

from src.resilience import resilience
from src.utils import get_networkGraph, set_networkGraph
from src.visualisation import *

clusters_bp = Blueprint('resilience_clusters', __name__, url_prefix="/api/v1/resilience")

def extract_args():
    args = request.args

    cluster_algorithm = args.get('cluster_algorithm')
    total_clusters = int(args.get('total_clusters'))
    number_of_clusters = int(args.get('number_of_clusters'))

    return cluster_algorithm, total_clusters, number_of_clusters

@clusters_bp.route('<session_id>/clusters')
def compute_clusters(session_id):
    cluster_algorithm, total_clusters, number_of_clusters = extract_args()

    networkGraphs = get_networkGraph(session_id)

    networkGraphs2, df = resilience(networkGraphs, attack='cluster', cluster_algorithm=cluster_algorithm,
                                    total_clusters=total_clusters, number_of_clusters=number_of_clusters)

    session_id2 = session_id + '_resilience'
    set_networkGraph(networkGraphs2, session_id2)

    layout = "map" if networkGraphs.is_spatial() else "sfdp"

    before = plot_network(networkGraphs, layout=layout, dynamic=False, fullPath=True)
    after = plot_network(networkGraphs2, layout=layout, dynamic=False, fullPath=True)
    heatmap_before = plot_heatmap(networkGraphs, fullPath=True)
    heatmap_after = plot_heatmap(networkGraphs2, fullPath=True)

    df_json = df.to_json(orient='split')

    return jsonify({"message": "Success", "data": df_json, "network_before": before, "network_after": after,
                    "heatmap_before": heatmap_before, "heatmap_after": heatmap_after})

