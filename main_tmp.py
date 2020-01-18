# -*- coding: utf-8 -*-
"""
Code temporaire servant à lancer le script principal depuis la racine du projet

"""

import os
import json
import sys

from src.utils import io
import src.core.nctrack as nc
import src.dbconnect as dbc
import src.core.model.stats as sts


def main(files, files_properties=None, out_dirname=".", method="nearest", db_file='database.db', log=True):
    
    if files_properties is not None and len(files) != len(files_properties):
        raise Exception ("Length of files and properties should match.")

    # Connecting to the database
    create_db = True
    conn = dbc.connect(db_file)

    for i in range(len(files)):
        # Extract the track informations
        file = files[i]
        name = file.split("\\")[-1].split(".")
        filename = name[0]
        ext = name[1]
        
        # Extract the meta.properties informations
        if files_properties is not None:
            file_props = files_properties[i]
            df_props = io.properties_to_df(file_props)
            df_props.insert(loc=0, column='track_id', value=[filename])
            if i == 0:
                dbc.create_table_from_df(conn, 'meta', df_props)
            dbc.df_to_table(conn, 'meta', df_props)
        
        # Open the geojson
        with open(file) as f:
            geojson = json.load(f)
                           
        # Convert in dataframe
        df = io.geojson_to_df(geojson, extract_coordinates=True)
        if log:
            print("========================")
            print("track : {0}, track size : {1}".format(filename, len(df)))
        try:
            df_corr = nc.correct_track(df, filename=filename, method=method)
    
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
            
            properties.remove('edge_id')
            properties.remove('track_id')
            properties.remove('point_idx')
    
            
            gj = io.df_to_geojson(df_corr, properties, geometry_type='type',
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
                dbc.create_table_from_df(conn, 'point', df_corr)
                create_db = False
            dbc.df_to_table(conn, 'point', df_corr)
        except Exception as e:
            print(e, "The track {0} has not been corrected and therefore not saved under the database")


    # closing the database
    conn.close()

if __name__ == "__main__":
    print("\n\t-----------------------\n",
            "\t       Matching\n\n")

# =============================================================================
#     1/ Read all the Geojson files
# =============================================================================
    print("1/ Reading the files")
    files = io.open_files("data/track")
    print(files[:10])
    
    files_properties = io.open_files("data/track", ext="properties")
    print(files_properties[:10])
    
# =============================================================================
#     2/ Map matching
# =============================================================================
    if len(sys.argv) > 1:
        method = sys.argv[1]
    else:
        method = 'hmm'
    dbfile = 'test/database/database_'+method+'.db'
    
    print("2/ Method : ", method)
    main(files, files_properties=files_properties, out_dirname='test/data', method=method, db_file=dbfile, log=True)

