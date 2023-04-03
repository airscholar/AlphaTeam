from flask import Blueprint, request
from flask_jsonpify import jsonify

from src.resilience import resilience
from src.utils import get_networkGraph, set_networkGraph
from src.visualisation import *
from backend.common.common import get_directed_toggle, get_multi_toggle, get_layout

custom_bp = Blueprint('resilience_custom', __name__, url_prefix="/api/v1/resilience")

def extract_args():
    args = request.args

    cluster_algorithm = args.get('cluster_algorithm') if (args.get('cluster_algorithm') or
                                                          not args.get('cluster_algorithm')=='') else None
    total_clusters = int(args.get('total_clusters')) if (args.get('total_clusters') or
                                                        not args.get('total_clusters')=='') else None
    cluster_ids = args.get('cluster_ids') if args.get('cluster_ids') else None
    list_of_nodes = args.get('list_of_nodes') if args.get('list_of_nodes') else None

    if list_of_nodes:
        list_of_nodes = list_of_nodes.split(',')
        try:
            list_of_nodes = [int(i) for i in list_of_nodes]
        except:
            list_of_nodes = [str(i) for i in list_of_nodes]

    if cluster_ids:
        cluster_ids = cluster_ids.split(',')
        try:
            cluster_ids = [int(i) for i in cluster_ids]
        except:
            cluster_ids = [str(i) for i in cluster_ids]

    return cluster_algorithm, total_clusters, cluster_ids, list_of_nodes

@custom_bp.route('<session_id>/custom')
def compute_custom(session_id):
    cluster_algorithm, total_clusters, cluster_ids, list_of_nodes = extract_args()

    networkGraphs = get_networkGraph(session_id)

    if list_of_nodes:
        networkGraphs2, df = resilience(networkGraphs, attack='custom', list_of_nodes=list_of_nodes)
    else:
        networkGraphs2, df = resilience(networkGraphs, attack='cluster_custom', cluster_algorithm=cluster_algorithm,
                                        total_clusters=total_clusters, cluster_ids=cluster_ids)


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

