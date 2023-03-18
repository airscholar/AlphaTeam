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
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    dynamic_toggle2 = False
    directed_toggle2 = False
    layout2 = 'map'
    tab = 'tab1'
    
    if request.method == 'POST':
        if (request.form.get('dynamic_toggle') is not None or request.form.get('directed_toggle') is not None or request.form.get('layout') is not None):
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
            df, graph_name1 = plot_all_metrics(networkGraphs, metrics, directed=directed_toggle, layout=layout)
            session['graph_name1'] = graph_name1
            tab = 'tab1'
        if (request.form.get('dynamic_toggle2') is not None or request.form.get('directed_toggle2') is not None or request.form.get('layout2') is not None):
            dynamic_toggle2 = bool(request.form.get('dynamic_toggle2'))
            directed_toggle2 = bool(request.form.get('directed_toggle2'))
            layout2 = request.form.get('layout2')
            df, graph_name2 = plot_all_metrics(networkGraphs, metrics, directed=directed_toggle2, layout=layout2)
            session['graph_name2'] = graph_name2
            tab = 'tab2'
    else:
        df, graph_name1 = plot_all_metrics(networkGraphs, metrics, directed=directed_toggle, layout=layout)
        session['graph_name1'] = graph_name1
        df, graph_name2 = plot_all_metrics(networkGraphs, metrics, directed=directed_toggle2, layout=layout2)
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

    return render_template('centrality_all.html', example=df, tab=tab,
    dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, 
    dynamic_toggle2=dynamic_toggle2, directed_toggle2=directed_toggle2, layout2=layout2, graph2=graph_path2)

@app.route('/centrality/degree', endpoint='degree', methods=['GET', 'POST'])
def centrality_degree():
    filename2 = session['filename2']
    multi = True
    metrics = 'degree_centrality'
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    dynamic_toggle2 = False
    directed_toggle2 = False
    layout2 = 'map'
    tab = 'tab1'
    
    if request.method == 'POST':
        if (request.form.get('dynamic_toggle') is not None or request.form.get('directed_toggle') is not None or request.form.get('layout') is not None):
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
            df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi, dynamic=dynamic_toggle, layout=layout)
            session['graph_name1'] = graph_name1
            tab = 'tab1'
        if (request.form.get('dynamic_toggle2') is not None or request.form.get('directed_toggle2') is not None or request.form.get('layout2') is not None):
            dynamic_toggle2 = bool(request.form.get('dynamic_toggle2'))
            directed_toggle2 = bool(request.form.get('directed_toggle2'))
            layout2 = request.form.get('layout2')
            df, graph_name2 = plot_metric(networkGraphs, metrics, directed=directed_toggle2, multi=multi, dynamic=dynamic_toggle2, layout=layout2)
            session['graph_name2'] = graph_name2
            tab = 'tab2'
    else:
        df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
        df, graph_name2 = plot_metric(networkGraphs, metrics, directed=directed_toggle2, multi=multi, dynamic=dynamic_toggle2, layout=layout2)
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

    return render_template('centrality_degree.html', example=df, tab=tab,
    dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, 
    dynamic_toggle2=dynamic_toggle2, directed_toggle2=directed_toggle2, layout2=layout2, graph2=graph_path2)

@app.route('/centrality/eigenvector', endpoint='eigenvector', methods=['GET', 'POST'])
def centrality_eigenvector():
    filename2 = session['filename2']
    multi = True
    metrics = 'eigenvector_centrality'
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    dynamic_toggle2 = False
    directed_toggle2 = False
    layout2 = 'map'
    tab = 'tab1'
    
    if request.method == 'POST':
        if (request.form.get('dynamic_toggle') is not None or request.form.get('directed_toggle') is not None or request.form.get('layout') is not None):
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
            df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi, dynamic=dynamic_toggle, layout=layout)
            session['graph_name1'] = graph_name1
            tab = 'tab1'
        if (request.form.get('dynamic_toggle2') is not None or request.form.get('directed_toggle2') is not None or request.form.get('layout2') is not None):
            dynamic_toggle2 = bool(request.form.get('dynamic_toggle2'))
            directed_toggle2 = bool(request.form.get('directed_toggle2'))
            layout2 = request.form.get('layout2')
            df, graph_name2 = plot_metric(networkGraphs, metrics, directed=directed_toggle2, multi=multi, dynamic=dynamic_toggle2, layout=layout2)
            session['graph_name2'] = graph_name2
            tab = 'tab2'
    else:
        df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
        df, graph_name2 = plot_metric(networkGraphs, metrics, directed=directed_toggle2, multi=multi, dynamic=dynamic_toggle2, layout=layout2)
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

    return render_template('centrality_eigenvector.html', example=df, tab=tab,
    dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, 
    dynamic_toggle2=dynamic_toggle2, directed_toggle2=directed_toggle2, layout2=layout2, graph2=graph_path2)

@app.route('/centrality/closeness', endpoint='closeness', methods=['GET', 'POST'])
def centrality_closeness():
    filename2 = session['filename2']
    multi = True
    metrics = 'closeness_centrality'
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    dynamic_toggle2 = False
    directed_toggle2 = False
    layout2 = 'map'
    tab = 'tab1'
    
    if request.method == 'POST':
        if (request.form.get('dynamic_toggle') is not None or request.form.get('directed_toggle') is not None or request.form.get('layout') is not None):
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
            df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi, dynamic=dynamic_toggle, layout=layout)
            session['graph_name1'] = graph_name1
            tab = 'tab1'
        if (request.form.get('dynamic_toggle2') is not None or request.form.get('directed_toggle2') is not None or request.form.get('layout2') is not None):
            dynamic_toggle2 = bool(request.form.get('dynamic_toggle2'))
            directed_toggle2 = bool(request.form.get('directed_toggle2'))
            layout2 = request.form.get('layout2')
            df, graph_name2 = plot_metric(networkGraphs, metrics, directed=directed_toggle2, multi=multi, dynamic=dynamic_toggle2, layout=layout2)
            session['graph_name2'] = graph_name2
            tab = 'tab2'
    else:
        df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
        df, graph_name2 = plot_metric(networkGraphs, metrics, directed=directed_toggle2, multi=multi, dynamic=dynamic_toggle2, layout=layout2)
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

    return render_template('centrality_closeness.html', example=df, tab=tab,
    dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, 
    dynamic_toggle2=dynamic_toggle2, directed_toggle2=directed_toggle2, layout2=layout2, graph2=graph_path2)


@app.route('/centrality/betwenness', endpoint='betwenness', methods=['GET', 'POST'])
def centrality_betwenness():
    filename2 = session['filename2']
    multi = True
    metrics = 'betweenness_centrality'
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    dynamic_toggle2 = False
    directed_toggle2 = False
    layout2 = 'map'
    tab = 'tab1'
    
    if request.method == 'POST':
        if (request.form.get('dynamic_toggle') is not None or request.form.get('directed_toggle') is not None or request.form.get('layout') is not None):
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
            df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi, dynamic=dynamic_toggle, layout=layout)
            session['graph_name1'] = graph_name1
            tab = 'tab1'
        if (request.form.get('dynamic_toggle2') is not None or request.form.get('directed_toggle2') is not None or request.form.get('layout2') is not None):
            dynamic_toggle2 = bool(request.form.get('dynamic_toggle2'))
            directed_toggle2 = bool(request.form.get('directed_toggle2'))
            layout2 = request.form.get('layout2')
            df, graph_name2 = plot_metric(networkGraphs, metrics, directed=directed_toggle2, multi=multi, dynamic=dynamic_toggle2, layout=layout2)
            session['graph_name2'] = graph_name2
            tab = 'tab2'
    else:
        df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
        df, graph_name2 = plot_metric(networkGraphs, metrics, directed=directed_toggle2, multi=multi, dynamic=dynamic_toggle2, layout=layout2)
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

    return render_template('centrality_betwenness.html', example=df, tab=tab,
    dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, 
    dynamic_toggle2=dynamic_toggle2, directed_toggle2=directed_toggle2, layout2=layout2, graph2=graph_path2)

@app.route('/centrality/load', endpoint='load', methods=['GET', 'POST'])
def centrality_load():
    filename2 = session['filename2']
    multi = True
    metrics = 'load_centrality'
    dynamic_toggle = False
    directed_toggle = False
    layout = 'map'
    dynamic_toggle2 = False
    directed_toggle2 = False
    layout2 = 'map'
    tab = 'tab1'
    
    if request.method == 'POST':
        if (request.form.get('dynamic_toggle') is not None or request.form.get('directed_toggle') is not None or request.form.get('layout') is not None):
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
            df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi, dynamic=dynamic_toggle, layout=layout)
            session['graph_name1'] = graph_name1
            tab = 'tab1'
        if (request.form.get('dynamic_toggle2') is not None or request.form.get('directed_toggle2') is not None or request.form.get('layout2') is not None):
            dynamic_toggle2 = bool(request.form.get('dynamic_toggle2'))
            directed_toggle2 = bool(request.form.get('directed_toggle2'))
            layout2 = request.form.get('layout2')
            df, graph_name2 = plot_metric(networkGraphs, metrics, directed=directed_toggle2, multi=multi, dynamic=dynamic_toggle2, layout=layout2)
            session['graph_name2'] = graph_name2
            tab = 'tab2'
    else:
        df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
        df, graph_name2 = plot_metric(networkGraphs, metrics, directed=directed_toggle2, multi=multi, dynamic=dynamic_toggle2, layout=layout2)
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

    return render_template('centrality_load.html', example=df, tab=tab,
    dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, 
    dynamic_toggle2=dynamic_toggle2, directed_toggle2=directed_toggle2, layout2=layout2, graph2=graph_path2)

#-------------------------------------------NODE--------------------------------------------

@app.route('/node_all', endpoint='node_all', methods=['GET', 'POST'])
def node_load():
    node_allDF = cache.get('node_allDF')
    if node_allDF is None:
        node_allDF = compute_node_metrics(networkGraphs, directed=False)
        cache.set('node_allDF', node_allDF)
    return render_template('node_all.html', example=node_allDF)

@app.route('/node/degree', endpoint='node_degree', methods=['GET', 'POST'])
@cache.cached(timeout=3600) # Cache the result for 1 hour
def node_degree():
    node_degreeDF = cache.get('node_degreeDF')
    if node_degreeDF is None:
        node_degreeDF = compute_nodes_degree(networkGraphs, directed=False)
        cache.set('node_degreeDF', node_degreeDF)
    return render_template('node_degree.html', example=node_degreeDF)

@app.route('/node/kcore', endpoint='node_kcore', methods=['GET', 'POST'])
@cache.cached(timeout=3600) # Cache the result for 1 hour
def node_kcore():
    node_kcoreDF = cache.get('node_kcoreDF')
    if node_kcoreDF is None:
        node_kcoreDF = compute_kcore(networkGraphs, directed=False)
        cache.set('node_kcoreDF', node_kcoreDF)
    return render_template('node_kcore.html', example=node_kcoreDF)

@app.route('/node/triangle', endpoint='node_triangle', methods=['GET', 'POST'])
@cache.cached(timeout=3600) # Cache the result for 1 hour
def node_triangle():
    node_triangleDF = cache.get('node_triangleDF')
    if node_triangleDF is None:
        node_triangleDF = compute_triangles(networkGraphs, directed=False)
        cache.set('node_triangleDF', node_triangleDF)
    return render_template('node_triangle.html', example=node_triangleDF)

@app.route('/node/pagerank', endpoint='node_pagerank', methods=['GET', 'POST'])
@cache.cached(timeout=3600) # Cache the result for 1 hour
def node_pagerank():
    node_pagerankDF = cache.get('node_pagerankDF')
    if node_pagerankDF is None:
        node_pagerankDF = compute_page_rank(networkGraphs, directed=False)
        cache.set('node_pagerankDF', node_pagerankDF)
    return render_template('node_pagerank.html', example=node_pagerankDF)

#-------------------------------------------EDGE--------------------------------------------

@app.route('/edge_all', endpoint='edge_all', methods=['GET', 'POST'])
@cache.cached(timeout=3600) # Cache the result for 1 hour
def edge_all():
    edge_allDF = cache.get('edge_allDF')
    if edge_allDF is None:
        edge_allDF = compute_load_centrality(networkGraphs, directed=False)
        cache.set('edge_allDF', edge_allDF)
    table_headers = list(edge_allDF.columns.values)
    table_rows = edge_allDF.values.tolist()
    return render_template('edge_all.html', example=edge_allDF)

#-------------------------------------------ML-CLUSTERING-----------------------------------

@app.route('/clustering/louvanian', endpoint='clustering_louvanian', methods=['GET', 'POST'])
@cache.cached(timeout=3600) # Cache the result for 1 hour
def clustering_louvanian():
    clustering_louvanianDF = cache.get('clustering_louvanianDF')
    if clustering_louvanianDF is None:
        clustering_louvanianDF = compute_load_centrality(networkGraphs, directed=False)
        cache.set('clustering_louvanianDF', clustering_louvanianDF)
    return render_template('clustering_louvanian.html', example=clustering_louvanianDF)

#-------------------------------------------MAIN--------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
