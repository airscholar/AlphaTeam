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

    return jsonify({"message": "Success", "file": file_name})


@visualisation_bp.route('<session_id>/heatmap')
def visualise_heatmap(session_id):
    G = get_networkGraph(session_id)

    file_name = plot_heatmap(G)

    return jsonify({"message": "Success", "file": file_name})


@visualisation_bp.route('/<session_id>/dataset')
def visualise_dataset(session_id):
    G = get_networkGraph(session_id)

    df = G.df.head(100).to_json()

    total_filtered = 10

    # sorting
    order = []
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        descending = request.args.get(f'order[{i}][dir]') == 'desc'

        i += 1

    # Set the pagination configuration
    page = request.args.get('page', 1, type=int)
    start = request.args.get('start', 1, type=int)
    length = request.args.get('length', 5, type=int)
    pagination = User.objects.paginate(page=start, per_page=length)
    data = {
        'data': [user.to_dict() for user in pagination.items],
        'recordsFiltered': 10,
        'recordsTotal': 100,
        'draw': 1
    }
    return data

    return df
