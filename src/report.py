"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: Report module contains functions for generating reports
"""

# ----------------------------------------- Imports ----------------------------------------- #


# ----------------------------------------- CONSTANT ----------------------------------------- #

red = "\033[0;91m"
green = "\033[0;92m"
yellow = "\033[0;93m"
blue = "\033[0;94m"


# ----------------------------------------- Functions ----------------------------------------- #

def generate_report(networkGraph):
    """
    Generate a report for the network graph
    :param networkGraph: Network graph
    :return: None
    """
    generate_report_summary(networkGraph)
    generate_report_network(networkGraph)
    generate_report_metrics(networkGraph)
    generate_report_clustering(networkGraph)
    generate_report_resilience(networkGraph)
    return 0


# ---------------------------------------------------------------------------------------- #


def generate_report_summary(networkGraph):
    """
    Generate a summary report for the network graph
    :param networkGraph: Network graph
    :return: None
    """
    return 0


# ---------------------------------------------------------------------------------------- #


def generate_report_network(networkGraph):
    """
    Generate a network report for the network graph
    :param networkGraph: Network graph
    :return: None
    """
    return 0


# ---------------------------------------------------------------------------------------- #


def generate_report_metrics(networkGraph):
    """
    Generate a metrics report for the network graph
    :param networkGraph: Network graph
    :return: None
    """
    return 0


# ---------------------------------------------------------------------------------------- #


def generate_report_clustering(networkGraph):
    """
    Generate a clustering report for the network graph
    :param networkGraph: Network graph
    :return: None
    """
    return 0


# ---------------------------------------------------------------------------------------- #


def generate_report_resilience(networkGraph):
    """
    Generate a resilience report for the network graph
    :param networkGraph: Network graph
    :return: None
    """
    return 0
