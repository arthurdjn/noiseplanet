# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 16:49:20 2019

@author: Utilisateur
"""

# Classic Library
import networkx as nx
import osmnx as ox                         # OSM
import numpy as np
import copy                                # for graph copy
from pyproj import Geod
import pandas as pd




def graph_from_track(track, network='all'):
    """
        Get the OSM network for a given track
        
        :param track: GPS track, containing the coordinates for each points.
                    The latitude is the first index of the coordinates, 
                    followed by the longitude : coord = [lat, lon]
                    Example : track = [[lat1, lon1],
                                       [lat2, lon2],
                                       [lat3, lon3],
                                       ...
                                       [latn, lonn]]
        type track: array like
        :param network: the type of OSM network (drive, all...)
        type network: String
        
        return: the OSM graph
        rtype: networkx.classes.multidigraph.MultiDiGraph
        
        -----------------------------------------------------------------------
        Example :
            >>> track = [[4.8396232, 45.7532804], 
                         [4.839917548464699, 45.75345336404514],
                         [4.828226357067425, 45.747825316200384]]
            >>> graph = graph_from_track(track, network='all')
            >>> graph
                <networkx.classes.multidigraph.MultiDiGraph at 0x155de2260c8>
                
            Then you can visualize the graph, with matplotlib with :
            >>> fig, ax = ox.plot_graph(graph)
            
            See the OSMNX documentation for more details
        -----------------------------------------------------------------------
    """
    lat = track[:, 0]
    lon = track[:, 1]
    graph = ox.graph_from_bbox(
        np.max(lat) + .001, np.min(lat) - 0.001, np.max(lon) + 0.001, np.min(lon) - 0.001,
        simplify=False,
        retain_all=True,
        network_type=network
    )
    return graph




def get_route_from_track(graph, track, states=[]):
    """
        Get the route of the corrected track
        
        :param graph: The OSMNX graph of the area
        type graph: network.classes.multidigraph.MultiDiGraph
        :param track: GPS points (latitudes and longitudes)
        type track: np.array like
        :param states: States refers to the id of the edges linked to the GPS
                projected points
        type states: array like
        
        return: The route, containing position of the track and edges corner
                if there is a turn/change in the direction,
                and the states
        rtype: tuple
                          
    """
    
    # Reference ellipsoid for distance
    geod = Geod(ellps='WGS84')
    
    # Find closest edges for each points
    if len(states) == 0:
        states = np.array(ox.get_nearest_edges(graph, track[:,1], track[:,0],  method="balltree", dist=0.00001))
    states = np.array(states)
    
    # Deep copy of the graph, so the original is not modified
    # This algorithm will add edges and nodes to the graph
    # to compute Dijkstras shortest path
    graph2 = copy.deepcopy(graph)
    
    # adding the projected nodes to the copied graph
    for i in range(len(track)):
        graph2.add_node(i, y=track[i, 0], x=track[i, 1], osmid=i)
                
        _, _, distance1 = geod.inv(track[i, 1], track[i, 0], graph2.nodes[states[i, 0]]['x'], graph2.nodes[states[i, 0]]['y'])
        graph2.add_edge(states[i, 0], i,
                        osmid=2*i, 
                        highway=graph2.edges[(states[i, 0], states[i, 1], 0)]["highway"],
                        oneway=graph2.edges[(states[i, 0], states[i, 1], 0)]["oneway"],
                        length=distance1)
    
        _, _, distance2 = geod.inv(track[i, 1], track[i, 0], graph2.nodes[states[i, 1]]['x'], graph2.nodes[states[i, 1]]['y'])
        graph2.add_edge(states[i, 1], i,
                        osmid=2*i+1, 
                        highway=graph2.edges[(states[i, 0], states[i, 1], 0)]["highway"],
                        oneway=graph2.edges[(states[i, 0], states[i, 1], 0)]["oneway"],
                        length=distance2)
    
    # adding edges in both directions
    for edge in list(graph2.edges):
        graph2.add_edge(edge[1], edge[0], 
                        osmid=graph2.edges[(edge[0], edge[1], 0)]["osmid"]*2, 
                        highway=graph2.edges[(edge[0], edge[1], 0)]["highway"],
                        oneway=graph2.edges[(edge[0], edge[1], 0)]["oneway"],
                        length=graph2.edges[(edge[0], edge[1], 0)]["length"])

    route = []
    path_length = []
    unlinked = []
    for i in range(len(track) - 1):       
        # If there is a changing direction (going from one edge to another,
        # compute Dijkstras algorithm to know what path to follow.
        if states[i][0] != states[i+1][0] or states[i][1] != states[i+1][1]:
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

    stats = pd.DataFrame({"path_length": np.array(path_length), 
                          "unlinked": np.array(unlinked)})
    
    return np.array(route), states, stats



if __name__ == "__main__":
    pass











