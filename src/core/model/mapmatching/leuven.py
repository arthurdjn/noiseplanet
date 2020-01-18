# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 16:41:41 2019

@author: Utilisateur
"""

# Classic Library
import osmnx as ox                         # OSM
import numpy as np
from pyproj import Geod
import json
import pandas as pd

# Leuven Map Matching algorithm
from leuvenmapmatching.matcher.distance import DistanceMatcher   # map matching
from leuvenmapmatching.map.inmem import InMemMap                 # leuven graph object

# Useful script
import src.core.model.mapmatching.route as rt
import src.core.model.stats as st


def match_leuven(graph, track):
    """
        Algorithm to match the track to the most probable route
            Use Leuven Map Matching algo.
            See the docs : https://leuvenmapmatching.readthedocs.io/en/latest/index.html

        :param graph: graph of the area
        type graph: network.classes.multidigraph.MultiDiGraph
        :param track: GPS points (latitudes and longitudes)
        type track: np.array like
        :param get_route: Compute the route during the matching
                (faster than computing again the route)
        type get_route: boolean
        return: GPS points matched to the closest route (latitudes and longitudes),
                the path linking all edgges together,
                the states
        rtype: tuple

        -----------------------------------------------------------------------
        Description :
            Leuven Map matching algorithm,
            Copyright 2015-2018, KU Leuven - DTAI Research Group, Sirris - Elucidata Group.

            leuven with non-emitting states (offline) for Map Matching.
        -----------------------------------------------------------------------
        Example :
            >>> place_name = "2e Arrondissement, Lyon, France"
            >>> distance = 1000  # meters
            >>> graph = ox.graph_from_address(place_name, distance)
            >>> track = track = [[4.8396232, 45.7532804],
                                 [4.839917548464699, 45.75345336404514],
                                 [4.828226357067425, 45.747825316200384]]
            >>> track_corr, route_corr, states = match_leuven(graph, track)
            >>> track_corr

            >>> route

            >>> states

        -----------------------------------------------------------------------
    """

    # Reference ellipsoid for distance
    geod = Geod(ellps='WGS84')

    # Creation of the Leuven Map object from the OSM network
    path = [(track[i][0], track[i][1]) for i in range(len(track))]

    map_con = InMemMap("myosm", use_latlon=True, use_rtree=True, index_edges=True)
    nodes_id = list(graph.nodes)
    for node in nodes_id:
        lat = graph.nodes[node]['y']
        lon = graph.nodes[node]['x']
        map_con.add_node(node, (lat, lon))

    edges_id = list(graph.edges)
    for edge in edges_id:
        node_a, node_b = edge[0], edge[1]
        map_con.add_edge(node_a, node_b)
        map_con.add_edge(node_b, node_a)

    map_con.purge()

    matcher = DistanceMatcher(map_con,
                             max_dist=200, max_dist_init=100,  # meter
                             min_prob_norm=0.001,
                             non_emitting_length_factor=0.75,
                             obs_noise=50, obs_noise_ne=75,  # meter
                             dist_noise=50,  # meter
                             non_emitting_states=False)
    states, lastidx = matcher.match(path)


    proj_dist = np.zeros(len(track))

    # States refers to edges id (node1_id, node2_id) where the GPS point is projected
    lat_corr, lon_corr = [], []
    lat_nodes = matcher.lattice_best
    for idx, m in enumerate(lat_nodes):
        lat, lon = m.edge_m.pi[:2]
        lat_corr.append(lat)
        lon_corr.append(lon)

        _, _, distance = geod.inv(track[idx][1], track[idx][0], lon, lat)
        proj_dist[idx] += distance

    track_corr = np.column_stack((lat_corr, lon_corr))

    # # Stack the stats
    # path_length = []
    # unlinked = []
    # # Compute the route coordinates
    # route = []

    # for i in range(len(track) - 1):
    #     if states[i] != states[i+1]:
    #         route.append(track_corr[i])
    #         route.append([map_con.graph[states[i][1]][0][0], map_con.graph[states[i][1]][0][1]])
    #         _, _, distance = geod.inv(track_corr[i][1], track_corr[i][0],
    #                                   map_con.graph[states[i][1]][0][1], map_con.graph[states[i][1]][0][0])
    #         path_length.append(distance)
    #         unlinked.append(0)

    #     else:
    #         route.append(track_corr[i])
    #         _, _, distance = geod.inv(track_corr[i][1], track_corr[i][0],
    #                                   track_corr[i+1][1], track_corr[i+1][0])
    #         path_length.append(distance)
    #         unlinked.append(0)
    # # Let's not forget the last point
    # route.append(track_corr[-1])
    # path_length.append(0)
    # unlinked.append(0)
    
    
    # stats = pd.DataFrame({"proj_length": proj_dist,
    #                       "path_length": path_length,
    #                       "unlinked": unlinked})

    route, _, stats_route = rt.get_route_from_track(graph, track_corr)
    stats = pd.DataFrame(dict({"proj_length": proj_dist}, **stats_route))
    
    return track_corr, np.array(route), states, stats





if __name__ == "__main__":
    # Open tracks
    import src.utils.io as io
    # Visualize the data
    import matplotlib.pyplot as plt
    from matplotlib import collections as mc   # for plotting
    
    print("\n\t-----------------------\n",
            "\t      Map Matching     \n\n")



# =============================================================================
#     1/ Open the track
# =============================================================================
    print("1/ Open the track")
    print("\t1.1/ Convert in dataframe")
    
    filename = '../../../../data/track/track_1.geojson'
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
#     4/ map matching leuven - Viterbi Algorithm
# =============================================================================
    print("4/ map matching leuven - Viterbi Algorithm")
    # 4.1/ leuven algo
    print("\t4.1/ Compute the route with the Viterbi (leuven) algorithm")
    track_leuven, route_leuven, statesid_leuven, stats_leuven = match_leuven(graph, track)
    route_leuven2, statesid_leuven2, stats_route_leuven = rt.get_route_from_track(graph, track_leuven)

    # 4.2/ Stats
    print("\t4.2/ Let's update the dataframe with the statistics")
    # Set stats indexes same as df
    stats_leuven = stats_leuven.set_index(df.index.values)
    try:
        stats_leuven['proj_accuracy'] = df['accuracy'].values / stats_leuven['proj_length']
    except KeyError as e:
        print(e, 'Error computing the projection accuracy')
    print(st.global_stats(stats_leuven).round(2))

    df_leuven = pd.concat([df, stats_leuven], axis=1, join='inner')
    df_leuven['longitude'] = track_leuven[:,1]
    df_leuven['latitude'] = track_leuven[:,0]
    df_leuven['edge_id'] = [(states[0], states[1], 0) for states in statesid_leuven]

    # 5.3/ Visualization leuven - Leuven Map Matching
    print("\t5.3/ Visualization of the map matching")
    fig, ax = ox.plot_graph(graph, node_color="skyblue", node_alpha=.5, node_size=15, show=False, close=False, annotate=True)
    plt.title("Map Matching with Viterbi's algorithm (leuven)", color="#999999")

    plt.scatter(track[:,1], track[:,0], s=30, marker='.', color="black", zorder=2, label='Original Point')
    plt.plot(track[:,1], track[:,0], linewidth=2, alpha=.7, color="black")
    plt.scatter(track_leuven[:,1], track_leuven[:,0], s=30, marker='.', color="darkcyan", zorder=2, label='Projected Point')
    plt.plot(route_leuven[:,1], route_leuven[:,0], linewidth=2, alpha=.7, color="darkcyan")

    # projection between the two tracks
    lines = [[(track[i,1], track[i,0]), (track_leuven[i,1], track_leuven[i,0])] for i in range(len(track))]
    lc = mc.LineCollection(lines, linestyle='--', colors='skyblue', alpha=1, linewidths=1, zorder=1, label='Projection')
    ax.add_collection(lc)

    ax.legend(loc=1, frameon=True, facecolor='w')
    # plt.savefig("../../../img/map_matching_leuven.png", dpi=600)













