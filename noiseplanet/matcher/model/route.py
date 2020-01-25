# -*- coding: utf-8 -*-

# Created on Tue Dec 24 16:49:20 2019

# @author: arthurd

"""
Route Module.

Track - OSM network interactions.
"""

# Classic Library
import networkx as nx
import osmnx as ox                         # OSM
import numpy as np
import copy                                # for graph copy
from pyproj import Geod




def graph_from_track(track, network='all'):
    """
    Get the OSM network for a given track.

    Parameters
    ----------
    track : numpy 2D array
        A 2D matrix composed by Latitudes (first column) and Longitudes (second column)
        of the track.
    network : String
        Network type extracted from the Open Street Map DataBase ('drive', 'pedestrian', 'all', etc.
        The default is 'all'.

    Returns
    -------
    graph : NetworkX MultiDiGraph
        Open Street Map graph of the track area.
        
    Example
    -------
        >>> import numpy as np
        >>> from noiseplanet.matcher.model.route import graph_from_track
        >>> track = np.array([[4.8396232, 45.7532804], 
                              [4.839917548464699, 45.75345336404514],
                              [4.828226357067425, 45.747825316200384]])
        >>> graph = graph_from_track(track, network='all')
        >>> graph
            <networkx.classes.multidigraph.MultiDiGraph at 0x155de2260c8>
        # Then you can visualize the graph, with matplotlib with :
        >>> import osmnx as ox
        >>> fig, ax = ox.plot_graph(graph)
        # See the OSMNX documentation for more details
    """
    lat = track[:, 0]
    lon = track[:, 1]
    graph = ox.graph_from_bbox(
                            np.max(lat) + .001, np.min(lat) - 0.001, 
                            np.max(lon) + .001, np.min(lon) - 0.001,
                            simplify=False,
                            retain_all=True,
                            network_type=network)
    return graph




def route_from_track(graph, track, edgeid=None):
    """
    Get the route connecting points of a track projected on the Open Street Map
    network.

    Parameters
    ----------
    graph : NetworkX MultiDiGraph
        Open Street Map graph where the route will be computed.
    track : numpy 2D array
        A 2D matrix composed by Latitudes (first column) and Longitudes (second column)
        of the track.    
    edgeid : numpy 2D array, optional
        List of edges to which each points belongs to.
        Edges id are composed by two extremity nodes id. 
        The default is None.

    Returns
    -------
    route : numpy 2D array
        Route connecting all track's points.
    stats : Dict
        Statistics of the routing connection.
        'path_length' is the distance on the graph between two following points,
        'unlinked' higlights unconnected points on the graph.
        
    Example
    -------
        >>> import numpy as np
        >>> from noiseplanet.matcher.model.route import route_from_track, graph_from_track
        >>> track = np.array([[45.75809136,  4.83577159],
                              [45.7580932 ,  4.83576182],
                              [45.7580929 ,  4.8357634 ],
                              [45.75809207,  4.8357678 ],
                              [45.75809207,  4.8357678 ],
                              [45.75809647,  4.83574439],
                              [45.75809908,  4.83573054],
                              [45.75809908,  4.83573054],
                              [45.75810077,  4.83572153],
                              [45.75810182,  4.83571596]])
        >>> graph = graph_from_track(track, network='all')
        >>> route_corr, stats = route_from_track(graph, track)
    """
                     
    # Reference ellipsoid for distance
    geod = Geod(ellps='WGS84')
    
    # Find closest edges for each points
    if edgeid is None:
        edgeid = np.array(ox.get_nearest_edges(graph, track[:, 1], track[:, 0],  method="balltree", dist=0.00001))
    edgeid = np.array(edgeid)
    
    # Deep copy of the graph, so the original is not modified
    # This algorithm will add edges and nodes to the graph
    # to compute Dijkstras shortest path
    graph2 = copy.deepcopy(graph)
    
    # adding the projected nodes to the copied graph
    for i in range(len(track)):
        graph2.add_node(i, y=track[i, 0], x=track[i, 1], osmid=i)
                
        _, _, distance1 = geod.inv(track[i, 1], track[i, 0], graph2.nodes[edgeid[i, 0]]['x'], graph2.nodes[edgeid[i, 0]]['y'])
        graph2.add_edge(edgeid[i, 0], i,
                        osmid=2*i, 
                        highway=graph2.edges[(edgeid[i, 0], edgeid[i, 1], 0)]["highway"],
                        oneway=graph2.edges[(edgeid[i, 0], edgeid[i, 1], 0)]["oneway"],
                        length=distance1)
    
        _, _, distance2 = geod.inv(track[i, 1], track[i, 0], graph2.nodes[edgeid[i, 1]]['x'], graph2.nodes[edgeid[i, 1]]['y'])
        graph2.add_edge(edgeid[i, 1], i,
                        osmid=2*i+1, 
                        highway=graph2.edges[(edgeid[i, 0], edgeid[i, 1], 0)]["highway"],
                        oneway=graph2.edges[(edgeid[i, 0], edgeid[i, 1], 0)]["oneway"],
                        length=distance2)
    
    # adding edges in both directions
    # for edge in list(graph2.edges):
    #     graph2.add_edge(edge[1], edge[0], 
    #                     osmid=graph2.edges[(edge[0], edge[1], 0)]["osmid"]*2, 
    #                     highway=graph2.edges[(edge[0], edge[1], 0)]["highway"],
    #                     oneway=graph2.edges[(edge[0], edge[1], 0)]["oneway"],
    #                     length=graph2.edges[(edge[0], edge[1], 0)]["length"])
    graph2 = graph2.to_undirected()

    route = []
    path_length = []
    unlinked = []
    for i in range(len(track) - 1):       
        # If there is a changing direction (going from one edge to another,
        # compute Dijkstras algorithm to know what path to follow.
        if edgeid[i][0] != edgeid[i+1][0] or edgeid[i][1] != edgeid[i+1][1]:
            # If the two nodes are connected
            try:
                path = nx.shortest_path(graph2, i, i+1, weight='length')
                distance = nx.shortest_path_length(graph2, i, i+1, weight='length')
                path_length.append(distance)
                unlinked.append(0)
                for nodeid in path:
                    route.append([graph2.nodes[nodeid]["y"], graph2.nodes[nodeid]["x"]])
            
            # If they are not connected, there is a mismatched
            except nx.NetworkXNoPath:
                route.append(track[i])
                _, _, distance = geod.inv(track[i, 1], track[i, 0], track[i+1, 1], track[i+1, 0])
                path_length.append(distance)
                unlinked.append(1)
        
        # If the route is already matched
        else:
            route.append(track[i])
            _, _, distance = geod.inv(track[i, 1], track[i, 0], track[i+1, 1], track[i+1, 0])
            path_length.append(distance)
            unlinked.append(0)
 
    # Let's not forget to add the last point
    route.append(track[-1])
    unlinked.append(0)     
    path_length.append(0)

    stats = {"path_length": np.array(path_length), 
             "unlinked": np.array(unlinked)}
    
    return np.array(route), stats


