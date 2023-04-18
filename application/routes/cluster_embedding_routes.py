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

@cluster_embedding_routes.route('/node2vec/clustering/embedding/kmeans', endpoint='clustering_embedding_kmeans',  methods=['GET', 'POST'])
def clustering_embedding_kmeans():
    filename2 = session['filename2']
    clustering_alg = 'kmeans'

    return render_template('node2vec/cluster/kmeans.html', session_id=filename2, clustering_alg=clustering_alg)

@cluster_embedding_routes.route('/node2vec/clustering/embedding/spectral', endpoint='clustering_embedding_spectral',  methods=['GET', 'POST'])
def clustering_embedding_spectral():
    filename2 = session['filename2']
    clustering_alg = 'spectral'

    return render_template('node2vec/cluster/spectral.html', session_id=filename2, clustering_alg=clustering_alg)


@cluster_embedding_routes.route('/node2vec/clustering/embedding/agglomerative', endpoint='clustering_embedding_agglomerative',  methods=['GET', 'POST'])
def clustering_embedding_agglomerative():
    filename2 = session['filename2']
    clustering_alg = 'agglomerative'

    return render_template('node2vec/cluster/agglomerative.html', session_id=filename2, clustering_alg=clustering_alg)


