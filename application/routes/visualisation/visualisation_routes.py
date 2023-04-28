import sys

from flask import Blueprint, render_template, session

from application.dictionary.information import *

sys.path.insert(1, '../../')
from src.metrics import *

visualisation_routes = Blueprint('visualisation_routes', __name__)


# -------------------------------------------VISUALISATION-----------------------------------
@visualisation_routes.route('/visualisation', methods=['GET', 'POST'], endpoint='visualisation')
def visualisation():
    """
    :Function: Visualise the network
    :return: the visualisation page
    """
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)

    show_temporal = str(networkGraphs.is_temporal()).lower()

    if networkGraphs.is_spatial():
        is_spatial = 'yes'
    else:
        is_spatial = 'no'

    return render_template('visualisation/visualisation.html', show_temporal=show_temporal,
                           session_id=filename2, is_spatial=is_spatial,
                           tooltip_network_tab=tooltips['network_tab'], tooltip_temporal_tab=tooltips['temporal_tab'],
                           tooltip_heatmap_tab=tooltips['heatmap_tab'],
                           tooltip_dynamic=tooltips['dynamic'], tooltip_layout_dropdown=tooltips['layout_dropdown'],
                           description=description['visualisation'])
