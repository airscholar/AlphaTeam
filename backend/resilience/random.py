from flask import Blueprint, request
from flask_jsonpify import jsonify

from src.resilience import resilience
from src.utils import get_networkGraph, set_networkGraph
from src.visualisation import *

random_bp = Blueprint('resilience_random', __name__, url_prefix="/api/v1/resilience")


def extract_args():
    """
    :Function: Extract the arguments from the request
    :return: the arguments (number of nodes, number of edges)
    :rtype: tuple
    """
    args = request.args

    number_of_nodes = args.get('number_of_nodes', None, type=int)
    number_of_edges = args.get('number_of_edges', None, type=int)

    if number_of_nodes == '':
        number_of_nodes = None
    if number_of_edges == '':
        number_of_edges = None

    print(number_of_nodes, number_of_edges)

    return number_of_nodes, number_of_edges


@random_bp.route('<session_id>/random')
def compute_random(session_id):
    """
    :Function: Compute the random resilience for the network
    :param session_id: the session id
    :type session_id: str
    :return: the clusters
    :rtype: json
    """
    number_of_nodes, number_of_edges = extract_args()

    networkGraphs = get_networkGraph(session_id)

    networkGraphs2, df = resilience(networkGraphs, attack='random', number_of_edges=number_of_edges,
                                    number_of_nodes=number_of_nodes)

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
