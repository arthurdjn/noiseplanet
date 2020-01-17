# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 22:16:26 2019

@author: arthurd
"""

import numpy as np
import pandas as pd
import json

from utils import io
import core.model.osmmatching as osmm
import core.model.mapmatching.route as rt
import core.representation.hexgrid as hxg


def correct_track(df, filename="track", method="hmm"):    
    # Fill None values by interpolation
    try:
        df = df.interpolate(method='quadratic', axis=0)
    except ValueError as e:
        print(e)
        print("The interpolation failed for {0}".format(filename))
    # Delete rows where there are no positions
    df = df[df['type'].notnull()]
    
    # Get lat lon
    track = np.column_stack((df['latitude'].values, df['longitude'].values))
    X = df['longitude'].values
    Y = df['latitude'].values
    
    # generate the OSM network
    graph = rt.graph_from_track(track, network='all')
            
    # method nearest
    if method =="nearest":       
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
                               
        # transform the dataframe in a geojson
        properties = [key for key in df_corr]
        properties.remove('type')
        properties.remove('longitude')
        properties.remove('latitude')
        properties.remove('elevation')
              
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
        

        
    # method hmm
    if method =="hmm":
        try:
            # the leuven library throw exception when points are too far from edges etc.
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
                
            # transform the dataframe in a geojson
            properties = [key for key in df_corr]
            properties.remove('type')
            properties.remove('longitude')
            properties.remove('latitude')
            properties.remove('elevation')
                       
            proj_init="epsg:4326"
            proj_out="epsg:3857"
            origin = (0, 0)
            side_length = 15
                        
            Q, R = hxg.nearest_hexagons(Y, X, side_length=side_length, origin=origin, 
                                proj_init=proj_init, proj_out=proj_out)
            df_corr['hex_id'] = list(zip(Q, R))
            # add to the database
            df_corr.insert(loc=0, column='point_idx', value=df_corr.index.values)
            df_corr.insert(loc=0, column='track_id', value=[filename]*len(df_corr))
            df_corr['edge_id'] = edgesid
            df_corr['osmid'] = [graph.edges[(edge_id[0], edge_id[1], 0)]['osmid'] for edge_id in df_corr['edge_id'].values]
                                  
        except Exception as e:
            print(e)

    return df_corr


if __name__ == "__main__":
    print("\n\t-----------------------\n",
            "\t       Matching\n\n")
    
# =============================================================================
#     1/ Read all the Geojson files
# =============================================================================
    print("1/ Reading the files")
    files = io.open_files("../../data/track")
    # files = files[:10]
    print(files[23:])
    filename = files[0]

# =============================================================================
#   2/ Convert track
# =============================================================================
    print("2/ Correct track")
    with open(filename) as f:
        geojson = json.load(f)
        
    gj = correct_track(geojson, filename=filename, method="hmm")



