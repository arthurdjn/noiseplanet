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
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print('SQLite3 version :', sqlite3.version)
    except Error as e:
        print(e)
    
    return conn
 

def create_table(conn, create_table_sql):
 
    try:
        cur = conn.cursor()
        cur.execute(create_table_sql)
    except Error as e:
        print(e)
      

def create_table_from_df(conn, table_name, df):
    sql_type = {np.dtype('O'): 'TEXT',
            np.dtype('float64'): 'REAL',
            np.dtype('float32'): 'REAL',
            np.dtype('int64'): 'INTEGER',
            np.dtype('int32'): 'INTEGER'}
    
    columns = ','.join([col_name.replace('-', '_').replace('.', '_') + " " + sql_type[key] for col_name, key in zip(df.keys(), df.dtypes.values)])
    create_table_sql = "CREATE TABLE IF NOT EXISTS " + table_name + "(id integer PRIMARY KEY," + columns + ");"

    
    try:
        cur = conn.cursor()
        cur.execute(create_table_sql)
        conn.commit()
    except Error as e:
        print(e)


def df_to_table(conn, table_name, df):
    
    # Converting all 'object' like type into string values
    keys = df.dtypes[df.dtypes.values == np.dtype('O')].index
    df[keys] = df[keys].astype(str)
        
    sql = "INSERT INTO " + table_name + "(" + ','.join([key.replace('-', '_').replace('.', '_') for key in df]) + ")"
    sql += "VALUES(" + ','.join(['?']*len(df.keys())) + ")"
        
    cur = conn.cursor()
    try :
        cur.executemany(sql, df.values)
        conn.commit()
    except Error as e:
        print(e)
    

def select_to_df(conn, query):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute(query)
 
    rows = cur.fetchall()
 
    col_names = [description[0] for description in cur.description]
    df = pd.DataFrame(rows, columns=col_names)
    
    # Convert back a stringed tuple to a tuple
    for key in df:
        if type(df[key][0]) == str and '(' in df[key][0] and ',' in df[key][0] and ')' in df[key][0]:
            df[key] = [literal_eval(x) for x in df[key]]
    
    return df










