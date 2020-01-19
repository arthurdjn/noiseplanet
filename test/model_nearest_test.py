# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 23:19:54 2020

@author: arthurd
"""

import json
import osmnx as ox
import pandas as pd
import numpy as np

# Visualize the data
import matplotlib.pyplot as plt
from matplotlib import collections as mc   # for plotting

# Open tracks
import noiseplanet.utils.io as io
import noiseplanet.matching.model.route as rt
import noiseplanet.matching.model.stats as st
from noiseplanet.matching.model.nearest import match_nearest_edge

print("\n\t-----------------------\n",
        "\t    Nearest Matching   \n\n")

# =============================================================================
#     1/ Open the track
# =============================================================================
print("1/ Open the track")
print("\t1.1/ Convert in dataframe")
filename = 'data/track/track_1.geojson'
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
plt.savefig("img/map_matching_nearest_" + filename + ".png", dpi=600)



