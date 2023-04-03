import os
import re
import shutil
import time

import flask
from flask import request, session
from flask_cors import CORS

from backend.clusters.clusters import cluster_bp
from backend.hotspot.density import hotspot_bp
from backend.metrics.metrics import metrics_bp
from backend.resilience.resilience import resilience_bp
from backend.visualisation.visualisation import visualisation_bp
from src.NetworkGraphs import NetworkGraphs
from src.utils import set_networkGraph, get_networkGraph

app = flask.Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['SECRET_KEY'] = 'your_secret_key'
api_bp = flask.Blueprint("api", __name__, url_prefix="/api/v1")


@api_bp.route('/')
def homepage():
    return {"message": "AlphaTeam Backend API"}


@api_bp.route('/upload', methods=['POST'])
def upload():
    data = request.form
    timestamp = str(int(time.time()))
    # Get the CSV file and the selected option
    if 'option2' in request.form:
        csv_file = request.form['csv_path']

        option = request.form['option']
        # Save the CSV file to a folder on the server with a filename based on the selected option and file extension
        if option != 'MTX':
            source_file = csv_file + option + '.csv'
            filename = option + re.sub(r'\W+', '', timestamp) + '.csv'
            filename2 = option + re.sub(r'\W+', '', timestamp)
        else:
            source_file = csv_file + option + '.mtx'
            filename = option + re.sub(r'\W+', '', timestamp) + '.mtx'
            filename2 = option + re.sub(r'\W+', '', timestamp)

        # Create the directory if it doesn't exist
        destination_dir = '../application/static/uploads/' + filename2
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        destination_file = filename
        print(source_file, destination_dir + '/' + destination_file)
        shutil.copy(source_file, destination_dir + '/' + destination_file)
        filepath = destination_dir + '/' + filename
        # Store the filename in a session variable
        session['filename'] = filename
        session['filename2'] = filename2
        session['filepath'] = filepath
        session['option'] = option
    else:
        csv_file = request.files['csv_file']
        option = request.form['option']
        # Save the CSV file to a folder on the server with a filename based on the selected option and file extension
        if option != 'MTX':
            filename = option + re.sub(r'\W+', '', timestamp) + '.csv'
            filename2 = option + re.sub(r'\W+', '', timestamp)
        else:
            filename = option + re.sub(r'\W+', '', timestamp) + '.mtx'
            filename2 = option + re.sub(r'\W+', '', timestamp)

        # Create the directory if it doesn't exist
        destination_dir = '../application/static/uploads/' + filename2
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        filepath = destination_dir + '/' + filename
        csv_file.save(filepath)

        # Store the filename in a session variable
        session['filename'] = filename
        session['filename2'] = filename2
        session['filepath'] = filepath
        session['option'] = option
        session['destination_dir'] = destination_dir

    networkGraphs = NetworkGraphs(filepath, session_folder=destination_dir, type=option)
    set_networkGraph(networkGraphs, filename2)
    # Redirect the user to the success page
    return {"message": "File uploaded successfully", "filename": filename, "filename2": filename2,
            "filepath": filepath, "full_path": os.getcwd() + '/' + filepath,
            "option": option}


@api_bp.route('/get_networkGraph/<session_id>', methods=['GET'])
def retrieve_networkGraph(session_id):
    networkGraphs = get_networkGraph(session_id)
    return networkGraphs.to_json()


# Register the API blueprint with the app
app.register_blueprint(api_bp)
app.register_blueprint(cluster_bp)
app.register_blueprint(metrics_bp)
app.register_blueprint(hotspot_bp)
app.register_blueprint(visualisation_bp)
app.register_blueprint(resilience_bp)

# add documentation
# api = flask_restx.Api(app, version='1.0', title='AlphaTeam Backend API',
#                       description='Backend API for AlphaTeam',
#                       doc='/api/v1/docs/')


if __name__ == '__main__':
    app.run()
