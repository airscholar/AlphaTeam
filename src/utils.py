"""
Author: Alpha Team Group Project
Date: March 2023
Purpose: utils.py contains utilities functions for the project
"""

# ----------------------------------------- Imports ----------------------------------------- #

# External imports
from _md5 import md5

import numpy as np
import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype

# ----------------------------------------- CONSTANT ----------------------------------------- #

red = "\033[0;91m"
green = "\033[0;92m"
yellow = "\033[0;93m"
blue = "\033[0;94m"
networkGraphs_cache = {}


# ----------------------------------------- Functions ----------------------------------------- #

def memoize(func):
    """
    :Function: Memoize the function to avoid recomputing the same value, leverage the cache
    :param func: Function to memoize
    :type func: function
    :return: Wrapper function
    :rtype: function
    """
    cache = {}

    def wrapper(*args, **kwargs):
        """
        :Function: Wrapper function for the memoization
        :param args: arguments
        :type args: list
        :param kwargs: keyword arguments
        :type kwargs: dict
        :return: Result of the function
        :rtype: any
        """
        key = (func, args, tuple(sorted(kwargs.items())))
        key_hash = md5(str(key).encode('utf-8')).hexdigest()
        if key_hash in cache:
            print(f"{green}CACHE: Using cache for {func.__name__}, hash: {yellow}{key_hash}")
            return cache[key_hash]
        print(f"{blue}CACHE: Computing value for {func.__name__}, hash: {yellow}{key_hash} ")
        result = func(*args, **kwargs)
        cache[key_hash] = result
        return result

    return wrapper


# ---------------------------------------------------------------------------------------- #


def set_networkGraph(networkGraph, session_id):
    """
    :Function: Set the network graph in the cache
    :param networkGraph: Network graph
    :type networkGraph: NetworkGraph
    :return: None
    """
    networkGraphs_cache[session_id] = networkGraph
    return 0


# ---------------------------------------------------------------------------------------- #


def get_networkGraph(session_id):
    """
    :Function: Get the network graph from the cache
    :param session_id: Session id
    :type session_id: str
    :return: Network graph
    :rtype: NetworkGraph
    """
    return networkGraphs_cache[session_id]


# ---------------------------------------------------------------------------------------- #


def is_saved(session_id):
    """
    :Function: Check if the network graph is saved in the cache
    :param session_id: Session id
    :type session_id: str
    :return: True if the network graph is saved, False otherwise
    :rtype: bool
    """
    return session_id in networkGraphs_cache.keys()


# ---------------------------------------------------------------------------------------- #


def delete_networkGraph(session_id):
    """
    :Function: Delete the network graph from the cache
    :param session_id: Session id
    :type session_id: str
    :return: None
    """
    del networkGraphs_cache[session_id]
    print(f"{red}CACHE: Deleted network graph with session id: {yellow}{session_id}")
    return 0


# ---------------------------------------------------------------------------------------- #


def return_nan(networkGraphs, column):
    """
    :Function: Return a dataframe with NaN values for the given metric
    :param networkGraphs: NetworkGraphs object
    :type networkGraphs: NetworkGraphs
    :param column: Column name
    :type column: str
    :return: Pandas dataframe with the metric and NaN values
    :rtype: pd.DataFrame
    """
    df = pd.DataFrame(columns=['Node', column])
    df['Node'] = list(networkGraphs.Graph.nodes())
    df[column] = np.nan
    return df


# ---------------------------------------------------------------------------------------- #


def clean_df(df):
    """
    :Function: Clean the dataframe by rounding the values to 6 decimals and shortening the strings to 12 characters
    :param df: Pandas dataframe to clean
    :type df: pd.DataFrame
    :return: Pandas dataframe cleaned
    :rtype: pd.DataFrame
    """

    # if the columns is float round it to 6 decimals
    for column in df.columns:
        # if the columns is a number round it to 6 decimals
        if is_numeric_dtype(df[column]):
            df[column] = df[column].round(6)

        if df[column].dtype == object:
            df[column] = df[column].apply(lambda x: x[:6] + '...' + x[-6:] if len(x) > 15 and x[:2] == '0x' else x[:12])

    return df
