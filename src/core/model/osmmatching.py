# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 16:03:37 2019

@author: Utilisateur
"""

# Classic Library
import osmnx as ox                         # OSM
import numpy as np
import json
import pandas as pd

# Useful script
import src.utils.io as io
import src.core.model.stats as st
import src.core.model.mapmatching.nearest as nearest
import src.core.model.mapmatching.leuven as leuven
import src.core.model.mapmatching.route as rt


def map_matching(graph, lat, lon, method='nearest'):
    
    track = np.column_stack((lat, lon))
    
    if method == 'nearest':
        track_coor, route_corr, edgeid, stats = nearest.match_nearest_edge(graph, track)
    elif method == 'hmm':
        track_coor, route_corr, edgeid, stats = leuven.match_leuven(graph, track)
    return track_coor, route_corr, edgeid, stats




if __name__ == "__main__":
    print("\n\t-----------------------\n",
            "\t      Map Matching     \n\n")
    
    # Visualize the data
    import matplotlib.pyplot as plt
    from matplotlib import collections as mc   # for plotting
    
# =============================================================================
#     1/ Open the track
# =============================================================================    
    print("1/ Open the track")
    print("\t1.1/ Convert in dataframe")
    filename = 'mapmatching\\test\\track(1).geojson'
    with open(filename) as f:
        geojson = json.load(f)
    
    # convert in dataframe
    df = io.geojson_to_df(geojson, extract_coordinates=True)
        
    print("\t1.2/ Clean the track")
    # Fill None values by interpolation
    df = df.interpolate(method='quadratic', axis=0)
    # Delete rows where no positions
    df = df[df['type'].notnull()]
    
# =============================================================================
#     2/ Extract the coordinates
# =============================================================================
    print("2/ Extract the coordinates")
    track = np.column_stack((df['latitude'].values, df['longitude'].values))

    X = df['longitude'].values
    Y = df['latitude'].values

# =============================================================================
#     3/ Plot the graph of the location
# =============================================================================
    print("3/ plot the graph and the track")
  
    graph = rt.graph_from_track(track, network='all')
    
# =============================================================================
#     4/ Algorithm to match the track to closest edge
# =============================================================================
    print("4/ Algorithm to match the track to closest edge")
    # 4.1/ Compute the path
    print("\t4.1/ Compute the route to the closest edge")
    track_nearest, route_nearest, statesid_nearest, stats_nearest = map_matching(graph, Y, X, method='nearest')
    
    # 4.2/ Set the stats
    print("\t4.2/ Let's update the dataframe with the statistics")
    # Set stats indexes same as df
    stats_nearest = stats_nearest.set_index(df.index.values)
    try:
        stats_nearest ['proj_accuracy'] = df['accuracy'].values / stats_nearest['proj_length']
    except KeyError:
        print(KeyError, 'Error computing the projection accuracy')
    print(st.global_stats(stats_nearest).round(2))
    
    # update the dataframe
    df_nearest = pd.concat([df, stats_nearest], axis=1, join='inner')
    df_nearest['longitude'] = track_nearest[:,1]
    df_nearest['latitude'] = track_nearest[:,0]
    df_nearest['edge_id'] = [(states[0], states[1], 0) for states in statesid_nearest]
    df_nearest['osmid'] = [graph.edges[edge_id]['osmid'] for edge_id in df_nearest['edge_id'].values]

    # 4.3/ Visualization Nearest
    print("\t4.3/ Visualization of the nearest routes")
    fig, ax = ox.plot_graph(graph, node_color="skyblue", node_alpha=.5, node_size=15, show=False, close=False, annotate=False) 
    plt.title("Map Matching to the closest edge", color="#999999")
    
    plt.scatter(track[:,1], track[:,0], s=30, marker='.', color="black", zorder=2, label='Original Point')
    plt.plot(track[:,1], track[:,0], linewidth=2, alpha=.7, color="black")
    plt.scatter(track_nearest[:,1], track_nearest[:,0], s=30, marker='.', color="darkcyan", zorder=2, label='Projected Point')
    plt.plot(route_nearest[:,1], route_nearest[:,0], linewidth=2, alpha=.7, color="darkcyan")

    # projection between the two tracks
    lines = [[(track[i,1], track[i,0]), (track_nearest[i,1], track_nearest[i,0])] for i in range(len(track))]
    lc = mc.LineCollection(lines, linestyle='--', colors='skyblue', alpha=1, linewidths=1, zorder=1, label='Projection')
    ax.add_collection(lc)
       
    ax.legend(loc=1, frameon=True, facecolor='w')
    # plt.savefig("map_matching_nearest.png", dpi=600)







