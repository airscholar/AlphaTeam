import sys

from flask import Blueprint, render_template, session
import requests
from application.dictionary.information import *
from flask import Blueprint, render_template, session, request

sys.path.insert(1, '../../')
from src.metrics import *

embedding_routes = Blueprint('embedding_routes', __name__)

# ----------------------------------------------CLUSTER-EMBEDDING------------------------------------------------------------------
BASE_URL = 'http://localhost:8000/api/v1/deeplearning/'


@embedding_routes.route('/node2vec/embedding', endpoint='node2vec_embedding', methods=['GET', 'POST'])
def embedding_visualisation():
    filename2 = session['filename2']

    return render_template('deepLearning/node2vec/embedding.html', session_id=filename2,
    
    description=description['node2vec_embedding'], tooltip_parameters=tooltips['parameters'], 
    tooltip_layout=tooltips['layout_dropdown'])

@embedding_routes.route('/dlembedding/embedding', endpoint='dlembedding_embedding', methods=['GET', 'POST'])
def dlembedding_embedding_visualisation():
    filename2 = session['filename2']

    return render_template('deepLearning/dlembedding/embedding.html', session_id=filename2,
    description=description['dlembedding_embedding'], tooltip_dimension=tooltips['dimension'], 
    tooltip_model_dropdown=tooltips['model_dropdown'], tooltip_layout=tooltips['layout_dropdown'], 
    tooltip_features=tooltips['features_checkbox'])
