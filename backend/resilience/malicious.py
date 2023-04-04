from flask import Blueprint, request
from flask_jsonpify import jsonify

from src.resilience import resilience
from src.utils import get_networkGraph, set_networkGraph
from src.visualisation import *
from backend.common.common import get_directed_toggle, get_multi_toggle, get_layout

malicious_bp = Blueprint('resilience_malicious', __name__, url_prefix="/api/v1/resilience")

def extract_args():
    args = request.args

    attack_type = args.get('attack_type')
    number_of_nodes_malicious = args.get('number_of_nodes_malicious')
    number_of_threshold = args.get('number_of_threshold')
    operator = args.get('operator')

    return attack_type, number_of_nodes_malicious, number_of_threshold, operator

@malicious_bp.route('<session_id>/malicious')
def compute_malicious(session_id):
    attack_type, number_of_nodes_malicious, number_of_threshold, operator = extract_args()

    networkGraphs = get_networkGraph(session_id)

    networkGraphs2, df = resilience(networkGraphs, attack='malicious', metric=attack_type,
                                    number_of_nodes=number_of_nodes_malicious, threshold=number_of_threshold,
                                    operator=operator)

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

