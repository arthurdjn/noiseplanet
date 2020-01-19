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
from noiseplanet.matching.model.leuven import match_leuven

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
fig, ax = ox.plot_graph(graph, node_color="skyblue", node_alpha=.5, node_size=15, show=False, close=False, annotate=False)
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

filename = filename.split("/")[-1].split(".")[0]
plt.savefig("img/map_matching_hmm_" + filename + ".png", dpi=600)


