from flask import Flask, request, render_template, redirect, url_for, session
from flask_session import Session
from routes.cluster_routes import cluster_routes
from routes.centrality_routes import centrality_routes
import csv
import sys
sys.path.insert(1, '../')
from src.NetworkGraphs import *
from src.metrics import *
from src.preprocessing import *
from src.visualisation import *
from flask import g  # Add this import at the beginning of the file

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
        cache.clear()

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

    # Redirect the user to the success page
    return redirect(url_for('home'))

@app.route('/home')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def home():
    # Get the filename from the session variable
    filename = session['filename']
    filename2 = session['filename2']
    filepath = session['filepath']
    option = session['option']
    
    # Assign the value to the global variable
    networkGraphs = session['network_graphs']
    if networkGraphs is None:
        g.networkGraphs = NetworkGraphs(filepath, session_folder='static/uploads/'+filename2, type=option)
        networkGraphs = g.networkGraphs
        session['network_graphs'] = networkGraphs

    networkGraphs = session['network_graphs']
    global_metrics = cache.get('global_metrics')
    if global_metrics is None:
        global_metrics = compute_global_metrics(networkGraphs)
        cache.set('global_metrics', global_metrics)
    
    # Pass the data to the HTML template
    return render_template('home.html', example=global_metrics)

@app.route('/uploaded_dataset')
def uploaded_dataset():
    return render_template('display_base_dataset.html', data=networkGraphs.df.head(100))

#-------------------------------------------VISUALISATION-----------------------------------

@app.route('/visualisation', methods=['GET', 'POST'], endpoint='visualisation')
def visualisation():
    networkGraphs = session['network_graphs']
    filename = session['filename']
    filename2 = session['filename2']
    dynamic_toggle = False
    dynamic_toggle2 = False
    tab = 'tab1'
    if networkGraphs.is_spatial():
        layout = 'map'
        layout2 = 'map'
        tab_false = 'true'
    else:
        layout = 'sfdp'
        layout2 = 'sfdp'
        tab_false = 'false'


    if request.method == 'POST':
        if (request.form.get('dynamic_toggle') is not None or request.form.get('layout') is not None):
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            layout = request.form.get('layout')
            graph_name1 = plot_network(networkGraphs, layout=layout, dynamic=dynamic_toggle)
            session['graph_name1'] = graph_name1
            tab = 'tab1'
        if (request.form.get('dynamic_toggle2') is not None or request.form.get('layout2') is not None):
            dynamic_toggle2 = bool(request.form.get('dynamic_toggle2'))
            layout2 = request.form.get('layout2')
            graph_name2 = plot_network(networkGraphs, layout=layout2, dynamic=dynamic_toggle2)
            session['graph_name2'] = graph_name2
            tab = 'tab2'
    else:
        graph_name1 = plot_network(networkGraphs, layout=layout, dynamic=dynamic_toggle)
        session['graph_name1'] = graph_name1
        graph_name2 = plot_network(networkGraphs, layout=layout2, dynamic=dynamic_toggle2)
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
    

    return render_template('visualisation.html', tab=tab, tab_false=tab_false,
    dynamic_toggle=dynamic_toggle, layout=layout, graph1=graph_path1, 
    dynamic_toggle2=dynamic_toggle2, layout2=layout2, graph2=graph_path2)

#-------------------------------------------NODE--------------------------------------------

@app.route('/node_all', endpoint='node_all', methods=['GET', 'POST'])
def node_all():
    networkGraphs = session['network_graphs']
    filename2 = session['filename2']
    metrics = 'nodes'
    multi_toggle = True
    directed_toggle = False
    multi_toggle2 = True
    directed_toggle2 = False
    multi_toggle3 = True
    dynamic_toggle3 = False
    directed_toggle3 = False
    multi_toggle4 = True
    dynamic_toggle4 = False
    directed_toggle4 = False
    tab = 'tab1'
    if networkGraphs.is_spatial():
        layout = 'map'
        layout2 = 'map'
        layout3 = 'map'
        layout4 = 'map'
    else:
        layout = 'sfdp'
        layout2 = 'sfdp'
        layout3 = 'sfdp'
        layout4 = 'sfdp'

    if request.method == 'POST':
        if (request.form.get('multi_toggle') is not None or request.form.get('directed_toggle') is not None or request.form.get('layout') is not None):
            multi_toggle = bool(request.form.get('multi_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
            df, graph_name1 = plot_all_metrics(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle, layout=layout)
            session['graph_name1'] = graph_name1
            tab = 'tab1'
        if (request.form.get('multi_toggle2') is not None or request.form.get('directed_toggle2') is not None or request.form.get('layout2') is not None):
            multi_toggle2 = bool(request.form.get('multi_toggle2'))
            directed_toggle2 = bool(request.form.get('directed_toggle2'))
            layout2 = request.form.get('layout2')
            df, graph_name2 = plot_histogram(networkGraphs, metrics, directed=directed_toggle2, multi=multi_toggle2)
            session['graph_name2'] = graph_name2
            tab = 'tab2'
        if (request.form.get('multi_toggle3') is not None or request.form.get('directed_toggle3') is not None or request.form.get('layout3') is not None):
            multi_toggle3 = bool(request.form.get('multi_toggle3'))
            directed_toggle3 = bool(request.form.get('directed_toggle3'))
            layout3 = request.form.get('layout3')
            df, graph_name3 = plot_boxplot(networkGraphs, metrics, directed=directed_toggle3, multi=multi_toggle3)
            session['graph_name3'] = graph_name3
            tab = 'tab3'
        if (request.form.get('multi_toggle4') is not None or request.form.get('directed_toggle4') is not None or request.form.get('layout4') is not None):
            multi_toggle4 = bool(request.form.get('multi_toggle4'))
            directed_toggle4 = bool(request.form.get('directed_toggle4'))
            layout4 = request.form.get('layout4')
            df, graph_name4 = plot_violin(networkGraphs, metrics, directed=directed_toggle4, multi=multi_toggle4)
            session['graph_name4'] = graph_name4
            tab = 'tab4'
    else:
        df, graph_name1 = plot_all_metrics(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle, layout=layout)
        session['graph_name1'] = graph_name1
        df, graph_name2 = plot_histogram(networkGraphs, metrics, directed=directed_toggle2, multi=multi_toggle2)
        session['graph_name2'] = graph_name2
        df, graph_name3 = plot_boxplot(networkGraphs, metrics, directed=directed_toggle3, multi=multi_toggle3)
        session['graph_name3'] = graph_name3
        df, graph_name4 = plot_violin(networkGraphs, metrics, directed=directed_toggle4, multi=multi_toggle4)
        session['graph_name4'] = graph_name4
    graph1 = session['graph_name1']
    graph2 = session['graph_name2']
    graph3 = session['graph_name3']
    graph4 = session['graph_name4']
    
    if graph1 == 'no_graph.html':
        graph_path1 = '../static/' + graph1
    else:
        graph_path1 = '../static/uploads/' + filename2 + '/' + graph1

    if graph2 == 'no_graph.html':
        graph_path2 = '../static/' + graph2
    else:
        graph_path2 = '../static/uploads/' + filename2 + '/' + graph2
    
    if graph3 == 'no_graph.html':
        graph_path3 = '../static/' + graph3
    else:
        graph_path3 = '../static/uploads/' + filename2 + '/' + graph3

    if graph4 == 'no_graph.html':
        graph_path4 = '../static/' + graph4
    else:
        graph_path4 = '../static/uploads/' + filename2 + '/' + graph4

    return render_template('node_all.html', example=df, tab=tab, method_name='All Nodes',
    multi_toggle=multi_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, 
    multi_toggle2=multi_toggle2, directed_toggle2=directed_toggle2, layout2=layout2, graph2=graph_path2,
    multi_toggle3=multi_toggle3, directed_toggle3=directed_toggle3, layout3=layout3, graph3=graph_path3,
    multi_toggle4=multi_toggle4, directed_toggle4=directed_toggle4, layout4=layout4, graph4=graph_path4)

@app.route('/node/degree', endpoint='node_degree', methods=['GET', 'POST'])
def node_degree():
    networkGraphs = session['network_graphs']
    filename2 = session['filename2']
    metrics = 'degree'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    multi_toggle2 = True
    dynamic_toggle2 = False
    directed_toggle2 = False
    layout2 = 'map'
    multi_toggle3 = True
    dynamic_toggle3 = False
    directed_toggle3 = False
    layout3 = 'map'
    multi_toggle4 = True
    dynamic_toggle4 = False
    directed_toggle4 = False
    layout4 = 'map'
    tab = 'tab1'
    
    if request.method == 'POST':
        if (request.form.get('multi_toggle') is not None or request.form.get('dynamic_toggle') is not None or request.form.get('directed_toggle') is not None or request.form.get('layout') is not None):
            multi_toggle = bool(request.form.get('multi_toggle'))
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
            df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle, dynamic=dynamic_toggle, layout=layout)
            session['graph_name1'] = graph_name1
            tab = 'tab1'
        if (request.form.get('multi_toggle2') is not None or request.form.get('dynamic_toggle2') is not None or request.form.get('directed_toggle2') is not None or request.form.get('layout2') is not None):
            multi_toggle2 = bool(request.form.get('multi_toggle2'))
            dynamic_toggle2 = bool(request.form.get('dynamic_toggle2'))
            directed_toggle2 = bool(request.form.get('directed_toggle2'))
            layout2 = request.form.get('layout2')
            df, graph_name2 = plot_histogram(networkGraphs, metrics, directed=directed_toggle2, multi=multi_toggle2)
            session['graph_name2'] = graph_name2
            tab = 'tab2'
        if (request.form.get('multi_toggle3') is not None or request.form.get('dynamic_toggle3') is not None or request.form.get('directed_toggle3') is not None or request.form.get('layout3') is not None):
            multi_toggle3 = bool(request.form.get('multi_toggle3'))
            dynamic_toggle3 = bool(request.form.get('dynamic_toggle3'))
            directed_toggle3 = bool(request.form.get('directed_toggle3'))
            layout3 = request.form.get('layout3')
            df, graph_name3 = plot_boxplot(networkGraphs, metrics, directed=directed_toggle3, multi=multi_toggle3)
            session['graph_name3'] = graph_name3
            tab = 'tab3'
        if (request.form.get('multi_toggle4') is not None or request.form.get('dynamic_toggle4') is not None or request.form.get('directed_toggle4') is not None or request.form.get('layout4') is not None):
            multi_toggle4 = bool(request.form.get('multi_toggle4'))
            dynamic_toggle4 = bool(request.form.get('dynamic_toggle4'))
            directed_toggle4 = bool(request.form.get('directed_toggle4'))
            layout4 = request.form.get('layout4')
            df, graph_name4 = plot_violin(networkGraphs, metrics, directed=directed_toggle4, multi=multi_toggle4)
            session['graph_name4'] = graph_name4
            tab = 'tab4'
    else:
        df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
        df, graph_name2 = plot_histogram(networkGraphs, metrics, directed=directed_toggle2, multi=multi_toggle2)
        session['graph_name2'] = graph_name2
        df, graph_name3 = plot_boxplot(networkGraphs, metrics, directed=directed_toggle3, multi=multi_toggle3)
        session['graph_name3'] = graph_name3
        df, graph_name4 = plot_violin(networkGraphs, metrics, directed=directed_toggle4, multi=multi_toggle4)
        session['graph_name4'] = graph_name4
    graph1 = session['graph_name1']
    graph2 = session['graph_name2']
    graph3 = session['graph_name3']
    graph4 = session['graph_name4']
    
    if graph1 == 'no_graph.html':
        graph_path1 = '../static/' + graph1
    else:
        graph_path1 = '../static/uploads/' + filename2 + '/' + graph1

    if graph2 == 'no_graph.html':
        graph_path2 = '../static/' + graph2
    else:
        graph_path2 = '../static/uploads/' + filename2 + '/' + graph2
    
    if graph3 == 'no_graph.html':
        graph_path3 = '../static/' + graph3
    else:
        graph_path3 = '../static/uploads/' + filename2 + '/' + graph3

    if graph4 == 'no_graph.html':
        graph_path4 = '../static/' + graph4
    else:
        graph_path4 = '../static/uploads/' + filename2 + '/' + graph4

    return render_template('node_degree.html', example=df, tab=tab, 
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, 
    multi_toggle2=multi_toggle2, dynamic_toggle2=dynamic_toggle2, directed_toggle2=directed_toggle2, layout2=layout2, graph2=graph_path2,
    multi_toggle3=multi_toggle3, dynamic_toggle3=dynamic_toggle3, directed_toggle3=directed_toggle3, layout3=layout3, graph3=graph_path3,
    multi_toggle4=multi_toggle4, dynamic_toggle4=dynamic_toggle4, directed_toggle4=directed_toggle4, layout4=layout4, graph4=graph_path4)

@app.route('/node/kcore', endpoint='node_kcore', methods=['GET', 'POST'])
def node_kcore():
    networkGraphs = session['network_graphs']
    filename2 = session['filename2']
    metrics = 'kcore'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    multi_toggle2 = True
    dynamic_toggle2 = False
    directed_toggle2 = False
    layout2 = 'map'
    multi_toggle3 = True
    dynamic_toggle3 = False
    directed_toggle3 = False
    layout3 = 'map'
    multi_toggle4 = True
    dynamic_toggle4 = False
    directed_toggle4 = False
    layout4 = 'map'
    tab = 'tab1'
    
    if request.method == 'POST':
        if (request.form.get('multi_toggle') is not None or request.form.get('dynamic_toggle') is not None or request.form.get('directed_toggle') is not None or request.form.get('layout') is not None):
            multi_toggle = bool(request.form.get('multi_toggle'))
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
            df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle, dynamic=dynamic_toggle, layout=layout)
            session['graph_name1'] = graph_name1
            tab = 'tab1'
        if (request.form.get('multi_toggle2') is not None or request.form.get('dynamic_toggle2') is not None or request.form.get('directed_toggle2') is not None or request.form.get('layout2') is not None):
            multi_toggle2 = bool(request.form.get('multi_toggle2'))
            dynamic_toggle2 = bool(request.form.get('dynamic_toggle2'))
            directed_toggle2 = bool(request.form.get('directed_toggle2'))
            layout2 = request.form.get('layout2')
            df, graph_name2 = plot_histogram(networkGraphs, metrics, directed=directed_toggle2, multi=multi_toggle2)
            session['graph_name2'] = graph_name2
            tab = 'tab2'
        if (request.form.get('multi_toggle3') is not None or request.form.get('dynamic_toggle3') is not None or request.form.get('directed_toggle3') is not None or request.form.get('layout3') is not None):
            multi_toggle3 = bool(request.form.get('multi_toggle3'))
            dynamic_toggle3 = bool(request.form.get('dynamic_toggle3'))
            directed_toggle3 = bool(request.form.get('directed_toggle3'))
            layout3 = request.form.get('layout3')
            df, graph_name3 = plot_boxplot(networkGraphs, metrics, directed=directed_toggle3, multi=multi_toggle3)
            session['graph_name3'] = graph_name3
            tab = 'tab3'
        if (request.form.get('multi_toggle4') is not None or request.form.get('dynamic_toggle4') is not None or request.form.get('directed_toggle4') is not None or request.form.get('layout4') is not None):
            multi_toggle4 = bool(request.form.get('multi_toggle4'))
            dynamic_toggle4 = bool(request.form.get('dynamic_toggle4'))
            directed_toggle4 = bool(request.form.get('directed_toggle4'))
            layout4 = request.form.get('layout4')
            df, graph_name4 = plot_violin(networkGraphs, metrics, directed=directed_toggle4, multi=multi_toggle4)
            session['graph_name4'] = graph_name4
            tab = 'tab4'
    else:
        df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
        df, graph_name2 = plot_histogram(networkGraphs, metrics, directed=directed_toggle2, multi=multi_toggle2)
        session['graph_name2'] = graph_name2
        df, graph_name3 = plot_boxplot(networkGraphs, metrics, directed=directed_toggle3, multi=multi_toggle3)
        session['graph_name3'] = graph_name3
        df, graph_name4 = plot_violin(networkGraphs, metrics, directed=directed_toggle4, multi=multi_toggle4)
        session['graph_name4'] = graph_name4
    graph1 = session['graph_name1']
    graph2 = session['graph_name2']
    graph3 = session['graph_name3']
    graph4 = session['graph_name4']
    
    if graph1 == 'no_graph.html':
        graph_path1 = '../static/' + graph1
    else:
        graph_path1 = '../static/uploads/' + filename2 + '/' + graph1

    if graph2 == 'no_graph.html':
        graph_path2 = '../static/' + graph2
    else:
        graph_path2 = '../static/uploads/' + filename2 + '/' + graph2
    
    if graph3 == 'no_graph.html':
        graph_path3 = '../static/' + graph3
    else:
        graph_path3 = '../static/uploads/' + filename2 + '/' + graph3

    if graph4 == 'no_graph.html':
        graph_path4 = '../static/' + graph4
    else:
        graph_path4 = '../static/uploads/' + filename2 + '/' + graph4

    return render_template('node_kcore.html', example=df, tab=tab, 
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, 
    multi_toggle2=multi_toggle2, dynamic_toggle2=dynamic_toggle2, directed_toggle2=directed_toggle2, layout2=layout2, graph2=graph_path2,
    multi_toggle3=multi_toggle3, dynamic_toggle3=dynamic_toggle3, directed_toggle3=directed_toggle3, layout3=layout3, graph3=graph_path3,
    multi_toggle4=multi_toggle4, dynamic_toggle4=dynamic_toggle4, directed_toggle4=directed_toggle4, layout4=layout4, graph4=graph_path4)

@app.route('/node/triangle', endpoint='node_triangle', methods=['GET', 'POST'])
def node_triangle():
    networkGraphs = session['network_graphs']
    filename2 = session['filename2']
    metrics = 'triangles'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    multi_toggle2 = True
    dynamic_toggle2 = False
    directed_toggle2 = False
    layout2 = 'map'
    multi_toggle3 = True
    dynamic_toggle3 = False
    directed_toggle3 = False
    layout3 = 'map'
    multi_toggle4 = True
    dynamic_toggle4 = False
    directed_toggle4 = False
    layout4 = 'map'
    tab = 'tab1'
    
    if request.method == 'POST':
        if (request.form.get('multi_toggle') is not None or request.form.get('dynamic_toggle') is not None or request.form.get('directed_toggle') is not None or request.form.get('layout') is not None):
            multi_toggle = bool(request.form.get('multi_toggle'))
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
            df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle, dynamic=dynamic_toggle, layout=layout)
            session['graph_name1'] = graph_name1
            tab = 'tab1'
        if (request.form.get('multi_toggle2') is not None or request.form.get('dynamic_toggle2') is not None or request.form.get('directed_toggle2') is not None or request.form.get('layout2') is not None):
            multi_toggle2 = bool(request.form.get('multi_toggle2'))
            dynamic_toggle2 = bool(request.form.get('dynamic_toggle2'))
            directed_toggle2 = bool(request.form.get('directed_toggle2'))
            layout2 = request.form.get('layout2')
            df, graph_name2 = plot_histogram(networkGraphs, metrics, directed=directed_toggle2, multi=multi_toggle2)
            session['graph_name2'] = graph_name2
            tab = 'tab2'
        if (request.form.get('multi_toggle3') is not None or request.form.get('dynamic_toggle3') is not None or request.form.get('directed_toggle3') is not None or request.form.get('layout3') is not None):
            multi_toggle3 = bool(request.form.get('multi_toggle3'))
            dynamic_toggle3 = bool(request.form.get('dynamic_toggle3'))
            directed_toggle3 = bool(request.form.get('directed_toggle3'))
            layout3 = request.form.get('layout3')
            df, graph_name3 = plot_boxplot(networkGraphs, metrics, directed=directed_toggle3, multi=multi_toggle3)
            session['graph_name3'] = graph_name3
            tab = 'tab3'
        if (request.form.get('multi_toggle4') is not None or request.form.get('dynamic_toggle4') is not None or request.form.get('directed_toggle4') is not None or request.form.get('layout4') is not None):
            multi_toggle4 = bool(request.form.get('multi_toggle4'))
            dynamic_toggle4 = bool(request.form.get('dynamic_toggle4'))
            directed_toggle4 = bool(request.form.get('directed_toggle4'))
            layout4 = request.form.get('layout4')
            df, graph_name4 = plot_violin(networkGraphs, metrics, directed=directed_toggle4, multi=multi_toggle4)
            session['graph_name4'] = graph_name4
            tab = 'tab4'
    else:
        df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
        df, graph_name2 = plot_histogram(networkGraphs, metrics, directed=directed_toggle2, multi=multi_toggle2)
        session['graph_name2'] = graph_name2
        df, graph_name3 = plot_boxplot(networkGraphs, metrics, directed=directed_toggle3, multi=multi_toggle3)
        session['graph_name3'] = graph_name3
        df, graph_name4 = plot_violin(networkGraphs, metrics, directed=directed_toggle4, multi=multi_toggle4)
        session['graph_name4'] = graph_name4
    graph1 = session['graph_name1']
    graph2 = session['graph_name2']
    graph3 = session['graph_name3']
    graph4 = session['graph_name4']
    
    if graph1 == 'no_graph.html':
        graph_path1 = '../static/' + graph1
    else:
        graph_path1 = '../static/uploads/' + filename2 + '/' + graph1

    if graph2 == 'no_graph.html':
        graph_path2 = '../static/' + graph2
    else:
        graph_path2 = '../static/uploads/' + filename2 + '/' + graph2
    
    if graph3 == 'no_graph.html':
        graph_path3 = '../static/' + graph3
    else:
        graph_path3 = '../static/uploads/' + filename2 + '/' + graph3

    if graph4 == 'no_graph.html':
        graph_path4 = '../static/' + graph4
    else:
        graph_path4 = '../static/uploads/' + filename2 + '/' + graph4

    return render_template('node_triangle.html', example=df, tab=tab, 
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, 
    multi_toggle2=multi_toggle2, dynamic_toggle2=dynamic_toggle2, directed_toggle2=directed_toggle2, layout2=layout2, graph2=graph_path2,
    multi_toggle3=multi_toggle3, dynamic_toggle3=dynamic_toggle3, directed_toggle3=directed_toggle3, layout3=layout3, graph3=graph_path3,
    multi_toggle4=multi_toggle4, dynamic_toggle4=dynamic_toggle4, directed_toggle4=directed_toggle4, layout4=layout4, graph4=graph_path4)

@app.route('/node/pagerank', endpoint='node_pagerank', methods=['GET', 'POST'])
def node_pagerank():
    networkGraphs = session['network_graphs']
    filename2 = session['filename2']
    metrics = 'pagerank'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    multi_toggle2 = True
    dynamic_toggle2 = False
    directed_toggle2 = False
    layout2 = 'map'
    multi_toggle3 = True
    dynamic_toggle3 = False
    directed_toggle3 = False
    layout3 = 'map'
    multi_toggle4 = True
    dynamic_toggle4 = False
    directed_toggle4 = False
    layout4 = 'map'
    tab = 'tab1'
    
    if request.method == 'POST':
        if (request.form.get('multi_toggle') is not None or request.form.get('dynamic_toggle') is not None or request.form.get('directed_toggle') is not None or request.form.get('layout') is not None):
            multi_toggle = bool(request.form.get('multi_toggle'))
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
            df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle, dynamic=dynamic_toggle, layout=layout)
            session['graph_name1'] = graph_name1
            tab = 'tab1'
        if (request.form.get('multi_toggle2') is not None or request.form.get('dynamic_toggle2') is not None or request.form.get('directed_toggle2') is not None or request.form.get('layout2') is not None):
            multi_toggle2 = bool(request.form.get('multi_toggle2'))
            dynamic_toggle2 = bool(request.form.get('dynamic_toggle2'))
            directed_toggle2 = bool(request.form.get('directed_toggle2'))
            layout2 = request.form.get('layout2')
            df, graph_name2 = plot_histogram(networkGraphs, metrics, directed=directed_toggle2, multi=multi_toggle2)
            session['graph_name2'] = graph_name2
            tab = 'tab2'
        if (request.form.get('multi_toggle3') is not None or request.form.get('dynamic_toggle3') is not None or request.form.get('directed_toggle3') is not None or request.form.get('layout3') is not None):
            multi_toggle3 = bool(request.form.get('multi_toggle3'))
            dynamic_toggle3 = bool(request.form.get('dynamic_toggle3'))
            directed_toggle3 = bool(request.form.get('directed_toggle3'))
            layout3 = request.form.get('layout3')
            df, graph_name3 = plot_boxplot(networkGraphs, metrics, directed=directed_toggle3, multi=multi_toggle3)
            session['graph_name3'] = graph_name3
            tab = 'tab3'
        if (request.form.get('multi_toggle4') is not None or request.form.get('dynamic_toggle4') is not None or request.form.get('directed_toggle4') is not None or request.form.get('layout4') is not None):
            multi_toggle4 = bool(request.form.get('multi_toggle4'))
            dynamic_toggle4 = bool(request.form.get('dynamic_toggle4'))
            directed_toggle4 = bool(request.form.get('directed_toggle4'))
            layout4 = request.form.get('layout4')
            df, graph_name4 = plot_violin(networkGraphs, metrics, directed=directed_toggle4, multi=multi_toggle4)
            session['graph_name4'] = graph_name4
            tab = 'tab4'
    else:
        df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
        df, graph_name2 = plot_histogram(networkGraphs, metrics, directed=directed_toggle2, multi=multi_toggle2)
        session['graph_name2'] = graph_name2
        df, graph_name3 = plot_boxplot(networkGraphs, metrics, directed=directed_toggle3, multi=multi_toggle3)
        session['graph_name3'] = graph_name3
        df, graph_name4 = plot_violin(networkGraphs, metrics, directed=directed_toggle4, multi=multi_toggle4)
        session['graph_name4'] = graph_name4
    graph1 = session['graph_name1']
    graph2 = session['graph_name2']
    graph3 = session['graph_name3']
    graph4 = session['graph_name4']
    
    if graph1 == 'no_graph.html':
        graph_path1 = '../static/' + graph1
    else:
        graph_path1 = '../static/uploads/' + filename2 + '/' + graph1

    if graph2 == 'no_graph.html':
        graph_path2 = '../static/' + graph2
    else:
        graph_path2 = '../static/uploads/' + filename2 + '/' + graph2
    
    if graph3 == 'no_graph.html':
        graph_path3 = '../static/' + graph3
    else:
        graph_path3 = '../static/uploads/' + filename2 + '/' + graph3

    if graph4 == 'no_graph.html':
        graph_path4 = '../static/' + graph4
    else:
        graph_path4 = '../static/uploads/' + filename2 + '/' + graph4

    return render_template('node_pagerank.html', example=df, tab=tab, 
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, 
    multi_toggle2=multi_toggle2, dynamic_toggle2=dynamic_toggle2, directed_toggle2=directed_toggle2, layout2=layout2, graph2=graph_path2,
    multi_toggle3=multi_toggle3, dynamic_toggle3=dynamic_toggle3, directed_toggle3=directed_toggle3, layout3=layout3, graph3=graph_path3,
    multi_toggle4=multi_toggle4, dynamic_toggle4=dynamic_toggle4, directed_toggle4=directed_toggle4, layout4=layout4, graph4=graph_path4)

#-------------------------------------------EDGE--------------------------------------------

@app.route('/edge_all', endpoint='edge_all', methods=['GET', 'POST'])
def edge_all():
    networkGraphs = session['network_graphs']

    edge_allDF = cache.get('edge_allDF')
    if edge_allDF is None:
        edge_allDF = compute_load_centrality(networkGraphs, directed=False)
        cache.set('edge_allDF', edge_allDF)
    table_headers = list(edge_allDF.columns.values)
    table_rows = edge_allDF.values.tolist()
    return render_template('edge_all.html', example=edge_allDF)


#-------------------------------------------RESILIENCE_ANALYSIS-----------------------------------

@app.route('/resilience/random', endpoint='resilience_random', methods=['GET', 'POST'])
def resilience_analyisis_random():
    return render_template('resilience_analyisis_random.html')

#-------------------------------------------MAIN--------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
