import sys

from flask import Blueprint, render_template, session

from application.dictionary.information import *

sys.path.insert(1, '../../')

hotspot_routes = Blueprint('hotspot_routes', __name__)


# -------------------------------------------HOTSPOT-----------------------------------------

@hotspot_routes.route('/hotspot/density', endpoint='hotspot_density', methods=['GET', 'POST'])
def hotspot_density():
    """
    :Function: Visualise the hotspot using density
    :return: the hotspot page
    """
    filename2 = session['filename2']
    hotspotType = 'density'

    return render_template('hotspot/hotspot_density.html', session_id=filename2, hotspotType=hotspotType,
                           method_name='Density',
                           description=description['hotspot_density'])
