# -*- coding: utf-8 -*-

# Created on Tue Dec 24 16:49:20 2019

# @author: arthurd

"""
Nearest Module.

Map Matching to the nearest edge.
"""

# Classic Library
import osmnx as ox
import numpy as np
from pyproj import Proj, Geod, Transformer

# Useful script
from noiseplanet.utils import oproj
import noiseplanet.matching.model.route as rt


def match_nearest_edge(graph, track):
    """
    Algorithm to match the track to the nearest edge on the Open Street Map network.

    This function match a track of GPS coordinates, in the (Lat, Lon) format.
    to a graph.

    It loops all over the points to match them to the closest edge of the
    OSM network. The GPS points are projected on the edge with an
    orthogonal projection.
    If the projected point goes outside of the edge, then it is match to
    one extremity (see noiseplanet.utils.oproj documentation for more details).

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
        Route connecting all track's points on the Open Street Map network.
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
        >>> from noiseplanet.matching.model.leuven import leuven
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
        >>> track_corr, route_corr, edgeid = match_nearest(graph, track)
    """
    # id of the nearest edges
    edgeid = ox.get_nearest_edges(graph, track[:,1], track[:,0],  method='balltree', dist=.000001)
    lat1, lat2, lon1, lon2 = [], [], [], []
    for edge in edgeid:
        lon1.append(graph.nodes[edge[0]]['x'])
        lat1.append(graph.nodes[edge[0]]['y'])
        lon2.append(graph.nodes[edge[1]]['x'])
        lat2.append(graph.nodes[edge[1]]['y'])

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
    route, stats_route = rt.route_from_track(graph, track_corr, edgeid=edgeid)
    stats = dict({"proj_length": proj_dist}, **stats_route)
    
    return track_corr, route, np.array(edgeid), stats





