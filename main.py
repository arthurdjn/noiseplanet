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


def main(files, out_dirname=".", method="nearest", db_file='database.db', log=True):
    
    # Connecting to the database
    conn = dbc.connect(db_file)
           
    
    for i in range(len(files)):
        if log:
            print("========================")
        
        file = files[i]
        name = file.split("\\")[-1].split(".")
        file_name = name[0]
        ext = name[1]
        
        #Open the geojson
        with open(file) as f:
            geojson = json.load(f)

        # convert in dataframe
        df = io.geojson_to_df(geojson, extract_coordinates=True)
        
        # Fill None values by interpolation
        try:
            df = df.interpolate(method='quadratic', axis=0)
        except ValueError as e:
            print(e)
            print("The interpolation failed for {0}".format(file_name))
        # Delete rows where no positions
        df = df[df['type'].notnull()]
        
        
        track = np.column_stack((df['latitude'].values, df['longitude'].values))
        X = df['longitude'].values
        Y = df['latitude'].values
        
        # generate the OSM network
        graph = rt.graph_from_track(track, network='all')
                
        # method nearest
        if method =="nearest":
            if log:
                print("track name : " + file_name + ", method " + method)
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
            directory = out_dirname + '\\track_nearest'
            outname = directory + '\\' + file_name + '_nearest' + '.' + ext
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
            df_corr.insert(loc=0, column='track_id', value=[file_name]*len(df_corr))
            df_corr['edge_id'] = edgesid
            if i == 0:
                dbc.create_table_from_df(conn, 'point', df_corr)
            dbc.df_to_table(conn, 'point', df_corr)
            
        # method hmm
        if method =="hmm":
            try:
                # the leuven library throw exception when points are too far from edges etc.
                if log:
                    print("track name : " + file_name + ", method " + method)
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
                directory = out_dirname + '\\track_hmm'
                outname = directory + '\\' + file_name + '_hmm' + '.' + ext
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
                df_corr.insert(loc=0, column='track_id', value=[file_name]*len(df_corr))
                df_corr['edge_id'] = edgesid
                if i == 0:
                    dbc.create_table_from_df(conn, 'point', df_corr)
                dbc.df_to_table(conn, 'point', df_corr)
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
    files = files[153:]
    
# =============================================================================
#     2/ Map matching
# =============================================================================
    print("2/ Map Matching")
    main(files, out_dirname='../data', method='hmm', db_file='../database/database_hmm.db', log=True)








