import pandas as pd
from flask import Blueprint, request
from flask_jsonpify import jsonify

from backend.common.common import get_arg_layout
from src.utils import get_networkGraph
from src.visualisation import plot_node2vec, plot_embedding_cluster

deepLearning_bp = Blueprint('deeplearning', __name__, url_prefix="/api/v1/deeplearning")

def get_arg_p(args):
    p = args.get('p', 1.0, type=float)
    return p

def get_arg_q(args):
    q = args.get('q', 1.0, type=float)
    return q

def get_arg_no_of_clusters(args):
    no_of_clusters = args.get('number_of_clusters', 0, type=int)
    return no_of_clusters

def get_arg_clustering_alg(args):
    clustering_alg = args.get('cluster_algorithm', 'kmeans', type=str)
    if clustering_alg not in ['kmeans', 'spectral', 'agglomerative']:
        raise ValueError('Clustering algorithm not supported, please choose between kmeans, spectral and agglomerative')
    return clustering_alg

@deepLearning_bp.route('<session_id>/node_embedding')
def node_embedding(session_id):
    q = get_arg_q(request.args)
    p = get_arg_p(request.args)
    layout = get_arg_layout(request.args)

    networkGraphs = get_networkGraph(session_id)

    if layout in ['TSNE', 'PCA', 'UMAP']:
        df, filename = plot_node2vec(networkGraphs, layout=layout, p=p, q=q, fullPath=True)
    else:
        raise ValueError('Layout not supported, please choose between TSNE, PCA and UMAP')

    df_json = df.to_json(orient='split')
    filename = filename.replace('../application/', '')
    return jsonify({'message': 'Success', 'data': df_json, 'filename': filename})


@deepLearning_bp.route('<session_id>/embedding_clustering')
def embedding_clustering(session_id):
    clustering_alg = get_arg_clustering_alg(request.args)

    if clustering_alg not in ['kmeans', 'spectral', 'agglomerative']:
        raise ValueError('Clustering algorithm not supported, please choose between kmeans, spectral and agglomerative')

    q = get_arg_q(request.args)
    p = get_arg_p(request.args)
    layout = get_arg_layout(request.args)
    no_of_clusters = get_arg_no_of_clusters(request.args)

    networkGraphs = get_networkGraph(session_id)

    if layout in ['TSNE', 'PCA', 'UMAP', 'map', 'sfdp', 'twopi']:
        df, filename = plot_embedding_cluster(networkGraphs,
                                              clustering_alg,
                                              layout=layout,
                                              p=p,
                                              q=q,
                                              noOfCluster=no_of_clusters,
                                              fullPath=True)
    else:
        raise ValueError('Layout not supported, please choose between TSNE, PCA and UMAP, map, sfdp, twopi')
    df_json = df.to_json(orient='split')
    filename = filename.replace('../application/', '../')
    return jsonify({'message': 'Success', 'data': df_json, 'filename': filename})

