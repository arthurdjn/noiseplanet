# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 16:41:02 2019

@author: arthurd
"""

# Classic Library
import osmnx as ox
import numpy as np
from pyproj import Proj, Geod, Transformer
import pandas as pd


# Useful script
from noiseplanet.utils import oproj
import noiseplanet.matching.model.route as rt


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
    route, _, stats_route = rt.route_from_track(graph, track_corr)
    stats = pd.DataFrame(dict({"proj_length": proj_dist}, **stats_route))

    return track_corr, route, list(zip(states[:,0], states[:,1])), stats





