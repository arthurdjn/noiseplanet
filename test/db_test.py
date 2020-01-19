# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 12:52:18 2020

@author: arthurd
"""


import pandas as pd
import noiseplanet as npt




def connect_test():

    conn = npt.db.connect("database/data.db")
    
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
    npt.db.create_table(conn, sql_create_point_table)
    
    df = pd.DataFrame({
                       'type': ['Point', 'Point'],
                       'longitude': [3, 3],
                       'latitude': [45.0, 45.1],
                       'elevation': [25.0, 250.0],
                       'leq_mean': [40.0, 45.0],
                       'marker-color': ['#fff', '#000'],
                       'accuracy': [6.0, 12.0],
                       'location_utc': [(19489489, 1515), (1494, 15615)]})
    
    npt.db.df_to_table(conn, 'point', df)
    npt.db.create_table_from_df(conn, 'geometry', df)
    
    query = "SELECT * FROM point"
    selection = npt.db.select_to_df(conn, query)
    print("\n" + query)
    print(selection.head())

    conn.close()
    

if __name__ == "__main__":
    connect_test()
    