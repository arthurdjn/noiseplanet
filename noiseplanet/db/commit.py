# -*- coding: utf-8 -*-

# Created on Thu Dec 5 16:49:20 2019

# @author: arthurd

"""
DBConnect Module.
Add DataFrame/Values to a DataBase.
"""

import numpy as np
import pandas as pd
from ast import literal_eval

from noiseplanet import utils, io
from noiseplanet.db.connect import database_query

def df_to_table(conn, table_name, df):
    """
    Paste Values from a DataFrame into a DataBase table.

    Parameters
    ----------
    conn : SQLite3 Connection
        The connection to the DataBase.
    table_name : String
        Name of the DataBase's table where the DataFrame will be pasted.
    df : pandas DataFrame
        DataFrame to transfer into the DataBase.

    Returns
    -------
    None.
    """
    # Create table if does not exist
    sql_type = {np.dtype('O'): 'TEXT',
                np.dtype('float64'): 'REAL',
                np.dtype('float32'): 'REAL',
                np.dtype('int64'): 'INTEGER',
                np.dtype('int32'): 'INTEGER'}
    
    columns = ','.join([col_name.replace('-', '_').replace('.', '_') + " " + sql_type[key] for col_name, key in zip(df.keys(), df.dtypes.values)])
    create_table_sql = "CREATE TABLE IF NOT EXISTS " + table_name + "(id integer PRIMARY KEY," + columns + ");"
    database_query(conn, create_table_sql)
    
    # Converting all 'object' like type into string values
    keys = df.dtypes[df.dtypes.values == np.dtype('O')].index
    df[keys] = df[keys].astype(str)
        
    # sql = "INSERT INTO " + table_name + "(" + ','.join([key.replace('-', '_').replace('.', '_') for key in df]) + ")"
    attributes = [key.replace('-', '_').replace('.', '_') for key in df.columns.values]
    sql = "INSERT INTO " + table_name + "(" + ','.join(attributes) + ")"
    sql += "VALUES(" + ','.join(['?']*len(df.keys())) + ")"
    database_query(conn, sql)
    

def geojson_to_table(conn, table_name, *file_geojson):
    """
    Add a GeoJson file to the table in a SQLite DataBase.

    Parameters
    ----------
    conn : SQLite3 Connection
        The connection to the DataBase.
    table_name : String
        Name of the DataBase's table where the DataFrame will be pasted.
    *file_geojson : String
        GeoJson files to add.

    Returns
    -------
    None.
    """
    
    for file in file_geojson:
        geojson = io.open_geojson(file)
        df = utils.geojson_to_df(geojson, normalize_header=True)
        df_to_table(conn, 'point', df)
    
    
def properties_to_table(conn, table_name, *file_properties):
    """
    Add a properties file to the table in a SQLite DataBase.

    Parameters
    ----------
    conn : SQLite3 Connection
        The connection to the DataBase.
    table_name : String
        Name of the DataBase's table where the DataFrame will be pasted.
    *file_properties : String
        Properties files to add.

    Returns
    -------
    None.
    """
    
    for file_prop in file_properties:
        properties = io.open_properties(file_prop)
        df = pd.DataFrame(data=properties, index=[0])
        df_to_table(conn, 'meta', df)

def track_to_db(conn, dir_track):
    """
    Add tracks informations in a SQLite DataBase.

    Parameters
    ----------
    conn : SQLite3 Connection
        The connection to the DataBase.
    dir_track : String
        Path to the track files.

    Returns
    -------
    None.
    """
    
    file_geojson = io.open_files(dir_track, ext='geojson')
    file_properties = io.open_files(dir_track, ext='properties')
    properties_to_table(conn, 'meta', *file_properties)
    geojson_to_table(conn, 'point', *file_geojson)


def select_to_df(conn, query):
    """
    Convert the query request into a DataFrame.

    Parameters
    ----------
    conn : SQLite3 Connection
        Connection to the DataBase.
    query : String
        Query to request on the DataBase.

    Returns
    -------
    df : pandas DataFrame
        The result of the Query, in a DataFrame format.
    """

    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
 
    col_names = [description[0] for description in cur.description]
    df = pd.DataFrame(rows, columns=col_names)
    
    try:
        del df['id']
    except KeyError as e:
        print("KeyError {0} : The column id was not deleted".format(e))
    
    # Convert back a stringed tuple to a tuple
    for key in df:
        # If the string is composed
        if (type(df[key][0]) == str and ('(' in df[key][0] and ',' in df[key][0] and ')' in df[key][0])):
            evaluated_col = []
            for x in df[key]:
                if x is None:
                    evaluated_col.append(None)
                else:
                    evaluated_col.append(literal_eval(x))
            df[key] = evaluated_col
    
    return df







