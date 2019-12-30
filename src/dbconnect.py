# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 11:28:24 2019

@author: arthurd
"""

import sqlite3
from sqlite3 import Error
import numpy as np


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
    





    
if __name__ == '__main__':
    import pandas as pd
    
    conn = connect("data.db")
    
    sql_create_point_table = """ CREATE TABLE IF NOT EXISTS point (
                                        id integer PRIMARY KEY,
                                        track_id TEXT,
                                        point_idx INT,
                                        type TEXT,
                                        longitude REAL,
                                        latitude REAL,
                                        elevation REAL,
                                        leq_mean REAL,
                                        marker_color TEXT,
                                        accuracy REAL,
                                        location_utc REAL
                                    ); """
    create_table(conn, sql_create_point_table)
    
    df = pd.DataFrame({
                       'type': ['Point', 'Point'],
                       'longitude': [3, 3],
                       'latitude': [45.0, 45.1],
                       'elevation': [25.0, 250.0],
                       'leq_mean': [40.0, 45.0],
                       'marker-color': ['#fff', '#000'],
                       'accuracy': [6.0, 12.0],
                       'location_utc': [(19489489, 1515), (1494, 15615)]})
    
    row = np.hstack(([['track(1)', df.index[1]], df.loc[1].values]))
            
    df_to_table(conn, 'point', df)
    
    
    create_table_from_df(conn, 'geometry', df)
    
    conn.close()



















