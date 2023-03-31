import flask_restx
from flask import Blueprint

metrics_bp = Blueprint('metrics', __name__, url_prefix="/api/v1/metrics")


@metrics_bp.route('/k-core')
def KCore():
    return {"message": "KCore metrics"}


@metrics_bp.route('/degree')
def Degree():
    return {"message": "Degree"}


@metrics_bp.route('/triangles')
def Triangles():
    return {"message": "Triangles"}


@metrics_bp.route('/pagerank')
def PageRank():
    return {"message": "PageRank"}


@metrics_bp.route('/betweenness-centrality')
def BetweennessCentrality():
    return {"message": "BetweennessCentrality"}


@metrics_bp.route('/closeness-centrality')
def ClosenessCentrality():
    return {"message": "ClosenessCentrality"}


@metrics_bp.route('/eigenvector-centrality')
def EigenvectorCentrality():
    return {"message": "EigenvectorCentrality"}


@metrics_bp.route('/load-centrality')
def LoadCentrality():
    return {"message": "LoadCentrality"}


@metrics_bp.route('/degree-centrality')
def DegreeCentrality():
    return {"message": "DegreeCentrality"}
