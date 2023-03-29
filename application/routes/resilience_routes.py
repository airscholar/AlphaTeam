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

resilience_routes = Blueprint('resilience_routes', __name__)

#-------------------------------------------RESILIENCE_ANALYSIS-----------------------------

@resilience_routes.route('/resilience/malicious', endpoint='resilience_malicious', methods=['GET', 'POST'])
def resilience_analyisis_malicious():
    layout = 'degree_centrality'
    layout2 = 'equal_to'
    tab_main = 'tab1'
    
    if request.method == 'POST':
        number_of_levels = request.form.get('number_of_levels', None)
        number_of_levels = int(number_of_levels) if number_of_levels else None
        number_of_threashold = request.form.get('number_of_threashold', None)
        layout2 = request.form.get('layout2')
        number_of_threashold = int(number_of_threashold) if number_of_threashold else None
        layout = request.form.get('layout')
    else:
        number_of_levels = None
        number_of_threashold = None
        session['val1'] = None
        session['val2'] = None

    val1 = session.get('val1', None)
    val2 = session.get('val2', None)
    if val1 != number_of_levels:
        session['val1'] = number_of_levels
        tab_main = 'tab1'
    if val2 != number_of_threashold:
        session['val2'] = number_of_threashold
        tab_main = 'tab2'
 
    return render_template('resilience/resilience_analyisis_malicious.html', tab_main=tab_main, 
    layout=layout, layout2=layout2, number_of_levels=number_of_levels, number_of_threashold=number_of_threashold)

@resilience_routes.route('/resilience/random', endpoint='resilience_random', methods=['GET', 'POST'])
def resilience_analyisis_random():
    tab_main = 'tab1'
    
    if request.method == 'POST':
        number_of_nodes = request.form.get('number_of_nodes', None)
        number_of_nodes = int(number_of_nodes) if number_of_nodes else None
        number_of_edges = request.form.get('number_of_edges', None)
        number_of_edges = int(number_of_edges) if number_of_edges else None
    else:
        number_of_nodes = None
        number_of_edges = None
        session['val1'] = None
        session['val2'] = None

    val1 = session.get('val1', None)
    val2 = session.get('val2', None)
    if val1 != number_of_nodes:
        session['val1'] = number_of_nodes
        tab_main = 'tab1'
    if val2 != number_of_edges:
        session['val2'] = number_of_edges
        tab_main = 'tab2'
 
    return render_template('resilience/resilience_analyisis_random.html', tab_main=tab_main, 
    number_of_nodes=number_of_nodes, number_of_edges=number_of_edges)

@resilience_routes.route('/resilience/cluster', endpoint='resilience_cluster', methods=['GET', 'POST'])
def resilience_analyisis_cluster():
    layout = 'louvain'
    
    if request.method == 'POST':
        number_of_cluster_to_generate = request.form.get('number_of_cluster_to_generate', None)
        number_of_cluster_to_generate = int(number_of_cluster_to_generate) if number_of_cluster_to_generate else None
        cluster_to_attack = request.form.get('cluster_to_attack', None)
        cluster_to_attack = int(cluster_to_attack) if cluster_to_attack else None
        layout = request.form.get('layout')
    else:
        number_of_cluster_to_generate = None
        cluster_to_attack = None
 
    return render_template('resilience/resilience_analyisis_cluster.html', layout=layout, number_of_cluster_to_generate=number_of_cluster_to_generate, cluster_to_attack=cluster_to_attack)
