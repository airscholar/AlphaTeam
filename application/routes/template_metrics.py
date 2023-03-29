from flask import Blueprint, render_template, session, request, redirect, url_for
import csv
import sys
import scipy as sp
from flask_caching import Cache
import matplotlib.pyplot as plt
import re
import time
import shutil
from dictionary.information import *

sys.path.insert(1, '../')
from src.utils import *
from src.NetworkGraphs import *
from src.metrics import *
from src.preprocessing import *
from src.visualisation import *
from flask import g
import html

def process_single_metric(metrics_arg, template_name_arg, method_name_arg, description_key_arg):
    filename2 = session['filename2']
    networkGraphs = get_networkGraph(filename2)
    metrics = metrics_arg
    multi_toggle = True
    dynamic_toggle = False
    directed_toggle = True
    tab = 'tab1'
    if networkGraphs.is_spatial():
        layout = 'map'
    else:
        layout = 'sfdp'

    if request.method == 'POST':
            multi_toggle = bool(request.form.get('multi_toggle'))
            dynamic_toggle = bool(request.form.get('dynamic_toggle'))
            directed_toggle = bool(request.form.get('directed_toggle'))
            layout = request.form.get('layout')
            if layout is None:
                if networkGraphs.is_spatial():
                    layout = 'map'
                else:
                    layout = 'sfdp'
            
            df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle, dynamic=dynamic_toggle, layout=layout)
            session['graph_name1'] = graph_name1
            df, graph_name2 = plot_histogram(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle)
            session['graph_name2'] = graph_name2
            df, graph_name3 = plot_boxplot(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle)
            session['graph_name3'] = graph_name3
            df, graph_name4 = plot_violin(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle)
            session['graph_name4'] = graph_name4
            tab = 'tab1'
    else:
        df, graph_name1 = plot_metric(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle, dynamic=dynamic_toggle, layout=layout)
        session['graph_name1'] = graph_name1
        df, graph_name2 = plot_histogram(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle)
        session['graph_name2'] = graph_name2
        df, graph_name3 = plot_boxplot(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle)
        session['graph_name3'] = graph_name3
        df, graph_name4 = plot_violin(networkGraphs, metrics, directed=directed_toggle, multi=multi_toggle)
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

    return render_template(template_name_arg, example=df, tab=tab, method_name=method_name_arg,
        description = description[description_key_arg],
    multi_toggle=multi_toggle, dynamic_toggle=dynamic_toggle, directed_toggle=directed_toggle, layout=layout, graph1=graph_path1, 
    graph2=graph_path2,
    graph3=graph_path3,
    graph4=graph_path4)
