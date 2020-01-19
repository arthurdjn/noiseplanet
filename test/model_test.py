# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 23:19:54 2020

@author: arthurd
"""

import osmnx as ox
import numpy as np

# Visualize the data
import matplotlib.pyplot as plt
from matplotlib import collections as mc

# Test the import
import noiseplanet.matching.model as model



def nearest_test(track):
    
    # Create graph
    graph = model.graph_from_track(track, network='all')
    
    # Compute the path
    track_corr, route_corr, statesid_nearest, stats_nearest = model.match_nearest_edge(graph, track)
   
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


def leuven_test(track):
    # Create graph
    graph = model.graph_from_track(track, network='all')
    
    # Compute the path
    track_corr, route_corr, statesid_nearest, stats_nearest = model.match_leuven(graph, track)
   
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



if __name__ == "__main__":

    track = np.array( [[45.7584882 ,  4.83585996],
           [45.75848068,  4.83586747],
           [45.75849549,  4.83585205],
           [45.75849134,  4.83584647],
           [45.75848135,  4.8358245 ],
           [45.75846756,  4.83580848],
           [45.75846756,  4.83580848],
           [45.75844998,  4.83580936],
           [45.7584067 ,  4.83580086],
           [45.7584067 ,  4.83580086],
           [45.75839346,  4.83579883],
           [45.75835386,  4.83579587],
           [45.75835386,  4.83579587],
           [45.75832859,  4.83578957],
           [45.75831305,  4.83578476],
           [45.75830179,  4.83577988],
           [45.75830179,  4.83577988],
           [45.75828395,  4.8357761 ],
           [45.7582776 ,  4.83578271],
           [45.7582776 ,  4.83578271],
           [45.75826788,  4.83577651],
           [45.75824111,  4.83577318],
           [45.75823187,  4.83577628],
           [45.75823187,  4.83577628],
           [45.75821196,  4.83577348],
           [45.7581896 ,  4.83577665],
           [45.7581896 ,  4.83577665],
           [45.75816541,  4.83579402],
           [45.75815477,  4.83579607],
           [45.75815477,  4.83579607],
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
           [45.7577991 ,  4.83545974],
           [45.7577991 ,  4.83545974],
           [45.75778494,  4.83544537],
           [45.75778018,  4.83542394],
           [45.75778018,  4.83542394],
           [45.75777708,  4.83542095],
           [45.75778355,  4.83537921],
           [45.75778355,  4.83537921],
           [45.75779486,  4.8353652 ],
           [45.75778985,  4.83535578],
           [45.75779875,  4.83534073],
           [45.75779875,  4.83534073],
           [45.75778759,  4.83534048],
           [45.75777132,  4.83530956],
           [45.75777132,  4.83530956],
           [45.75777826,  4.83529123],
           [45.75772724,  4.83526193],
           [45.75772724,  4.83526193],
           [45.75770642,  4.8352539 ],
           [45.75765273,  4.83523469],
           [45.75765273,  4.83523469],
           [45.75763036,  4.8352032 ],
           [45.75760354,  4.83521685],
           [45.75760031,  4.83517866],
           [45.75760031,  4.83517866],
           [45.75760174,  4.83514537],
           [45.75755343,  4.83511274],
           [45.75757394,  4.8350941 ],
           [45.75757394,  4.8350941 ],
           [45.75762054,  4.83503878],
           [45.75769855,  4.83501164],
           [45.75769951,  4.83498337],
           [45.75772904,  4.83492365],
           [45.75771774,  4.83488041],
           [45.75771774,  4.83488041],
           [45.75769201,  4.83486014],
           [45.75765675,  4.83483411],
           [45.75763482,  4.83482225],
           [45.75763482,  4.83482225],
           [45.75763427,  4.83480956],
           [45.75763733,  4.83478114],
           [45.75762267,  4.83474527],
           [45.75762676,  4.83470367],
           [45.7576598 ,  4.83467878],
           [45.7576598 ,  4.83467878],
           [45.75767969,  4.83464587],
           [45.75771624,  4.83461801],
           [45.75774496,  4.83460304],
           [45.75774496,  4.83460304],
           [45.75777047,  4.83460116],
           [45.75783754,  4.83453986],
           [45.75783754,  4.83453986],
           [45.75786403,  4.83448469],
           [45.75789904,  4.83445298],
           [45.75789904,  4.83445298],
           [45.75792369,  4.83443289]])
    
    nearest_test(track)
    
    leuven_test(track)    









