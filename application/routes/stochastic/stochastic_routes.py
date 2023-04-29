import sys

from flask import Blueprint, render_template, session

from application.dictionary.information import *

sys.path.insert(1, '../../')
from src.metrics import *

stochastic_routes = Blueprint('stochastic_routes', __name__)

#--------------------------------------------------------------------------------------------------------------------------------------
@stochastic_routes.route('/stochastic/clustering_coefficient', methods=['GET', 'POST'], endpoint='clustering_coefficient')
def clustering_coefficient():
    """
    :Function: Stochastic Analysis of the network
    :return: the Clustering Coefficient page
    """
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)

    return render_template('stochastic/clustering_coefficient.html', session_id=filename2, 
                           tooltip_histogram_tab=tooltips['histogram_tab'], tooltip_boxplot_tab=tooltips['boxplot_tab'],
                           tooltip_violinplot_tab=tooltips['violinplot_tab'],
                           description=description['clustering_coefficient'])

@stochastic_routes.route('/stochastic/shortest_path', methods=['GET', 'POST'], endpoint='shortest_path')
def shortest_path():
    """
    :Function: Stochastic Analysis of the network
    :return: the Shortest Path page
    """
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)

    return render_template('stochastic/shortest_path.html', session_id=filename2, 
                           tooltip_histogram_tab=tooltips['histogram_tab'], tooltip_boxplot_tab=tooltips['boxplot_tab'],
                           tooltip_violinplot_tab=tooltips['violinplot_tab'],
                           description=description['shortest_path'])

