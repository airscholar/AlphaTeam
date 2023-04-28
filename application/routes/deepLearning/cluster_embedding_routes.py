import sys

from flask import Blueprint, render_template, session

from application.dictionary.information import *

sys.path.insert(1, '../../')

cluster_embedding_routes = Blueprint('cluster_embedding_routes', __name__)

# ----------------------------------------------CLUSTER-EMBEDDING------------------------------------------------------------------
BASE_URL = 'http://localhost:8000/api/v1/deeplearning/'


@cluster_embedding_routes.route('/node2vec/clustering/embedding/kmeans', endpoint='clustering_embedding_kmeans',
                                methods=['GET', 'POST'])
def clustering_embedding_kmeans():
    filename2 = session['filename2']
    clustering_alg = 'kmeans'

    return render_template('deepLearning/node2vec/cluster/kmeans.html', session_id=filename2,
                           clustering_alg=clustering_alg,
                           description=description['node2vec_kmeans'], tooltip_parameters=tooltips['parameters'],
                           tooltip_layout=tooltips['layout_dropdown'],
                           tooltip_number_of_clusters=tooltips['number_of_clusters'])


@cluster_embedding_routes.route('/node2vec/clustering/embedding/spectral', endpoint='clustering_embedding_spectral',
                                methods=['GET', 'POST'])
def clustering_embedding_spectral():
    filename2 = session['filename2']
    clustering_alg = 'spectral'

    return render_template('deepLearning/node2vec/cluster/spectral.html', session_id=filename2,
                           clustering_alg=clustering_alg,
                           description=description['node2vec_spectral'], tooltip_parameters=tooltips['parameters'],
                           tooltip_layout=tooltips['layout_dropdown'],
                           tooltip_number_of_clusters=tooltips['number_of_clusters'])


@cluster_embedding_routes.route('/node2vec/clustering/embedding/agglomerative',
                                endpoint='clustering_embedding_agglomerative', methods=['GET', 'POST'])
def clustering_embedding_agglomerative():
    filename2 = session['filename2']
    clustering_alg = 'agglomerative'

    return render_template('deepLearning/node2vec/cluster/agglomerative.html', session_id=filename2,
                           clustering_alg=clustering_alg,
                           description=description['node2vec_agglomerative'], tooltip_parameters=tooltips['parameters'],
                           tooltip_layout=tooltips['layout_dropdown'],
                           tooltip_number_of_clusters=tooltips['number_of_clusters'])


# Dl embedding

@cluster_embedding_routes.route('/dlembedding/clustering/embedding/kmeans',
                                endpoint='dlembedding_clustering_embedding_kmeans', methods=['GET', 'POST'])
def clustering_embedding_kmeans():
    filename2 = session['filename2']
    clustering_alg = 'kmeans'

    return render_template('deepLearning/dlembedding/cluster/kmeans.html', session_id=filename2,
                           clustering_alg=clustering_alg,
                           description=description['dlembedding_kmeans'], tooltip_dimension=tooltips['dimension'],
                           tooltip_model_dropdown=tooltips['model_dropdown'],
                           tooltip_layout=tooltips['layout_dropdown'],
                           tooltip_features=tooltips['features_checkbox'],
                           tooltip_number_of_clusters=tooltips['number_of_clusters'])


@cluster_embedding_routes.route('/dlembedding/clustering/embedding/spectral',
                                endpoint='dlembedding_clustering_embedding_spectral', methods=['GET', 'POST'])
def clustering_embedding_spectral():
    filename2 = session['filename2']
    clustering_alg = 'spectral'

    return render_template('deepLearning/dlembedding/cluster/spectral.html', session_id=filename2,
                           clustering_alg=clustering_alg,
                           description=description['dlembedding_spectral'], tooltip_dimension=tooltips['dimension'],
                           tooltip_model_dropdown=tooltips['model_dropdown'],
                           tooltip_layout=tooltips['layout_dropdown'],
                           tooltip_features=tooltips['features_checkbox'],
                           tooltip_number_of_clusters=tooltips['number_of_clusters'])


@cluster_embedding_routes.route('/dlembedding/clustering/embedding/agglomerative',
                                endpoint='dlembedding_clustering_embedding_agglomerative', methods=['GET', 'POST'])
def clustering_embedding_agglomerative():
    filename2 = session['filename2']
    clustering_alg = 'agglomerative'

    return render_template('deepLearning/dlembedding/cluster/agglomerative.html', session_id=filename2,
                           clustering_alg=clustering_alg,
                           description=description['dlembedding_agglomerative'],
                           tooltip_dimension=tooltips['dimension'],
                           tooltip_model_dropdown=tooltips['model_dropdown'],
                           tooltip_layout=tooltips['layout_dropdown'],
                           tooltip_features=tooltips['features_checkbox'],
                           tooltip_number_of_clusters=tooltips['number_of_clusters'])
