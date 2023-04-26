from flask import Blueprint, request
from flask_jsonpify import jsonify

from backend.common.common import get_arg_dynamic_toggle, get_arg_layout
from src.utils import get_networkGraph
from src.visualisation import *

visualisation_bp = Blueprint('visualisation', __name__, url_prefix="/api/v1/visualisation")


@visualisation_bp.route('<session_id>/plot_network/<plot_type>')
def visualise_network(session_id, plot_type):
    dynamic_toggle = get_arg_dynamic_toggle(request.args)
    layout = get_arg_layout(request.args)

    G = get_networkGraph(session_id)

    file_name = None

    if plot_type == 'spatial':
        file_name = plot_network(G, layout=layout, dynamic=dynamic_toggle)
    elif plot_type == 'temporal':
        file_name = plot_temporal(G, layout=layout)

    return jsonify({"message": "Success", "filename": file_name})


@visualisation_bp.route('<session_id>/heatmap')
def visualise_heatmap(session_id):
    G = get_networkGraph(session_id)

    file_name = plot_heatmap(G)

    return jsonify({"message": "Success", "filename": file_name})


@visualisation_bp.route('/<session_id>/dataset')
def visualise_dataset(session_id):
    G = get_networkGraph(session_id)

    df = G.df.head(3000).to_json(orient='split')

    return jsonify({"message": "Success", "data": df})
