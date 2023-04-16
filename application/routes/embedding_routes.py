import sys

import requests
from application.dictionary.information import *
from flask import Blueprint, render_template, session, request
from application.routes.template_metrics import *

sys.path.insert(1, '../')
from src.metrics import *

embedding_routes = Blueprint('embedding_routes', __name__)

# ----------------------------------------------CLUSTER-EMBEDDING------------------------------------------------------------------
BASE_URL = 'http://localhost:8000/api/v1/deeplearning/'


@embedding_routes.route('/embedding', endpoint='embedding', methods=['GET', 'POST'])
def embedding_visualisation():
    filename2 = session['filename2']

    return render_template('deep_learning/embedding.html', session_id=filename2)
