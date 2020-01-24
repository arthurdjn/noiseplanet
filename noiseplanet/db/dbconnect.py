# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 11:28:24 2019

@author: arthurd
"""

import sqlite3
from sqlite3 import Error
import numpy as np
import pandas as pd
from ast import literal_eval


def connect(db_file):
    """
    Create a DataBase connection to a SQLite DataBase.

    Parameters
    ----------
    db_file : String
        Path to the DataBase file. If the DataBase does not exists, a new one is created.

    Returns
    -------
    conn : SQLite3 Connection
        Connection to the DataBase db_file.
    """
    
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print('SQLite3 version :', sqlite3.version)
    except Error as e:
        print(e)
    
    return conn
 

def database_query(conn, query):
    """
    Request a query in a database.

    Parameters
    ----------
    conn : SQLite3 Connection
        Connection to the DataBase where the query is requested.
    create_table_sql : String
        SQL query to create a table in.

    Returns
    -------
    None.
    """
    try:
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
    except Error as e:
        print('Error : {0}'.format(e))
      



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
        if (type(df[key][0]) == str and ('(' in df[key][0] and ',' in df[key][0] and ')' in df[key][0]) or 
            ('[' in df[key][0] and ',' in df[key][0] and ']' in df[key][0])):
            evaluated_col = []
            for x in df[key]:
                if x is None:
                    evaluated_col.append(None)
                else:
                    evaluated_col.append(literal_eval(x))
            df[key] = evaluated_col
    
    return df


