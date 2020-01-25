# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 23:19:54 2020

@author: arthurd
"""

import osmnx as ox
import numpy as np
import time

# Visualize the data
import matplotlib.pyplot as plt
from matplotlib import collections as mc

# Test the import
from noiseplanet.matcher import model
from noiseplanet.matcher.model import route




def test_nearest():
    print('Test match_nearest_edge(graph, track)')
    track = np.array( [[45.75815477,  4.83579607],
                       [45.75815501,  4.83578568],
                       [45.75813165,  4.83577836],
                       [45.75811917,  4.83577826],
                       [45.75811917,  4.83577826],
                       [45.75810508,  4.83574771],
                       [45.75807665,  4.83572188],
                       [45.75807665,  4.83572188],
                       [45.75806175,  4.83570647],
                       [45.75805712,  4.8356987 ],
                       [45.75804746,  4.83569629],
                       [45.75803752,  4.83568949],
                       [45.75802591,  4.83566137],
                       [45.75802629,  4.83565147],
                       [45.75802629,  4.83565147],
                       [45.75801363,  4.83562952],
                       [45.75800574,  4.83562477],
                       [45.75800574,  4.83562477],
                       [45.75799968,  4.83560606],
                       [45.75800028,  4.83559067],
                       [45.75800028,  4.83559067],
                       [45.75799686,  4.83558285],
                       [45.75797956,  4.83556543],
                       [45.75797466,  4.83555272],
                       [45.75797466,  4.83555272],
                       [45.75796105,  4.83554806],
                       [45.75793787,  4.83553723],
                       [45.75793787,  4.83553723],
                       [45.75793882,  4.83553601],
                       [45.75792874,  4.83550413],
                       [45.75793143,  4.83549635],
                       [45.75793143,  4.83549635],
                       [45.75791593,  4.83548718],
                       [45.75788795,  4.83546475],
                       [45.75788795,  4.83546475],
                       [45.75786658,  4.83547026],
                       [45.75783632,  4.83546862],
                       [45.75783632,  4.83546862],
                       [45.75782964,  4.83547046],
                       [45.75780487,  4.83546808],
                       [45.7577991 ,  4.83545974]])
    
    # Create graph
    graph = model.graph_from_track(track, network='all')
    
    # Compute the path
    start = time.time()
    track_corr, route_corr, edgeid, stats = model.match_nearest_edge(graph, track)
    print('Map Matching nearest in {0}s'.format(round(time.time() - start, 5)))
    # Visualization Nearest
    fig, ax = ox.plot_graph(graph, node_color="skyblue", node_alpha=.5, node_size=15, show=False, close=False, annotate=False)
    plt.title("Map Matching to the closest edge", color="#999999")
    
    plt.scatter(track[:, 1], track[:, 0], s=30, marker='.', color="black", zorder=2, label='Original Point')
    plt.plot(track[:, 1], track[:, 0], linewidth=2, alpha=.7, color="black")
    plt.scatter(track_corr[:, 1], track_corr[:, 0], s=30, marker='.', color="darkcyan", zorder=2, label='Projected Point')
    plt.plot(route_corr[:, 1], route_corr[:, 0], linewidth=2, alpha=.7, color="darkcyan")
    
    # projection between the two tracks
    lines = [[(track[i, 1], track[i, 0]), (track_corr[i, 1], track_corr[i, 0])] for i in range(len(track))]
    lc = mc.LineCollection(lines, linestyle='--', colors='skyblue', alpha=1, linewidths=1, zorder=1, label='Projection')
    ax.add_collection(lc)
    
    ax.legend(loc=1, frameon=True, facecolor='w')


def test_leuven():
    print('Test match_leuven(graph, track)')
    track = np.array( [[45.75815477,  4.83579607],
                       [45.75815501,  4.83578568],
                       [45.75813165,  4.83577836],
                       [45.75811917,  4.83577826],
                       [45.75811917,  4.83577826],
                       [45.75810508,  4.83574771],
                       [45.75807665,  4.83572188],
                       [45.75807665,  4.83572188],
                       [45.75806175,  4.83570647],
                       [45.75805712,  4.8356987 ],
                       [45.75804746,  4.83569629],
                       [45.75803752,  4.83568949],
                       [45.75802591,  4.83566137],
                       [45.75802629,  4.83565147],
                       [45.75802629,  4.83565147],
                       [45.75801363,  4.83562952],
                       [45.75800574,  4.83562477],
                       [45.75800574,  4.83562477],
                       [45.75799968,  4.83560606],
                       [45.75800028,  4.83559067],
                       [45.75800028,  4.83559067],
                       [45.75799686,  4.83558285],
                       [45.75797956,  4.83556543],
                       [45.75797466,  4.83555272],
                       [45.75797466,  4.83555272],
                       [45.75796105,  4.83554806],
                       [45.75793787,  4.83553723],
                       [45.75793787,  4.83553723],
                       [45.75793882,  4.83553601],
                       [45.75792874,  4.83550413],
                       [45.75793143,  4.83549635],
                       [45.75793143,  4.83549635],
                       [45.75791593,  4.83548718],
                       [45.75788795,  4.83546475],
                       [45.75788795,  4.83546475],
                       [45.75786658,  4.83547026],
                       [45.75783632,  4.83546862],
                       [45.75783632,  4.83546862],
                       [45.75782964,  4.83547046],
                       [45.75780487,  4.83546808],
                       [45.7577991 ,  4.83545974]])

    
    # Create graph
    graph = model.graph_from_track(track, network='all')
    
    # Compute the path
    start = time.time()
    track_corr, route_corr, edgeid, stats = model.match_leuven(graph, track)
    print('Map Matching hmm in {0}s'.format(round(time.time() - start, 5)))
    # Visualization Nearest
    fig, ax = ox.plot_graph(graph, node_color="skyblue", node_alpha=.5, node_size=15, show=False, close=False, annotate=False)
    plt.title("Map Matching to the closest edge", color="#999999")
    
    plt.scatter(track[:, 1], track[:, 0], s=30, marker='.', color="black", zorder=2, label='Original Point')
    plt.plot(track[:, 1], track[:, 0], linewidth=2, alpha=.7, color="black")
    plt.scatter(track_corr[:, 1], track_corr[:, 0], s=30, marker='.', color="darkcyan", zorder=2, label='Projected Point')
    plt.plot(route_corr[:, 1], route_corr[:, 0], linewidth=2, alpha=.7, color="darkcyan")
    
    # projection between the two tracks
    lines = [[(track[i, 1], track[i, 0]), (track_corr[i, 1], track_corr[i, 0])] for i in range(len(track))]
    lc = mc.LineCollection(lines, linestyle='--', colors='skyblue', alpha=1, linewidths=1, zorder=1, label='Projection')
    ax.add_collection(lc)
    
    ax.legend(loc=1, frameon=True, facecolor='w')


def test_route_from_track():
    print('Test route_from_track(track)')
    track = np.array(  [[45.75809136,  4.83577159],
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
                        [45.75802703,  4.83557288],
                        [45.75801895,  4.83556895],
                        [45.75801895,  4.83556895],
                        [45.75800954,  4.83556438],
                        [45.75800681,  4.83556305],
                        [45.75800681,  4.83556305],
                        [45.75800209,  4.83556076],
                        [45.75798288,  4.83555142],
                        [45.75797578,  4.83554797],
                        [45.75797578,  4.83554797],
                        [45.75796259,  4.83554156],
                        [45.7579395 ,  4.83553033],
                        [45.7579395 ,  4.83553033],
                        [45.75794009,  4.83553062],
                        [45.75792429,  4.83552294],
                        [45.75792505,  4.83552331],
                        [45.75792505,  4.83552331],
                        [45.7579092 ,  4.83551561],
                        [45.75787935,  4.8355011 ],
                        [45.75787935,  4.8355011 ],
                        [45.75786135,  4.83549235],
                        [45.75783387,  4.83547899],
                        [45.75783387,  4.83547899],
                        [45.75782827,  4.83547626],
                        [45.75780555,  4.83546522],
                        [45.7577986 ,  4.83546184]])
    
    edgeid = np.array([ [6135818902, 6135818901],
                        [6135818901, 6135818902],
                        [6135818902, 6135818901],
                        [6135818901, 6135818902],
                        [6135818901, 6135818902],
                        [6135818901, 6135818902],
                        [6135818901, 6135818902],
                        [6135818901, 6135818902],
                        [6135818902, 6135818901],
                        [6135818902, 6135818901],
                        [6135818901, 6135818902],
                        [6135818902, 6135818901],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765],
                        [ 192313667, 1777581765]])
    graph = route.graph_from_track(track)
    start = time.time()
    route_corr, stats = route.route_from_track(graph, track, edgeid=None)
    print('Route without edgeid computed in : {0}s'.format(round(time.time() - start, 5)))
    start = time.time()
    route_corr, stats = route.route_from_track(graph, track, edgeid=edgeid)
    print('Route with edgeid computed in : {0}s'.format(round(time.time() - start, 5)))
    
    # Visualization leuven - Leuven Map Matching
    fig, ax = ox.plot_graph(graph, node_color="skyblue", node_alpha=.5, node_size=15, show=False, close=False, annotate=False)
    plt.title("Map Matching with Viterbi's algorithm (leuven)", color="#999999")
    plt.scatter(track[:, 1], track[:, 0], s=30, marker='.', color="darkcyan", zorder=2, label='Original Point')
    plt.plot(route_corr[:, 1], route_corr[:, 0], linewidth=2, alpha=.7, color="darkcyan")
    


if __name__ == "__main__":

    # Testing the different method of Map Matching
    test_nearest()
    test_leuven()    

    # Testing route functions
    test_route_from_track()

    





