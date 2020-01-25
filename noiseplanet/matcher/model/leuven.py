# -*- coding: utf-8 -*-

# Created on Tue Dec 24 16:49:20 2019

# @author: arthurd

"""
Leuven Module.
Map Matching from Leuven algorithm.
"""

# Classic Library
import numpy as np
from pyproj import Geod

# Leuven Map Matching algorithm
from leuvenmapmatching.matcher.distance import DistanceMatcher   # map matching
from leuvenmapmatching.map.inmem import InMemMap                 # leuven graph object


def match_leuven(graph, track):
    """
     Algorithm to match the track to the most probable route.
     
     Rely on Leuven Map Matching package.
     Copyright 2015-2018, KU Leuven - DTAI Research Group, Sirris - Elucidata Group.
     See the docs : https://leuvenmapmatching.readthedocs.io/en/latest/index.html
     
     If you want custom Distance Matcher, then change 'matcher' on this function.
     
    Parameters
    ----------
    graph : NetworkX MultiDiGraph
        Graph of the Open Street Map network.
    track : numpy 2D array
        A 2D matrix composed by Latitudes (first column) and Longitudes (second column)
        of the track.

    Returns
    -------
    track_corr : numpy 2D array
        A 2D matrix composed by Latitudes (first column) and Longitudes (second column)
        of the corrected track.
    route : numpy 2D array
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

    Example
    -------
        >>> import osmnx as ox
        >>> import numpy as np
        >>> from noiseplanet.matcher.model.leuven import match_leuven
        >>> place_name = "2e Arrondissement, Lyon, France"
        >>> distance = 1000  # meters
        >>> graph = ox.graph_from_address(place_name, distance)
        >>> track = np.array([[45.75809136,  4.83577159],
                              [45.7580932 ,  4.83576182],
                              [45.7580929 ,  4.8357634 ],
                              [45.75809207,  4.8357678 ],
                              [45.75809207,  4.8357678 ],
                              [45.75809647,  4.83574439],
                              [45.75809908,  4.83573054],
                              [45.75809908,  4.83573054],
                              [45.75810077,  4.83572153],
                              [45.75810182,  4.83571596],
                              [45.75810159,  4.83571719],
                              [45.7581021 ,  4.83571442],
                              [45.7580448 ,  4.83558152],
                              [45.75804304,  4.83558066],
                              [45.75804304,  4.83558066],
                              [45.75802703,  4.83557288]])
        >>> track_corr, route_corr, edgeid = match_leuven(graph, track)
    """

    # Reference ellipsoid for distance
    geod = Geod(ellps='WGS84')
    
    # path is a list of tuples (lat, lon)
    path = list(zip(track[:, 0], track[:, 1]))
    
    # Creation of the Leuven Map object from the OSM network
    map_con = InMemMap("myosm", use_latlon=True, use_rtree=True, index_edges=True)
    # Add the OSM network into the Leuven Map object
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
    
    # Matching parameters
    matcher = DistanceMatcher(map_con,
                             max_dist=200, max_dist_init=100,  # meter
                             min_prob_norm=0.001,
                             non_emitting_length_factor=0.75,
                             obs_noise=50, obs_noise_ne=75,  # meter
                             dist_noise=50,  # meter
                             non_emitting_edgeid=False)
    edgeid, lastidx = matcher.match(path)

    proj_dist = np.zeros(len(track))

    # edgeid refers to edges id (node1_id, node2_id) where the GPS point is projected
    lat_corr, lon_corr = [], []
    lat_nodes = matcher.lattice_best
    for idx, m in enumerate(lat_nodes):
        lat, lon = m.edge_m.pi[:2]
        lat_corr.append(lat)
        lon_corr.append(lon)

        _, _, distance = geod.inv(track[idx][1], track[idx][0], lon, lat)
        proj_dist[idx] += distance

    track_corr = np.column_stack((lat_corr, lon_corr))
    # Stack the stats
    path_length = []
    unlinked = []
    # Compute the route coordinates
    route = []

    for i in range(len(track) - 1):
        if edgeid[i] != edgeid[i+1]:
            route.append(track_corr[i])
            route.append([map_con.graph[edgeid[i][1]][0][0], map_con.graph[edgeid[i][1]][0][1]])
            _, _, distance = geod.inv(track_corr[i][1], track_corr[i][0],
                                      map_con.graph[edgeid[i][1]][0][1], map_con.graph[edgeid[i][1]][0][0])
            path_length.append(distance)
            unlinked.append(0)

        else:
            route.append(track_corr[i])
            _, _, distance = geod.inv(track_corr[i][1], track_corr[i][0],
                                      track_corr[i+1][1], track_corr[i+1][0])
            path_length.append(distance)
            unlinked.append(0)
    # Let's not forget the last point
    route.append(track_corr[-1])
    path_length.append(0)
    unlinked.append(0)
    
    
    stats = {"proj_length": proj_dist,
             "path_length": path_length,
             "unlinked": unlinked}

    # route, stats_route = route_from_track(graph, track_corr)
    # stats = pd.DataFrame(dict({"proj_length": proj_dist}, **stats_route))
    
    return track_corr, np.array(route), np.array(edgeid), stats
