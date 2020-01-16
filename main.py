# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 22:16:26 2019

@author: arthurd
"""

import os
import json
import numpy as np
import pandas as pd

from src.utils import io
import src.core.model.stats as st
import src.core.model.osmmatching as osmm
import src.core.model.mapmatching.route as rt
import src.dbconnect as dbc
import src.core.representation.hexgrid as hxg


def main(files, properties=[], out_dirname=".", method="nearest", db_file='database.db', log=True):
    
    
    if len(files) != len(properties):
        raise Exception ("Length of files and properties should match")
    
    # Connecting to the database
    conn = dbc.connect(db_file)
           
    
    for i in range(len(files)):
        if log:
            print("========================")
        
        # Extract the track informations
        file = files[i]
        file_props = properties[i]
        name = file.split("\\")[-1].split(".")
        filename = name[0]
        ext = name[1]
    
        # Open the geojson
        with open(file) as f:
            geojson = json.load(f)

        # Convert in dataframe
        df = io.geojson_to_df(geojson, extract_coordinates=True)
        df_props = io.properties_to_df(file_props)
        df_props.insert(loc=0, column='track_id', value=[filename])
        
        # Fill None values by interpolation
        try:
            df = df.interpolate(method='quadratic', axis=0)
        except ValueError as e:
            print(e)
            print("The interpolation failed for {0}".format(filename))
        # Delete rows where no positions
        df = df[df['type'].notnull()]
        
        # Get lat lon
        track = np.column_stack((df['latitude'].values, df['longitude'].values))
        X = df['longitude'].values
        Y = df['latitude'].values
        
        # generate the OSM network
        graph = rt.graph_from_track(track, network='all')
                
        # method nearest
        if method =="nearest":
            if log:
                print("track name : " + filename + ", method " + method)
                print("track length : " + str(len(track)))
            
            # compute the projection
            track_corr, route_corr, edgesid, stats = osmm.map_matching(graph, Y, X, method=method)
            
            # index the stats as the df
            stats = stats.set_index(df.index.values)
            # add statistics and verify that the column 'accuracy' exists
            try:
                stats['proj_accuracy'] = df['accuracy'].values / stats['proj_length']
            except KeyError as error:
                print(error, 'Error computing the projection accuracy')
            
            # update the df with the new points
            df_corr = pd.concat([df, stats], axis=1, join='inner')
            df_corr['longitude'] = track_corr[:,1]
            df_corr['latitude'] = track_corr[:,0]
                       
            if log:
                print("-------------")
                print("Stats nearest")
                print(st.global_stats(stats).round(2))
                
            # transform the dataframe in a geojson
            properties = [key for key in df_corr]
            properties.remove('type')
            properties.remove('longitude')
            properties.remove('latitude')
            properties.remove('elevation')
            gj = io.df_to_geojson(df_corr, properties, geometry_type='type', 
                  lat='latitude', lon='longitude', z='elevation')
            
            # test if the out directory exists
            directory = out_dirname + '/track_nearest'
            outname = directory + '/' + filename + '_nearest' + '.' + ext
            if not os.path.exists(directory):
                os.makedirs(directory)
            
            # write the geojson
            with open(outname, 'w') as f:
                json.dump(gj, f)
            
            proj_init="epsg:4326"
            proj_out="epsg:3857"
            origin = (0, 0)
            side_length = 50
                        
            Q, R = hxg.nearest_hexagons(Y, X, side_length=side_length, origin=origin, 
                                proj_init=proj_init, proj_out=proj_out)
            df_corr['hex_id'] = list(zip(Q, R))
            # add to the database
            df_corr.insert(loc=0, column='point_idx', value=df_corr.index.values)
            df_corr.insert(loc=0, column='track_id', value=[filename]*len(df_corr))
            df_corr['edge_id'] = edgesid
            df_corr['osmid'] = [graph.edges[(edge_id[0], edge_id[1], 0)]['osmid'] for edge_id in df_corr['edge_id'].values]
            
            if i == 0:
                dbc.create_table_from_df(conn, 'point', df_corr)
                dbc.create_table_from_df(conn, 'meta', df_props)
            dbc.df_to_table(conn, 'point', df_corr)
            dbc.df_to_table(conn, 'meta', df_props)
            
        # method hmm
        if method =="hmm":
            try:
                # the leuven library throw exception when points are too far from edges etc.
                if log:
                    print("track name : " + filename + ", method " + method)
                    print("track length : " + str(len(track)))
                # compute the projection
                track_corr, route_corr, edgesid, stats = osmm.map_matching(graph, Y, X, method=method)
                
                # index the stats as the df
                stats = stats.set_index(df.index.values)
                # add statistics and verify that the column 'accuracy' exists
                try:
                    stats['proj_accuracy'] = df['accuracy'].values / stats['proj_length']
                except KeyError as error:
                    print(error, 'Error computing the projection accuracy')
                
                # update the df with the new points
                df_corr = pd.concat([df, stats], axis=1, join='inner')
                df_corr['longitude'] = track_corr[:,1]
                df_corr['latitude'] = track_corr[:,0]
                           
                if log:
                    print("-------------")
                    print("Stats hmm")
                    print(st.global_stats(stats).round(2))
                    
                # transform the dataframe in a geojson
                properties = [key for key in df_corr]
                properties.remove('type')
                properties.remove('longitude')
                properties.remove('latitude')
                properties.remove('elevation')
                gj = io.df_to_geojson(df_corr, properties, geometry_type='type', 
                      lat='latitude', lon='longitude', z='elevation')
                
                # test if the out directory exists
                directory = out_dirname + '/track_hmm'
                outname = directory + '/' + filename + '_hmm' + '.' + ext
                if not os.path.exists(directory):
                    os.makedirs(directory)
                
                # write the geojson
                with open(outname, 'w') as f:
                    json.dump(gj, f)
                
                proj_init="epsg:4326"
                proj_out="epsg:3857"
                origin = (0, 0)
                side_length = 50
                            
                Q, R = hxg.nearest_hexagons(Y, X, side_length=side_length, origin=origin, 
                                    proj_init=proj_init, proj_out=proj_out)
                df_corr['hex_id'] = list(zip(Q, R))
                # add to the database
                df_corr.insert(loc=0, column='point_idx', value=df_corr.index.values)
                df_corr.insert(loc=0, column='track_id', value=[filename]*len(df_corr))
                df_corr['edge_id'] = edgesid
                df_corr['osmid'] = [graph.edges[(edge_id[0], edge_id[1], 0)]['osmid'] for edge_id in df_corr['edge_id'].values]
                                      
                # Create the db
                if i == 0:
                    dbc.create_table_from_df(conn, 'point', df_corr)
                    dbc.create_table_from_df(conn, 'meta', df_props)
                dbc.df_to_table(conn, 'point', df_corr)
                dbc.df_to_table(conn, 'meta', df_props)
            except Exception as e:
                print(e)
            
            
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
    # files = files[:10]
    print(files[23:])
    files = [files[0]]
    
    properties = io.open_files("data/track", ext="properties")
    # files = files[:10]
    print(properties[23:])
    properties = [properties[0]]
    
# =============================================================================
#     2/ Map matching
# =============================================================================
    print("2/ Map Matching")
    main(files, properties=properties, out_dirname='data', method='hmm', db_file='database/database_hmm3.db', log=True)









