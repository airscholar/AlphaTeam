import sys

from flask import Blueprint, render_template, session, request

sys.path.insert(1, '../')
from src.metrics import *
from src.visualisation import *

centrality_routes = Blueprint('centrality_routes', __name__)


# -------------------------------------------CENTRALITY--------------------------------------
@centrality_routes.route('/centrality', endpoint='centrality', methods=['GET', 'POST'])
def centrality_all():
    """
    :Function: Visualise the centrality metrics
    :return: the centrality page
    """
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    metrics = 'centralities'
    multi_toggle = True
    directed_toggle = False
    multi_toggle2 = True
    directed_toggle2 = False
    multi_toggle3 = True
    directed_toggle3 = False
    multi_toggle4 = True
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
        if (request.form.get('multi_toggle') is not None or request.form.get(
                'directed_toggle') is not None or request.form.get('layout') is not None):
            multi_toggle = bool(request.form.get('multi_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
            df, graph_name1 = plot_all_metrics(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle,
                                               layout=layout)
            session['graph_name1'] = graph_name1
            tab = 'tab1'
        if (request.form.get('multi_toggle2') is not None or request.form.get(
                'directed_toggle2') is not None or request.form.get('layout2') is not None):
            multi_toggle2 = bool(request.form.get('multi_toggle2'))
            directed_toggle2 = bool(request.form.get('directed_toggle2'))
            layout2 = request.form.get('layout2')
            df, graph_name2 = plot_histogram(networkGraphs, metrics, directed=directed_toggle2, multi=multi_toggle2)
            session['graph_name2'] = graph_name2
            tab = 'tab2'
        if (request.form.get('multi_toggle3') is not None or request.form.get(
                'directed_toggle3') is not None or request.form.get('layout3') is not None):
            multi_toggle3 = bool(request.form.get('multi_toggle3'))
            directed_toggle3 = bool(request.form.get('directed_toggle3'))
            layout3 = request.form.get('layout3')
            df, graph_name3 = plot_boxplot(networkGraphs, metrics, directed=directed_toggle3, multi=multi_toggle3)
            session['graph_name3'] = graph_name3
            tab = 'tab3'
        if (request.form.get('multi_toggle4') is not None or request.form.get(
                'directed_toggle4') is not None or request.form.get('layout4') is not None):
            multi_toggle4 = bool(request.form.get('multi_toggle4'))
            directed_toggle4 = bool(request.form.get('directed_toggle4'))
            layout4 = request.form.get('layout4')
            df, graph_name4 = plot_violin(networkGraphs, metrics, directed=directed_toggle4, multi=multi_toggle4)
            session['graph_name4'] = graph_name4
            tab = 'tab4'
    else:
        df, graph_name1 = plot_all_metrics(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle,
                                           layout=layout)
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

    return render_template('centrality/centrality_all.html', example=df, tab=tab, method_name='All Centrality',
                           multi_toggle=multi_toggle, directed_toggle=directed_toggle, layout=layout,
                           graph1=graph_path1,
                           multi_toggle2=multi_toggle2, directed_toggle2=directed_toggle2, layout2=layout2,
                           graph2=graph_path2,
                           multi_toggle3=multi_toggle3, directed_toggle3=directed_toggle3, layout3=layout3,
                           graph3=graph_path3,
                           multi_toggle4=multi_toggle4, directed_toggle4=directed_toggle4, layout4=layout4,
                           graph4=graph_path4)


@centrality_routes.route('/centrality/degree', endpoint='degree', methods=['GET', 'POST'])
def centrality_degree():
    """
    :Function: Degree centrality page
    :return: degree centrality page
    """
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    metrics = 'degree_centrality'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = True
    multi_toggle2 = True
    dynamic_toggle2 = False
    directed_toggle2 = True
    multi_toggle3 = True
    dynamic_toggle3 = False
    directed_toggle3 = True
    multi_toggle4 = True
    dynamic_toggle4 = False
    directed_toggle4 = True
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
        if (request.form.get('multi_toggle') is not None or request.form.get(
                'dynamic_toggle') is not None or request.form.get('directed_toggle') is not None or request.form.get(
            'layout') is not None):
            multi_toggle = bool(request.form.get('multi_toggle'))
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
            df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle,
                                          dynamic=dynamic_toggle, layout=layout)
            session['graph_name1'] = graph_name1
            tab = 'tab1'
        if (request.form.get('multi_toggle2') is not None or request.form.get(
                'dynamic_toggle2') is not None or request.form.get('directed_toggle2') is not None or request.form.get(
            'layout2') is not None):
            multi_toggle2 = bool(request.form.get('multi_toggle2'))
            dynamic_toggle2 = bool(request.form.get('dynamic_toggle2'))
            directed_toggle2 = bool(request.form.get('directed_toggle2'))
            layout2 = request.form.get('layout2')
            df, graph_name2 = plot_histogram(networkGraphs, metrics, directed=directed_toggle2, multi=multi_toggle2)
            session['graph_name2'] = graph_name2
            tab = 'tab2'
        if (request.form.get('multi_toggle3') is not None or request.form.get(
                'dynamic_toggle3') is not None or request.form.get('directed_toggle3') is not None or request.form.get(
            'layout3') is not None):
            multi_toggle3 = bool(request.form.get('multi_toggle3'))
            dynamic_toggle3 = bool(request.form.get('dynamic_toggle3'))
            directed_toggle3 = bool(request.form.get('directed_toggle3'))
            layout3 = request.form.get('layout3')
            df, graph_name3 = plot_boxplot(networkGraphs, metrics, directed=directed_toggle3, multi=multi_toggle3)
            session['graph_name3'] = graph_name3
            tab = 'tab3'
        if (request.form.get('multi_toggle4') is not None or request.form.get(
                'dynamic_toggle4') is not None or request.form.get('directed_toggle4') is not None or request.form.get(
            'layout4') is not None):
            multi_toggle4 = bool(request.form.get('multi_toggle4'))
            dynamic_toggle4 = bool(request.form.get('dynamic_toggle4'))
            directed_toggle4 = bool(request.form.get('directed_toggle4'))
            layout4 = request.form.get('layout4')
            df, graph_name4 = plot_violin(networkGraphs, metrics, directed=directed_toggle4, multi=multi_toggle4)
            session['graph_name4'] = graph_name4
            tab = 'tab4'
    else:
        df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle,
                                      dynamic=dynamic_toggle, layout=layout)
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

    return render_template('centrality/centrality_degree.html', example=df, tab=tab, method_name='Degree Centrality',
                           multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle,
                           layout=layout, graph1=graph_path1,
                           multi_toggle2=multi_toggle2, dynamic_toggle2=dynamic_toggle2,
                           directed_toggle2=directed_toggle2, layout2=layout2, graph2=graph_path2,
                           multi_toggle3=multi_toggle3, dynamic_toggle3=dynamic_toggle3,
                           directed_toggle3=directed_toggle3, layout3=layout3, graph3=graph_path3,
                           multi_toggle4=multi_toggle4, dynamic_toggle4=dynamic_toggle4,
                           directed_toggle4=directed_toggle4, layout4=layout4, graph4=graph_path4)


@centrality_routes.route('/centrality/eigenvector', endpoint='eigenvector', methods=['GET', 'POST'])
def centrality_eigenvector():
    """
    :Function: Visualisae Eigenvector Centrality
    :return: Eigenvector Centrality plot page
    """
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    metrics = 'eigenvector_centrality'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = True
    multi_toggle2 = True
    dynamic_toggle2 = False
    directed_toggle2 = True
    multi_toggle3 = True
    dynamic_toggle3 = False
    directed_toggle3 = True
    multi_toggle4 = True
    dynamic_toggle4 = False
    directed_toggle4 = True
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
        if (request.form.get('multi_toggle') is not None or request.form.get(
                'dynamic_toggle') is not None or request.form.get('directed_toggle') is not None or request.form.get(
            'layout') is not None):
            multi_toggle = bool(request.form.get('multi_toggle'))
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
            df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle,
                                          dynamic=dynamic_toggle, layout=layout)
            session['graph_name1'] = graph_name1
            tab = 'tab1'
        if (request.form.get('multi_toggle2') is not None or request.form.get(
                'dynamic_toggle2') is not None or request.form.get('directed_toggle2') is not None or request.form.get(
            'layout2') is not None):
            multi_toggle2 = bool(request.form.get('multi_toggle2'))
            dynamic_toggle2 = bool(request.form.get('dynamic_toggle2'))
            directed_toggle2 = bool(request.form.get('directed_toggle2'))
            layout2 = request.form.get('layout2')
            df, graph_name2 = plot_histogram(networkGraphs, metrics, directed=directed_toggle2, multi=multi_toggle2)
            session['graph_name2'] = graph_name2
            tab = 'tab2'
        if (request.form.get('multi_toggle3') is not None or request.form.get(
                'dynamic_toggle3') is not None or request.form.get('directed_toggle3') is not None or request.form.get(
            'layout3') is not None):
            multi_toggle3 = bool(request.form.get('multi_toggle3'))
            dynamic_toggle3 = bool(request.form.get('dynamic_toggle3'))
            directed_toggle3 = bool(request.form.get('directed_toggle3'))
            layout3 = request.form.get('layout3')
            df, graph_name3 = plot_boxplot(networkGraphs, metrics, directed=directed_toggle3, multi=multi_toggle3)
            session['graph_name3'] = graph_name3
            tab = 'tab3'
        if (request.form.get('multi_toggle4') is not None or request.form.get(
                'dynamic_toggle4') is not None or request.form.get('directed_toggle4') is not None or request.form.get(
            'layout4') is not None):
            multi_toggle4 = bool(request.form.get('multi_toggle4'))
            dynamic_toggle4 = bool(request.form.get('dynamic_toggle4'))
            directed_toggle4 = bool(request.form.get('directed_toggle4'))
            layout4 = request.form.get('layout4')
            df, graph_name4 = plot_violin(networkGraphs, metrics, directed=directed_toggle4, multi=multi_toggle4)
            session['graph_name4'] = graph_name4
            tab = 'tab4'
    else:
        df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle,
                                      dynamic=dynamic_toggle, layout=layout)
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

    return render_template('centrality/centrality_eigenvector.html', example=df, tab=tab,
                           method_name='Eigenvector Centrality',
                           multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle,
                           layout=layout, graph1=graph_path1,
                           multi_toggle2=multi_toggle2, dynamic_toggle2=dynamic_toggle2,
                           directed_toggle2=directed_toggle2, layout2=layout2, graph2=graph_path2,
                           multi_toggle3=multi_toggle3, dynamic_toggle3=dynamic_toggle3,
                           directed_toggle3=directed_toggle3, layout3=layout3, graph3=graph_path3,
                           multi_toggle4=multi_toggle4, dynamic_toggle4=dynamic_toggle4,
                           directed_toggle4=directed_toggle4, layout4=layout4, graph4=graph_path4)


@centrality_routes.route('/centrality/closeness', endpoint='closeness', methods=['GET', 'POST'])
def centrality_closeness():
    """
    :Function: visualise closeness centrality
    :return: closeness centrality page
    """
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    metrics = 'closeness_centrality'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = True
    multi_toggle2 = True
    dynamic_toggle2 = False
    directed_toggle2 = True
    multi_toggle3 = True
    dynamic_toggle3 = False
    directed_toggle3 = True
    multi_toggle4 = True
    dynamic_toggle4 = False
    directed_toggle4 = True
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
        if (request.form.get('multi_toggle') is not None or request.form.get(
                'dynamic_toggle') is not None or request.form.get('directed_toggle') is not None or request.form.get(
            'layout') is not None):
            multi_toggle = bool(request.form.get('multi_toggle'))
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
            df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle,
                                          dynamic=dynamic_toggle, layout=layout)
            session['graph_name1'] = graph_name1
            tab = 'tab1'
        if (request.form.get('multi_toggle2') is not None or request.form.get(
                'dynamic_toggle2') is not None or request.form.get('directed_toggle2') is not None or request.form.get(
            'layout2') is not None):
            multi_toggle2 = bool(request.form.get('multi_toggle2'))
            dynamic_toggle2 = bool(request.form.get('dynamic_toggle2'))
            directed_toggle2 = bool(request.form.get('directed_toggle2'))
            layout2 = request.form.get('layout2')
            df, graph_name2 = plot_histogram(networkGraphs, metrics, directed=directed_toggle2, multi=multi_toggle2)
            session['graph_name2'] = graph_name2
            tab = 'tab2'
        if (request.form.get('multi_toggle3') is not None or request.form.get(
                'dynamic_toggle3') is not None or request.form.get('directed_toggle3') is not None or request.form.get(
            'layout3') is not None):
            multi_toggle3 = bool(request.form.get('multi_toggle3'))
            dynamic_toggle3 = bool(request.form.get('dynamic_toggle3'))
            directed_toggle3 = bool(request.form.get('directed_toggle3'))
            layout3 = request.form.get('layout3')
            df, graph_name3 = plot_boxplot(networkGraphs, metrics, directed=directed_toggle3, multi=multi_toggle3)
            session['graph_name3'] = graph_name3
            tab = 'tab3'
        if (request.form.get('multi_toggle4') is not None or request.form.get(
                'dynamic_toggle4') is not None or request.form.get('directed_toggle4') is not None or request.form.get(
            'layout4') is not None):
            multi_toggle4 = bool(request.form.get('multi_toggle4'))
            dynamic_toggle4 = bool(request.form.get('dynamic_toggle4'))
            directed_toggle4 = bool(request.form.get('directed_toggle4'))
            layout4 = request.form.get('layout4')
            df, graph_name4 = plot_violin(networkGraphs, metrics, directed=directed_toggle4, multi=multi_toggle4)
            session['graph_name4'] = graph_name4
            tab = 'tab4'
    else:
        df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle,
                                      dynamic=dynamic_toggle, layout=layout)
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

    return render_template('centrality/centrality_closeness.html', example=df, tab=tab,
                           method_name='Closeness Centrality',
                           multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle,
                           layout=layout, graph1=graph_path1,
                           multi_toggle2=multi_toggle2, dynamic_toggle2=dynamic_toggle2,
                           directed_toggle2=directed_toggle2, layout2=layout2, graph2=graph_path2,
                           multi_toggle3=multi_toggle3, dynamic_toggle3=dynamic_toggle3,
                           directed_toggle3=directed_toggle3, layout3=layout3, graph3=graph_path3,
                           multi_toggle4=multi_toggle4, dynamic_toggle4=dynamic_toggle4,
                           directed_toggle4=directed_toggle4, layout4=layout4, graph4=graph_path4)


@centrality_routes.route('/centrality/betwenness', endpoint='betwenness', methods=['GET', 'POST'])
def centrality_betwenness():
    """
    :Function: Visualization of the betwenness centrality
    :return: betwenness centrality page
    """
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    metrics = 'betweenness_centrality'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = True
    multi_toggle2 = True
    dynamic_toggle2 = False
    directed_toggle2 = True
    multi_toggle3 = True
    dynamic_toggle3 = False
    directed_toggle3 = True
    multi_toggle4 = True
    dynamic_toggle4 = False
    directed_toggle4 = True
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
        if (request.form.get('multi_toggle') is not None or request.form.get(
                'dynamic_toggle') is not None or request.form.get('directed_toggle') is not None or request.form.get(
            'layout') is not None):
            multi_toggle = bool(request.form.get('multi_toggle'))
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
            df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle,
                                          dynamic=dynamic_toggle, layout=layout)
            session['graph_name1'] = graph_name1
            tab = 'tab1'
        if (request.form.get('multi_toggle2') is not None or request.form.get(
                'dynamic_toggle2') is not None or request.form.get('directed_toggle2') is not None or request.form.get(
            'layout2') is not None):
            multi_toggle2 = bool(request.form.get('multi_toggle2'))
            dynamic_toggle2 = bool(request.form.get('dynamic_toggle2'))
            directed_toggle2 = bool(request.form.get('directed_toggle2'))
            layout2 = request.form.get('layout2')
            df, graph_name2 = plot_histogram(networkGraphs, metrics, directed=directed_toggle2, multi=multi_toggle2)
            session['graph_name2'] = graph_name2
            tab = 'tab2'
        if (request.form.get('multi_toggle3') is not None or request.form.get(
                'dynamic_toggle3') is not None or request.form.get('directed_toggle3') is not None or request.form.get(
            'layout3') is not None):
            multi_toggle3 = bool(request.form.get('multi_toggle3'))
            dynamic_toggle3 = bool(request.form.get('dynamic_toggle3'))
            directed_toggle3 = bool(request.form.get('directed_toggle3'))
            layout3 = request.form.get('layout3')
            df, graph_name3 = plot_boxplot(networkGraphs, metrics, directed=directed_toggle3, multi=multi_toggle3)
            session['graph_name3'] = graph_name3
            tab = 'tab3'
        if (request.form.get('multi_toggle4') is not None or request.form.get(
                'dynamic_toggle4') is not None or request.form.get('directed_toggle4') is not None or request.form.get(
            'layout4') is not None):
            multi_toggle4 = bool(request.form.get('multi_toggle4'))
            dynamic_toggle4 = bool(request.form.get('dynamic_toggle4'))
            directed_toggle4 = bool(request.form.get('directed_toggle4'))
            layout4 = request.form.get('layout4')
            df, graph_name4 = plot_violin(networkGraphs, metrics, directed=directed_toggle4, multi=multi_toggle4)
            session['graph_name4'] = graph_name4
            tab = 'tab4'
    else:
        df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle,
                                      dynamic=dynamic_toggle, layout=layout)
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

    return render_template('centrality/centrality_betwenness.html', example=df, tab=tab,
                           method_name='Betwenness Centrality',
                           multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle,
                           layout=layout, graph1=graph_path1,
                           multi_toggle2=multi_toggle2, dynamic_toggle2=dynamic_toggle2,
                           directed_toggle2=directed_toggle2, layout2=layout2, graph2=graph_path2,
                           multi_toggle3=multi_toggle3, dynamic_toggle3=dynamic_toggle3,
                           directed_toggle3=directed_toggle3, layout3=layout3, graph3=graph_path3,
                           multi_toggle4=multi_toggle4, dynamic_toggle4=dynamic_toggle4,
                           directed_toggle4=directed_toggle4, layout4=layout4, graph4=graph_path4)


@centrality_routes.route('/centrality/load', endpoint='load', methods=['GET', 'POST'])
def centrality_load():
    """
    :Function: Visualize the load centrality of the network
    :return:
    """
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    metrics = 'load_centrality'
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = True
    multi_toggle2 = True
    dynamic_toggle2 = False
    directed_toggle2 = True
    multi_toggle3 = True
    dynamic_toggle3 = False
    directed_toggle3 = True
    multi_toggle4 = True
    dynamic_toggle4 = False
    directed_toggle4 = True
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
        if (request.form.get('multi_toggle') is not None or request.form.get(
                'dynamic_toggle') is not None or request.form.get('directed_toggle') is not None or request.form.get(
            'layout') is not None):
            multi_toggle = bool(request.form.get('multi_toggle'))
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
            df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle,
                                          dynamic=dynamic_toggle, layout=layout)
            session['graph_name1'] = graph_name1
            tab = 'tab1'
        if (request.form.get('multi_toggle2') is not None or request.form.get(
                'dynamic_toggle2') is not None or request.form.get('directed_toggle2') is not None or request.form.get(
            'layout2') is not None):
            multi_toggle2 = bool(request.form.get('multi_toggle2'))
            dynamic_toggle2 = bool(request.form.get('dynamic_toggle2'))
            directed_toggle2 = bool(request.form.get('directed_toggle2'))
            layout2 = request.form.get('layout2')
            df, graph_name2 = plot_histogram(networkGraphs, metrics, directed=directed_toggle2, multi=multi_toggle2)
            session['graph_name2'] = graph_name2
            tab = 'tab2'
        if (request.form.get('multi_toggle3') is not None or request.form.get(
                'dynamic_toggle3') is not None or request.form.get('directed_toggle3') is not None or request.form.get(
            'layout3') is not None):
            multi_toggle3 = bool(request.form.get('multi_toggle3'))
            dynamic_toggle3 = bool(request.form.get('dynamic_toggle3'))
            directed_toggle3 = bool(request.form.get('directed_toggle3'))
            layout3 = request.form.get('layout3')
            df, graph_name3 = plot_boxplot(networkGraphs, metrics, directed=directed_toggle3, multi=multi_toggle3)
            session['graph_name3'] = graph_name3
            tab = 'tab3'
        if (request.form.get('multi_toggle4') is not None or request.form.get(
                'dynamic_toggle4') is not None or request.form.get('directed_toggle4') is not None or request.form.get(
            'layout4') is not None):
            multi_toggle4 = bool(request.form.get('multi_toggle4'))
            dynamic_toggle4 = bool(request.form.get('dynamic_toggle4'))
            directed_toggle4 = bool(request.form.get('directed_toggle4'))
            layout4 = request.form.get('layout4')
            df, graph_name4 = plot_violin(networkGraphs, metrics, directed=directed_toggle4, multi=multi_toggle4)
            session['graph_name4'] = graph_name4
            tab = 'tab4'
    else:
        df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle,
                                      dynamic=dynamic_toggle, layout=layout)
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

    return render_template('centrality/centrality_load.html', example=df, tab=tab, method_name='Load Centrality',
                           multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle,
                           layout=layout, graph1=graph_path1,
                           multi_toggle2=multi_toggle2, dynamic_toggle2=dynamic_toggle2,
                           directed_toggle2=directed_toggle2, layout2=layout2, graph2=graph_path2,
                           multi_toggle3=multi_toggle3, dynamic_toggle3=dynamic_toggle3,
                           directed_toggle3=directed_toggle3, layout3=layout3, graph3=graph_path3,
                           multi_toggle4=multi_toggle4, dynamic_toggle4=dynamic_toggle4,
                           directed_toggle4=directed_toggle4, layout4=layout4, graph4=graph_path4)
