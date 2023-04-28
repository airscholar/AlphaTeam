from flask import Blueprint, request
from flask_jsonpify import jsonify

from src.resilience import resilience
from src.utils import get_networkGraph, set_networkGraph
from src.visualisation import *

custom_bp = Blueprint('resilience_custom', __name__, url_prefix="/api/v1/resilience")


def get_args_listOfNodes():
    """
    :Function: Extract the list of nodes from the request
    :return: the list of nodes (list_of_nodes)
    :rtype: list
    """
    args = request.args
    list_of_nodes = args.get('list_of_nodes')

    if list_of_nodes:
        list_of_nodes = list_of_nodes.split(',')
        try:
            list_of_nodes = [int(i) for i in list_of_nodes]
        except:
            list_of_nodes = [str(i) for i in list_of_nodes]

    return list_of_nodes


@custom_bp.route('<session_id>/custom')
def compute_custom(session_id):
    """
    :Function: Compute the custom resilience of the network
    :param session_id: the session id
    :type session_id: str
    :return: the custom resilience of the network
    :rtype: json
    """
    list_of_nodes = get_args_listOfNodes()

    networkGraphs = get_networkGraph(session_id)

    networkGraphs2, df = resilience(networkGraphs, attack='custom', list_of_nodes=list_of_nodes)

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
