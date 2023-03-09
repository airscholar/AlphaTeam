from flask import render_template, request
from jinja2 import TemplateNotFound

from application.home import blueprint
from src.NetworkGraphs import *

filename = './datasets/Railway.csv'
cols = ['train', 'st_no', 'st_id', 'date', 'arr_time', 'dep_time', 'stay_time', 'mileage', 'lat', 'lon']
df = pd.read_csv(filename, names=cols, header=None)

networkGraphs = NetworkGraphs(filename, type="RAILWAY", spatial=True)


@blueprint.route('/')
def home():
    return render_template('home/upload.html', segment='upload')


@blueprint.route('/index')
def index():
    global_metrics = compute_global_metrics(networkGraphs)
    return render_template('home/index.html',
                           metrics_table=
                           global_metrics.to_html(classes='table', table_id="datatablesSimple", header="true"),
                           datasetDf=df[:100].to_html(classes='table', table_id="datasetSimple", header="true"),
                           segment='index')


@blueprint.route('/all_centrality')
def all_centrality():
    allCentralityDF = compute_node_metrics(networkGraphs, directed=False)
    return render_template('home/all_centrality.html',
                           datasetDf=allCentralityDF.to_html(classes='table', table_id="datatablesSimple",
                                                             header="true"),
                           segment='all_centrality')


@blueprint.route('/<template>')
def route_template(template):
    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):
    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
