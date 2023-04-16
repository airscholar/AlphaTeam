import sys

from application.dictionary.information import *
from flask import Blueprint, render_template, session
from application.routes.template_metrics import *

from backend.common.common import process_metric

sys.path.insert(1, '../')
from src.metrics import *

cluster_embedding_routes = Blueprint('cluster_embedding_routes', __name__)


#----------------------------------------------CLUSTER-EMBEDDING------------------------------------------------------------------
BASE_URL = 'http://localhost:8000/api/v1/deeplearning/'

def get_embedding_cluster_details(filename2, layout, p_value, q_value, clustering_alg, number_of_clusters):
    url_query = f'?p={p_value}&q={q_value}&layout={layout}&cluster_algorithm={clustering_alg}&number_of_clusters={number_of_clusters}'

    json_data = requests.get(f'{BASE_URL}{filename2}/embedding_clustering' + url_query).json()

    df = pd.read_json(json_data['data'], orient='split')
    graph_name = json_data['filename']

    return df, graph_name

def compute_embedding_cluster(filename2, clustering_alg):
    p_value = 1
    q_value = 1
    layout = 'TSNE'
    number_of_clusters = 8
    if request.method == 'POST': 
        q_value = request.form.get('q_value',None)
        p_value = request.form.get('p_value',None)
        number_of_clusters = request.form.get('number_of_clusters',None)
        layout = request.form.get('layout')
        q_value = int(q_value) if q_value else 1
        p_value = int(p_value) if p_value else 1
        number_of_clusters = int(number_of_clusters) if p_value else 8

    df, graph_name = get_embedding_cluster_details(filename2, layout, p_value, q_value, clustering_alg, number_of_clusters)

    if graph_name == 'no_graph.html':
        graph_embedding_cluster_path = '../static/' + graph_name
    else:
        graph_embedding_cluster_path = '../' + graph_name

    return df, graph_embedding_cluster_path, p_value, q_value, number_of_clusters, layout

@cluster_embedding_routes.route('/clustering/embedding/kmeans', endpoint='clustering_embedding_kmeans',  methods=['GET', 'POST'])
def clustering_embedding_kmeans():
    filename2 = session['filename2']
    clustering_alg = 'kmeans'

    return render_template('deep_learning/cluster/kmeans.html', session_id=filename2, clustering_alg=clustering_alg)

@cluster_embedding_routes.route('/clustering/embedding/spectral', endpoint='clustering_embedding_spectral',  methods=['GET', 'POST'])
def clustering_embedding_spectral():
    filename2 = session['filename2']
    clustering_alg = 'spectral'

    return render_template('deep_learning/cluster/spectral.html', session_id=filename2, clustering_alg=clustering_alg)


@cluster_embedding_routes.route('/clustering/embedding/agglomerative', endpoint='clustering_embedding_agglomerative',  methods=['GET', 'POST'])
def clustering_embedding_agglomerative():
    filename2 = session['filename2']
    clustering_alg = 'agglomerative'

    return render_template('deep_learning/cluster/agglomerative.html', session_id=filename2, clustering_alg=clustering_alg)


