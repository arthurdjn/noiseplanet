# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 16:41:02 2019

@author: arthurd
"""

# Classic Library
import osmnx as ox                         # OSM
import numpy as np
from pyproj import Proj, Geod, Transformer
import json
import pandas as pd


# Useful script
import noiseplanet.matching.model.oproj as oproj
import noiseplanet.matching.model.route as rt
import noiseplanet.matching.model.stats as st



def match_nearest_edge(graph, track):
    """
        Algorithm to match the track to the nearest edge

        param graph: graph of the area
        type graph: network.classes.multidigraph.MultiDiGraph
        param track: GPS points (latitudes and longitudes)
        type track: np.array like

        return: GPS points matched to the closest route (latitudes and longitudes),
                the path linking all edgges together,
                the states
        rtype: tuple

        -----------------------------------------------------------------------
        Description :
            This function match a track of GPS coordinates, in the format [lat, lon]
            to a graph.

            It loops all over the points to match them to the closest edge of the
            OSMNX network. The GPS points are projected on the edge with an
            orthogonal projection.
            If the projected point goes outside of the edge, then it is match to
            one extremity (see oproj.py documentation for more details).

            The id of the closest edge is stacked (into the array 'states'), so the
            path from each nodes along edges can be computed.
        -----------------------------------------------------------------------
        Example :
            >>> place_name = "2e Arrondissement, Lyon, France"
            >>> distance = 1000  # meters
            >>> graph = ox.graph_from_address(place_name, distance)
            >>> track = track = [[4.8396232, 45.7532804],
                                 [4.839917548464699, 45.75345336404514],
                                 [4.828226357067425, 45.747825316200384]]
            >>> track_corr, route_corr, states = match_nearest_edge(graph, track)
        -----------------------------------------------------------------------
    """
    # id of the nearest edges
    states = ox.get_nearest_edges(graph, track[:,1], track[:,0],  method='balltree', dist=.000001)
    lat1, lat2, lon1, lon2 = [], [], [], []
    for stateid in states:
        lon1.append(graph.nodes[stateid[0]]['x'])
        lat1.append(graph.nodes[stateid[0]]['y'])
        lon2.append(graph.nodes[stateid[1]]['x'])
        lat2.append(graph.nodes[stateid[1]]['y'])

    # Reference ellipsoid for distance
    # Projection of the point in the web mercator coordinate system (used by OSM)
    proj_init="epsg:4326"       # geographic coordinates
    proj_out="epsg:3857"        # web mercator coordinates
    # Using the class Transformer, faster for large dataset
    transformer = Transformer.from_proj(Proj(init=proj_init), Proj(init=proj_out))
    Xt, Yt = transformer.transform(track[:,1], track[:,0])
    # Projecting the nearest edges' nodes 1, 2 into the same coordinates system
    X1, Y1 = transformer.transform(lon1, lat1)
    X2, Y2 = transformer.transform(lon2, lat2)

    # With the transform function (slower since the 2.2.0 update)
    # Xt, Yt = transform(Proj(init=proj_init), Proj(init=proj_out), track[:,1], track[:,0])
    # X1, Y1 = transform(Proj(init=proj_init), Proj(init=proj_out), lon1, lat1)
    # X2, Y2 = transform(Proj(init=proj_init), Proj(init=proj_out), lon2, lat2)

    # Need to evaluate the projection for each point distance(point, point_proj)
    proj_dist = np.zeros(len(track))
    Xcorr, Ycorr = [], []
    for i in range(len(track)):
        # Ortho projection
        x, y = Xt[i], Yt[i]
        xH, yH = oproj.orthoProjSegment((x, y), (X1[i], Y1[i]), (X2[i], Y2[i]))
        # Stack the coordinates in the web mercator coordinates system
        Xcorr.append(xH)
        Ycorr.append(yH)

    transformer = Transformer.from_proj(Proj(init=proj_out), Proj(init=proj_init))

    lon_corr, lat_corr = transformer.transform(Xcorr, Ycorr)
    # With the transform function (slower since the 2.2.0 update)
    # lon_corr, lat_corr = transform(Proj(init=proj_out), Proj(init=proj_init), Xcorr, Ycorr)

    # Evaluate the distance betweeen these points
    # Reference ellipsoid for distance
    geod = Geod(ellps='WGS84')
    _, _, proj_dist = geod.inv(track[:,1], track[:,0], lon_corr, lat_corr)

    track_corr = np.column_stack((lat_corr, lon_corr))
    route, _, stats_route = rt.get_route_from_track(graph, track_corr)
    stats = pd.DataFrame(dict({"proj_length": proj_dist}, **stats_route))

    return track_corr, route, list(zip(states[:,0], states[:,1])), stats



if __name__ == "__main__":
    # Open tracks
    import noiseplanet.utils.io as io
    # Visualize the data
    import matplotlib.pyplot as plt
    from matplotlib import collections as mc   # for plotting

    
    print("\n\t-----------------------\n",
            "\t    Nearest Matching   \n\n")

# =============================================================================
#     1/ Open the track
# =============================================================================
    print("1/ Open the track")
    print("\t1.1/ Convert in dataframe")
    filename = '../../../data/track/track_105.geojson'
    with open(filename) as f:
        geojson = json.load(f)

    # convert in dataframe
    df = io.geojson_to_df(geojson, extract_coordinates=True)

    print("\t1.2/ Clean the track")
    # Fill None values by interpolation
    try:
        df = df.interpolate(method='quadratic', axis=0)
    except ValueError as e:
        print(e)
        print("The interpolation failed for {0}".format(filename))
    # Delete rows where no positions
    df = df[df['type'].notnull()]

# =============================================================================
#     2/ Extract the coordinates
# =============================================================================
    print("2/ Extract the coordinates")
    track = np.column_stack((df['latitude'].values, df['longitude'].values))

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
    track_nearest, route_nearest, statesid_nearest, stats_nearest = match_nearest_edge(graph, track)
    route_nearest, statesid_nearest2, stats_route_nearest = rt.get_route_from_track(graph, track_nearest)

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
    filename = filename.split("/")[-1].split(".")[0]
    plt.savefig("../../../img/map_matching_nearest_" + filename + ".png", dpi=600)







