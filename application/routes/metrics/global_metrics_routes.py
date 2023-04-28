import sys

from flask import Blueprint, render_template, session
from flask import request

from application.dictionary.information import *

sys.path.insert(1, '../../')
from src.metrics import *

global_metrics_routes = Blueprint('global_metrics_routes', __name__)


# -------------------------------------------GLOBAL-METRICS-----------------------------------
@global_metrics_routes.route('/global-metrics', methods=['GET', 'POST'])
def globalmetrics():
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    multi_toggle = False
    directed_toggle = False

    if request.method == 'POST':
        multi_toggle = bool(request.form.get('multi_toggle'))
        directed_toggle = bool(request.form.get('directed_toggle'))
        global_metrics = compute_global_metrics(networkGraphs, directed_toggle, multi_toggle)
    else:
        global_metrics = compute_global_metrics(networkGraphs, directed_toggle, multi_toggle)

    return render_template('metrics/global_metrics.html', example=global_metrics, multi_toggle=multi_toggle,
                           directed_toggle=directed_toggle,
                           tooltip_multi=tooltips['multi'], tooltip_directed=tooltips['directed'],
                           description=description['global_metrics'])
