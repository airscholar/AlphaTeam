from flask import Flask, request, jsonify, send_file, render_template
from threading import Thread
import nbformat
from nbconvert import PythonExporter
import io
from pyvis.network import Network
import networkx as nx # import networkx package
import os

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Check if a file was uploaded
    if 'csv_file' not in request.files:
        return 'No file was uploaded.', 400
    
    # Get the uploaded file
    file = request.files.get('csv_file')
    print(file)  # Debugging statement
    print(file.filename)  # Debugging statement

    # Save the uploaded file to the same directory as app.py
    file_path = os.path.join(os.getcwd(), 'data.csv')
    file.save(file_path)
    # Start the machine learning process in the background
    thread = Thread(target=run_machine_learning, args=(file,))
    thread.start()

    # Return a response to the user
    return jsonify({'message': 'Processing the uploaded file...'})

def run_machine_learning(file):
    # Read the contents of the uploaded file
    csv_data = file.read().decode('utf-8')

    # Convert the Rail.ipynb notebook to Python code
    notebook_path = 'Rail.ipynb'
    with io.open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    exporter = PythonExporter()
    source, meta = exporter.from_notebook_node(nb)

    # Define the network variable in the global namespace of the notebook
    source = "global network\nnetwork = {}\n" + source

    # Execute the Python code with the uploaded file data
    network = exec(source, {'network': {}})
    graph = network

    # Generate the graph visualization using pyvis
    net = Network(height="100%", width="100%", bgcolor="#222222", font_color="white")
    net.barnes_hut(gravity=-8000, central_gravity=0.3, spring_length=150)
    net.show_buttons(filter_=['physics'])
    
    for train, stations in graph.items():
        for i, station in enumerate(stations):
            net.add_node(station['id'], label=station['name'], x=station['lon'], y=station['lat'])

            # Add edges between adjacent stations
            if i > 0:
                net.add_edge(stations[i-1]['id'], station['id'])

            # Add node sizes and colors based on the number of trains passing through
            num_trains = len(network[train])
            net.nodes[station['id']]['size'] = num_trains
            net.nodes[station['id']]['color'] = "rgb({}, 0, 0)".format(255 - num_trains)

    # Get the HTML representation of the graph
    graph_html = net.to_html()

    # Return the HTML string
    return graph_html

@app.route('/graph')
def serve_graph():
    # Call the run_machine_learning() function to generate the graph
    graph_html = run_machine_learning()

    # Render the graph HTML on the page
    return render_template('graph.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run()
