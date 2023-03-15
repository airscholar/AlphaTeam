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
        filepath = './uploads/'+filename2
        if os.path.exists(filepath):
            shutil.rmtree(filepath)
        imagepath = app.root_path + '/static/img/' + filename + '.png'
        if os.path.exists(imagepath):
            os.remove(imagepath)
        
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
        filepath = './uploads/'+filename2
        if os.path.exists(filepath):
            shutil.rmtree(filepath)
        imagepath = app.root_path + '/static/img/' + filename + '.png'
        if os.path.exists(imagepath):
            os.remove(imagepath)
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
        destination_dir = './uploads/'+filename2
        # Create the directory if it doesn't exist
        destination_dir = './uploads/'+filename2
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
        destination_dir = './uploads/'+filename2
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
    networkGraphs = NetworkGraphs(filepath, type=option, spatial=True)

    global_metrics = cache.get('global_metrics')
    if global_metrics is None:
        global_metrics = compute_global_metrics(networkGraphs)
        cache.set('global_metrics', global_metrics)
    table_headers = list(global_metrics.columns.values)
    table_rows = global_metrics.values.tolist()
    
    # Pass the data to the HTML template
    return render_template('home.html', data=networkGraphs.df, global_metrics=global_metrics)

    #return render_template('home.html', data=networkGraphs.df, table_headers=table_headers, table_rows=table_rows)

#-------------------------------------------VISUALISATION-----------------------------------

@app.route('/visualise/static', endpoint='my_static')
def static():
    filename = session['filename']
    obj = static_visualisation(networkGraphs, "My Plot", directed=False)
    plot = static_visualisation(networkGraphs, "My Plot", directed=False)
    image_path = 'img/' + filename + '.png'
    if not os.path.exists(app.root_path + '/static/img/' + filename + '.png'):
        plot.savefig(app.root_path + '/static/img/' + filename + '.png', bbox_inches='tight')
    print(image_path)
    return render_template('static_visualisation.html', image_path=image_path)

@app.route('/visualise/dynamic', endpoint='my_dynamic')
def dynamic():
    return render_template('dynamic_visualisation.html')

#-------------------------------------------CENTRALITY--------------------------------------

@app.route('/centrality', endpoint='centrality')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def centrality_all():
    allCentralityDF = cache.get('allCentralityDF')
    if allCentralityDF is None:
        allCentralityDF = compute_node_centralities(networkGraphs, directed=False)
        cache.set('allCentralityDF', allCentralityDF)
    table_headers = list(allCentralityDF.columns.values)
    table_rows = allCentralityDF.values.tolist()
    return render_template('centrality_all.html', table_headers=table_headers, table_rows=table_rows)

@app.route('/centrality/degree', endpoint='degree')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def centrality_degree():
    centrality_degreeDF = cache.get('centrality_degreeDF')
    if centrality_degreeDF is None:
        centrality_degreeDF = compute_degree_centrality(networkGraphs, directed=False)
        cache.set('centrality_degreeDF', centrality_degreeDF)
    table_headers = list(centrality_degreeDF.columns.values)
    table_rows = centrality_degreeDF.values.tolist()
    return render_template('centrality_degree.html', table_headers=table_headers, table_rows=table_rows)

@app.route('/centrality/eigenvector', endpoint='eigenvector')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def centrality_eigenvector():
    centrality_eigenvectorDF = cache.get('centrality_eigenvectorDF')
    if centrality_eigenvectorDF is None:
        centrality_eigenvectorDF = compute_eigen_centrality(networkGraphs, directed=False)
        cache.set('centrality_eigenvectorDF', centrality_eigenvectorDF)
    table_headers = list(centrality_eigenvectorDF.columns.values)
    table_rows = centrality_eigenvectorDF.values.tolist()
    return render_template('centrality_eigenvector.html', table_headers=table_headers, table_rows=table_rows)

@app.route('/centrality/closeness', endpoint='closeness')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def centrality_closeness():
    centrality_closenessDF = cache.get('centrality_closenessDF')
    if centrality_closenessDF is None:
        centrality_closenessDF = compute_closeness_centrality(networkGraphs, directed=False)
        cache.set('centrality_closenessDF', centrality_closenessDF)
    table_headers = list(centrality_closenessDF.columns.values)
    table_rows = centrality_closenessDF.values.tolist()
    return render_template('centrality_closeness.html', table_headers=table_headers, table_rows=table_rows)

@app.route('/centrality/betwenness', endpoint='betwenness')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def centrality_betwenness():
    centrality_betwennessDF = cache.get('centrality_betwennessDF')
    if centrality_betwennessDF is None:
        centrality_betwennessDF = compute_betweeness_centrality(networkGraphs, directed=False)
        cache.set('centrality_betwennessDF', centrality_betwennessDF)
    table_headers = list(centrality_betwennessDF.columns.values)
    table_rows = centrality_betwennessDF.values.tolist()
    return render_template('centrality_betwenness.html', table_headers=table_headers, table_rows=table_rows)

@app.route('/centrality/load', endpoint='load')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def centrality_load():
    centrality_loadDF = cache.get('centrality_loadDF')
    if centrality_loadDF is None:
        centrality_loadDF = compute_load_centrality(networkGraphs, directed=False)
        cache.set('centrality_loadDF', centrality_loadDF)
    table_headers = list(centrality_loadDF.columns.values)
    table_rows = centrality_loadDF.values.tolist()
    return render_template('centrality_load.html', table_headers=table_headers, table_rows=table_rows)

#-------------------------------------------NODE--------------------------------------------

@app.route('/node_all', endpoint='node_all')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def node_load():
    node_allDF = cache.get('node_allDF')
    if node_allDF is None:
        node_allDF = compute_node_metrics(networkGraphs, directed=False)
        cache.set('node_allDF', node_allDF)
    table_headers = list(node_allDF.columns.values)
    table_rows = node_allDF.values.tolist()
    return render_template('node_all.html', table_headers=table_headers, table_rows=table_rows)

@app.route('/node/degree', endpoint='node_degree')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def node_degree():
    node_degreeDF = cache.get('node_degreeDF')
    if node_degreeDF is None:
        node_degreeDF = compute_nodes_degree(networkGraphs, directed=False)
        cache.set('node_degreeDF', node_degreeDF)
    table_headers = list(node_degreeDF.columns.values)
    table_rows = node_degreeDF.values.tolist()
    return render_template('node_degree.html', table_headers=table_headers, table_rows=table_rows)

@app.route('/node/kcore', endpoint='node_kcore')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def node_kcore():
    node_kcoreDF = cache.get('node_kcoreDF')
    if node_kcoreDF is None:
        node_kcoreDF = compute_kcore(networkGraphs, directed=False)
        cache.set('node_kcoreDF', node_kcoreDF)
    table_headers = list(node_kcoreDF.columns.values)
    table_rows = node_kcoreDF.values.tolist()
    return render_template('node_kcore.html', table_headers=table_headers, table_rows=table_rows)

@app.route('/node/triangle', endpoint='node_triangle')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def node_triangle():
    node_triangleDF = cache.get('node_triangleDF')
    if node_triangleDF is None:
        node_triangleDF = compute_triangles(networkGraphs, directed=False)
        cache.set('node_triangleDF', node_triangleDF)
    table_headers = list(node_triangleDF.columns.values)
    table_rows = node_triangleDF.values.tolist()
    return render_template('node_triangle.html', table_headers=table_headers, table_rows=table_rows)

@app.route('/node/pagerank', endpoint='node_pagerank')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def node_pagerank():
    node_pagerankDF = cache.get('node_pagerankDF')
    if node_pagerankDF is None:
        node_pagerankDF = compute_page_rank(networkGraphs, directed=False)
        cache.set('node_pagerankDF', node_pagerankDF)
    table_headers = list(node_pagerankDF.columns.values)
    table_rows = node_pagerankDF.values.tolist()
    return render_template('node_pagerank.html', table_headers=table_headers, table_rows=table_rows)

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
    return render_template('edge_all.html', table_headers=table_headers, table_rows=table_rows)

#-------------------------------------------ML-CLUSTERING-----------------------------------

@app.route('/clustering/louvanian', endpoint='clustering_louvanian')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def clustering_louvanian():
    clustering_louvanianDF = cache.get('clustering_louvanianDF')
    if clustering_louvanianDF is None:
        clustering_louvanianDF = compute_load_centrality(networkGraphs, directed=False)
        cache.set('clustering_louvanianDF', clustering_louvanianDF)
    table_headers = list(clustering_louvanianDF.columns.values)
    table_rows = clustering_louvanianDF.values.tolist()
    return render_template('clustering_louvanian.html', table_headers=table_headers, table_rows=table_rows)

#-------------------------------------------MAIN--------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
