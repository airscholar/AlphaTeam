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
    dynamic_toggle2 = True
    directed_toggle2 = True
    layout2 = 'twopi'
    
    if request.method == 'POST':
        if request.form.get('dynamic_toggle') is not None:
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
            df, graph_name1 = plot_all_metrics(networkGraphs, metrics, directed=directed_toggle, layout=layout)
            session['graph_name1'] = graph_name1
        if request.form.get('dynamic_toggle2') is not None:
            dynamic_toggle2 = bool(request.form.get('dynamic_toggle2'))
            directed_toggle2 = bool(request.form.get('directed_toggle2'))
            layout2 = request.form.get('layout2')
            df, graph_name2 = plot_all_metrics(networkGraphs, metrics, directed=directed_toggle2, layout=layout2)
            session['graph_name2'] = graph_name2
    else:
        df, graph_name1 = plot_all_metrics(networkGraphs, metrics, directed=directed_toggle, layout=layout)
        session['graph_name1'] = graph_name1
        df, graph_name2 = plot_all_metrics(networkGraphs, metrics, directed=directed_toggle2, layout=layout2)
        session['graph_name2'] = graph_name2
    graph1 = session['graph_name1']
    graph_path1 = 'static/uploads/'+filename2+'/'+graph1
    graph2 = session['graph_name2']
    graph_path2 = 'static/uploads/'+filename2+'/'+graph_name2

    return render_template('centrality_all.html', example=df, 
    dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, 
    dynamic_toggle2=dynamic_toggle2, directed_toggle2=directed_toggle2, layout2=layout2, graph2=graph_path2)

@app.route('/centrality/degree', endpoint='degree')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def centrality_degree():
    centrality_degreeDF = cache.get('centrality_degreeDF')
    if centrality_degreeDF is None:
        centrality_degreeDF = compute_degree_centrality(networkGraphs, directed=False)
        cache.set('centrality_degreeDF', centrality_degreeDF)
    return render_template('centrality_degree.html', example=centrality_degreeDF)

@app.route('/centrality/eigenvector', endpoint='eigenvector')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def centrality_eigenvector():
    centrality_eigenvectorDF = cache.get('centrality_eigenvectorDF')
    if centrality_eigenvectorDF is None:
        centrality_eigenvectorDF = compute_eigen_centrality(networkGraphs, directed=False)
        cache.set('centrality_eigenvectorDF', centrality_eigenvectorDF)
    return render_template('centrality_eigenvector.html', example=centrality_eigenvectorDF)

@app.route('/centrality/closeness', endpoint='closeness')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def centrality_closeness():
    centrality_closenessDF = cache.get('centrality_closenessDF')
    if centrality_closenessDF is None:
        centrality_closenessDF = compute_closeness_centrality(networkGraphs, directed=False)
        cache.set('centrality_closenessDF', centrality_closenessDF)
    return render_template('centrality_closeness.html', example=centrality_closenessDF)

@app.route('/centrality/betwenness', endpoint='betwenness')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def centrality_betwenness():
    centrality_betwennessDF = cache.get('centrality_betwennessDF')
    if centrality_betwennessDF is None:
        centrality_betwennessDF = compute_betweeness_centrality(networkGraphs, directed=False)
        cache.set('centrality_betwennessDF', centrality_betwennessDF)
    return render_template('centrality_betwenness.html', example=centrality_betwennessDF)

@app.route('/centrality/load', endpoint='load')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def centrality_load():
    centrality_loadDF = cache.get('centrality_loadDF')
    if centrality_loadDF is None:
        centrality_loadDF = compute_load_centrality(networkGraphs, directed=False)
        cache.set('centrality_loadDF', centrality_loadDF)
    return render_template('centrality_load.html', example=centrality_loadDF)

#-------------------------------------------NODE--------------------------------------------

@app.route('/node_all', endpoint='node_all')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def node_load():
    node_allDF = cache.get('node_allDF')
    if node_allDF is None:
        node_allDF = compute_node_metrics(networkGraphs, directed=False)
        cache.set('node_allDF', node_allDF)
    return render_template('node_all.html', example=node_allDF)

@app.route('/node/degree', endpoint='node_degree')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def node_degree():
    node_degreeDF = cache.get('node_degreeDF')
    if node_degreeDF is None:
        node_degreeDF = compute_nodes_degree(networkGraphs, directed=False)
        cache.set('node_degreeDF', node_degreeDF)
    return render_template('node_degree.html', example=node_degreeDF)

@app.route('/node/kcore', endpoint='node_kcore')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def node_kcore():
    node_kcoreDF = cache.get('node_kcoreDF')
    if node_kcoreDF is None:
        node_kcoreDF = compute_kcore(networkGraphs, directed=False)
        cache.set('node_kcoreDF', node_kcoreDF)
    return render_template('node_kcore.html', example=node_kcoreDF)

@app.route('/node/triangle', endpoint='node_triangle')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def node_triangle():
    node_triangleDF = cache.get('node_triangleDF')
    if node_triangleDF is None:
        node_triangleDF = compute_triangles(networkGraphs, directed=False)
        cache.set('node_triangleDF', node_triangleDF)
    return render_template('node_triangle.html', example=node_triangleDF)

@app.route('/node/pagerank', endpoint='node_pagerank')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def node_pagerank():
    node_pagerankDF = cache.get('node_pagerankDF')
    if node_pagerankDF is None:
        node_pagerankDF = compute_page_rank(networkGraphs, directed=False)
        cache.set('node_pagerankDF', node_pagerankDF)
    return render_template('node_pagerank.html', example=node_pagerankDF)

#-------------------------------------------EDGE--------------------------------------------

@app.route('/edge_all', endpoint='edge_all')
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

@app.route('/clustering/louvanian', endpoint='clustering_louvanian')
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
