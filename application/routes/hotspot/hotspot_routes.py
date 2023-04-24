import sys

import requests
from application.dictionary.information import *
from flask import Blueprint, render_template, session, request

sys.path.insert(1, '../../')
from src.metrics import *

hotspot_routes = Blueprint('hotspot_routes', __name__)

# -------------------------------------------HOTSPOT-----------------------------------------

@hotspot_routes.route('/hotspot/density', endpoint='hotspot_density', methods=['GET', 'POST'])
def hotspot_density():
    filename2 = session['filename2']
    hotspotType = 'density'

    return render_template('hotspot/hotspot_density.html', session_id=filename2, hotspotType=hotspotType, method_name='Density')
