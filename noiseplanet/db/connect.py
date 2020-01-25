# -*- coding: utf-8 -*-

# Created on Thu Dec 5 16:49:20 2019

# @author: arthurd

"""
DBConnect Module.

Connection to DataBase.
"""

import sqlite3
from sqlite3 import Error


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
      

