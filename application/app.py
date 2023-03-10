from flask import Flask, request, render_template, redirect, url_for, session
import csv
from src.NetworkGraphs import *
import scipy as sp
from flask_caching import Cache

app = Flask(__name__)
app.secret_key = 'my-secret-key' # set a secret key for the session
cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

filepath = './datasets/Railway.csv'

cols = ['train', 'st_no', 'st_id', 'date', 'arr_time', 'dep_time', 'stay_time', 'mileage', 'lat', 'lon']
df = pd.read_csv(filepath, names=cols, header=None)
networkGraphs = NetworkGraphs(filepath, type="RAILWAY", spatial=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Get the CSV file and the selected option
    csv_file = request.files['csv_file']
    option = request.form['option']

    # Save the CSV file to a folder on the server with a filename based on the selected option and file extension
    if option != 'General':
        filename = option + '.csv'
    else:
        filename = option + '.mtx'

    csv_file.save('uploads/' + filename)
    # Do something with the CSV file and selected option
    # (e.g., process the file data and store it in a database)

    # Store the filename in a session variable
    session['filename'] = filename

    # Redirect the user to the success page
    return redirect(url_for('home'))

@app.route('/home')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def home():
    # Get the filename from the session variable
    filename = session['filename']
    
    global_metrics = cache.get('global_metrics')
    if global_metrics is None:
        global_metrics = compute_global_metrics(networkGraphs)
        cache.set('global_metrics', global_metrics)
    table_headers = list(global_metrics.columns.values)
    table_rows = global_metrics.values.tolist()

    # Open the CSV file and read its contents
    with open('uploads/' + filename, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # skip the header row
        data = [header]  # initialize the data list with the header row
        for i, row in enumerate(reader):
            if i < 100:
                data.append(row)
            else:
                break

    # Pass the data to the HTML template
    return render_template('home.html', data=data, table_headers=table_headers, table_rows=table_rows)

@app.route('/visualise/static', endpoint='my_static')
def static():
    image_path = '/img/example.png'
    return render_template('static.html', image_path=image_path)

@app.route('/visualise/dynamic', endpoint='my_dynamic')
def dynamic():
    return render_template('dynamic.html')

@app.route('/centrality', endpoint='centrality')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def centrality():
    allCentralityDF = cache.get('allCentralityDF')
    if allCentralityDF is None:
        allCentralityDF = compute_node_metrics(networkGraphs, directed=False)
        cache.set('allCentralityDF', allCentralityDF)
    table_headers = list(allCentralityDF.columns.values)
    table_rows = allCentralityDF.values.tolist()
    return render_template('centrality.html', table_headers=table_headers, table_rows=table_rows)

@app.route('/degree', endpoint='degree')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def degree():
    degreeDF = cache.get('degreeDF')
    if degreeDF is None:
        degreeDF = compute_degree_centrality(networkGraphs, directed=False)
        cache.set('degreeDF', degreeDF)
    table_headers = list(degreeDF.columns.values)
    table_rows = degreeDF.values.tolist()
    return render_template('centrality_degree.html', table_headers=table_headers, table_rows=table_rows)

@app.route('/eigenvector', endpoint='eigenvector')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def eigenvector():
    eigenvectorDF = cache.get('eigenvectorDF')
    if eigenvectorDF is None:
        eigenvectorDF = compute_eigen_centrality(networkGraphs, directed=False)
        cache.set('eigenvectorDF', eigenvectorDF)
    table_headers = list(eigenvectorDF.columns.values)
    table_rows = eigenvectorDF.values.tolist()
    return render_template('centrality_eigenvector.html', table_headers=table_headers, table_rows=table_rows)

@app.route('/closeness', endpoint='closeness')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def closeness():
    closenessDF = cache.get('closenessDF')
    if closenessDF is None:
        closenessDF = compute_closeness_centrality(networkGraphs, directed=False)
        cache.set('closenessDF', closenessDF)
    table_headers = list(closenessDF.columns.values)
    table_rows = closenessDF.values.tolist()
    return render_template('centrality_closeness.html', table_headers=table_headers, table_rows=table_rows)

@app.route('/betwenness', endpoint='betwenness')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def betwenness():
    betwennessDF = cache.get('betwennessDF')
    if betwennessDF is None:
        betwennessDF = compute_betweeness_centrality(networkGraphs, directed=False)
        cache.set('betwennessDF', betwennessDF)
    table_headers = list(betwennessDF.columns.values)
    table_rows = betwennessDF.values.tolist()
    return render_template('centrality_betwenness.html', table_headers=table_headers, table_rows=table_rows)

@app.route('/load', endpoint='load')
@cache.cached(timeout=3600) # Cache the result for 1 hour
def load():
    loadDF = cache.get('loadDF')
    if loadDF is None:
        loadDF = compute_load_centrality(networkGraphs, directed=False)
        cache.set('loadDF', loadDF)
    table_headers = list(loadDF.columns.values)
    table_rows = loadDF.values.tolist()
    return render_template('centrality_load.html', table_headers=table_headers, table_rows=table_rows)

if __name__ == '__main__':
    app.run(debug=True)
