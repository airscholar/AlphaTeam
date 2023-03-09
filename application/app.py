from flask import Flask, request, render_template, redirect, url_for, session
import csv
from src.NetworkGraphs import *
import scipy as sp

app = Flask(__name__)
app.secret_key = 'my-secret-key' # set a secret key for the session

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
def home():
    # Get the filename from the session variable
    filename = session['filename']

    # Open the CSV file and read its contents
    with open('uploads/' + filename, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # skip the header row
        data = [header]  # initialize the data list with the header row
        for i, row in enumerate(reader):
            if i < 50:
                data.append(row)
            else:
                break

    global_metrics = compute_global_metrics(networkGraphs)

    # Pass the data to the HTML template
    return render_template('home.html', data=data,  metrics_table=
                           global_metrics.to_html(classes='table', table_id="datatablesSimple", header="true"),
                           datasetDf=df[:100].to_html(classes='table', table_id="datasetSimple", header="true"))

@app.route('/visualise/static', endpoint='my_static')
def static():
    image_path = '/img/example.png'
    return render_template('static.html', image_path=image_path)

@app.route('/visualise/dynamic', endpoint='my_dynamic')
def dynamic():
    return render_template('dynamic.html')

@app.route('/centrality', endpoint='centrality')
def dynamic():
    allCentralityDF = compute_node_metrics(networkGraphs, directed=False)
    return render_template('centrality.html',  datasetDf=allCentralityDF.to_html(classes='table', table_id="datatablesSimple",
                                                             header="true"))

if __name__ == '__main__':
    app.run(debug=True)
