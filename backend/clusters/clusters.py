import flask_restx
from flask import Blueprint

cluster_bp = Blueprint('clusters', __name__, url_prefix="/api/v1/clusters")

@cluster_bp.route('/louvain')
def LouvainClustering():
    return {"message": "Louvain Clustering"}


@cluster_bp.route('/spectral')
def SpectralClustering():
    return {"message": "Spectral Clustering"}


@cluster_bp.route('/kmeans')
def KMeansClustering():
    return {"message": "KMeans Clustering"}


@cluster_bp.route('/asyn-lpa')
def AsynLpaClustering():
    return {"message": "AsynLpa Clustering"}




