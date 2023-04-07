import sys

from dictionary.information import *
from flask import Blueprint, render_template, session
from routes.template_metrics import *

from backend.common.common import process_metric

sys.path.insert(1, '../')
from src.metrics import *

embedding_routes = Blueprint('embedding_routes', __name__)


#----------------------------------------------CLUSTER-EMBEDDING------------------------------------------------------------------

@embedding_routes.route('/embedding', endpoint='embedding', methods=['GET'])
def embedding_kmeans():
    filename2 = session['filename2']
    graph_path1 = '../static/no_graph.html'
    graph_path2 = '../static/no_graph.html'
    df = pd.DataFrame()
#     attack_types = ['degree_centrality', 'betweenness_centrality', 'closeness_centrality', 'eigenvector_centrality',
#                     'load_centrality', 'kcore', 'degree', 'pagerank', 'triangles']

#     number_of_nodes_malicious = None
#     number_of_threshold = None
#     number_of_clusters = None

    return render_template('deep_learning/embedding.html', session_id=filename2, example=df,
                            graph_path1=graph_path1, graph_path2=graph_path2)

