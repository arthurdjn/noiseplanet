# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 22:16:26 2019

@author: arthurd
"""

import pandas as pd

from noiseplanet import db, utils, io, matching
   



def main(dir_geojson, dir_properties=None, out_dirname=".", method="nearest", db_file='database.db', log=True):
    # Map Matching on all the geojson tracks
    matching.match_from_geojsons(dir_geojson, out_dirname=out_dirname, method=method, log=True)
    
    # Connecting to the database
    conn = db.connect(db_file)
    files_geojson = io.open_files(out_dirname, ext='geojson')
    files_properties = io.open_files(dir_properties, ext='properties')
    
    # Saving in a SQLite DataBase
    # Table 'Point'
    for file_gj in files_geojson:
        geojson = io.open_geojson(file_gj)
        df = utils.geojson_to_df(geojson, normalize_header=True)
        db.df_to_table(conn, 'point', df)
    # Table 'Meta'
    for file_prop in files_properties:
        properties = io.open_properties(file_prop)
        df = pd.DataFrame(data=properties, index=[0])
        db.df_to_table(conn, 'meta', df)
    
    # Closing the database
    conn.close()

if __name__ == "__main__":
    # Directory
    dir_geojson = "../../nc_data/test/data/track"
    dir_properties = "../../nc_data/test/data/track"
    # Matching and saving into a DB
    main(dir_geojson, dir_properties=dir_properties, out_dirname='.', method='nearest', db_file="database_raw405.db", log=True)










