from flask import Flask, request, jsonify, send_file, render_template
from threading import Thread
import nbformat
from nbconvert import PythonExporter
import io
from pyvis.network import Network
import networkx as nx # import networkx package
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from Rail import Railway

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('index.html')

def process_file(file_path):
    # Create an instance of the Railway class
    r = Railway(file_path)
    r.load_data()
    r.set_station_id()
    r.create_network_graph()
    r.plot_graph()

@app.route('/upload', methods=['POST'])
def upload():
    # Check if a file was uploaded
    if 'csv_file' not in request.files:
        return 'No file was uploaded.', 400
    
    # Get the uploaded file
    file = request.files.get('csv_file')
    # Save the uploaded file to the datasets directory
    file_path = os.path.join(os.path.dirname(__file__), '..', 'datasets', 'Railway.csv')
    file.save(file_path)

    # Start the process_file function in the background
    thread = Thread(target=process_file, args=(file_path,))
    thread.start()

    # Return a response to the user
    return jsonify({'message': 'Processing the uploaded file...'})

@app.route('/graph')
def serve_graph():
    # Render the graph HTML on the page
    return render_template('graph.html')

if __name__ == '__main__':
    app.run()
