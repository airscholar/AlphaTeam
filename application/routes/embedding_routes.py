import sys

from dictionary.information import *
from flask import Blueprint, render_template, session
from routes.template_metrics import *

from backend.common.common import process_metric

sys.path.insert(1, '../')
from src.metrics import *

embedding_routes = Blueprint('embedding_routes', __name__)

#----------------------------------------------CLUSTER-EMBEDDING------------------------------------------------------------------
BASE_URL = 'http://localhost:8000/api/v1/deeplearning/'

def get_embedding_details(filename2, layout, p_value, q_value):
    url_query = f'?p={p_value}&q={q_value}&layout={layout}'

    json_data = requests.get(f'{BASE_URL}{filename2}/node_embedding' + url_query).json()

    df = pd.read_json(json_data['data'], orient='split')
    graph_name = json_data['filename']

    return df, graph_name

def compute_embedding(filename2):
    p_value = 1
    q_value = 1
    layout = 'TSNE'
    if request.method == 'POST':
        q_value = request.form.get('q_value',None)
        p_value = request.form.get('p_value',None)
        layout = request.form.get('layout')
        q_value = int(q_value) if q_value else 1
        p_value = int(p_value) if p_value else 1

    df, graph_name = get_embedding_details(filename2, layout, p_value, q_value)

    if graph_name == 'no_graph.html':
        graph_embedding_path = '../static/' + graph_name
    else:
        graph_embedding_path = graph_name

    return df, graph_embedding_path, p_value, q_value, layout

@embedding_routes.route('/embedding', endpoint='embedding',  methods=['GET', 'POST'])
def embedding_kmeans():
    filename2 = session['filename2']
    
    df, graph_embedding_path, p_value, q_value, layout = compute_embedding(filename2)

    return render_template('deep_learning/embedding.html', session_id=filename2, example=df,
                            graph_embedding=graph_embedding_path, p_value=p_value, q_value=q_value, layout=layout)

