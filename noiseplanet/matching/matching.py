# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 22:26:12 2020

@author: Utilisateur
"""

# Classic Library
import numpy as np
import pandas as pd

# Useful package
from noiseplanet import io, utils
from noiseplanet.matching import model
from noiseplanet.matching import datacleaner


def match(graph, track, method='hmm'):
    """
    Match a (Lat, Lon) track on the Open Street Map road network.

    Parameters
    ----------
    graph : NetworkX MultiDiGraph
        The OSM graph to match the track.
    track : numpy 2D array
        A 2D matrix composed by Latitudes (first column) and Longitudes (second column)
        of the track.
    method : String, optional
        Method used to match the track on the map. 
        'nearest' match the track on the nearest road.
        'hmm' is a Hidden Markov Model based map matching algorithm.
        The default is 'hmm'.

    Returns
    -------
    track_corr : numpy 2D array
        A 2D matrix composed by Latitudes (first column) and Longitudes (second column)
        of the track.
    route_corr : numpy 2D array
        A 2D matrix composed by Latitudes (first column) and Longitudes (second column)
        of the path connecting all track's points.
    edgeid : numpy 2D array
        List of edges to which each points belongs to.
        Edges id are composed by two extremity nodes id. 
    stats : Dict
        Statistics of the Map Matching.
        'proj_length' is the length of the projection (from track's point to corrected ones),
        'path_length' is the distance on the graph between two following points,
        'unlinked' higlights unconnected points on the graph.
    """
    
    if method == 'nearest':
        track_corr, route_corr, edgeid, stats = model.match_nearest_edge(graph, track)
    elif method == 'hmm':
        track_corr, route_corr, edgeid, stats = model.match_leuven(graph, track)
    return track_corr, route_corr, edgeid, stats


def match_geojson(geojson, method="hmm", log=True):
    """
    Match a GeoJson track on the Open Street Map network.

    Parameters
    ----------
    geojson : Dict
        GeoJson track to match on the Open Street Map network,
        on the dictionary format.
    method : String, optional
        Method used to match the track on the map. 
        'nearest' match the track on the nearest road.
        'hmm' is a Hidden Markov Model based map matching algorithm.
        The default is 'hmm'.
    log : Boolean, optional
        Display console log of the Map Matching results. 
        The default is True.

    Returns
    -------
    geojson_corr : Dict
        Corrected track on a GeoJson dictionary format.
    """ 
    # Convert in dataframe
    df = utils.geojson_to_df(geojson, normalize_header=True)
    df = datacleaner.clean_data(df)
     
    if log:
        print('Length : {0}'.format(len(df)))
    
    coord = np.array([*df['coordinates']])
    X = coord[:, 0]
    Y = coord[:, 1]
    track = np.column_stack((Y, X))
    graph = model.graph_from_track(track, network='all')
    track_corr, route_corr, edgeid, stats = match(graph, track, method=method)
    stats = pd.DataFrame(stats)
    stats = stats.set_index(df.index.values)
    # stats['proj_accuracy'] = df['accuracy'].values / stats['proj_length']
    df_corr = pd.concat([df, stats], axis=1, join='inner')
    if log:
        print('Stats {0}'.format(method))
        print(stats.describe().round(3))
            
    coord[:, 0] = track_corr[:, 1]
    coord[:, 1] = track_corr[:, 0]
    df_corr['coordinates'] = coord        
    proj_init="epsg:4326"
    proj_out="epsg:3857"
    origin = (0, 0)
    side_length = 15     
    Q, R = utils.hexgrid.nearest_hexagons(Y, X, side_length=side_length, origin=origin, 
                        proj_init=proj_init, proj_out=proj_out)
    
    df_corr['hex_id'] = list(zip(Q, R))
    df_corr['edge_id'] = list(zip(edgeid[:,0], edgeid[:, 1]))
    graph_undirected = graph.to_undirected()
    df_corr['osmid'] = [graph_undirected.edges[(edgeid[0], edgeid[1], 0)]['osmid'] for edgeid in df_corr['edge_id'].values]
    
    geometry = 'Point'
    coordinates = 'coordinates'
    properties = [key for key in df.columns.values[2:]]
    geojson = utils.df_to_geojson(df_corr, geometry, coordinates, properties)
    
    return geojson


def match_from_geojson(file, out_dirname='.', method="hmm", log=True):
    """
    Match a GeoJson track on the Open Street Map network.

    Parameters
    ----------
    file : String
        Path to the GeoJson file. It should contain track's points informations used 
        to match on the network.
    out_dirname : String, optional
        Output directory path in which the corrected GeoJson track file is saved. 
        The default is '.', the current working folder.
    method : String, optional
        Method used to match the track on the map. 
        'nearest' match the track on the nearest road.
        'hmm' is a Hidden Markov Model based map matching algorithm.
        The default is 'hmm'.
    log : Boolean, optional
        Display console log of the Map Matching results. 
        The default is True.

    Returns
    -------
    None.
    """

    name = file.split("\\")[-1].split(".")[0]    
    # Open the geojson
    geojson = io.open_geojson(file)
    if log:
        print('Name : {0}'.format(name))
    geojson_corr = match_geojson(geojson, method="hmm", log=True)
        
    out_file = out_dirname + '/' + name + '_' + method + '.geojson'
    io.save_geojson(geojson_corr, out_file)


def match_from_geojsons(dirname, out_dirname=".", method="hmm", log=True):
    """
    Match a list of GeoJson tracks on the Open Street Map network.

    Parameters
    ----------
    dirname : String
        Path to the directory in which GeoJson tomatch are contained. 
        All GeoJson files should contain track's points informations used to match on the network.
    out_dirname : String, optional
        Output directory path in which the corrected GeoJson tracks files are saved. 
        The default is '.', the current working folder.
    method : String, optional
        Method used to match the track on the map. 
        'nearest' match the track on the nearest road.
        'hmm' is a Hidden Markov Model based map matching algorithm.
        The default is 'hmm'.
    log : Boolean, optional
        Display console log of the Map Matching results. 
        The default is True.

    Returns
    -------
    None.
    """
    
    files = io.open_files(dirname, ext='geojson')
    for i, file in enumerate(files):
        if log:
            print('--------------------------',
                  '\nTrack n° {0}'.format(i))   
            
        try:
            match_from_geojson(file, out_dirname=out_dirname, method=method, log=log)
        except Exception as e:
            print('Exception Error : {0}'.format(e))
            continue



