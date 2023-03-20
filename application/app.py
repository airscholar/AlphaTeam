from flask import Flask, request, render_template, redirect, url_for, session
import csv
import sys
sys.path.insert(1, '../')
from src.NetworkGraphs import *
from src.metrics import *
from src.preprocessing import *
from src.visualisation import *

import scipy as sp
from flask_caching import Cache
import matplotlib.pyplot as plt
import re
import time
import shutil

app = Flask(__name__)
app.secret_key = 'my-secret-key' # set a secret key for the session
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

# Define the global variable
networkGraphs = None

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
    global networkGraphs
    networkGraphs = NetworkGraphs(filepath, session_folder='static/uploads/'+filename2, type=option)

    global_metrics = cache.get('global_metrics')
    if global_metrics is None:
        global_metrics = compute_global_metrics(networkGraphs)
        cache.set('global_metrics', global_metrics)
    
    # Pass the data to the HTML template
    return render_template('home.html', data=networkGraphs.df.head(100), example=global_metrics)

#-------------------------------------------VISUALISATION-----------------------------------

@app.route('/visualise/static', methods=['GET', 'POST'], endpoint='my_static')
def static_visualisation():
    filename = session['filename']
    filename2 = session['filename2']
    dynamic_toggle = False
    directed_toggle = False
    layout = 'option1'

    if request.method == 'POST':
        # Get form data
        dynamic_toggle = bool(request.form.get('dynamic_toggle'))
        directed_toggle = bool(request.form.get('directed_toggle'))
        layout = request.form.get('layout')

        # Update visualization based on form data
        # Example code:
        # if dynamic_toggle:
        #     # Do something for dynamic toggle on
        # else:
        #     # Do something for dynamic toggle off

        # if directed_toggle:
        #     # Do something for directed toggle on
        # else:
        #     # Do something for directed toggle off

        print(layout)
        # if layout == 'map':
        #     # Do something for map layout selected
        # elif layout == 'sfdp':
        #     # Do something for sfdp layout selected
        # elif layout == 'twopi':
        #     # Do something for twopi layout selected
        
    return render_template('static_visualisation.html', dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout)


@app.route('/visualise/dynamic', endpoint='my_dynamic')
def dynamic():
    return render_template('dynamic_visualisation.html')

#-------------------------------------------CENTRALITY--------------------------------------

@app.route('/centrality', endpoint='centrality', methods=['GET', 'POST'])
def centrality_all():
    filename2 = session['filename2']
    metrics = 'centralities'
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
            df, graph_name1 = plot_all_metrics(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle, layout=layout)
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

    return render_template('centrality_all.html', example=df, tab=tab, 
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, 
    multi_toggle2=multi_toggle2, dynamic_toggle2=dynamic_toggle2, directed_toggle2=directed_toggle2, layout2=layout2, graph2=graph_path2,
    multi_toggle3=multi_toggle3, dynamic_toggle3=dynamic_toggle3, directed_toggle3=directed_toggle3, layout3=layout3, graph3=graph_path3,
    multi_toggle4=multi_toggle4, dynamic_toggle4=dynamic_toggle4, directed_toggle4=directed_toggle4, layout4=layout4, graph4=graph_path4)

@app.route('/centrality/degree', endpoint='degree', methods=['GET', 'POST'])
def centrality_degree():
    filename2 = session['filename2']
    metrics = 'degree_centrality'
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

    return render_template('centrality_degree.html', example=df, tab=tab, 
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, 
    multi_toggle2=multi_toggle2, dynamic_toggle2=dynamic_toggle2, directed_toggle2=directed_toggle2, layout2=layout2, graph2=graph_path2,
    multi_toggle3=multi_toggle3, dynamic_toggle3=dynamic_toggle3, directed_toggle3=directed_toggle3, layout3=layout3, graph3=graph_path3,
    multi_toggle4=multi_toggle4, dynamic_toggle4=dynamic_toggle4, directed_toggle4=directed_toggle4, layout4=layout4, graph4=graph_path4)

@app.route('/centrality/eigenvector', endpoint='eigenvector', methods=['GET', 'POST'])
def centrality_eigenvector():
    filename2 = session['filename2']
    metrics = 'eigenvector_centrality'
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

    return render_template('centrality_eigenvector.html', example=df, tab=tab, 
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, 
    multi_toggle2=multi_toggle2, dynamic_toggle2=dynamic_toggle2, directed_toggle2=directed_toggle2, layout2=layout2, graph2=graph_path2,
    multi_toggle3=multi_toggle3, dynamic_toggle3=dynamic_toggle3, directed_toggle3=directed_toggle3, layout3=layout3, graph3=graph_path3,
    multi_toggle4=multi_toggle4, dynamic_toggle4=dynamic_toggle4, directed_toggle4=directed_toggle4, layout4=layout4, graph4=graph_path4)

@app.route('/centrality/closeness', endpoint='closeness', methods=['GET', 'POST'])
def centrality_closeness():
    filename2 = session['filename2']
    metrics = 'closeness_centrality'
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

    return render_template('centrality_closeness.html', example=df, tab=tab, 
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, 
    multi_toggle2=multi_toggle2, dynamic_toggle2=dynamic_toggle2, directed_toggle2=directed_toggle2, layout2=layout2, graph2=graph_path2,
    multi_toggle3=multi_toggle3, dynamic_toggle3=dynamic_toggle3, directed_toggle3=directed_toggle3, layout3=layout3, graph3=graph_path3,
    multi_toggle4=multi_toggle4, dynamic_toggle4=dynamic_toggle4, directed_toggle4=directed_toggle4, layout4=layout4, graph4=graph_path4)

@app.route('/centrality/betwenness', endpoint='betwenness', methods=['GET', 'POST'])
def centrality_betwenness():
    filename2 = session['filename2']
    metrics = 'betweenness_centrality'
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

    return render_template('centrality_betwenness.html', example=df, tab=tab, 
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, 
    multi_toggle2=multi_toggle2, dynamic_toggle2=dynamic_toggle2, directed_toggle2=directed_toggle2, layout2=layout2, graph2=graph_path2,
    multi_toggle3=multi_toggle3, dynamic_toggle3=dynamic_toggle3, directed_toggle3=directed_toggle3, layout3=layout3, graph3=graph_path3,
    multi_toggle4=multi_toggle4, dynamic_toggle4=dynamic_toggle4, directed_toggle4=directed_toggle4, layout4=layout4, graph4=graph_path4)

@app.route('/centrality/load', endpoint='load', methods=['GET', 'POST'])
def centrality_load():
    filename2 = session['filename2']
    metrics = 'load_centrality'
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

    return render_template('centrality_load.html', example=df, tab=tab, 
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, 
    multi_toggle2=multi_toggle2, dynamic_toggle2=dynamic_toggle2, directed_toggle2=directed_toggle2, layout2=layout2, graph2=graph_path2,
    multi_toggle3=multi_toggle3, dynamic_toggle3=dynamic_toggle3, directed_toggle3=directed_toggle3, layout3=layout3, graph3=graph_path3,
    multi_toggle4=multi_toggle4, dynamic_toggle4=dynamic_toggle4, directed_toggle4=directed_toggle4, layout4=layout4, graph4=graph_path4)

#-------------------------------------------NODE--------------------------------------------

@app.route('/node_all', endpoint='node_all', methods=['GET', 'POST'])
def node_all():
    filename2 = session['filename2']
    metrics = 'nodes'
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
            df, graph_name1 = plot_all_metrics(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle, layout=layout)
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

    return render_template('node_all.html', example=df, tab=tab, 
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, 
    multi_toggle2=multi_toggle2, dynamic_toggle2=dynamic_toggle2, directed_toggle2=directed_toggle2, layout2=layout2, graph2=graph_path2,
    multi_toggle3=multi_toggle3, dynamic_toggle3=dynamic_toggle3, directed_toggle3=directed_toggle3, layout3=layout3, graph3=graph_path3,
    multi_toggle4=multi_toggle4, dynamic_toggle4=dynamic_toggle4, directed_toggle4=directed_toggle4, layout4=layout4, graph4=graph_path4)

@app.route('/node/degree', endpoint='node_degree', methods=['GET', 'POST'])
def node_degree():
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
    edge_allDF = cache.get('edge_allDF')
    if edge_allDF is None:
        edge_allDF = compute_load_centrality(networkGraphs, directed=False)
        cache.set('edge_allDF', edge_allDF)
    table_headers = list(edge_allDF.columns.values)
    table_rows = edge_allDF.values.tolist()
    return render_template('edge_all.html', example=edge_allDF)

#-------------------------------------------ML-CLUSTERING-----------------------------------

@app.route('/clustering/louvain', endpoint='clustering_louvanian', methods=['GET', 'POST'])
def clustering_louvanian():
    filename2 = session['filename2']
    clusterType = 'louvain'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    
    if request.method == 'POST':
            multi_toggle = bool(request.form.get('multi_toggle'))
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
            df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
            session['graph_name1'] = graph_name1
    else:
        df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
    graph1 = session['graph_name1']
 
    if graph1 == 'no_graph.html':
        graph_path1 = '../static/' + graph1
    else:
        graph_path1 = '../static/uploads/' + filename2 + '/' + graph1

    return render_template('clustering_louvanian.html', example=df,
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, method_name='Louvain')

@app.route('/clustering/greedy_modularity', endpoint='clustering_greedy_modularity', methods=['GET', 'POST'])
def clustering_greedy_modularity():
    filename2 = session['filename2']
    clusterType = 'greedy_modularity'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    
    if request.method == 'POST':
            multi_toggle = bool(request.form.get('multi_toggle'))
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
            df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
            session['graph_name1'] = graph_name1
    else:
        df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
    graph1 = session['graph_name1']
 
    if graph1 == 'no_graph.html':
        graph_path1 = '../static/' + graph1
    else:
        graph_path1 = '../static/uploads/' + filename2 + '/' + graph1

    return render_template('clustering_greedy_modularity.html', example=df,
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, method_name='Greedy Modularity')

@app.route('/clustering/label_propagation', endpoint='clustering_label_propagation', methods=['GET', 'POST'])
def clustering_label_propagation():
    filename2 = session['filename2']
    clusterType = 'label_propagation'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    
    if request.method == 'POST':
            multi_toggle = bool(request.form.get('multi_toggle'))
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
            df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
            session['graph_name1'] = graph_name1
    else:
        df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
    graph1 = session['graph_name1']
 
    if graph1 == 'no_graph.html':
        graph_path1 = '../static/' + graph1
    else:
        graph_path1 = '../static/uploads/' + filename2 + '/' + graph1

    return render_template('clustering_label_propagation.html', example=df,
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, method_name='Label Propagation')

@app.route('/clustering/asyn_lpa', endpoint='clustering_asyn_lpa', methods=['GET', 'POST'])
def clustering_asyn_lpa():
    filename2 = session['filename2']
    clusterType = 'asyn_lpa'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    
    if request.method == 'POST':
            multi_toggle = bool(request.form.get('multi_toggle'))
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
            df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
            session['graph_name1'] = graph_name1
    else:
        df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
    graph1 = session['graph_name1']
 
    if graph1 == 'no_graph.html':
        graph_path1 = '../static/' + graph1
    else:
        graph_path1 = '../static/uploads/' + filename2 + '/' + graph1

    return render_template('clustering_asyn_lpa.html', example=df,
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, method_name='Asyn Lpa')

@app.route('/clustering/girvan_newman', endpoint='clustering_girvan_newman', methods=['GET', 'POST'])
def clustering_girvan_newman():
    filename2 = session['filename2']
    clusterType = 'girvan_newman'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    
    if request.method == 'POST':
            multi_toggle = bool(request.form.get('multi_toggle'))
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
            df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
            session['graph_name1'] = graph_name1
    else:
        df, graph_name1 = plot_cluster(networkGraphs, clusterType, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
    graph1 = session['graph_name1']
 
    if graph1 == 'no_graph.html':
        graph_path1 = '../static/' + graph1
    else:
        graph_path1 = '../static/uploads/' + filename2 + '/' + graph1

    return render_template('clustering_girvan_newman.html', example=df,
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, method_name='Girvan Newman')

#-------------------------------------------RESILIENCE_ANALYSIS-----------------------------------

@app.route('/resilience/random', endpoint='resilience_random', methods=['GET', 'POST'])
def resilience_analyisis_random():
    return render_template('resilience_analyisis_random.html')



#-------------------------------------------MAIN--------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
