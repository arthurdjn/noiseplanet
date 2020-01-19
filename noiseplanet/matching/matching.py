# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 22:26:12 2020

@author: Utilisateur
"""

# Classic Library
import numpy as np
import pandas as pd

# Useful package
from noiseplanet.matching import model
from noiseplanet.matching.datacleaner import clean_data
from noiseplanet.utils import hexgrid


def match(graph, track, method='hmm'):

    if method == 'nearest':
        track_coor, route_corr, edgeid, stats = model.match_nearest_edge(graph, track)
    elif method == 'hmm':
        track_coor, route_corr, edgeid, stats = model.match_leuven(graph, track)
    return track_coor, route_corr, edgeid, stats


def correct_track(df, filename="track", method="hmm"):    
    df = clean_data(df)
    # Get lat lon
    track = np.column_stack((df['latitude'].values, df['longitude'].values))
    X = df['longitude'].values
    Y = df['latitude'].values
    track = np.column_stack((Y, X))
    
    # generate the OSM network
    graph = model.graph_from_track(track, network='all')
                 
    # the leuven library throw exception when points are too far from edges etc.
    # compute the projection
    track_corr, route_corr, edge_id, stats = match(graph, track, method=method)
    
    # index the stats as the df
    stats = stats.set_index(df.index.values)
    # add statistics and verify that the column 'accuracy' exists
    try:
        stats['proj_accuracy'] = df['accuracy'].values / stats['proj_length']
    except KeyError as e:
        print('{0} Error computing the projection accuracy'.format(e))
    
    # update the df with the new points
    df_corr = pd.concat([df, stats], axis=1, join='inner')
    df_corr['longitude'] = track_corr[:,1]
    df_corr['latitude'] = track_corr[:,0]
                       
    proj_init="epsg:4326"
    proj_out="epsg:3857"
    origin = (0, 0)
    side_length = 15
                
    Q, R = hexgrid.nearest_hexagons(Y, X, side_length=side_length, origin=origin, 
                        proj_init=proj_init, proj_out=proj_out)
    df_corr['hex_id'] = list(zip(Q, R))
    # add to the database
    df_corr.insert(loc=0, column='point_idx', value=df_corr.index.values)
    df_corr.insert(loc=0, column='track_id', value=[filename]*len(df_corr))

    df_corr['edge_id'] = edge_id
    graph_undirected = graph.to_undirected()
    df_corr['osmid'] = [graph_undirected.edges[(edge_id[0], edge_id[1], 0)]['osmid'] for edge_id in df_corr['edge_id'].values]
                          

    return df_corr








    
    