# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 22:16:26 2019

@author: arthurd
"""

import os
import json


import noiseplanet.utils as utils
import noiseplanet.io as io
import noiseplanet.db as db

from noiseplanet import matching
from noiseplanet.matching import stats as sts

    
    

def main(files, files_properties=None, out_dirname=".", method="nearest", db_file='database.db', log=True):
    
    if files_properties is not None and len(files) != len(files_properties):
        raise Exception ("Length of files and properties should match.")

    # Connecting to the database
    create_db = True
    conn = db.connect(db_file)

    for i in range(len(files)):
        # Extract the track informations
        file = files[i]
        name = file.split("\\")[-1].split(".")
        filename = name[0]
        ext = name[1]
        
        # Extract the meta.properties informations
        if files_properties is not None:
            file_props = files_properties[i]
            df_props = utils.properties_to_df(file_props)
            df_props.insert(loc=0, column='track_id', value=[filename])
            if create_db:
                db.create_table_from_df(conn, 'meta', df_props)
            db.df_to_table(conn, 'meta', df_props)
        
        # Open the geojson
        with open(file) as f:
            geojson = json.load(f)
                           
        # Convert in dataframe
        df = utils.geojson_to_df(geojson, extract_coordinates=True)
        if log:
            print("========================")
            print("track : {0}, track size : {1}".format(filename, len(df)))
        try:
            df_corr = matching.correct_track(df, filename=filename, method=method)
    
            if log:
                print("------------------------")
                print("stats {0}".format(method))
                print(sts.global_stats(df_corr[['proj_length', 'path_length', 'unlinked', 'proj_accuracy']]).round(3))
    
    
            # Convert back to geojson
            properties = [key for key in df_corr]
            properties.remove('type')
            properties.remove('longitude')
            properties.remove('latitude')
            properties.remove('elevation')
            # remove useless attributes
            properties.remove('edge_id')
            properties.remove('track_id')
            properties.remove('point_idx')
    
            gj = utils.df_to_geojson(df_corr, properties, geometry_type='type',
                                  lat='latitude', lon='longitude', z='elevation')
    
            # test if the out directory exists
            directory = out_dirname + '/track_' + method
            outname = directory + '/' + filename + '_' + method + '.' + ext
            if not os.path.exists(directory):
                os.makedirs(directory)
    
            # write the geojson
            with open(outname, 'w') as f:
                json.dump(gj, f)
    
            # Create and add to the database
            if create_db:
                db.create_table_from_df(conn, 'point', df_corr)
                create_db = False
            db.df_to_table(conn, 'point', df_corr)
        except Exception as e:
            print(e, "The track {0} has not been corrected and therefore not saved in the database".format(filename))


    # closing the database
    conn.close()

if __name__ == "__main__":
    print("\n\t-----------------------\n",
            "\t       Matching\n\n")

# =============================================================================
#     1/ Read all the Geojson files
# =============================================================================
    print("1/ Reading the files")
    files = io.open_files("../data/track")
    print(files[:10])
    
    files = files[7:10]
    
    files_properties = io.open_files("../data/track", ext="properties")
    print(files_properties[:10])
    files_properties = files_properties[7:10]
    
    
# =============================================================================
#     2/ Map matching
# =============================================================================
    print("2/ Map Matching")
    main(files, files_properties=files_properties, out_dirname='../data', method='nearest', db_file='../database/database_nearest2.db', log=True)










