# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 16:41:41 2019

@author: arthurd
"""

# Classic Library
import numpy as np
from pyproj import Geod
import pandas as pd

# Leuven Map Matching algorithm
from leuvenmapmatching.matcher.distance import DistanceMatcher   # map matching
from leuvenmapmatching.map.inmem import InMemMap                 # leuven graph object
# import noiseplanet.matching.model.route as rt


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
    # Stack the stats
    path_length = []
    unlinked = []
    # Compute the route coordinates
    route = []

    for i in range(len(track) - 1):
        if states[i] != states[i+1]:
            route.append(track_corr[i])
            route.append([map_con.graph[states[i][1]][0][0], map_con.graph[states[i][1]][0][1]])
            _, _, distance = geod.inv(track_corr[i][1], track_corr[i][0],
                                      map_con.graph[states[i][1]][0][1], map_con.graph[states[i][1]][0][0])
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
    
    
    stats = pd.DataFrame({"proj_length": proj_dist,
                          "path_length": path_length,
                          "unlinked": unlinked})

    # route, _, stats_route = rt.route_from_track(graph, track_corr)
    # stats = pd.DataFrame(dict({"proj_length": proj_dist}, **stats_route))
    
    return track_corr, np.array(route), states, stats
