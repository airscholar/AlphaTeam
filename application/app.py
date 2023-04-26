import sys

import requests
from flask import Flask, request, render_template, session
from flask_cors import CORS

from flask_session import Session
from application.routes.metrics.centrality_routes import centrality_routes
from application.routes.clusters.cluster_routes import cluster_routes
from application.routes.metrics.node_routes import node_routes
from application.routes.resilience.resilience_routes import resilience_routes
from application.routes.deepLearning.cluster_embedding_routes import cluster_embedding_routes
from application.routes.deepLearning.embedding_routes import embedding_routes
from application.routes.hotspot.hotspot_routes import hotspot_routes
from application.routes.metrics.global_metrics_routes import global_metrics_routes
from application.routes.visualisation.visualisation_routes import visualisation_routes

sys.path.insert(1, '../')
from src.NetworkGraphs import *
from src.metrics import *
from src.visualisation import *
from src.utils import *

from flask_caching import Cache
import shutil

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

app.register_blueprint(cluster_routes)
app.register_blueprint(centrality_routes)
app.register_blueprint(node_routes)
app.register_blueprint(resilience_routes)
app.register_blueprint(cluster_embedding_routes)
app.register_blueprint(embedding_routes)
app.register_blueprint(hotspot_routes)
app.register_blueprint(global_metrics_routes)
app.register_blueprint(visualisation_routes)

BASE_URL = 'http://3.221.153.241:8000/api/v1'


# Define a custom error page for 500 Internal Server Error
@app.errorhandler(500)
def internal_server_error(e):
    if cache.has('global_metrics') or 'filename' in session:
        # Delete the file
        filename = session['filename']
        filename2 = session['filename2']
        filepath = 'static/uploads/' + filename2
        if os.path.exists(filepath):
            shutil.rmtree(filepath)
        if is_saved(filename2):
            delete_networkGraph(filename2)
            cache.clear()
        # Remove the keys from the session
        session.pop('network_graphs', None)
        session.pop('filename', None)
        session.pop('filename2', None)
        session.pop('filepath', None)
        session.pop('option', None)
        session.clear()
    return render_template('500.html')


# Define a custom error page for 404 Not Found Error
@app.errorhandler(404)
def not_found_error(e):
    return render_template('404.html')


@app.route('/')
def index():
    # Check if global_metrics is present in the cache and filename is present in the session
    if cache.has('global_metrics') or 'filename' in session:
        # Delete the file
        filename = session['filename']
        filename2 = session['filename2']
        filepath = 'static/uploads/' + filename2
        if os.path.exists(filepath):
            shutil.rmtree(filepath)
        # Clear the cache
        cache.clear()
        if is_saved(filename2):
            delete_networkGraph(filename2)
        # Remove the keys from the session
        session.pop('network_graphs', None)
        session.pop('filename', None)
        session.pop('filename2', None)
        session.pop('filepath', None)
        session.pop('full_path', None)
        session.pop('option', None)
        session.clear()

    return render_template('index.html')


@app.route('/index/sample-dataset')
def index_sample():
    return render_template('index_sample_dataset.html')


@app.route('/home')
def home():
    args = request.args
    filename = args.get('filename')
    filename2 = args.get('filename2')
    filepath = args.get('filepath')
    full_path = args.get('full_path')
    option = args.get('option')

    networkGraphs = None

    if filename2 is None or filename2 == '':
        filename2 = session['filename2']
        networkGraphs = get_networkGraph(filename2)
    else:
        session['filename'] = filename
        session['filename2'] = filename2
        session['filepath'] = filepath
        session['full_path'] = full_path
        session['option'] = option

    # networkGraphs = NetworkGraphs(filepath, session_folder=filepath.split('/'+filename)[0], type=option)
        networkGraphs = NetworkGraphs(full_path, session_folder=filepath.split('.')[0], type=option)
        set_networkGraph(networkGraphs, filename2)

    # Pass the data to the HTML template
    return render_template('home.html', session_id=filename2)

# -------------------------------------------MAIN--------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
