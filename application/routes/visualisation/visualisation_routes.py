import sys

from application.dictionary.information import *
from flask import Blueprint, render_template, session
from flask import request
from backend.common.common import process_metric

sys.path.insert(1, '../../')
from src.metrics import *

visualisation_routes = Blueprint('visualisation_routes', __name__)

# -------------------------------------------VISUALISATION-----------------------------------

@visualisation_routes.route('/visualisation', methods=['GET', 'POST'], endpoint='visualisation')
def visualisation():
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)

    show_temporal = str(networkGraphs.is_temporal()).lower()

    if networkGraphs.is_spatial():
        is_spatial = 'yes'
    else:
        is_spatial = 'no'

    print('check spatial if yes means map, else sfdp', is_spatial)

    return render_template('visualisation/visualisation.html', show_temporal=show_temporal,
                           session_id=filename2, is_spatial=is_spatial,
                           #tooltips adding from here
                            tooltip_network_tab=tooltips['network_tab'], tooltip_temporal_tab=tooltips['temporal_tab'], tooltip_heatmap_tab=tooltips['heatmap_tab'],
                            tooltip_dynamic=tooltips['dynamic'], tooltip_layout_dropdown=tooltips['layout_dropdown'], description=description['visualisation'])
