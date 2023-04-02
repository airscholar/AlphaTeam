from flask import Blueprint, request
from flask_jsonpify import jsonify

from backend.common.common import extract_args
from src.utils import get_networkGraph
from src.visualisation import *

visualisation_bp = Blueprint('visualisation', __name__, url_prefix="/api/v1/visualisation")


@visualisation_bp.route('<session_id>/plot_network/<plot_type>')
def visualise_network(session_id, plot_type):
    _, _, dynamic_toggle, layout = extract_args(request.args)

    G = get_networkGraph(session_id)

    file_name = None

    if plot_type == 'spatial':
        file_name = plot_network(G, layout=layout, dynamic=dynamic_toggle)
    elif plot_type == 'temporal':
        file_name = plot_temporal(G, layout=layout)

    return jsonify({"message": "Success", "file": file_name})
