from flask import Flask, request, render_template, redirect, url_for, session
from flask_session import Session
from dictionary.information import *
from routes.cluster_routes import cluster_routes
from routes.centrality_routes import centrality_routes 
from routes.node_routes import node_routes
from routes.resilience_routes import resilience_routes
import html
import csv
import sys
sys.path.insert(1, '../')
from src.NetworkGraphs import *
from src.metrics import *
from src.preprocessing import *
from src.visualisation import *
from src.utils import *

import scipy as sp
from flask_caching import Cache
import matplotlib.pyplot as plt
import re
import time
import shutil

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

app.register_blueprint(cluster_routes)
app.register_blueprint(centrality_routes)
app.register_blueprint(node_routes)
app.register_blueprint(resilience_routes)

# Define a custom error page for 500 Internal Server Error
@app.errorhandler(500)
def internal_server_error(e):
    if cache.has('global_metrics') or 'filename' in session:
        # Delete the file
        filename = session['filename']
        filename2 = session['filename2']
        filepath = 'static/uploads/'+filename2
        if os.path.exists(filepath):
            shutil.rmtree(filepath)        
        #cache.clear()
        # Remove the keys from the session
        #session.pop('network_graphs', None)
        #session.pop('filename', None)
        #session.pop('filename2', None)
        #session.pop('filepath', None)
        #session.pop('option', None)
        #session.clear()
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
        filepath = 'static/uploads/'+filename2
        if os.path.exists(filepath):
            shutil.rmtree(filepath)
        # Clear the cache
        cache.clear()
        # Remove the keys from the session
        session.pop('network_graphs', None)
        session.pop('filename', None)
        session.pop('filename2', None)
        session.pop('filepath', None)
        session.pop('option', None)
        session.clear()
    return render_template('index.html')

@app.route('/index/sample-dataset')
def index_sample():
    return render_template('index_sample_dataset.html')

@app.route('/upload', methods=['POST'])
def upload():
    data = request.form
    print(data)
    timestamp = str(int(time.time()))

    # Get the CSV file and the selected option
    if 'option2' in request.form:
        csv_file = request.form['csv_path']
        option = request.form['option']
        # Save the CSV file to a folder on the server with a filename based on the selected option and file extension
        if option != 'MTX':
            source_file = csv_file + option +'.csv'
            filename = option + re.sub(r'\W+', '', timestamp) + '.csv'
            filename2 = option + re.sub(r'\W+', '', timestamp)
        else:
            source_file = csv_file + option +'.mtx'
            filename = option + re.sub(r'\W+', '', timestamp) + '.mtx'
            filename2 = option + re.sub(r'\W+', '', timestamp)
        # Check if the directory exists, and create it if it doesn't
        destination_dir = 'static/uploads/'+filename2
        # Create the directory if it doesn't exist
        destination_dir = 'static/uploads/'+filename2
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        destination_file = filename
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
        destination_dir = 'static/uploads/'+filename2
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        csv_file.save(destination_dir + '/' + filename)
        # Do something with the CSV file and selected option
        # (e.g., process the file data and store it in a database)

        filepath = destination_dir + '/' + filename
        
        # Store the filename in a session variable
        session['filename'] = filename
        session['filename2'] = filename2
        session['filepath'] = filepath
        session['option'] = option    

    networkGraphs = NetworkGraphs(filepath, session_folder='static/uploads/'+filename2, type=option)
    set_networkGraph(networkGraphs, filename2)
    # Redirect the user to the success page
    return redirect(url_for('home'))

@app.route('/home')
def home():
    # Get the filename from the session variable
    filename = session['filename']
    filename2 = session['filename2']
    filepath = session['filepath']
    option = session['option']
    networkGraphs = get_networkGraph(filename2)

    # Pass the data to the HTML template
    return render_template('home.html', data=networkGraphs.df.head(100))

@app.route('/global-metrics', methods=['GET', 'POST'])
def globalmetrics():
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    multi_toggle = False
    directed_toggle = False
    
    if request.method == 'POST':
        multi_toggle = bool(request.form.get('multi_toggle'))
        directed_toggle = bool(request.form.get('directed_toggle'))
        global_metrics = compute_global_metrics(networkGraphs, directed_toggle, multi_toggle)
    else:
        global_metrics = compute_global_metrics(networkGraphs, directed_toggle, multi_toggle)

    return render_template('global_metrics.html', example=global_metrics, multi_toggle=multi_toggle, directed_toggle=directed_toggle)

#-------------------------------------------VISUALISATION-----------------------------------

@app.route('/visualisation', methods=['GET', 'POST'], endpoint='visualisation')
def visualisation():
    filename = session['filename']
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    dynamic_toggle = False
    tab = 'tab1'
    if networkGraphs.is_spatial():
        layout = 'map'
        layout2 = 'map'
        show_temporal = str(networkGraphs.is_temporal()).lower()
        print('tab false spatial', show_temporal)
    else:
        layout = 'sfdp'
        layout2 = 'sfdp'
        show_temporal = str(networkGraphs.is_temporal()).lower()
        print('tab is temporal', show_temporal)


    if request.method == 'POST':
        if (request.form.get('dynamic_toggle') is not None or request.form.get('layout') is not None):
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            layout = request.form.get('layout')
            graph_name1 = plot_network(networkGraphs, layout=layout, dynamic=dynamic_toggle)
            session['graph_name1'] = graph_name1
            tab = 'tab1'
        if (request.form.get('layout2') is not None):
            layout2 = request.form.get('layout2')
            graph_name2 = plot_temporal(networkGraphs, layout=layout2)
            session['graph_name2'] = graph_name2
            tab = 'tab2'
    else:
        graph_name1 = plot_network(networkGraphs, layout=layout, dynamic=dynamic_toggle)
        session['graph_name1'] = graph_name1
        graph_name2 = plot_temporal(networkGraphs, layout=layout2)
        session['graph_name2'] = graph_name2
    graph1 = session['graph_name1']
    graph2 = session['graph_name2']
    

    if graph1 == 'no_graph.html':
        graph_path1 = '../static/' + graph1
    else:
        graph_path1 = '../static/uploads/' + filename2 + '/' + graph1

    if graph2 == 'no_graph.html':
        graph_path2 = '../static/' + graph2
    else:
        graph_path2 = '../static/uploads/' + filename2 + '/' + graph2
    

    return render_template('visualisation.html', tab=tab, show_temporal=show_temporal,
    dynamic_toggle=dynamic_toggle, layout=layout, graph1=graph_path1, 
    layout2=layout2, graph2=graph_path2)

#-------------------------------------------HOTSPOT-----------------------------------------

@app.route('/hotspot/density', endpoint='hotspot_density', methods=['GET', 'POST'])
def hotspot_density():
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)

    df, graph_name1 = plot_hotspot(networkGraphs)
    session['graph_name1'] = graph_name1
    graph1 = session['graph_name1']
 
    if graph1 == 'no_graph.html':
        graph_path1 = '../static/' + graph1
    else:
        graph_path1 = '../static/uploads/' + filename2 + '/' + graph1

    if graph1 == 'no_graph.html':
        graph_path1 = '../static/' + graph1
    else:
        graph_path1 = '../static/uploads/' + filename2 + '/' + graph1
        
    return render_template('hotspot_density.html', example=df, graph1=graph_path1, method_name='Density')


#-------------------------------------------MAIN--------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
