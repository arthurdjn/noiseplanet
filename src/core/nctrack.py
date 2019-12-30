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
import model.stats as st
import model.mapmatching as mm



def track_to_df(file_name, dir_path='.'):
    
    file = dir_path + '\\' + file_name
    
    #Open the geojson
    with open(file) as f:
        geojson = json.load(f)

    # convert in dataframe
    df = io.geojson_to_df(geojson, extract_coordinates=True)
    
    # Fill None values by interpolation
    df = df.interpolate(method='quadratic', axis=0)
    # Delete rows where no positions
    df = df[df['type'].notnull()]
    
    return df



def match_tracks(files, out_dirname=".", proj="all", log=True):
    for i in range(len(files)):
        if log:
            print("\n========================\n")
        
        file = files[i]
        name = file.split("\\")[-1].split(".")
        filename = name[0]
        ext = name[1]
        
        df = track_to_df(file)
        
        track = np.column_stack((df['latitude'].values, df['longitude'].values))
        
        # generate the OSM network
        graph = mm.graph_from_track(track, network='all')
                    
        # proj nearest
        if proj == "all" or proj=="nearest":
            if log:
                print("track name : " + filename + ", method nearest")
                print("track length : " + str(len(track)))
            
            # compute the projection
            track_nearest, route_nearest, statesid_nearest, stats_nearest = mm.match_nearest_edge(graph, track)
            
            # index the stats as the df
            stats_nearest = stats_nearest.set_index(df.index.values)
            # add statistics and verify that the column 'accuracy' exists
            try:
                stats_nearest['proj_accuracy'] = df['accuracy'].values / stats_nearest['proj_length']
            except KeyError as error:
                print(error, 'Error computing the projection accuracy')
            
            # update the df with the new points
            df_nearest = pd.concat([df, stats_nearest], axis=1, join='inner')
            df_nearest['longitude'] = track_nearest[:,1]
            df_nearest['latitude'] = track_nearest[:,0]
            
            if log:
                print("\n-------------")
                print("Stats nearest")
                print(st.global_stats(stats_nearest).round(2))
                
            # transform the dataframe in a geojson
            properties = [key for key in df_nearest]
            properties.remove('type')
            properties.remove('longitude')
            properties.remove('latitude')
            properties.remove('elevation')
            gj = io.df_to_geojson(df_nearest, properties, geometry_type='type', 
                  lat='latitude', lon='longitude', z='elevation')
            
            # test if the out directory exists
            directory = out_dirname + '\\track_nearest'
            outname = '\\' + filename + '_nearest' + '.' + ext
            if not os.path.exists(directory):
                os.makedirs(directory)
            # write the geojson
            with open(outname, 'w') as f:
                json.dump(gj, f)
            
        if proj=="all" or proj=="hmm":
            if log:
                print("\ntrack name : " + filename + ", method hmm")
                print("track length : " + str(len(track)))
            
            # compute the hmm matching
            track_hmm, route_hmm, statesid_hmm, stats_hmm = mm.match_hmm(graph, track)
            
            # index the stats as the df
            stats_hmm = stats_hmm.set_index(df.index.values)
            # add stats and verify that the column 'accuracy' exists
            try:
                stats_hmm['proj_accuracy'] = df['accuracy'].values / stats_hmm['proj_length']
            except KeyError as error:
                print(error, 'Error computing the projection accuracy')
            
            # update the df with the new points
            df_hmm = pd.concat([df, stats_hmm], axis=1, join='inner')
            df_hmm['longitude'] = track_hmm[:,1]
            df_hmm['latitude'] = track_hmm[:,0]
            
            if log:
                print("\n-------------")
                print("Stats hmm")
                print(st.global_stats(stats_hmm).round(2))
                
            # transform the dataframe in a geojson
            properties = [key for key in df_hmm]
            properties.remove('type')
            properties.remove('longitude')
            properties.remove('latitude')
            properties.remove('elevation')
            gj = io.df_to_geojson(df_hmm, properties, geometry_type='type', 
                  lat='latitude', lon='longitude', z='elevation')
            
            # test if the out directory exists
            directory = out_dirname + '\\track_hmm'
            outname = '\\' + filename + '_hmm' + '.' + ext
            if not os.path.exists(directory):
                os.makedirs(directory)
            # write the geojson            
            with open(outname, 'w') as f:
                json.dump(gj, f)
    
    if log:  
        print("\n========================n")



if __name__ == "__main__":
    print("\n\t-----------------------\n",
            "\t       Matching\n\n")
    
# =============================================================================
#     1/ Read all the Geojson files
# =============================================================================
    print("1/ Reading the files")
    files = io.open_files("..\\..\\data\\track")
    # files = files[:10]
    print(files)
    
# =============================================================================
#     2/ Map matching
# =============================================================================
    print("2/ Map Matching")
    match_tracks(files, out_dirname='..\\..\\data', log=True)









